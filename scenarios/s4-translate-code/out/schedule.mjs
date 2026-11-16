// PY: Port of app/campusroute/schedule.py to JavaScript (Node 18+ ES module)

export const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const DAY_ALIASES = {
  "mon": 0, "monday": 0,
  "tue": 1, "tues": 1, "tuesday": 1,
  "wed": 2, "wednesday": 2,
  "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
  "fri": 4, "friday": 4,
  "sat": 5, "saturday": 5,
  "sun": 6, "sunday": 6,
};

export const REQUIRED_COLUMNS = ["day", "start", "end", "course", "room"];

export class ScheduleError extends Error {
  constructor(message) {
    super(message);
    this.name = "ScheduleError";
  }
}

export class Time {
  constructor(hour, minute) {
    this.hour = hour;
    this.minute = minute;
  }

  compareTo(other) {
    if (this.hour !== other.hour) return this.hour - other.hour;
    return this.minute - other.minute;
  }

  toISOString() {
    const hh = String(this.hour).padStart(2, "0");
    const mm = String(this.minute).padStart(2, "0");
    return `${hh}:${mm}`;
  }

  toString() {
    return this.toISOString();
  }
}

export class Session {
  constructor(course, day, start, end, room) {
    this.course = course;
    this.day = day;
    this.start = start;
    this.end = end;
    this.room = room;
  }

  get minutes() {
    return (this.end.hour * 60 + this.end.minute) - (this.start.hour * 60 + this.start.minute);
  }

  overlaps(other) {
    return (
      this.day === other.day &&
      this.start.compareTo(other.end) < 0 &&
      other.start.compareTo(this.end) < 0
    );
  }
}

export function parseTime(text) {
  const raw = (text || "").trim();
  const parts = raw.split(":");
  // PY: isascii() and isdigit(): check ASCII digits only
  if (parts.length !== 2 || !parts.every(p => /^\d+$/.test(p)) || parts[1].length !== 2) {
    throw new ScheduleError(`invalid time '${text}' (expected HH:MM)`);
  }
  const hour = parseInt(parts[0], 10);
  const minute = parseInt(parts[1], 10);
  if (!(hour >= 0 && hour <= 23 && minute >= 0 && minute <= 59)) {
    throw new ScheduleError(`invalid time '${text}' (out of range)`);
  }
  return new Time(hour, minute);
}

export function parseDay(text) {
  const key = (text || "").trim().toLowerCase();
  if (!(key in DAY_ALIASES)) {
    throw new ScheduleError(`invalid day '${text}'`);
  }
  return DAY_ALIASES[key];
}

// PY: csv.reader handling quoted fields with commas
function parseCSVLine(line) {
  const fields = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"') {
        if (i + 1 < line.length && line[i + 1] === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        current += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ',') {
        fields.push(current);
        current = "";
      } else {
        current += ch;
      }
    }
  }
  fields.push(current);
  return fields;
}

export function parseSchedule(lines) {
  const numbered = [];
  let lineIdx = 1;
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !line.trimStart().startsWith("#")) {
      numbered.push({ lineNo: lineIdx, line });
    }
    lineIdx++;
  }

  if (numbered.length === 0) {
    return [];
  }

  const header = parseCSVLine(numbered[0].line).map(h => h.trim().toLowerCase());
  const missing = REQUIRED_COLUMNS.filter(c => !header.includes(c));
  if (missing.length > 0) {
    throw new ScheduleError(`missing column(s): ${missing.join(", ")}`);
  }

  const sessions = [];
  for (let i = 1; i < numbered.length; i++) {
    const { lineNo, line } = numbered[i];
    const row = parseCSVLine(line);
    if (row.length !== header.length) {
      throw new ScheduleError(`line ${lineNo}: expected ${header.length} fields, got ${row.length}`);
    }
    const rec = {};
    for (let j = 0; j < header.length; j++) {
      rec[header[j]] = row[j].trim();
    }

    let session;
    try {
      session = new Session(
        rec["course"],
        parseDay(rec["day"]),
        parseTime(rec["start"]),
        parseTime(rec["end"]),
        rec["room"].toUpperCase()
      );
    } catch (err) {
      if (err instanceof ScheduleError) {
        throw new ScheduleError(`line ${lineNo}: ${err.message}`);
      }
      throw err;
    }

    if (!session.course) {
      throw new ScheduleError(`line ${lineNo}: course is empty`);
    }
    if (session.end.compareTo(session.start) <= 0) {
      throw new ScheduleError(`line ${lineNo}: end time must be after start time`);
    }
    sessions.push(session);
  }

  // PY: Sort by (day, start, course)
  sessions.sort((a, b) => {
    if (a.day !== b.day) return a.day - b.day;
    const timeDiff = a.start.compareTo(b.start);
    if (timeDiff !== 0) return timeDiff;
    return a.course.localeCompare(b.course);
  });

  return sessions;
}

export function findConflicts(sessions) {
  const ordered = [...sessions].sort((a, b) => {
    if (a.day !== b.day) return a.day - b.day;
    const timeDiff = a.start.compareTo(b.start);
    if (timeDiff !== 0) return timeDiff;
    return a.course.localeCompare(b.course);
  });

  const clashes = [];
  for (let i = 0; i < ordered.length; i++) {
    const first = ordered[i];
    for (let j = i + 1; j < ordered.length; j++) {
      const second = ordered[j];
      if (second.day !== first.day || second.start.compareTo(first.end) >= 0) {
        break;
      }
      clashes.push([first, second]);
    }
  }
  return clashes;
}

// PY: Date.getDay() returns 0 for Sunday. Python weekday() returns 0 for Monday.
export function getPythonWeekday(date) {
  return (date.getDay() + 6) % 7;
}

export function occurrenceAfter(session, now) {
  // PY: % 7 with negative numbers in JS: ((a % b) + b) % b
  const nowWd = getPythonWeekday(now);
  const daysAhead = ((session.day - nowWd) % 7 + 7) % 7;
  const candidate = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate() + daysAhead,
    session.start.hour,
    session.start.minute,
    0,
    0
  );
  if (candidate.getTime() <= now.getTime()) {
    // PY: Add 7 calendar days
    candidate.setDate(candidate.getDate() + 7);
  }
  return candidate;
}

export function currentSession(sessions, now) {
  const nowWd = getPythonWeekday(now);
  const nowTime = new Time(now.getHours(), now.getMinutes());
  for (const s of sessions) {
    if (s.day === nowWd && s.start.compareTo(nowTime) <= 0 && nowTime.compareTo(s.end) < 0) {
      return s;
    }
  }
  return null;
}

export function nextSession(sessions, now) {
  let best = null;
  for (const s of sessions) {
    const when = occurrenceAfter(s, now);
    if (best === null || when.getTime() < best[1].getTime()) {
      best = [s, when];
    }
  }
  return best;
}

export function minutesUntil(now, then) {
  // PY: Whole minutes rounded up using Math.floor((seconds + 59) / 60)
  const ms = then.getTime() - now.getTime();
  const seconds = Math.floor(ms / 1000);
  if (seconds <= 0) {
    return 0;
  }
  return Math.floor((seconds + 59) / 60);
}

export function weeklyMinutes(sessions) {
  // PY: Use Map to preserve insertion order for non-numeric keys
  const totals = new Map();
  for (const s of sessions) {
    const current = totals.get(s.course) || 0;
    totals.set(s.course, current + s.minutes);
  }
  return totals;
}

export function formatSession(s) {
  return `${DAY_NAMES[s.day]} ${s.start.toISOString()}-${s.end.toISOString()} ${s.course} @ ${s.room}`;
}
