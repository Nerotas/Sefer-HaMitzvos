import csv
import re

def compare_mitzvot_files():
    """Compare the Schedule.csv with MitzvosMasterList.csv to find mismatches."""

    # Read the master list
    master_list = {}
    with open('MitzvosMasterList.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                number = int(row['Number'])
                master_list[number] = {
                    'mitzvah': row['Mitzvah'].strip(),
                    'reference': row['Biblical Reference'].strip()
                }
            except ValueError:
                continue

    # Read the schedule and check numbered mitzvot
    mismatches = []
    schedule_entries = []

    with open('Schedule.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mitzvos_field = row['Mitzvos'].strip()

            # Skip intro entries
            if mitzvos_field.startswith('Intro'):
                continue

            # Extract numbers from the Mitzvos field
            # Handle cases like "1", "66, 67", "122, 123", etc.
            numbers = []
            if ',' in mitzvos_field:
                # Multiple numbers
                parts = mitzvos_field.split(',')
                for part in parts:
                    part = part.strip()
                    if part.isdigit():
                        numbers.append(int(part))
            else:
                # Single number
                if mitzvos_field.isdigit():
                    numbers.append(int(mitzvos_field))

            if numbers:
                schedule_entries.append({
                    'date': row['Date'],
                    'numbers': numbers,
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip()
                })

    # Compare each entry
    print("COMPARISON RESULTS:\n")
    print("=" * 80)

    total_checked = 0
    total_mismatches = 0

    for entry in schedule_entries:
        for num in entry['numbers']:
            total_checked += 1

            if num not in master_list:
                print(f"ERROR: Mitzvah {num} not found in master list!")
                total_mismatches += 1
                continue

            master_mitzvah = master_list[num]['mitzvah']
            master_reference = master_list[num]['reference']
            schedule_title = entry['title']
            schedule_source = entry['source']

            # Check if titles match (allowing for some variation)
            title_match = (master_mitzvah.lower().replace('‑', '-') ==
                          schedule_title.lower().replace('‑', '-'))

            # Check if sources match (extract book and chapter:verse)
            source_match = (master_reference == schedule_source)

            if not title_match or not source_match:
                print(f"\nMISMATCH for Mitzvah {num} ({entry['date']}):")
                print(f"  Master List: '{master_mitzvah}' | {master_reference}")
                print(f"  Schedule:    '{schedule_title}' | {schedule_source}")

                if not title_match:
                    print(f"  → TITLE MISMATCH")
                if not source_match:
                    print(f"  → SOURCE MISMATCH")

                total_mismatches += 1
                mismatches.append({
                    'number': num,
                    'date': entry['date'],
                    'master_title': master_mitzvah,
                    'schedule_title': schedule_title,
                    'master_source': master_reference,
                    'schedule_source': schedule_source
                })

    print(f"\n" + "=" * 80)
    print(f"SUMMARY:")
    print(f"Total mitzvot checked: {total_checked}")
    print(f"Total mismatches found: {total_mismatches}")
    print(f"Accuracy: {((total_checked - total_mismatches) / total_checked * 100):.1f}%")

    return mismatches

if __name__ == "__main__":
    mismatches = compare_mitzvot_files()