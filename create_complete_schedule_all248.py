#!/usr/bin/env python3
"""
Create a COMPLETE Sefer HaMitzvos schedule with ALL 248 positive mitzvot:
- Start: 10/20/25, End: 10/04/26 (350 days)
- Include 14 introductions, ALL 248 positive, all 365 negative mitzvot, 1 conclusion
- Total: 628 entries in 350 days (some days will have 2 entries)
"""

import json
import csv
from datetime import datetime, timedelta

def load_sefer_hamitzvot():
    """Load the Sefer HaMitzvot JSON file"""
    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_positive_summary(mitzvah_text):
    """Extract a clean summary from positive commandment text"""
    if not mitzvah_text:
        return "Positive commandment from Sefer HaMitzvot"

    # Handle list format from JSON
    if isinstance(mitzvah_text, list):
        mitzvah_text = mitzvah_text[0] if mitzvah_text else ""

    text = str(mitzvah_text)

    # Try various patterns for positive commandments
    patterns = [
        r"That is that He commanded us (.+?)(?:\.|$)",
        r"And that is that He commanded us (.+?)(?:\.|$)",
        r"That is that we were commanded (.+?)(?:\.|$)",
        r"And that is that we were commanded (.+?)(?:\.|$)",
    ]

    import re
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            summary = matches[0].strip()
            # Clean up the summary
            summary = re.sub(r'\s+', ' ', summary)
            summary = summary.replace(' - ', ' ')
            summary = summary.rstrip('.,;:')

            # Make it a complete sentence
            if summary and not summary.endswith('.'):
                return f"We are commanded {summary}."
            elif summary:
                return summary.capitalize()

    # Fallback: try to extract any meaningful content
    if "belief" in text.lower() or "believe" in text.lower():
        return "We are commanded regarding belief in God."
    elif "love" in text.lower():
        return "We are commanded to love God."
    elif "fear" in text.lower() or "awe" in text.lower():
        return "We are commanded to fear God."
    elif "serve" in text.lower():
        return "We are commanded to serve God."
    elif "tefillin" in text.lower():
        return "We are commanded regarding tefillin."
    elif "tzitzit" in text.lower():
        return "We are commanded regarding tzitzit."
    elif "mezuzah" in text.lower():
        return "We are commanded regarding mezuzah."
    elif "temple" in text.lower():
        return "We are commanded regarding the Temple."
    elif "priest" in text.lower():
        return "We are commanded regarding priestly service."
    elif "sacrifice" in text.lower() or "offering" in text.lower():
        return "We are commanded regarding sacrificial offerings."

    return "Positive commandment from Sefer HaMitzvot."

def extract_negative_summary(mitzvah_text):
    """Extract a clean summary from negative commandment text"""
    if not mitzvah_text:
        return "Negative commandment from Sefer HaMitzvot"

    # Handle list format from JSON
    if isinstance(mitzvah_text, list):
        mitzvah_text = mitzvah_text[0] if mitzvah_text else ""

    text = str(mitzvah_text)

    # Try various patterns for negative commandments
    patterns = [
        r"That He prohibited us from (.+?)(?:\.|$)",
        r"That He prohibited us (.+?)(?:\.|$)",
        r"prohibited us from (.+?)(?:\.|$)",
        r"prohibited us (.+?)(?:\.|$)",
    ]

    import re
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            summary = matches[0].strip()
            # Clean up the summary
            summary = re.sub(r'\s+', ' ', summary)
            summary = summary.replace(' - ', ' ')
            summary = summary.rstrip('.,;:')

            if summary:
                # Make it a complete sentence starting with "We are prohibited from"
                if not summary.startswith("We are"):
                    return f"We are prohibited from {summary}."
                else:
                    return summary.capitalize()

    # Check for existing "Not to" patterns
    if text.startswith("Not to "):
        content = text[7:].strip().rstrip('.,;:')
        return f"We are prohibited from {content}."

    # Fallback based on content
    if "idol" in text.lower():
        return "We are prohibited from idolatry."
    elif "swear" in text.lower():
        return "We are prohibited from false oaths."
    elif "eat" in text.lower():
        return "We are prohibited from eating forbidden foods."
    elif "work" in text.lower() and "sabbath" in text.lower():
        return "We are prohibited from Sabbath work."

    return "Negative commandment from Sefer HaMitzvot."

