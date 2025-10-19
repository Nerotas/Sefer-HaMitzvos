#!/usr/bin/env python3
"""
Normalize all biblical sources in CSV to use Hebrew names consistently.
This script will:
1. Update biblical source column (5th column) to use Hebrew names
2. Update summary text to use Hebrew names  
3. Preserve all other data exactly
"""

import csv
import re
from datetime import datetime

def normalize_biblical_sources():
    """Normalize all biblical references to Hebrew names in CSV"""
    
    # Mapping of English to Hebrew book names
    english_to_hebrew = {
        'Genesis': 'Bereishis',
        'Exodus': 'Shemos', 
        'Leviticus': 'Vayikra',
        'Numbers': 'Bamidbar',
        'Deuteronomy': 'Devarim'
    }
    
    input_file = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
    backup_file = f'Schedule_Complete_Sefer_HaMitzvos_WithBiblical_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    print("=== NORMALIZING BIBLICAL SOURCES TO HEBREW ===\n")
    
    # Read the CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Create backup
    with open(backup_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ Created backup: {backup_file}")
    
    changes_made = 0
    
    print("\n🔄 Processing entries...")
    
    for i, row in enumerate(rows):
        if i == 0:  # Skip header
            continue
            
        if len(row) < 5:  # Skip incomplete rows
            continue
            
        original_row = row.copy()
        
        # Update biblical source column (index 4)
        biblical_source = row[4]
        for english, hebrew in english_to_hebrew.items():
            if english in biblical_source:
                row[4] = biblical_source.replace(english, hebrew)
        
        # Update summary text (index 3) 
        summary = row[3]
        for english, hebrew in english_to_hebrew.items():
            # Case insensitive replacement for summary text
            pattern = re.compile(re.escape(english), re.IGNORECASE)
            summary = pattern.sub(hebrew, summary)
        
        # Also handle lowercase versions in parentheses
        for english, hebrew in english_to_hebrew.items():
            pattern = re.compile(r'\(' + re.escape(english.lower()) + r'\s+\d+', re.IGNORECASE)
            summary = pattern.sub(lambda m: m.group(0).replace(english.lower(), hebrew), summary)
        
        row[3] = summary
        
        # Check if changes were made
        if row != original_row:
            changes_made += 1
            print(f"   Updated row {i}: {row[2]}")
            
            # Show specific changes for biblical source
            if row[4] != original_row[4]:
                print(f"     📖 Source: '{original_row[4]}' → '{row[4]}'")
            
            # Show if summary was updated
            if row[3] != original_row[3]:
                print(f"     📝 Summary updated (English→Hebrew references)")
    
    # Write updated CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\n✅ NORMALIZATION COMPLETE")
    print(f"📊 Total entries processed: {len(rows) - 1}")
    print(f"🔄 Entries modified: {changes_made}")
    print(f"💾 Updated file: {input_file}")
    print(f"🔒 Backup saved as: {backup_file}")
    
    if changes_made > 0:
        print(f"\n📋 HEBREW BOOK NAME MAPPING APPLIED:")
        for english, hebrew in english_to_hebrew.items():
            print(f"   {english} → {hebrew}")
    
    return changes_made

if __name__ == "__main__":
    normalize_biblical_sources()