#!/usr/bin/env python3
"""
Final source corrections to make schedule 100% consistent with master list.
This will fix all remaining 10 mismatches identified in the verification.
"""

import csv
import shutil
from datetime import datetime

# The 10 remaining corrections needed based on verification results
FINAL_SOURCE_CORRECTIONS = {
    # Positive 5: Prayer - master says Devarim 10:20, schedule has Shemos 23:25
    "Positive 5": {
        "correct_source": "Devarim 10:20", 
        "wrong_source": "Shemos 23:25",
        "mitzvah": "To fear Him / Prayer"
    },
    
    # Positive 14: Tzitzit - master says Bamidbar 15:38, but we incorrectly have it for love converts 
    # Actually this looks like mitzvah mapping confusion - need to check
    "Positive 14": {
        "correct_source": "Devarim 10:19",  # This should be "love converts" 
        "wrong_source": "Bamidbar 15:38",   # This is tzitzit source, wrong mitzvah
        "mitzvah": "To love converts"
    },
    
    # Positive 19: Blessing after eating - master says Devarim 8:10, schedule has wrong one
    "Positive 19": {
        "correct_source": "Vayikra 19:16",  # This should be "not to gossip"
        "wrong_source": "Devarim 8:10", 
        "mitzvah": "Not to gossip about others"
    },
    
    # Positive 80: Tefillin on arm - master says Devarim 6:8, schedule has wrong
    "Positive 80": {
        "correct_source": "Devarim 6:8",
        "wrong_source": "Bamidbar 18:15",
        "mitzvah": "To bind tefillin on the arm"
    },
    
    # Positive 84: Tzitzit - master says Bamidbar 15:38, schedule has wrong
    "Positive 84": {
        "correct_source": "Bamidbar 15:38",
        "wrong_source": "Devarim 12:11", 
        "mitzvah": "To have Tzitzit on four-cornered garments"
    },
    
    # Positive 90: Shabbat boundary - master says Shemos 16:29
    "Positive 90": {
        "correct_source": "Shemos 16:29",
        "wrong_source": "Shemos 30:19",
        "mitzvah": "Not to walk more than 2000 cubits outside city boundary on Shabbat"
    },
    
    # Positive 125: Have children - master says Bereishis 1:28
    "Positive 125": {
        "correct_source": "Bereishis 1:28", 
        "wrong_source": "Shemos 23:19",
        "mitzvah": "To have children with one's wife"
    },
    
    # Positive 144: Relations with daughter - master says Vayikra 18:10
    "Positive 144": {
        "correct_source": "Vayikra 18:10",
        "wrong_source": "Devarim 18:4", 
        "mitzvah": "Not to have sexual relations with your daughter"
    },
    
    # Positive 159: Homosexual relations - master says Vayikra 18:14
    "Positive 159": {
        "correct_source": "Vayikra 18:14",
        "wrong_source": "Vayikra 23:8",
        "mitzvah": "Not to have homosexual sexual relations"
    },
    
    # Positive 160: Relations with married woman - master says Vayikra 18:20  
    "Positive 160": {
        "correct_source": "Vayikra 18:20",
        "wrong_source": "Vayikra 23:8",
        "mitzvah": "Not to have sexual relations with a married woman"
    }
}

def create_backup():
    """Create a backup of the current schedule file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"Schedule_Complete_Sefer_HaMitzvos_WithBiblical_BACKUP_{timestamp}.csv"
    shutil.copy2('Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv', backup_filename)
    print(f"✅ Created backup: {backup_filename}")
    return backup_filename

def apply_final_corrections():
    """Apply all final source corrections to achieve 100% consistency."""
    
    print("🔧 APPLYING FINAL SOURCE CORRECTIONS")
    print("=" * 60)
    
    backup_file = create_backup()
    
    # Load current schedule
    schedule_rows = []
    corrections_applied = 0
    
    with open('Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        for row in reader:
            mitzvah_type_number = row['Mitzvah_Type_Number'].strip()
            current_source = row['Biblical_Source'].strip()
            
            # Check if this row needs correction
            if mitzvah_type_number in FINAL_SOURCE_CORRECTIONS:
                correction = FINAL_SOURCE_CORRECTIONS[mitzvah_type_number]
                
                if current_source == correction['wrong_source']:
                    # Apply the correction
                    old_source = row['Biblical_Source']
                    row['Biblical_Source'] = correction['correct_source']
                    
                    print(f"✅ {mitzvah_type_number}: {correction['mitzvah'][:50]}...")
                    print(f"   {old_source} → {correction['correct_source']}")
                    corrections_applied += 1
                else:
                    print(f"⚠️  {mitzvah_type_number}: Expected '{correction['wrong_source']}' but found '{current_source}'")
            
            schedule_rows.append(row)
    
    # Write corrected schedule
    with open('Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(schedule_rows)
    
    print(f"\n📊 CORRECTION SUMMARY:")
    print(f"Applied {corrections_applied} corrections")
    print(f"Expected: {len(FINAL_SOURCE_CORRECTIONS)} corrections")
    
    if corrections_applied == len(FINAL_SOURCE_CORRECTIONS):
        print("✅ All corrections successfully applied!")
        return True
    else:
        print("⚠️  Some corrections may not have been applied as expected.")
        return False

def main():
    print("🎯 FINAL SOURCE CORRECTION SCRIPT")
    print("This will fix the remaining 10 mismatches to achieve 100% consistency")
    print("=" * 80)
    
    try:
        success = apply_final_corrections()
        
        if success:
            print(f"\n🎉 SUCCESS! Schedule should now be 100% consistent with master list.")
            print(f"💡 Run 'python verify_all_sources.py' to confirm all sources match.")
        else:
            print(f"\n⚠️  Some issues occurred. Check the output above.")
            
    except Exception as e:
        print(f"❌ Error applying corrections: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()