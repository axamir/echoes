#!/usr/bin/env python3
"""Build timeline/comparison.csv from the email archive and official announcements.

Inputs (read only):
  data/emails.json                  91 email-thread records
  data/official_announcements.json  34 dated official announcements

Output:
  timeline/comparison.csv           one row per record, merged and sorted

The status column is a calendar-date ordering label only. For each row, the
script finds the nearest row on the other side (echo-archive vs official) by
calendar-day distance. If two other-side dates are equally near — one earlier
and one later — the later date is used. If this row's calendar date is
strictly earlier than that nearest other-side date, the label is
DOCUMENTED BEFORE; otherwise (same day or later) it is DOCUMENTED AFTER.
Same-day counts as AFTER because official dates have no time of day, so
order within a day cannot be established.

These labels record date order only. They do not imply any connection, cause,
or priority between an email thread and an announcement.

Run from the repository root:
    python3 analysis/scripts/build_comparison_csv.py
"""
import csv
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EMAILS = ROOT / "data" / "emails.json"
ANNOUNCEMENTS = ROOT / "data" / "official_announcements.json"
OUT = ROOT / "timeline" / "comparison.csv"

COLUMNS = ["date", "source", "file", "event", "status"]


def calendar_date(value):
    return date.fromisoformat(value[:10])


def echo_event(record):
    subject = (record.get("subject") or "").strip()
    if subject:
        return subject
    parts = [p for p in (record.get("echo_label"), record.get("case_id")) if p]
    return " / ".join(parts)


def official_event(record):
    return f"{record['id']}: {record['organization']}: {record['announcement']}"


def sort_key(row, index):
    # Calendar date, then time. Official rows have no time and sort before
    # timed echo rows on the same day. The original index keeps the sort stable.
    day = calendar_date(row["date"])
    raw = row["date"]
    if "T" in raw:
        time = datetime.strptime(raw, "%Y-%m-%dT%H:%M").time()
        return (day, 1, time, index)
    return (day, 0, None, index)


def nearest_other_date(day, other_days):
    """Return the nearest other-side calendar date.

    Distance is the absolute gap in days. A tie between an earlier and a later
    candidate is broken by picking the later date.
    """
    min_distance = min(abs((day - other).days) for other in other_days)
    at_min = [other for other in other_days if abs((day - other).days) == min_distance]
    return max(at_min)


def status_for(day, other_days):
    nearest = nearest_other_date(day, other_days)
    if day < nearest:
        return "DOCUMENTED BEFORE"
    return "DOCUMENTED AFTER"


def load_rows():
    emails = json.loads(EMAILS.read_text(encoding="utf-8"))
    announcements = json.loads(ANNOUNCEMENTS.read_text(encoding="utf-8"))

    echo_rows = [
        {
            "date": record["date"],
            "source": "echo-archive",
            "file": record["source_file"],
            "event": echo_event(record),
        }
        for record in emails
    ]
    official_rows = [
        {
            "date": record["date"],
            "source": "official",
            "file": record["primary_source_url"],
            "event": official_event(record),
        }
        for record in announcements
    ]

    echo_days = sorted({calendar_date(row["date"]) for row in echo_rows})
    official_days = sorted({calendar_date(row["date"]) for row in official_rows})
    if not echo_days or not official_days:
        raise SystemExit("both emails.json and official_announcements.json must be non-empty")

    for row in echo_rows:
        row["status"] = status_for(calendar_date(row["date"]), official_days)
    for row in official_rows:
        row["status"] = status_for(calendar_date(row["date"]), echo_days)

    rows = echo_rows + official_rows
    rows = [row for _, row in sorted(enumerate(rows), key=lambda item: sort_key(item[1], item[0]))]
    return rows


def main():
    rows = load_rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    before = sum(1 for row in rows if row["status"] == "DOCUMENTED BEFORE")
    after = sum(1 for row in rows if row["status"] == "DOCUMENTED AFTER")
    before_echo = sum(
        1 for row in rows
        if row["status"] == "DOCUMENTED BEFORE" and row["source"] == "echo-archive"
    )
    before_official = sum(
        1 for row in rows
        if row["status"] == "DOCUMENTED BEFORE" and row["source"] == "official"
    )
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} rows")
    print(f"DOCUMENTED BEFORE: {before} (echo-archive {before_echo}, official {before_official})")
    print(f"DOCUMENTED AFTER:  {after}")


if __name__ == "__main__":
    main()
