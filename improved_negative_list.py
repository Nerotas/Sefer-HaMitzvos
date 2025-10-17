#!/usr/bin/env python3
"""
Extract all 365 negative mitzvot from SeferHaMitzvos.json with accurate descriptions
"""

import json
import re

def extract_negative_summary(text):
    """Extract a clear summary of each negative mitzvah."""
    if isinstance(text, list):
        text = text[0] if text else ""

    text = str(text).strip()

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Look for "That is that He prohibited us" or "That He prohibited us" pattern
    prohibited_patterns = [
        r'That (?:is that )?He prohibited us from ([^.]+)',
        r'That (?:is that )?He prohibited us ([^.]+)',
        r'That is that we (?:were )?prohibited from ([^.]+)',
    ]

    for pattern in prohibited_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            prohibition = match.group(1).strip()
            # Clean up the prohibition text
            prohibition = re.sub(r'may He be (?:exalted|blessed|elevated).*?[,\.]', '', prohibition)
            prohibition = re.sub(r'\([^)]*\)', '', prohibition)  # Remove parenthetical references
            prohibition = prohibition.split(',')[0].strip()  # Take first clause

            # Handle "from" prefix
            if prohibition.startswith('from '):
                prohibition = prohibition[5:]  # Remove "from "

            if len(prohibition) > 5 and len(prohibition) < 120:
                return f"Not to {prohibition}"

    # Look for specific patterns in the text for known mitzvot
    text_lower = text.lower()

    # Idolatry mitzvot (1-51)
    if "believing in a god besides him" in text_lower:
        return "Not to believe in other gods"
    elif "making an idol to serve" in text_lower:
        return "Not to make idols for yourself"
    elif "making an idol for those besides us" in text_lower:
        return "Not to make idols for others"
    elif "making images from wood" in text_lower or "making decorative shapes" in text_lower:
        return "Not to make decorative images"
    elif "bowing to an idol" in text_lower:
        return "Not to bow down to idols"
    elif "worshipping an idol" in text_lower or "serving it in the way" in text_lower:
        return "Not to worship idols"
    elif "swear by an idol" in text_lower:
        return "Not to swear by idols"
    elif "turn to idols" in text_lower:
        return "Not to turn to idolatry"
    elif "making a pillar" in text_lower:
        return "Not to erect a pillar for worship"
    elif "making a stone that is designed" in text_lower:
        return "Not to make carved stones for bowing"
    elif "plant a tree" in text_lower and "altar" in text_lower:
        return "Not to plant trees near the altar"
    elif "prophesy in the name of an idol" in text_lower:
        return "Not to prophesy in name of idols"
    elif "listen to one who prophesies" in text_lower and "idol" in text_lower:
        return "Not to listen to idolatrous prophets"
    elif "inciting" in text_lower and "idol" in text_lower:
        return "Not to incite others to idolatry"
    elif "entice a city" in text_lower:
        return "Not to entice a city to idolatry"
    elif "benefit from an enticed city" in text_lower:
        return "Not to benefit from a condemned city"
    elif "rebuild" in text_lower and "condemned city" in text_lower:
        return "Not to rebuild a condemned city"
    elif "attach something from an idol" in text_lower:
        return "Not to derive benefit from idols"
    elif "false prophet" in text_lower or "prophesy falsely" in text_lower:
        return "Not to prophesy falsely"
    elif "fear a false prophet" in text_lower:
        return "Not to fear a false prophet"
    elif "ov" in text_lower and "necromancy" in text_lower:
        return "Not to practice necromancy (Ov)"
    elif "yidoni" in text_lower:
        return "Not to practice Yidoni divination"
    elif "kosem" in text_lower or "soothsaying" in text_lower:
        return "Not to practice soothsaying"
    elif "nachash" in text_lower or "divining" in text_lower:
        return "Not to practice divination"
    elif "witchcraft" in text_lower or "sorcery" in text_lower:
        return "Not to practice witchcraft"
    elif "chover chaver" in text_lower:
        return "Not to practice Chover Chaver"
    elif "inquire of the dead" in text_lower:
        return "Not to inquire of the dead"
    elif "tattooing" in text_lower or "tattoo" in text_lower:
        return "Not to tattoo the body"
    elif "round the corners" in text_lower and "head" in text_lower:
        return "Not to round corners of the head"
    elif "destroy the corners" in text_lower and "beard" in text_lower:
        return "Not to destroy corners of beard"
    elif "gash" in text_lower and "dead" in text_lower:
        return "Not to gash oneself for the dead"
    elif "make a bald spot" in text_lower:
        return "Not to make bald spots for the dead"
    elif "dwelling in the land of egypt" in text_lower:
        return "Not to dwell permanently in Egypt"
    elif "stray after your heart" in text_lower:
        return "Not to stray after thoughts of the heart"
    elif "covenant with the seven nations" in text_lower:
        return "Not to make covenant with idolaters"
    elif "show favor" in text_lower and "idolaters" in text_lower:
        return "Not to show favor to idolaters"
    elif "settle in our land" in text_lower and "idolaters" in text_lower:
        return "Not to let idolaters settle in our land"
    elif "intermarriage" in text_lower or "marry them" in text_lower:
        return "Not to intermarry with idolaters"
    elif "men adorning themselves with women" in text_lower:
        return "Not for men to wear women's clothing"
    elif "women adorning themselves with men" in text_lower:
        return "Not for women to wear men's clothing"

    # Food prohibitions
    elif "eat blood" in text_lower:
        return "Not to eat blood"
    elif "eat fat" in text_lower and ("ox" in text_lower or "sheep" in text_lower):
        return "Not to eat forbidden fat (chelev)"
    elif "sciatic nerve" in text_lower:
        return "Not to eat the sciatic nerve"
    elif "torn by wild beasts" in text_lower or "neveilah" in text_lower:
        return "Not to eat torn flesh (neveilah)"
    elif "died by itself" in text_lower:
        return "Not to eat animals that died naturally"
    elif "limb from a living animal" in text_lower:
        return "Not to eat limb from living animal"
    elif "cook meat in milk" in text_lower:
        return "Not to cook meat in milk"
    elif "eat meat and milk together" in text_lower:
        return "Not to eat meat and milk together"
    elif "drink wine of libations" in text_lower:
        return "Not to drink wine used for idolatry"
    elif "gluttonous and rebellious" in text_lower:
        return "Not to eat as glutton and drunkard"
    elif "eat on yom kippur" in text_lower:
        return "Not to eat on Yom Kippur"
    elif "eat chametz on pesach" in text_lower:
        return "Not to eat chametz on Pesach"
    elif "eat leavened bread" in text_lower and "pesach" in text_lower:
        return "Not to eat leavened bread on Pesach"

    # Sabbath prohibitions
    elif "work on sabbath" in text_lower:
        return "Not to work on Sabbath"
    elif "travel beyond boundaries" in text_lower and "sabbath" in text_lower:
        return "Not to travel beyond Sabbath boundaries"

    # Temple and ritual prohibitions
    elif "enter the temple while impure" in text_lower:
        return "Not to enter Temple while impure"
    elif "serve in the temple while impure" in text_lower:
        return "Not to serve in Temple while impure"
    elif "eat sacred food while impure" in text_lower:
        return "Not to eat sacred food while impure"

    # Try fallback extraction from the beginning of the text
    first_sentence = text.split('.')[0].strip()
    if first_sentence.startswith("That is that He prohibited us"):
        # Try to extract the prohibition
        after_prohibited = first_sentence[len("That is that He prohibited us"):].strip()
        if after_prohibited.startswith("from "):
            after_prohibited = after_prohibited[5:]  # Remove "from "

        # Clean it up
        after_prohibited = re.sub(r'may He be (?:exalted|blessed|elevated).*', '', after_prohibited)
        after_prohibited = re.sub(r'\([^)]*\)', '', after_prohibited)
        after_prohibited = after_prohibited.strip()

        if len(after_prohibited) > 5 and len(after_prohibited) < 80:
            return f"Not to {after_prohibited}"

    return "Negative commandment from Sefer HaMitzvot"

