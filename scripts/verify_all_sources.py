#!/usr/bin/env python3
"""
Comprehensive verification of all biblical sources in the schedule against the master list.
This will identify any sources that don't match the authoritative master list.
"""

import csv
import re
from collections import defaultdict

def load_master_sources():
    """Load all biblical sources from the master list."""
    master_sources = {}
    
    print("📖 Loading master list sources...")
    with open('archive/MitzvosMasterList.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            number = int(row['Number'])
            reference = row['Biblical Reference'].strip()
            mitzvah = row['Mitzvah'].strip()
            master_sources[number] = {
                'reference': reference,
                'mitzvah': mitzvah
            }
    
    print(f"✅ Loaded {len(master_sources)} master references")
    return master_sources

def load_schedule_sources():
    """Load all biblical sources from the current schedule."""
    schedule_sources = {}
    
    print("📅 Loading schedule sources...")
    with open('Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract mitzvah number from format like "Positive 14" or "Negative 35"
            mitzvah_type_number = row['Mitzvah_Type_Number'].strip()
            match = re.search(r'(Positive|Negative)\s+(\d+)', mitzvah_type_number)
            if match:
                mitzvah_type = match.group(1)
                mitzvah_number = int(match.group(2))
                
                # Convert to master list numbering (Positive 1-248, Negative 249-613)
                if mitzvah_type == "Positive":
                    master_number = mitzvah_number
                else:  # Negative
                    master_number = 248 + mitzvah_number
                
                schedule_sources[master_number] = {
                    'reference': row['Biblical_Source'].strip(),
                    'summary': row['Summary'].strip(),
                    'date': row['Date'],
                    'mitzvah_type_number': mitzvah_type_number
                }
    
    print(f"✅ Loaded {len(schedule_sources)} schedule references")
    return schedule_sources

def compare_sources():
    """Compare all sources between schedule and master list."""
    master_sources = load_master_sources()
    schedule_sources = load_schedule_sources()
    
    print("\n🔍 Comparing all sources...")
    print("=" * 80)
    
    mismatches = []
    matches = []
    missing_in_schedule = []
    extra_in_schedule = []
    
    # Check each master list entry
    for master_num in sorted(master_sources.keys()):
        master_ref = master_sources[master_num]['reference']
        master_mitzvah = master_sources[master_num]['mitzvah']
        
        if master_num in schedule_sources:
            schedule_ref = schedule_sources[master_num]['reference']
            if master_ref == schedule_ref:
                matches.append(master_num)
            else:
                mismatches.append({
                    'number': master_num,
                    'master_ref': master_ref,
                    'schedule_ref': schedule_ref,
                    'mitzvah': master_mitzvah,
                    'mitzvah_type': schedule_sources[master_num]['mitzvah_type_number']
                })
        else:
            missing_in_schedule.append({
                'number': master_num,
                'reference': master_ref,
                'mitzvah': master_mitzvah
            })
    
    # Check for extra entries in schedule
    for schedule_num in schedule_sources.keys():
        if schedule_num not in master_sources:
            extra_in_schedule.append({
                'number': schedule_num,
                'reference': schedule_sources[schedule_num]['reference'],
                'mitzvah_type': schedule_sources[schedule_num]['mitzvah_type_number']
            })
    
    # Print results
    print(f"📊 COMPARISON RESULTS:")
    print(f"✅ Matching sources: {len(matches)}")
    print(f"❌ Mismatched sources: {len(mismatches)}")
    print(f"🔍 Missing in schedule: {len(missing_in_schedule)}")
    print(f"➕ Extra in schedule: {len(extra_in_schedule)}")
    
    if mismatches:
        print(f"\n❌ MISMATCHED SOURCES ({len(mismatches)}):")
        print("-" * 80)
        for mismatch in mismatches[:20]:  # Show first 20
            print(f"#{mismatch['number']} ({mismatch['mitzvah_type']}) - {mismatch['mitzvah'][:60]}...")
            print(f"  Master:   {mismatch['master_ref']}")
            print(f"  Schedule: {mismatch['schedule_ref']}")
            print()
        
        if len(mismatches) > 20:
            print(f"... and {len(mismatches) - 20} more mismatches")
    
    if missing_in_schedule:
        print(f"\n🔍 MISSING IN SCHEDULE ({len(missing_in_schedule)}):")
        print("-" * 80)
        for missing in missing_in_schedule[:10]:
            print(f"#{missing['number']} - {missing['mitzvah'][:60]}... → {missing['reference']}")
        
        if len(missing_in_schedule) > 10:
            print(f"... and {len(missing_in_schedule) - 10} more missing")
    
    if extra_in_schedule:
        print(f"\n➕ EXTRA IN SCHEDULE ({len(extra_in_schedule)}):")
        print("-" * 80)
        for extra in extra_in_schedule:
            print(f"#{extra['number']} ({extra['mitzvah_type']}) → {extra['reference']}")
    
    # Summary
    total_master = len(master_sources)
    total_schedule = len(schedule_sources)
    match_percentage = (len(matches) / total_master) * 100 if total_master > 0 else 0
    
    print(f"\n📈 SUMMARY:")
    print(f"Master list: {total_master} mitzvot")
    print(f"Schedule: {total_schedule} mitzvot")
    print(f"Match rate: {match_percentage:.1f}%")
    
    if len(mismatches) == 0 and len(missing_in_schedule) == 0 and len(extra_in_schedule) == 0:
        print("\n🎉 PERFECT MATCH! All sources are consistent with the master list.")
        return True
    else:
        print(f"\n⚠️  Found {len(mismatches)} mismatches that need correction.")
        return False

if __name__ == "__main__":
    print("🔍 COMPREHENSIVE SOURCE VERIFICATION")
    print("Comparing Schedule vs Master List")
    print("=" * 80)
    
    try:
        all_match = compare_sources()
        if all_match:
            print("\n✅ All sources verified - schedule is consistent with master list!")
        else:
            print("\n❌ Some sources need correction to match master list.")
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()