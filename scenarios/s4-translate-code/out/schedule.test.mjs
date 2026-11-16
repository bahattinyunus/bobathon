import { test, describe } from "node:test";
import assert from "node:assert/strict";

import {
  ScheduleError,
  Session,
  Time,
  findConflicts,
  formatSession,
  minutesUntil,
  nextSession,
  parseDay,
  parseSchedule,
  parseTime,
  weeklyMinutes,
} from "./schedule.mjs";

const SAMPLE = `
day,start,end,course,room
Mon,09:00,10:50,CS201,eng-b204
Wed,09:00,10:50,CS201,ENG-B204
Mon,13:00,14:50,MATH203,SCI-202
Fri,14:00,15:50,HUM101,INO-AUD
`.trim().split("\n");

// 1 March 2027 is a Monday (month is 0-based in JS: 2 is March)
const MONDAY = new Date(2027, 2, 1, 0, 0, 0, 0);

function cloneDateWithTime(baseDate, hours, minutes = 0, seconds = 0) {
  const d = new Date(baseDate.getTime());
  d.setHours(hours, minutes, seconds, 0);
  return d;
}

describe("ParseTest", () => {
  test("test_sorted_by_day_then_time", () => {
    const s = parseSchedule(SAMPLE);
    assert.deepEqual(
      s.map(x => [x.course, x.day]),
      [["CS201", 0], ["MATH203", 0], ["CS201", 2], ["HUM101", 4]]
    );
  });

  test("test_room_upper_cased", () => {
    assert.equal(parseSchedule(SAMPLE)[0].room, "ENG-B204");
  });

  test("test_comments_and_blank_lines", () => {
    const lines = ["# my schedule", "", SAMPLE[0], "  ", SAMPLE[1]];
    assert.equal(parseSchedule(lines).length, 1);
  });

  test("test_parse_time", () => {
    const t = parseTime("9:05");
    assert.equal(t.hour, 9);
    assert.equal(t.minute, 5);
    for (const bad of ["24:00", "09:5", "9h05", "", "12:60", "1²:00", "-1:00"]) {
      assert.throws(
        () => parseTime(bad),
        ScheduleError,
        `Expected ScheduleError for bad time: ${bad}`
      );
    }
  });

  test("test_error_reports_real_line_number", () => {
    const lines = ["# comment", SAMPLE[0], "Mon,10:00,09:00,X,R"];
    assert.throws(
      () => parseSchedule(lines),
      /^ScheduleError: line 3: end time/
    );
  });

  test("test_bad_day", () => {
    assert.throws(
      () => parseSchedule([SAMPLE[0], "Pzt,09:00,10:00,X,R"]),
      /line 2: invalid day 'Pzt'/
    );
  });

  test("test_missing_column", () => {
    assert.throws(
      () => parseSchedule(["day,start,end,course", "Mon,09:00,10:00,X"]),
      /missing column/
    );
  });

  test("test_wrong_field_count", () => {
    assert.throws(
      () => parseSchedule([SAMPLE[0], "Mon,09:00,10:00,X"]),
      /expected 5 fields, got 4/
    );
  });

  test("test_quoted_course_with_comma", () => {
    const s = parseSchedule([SAMPLE[0], 'Tue,10:00,11:50,"CS203 Computer Organization, Section 2",ENG-A101']);
    assert.equal(s[0].course, "CS203 Computer Organization, Section 2");
  });

  test("test_day_names_case_insensitive", () => {
    const s = parseSchedule([SAMPLE[0], "THURSDAY,11:00,12:50,PHYS102,SCI-110"]);
    assert.equal(s[0].day, 3);
  });

  test("test_empty", () => {
    assert.deepEqual(parseSchedule([]), []);
  });
});

describe("NextSessionTest", () => {
  const s = parseSchedule(SAMPLE);

  test("test_later_same_day", () => {
    const now = cloneDateWithTime(MONDAY, 9, 30);
    const [session, when] = nextSession(s, now);
    assert.equal(session.course, "MATH203");
    assert.equal(when.getTime(), cloneDateWithTime(MONDAY, 13, 0).getTime());
  });

  test("test_exact_start_time_is_not_next", () => {
    const now = cloneDateWithTime(MONDAY, 13, 0);
    const [session] = nextSession(s, now);
    assert.equal(session.course, "CS201"); // Wednesday
  });

  test("test_wraps_to_next_week", () => {
    const saturday = new Date(2027, 2, 6, 12, 0, 0, 0);
    const [session, when] = nextSession(s, saturday);
    const expected = new Date(2027, 2, 8, 9, 0, 0, 0);
    assert.equal(when.getTime(), expected.getTime());
  });

  test("test_empty_schedule", () => {
    assert.equal(nextSession([], MONDAY), null);
  });

  test("test_minutes_until_rounds_up", () => {
    assert.equal(minutesUntil(MONDAY, cloneDateWithTime(MONDAY, 0, 0, 1)), 1);
    assert.equal(minutesUntil(MONDAY, cloneDateWithTime(MONDAY, 0, 2, 0)), 2);
    assert.equal(minutesUntil(cloneDateWithTime(MONDAY, 0, 5, 0), MONDAY), 0);
  });
});

describe("ReportsTest", () => {
  test("test_conflicts", () => {
    const s = parseSchedule([...SAMPLE, "Mon,10:00,11:00,LAB,ENG-A214"]);
    const pairs = findConflicts(s).map(([a, b]) => [a.course, b.course]);
    assert.deepEqual(pairs, [["CS201", "LAB"]]);
  });

  test("test_back_to_back_is_not_conflict", () => {
    const s = parseSchedule([...SAMPLE, "Mon,10:50,11:30,LAB,ENG-A214"]);
    assert.deepEqual(findConflicts(s), []);
  });

  test("test_weekly_minutes_keeps_first_appearance_order", () => {
    const map = weeklyMinutes(parseSchedule(SAMPLE));
    assert.deepEqual(Array.from(map.entries()), [
      ["CS201", 220],
      ["MATH203", 110],
      ["HUM101", 110],
    ]);
  });

  test("test_format", () => {
    const s = new Session("CS201", 2, new Time(9, 0), new Time(10, 50), "ENG-B204");
    assert.equal(formatSession(s), "Wed 09:00-10:50 CS201 @ ENG-B204");
  });
});
