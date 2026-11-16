"""Opening hours for CampusRoute places (backlog CR-11).

Implement is_open(). Read README.md for the rules. Standard library only.
"""

from datetime import datetime
import re

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEK_MINUTES = 7 * 24 * 60

TIME_RE = re.compile(r"^(\d{2}):(\d{2})$")


def _parse_time(t_str: str, is_end: bool = False) -> int:
    m = TIME_RE.match(t_str)
    if not m:
        raise ValueError(f"Invalid time format: {t_str}")
    hh = int(m.group(1))
    mm = int(m.group(2))
    if mm < 0 or mm > 59:
        raise ValueError(f"Invalid minute: {mm}")
    if is_end:
        if hh < 0 or hh > 24:
            raise ValueError(f"Invalid end hour: {hh}")
        if hh == 24 and mm != 0:
            raise ValueError(f"24:{mm:02d} is not allowed")
    else:
        if hh < 0 or hh > 23:
            raise ValueError(f"Invalid start hour: {hh}")
    return hh * 60 + mm


def is_open(hours: str, now: datetime) -> bool:
    """True if a place with this ``hours`` string is open at ``now``.

    >>> is_open("Mon-Fri 08:00-17:00", datetime(2027, 3, 1, 9, 0))   # a Monday
    True
    """
    if not isinstance(hours, str):
        raise ValueError("hours must be a string")
    hours_clean = hours.strip()
    if not hours_clean:
        raise ValueError("Empty hours string")

    # day_intervals maps each day index (0..6) to list of (start_week_min, end_week_min)
    day_intervals = {d: [] for d in range(7)}

    segments = hours_clean.split(";")
    for seg in segments:
        seg = seg.strip()
        if not seg:
            raise ValueError("Empty segment in hours")
        tokens = seg.split()
        if len(tokens) != 2:
            raise ValueError(f"Invalid segment format: {seg}")
        days_part, time_part = tokens[0].lower(), tokens[1].lower()

        # Parse days
        if "-" in days_part:
            d_parts = days_part.split("-")
            if len(d_parts) != 2:
                raise ValueError(f"Invalid day range: {days_part}")
            d1_name, d2_name = d_parts[0], d_parts[1]
            if d1_name not in DAYS or d2_name not in DAYS:
                raise ValueError(f"Unknown day in range: {days_part}")
            idx1 = DAYS.index(d1_name)
            idx2 = DAYS.index(d2_name)
            if idx1 > idx2:
                raise ValueError(f"Backwards day range: {days_part}")
            target_days = list(range(idx1, idx2 + 1))
        else:
            if days_part not in DAYS:
                raise ValueError(f"Unknown day: {days_part}")
            target_days = [DAYS.index(days_part)]

        if time_part == "closed":
            for d in target_days:
                day_intervals[d].clear()
            continue

        # Parse time range
        if "-" not in time_part:
            raise ValueError(f"Invalid time range: {time_part}")
        t_parts = time_part.split("-")
        if len(t_parts) != 2:
            raise ValueError(f"Invalid time range: {time_part}")
        start_min = _parse_time(t_parts[0], is_end=False)
        end_min = _parse_time(t_parts[1], is_end=True)
        if start_min == end_min:
            raise ValueError(f"Start time equals end time: {time_part}")

        duration = (end_min - start_min) if end_min > start_min else (1440 - start_min + end_min)

        for d in target_days:
            start_week_min = d * 1440 + start_min
            end_week_min = start_week_min + duration
            day_intervals[d].append((start_week_min, end_week_min))

    weekday = now.weekday()
    now_week_min = weekday * 1440 + now.hour * 60 + now.minute

    for d in range(7):
        for start_w, end_w in day_intervals[d]:
            if end_w <= WEEK_MINUTES:
                if start_w <= now_week_min < end_w:
                    return True
            else:
                if now_week_min >= start_w or now_week_min < (end_w - WEEK_MINUTES):
                    return True

    return False
