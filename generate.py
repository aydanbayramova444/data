"""Create a SYNTHETIC, intentionally messy support-ticket export."""
import csv
import random
from datetime import datetime, timedelta

# category: (share of tickets, median hours to resolve, SLA in hours)
CATEGORIES = {
    "Card": (30, 5, 8),
    "Mobile app": (24, 7, 12),
    "Transfer": (18, 9, 12),
    "Account access": (16, 3, 4),
    "ATM": (12, 18, 24),
}
CHANNELS = {"Call center": (40, 0.8), "Chat": (35, 1.0), "Email": (15, 1.5), "Branch": (10, 0.9)}


def generate(path, n=6000, seed=42):
    rng = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        cat = rng.choices(list(CATEGORIES), [v[0] for v in CATEGORIES.values()])[0]
        channel = rng.choices(list(CHANNELS), [v[0] for v in CHANNELS.values()])[0]
        created = datetime(2026, 5, 1) + timedelta(minutes=rng.randrange(184 * 24 * 60))
        _, median, sla = CATEGORIES[cat]
        night = 1.4 if created.hour >= 20 or created.hour < 8 else 1
        hours = median * CHANNELS[channel][1] * night * rng.lognormvariate(0, 0.5)
        score = min(5, max(1, round(4.6 - 1.2 * hours / sla + rng.gauss(0, 0.7))))
        date_format = "%d.%m.%Y %H:%M" if rng.random() < 0.15 else "%Y-%m-%d %H:%M"
        if rng.random() < 0.1:
            cat = f" {cat.upper()} "
        if rng.random() < 0.01:
            hours = -hours
        rows.append([i, created.strftime(date_format), cat, channel, round(hours, 2), sla,
                     score if rng.random() > 0.2 else ""])
    rows += rng.sample(rows, n // 50)
    rng.shuffle(rows)
    with open(path, "w", newline="") as f:
        out = csv.writer(f, lineterminator="\n")
        out.writerow(["id", "created_at", "category", "channel", "hours", "sla_hours", "csat"])
        out.writerows(rows)
