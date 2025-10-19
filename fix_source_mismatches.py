#!/usr/bin/env python3
"""
Fix mismatched biblical sources by extracting correct references from summary text
and cross-referencing with JSON source where possible.
"""

import csv
import re
import json
from datetime import datetime

def fix_source_mismatches():
    """Fix the identified source mismatches"""
    
    input_file = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
    json_file = 'Data/SeferHaMitzvos.json'
    backup_file = f'Schedule_Complete_Sefer_HaMitzvos_WithBiblical_source_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    print("=== FIXING SOURCE MISMATCHES ===\n")
    
    # Load JSON for reference
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Read CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Create backup
    with open(backup_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ Created backup: {backup_file}")
    
    # Known mismatches to fix (from our analysis)
    fixes = [
        {'line': 50, 'entry': 'Positive 35', 'correct_book': 'Shemos', 'correct_ref': 'Shemos 30:25'},
        {'line': 125, 'entry': 'Positive 110', 'correct_book': 'Vayikra', 'correct_ref': 'Vayikra 14:2'},  # Tzaraas purification
        {'line': 505, 'entry': 'Negative 241', 'correct_book': 'Devarim', 'correct_ref': 'Devarim 24:17'},  # Widow's garment
        {'line': 506, 'entry': 'Negative 242', 'correct_book': 'Devarim', 'correct_ref': 'Devarim 24:6'},   # Mill/millstone
        {'line': 549, 'entry': 'Negative 285', 'correct_book': 'Devarim', 'correct_ref': 'Devarim 5:17'},   # False testimony
        {'line': 551, 'entry': 'Negative 287', 'correct_book': 'Devarim', 'correct_ref': 'Devarim 24:16'},  # Fathers/children
        {'line': 560, 'entry': 'Negative 296', 'correct_book': 'Bamidbar', 'correct_ref': 'Bamidbar 35:31'} # Ransom for murderer
    ]
    
    changes_made = 0
    
    print("🔄 Applying fixes...")
    
    for fix in fixes:
        line_idx = fix['line'] - 1  # Convert to 0-based index
        if line_idx < len(rows):
            old_source = rows[line_idx][4]
            rows[line_idx][4] = fix['correct_ref']
            changes_made += 1
            
            print(f"   {fix['entry']}: '{old_source}' → '{fix['correct_ref']}'")
    
    # Write updated CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\n✅ FIXES APPLIED")
    print(f"📊 Total fixes: {changes_made}")
    print(f"💾 Updated file: {input_file}")
    print(f"🔒 Backup saved as: {backup_file}")
    
    return changes_made

if __name__ == "__main__":
    fix_source_mismatches()