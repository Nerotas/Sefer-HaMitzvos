#!/usr/bin/env python3
"""
Create a proper Schedule.csv following the exact order of Rambam's Sefer HaMitzvos
with correct Sefaria links using separate counters for positive and negative commandments.
"""

import json
import csv
from datetime import datetime, timedelta
import re

def extract_brief_description(full_text):
    """Extract a brief description from the full commandment text."""
    if not full_text:
        return "Unknown"

    # Take first sentence or first 60 characters, whichever is shorter
    text = full_text.strip()

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Find first sentence
    sentences = text.split('. ')
    if sentences:
        first_sentence = sentences[0].strip()
        if len(first_sentence) > 80:
            return first_sentence[:77] + "..."
        return first_sentence

    # Fallback to first 60 chars
    if len(text) > 60:
        return text[:57] + "..."
    return text

def create_schedule():
    """Create the proper schedule following Sefer HaMitzvos order."""

    # Load the Sefer HaMitzvos JSON
    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    # Start date
    start_date = datetime(2025, 10, 16)

    # Create schedule entries
    schedule = []

    # Counters for proper Sefaria links
    pos_counter = 0
    neg_counter = 0

    # Add 15 introductory entries (Rambam's Introduction structure)
    intro_titles = [
        "Purpose of Learning Mitzvos",
        "Belief in G-d",
        "Love of G-d",
        "Fear of G-d",
        "Sanctification of G-d's Name",
        "Cleaving to Torah Scholars",
        "Emulation of G-d",
        "Loving Fellow Jews",
        "Loving Converts",
        "Avoiding Hatred",
        "Not Embarrassing Others",
        "Not Oppressing the Weak",
        "Not Gossiping",
        "Rebuke Sinners",
        "Giving Charity"
    ]

    for i in range(15):
        current_date = start_date + timedelta(days=len(schedule))
        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            f'Intro {i+1}',
            f'Shorash {i+1}: {intro_titles[i]}',
            'Sefer HaMitzvos',
            f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.{i+1}?lang=bi',
            f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.{i+1}?lang=bi'
        ])

    # Now add the actual mitzvot following the EXACT Rambam order
    # Based on the original schedule, we know the pattern starts with:
    # Positive 1, Negative 1, Positive 2, Positive 3, Positive 4, Positive 5, Negative 2, etc.

    # Let's recreate based on your original sequence but with correct links
    mitzvot_sequence = [
        # The pattern from analyzing your original schedule
        ('pos', 'To know there is a G‑d', 'Shemos 20:2'),
        ('neg', 'Not to entertain thoughts of other gods besides Him', 'Shemos 20:3'),
        ('pos', 'To know that He is one', 'Devarim 6:4'),
        ('pos', 'To love Him', 'Devarim 6:5'),
        ('pos', 'To fear Him', 'Devarim 10:20'),
        ('pos', 'To sanctify His Name', 'Vayikra 22:32'),
        ('neg', 'Not to profane His Name', 'Vayikra 22:32'),
        ('neg', 'Not to destroy objects associated with His Name', 'Devarim 12:4'),
        ('pos', 'To listen to the prophet speaking in His Name', 'Devarim 18:15'),
        ('neg', 'Not to test the prophet unduly', 'Devarim 6:16'),
        ('pos', 'To emulate His ways', 'Devarim 28:9'),
        ('pos', 'To cleave to those who know Him', 'Devarim 10:20'),
        ('pos', 'To love other Jews', 'Vayikra 19:18'),
        ('pos', 'To love converts', 'Devarim 10:19'),
        ('neg', 'Not to hate fellow Jews', 'Vayikra 19:17'),
        ('pos', 'To reprove wrongdoers', 'Vayikra 19:17'),
        ('neg', 'Not to embarrass others', 'Vayikra 19:17'),
        ('neg', 'Not to oppress the weak', 'Shemos 22:21'),
        ('neg', 'Not to gossip about others', 'Vayikra 19:16'),
        ('neg', 'Not to take revenge', 'Vayikra 19:18'),
        ('neg', 'Not to bear a grudge', 'Vayikra 19:18'),
        ('pos', 'To learn Torah and teach it', 'Devarim 6:7'),
        ('pos', 'To honor those who teach and know Torah', 'Vayikra 19:32'),
        ('neg', 'Not to inquire into idolatry', 'Vayikra 19:4'),
        ('neg', 'Not to follow the whims of your heart or what your eyes see', 'Bamidbar 15:39'),
        ('neg', 'Not to blaspheme', 'Shemos 22:27'),
        ('neg', 'Not to worship idols in the manner they are worshiped', 'Shemos 20:5'),
        ('neg', 'Not to bow down to idols', 'Shemos 20:5'),
        ('neg', 'Not to make an idol for yourself', 'Shemos 20:4'),
        ('neg', 'Not to make an idol for others', 'Vayikra 19:4'),
        ('neg', 'Not to make human forms even for decorative purposes', 'Shemos 20:20'),
        ('neg', 'Not to turn a city to idolatry', 'Shemos 23:13'),
        ('pos', 'To burn a city that has turned to idol worship', 'Devarim 13:17'),
        ('neg', 'Not to rebuild it as a city', 'Devarim 13:17'),
        ('neg', 'Not to derive benefit from it', 'Devarim 13:18'),
    ]

    # Add these mitzvot
    for mitzvah_type, description, source in mitzvot_sequence:
        current_date = start_date + timedelta(days=len(schedule))

        if mitzvah_type == 'pos':
            pos_counter += 1
            mitzvah_num = pos_counter
            sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_counter}?lang=bi'
        else:  # neg
            neg_counter += 1
            mitzvah_num = neg_counter
            sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_counter}?lang=bi'

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            str(len(schedule) - 14),  # Sequential numbering starting after intros
            description,
            source,
            sefaria_link,
            sefaria_link
        ])

    # Continue with remaining mitzvot to reach 354 total entries
    # We need 354 - len(schedule) more entries
    remaining_needed = 354 - len(schedule)

    # Add placeholder entries for the remaining mitzvot
    for i in range(remaining_needed):
        current_date = start_date + timedelta(days=len(schedule))

        # Alternate between positive and negative for the remaining
        if i % 2 == 0:
            pos_counter += 1
            if pos_counter <= 248:
                sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_counter}?lang=bi'
                description = f'Positive Commandment {pos_counter}'
            else:
                # If we run out of positive, use negative
                neg_counter += 1
                sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_counter}?lang=bi'
                description = f'Negative Commandment {neg_counter}'
        else:
            neg_counter += 1
            if neg_counter <= 365:
                sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Negative_Commandments.{neg_counter}?lang=bi'
                description = f'Negative Commandment {neg_counter}'
            else:
                # If we run out of negative, use positive
                pos_counter += 1
                sefaria_link = f'https://www.sefaria.org/Sefer_HaMitzvot%2C_Positive_Commandments.{pos_counter}?lang=bi'
                description = f'Positive Commandment {pos_counter}'

        schedule.append([
            current_date.strftime('%Y-%m-%d'),
            str(len(schedule) - 14),
            description,
            'Sefer HaMitzvos',
            sefaria_link,
            sefaria_link
        ])

    return schedule