def create_complete_schedule():
    """Create the complete schedule with ALL 248 positive mitzvot"""

    # Load the data
    sefer_data = load_sefer_hamitzvot()
    intros = sefer_data['text']['Shorashim']
    positive_mitzvot = sefer_data['text']['Positive Commandments']
    negative_mitzvot = sefer_data['text']['Negative Commandments']

    print(f"Loaded data:")
    print(f"- Introductions: {len(intros)}")
    print(f"- Positive Mitzvot: {len(positive_mitzvot)}")
    print(f"- Negative Mitzvot: {len(negative_mitzvot)}")
    print(f"- Total entries needed: {len(intros) + len(positive_mitzvot) + len(negative_mitzvot) + 1}")

    # Date range
    start_date = datetime(2025, 10, 20)
    end_date = datetime(2026, 10, 4)
    total_days = (end_date - start_date).days + 1
    total_entries = len(intros) + len(positive_mitzvot) + len(negative_mitzvot) + 1  # +1 for conclusion

    print(f"Available days: {total_days}")
    print(f"Total entries: {total_entries}")
    print(f"Entries per day average: {total_entries / total_days:.2f}")

    schedule = []
    current_date = start_date
    entry_number = 1

    # Phase 1: Introduction (14 entries)
    print("Phase 1: Adding introductions...")
    intro_summaries = [
        "Introduction to Counting the Mitzvot.",
        "Principle 1: Not rabbinic commandments.",
        "Principle 2: Not derived through hermeneutics.",
        "Principle 3: Only perpetual commandments.",
        "Principle 4: Not general Torah commands.",
        "Principle 5: Not reasons as separate mitzvot.",
        "Principle 6: Separate positive and negative.",
        "Principle 7: Not details of commandments.",
        "Principle 8: Not negation of positive commands.",
        "Principle 9: Count substance, not statements.",
        "Principle 10: Not preliminaries to commandments.",
        "Principle 11: Not parts of unified commandments.",
        "Principle 12: Not work process components.",
        "Principle 13: Not repetition-based counting."
    ]

    for i in range(len(intros)):
        summary = intro_summaries[i] if i < len(intro_summaries) else f"Introduction principle {i+1}."
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            entry_number,
            f"Intro {i + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.{i+1}?lang=bi"
        ])
        entry_number += 1
        current_date += timedelta(days=1)

    # Phase 2: ALL 248 Positive Mitzvot
    print("Phase 2: Adding ALL positive mitzvot...")
    for i in range(len(positive_mitzvot)):
        try:
            full_text = positive_mitzvot[i][0] if isinstance(positive_mitzvot[i], list) else positive_mitzvot[i]
            summary = extract_positive_summary(full_text)
        except:
            summary = f"Positive commandment {i+1} from Sefer HaMitzvot."

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            entry_number,
            f"Positive {i + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{i+1}?lang=bi"
        ])
        entry_number += 1

        # We have 350 days total, 14 used for intros, 1 for conclusion = 335 days for 613 mitzvot
        # Average ~1.83 entries per day, so some days need 2 entries
        remaining_entries = len(positive_mitzvot) + len(negative_mitzvot) - (i + 1)  # +1 because i is 0-indexed
        remaining_days = (end_date - current_date).days

        if remaining_entries > remaining_days:
            # Add another entry today if we're behind schedule
            if i + 1 < len(positive_mitzvot):  # Don't go past positive mitzvot
                continue  # Don't advance the date, add another entry

        current_date += timedelta(days=1)

    # Phase 3: ALL 365 Negative Mitzvot
    print("Phase 3: Adding ALL negative mitzvot...")
    for i in range(len(negative_mitzvot)):
        try:
            full_text = negative_mitzvot[i][0] if isinstance(negative_mitzvot[i], list) else negative_mitzvot[i]
            summary = extract_negative_summary(full_text)
        except:
            summary = f"Negative commandment {i+1} from Sefer HaMitzvot."

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            entry_number,
            f"Negative {i + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{i+1}?lang=bi"
        ])
        entry_number += 1

        # Check if we need to add multiple entries per day to fit everything
        remaining_entries = len(negative_mitzvot) - (i + 1)  # Remaining after this one
        remaining_days = (end_date - current_date).days

        if remaining_entries > remaining_days and remaining_entries > 0:
            # Add another entry today if we're behind schedule
            continue  # Don't advance the date

        current_date += timedelta(days=1)

    # Phase 4: Conclusion
    print("Phase 4: Adding conclusion...")
    schedule.append([
        current_date.strftime('%Y-%m-%d'),
        entry_number,
        "Conclusion",
        "Conclusion for Positive Commandments.",
        "https://www.sefaria.org/Sefer_HaMitzvot%2C_Conclusion_for_Positive_Commandments?lang=bi"
    ])

    print(f"\nSchedule created with {len(schedule)} total entries")
    print(f"Final date: {current_date.strftime('%Y-%m-%d')}")
    return schedule

def save_schedule(schedule):
    """Save the schedule to CSV"""
    filename = 'Schedule_Complete_Sefer_HaMitzvos_Fixed_All248.csv'

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link'])
        writer.writerows(schedule)

    print(f"Schedule saved to: {filename}")

    # Print summary statistics
    pos_count = len([row for row in schedule if row[2].startswith('Positive')])
    neg_count = len([row for row in schedule if row[2].startswith('Negative')])
    intro_count = len([row for row in schedule if row[2].startswith('Intro')])

    print(f"\nFinal Statistics:")
    print(f"- Introductions: {intro_count}")
    print(f"- Positive Mitzvot: {pos_count}")
    print(f"- Negative Mitzvot: {neg_count}")
    print(f"- Total entries: {len(schedule)}")

if __name__ == "__main__":
    schedule = create_complete_schedule()
    save_schedule(schedule)