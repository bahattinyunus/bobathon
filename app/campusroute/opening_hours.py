"""Opening hours parsing and query (backlog item CR-11).

Conforms to standard CampusRoute hours formats:
    "Mon-Fri 08:00-24:00; Sat 10:00-18:00; Sun 12:00-20:00"
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEK_MINUTES = 7 * 24 * 60

TIME_RE = re.compile(r"^(\d{2}):(\d{2})$")


def parse_time_minutes(t_str: str, is_end: bool = False) -> int:
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


def is_open(hours: Optional[str], now: datetime) -> bool:
    """True if a place with this hours string is open at now.

    >>> is_open("Mon-Fri 08:00-17:00", datetime(2027, 3, 1, 9, 0))
    True
    """
    if not hours or not isinstance(hours, str):
        return False
    hours_clean = hours.strip()
    if not hours_clean:
        return False

    day_intervals = {d: [] for d in range(7)}

    segments = hours_clean.split(";")
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        tokens = seg.split()
        if len(tokens) != 2:
            continue
        days_part, time_part = tokens[0].lower(), tokens[1].lower()

        if "-" in days_part:
            d_parts = days_part.split("-")
            if len(d_parts) != 2 or d_parts[0] not in DAYS or d_parts[1] not in DAYS:
                continue
            idx1 = DAYS.index(d_parts[0])
            idx2 = DAYS.index(d_parts[1])
            if idx1 > idx2:
                continue
            target_days = list(range(idx1, idx2 + 1))
        else:
            if days_part not in DAYS:
                continue
            target_days = [DAYS.index(days_part)]

        if time_part == "closed":
            for d in target_days:
                day_intervals[d].clear()
            continue

        if "-" not in time_part:
            continue
        t_parts = time_part.split("-")
        if len(t_parts) != 2:
            continue

        try:
            start_min = parse_time_minutes(t_parts[0], is_end=False)
            end_min = parse_time_minutes(t_parts[1], is_end=True)
        except ValueError:
            continue

        if start_min == end_min:
            continue

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
