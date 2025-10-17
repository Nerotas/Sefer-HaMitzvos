#!/usr/bin/env python3
"""
Create a proper Sefer HaMitzvos schedule:
- Start: 10/20/25, End: 10/04/26 (350 days)
- Include 14 introductions, all 248 positive, all 365 negative mitzvot, 1 conclusion
- Distribute evenly with some days having 2 mitzvot when needed
"""

import json
import csv
from datetime import datetime, timedelta
import re

def clean_text(text):
    """Clean and extract key information from mitzvah text."""
    if isinstance(text, list):
        text = text[0] if text else ""

    text = str(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()

    # Extract the main commandment description
    if "That is the command that He commanded us" in text:
        # For positive commandments
        start = text.find("That is the command that He commanded us")
        if start != -1:
            segment = text[start:start+150]
            if "believe in God" in segment:
                return "To believe in God"
            elif "belief in [God's] unity" in segment:
                return "To believe in God's unity"
            elif "loving Him" in segment:
                return "To love God"
            elif "believe in His awe" in segment:
                return "To fear God"
            elif "serve Him" in segment:
                return "To serve God (prayer)"
            elif "associate with the sages" in segment:
                return "To cling to Torah scholars"
            elif "swear by His name" in segment:
                return "To swear by God's name when necessary"
            elif "imitate Him" in segment:
                return "To emulate God's ways"
            elif "sanctify His name" in segment:
                return "To sanctify God's name (Kiddush Hashem)"
            elif "read the recitation of Shema" in segment:
                return "To recite Shema morning and evening"
            elif "study Torah" in segment:
                return "To study and teach Torah"
            elif "put on the head tefillin" in segment:
                return "To wear tefillin on the head"

    elif "That He prohibited us" in text or "That is that He prohibited us" in text:
        # For negative commandments
        if "believing in a god besides Him" in text:
            return "Not to believe in other gods"
        elif "making an idol to serve" in text:
            return "Not to make idols for yourself"
        elif "making an idol for those besides us" in text:
            return "Not to make idols for others"
        elif "making images from wood" in text:
            return "Not to make decorative images"
        elif "bowing to an idol" in text:
            return "Not to bow down to idols"
        elif "worshipping an idol" in text:
            return "Not to worship idols in their manner"

    # Fallback - take first meaningful sentence
    sentences = text.split('.')
    if sentences:
        first = sentences[0].strip()
        if len(first) > 5:  # Avoid empty or very short strings
            return first[:60] + ("..." if len(first) > 60 else "")

    return "Commandment from Sefer HaMitzvot"

def create_comprehensive_schedule():
    """Create the complete schedule with proper distribution."""

    # Load data
    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    positive_mitzvot = sefer_data['text']['Positive Commandments']
    negative_mitzvot = sefer_data['text']['Negative Commandments']

    # Date parameters
    start_date = datetime(2025, 10, 20)
    end_date = datetime(2026, 10, 4)
    total_days = (end_date - start_date).days + 1

    print(f"Creating schedule for {total_days} days")
    print(f"Positive mitzvot: {len(positive_mitzvot)}")
    print(f"Negative mitzvot: {len(negative_mitzvot)}")

    schedule = []
    current_date = start_date

    # Phase 1: Introductions (14 days)
    intro_titles = [
        "Introduction to Counting the Mitzvot",
        "Principle 1: Not rabbinic commandments",
        "Principle 2: Not derived through hermeneutics",
        "Principle 3: Only perpetual commandments",
        "Principle 4: Not general Torah commands",
        "Principle 5: Not reasons as separate mitzvot",
        "Principle 6: Separate positive and negative",
        "Principle 7: Not details of commandments",
        "Principle 8: Not negation of positive commands",
        "Principle 9: Count substance, not statements",
        "Principle 10: Not preliminaries to commandments",
        "Principle 11: Not parts of unified commandments",
        "Principle 12: Not work process components",
        "Principle 13: Not repetition-based counting"
    ]

    for i, title in enumerate(intro_titles):
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            len(schedule) + 1,
            f"Intro {i+1}",
            title,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.{i+1}?lang=bi"
        ])
        current_date += timedelta(days=1)

    # Phase 2: All Positive Mitzvot (248 total)
    print(f"Starting positive mitzvot on {current_date.strftime('%Y-%m-%d')}")

    # Calculate optimal distribution: 350 total days - 14 intros - 1 conclusion = 335 days for mitzvot
    # Need to fit 248 positive + 365 negative = 613 total mitzvot in 335 days
    total_mitzvot_days = 335
    positive_ratio = len(positive_mitzvot) / (len(positive_mitzvot) + len(negative_mitzvot))
    days_for_positives = int(total_mitzvot_days * positive_ratio) + 5  # About 135 days for positives

    pos_per_day = len(positive_mitzvot) / days_for_positives
    print(f"Positive mitzvot per day: {pos_per_day:.2f}")

    pos_index = 0
    pos_day_count = 0
    while pos_index < len(positive_mitzvot) and pos_day_count < days_for_positives:

        # Add first positive mitzvah for the day
        summary = clean_text(positive_mitzvot[pos_index])
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            len(schedule) + 1,
            f"Positive {pos_index + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_index + 1}?lang=bi"
        ])
        pos_index += 1

        # Add second positive mitzvah if we need to catch up
        if pos_per_day > 1.8 and pos_index < len(positive_mitzvot):
            summary = clean_text(positive_mitzvot[pos_index])
            schedule.append([
                current_date.strftime('%Y-%m-%d'),
                len(schedule) + 1,
                f"Positive {pos_index + 1}",
                summary,
                f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_index + 1}?lang=bi"
            ])
            pos_index += 1

        current_date += timedelta(days=1)
        pos_day_count += 1

    # Phase 3: All Negative Mitzvot (365 total)
    print(f"Starting negative mitzvot on {current_date.strftime('%Y-%m-%d')}")
    print(f"Positive mitzvot completed: {pos_index}/{len(positive_mitzvot)}")

    # Calculate remaining days for negatives
    days_until_end = (end_date - current_date).days
    days_for_negatives = days_until_end - 1  # Leave 1 day for conclusion

    neg_per_day = len(negative_mitzvot) / days_for_negatives
    print(f"Negative mitzvot per day: {neg_per_day:.2f}")

    neg_index = 0
    neg_day_count = 0
    while neg_index < len(negative_mitzvot) and neg_day_count < days_for_negatives:

        # Add first negative mitzvah for the day
        summary = clean_text(negative_mitzvot[neg_index])
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            len(schedule) + 1,
            f"Negative {neg_index + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_index + 1}?lang=bi"
        ])
        neg_index += 1

        # Add second negative mitzvah if we need to fit them all
        if neg_per_day > 1.8 and neg_index < len(negative_mitzvot):
            summary = clean_text(negative_mitzvot[neg_index])
            schedule.append([
                current_date.strftime('%Y-%m-%d'),
                len(schedule) + 1,
                f"Negative {neg_index + 1}",
                summary,
                f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_index + 1}?lang=bi"
            ])
            neg_index += 1

        current_date += timedelta(days=1)
        neg_day_count += 1    # Phase 4: Conclusion
    schedule.append([
        end_date.strftime('%Y-%m-%d'),
        len(schedule) + 1,
        "Conclusion",
        "Completion of Sefer HaMitzvot study",
        "https://www.sefaria.org/Sefer_HaMitzvot%2C_Conclusion_for_Positive_Commandments?lang=bi"
    ])

    return schedule

