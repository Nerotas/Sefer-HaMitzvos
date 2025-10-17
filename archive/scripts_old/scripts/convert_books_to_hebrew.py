import csv
import re

# Mapping of English biblical book names to Hebrew names
book_mappings = {
    'Genesis': 'Bereishis',
    'Exodus': 'Shemos',
    'Leviticus': 'Vayikra',
    'Numbers': 'Bamidbar',
    'Deuteronomy': 'Devarim',
    'Joshua': 'Yehoshua',
    'Judges': 'Shoftim',
    'Samuel': 'Shmuel',
    'Kings': 'Melachim',
    'Isaiah': 'Yeshayahu',
    'Jeremiah': 'Yirmiyahu',
    'Ezekiel': 'Yechezkel',
    'Hosea': 'Hoshea',
    'Joel': 'Yoel',
    'Amos': 'Amos',
    'Obadiah': 'Ovadyah',
    'Jonah': 'Yonah',
    'Micah': 'Michah',
    'Nahum': 'Nachum',
    'Habakkuk': 'Chavakuk',
    'Zephaniah': 'Tzefanyah',
    'Haggai': 'Chaggai',
    'Zechariah': 'Zecharyah',
    'Malachi': 'Malachi',
    'Psalms': 'Tehillim',
    'Proverbs': 'Mishlei',
    'Job': 'Iyov',
    'Song': 'Shir HaShirim',
    'Ruth': 'Rus',
    'Lamentations': 'Eichah',
    'Ecclesiastes': 'Koheles',
    'Esther': 'Esther',
    'Daniel': 'Daniel',
    'Ezra': 'Ezra',
    'Nehemiah': 'Nechemiah',
    'Chronicles': 'Divrei HaYamim'
}

def convert_book_names_to_hebrew():
    """Convert biblical book names from English to Hebrew in the CSV file."""

    # Read the current CSV
    rows = []
    with open('MitzvosMasterList.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Process each row (skip header)
    books_found = set()
    conversions_made = 0

    for i in range(1, len(rows)):  # Skip header row
        if len(rows[i]) >= 3:
            reference = rows[i][2]
            books_found.add(reference.split()[0] if reference.split() else '')

            # Replace each English book name with Hebrew equivalent
            for english, hebrew in book_mappings.items():
                if reference.startswith(english):
                    # Replace the book name while preserving the chapter:verse
                    new_reference = reference.replace(english, hebrew, 1)
                    rows[i][2] = new_reference
                    conversions_made += 1
                    print(f"Converted: {reference} -> {new_reference}")
                    break

    # Write the updated CSV
    with open('MitzvosMasterList.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\nConversion complete!")
    print(f"Total conversions made: {conversions_made}")
    print(f"Books found in file: {sorted(books_found)}")

if __name__ == "__main__":
    convert_book_names_to_hebrew()