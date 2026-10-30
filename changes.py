"""Print the three biggest percent changes in pallets between the last ISO week
in a shipments export and the week before. Clients and routes are ranked
together.

Usage: python3 changes.py [path/to/export.csv]
"""

import csv
import math
import sys
from collections import defaultdict
from datetime import date, timedelta

TOP = 3


def iso_week(d):
    year, week, _ = d.isocalendar()
    return (year, week)


def week_before(week):
    monday = date.fromisocalendar(week[0], week[1], 1)
    return iso_week(monday - timedelta(days=7))


def label(week):
    return f"{week[0]}-W{week[1]:02d}"


def percent(before, after):
    # There is no percentage from 0 pallets, so anything new ranks first.
    if before == 0:
        return math.inf if after else 0.0
    return (after - before) / before * 100


def format_percent(pct):
    return "new" if pct == math.inf else f"{pct:+.1f}%"


def main(path):
    # pallets[(kind, name)][(year, week)] -> total pallets that week
    pallets = defaultdict(lambda: defaultdict(int))
    weeks = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            week = iso_week(date.fromisoformat(row["date"]))
            weeks.add(week)
            n = int(row["pallets"])
            pallets[("client", row["client"])][week] += n
            pallets[("route", row["route"])][week] += n

    if not weeks:
        sys.exit(f"{path}: no shipments found")
    last = max(weeks)
    prev = week_before(last)

    changes = []
    for (kind, name), by_week in pallets.items():
        before, after = by_week.get(prev, 0), by_week.get(last, 0)
        changes.append((kind, name, before, after, percent(before, after)))
    # Biggest change first, up or down; ties by name so the output is stable.
    changes.sort(key=lambda c: (-abs(c[4]), c[1], c[0]))
    top = changes[:TOP]

    print(f"Pallet changes by percent, {label(prev)} -> {label(last)} (clients and routes)")
    width = max(len(c[1]) for c in top)
    for i, (kind, name, before, after, pct) in enumerate(top, 1):
        print(f"{i}. {kind:<6} {name:<{width}}  {before:>4} -> {after:>4}  {format_percent(pct)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "shipments-export-sample.csv")
