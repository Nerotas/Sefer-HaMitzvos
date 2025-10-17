#!/usr/bin/env python3
"""
Extract all positive mitzvot from SeferHaMitzvos.json in order with simple descriptions
"""

import json
import re

def extract_simple_summary(text):
    """Extract a concise summary of each mitzvah."""
    if isinstance(text, list):
        text = text[0] if text else ""

    text = str(text).strip()

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Look for key phrases that indicate the mitzvah
    if "That is the command that He commanded us to believe in God" in text:
        return "To believe in God"
    elif "belief in [God's] unity" in text or "unity" in text:
        return "To believe in God's unity"
    elif "loving Him" in text:
        return "To love God"
    elif "believe in His awe" in text or "fear" in text:
        return "To fear God"
    elif "serve Him" in text and "prayer" in text:
        return "To serve God (prayer)"
    elif "associate with the sages" in text:
        return "To cling to Torah scholars"
    elif "swear by His name" in text:
        return "To swear by God's name when necessary"
    elif "imitate Him" in text:
        return "To emulate God's ways"
    elif "sanctify His name" in text:
        return "To sanctify God's name (Kiddush Hashem)"
    elif "recitation of Shema" in text:
        return "To recite Shema morning and evening"
    elif "study Torah" in text:
        return "To study and teach Torah"
    elif "head tefillin" in text:
        return "To wear tefillin on the head"
    elif "hand tefillin" in text:
        return "To bind tefillin on the arm"
    elif "tzitzit" in text or "fringes" in text:
        return "To wear tzitzit (fringes)"
    elif "mezuzah" in text:
        return "To affix mezuzah on doorposts"
    elif "assemble the people" in text:
        return "Hakhel - assembly every seven years"
    elif "king" in text and "Torah scroll" in text:
        return "King must write a Torah scroll"
    elif "write a Torah scroll" in text:
        return "To write a Torah scroll"
    elif "bless Him after eating" in text:
        return "To bless after eating (Birkat HaMazon)"
    elif "build a choice house" in text or "sanctuary" in text:
        return "To build the Temple"
    elif "fear this Temple" in text or "fear My sanctuary" in text:
        return "To revere the Temple"
    elif "guard the Temple" in text:
        return "To guard the Temple"
    elif "Levites" in text and "serve" in text:
        return "Levites to serve in the Temple"
    elif "wash their hands and feet" in text:
        return "Priests to sanctify hands and feet"
    elif "kindle the lamps" in text:
        return "To kindle the menorah"
    elif "bless Israel" in text:
        return "Priestly blessing"
    elif "bread of display" in text:
        return "To place showbread on the table"
    elif "burn incense" in text:
        return "To burn incense daily"
    elif "burn a fire on the altar" in text:
        return "To maintain fire on the altar"
    elif "remove the ashes" in text:
        return "To remove ashes from the altar"
    elif "send away the impure" in text:
        return "To send impure from the Temple"
    elif "honor the seed of Aharon" in text:
        return "To honor the priests"
    elif "priestly garments" in text:
        return "Priests to wear special garments"
    elif "carry the ark" in text:
        return "To carry the ark on shoulders"
    elif "anointing oil" in text:
        return "To make anointing oil"
    elif "serve in watches" in text:
        return "Priestly service in watches"
    elif "become impure for the relatives" in text:
        return "To mourn for relatives"
    elif "high priest to marry a virgin" in text:
        return "High priest to marry virgin"
    elif "two one-year old lambs" in text and "daily" in text:
        return "Daily offering (Tamid)"
    elif "griddle-cakes" in text or "grain offering" in text and "high priest" in text:
        return "High priest's daily grain offering"
    elif "Shabbat" in text and "sacrifice" in text:
        return "Additional Shabbat offering"
    elif "Rosh Chodesh" in text or "beginnings of your months" in text:
        return "Rosh Chodesh additional offering"
    elif "seven days of Pesach" in text:
        return "Pesach festival offerings"
    elif "grain offering of the omer" in text:
        return "Omer offering"
    elif "fiftieth day" in text and "Atzeret" in text:
        return "Shavuot additional offering"
    elif "two breads of chametz" in text:
        return "Two loaves offering on Shavuot"
    elif "first day of Tishrei" in text:
        return "Rosh Hashanah additional offering"
    elif "tenth day of Tishrei" in text:
        return "Yom Kippur additional offering"
    elif "service of the day" in text and "Yom Kippur" in text:
        return "Yom Kippur Temple service"
    elif "holiday of Sukkot" in text and "burnt-offering" in text:
        return "Sukkot festival offerings"
    elif "eighth day" in text and "Atzeret" in text:
        return "Shemini Atzeret offering"
    elif "ascend to the Temple three times" in text:
        return "Pilgrimage to Temple (Aliyah LaRegel)"
    elif "appear" in text and "festivals" in text:
        return "To appear before God on festivals"
    elif "rejoice in the festivals" in text:
        return "To rejoice on festivals"
    elif "slaughter the Pesach-offering" in text:
        return "To offer the Paschal lamb"

    # Fallback - extract first meaningful phrase
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence.startswith("That is that He commanded us"):
            # Try to extract the core command
            if " to " in sentence:
                parts = sentence.split(" to ", 1)
                if len(parts) > 1:
                    command = parts[1].strip()
                    # Clean up the command
                    command = re.sub(r'\([^)]*\)', '', command)  # Remove parenthetical references
                    command = command.split(',')[0]  # Take first part before comma
                    command = command.split('.')[0]  # Take first sentence
                    if len(command) > 5 and len(command) < 80:
                        return f"To {command}"

    return "Mitzvah from Sefer HaMitzvot"

def main():
    """Load and display all positive mitzvot."""

    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    positive_mitzvot = sefer_data['text']['Positive Commandments']

    print("SEFER HAMITZVOT - ALL 248 POSITIVE COMMANDMENTS")
    print("=" * 60)
    print(f"Total Positive Mitzvot: {len(positive_mitzvot)}")
    print()

    for i, mitzvah_text in enumerate(positive_mitzvot, 1):
        summary = extract_simple_summary(mitzvah_text)
        print(f"{i:3d}. {summary}")

    print()
    print("=" * 60)
    print(f"Total: {len(positive_mitzvot)} Positive Commandments")

if __name__ == "__main__":
    main()