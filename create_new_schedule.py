#!/usr/bin/env python3
"""
Create a new Sefer HaMitzvos schedule with the exact specifications:
- Start: 10/20/25, End: 10/04/26 (349 days total)
- Include introductions and conclusion (one day each)
- All 248 positive mitzvot, then all 365 negative mitzvot
- Start with one per day, increase to two per day as needed to fit timeline
- Output: date, sequential number, pos/neg number, summary, sefaria link
"""

import json
import csv
from datetime import datetime, timedelta
import re

def extract_summary(full_text):
    """Extract a concise summary from the full commandment text."""
    if not full_text:
        return "Unknown commandment"

    # Handle if it's a list (take first element)
    if isinstance(full_text, list):
        if len(full_text) > 0:
            text = str(full_text[0])
        else:
            return "Unknown commandment"
    else:
        text = str(full_text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()

    # Look for key phrases that indicate the main commandment
    if "That is that He commanded us" in text:
        # Find the main action after this phrase
        start = text.find("That is that He commanded us")
        if start != -1:
            remaining = text[start:start+200]
            sentences = remaining.split('. ')
            if len(sentences) > 0:
                first_sentence = sentences[0].strip()
                # Clean up and make it concise
                summary = first_sentence.replace("That is that He commanded us", "To").strip()
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                return summary

    # Look for "That is that He prohibited us"
    if "That He prohibited us" in text:
        start = text.find("That He prohibited us")
        if start != -1:
            remaining = text[start:start+200]
            sentences = remaining.split('. ')
            if len(sentences) > 0:
                first_sentence = sentences[0].strip()
                summary = first_sentence.replace("That He prohibited us", "Not to").strip()
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                return summary

    # Fallback: take first sentence
    sentences = text.split('. ')
    if sentences:
        first_sentence = sentences[0].strip()
        if len(first_sentence) > 80:
            return first_sentence[:77] + "..."
        return first_sentence

    # Last resort
    if len(text) > 80:
        return text[:77] + "..."
    return text

def create_schedule():
    """Create the schedule according to specifications."""

    # Load the Sefer HaMitzvos JSON
    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    # Date range: 10/20/25 to 10/04/26
    start_date = datetime(2025, 10, 20)
    end_date = datetime(2026, 10, 4)
    total_days = (end_date - start_date).days + 1

    print(f"Total days available: {total_days}")

    # Count what we need to fit
    positive_mitzvot = sefer_data['text']['Positive Commandments']
    negative_mitzvot = sefer_data['text']['Negative Commandments']

    # Introductions (we'll use about 14 key principles)
    intro_count = 14
    conclusion_count = 1

    total_mitzvot = len(positive_mitzvot) + len(negative_mitzvot)
    total_items = intro_count + total_mitzvot + conclusion_count

    print(f"Items to schedule:")
    print(f"  Introductions: {intro_count}")
    print(f"  Positive Mitzvot: {len(positive_mitzvot)}")
    print(f"  Negative Mitzvot: {len(negative_mitzvot)}")
    print(f"  Conclusion: {conclusion_count}")
    print(f"  Total: {total_items}")

    # Calculate distribution
    mitzvot_days = total_days - intro_count - conclusion_count
    print(f"Days available for mitzvot: {mitzvot_days}")

    # Determine how many mitzvot per day needed
    avg_per_day = total_mitzvot / mitzvot_days
    print(f"Average mitzvot per day needed: {avg_per_day:.2f}")

    schedule = []
    current_date = start_date
    sequential_counter = 1

    # Add introductions (14 key principles)
    intro_titles = [
        "Introduction to Counting the Mitzvot",
        "Principle 1: Not to count rabbinic commandments",
        "Principle 2: Not to count derived laws",
        "Principle 3: Not to count temporary commandments",
        "Principle 4: Not to count general Torah commands",
        "Principle 5: Not to count reasons as separate mitzvot",
        "Principle 6: Count positive and negative parts separately",
        "Principle 7: Not to count details of commandments",
        "Principle 8: Not to count negation of positive commandments",
        "Principle 9: Count the substance, not the statements",
        "Principle 10: Not to count preliminaries",
        "Principle 11: Not to count parts of unified commandments",
        "Principle 12: Not to count parts of work processes",
        "Principle 13: Count by substance, not by repetition"
    ]

    for i, title in enumerate(intro_titles):
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            sequential_counter,
            f"Intro {i+1}",
            title,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.{i+1}?lang=bi"
        ])
        current_date += timedelta(days=1)
        sequential_counter += 1

    # Process positive mitzvot
    pos_counter = 1
    for mitzvah_text in positive_mitzvot:
        summary = extract_summary(mitzvah_text)

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            sequential_counter,
            f"Positive {pos_counter}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_counter}?lang=bi"
        ])

        pos_counter += 1
        sequential_counter += 1

        # Determine if we need to add another mitzvah today
        remaining_mitzvot = total_mitzvot - (sequential_counter - intro_count - 1)
        remaining_days = mitzvot_days - (sequential_counter - intro_count - 1) // 2  # Rough estimate

        if remaining_days > 0 and remaining_mitzvot / remaining_days > 1.5:
            # Add a second positive mitzvah if we have more
            if pos_counter <= len(positive_mitzvot):
                mitzvah_text = positive_mitzvot[pos_counter - 1]
                summary = extract_summary(mitzvah_text)

                schedule.append([
                    current_date.strftime('%Y-%m-%d'),
                    sequential_counter,
                    f"Positive {pos_counter}",
                    summary,
                    f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_counter}?lang=bi"
                ])
                pos_counter += 1
                sequential_counter += 1

        current_date += timedelta(days=1)

    # Process negative mitzvot
    neg_counter = 1
    for mitzvah_text in negative_mitzvot:
        summary = extract_summary(mitzvah_text)

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            sequential_counter,
            f"Negative {neg_counter}",
            summary,
            f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_counter}?lang=bi"
        ])

        neg_counter += 1
        sequential_counter += 1

        # Check if we need to fit more mitzvot per day
        remaining_mitzvot = len(negative_mitzvot) - neg_counter + 1
        remaining_days = (end_date - current_date).days

        if remaining_days > 1 and remaining_mitzvot > 0 and remaining_mitzvot / remaining_days > 1.2:
            # Add a second negative mitzvah if we have more and need to catch up
            if neg_counter <= len(negative_mitzvot):
                mitzvah_text = negative_mitzvot[neg_counter - 1]
                summary = extract_summary(mitzvah_text)

                schedule.append([
                    current_date.strftime('%Y-%m-%d'),
                    sequential_counter,
                    f"Negative {neg_counter}",
                    summary,
                    f"https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_counter}?lang=bi"
                ])
                neg_counter += 1
                sequential_counter += 1

        current_date += timedelta(days=1)

        # Safety check - don't go past end date
        if current_date > end_date:
            break

    # Add conclusion on the final day
    if current_date <= end_date:
        schedule.append([
            end_date.strftime('%Y-%m-%d'),
            sequential_counter,
            "Conclusion",
            "Conclusion of the Sefer HaMitzvot",
            "https://www.sefaria.org/Sefer_HaMitzvot%2C_Conclusion_for_Positive_Commandments?lang=bi"
        ])

    return schedule

