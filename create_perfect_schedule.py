#!/usr/bin/env python3
"""
Final Sefer HaMitzvos schedule - ensures all 613 mitzvot are covered
Start: 10/20/25, End: 10/04/26 (350 days)
Structure: 14 introductions + all 248 positive + all 365 negative + 1 conclusion
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
    # Remove HTML tags and clean up
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()

    # Extract meaningful content
    if "That is the command that He commanded us" in text:
        # Positive commandment patterns
        if "believe in God" in text:
            return "To believe in God"
        elif "belief in [God's] unity" in text or "unity" in text:
            return "To believe in God's unity"
        elif "loving Him" in text:
            return "To love God"
        elif "believe in His awe" in text or "fear" in text:
            return "To fear God"
        elif "serve Him" in text or "prayer" in text:
            return "To serve God (prayer)"
        elif "associate with the sages" in text:
            return "To cling to Torah scholars"
        elif "swear by His name" in text:
            return "To swear by God's name when necessary"
        elif "imitate Him" in text:
            return "To emulate God's ways"
        elif "sanctify His name" in text:
            return "To sanctify God's name"
        elif "Shema" in text:
            return "To recite Shema morning and evening"
        elif "study Torah" in text or "learn" in text:
            return "To study and teach Torah"
        elif "tefillin" in text and "head" in text:
            return "To wear tefillin on the head"
        elif "tefillin" in text and "arm" in text:
            return "To bind tefillin on the arm"

    elif "prohibited us" in text or "That He prohibited us" in text:
        # Negative commandment patterns
        if "believing in a god besides" in text or "other god" in text:
            return "Not to believe in other gods"
        elif "making an idol" in text and "serve" in text:
            return "Not to make idols for yourself"
        elif "making an idol" in text and "others" in text:
            return "Not to make idols for others"
        elif "making images" in text or "decorative" in text:
            return "Not to make decorative images"
        elif "bowing to an idol" in text:
            return "Not to bow down to idols"
        elif "worshipping an idol" in text:
            return "Not to worship idols"

    # Fallback - extract first meaningful sentence
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10 and not sentence.startswith('That is'):
            return sentence[:70] + ("..." if len(sentence) > 70 else "")

    return "Commandment from Sefer HaMitzvot"

def create_perfect_schedule():
    """Create schedule that covers all mitzvot exactly."""

    # Load the Sefer HaMitzvos data
    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    positive_mitzvot = sefer_data['text']['Positive Commandments']
    negative_mitzvot = sefer_data['text']['Negative Commandments']

    print(f"Loaded {len(positive_mitzvot)} positive and {len(negative_mitzvot)} negative mitzvot")

    # Date setup
    start_date = datetime(2025, 10, 20)
    end_date = datetime(2026, 10, 4)
    total_days = (end_date - start_date).days + 1
    print(f"Total days available: {total_days}")

    schedule = []
    current_date = start_date

    # Phase 1: 14 Introductions (one per day)
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

    print(f"After introductions, starting mitzvot on {current_date.strftime('%Y-%m-%d')}")

    # Phase 2: All 248 Positive Mitzvot
    # We have 335 days left for mitzvot (350 - 14 intros - 1 conclusion)
    # Let's allocate 125 days for positives (about 2 per day)
    days_for_positives = 125

    pos_index = 0
    for day in range(days_for_positives):
        if pos_index >= len(positive_mitzvot):
            break

        # First mitzvah of the day
        summary = clean_text(positive_mitzvot[pos_index])
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            len(schedule) + 1,
            f"Positive {pos_index + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_index + 1}?lang=bi"
        ])
        pos_index += 1

        # Second mitzvah if we still have more to cover
        if pos_index < len(positive_mitzvot):
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

    print(f"Completed {pos_index}/{len(positive_mitzvot)} positive mitzvot")
    print(f"Starting negative mitzvot on {current_date.strftime('%Y-%m-%d')}")

    # Phase 3: All 365 Negative Mitzvot
    # Calculate remaining days
    days_until_end = (end_date - current_date).days
    days_for_negatives = days_until_end - 1  # Save last day for conclusion

    print(f"Days available for negative mitzvot: {days_for_negatives}")

    neg_index = 0
    for day in range(days_for_negatives):
        if neg_index >= len(negative_mitzvot):
            break

        # First negative mitzvah of the day
        summary = clean_text(negative_mitzvot[neg_index])
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            len(schedule) + 1,
            f"Negative {neg_index + 1}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_index + 1}?lang=bi"
        ])
        neg_index += 1

        # Second negative mitzvah if needed to fit them all
        remaining_days = days_for_negatives - day - 1
        remaining_mitzvot = len(negative_mitzvot) - neg_index

        if remaining_days > 0 and remaining_mitzvot > remaining_days and neg_index < len(negative_mitzvot):
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

    print(f"Completed {neg_index}/{len(negative_mitzvot)} negative mitzvot")

    # Phase 4: Conclusion on the last day
    schedule.append([
        end_date.strftime('%Y-%m-%d'),
        len(schedule) + 1,
        "Conclusion",
        "Completion of Sefer HaMitzvot study cycle",
        "https://www.sefaria.org/Sefer_HaMitzvot?lang=bi"
    ])

    return schedule

def main():
    """Generate the final perfect schedule."""

    print("Creating FINAL Sefer HaMitzvos Schedule")
    print("=" * 50)

    schedule = create_perfect_schedule()

    # Save to CSV
    headers = ['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link']
    filename = 'Schedule_Final_Sefer_HaMitzvos.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(schedule)

    print(f"\n✅ Created: {filename}")
    print(f"📅 Total entries: {len(schedule)}")
    print(f"📅 Date range: {schedule[0][0]} to {schedule[-1][0]}")

    # Final statistics
    intros = sum(1 for x in schedule if 'Intro' in x[2])
    positives = sum(1 for x in schedule if 'Positive' in x[2])
    negatives = sum(1 for x in schedule if 'Negative' in x[2])
    conclusions = sum(1 for x in schedule if 'Conclusion' in x[2])

    print(f"\n📊 FINAL BREAKDOWN:")
    print(f"   Introductions: {intros}")
    print(f"   Positive Mitzvot: {positives} (target: 248)")
    print(f"   Negative Mitzvot: {negatives} (target: 365)")
    print(f"   Conclusions: {conclusions}")
    print(f"   TOTAL: {intros + positives + negatives + conclusions}")

    # Show key samples
    print(f"\n📋 Sample entries:")
    for i in [0, 14, 15, len(schedule)//2, -2, -1]:
        if 0 <= i < len(schedule):
            entry = schedule[i]
            print(f"  #{entry[1]:3d} {entry[0]} | {entry[2]:15s} | {entry[3][:50]}")

if __name__ == "__main__":
    main()