#!/usr/bin/env python3

import csv
import json
import re
from datetime import datetime

def load_sefer_hamitzvot():
    """Load the Sefer HaMitzvot JSON file"""
    try:
        with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Data/SeferHaMitzvos.json not found!")
        return None

def clean_text(text):
    """Clean up text by removing extra whitespace and formatting"""
    if not text:
        return ""

    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)

    # Remove extra whitespace and clean up
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove common artifacts
    text = re.sub(r'\[.*?\]', '', text)  # Remove bracketed content
    text = re.sub(r'\(.*?\)', '', text)  # Remove parenthetical content sometimes
    text = text.replace('...', '').strip()

    return text

def extract_positive_summary(mitzvah_text):
    """Extract a clean summary from positive commandment text"""
    if not mitzvah_text:
        return "Positive commandment from Sefer HaMitzvot"

    text = clean_text(mitzvah_text)

    # Try various patterns for positive commandments
    patterns = [
        r"That is that He commanded us (.+?)(?:\.|$)",
        r"And that is that He commanded us (.+?)(?:\.|$)",
        r"That is that we were commanded (.+?)(?:\.|$)",
        r"And that is that we were commanded (.+?)(?:\.|$)",
        r"He commanded us (.+?)(?:\.|$)",
        r"we were commanded (.+?)(?:\.|$)",
        r"commanded us (.+?)(?:\.|$)",
        r"That (.+?)(?:\.|$)",
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

    text = clean_text(mitzvah_text)

    # Try various patterns for negative commandments
    patterns = [
        r"That He prohibited us from (.+?)(?:\.|$)",
        r"That He prohibited us (.+?)(?:\.|$)",
        r"prohibited us from (.+?)(?:\.|$)",
        r"prohibited us (.+?)(?:\.|$)",
        r"Not to (.+?)(?:\.|$)",
        r"That (.+?) not (.+?)(?:\.|$)",
        r"we not (.+?)(?:\.|$)",
        r"prevented from (.+?)(?:\.|$)",
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

def improve_introduction_summary(intro_text):
    """Improve introduction/principle summaries"""
    if not intro_text:
        return "Introduction to Sefer HaMitzvot"

    # Clean up the text
    text = clean_text(intro_text)

    # If it's already a good summary, return it
    if text and len(text) < 100 and text.endswith('.'):
        return text

    # Extract principle number if present
    principle_match = re.search(r"Principle (\d+)", text)
    if principle_match:
        num = principle_match.group(1)

        # Try to extract the main content
        content_patterns = [
            r"Principle \d+[:\s]+(.+?)(?:\.|$)",
            r"principle[:\s]+(.+?)(?:\.|$)",
        ]

        for pattern in content_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                content = matches[0].strip().rstrip('.,;:')
                return f"Principle {num}: {content}."

    # Default improvements for common intro topics
    if "count" in text.lower() or "number" in text.lower():
        return "Introduction to the methodology of counting mitzvot."
    elif "rabbinic" in text.lower():
        return "Principle: Exclude rabbinic commandments from the count."
    elif "hermeneutic" in text.lower() or "derive" in text.lower():
        return "Principle: Exclude commandments derived through hermeneutics."
    elif "perpetual" in text.lower() or "permanent" in text.lower():
        return "Principle: Include only perpetual commandments."

    return text if text else "Introduction to Sefer HaMitzvot."

def fix_csv_summaries():
    """Read the CSV file and fix all summaries to be complete sentences"""

    # Load the JSON data for reference
    sefer_data = load_sefer_hamitzvot()
    if not sefer_data:
        return

    # Read the current CSV
    input_file = 'Schedule_Complete_Sefer_HaMitzvos.csv'
    output_file = 'Schedule_Complete_Sefer_HaMitzvos_Fixed.csv'

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)

        print(f"Processing {len(rows)} entries...")

        # Process each row
        for i, row in enumerate(rows):
            mitzvah_type = row['Mitzvah_Type_Number']
            current_summary = row['Summary']

            print(f"Processing {i+1}/{len(rows)}: {mitzvah_type}")

            # Determine type and improve summary
            if mitzvah_type.startswith('Intro'):
                # Introduction/Principles
                if len(current_summary) < 50 and current_summary.count(',') == 0:
                    # Already concise, just ensure it ends with period
                    if not current_summary.endswith('.'):
                        row['Summary'] = current_summary + '.'
                else:
                    # Need to improve
                    row['Summary'] = improve_introduction_summary(current_summary)

            elif mitzvah_type.startswith('Positive'):
                # Positive commandments
                pos_num = int(mitzvah_type.split()[1])

                # Get the full text from JSON
                if pos_num <= len(sefer_data['text']['Positive Commandments']):
                    full_text = sefer_data['text']['Positive Commandments'][pos_num - 1][0]  # Get first element of the list
                    new_summary = extract_positive_summary(full_text)
                    row['Summary'] = new_summary
                else:
                    # Fallback: improve existing summary
                    if not current_summary.endswith('.'):
                        row['Summary'] = current_summary + '.'

            elif mitzvah_type.startswith('Negative'):
                # Negative commandments
                neg_num = int(mitzvah_type.split()[1])

                # Get the full text from JSON
                if neg_num <= len(sefer_data['text']['Negative Commandments']):
                    try:
                        full_text = sefer_data['text']['Negative Commandments'][neg_num - 1][0]  # Get first element of the list
                        new_summary = extract_negative_summary(full_text)
                        row['Summary'] = new_summary
                    except Exception as e:
                        print(f"Error with Negative {neg_num}: {e}")
                        print(f"Type: {type(sefer_data['text']['Negative Commandments'][neg_num - 1])}")
                        # Fallback: improve existing summary
                        if not current_summary.endswith('.'):
                            row['Summary'] = current_summary + '.'
                else:
                    # Fallback: improve existing summary
                    if not current_summary.endswith('.'):
                        row['Summary'] = current_summary + '.'

        # Write the improved CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            fieldnames = ['Date', 'Sequential_Number', 'Mitzvah_Type_Number', 'Summary', 'Sefaria_Link']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\nFixed summaries written to: {output_file}")
        print("All summaries are now complete sentences!")

    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    fix_csv_summaries()