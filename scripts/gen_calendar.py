"""Generate the UP 591 AY 2026-27 seminar calendar (.ics).

Source of truth for session dates/topics for the calendar subscription.
The schedule table in schedule/schedule.qmd is maintained alongside this file.

Run from the repo root:
    python3 scripts/gen_calendar.py

Emits schedule/up591-ay26-27.ics (RFC 5545, America/Chicago, DST-correct).
"""
from __future__ import annotations

import datetime as dt
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "schedule" / "up591-ay26-27.ics"

# (date, title, location, description)
# All sessions: Fridays 12:00-12:50 pm. Oct 30 is the Zoom mentor panel.
SESSIONS: list[tuple[dt.date, str, str, str]] = [
    (
        dt.date(2026, 8, 28),
        "UP 591: Seminar Introduction",
        "Temple Buell Hall 225",
        "Course introduction and structure; mentoring pilot overview; Plan of Study peer review.",
    ),
    (
        dt.date(2026, 9, 25),
        "UP 591: FAA Career Services & Building a Professional Network",
        "Temple Buell Hall 225",
        "Conversation with Ana Rodas (FAA Career Services); network-building exercise; mentor matches announced.",
    ),
    (
        dt.date(2026, 10, 30),
        "UP 591: Mentor Panel (Zoom)",
        "Online (Zoom)",
        "Panel discussion with mentor-practitioners on building a professional identity and practice.",
    ),
    (
        dt.date(2026, 11, 20),
        "UP 591: Portfolio Development",
        "Temple Buell Hall 225",
        "Portfolio structure and goals; key document review.",
    ),
    (
        dt.date(2026, 12, 4),
        "UP 591: End-of-Semester Studio + Feedback Launch",
        "Temple Buell Hall 225",
        "Studio peer review of near-final portfolios; December structured feedback exchange with your mentor.",
    ),
    (
        dt.date(2027, 1, 22),
        "UP 591: Semester 2 Check-In",
        "Temple Buell Hall 225",
        "Review expectations for end-of-semester deliverables; implementing your professional development and job search plans.",
    ),
    (
        dt.date(2027, 2, 26),
        "UP 591: Developing a Job Search Strategy",
        "Temple Buell Hall 225",
        "Considerations for developing a job search strategy; transition planning conversation with your mentor.",
    ),
    (
        dt.date(2027, 3, 26),
        "UP 591: Professional Identity & Capstone Communication",
        "Temple Buell Hall 225",
        "Articulate and update your professional identity; translating your capstone work for audiences.",
    ),
    (
        dt.date(2027, 4, 23),
        "UP 591: Poster Review + Exit Prep",
        "Temple Buell Hall 225",
        "Peer review of draft posters; April final structured feedback exchange with your mentor.",
    ),
]

START = dt.time(12, 0)
END = dt.time(12, 50)

ICS_HEADER = "\r\n".join(
    [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//The System//UP 591 AY 2026-27//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:UP 591 Capstone Seminar (AY 2026-27)",
        "X-WR-TIMEZONE:America/Chicago",
        # ---- America/Chicago VTIMEZONE (2026-27) ----
        "BEGIN:VTIMEZONE",
        "TZID:America/Chicago",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:-0600",
        "TZOFFSETTO:-0500",
        "TZNAME:CDT",
        "DTSTART:19700308T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU",
        "END:DAYLIGHT",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:-0500",
        "TZOFFSETTO:-0600",
        "TZNAME:CST",
        "DTSTART:19701101T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]
)


def _fold(line: str) -> str:
    """RFC 5545 line folding at 75 octets."""
    if len(line) <= 75:
        return line
    out = [line[:75]]
    rest = line[75:]
    while rest:
        out.append(" " + rest[:74])
        rest = rest[74:]
    return "\r\n".join(out)


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")


def build_ics() -> str:
    stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    lines = ICS_HEADER.split("\r\n")
    for date, title, location, desc in SESSIONS:
        start = dt.datetime.combine(date, START)
        end = dt.datetime.combine(date, END)
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:up591-{date:%Y-%m-%d}@andrew-greenlee.com",
                f"DTSTAMP:{stamp}",
                f"DTSTART;TZID=America/Chicago:{start:%Y%m%dT%H%M%S}",
                f"DTEND;TZID=America/Chicago:{end:%Y%m%dT%H%M%S}",
                _fold(f"SUMMARY:{_escape(title)}"),
                _fold(f"LOCATION:{_escape(location)}"),
                _fold(f"DESCRIPTION:{_escape(desc)}"),
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_ics(), encoding="utf-8")
    print(f"Wrote {OUT} ({len(SESSIONS)} events)")


if __name__ == "__main__":
    main()