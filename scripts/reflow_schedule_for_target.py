#!/usr/bin/env python3
"""
Reflow the Sefer HaMitzvos schedule dates to:
- Start with 1 entry per day (single message)
- Then switch to 2 entries per day (two messages combined into one day)
- Finish by a target date

This script preserves the order of entries and reassigns the Date column so the
loader groups entries by date (multiple rows with same Date become one message).

Usage (examples):
  python scripts/reflow_schedule_for_target.py \
    --input Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv \
    --output Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv \
    --start-date 2025-10-20 \
    --target-date 2026-10-04

Dry-run only (no write):
  python scripts/reflow_schedule_for_target.py --start-date 2025-10-20 --target-date 2026-10-04 --dry-run

If --output is the same as --input, a timestamped backup will be created automatically.
"""

import argparse
import csv
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Reflow schedule dates to meet a target finish date with 1/day then 2/day.")
    parser.add_argument("--input", default="Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv", help="Input CSV path")
    parser.add_argument("--output", default="Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv", help="Output CSV path")
    parser.add_argument("--start-date", required=False, help="Start date (YYYY-MM-DD). Default: tomorrow in America/Chicago")
    parser.add_argument("--target-date", required=True, help="Target finish date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Compute and print plan without writing output")
    return parser.parse_args()


def to_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def daterange(start: date, end: date):
    # Inclusive range of dates
    cur = start
    while cur <= end:
        yield cur
        cur = cur + timedelta(days=1)


def compute_switch_days(total_entries: int, start: date, target: date):
    # D is number of calendar days available (inclusive)
    D = (target - start).days + 1
    if D <= 0:
        raise ValueError("Target date must be on or after start date")

    # Feasibility: at most 2 entries per day in phase 2
    if 2 * D < total_entries:
        return {
            "feasible": False,
            "days_available": D,
            "max_capacity": 2 * D,
            "entries": total_entries,
        }

    # Choose the longest possible 1/day stretch (x) before switching to 2/day so we still finish by target.
    # Constraint: x + 2*(D - x) >= total_entries -> 2D - x >= total_entries -> x <= 2D - total_entries
    x = min(D, max(0, 2 * D - total_entries))
    return {
        "feasible": True,
        "days_available": D,
        "entries": total_entries,
        "single_days": x,
        "double_days": max(0, D - x),
    }


def main():
    args = parse_args()

    # Determine default start date (tomorrow America/Chicago). We don't have timezone libs here;
    # using system local date + 1 day is sufficient for a default. Users can override.
    today = date.today()
    default_start = today + timedelta(days=1)
    start_date = to_date(args.start_date) if args.start_date else default_start
    target_date = to_date(args.target_date)

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"Input CSV not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Read rows preserving order by original Date ascending, then stable within the same date
    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not rows:
        print("No rows found in input CSV.", file=sys.stderr)
        sys.exit(1)

    # Sort by original Date (parse), keeping stable order otherwise
    def parse_date_safe(row):
        key = "Date" if "Date" in row else list(row.keys())[0]
        try:
            return to_date(row[key].strip())
        except Exception:
            return date.min

    rows.sort(key=parse_date_safe)

    total_entries = len(rows)
    plan = compute_switch_days(total_entries, start_date, target_date)

    if not plan["feasible"]:
        print("Plan is not feasible.")
        print(f"  Entries: {plan['entries']}")
        print(f"  Days available: {plan['days_available']}")
        print(f"  Max capacity at 2/day: {plan['max_capacity']}")
        sys.exit(2)

    x = plan["single_days"]
    D = plan["days_available"]

    # Assign new dates
    dates = list(daterange(start_date, target_date))
    assigned = 0
    for day_index, d in enumerate(dates):
        if assigned >= total_entries:
            break
        new_date_str = d.isoformat()
        # one per day during single phase
        if day_index < x:
            rows[assigned]["Date"] = new_date_str
            assigned += 1
        else:
            # two per day during double phase
            rows[assigned]["Date"] = new_date_str
            assigned += 1
            if assigned < total_entries:
                rows[assigned]["Date"] = new_date_str
                assigned += 1

    if assigned < total_entries:
        print("Error: Not enough days to assign all entries even after phase switch.", file=sys.stderr)
        sys.exit(3)

    # Report
    print("Reflow plan:")
    print(f"  Start date:   {start_date}")
    print(f"  Target date:  {target_date}")
    print(f"  Total entries: {total_entries}")
    print(f"  Days:          {D}")
    print(f"  1/day until:   {start_date} -> {start_date + timedelta(days=x-1) if x>0 else 'N/A'} ({x} days)")
    print(f"  Then 2/day for {max(0, D-x)} day(s) or until complete")

    if args.dry_run:
        print("Dry run complete (no file written).")
        return

    # Backup if writing in-place
    if out_path.resolve() == in_path.resolve():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = in_path.with_name(in_path.stem + f"_BACKUP_{ts}" + in_path.suffix)
        backup.write_bytes(in_path.read_bytes())
        print(f"Backup created: {backup}")

    # Write out with same fieldnames
    # Ensure Date is first column if it was in the original
    if "Date" in fieldnames:
        # keep order as-is
        ordered_fields = fieldnames
    else:
        # put Date first
        ordered_fields = ["Date"] + [fn for fn in fieldnames if fn != "Date"]

    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote updated schedule to: {out_path}")


if __name__ == "__main__":
    main()