def main():
    """Main function to create and save the schedule."""

    print("Creating new Sefer HaMitzvos schedule with exact specifications...")
    print("=" * 60)

    # Create the schedule
    schedule = create_schedule()

    # Write to CSV
    headers = ['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link']

    filename = 'Schedule_New_Sefer_HaMitzvos.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(schedule)

    print(f"✅ Created {filename} with {len(schedule)} entries")
    print(f"📅 Date range: {schedule[0][0]} to {schedule[-1][0]}")

    # Show first few entries for verification
    print("\n📋 First 15 entries:")
    print(f"{'#':<3} {'Date':<12} {'Type':<12} {'Summary':<50}")
    print("-" * 80)
    for i, entry in enumerate(schedule[:15]):
        print(f"{entry[1]:<3} {entry[0]:<12} {entry[2]:<12} {entry[3][:47]:<50}")

    # Show some positive mitzvot
    print("\n📋 Sample positive mitzvot:")
    pos_entries = [entry for entry in schedule if 'Positive' in entry[2]][:5]
    for entry in pos_entries:
        print(f"{entry[1]:<3} {entry[0]:<12} {entry[2]:<12} {entry[3][:47]:<50}")

    # Show some negative mitzvot
    print("\n📋 Sample negative mitzvot:")
    neg_entries = [entry for entry in schedule if 'Negative' in entry[2]][:5]
    for entry in neg_entries:
        print(f"{entry[1]:<3} {entry[0]:<12} {entry[2]:<12} {entry[3][:47]:<50}")

    # Show final entries
    print("\n📋 Final entries:")
    for entry in schedule[-3:]:
        print(f"{entry[1]:<3} {entry[0]:<12} {entry[2]:<12} {entry[3][:47]:<50}")

    # Statistics
    intro_count = sum(1 for entry in schedule if 'Intro' in entry[2])
    pos_count = sum(1 for entry in schedule if 'Positive' in entry[2])
    neg_count = sum(1 for entry in schedule if 'Negative' in entry[2])
    conclusion_count = sum(1 for entry in schedule if 'Conclusion' in entry[2])

    print(f"\n📊 Final Statistics:")
    print(f"   Introductions: {intro_count}")
    print(f"   Positive Mitzvot: {pos_count}")
    print(f"   Negative Mitzvot: {neg_count}")
    print(f"   Conclusions: {conclusion_count}")
    print(f"   Total Entries: {len(schedule)}")
    print(f"   Target Days: 349 (Oct 20, 2025 - Oct 4, 2026)")

if __name__ == "__main__":
    main()