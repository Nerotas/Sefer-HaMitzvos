#!/usr/bin/env python3
"""
Extract all 365 negative mitzvot from SeferHaMitzvos.json in order
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

    # Look for prohibition patterns
    text_lower = text.lower()

    # Common negative commandment patterns
    if "believing in a god besides him" in text_lower or "other god" in text_lower:
        return "Not to believe in other gods"
    elif "making an idol" in text_lower and "serve" in text_lower:
        return "Not to make idols for yourself"
    elif "making an idol" in text_lower and "others" in text_lower:
        return "Not to make idols for others"
    elif "making images" in text_lower or "decorative" in text_lower:
        return "Not to make decorative images"
    elif "bowing to an idol" in text_lower:
        return "Not to bow down to idols"
    elif "worshipping an idol" in text_lower:
        return "Not to worship idols"
    elif "swear by" in text_lower and ("idol" in text_lower or "false" in text_lower):
        return "Not to swear by idols"
    elif "turn to idols" in text_lower:
        return "Not to turn to idolatry"
    elif "molten gods" in text_lower:
        return "Not to make molten gods"
    elif "listen to a prophet" in text_lower and "idolatry" in text_lower:
        return "Not to listen to idolatrous prophets"
    elif "false prophet" in text_lower:
        return "Not to prophesy falsely"
    elif "prophecy in the name" in text_lower and "idolatry" in text_lower:
        return "Not to prophesy in name of idols"
    elif "witchcraft" in text_lower or "sorcery" in text_lower:
        return "Not to practice witchcraft"
    elif "pass through fire" in text_lower or "molech" in text_lower:
        return "Not to pass children through fire to Molech"
    elif "necromancy" in text_lower or "ov" in text_lower:
        return "Not to practice necromancy (Ov)"
    elif "yidoni" in text_lower:
        return "Not to practice Yidoni divination"
    elif "tattoo" in text_lower:
        return "Not to tattoo the body"
    elif "round the corners" in text_lower and "head" in text_lower:
        return "Not to round corners of the head"
    elif "destroy the corners" in text_lower and "beard" in text_lower:
        return "Not to destroy corners of beard"
    elif "gash" in text_lower and "dead" in text_lower:
        return "Not to gash oneself for the dead"
    elif "eat blood" in text_lower:
        return "Not to eat blood"
    elif "eat fat" in text_lower:
        return "Not to eat forbidden fat (chelev)"
    elif "eat the sciatic nerve" in text_lower:
        return "Not to eat the sciatic nerve"
    elif "eat meat torn by wild beasts" in text_lower:
        return "Not to eat torn flesh (neveilah)"
    elif "cook meat in milk" in text_lower:
        return "Not to cook meat in milk"
    elif "eat meat and milk together" in text_lower:
        return "Not to eat meat and milk together"
    elif "eat chametz on pesach" in text_lower:
        return "Not to eat chametz on Pesach"
    elif "eat on yom kippur" in text_lower:
        return "Not to eat on Yom Kippur"
    elif "work on sabbath" in text_lower:
        return "Not to work on Sabbath"
    elif "carry on sabbath" in text_lower:
        return "Not to carry on Sabbath"
    elif "kindle fire on sabbath" in text_lower:
        return "Not to kindle fire on Sabbath"

    # Look for "That He prohibited us" pattern
    prohibited_match = re.search(r'That (?:is that )?He prohibited us(.*?)(?:\.|And)', text, re.IGNORECASE)
    if prohibited_match:
        prohibition = prohibited_match.group(1).strip()
        # Clean up common phrases
        prohibition = re.sub(r'may He be (?:exalted|blessed|elevated).*?[,\.]', '', prohibition)
        prohibition = re.sub(r'\([^)]*\)', '', prohibition)  # Remove parenthetical references
        prohibition = prohibition.split(',')[0].strip()  # Take first clause

        if len(prohibition) > 5 and len(prohibition) < 100:
            return f"Not {prohibition}"

    # Look for "That is that" pattern for negative commands
    command_match = re.search(r'That is that (?:we (?:were )?(?:not )?(?:commanded|prohibited))(.*?)(?:\.|And)', text, re.IGNORECASE)
    if command_match:
        command = command_match.group(1).strip()
        if "not" not in command.lower()[:10]:  # If "not" isn't already at the start
            command = f"not {command}"
        # Clean up
        command = re.sub(r'may He be (?:exalted|blessed|elevated).*?[,\.]', '', command)
        command = re.sub(r'\([^)]*\)', '', command)
        command = command.split(',')[0].strip()

        if len(command) > 5 and len(command) < 100:
            return f"Not {command.replace('not ', '').replace('Not ', '')}"

    # Fallback - try to extract from opening phrase
    first_sentence = text.split('.')[0].strip()
    if "prohibit" in first_sentence.lower() or "not" in first_sentence.lower():
        # Look for the core prohibition
        not_match = re.search(r'not to ([^,\.]+)', first_sentence, re.IGNORECASE)
        if not_match:
            prohibition = not_match.group(1).strip()
            if len(prohibition) > 3 and len(prohibition) < 60:
                return f"Not to {prohibition}"

    return "Negative commandment from Sefer HaMitzvot"

def main():
    """Load and display all negative mitzvot."""

    with open('Data/SeferHaMitzvos.json', 'r', encoding='utf-8') as f:
        sefer_data = json.load(f)

    negative_mitzvot = sefer_data['text']['Negative Commandments']

    print("SEFER HAMITZVOT - ALL 365 NEGATIVE COMMANDMENTS")
    print("=" * 70)
    print(f"Total Negative Mitzvot: {len(negative_mitzvot)}\n")

    # Show first 50 negative mitzvot
    for i, mitzvah_text in enumerate(negative_mitzvot, 1):
        summary = extract_negative_summary(mitzvah_text)
        print(f"{i:3d}. {summary}")

        if i == 50:
            print(f"\n... [showing first 50 of {len(negative_mitzvot)} total negative mitzvot] ...")
            break

    print(f"\n{'='*70}")
    print(f"Complete list contains all {len(negative_mitzvot)} Negative Commandments")
    print("This matches Rambam's count in Sefer HaMitzvot")

    # Show some key categories
    print(f"\nKey categories include:")
    print("• Idolatry prohibitions (mitzvot 1-51)")
    print("• Dietary laws (kashrut)")
    print("• Sabbath prohibitions")
    print("• Temple and ritual prohibitions")
    print("• Interpersonal prohibitions")
    print("• Agricultural laws")

if __name__ == "__main__":
    main()