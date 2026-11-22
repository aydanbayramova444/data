"""Extract, transform and load the ticket export into SQLite."""
import csv
import sqlite3
from datetime import datetime

NAMES = {c.lower(): c for c in ["Card", "Mobile app", "Transfer", "Account access", "ATM"]}
COLUMNS = ["id", "created_at", "month", "shift", "category", "channel", "hours",
           "sla_hours", "met_sla", "csat"]


def parse_date(value):
    for fmt in ("%Y-%m-%d %H:%M", "%d.%m.%Y %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unknown date format: {value}")


def transform(rows):
    clean, seen = [], set()
    removed = {"duplicates": 0, "invalid_duration": 0}
    for r in rows:
        if r["id"] in seen:
            removed["duplicates"] += 1
            continue
        seen.add(r["id"])
        hours = float(r["hours"])
        if hours <= 0:
            removed["invalid_duration"] += 1
            continue
        date, sla = parse_date(r["created_at"]), int(r["sla_hours"])
        clean.append((int(r["id"]), date.isoformat(" "), date.strftime("%Y-%m"),
                      "Day" if 8 <= date.hour < 20 else "Night",
                      NAMES[r["category"].strip().lower()], r["channel"], hours, sla,
                      int(hours <= sla), int(r["csat"]) if r["csat"] else None))
    return clean, removed


def run(raw_path, clean_path, db_path):
    with open(raw_path, newline="") as f:
        raw = list(csv.DictReader(f))
    clean, removed = transform(raw)
    with open(clean_path, "w", newline="") as f:
        out = csv.writer(f, lineterminator="\n")
        out.writerow(COLUMNS)
        out.writerows(clean)
    db = sqlite3.connect(db_path)
    db.execute("DROP TABLE IF EXISTS tickets")
    db.execute(f"CREATE TABLE tickets ({', '.join(COLUMNS)})")
    db.executemany(f"INSERT INTO tickets VALUES ({','.join('?' * len(COLUMNS))})", clean)
    db.commit()
    return db, {"raw_rows": len(raw), **removed, "clean_rows": len(clean)}