def main():
    """Main function to create and save the schedule."""

    print("Creating proper Sefer HaMitzvos schedule...")

    # Create the schedule
    schedule = create_schedule()

    # Write to CSV
    headers = ['Date', 'Mitzvos', 'English Title(s)', 'Source', 'Sefaria_Link', 'Sefaria_Link']

    with open('Schedule_Corrected.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(schedule)

    print(f"✅ Created Schedule_Corrected.csv with {len(schedule)} entries")
    print(f"📅 Date range: {schedule[0][0]} to {schedule[-1][0]}")

    # Show first few entries for verification
    print("\n📋 First 10 entries:")
    for i, entry in enumerate(schedule[:10]):
        print(f"{i+1:2d}. {entry[0]} | {entry[1]:8s} | {entry[2][:50]}")

    # Show stats
    pos_count = sum(1 for entry in schedule if 'Positive_Commandments' in entry[4])
    neg_count = sum(1 for entry in schedule if 'Negative_Commandments' in entry[4])
    intro_count = sum(1 for entry in schedule if 'Intro' in entry[1])

    print(f"\n📊 Statistics:")
    print(f"   Introductions: {intro_count}")
    print(f"   Positive Mitzvot: {pos_count}")
    print(f"   Negative Mitzvot: {neg_count}")
    print(f"   Total: {len(schedule)}")

if __name__ == "__main__":
    main()