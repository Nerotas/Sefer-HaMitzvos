import csv
import json
from datetime import datetime, timedelta

def extract_conclusion_summary():
    """Extract a meaningful summary from the Conclusion for Positive Commandments"""
    try:
        with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        conclusion_text = data['text']['Conclusion for Positive Commandments']
        if conclusion_text and len(conclusion_text) > 0:
            # Use the last paragraph as it contains the key summary
            last_paragraph = conclusion_text[-1].strip()
            return last_paragraph

        return "Conclusion for Positive Commandments."
    except:
        return "Conclusion for Positive Commandments."

def reorder_schedule():
    """Reorder the schedule to place the conclusion between positive and negative mitzvot"""

    # Read the current schedule
    entries = []
    with open('Schedule_Complete_Sefer_HaMitzvos.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            entries.append(row)

    print(f"Total entries read: {len(entries)}")

    # Separate the entries
    introduction_entries = []
    positive_entries = []
    negative_entries = []
    conclusion_entry = None

    for entry in entries:
        mitzvah_type = entry['Mitzvah_Type_Number']
        if 'Intro' in mitzvah_type:
            introduction_entries.append(entry)
        elif 'Positive' in mitzvah_type:
            positive_entries.append(entry)
        elif 'Negative' in mitzvah_type:
            negative_entries.append(entry)
        elif 'Conclusion' in mitzvah_type:
            conclusion_entry = entry

    print(f"Introduction entries: {len(introduction_entries)}")
    print(f"Positive entries: {len(positive_entries)}")
    print(f"Negative entries: {len(negative_entries)}")
    print(f"Conclusion entry: {'Found' if conclusion_entry else 'Not found'}")

    # Extract better summary for conclusion
    better_summary = extract_conclusion_summary()
    if conclusion_entry:
        conclusion_entry['Summary'] = better_summary
        print(f"Updated conclusion summary: {better_summary[:100]}...")

    # Reorganize all entries in the correct order
    all_entries = []
    all_entries.extend(introduction_entries)
    all_entries.extend(positive_entries)

    # Add conclusion right after positive entries
    if conclusion_entry:
        all_entries.append(conclusion_entry)

    all_entries.extend(negative_entries)

    print(f"Total reorganized entries: {len(all_entries)}")

    # Redistribute across dates maintaining 1-2 entries per day
    start_date = datetime(2025, 10, 20)
    current_date = start_date
    current_entry_number = 1

    # Calculate optimal distribution
    total_entries = len(all_entries)
    total_days = 350  # October 20, 2025 to October 4, 2026

    # Optimal distribution: fill with 2 entries per day first, then remainder with 1
    days_with_two = total_entries - total_days
    days_with_one = total_days - days_with_two

    print(f"Distribution: {days_with_one} days with 1 entry, {days_with_two} days with 2 entries")

    entry_index = 0
    day_count = 0

    for day in range(total_days):
        date_str = current_date.strftime('%Y-%m-%d')

        # Determine how many entries for this day
        if day < days_with_two:
            entries_today = 2
        else:
            entries_today = 1

        # Assign entries for this day
        for i in range(entries_today):
            if entry_index < len(all_entries):
                entry = all_entries[entry_index]
                entry['Date'] = date_str
                entry['Sequential_Number'] = str(current_entry_number)
                entry_index += 1
                current_entry_number += 1

        current_date += timedelta(days=1)
        day_count += 1

    # Write the reordered schedule
    with open('Schedule_Complete_Sefer_HaMitzvos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_entries)

    print(f"Schedule successfully reordered!")
    print(f"Conclusion now appears between positive and negative mitzvot")
    print(f"Total entries distributed across {total_days} days")

if __name__ == "__main__":
    reorder_schedule()