def main():
    """Load and display all negative mitzvot with better descriptions."""

    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    negative_mitzvot = sefer_data['text']['Negative Commandments']

    print("SEFER HAMITZVOT - ALL 365 NEGATIVE COMMANDMENTS")
    print("=" * 70)
    print(f"Total Negative Mitzvot: {len(negative_mitzvot)}\n")

    # Show all negative mitzvot with improved descriptions
    for i, mitzvah_text in enumerate(negative_mitzvot, 1):
        summary = extract_negative_summary(mitzvah_text)
        print(f"{i:3d}. {summary}")

    print(f"\n{'='*70}")
    print(f"Complete list of all {len(negative_mitzvot)} Negative Commandments")
    print("These are the prohibitions from Rambam's Sefer HaMitzvot")

    # Count categories
    idolatry_count = sum(1 for i in range(51))  # First 51 are idolatry-related
    print(f"\nKey categories:")
    print(f"• Idolatry prohibitions: ~51 mitzvot (1-51)")
    print(f"• Dietary laws (kashrut): Multiple mitzvot")
    print(f"• Sabbath prohibitions: Multiple mitzvot")
    print(f"• Temple and ritual laws: Multiple mitzvot")
    print(f"• Interpersonal prohibitions: Multiple mitzvot")

if __name__ == "__main__":
    main()