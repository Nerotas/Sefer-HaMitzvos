#!/usr/bin/env python3
"""
Create a PROPERLY DISTRIBUTED Sefer HaMitzvos schedule:
- Start: 10/20/25, End: 10/04/26 (350 days total)
- 14 intro days (1 per day) + 335 mitzvot days + 1 conclusion day = 350 days
- 335 mitzvot days: 57 days with 1 mitzvah + 278 days with 2 mitzvot = 613 total mitzvot
- ALL 248 positive + ALL 365 negative mitzvot with complete sentences
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
        return "We are commanded in this positive mitzvah."

    # Handle list format from JSON
    if isinstance(mitzvah_text, list):
        mitzvah_text = mitzvah_text[0] if mitzvah_text else ""

    text = str(mitzvah_text)

    # Try various patterns for positive commandments
    import re
    patterns = [
        r"That is that He commanded us (.+?)(?:\.|$)",
        r"And that is that He commanded us (.+?)(?:\.|$)",
        r"That is that we were commanded (.+?)(?:\.|$)",
        r"And that is that we were commanded (.+?)(?:\.|$)",
    ]

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

    # Fallback based on content
    content_lower = text.lower()
    if "belief" in content_lower or "believe" in content_lower:
        if "unity" in content_lower:
            return "We are commanded to believe in God's unity."
        return "We are commanded to believe in God."
    elif "love" in content_lower:
        return "We are commanded to love God."
    elif "fear" in content_lower or "awe" in content_lower:
        return "We are commanded to fear God."
    elif "serve" in content_lower:
        return "We are commanded to serve God."
    elif "tefillin" in content_lower:
        if "head" in content_lower:
            return "We are commanded to put on head tefillin."
        elif "hand" in content_lower:
            return "We are commanded to put on hand tefillin."
        return "We are commanded regarding tefillin."
    elif "tzitzit" in content_lower:
        return "We are commanded to make tzitzit."
    elif "mezuzah" in content_lower:
        return "We are commanded to make a mezuzah."
    elif "temple" in content_lower:
        return "We are commanded regarding the Temple."
    elif "priest" in content_lower:
        return "We are commanded regarding priestly service."
    elif "sacrifice" in content_lower or "offering" in content_lower:
        return "We are commanded regarding sacrificial offerings."

    return "We are commanded in this positive mitzvah."

def extract_negative_summary(mitzvah_text):
    """Extract a clean summary from negative commandment text"""
    if not mitzvah_text:
        return "We are prohibited in this negative mitzvah."

    # Handle list format from JSON
    if isinstance(mitzvah_text, list):
        mitzvah_text = mitzvah_text[0] if mitzvah_text else ""

    text = str(mitzvah_text)

    # Try various patterns for negative commandments
    import re
    patterns = [
        r"That He prohibited us from (.+?)(?:\.|$)",
        r"That He prohibited us (.+?)(?:\.|$)",
        r"prohibited us from (.+?)(?:\.|$)",
        r"prohibited us (.+?)(?:\.|$)",
    ]

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

    # Fallback based on content
    content_lower = text.lower()
    if "idol" in content_lower:
        return "We are prohibited from idolatry."
    elif "swear" in content_lower:
        return "We are prohibited from false oaths."
    elif "eat" in content_lower:
        return "We are prohibited from eating forbidden foods."
    elif "work" in content_lower and "sabbath" in content_lower:
        return "We are prohibited from Sabbath work."

    return "We are prohibited in this negative mitzvah."

def create_optimally_distributed_schedule():
    """Create the schedule with proper 1-2 entries per day distribution"""

    # Load the data
    sefer_data = load_sefer_hamitzvot()
    intros = sefer_data['text']['Shorashim']
    positive_mitzvot = sefer_data['text']['Positive Commandments']
    negative_mitzvot = sefer_data['text']['Negative Commandments']

    print(f"Loaded data:")
    print(f"- Introductions: {len(intros)}")
    print(f"- Positive Mitzvot: {len(positive_mitzvot)}")
    print(f"- Negative Mitzvot: {len(negative_mitzvot)}")
    print(f"- Total mitzvot: {len(positive_mitzvot) + len(negative_mitzvot)}")

    # Calculate distribution
    total_days = 350
    intro_days = len(intros)  # 14
    conclusion_days = 1
    mitzvot_days = total_days - intro_days - conclusion_days  # 335
    total_mitzvot = len(positive_mitzvot) + len(negative_mitzvot)  # 613

    # Calculate optimal distribution: 57 days with 1 mitzvah + 278 days with 2 mitzvot
    days_with_1 = 57
    days_with_2 = 278

    print(f"\nDistribution plan:")
    print(f"- Total days: {total_days}")
    print(f"- Introduction days: {intro_days}")
    print(f"- Mitzvot days: {mitzvot_days}")
    print(f"- Days with 1 mitzvah: {days_with_1}")
    print(f"- Days with 2 mitzvot: {days_with_2}")
    print(f"- Conclusion days: {conclusion_days}")

    # Date range
    start_date = datetime(2025, 10, 20)
    current_date = start_date

    schedule = []
    entry_number = 1

    # Phase 1: Introduction (14 days, 1 per day)
    print("\nPhase 1: Adding introductions...")
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

    # Phase 2: Mitzvot with optimal distribution (335 days)
    print("Phase 2: Adding mitzvot with optimal distribution...")

    # Combine all mitzvot in order: all positive first, then all negative
    all_mitzvot = []

    # Add all positive mitzvot
    for i in range(len(positive_mitzvot)):
        try:
            full_text = positive_mitzvot[i][0] if isinstance(positive_mitzvot[i], list) else positive_mitzvot[i]
            summary = extract_positive_summary(full_text)
        except:
            summary = f"We are commanded in positive mitzvah {i+1}."

        all_mitzvot.append({
            'type': 'Positive',
            'number': i + 1,
            'summary': summary,
            'link': f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{i+1}?lang=bi"
        })

    # Add all negative mitzvot
    for i in range(len(negative_mitzvot)):
        try:
            full_text = negative_mitzvot[i][0] if isinstance(negative_mitzvot[i], list) else negative_mitzvot[i]
            summary = extract_negative_summary(full_text)
        except:
            summary = f"We are prohibited in negative mitzvah {i+1}."

        all_mitzvot.append({
            'type': 'Negative',
            'number': i + 1,
            'summary': summary,
            'link': f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{i+1}?lang=bi"
        })

    # Distribute mitzvot across 335 days
    mitzvah_index = 0

    # Strategy: Start with days having 2 mitzvot, then finish with days having 1
    # This ensures we don't run out of mitzvot at the end

    for day in range(mitzvot_days):
        if day < days_with_2:
            # Days with 2 mitzvot (first 278 days)
            entries_today = 2
        else:
            # Days with 1 mitzvah (last 57 days)
            entries_today = 1

        for entry_in_day in range(entries_today):
            if mitzvah_index < len(all_mitzvot):
                mitzvah = all_mitzvot[mitzvah_index]
                schedule.append([
                    current_date.strftime('%Y-%m-%d'),
                    entry_number,
                    f"{mitzvah['type']} {mitzvah['number']}",
                    mitzvah['summary'],
                    mitzvah['link']
                ])
                entry_number += 1
                mitzvah_index += 1

        current_date += timedelta(days=1)

    # Phase 3: Conclusion (1 day)
    print("Phase 3: Adding conclusion...")
    schedule.append([
        current_date.strftime('%Y-%m-%d'),
        entry_number,
        "Conclusion",
        "Conclusion for Positive Commandments.",
        "https://www.sefaria.org/Sefer_HaMitzvot%2C_Conclusion_for_Positive_Commandments?lang=bi"
    ])

    print(f"\nSchedule created with {len(schedule)} total entries")
    print(f"Final date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Mitzvot processed: {mitzvah_index}/{len(all_mitzvot)}")

    return schedule

def save_schedule(schedule):
    """Save the schedule to CSV"""
    filename = 'Schedule_Complete_Sefer_HaMitzvos_Optimized.csv'

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link'])
        writer.writerows(schedule)

    print(f"Schedule saved to: {filename}")

    # Analyze the daily distribution
    from collections import defaultdict
    daily_counts = defaultdict(int)

    for row in schedule:
        date = row[0]
        daily_counts[date] += 1

    entries_per_day = list(daily_counts.values())
    days_with_1 = sum(1 for count in entries_per_day if count == 1)
    days_with_2 = sum(1 for count in entries_per_day if count == 2)
    days_with_other = sum(1 for count in entries_per_day if count not in [1, 2])

    print(f"\nFinal Distribution Analysis:")
    print(f"- Days with 1 entry: {days_with_1}")
    print(f"- Days with 2 entries: {days_with_2}")
    print(f"- Days with other: {days_with_other}")

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
    schedule = create_optimally_distributed_schedule()
    save_schedule(schedule)