def main():
    """Main execution function."""

    print("Creating comprehensive Sefer HaMitzvos schedule...")
    print("=" * 60)

    schedule = create_comprehensive_schedule()

    # Save to CSV
    headers = ['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link']
    filename = 'Schedule_Complete_Sefer_HaMitzvos.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(schedule)

    print(f"✅ Created {filename}")
    print(f"📅 Total entries: {len(schedule)}")
    print(f"📅 Date range: {schedule[0][0]} to {schedule[-1][0]}")

    # Statistics
    intros = sum(1 for x in schedule if 'Intro' in x[2])
    positives = sum(1 for x in schedule if 'Positive' in x[2])
    negatives = sum(1 for x in schedule if 'Negative' in x[2])
    conclusions = sum(1 for x in schedule if 'Conclusion' in x[2])

    print(f"\n📊 Content breakdown:")
    print(f"   Introductions: {intros}")
    print(f"   Positive Mitzvot: {positives}")
    print(f"   Negative Mitzvot: {negatives}")
    print(f"   Conclusions: {conclusions}")

    # Show samples
    print(f"\n📋 First 10 entries:")
    for i in range(min(10, len(schedule))):
        entry = schedule[i]
        print(f"  {entry[1]:3d}. {entry[0]} | {entry[2]:12s} | {entry[3][:40]}")

    # Show transition points
    first_pos = next((i for i, x in enumerate(schedule) if 'Positive 1' in x[2]), None)
    first_neg = next((i for i, x in enumerate(schedule) if 'Negative 1' in x[2]), None)

    if first_pos:
        print(f"\n📋 First positive mitzvah (entry #{first_pos + 1}):")
        entry = schedule[first_pos]
        print(f"  {entry[1]:3d}. {entry[0]} | {entry[2]:12s} | {entry[3]}")

    if first_neg:
        print(f"\n📋 First negative mitzvah (entry #{first_neg + 1}):")
        entry = schedule[first_neg]
        print(f"  {entry[1]:3d}. {entry[0]} | {entry[2]:12s} | {entry[3]}")

if __name__ == "__main__":
    main()