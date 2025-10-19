#!/usr/bin/env python3
"""
Source Correction Plan for Mitzvah Schedule
Based on comprehensive analysis findings
"""

import csv
from datetime import datetime

# Critical source corrections based on analysis
CRITICAL_CORRECTIONS = [
    {
        'schedule_num': 28,
        'current_source': 'Devarim 10:19',
        'master_source': 'Bamidbar 15:38',
        'description': 'Tzitzit (fringes)',
        'confidence': 'HIGH - Exact match confirmed'
    },
    {
        'schedule_num': 19,
        'current_source': 'Devarim 10:20',
        'master_source': 'Shemos 23:25',
        'description': 'Prayer to G-d',
        'confidence': 'HIGH - Same concept'
    },
    {
        'schedule_num': 33,
        'current_source': 'Vayikra 19:16',
        'master_source': 'Devarim 8:10',
        'description': 'Blessing after eating',
        'confidence': 'HIGH - Same concept'
    },
    {
        'schedule_num': 139,
        'current_source': 'Bereishis 1:28',
        'master_source': 'Shemos 23:19',
        'description': 'First-fruits to Temple',
        'confidence': 'HIGH - Same concept'
    },
    {
        'schedule_num': 94,
        'current_source': 'Devarim 6:8',
        'master_source': 'Bamidbar 18:15',
        'description': 'Redeem firstborn sons',
        'confidence': 'HIGH - Same concept'
    }
]

def create_correction_report():
    """Create a prioritized correction report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"source_correction_plan_{timestamp}.csv"

    print("Creating Source Correction Plan...")
    print("="*50)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Priority', 'Schedule_Num', 'Current_Source', 'Correct_Source',
            'Description', 'Confidence', 'Action_Required'
        ])

        # Critical corrections first
        for i, correction in enumerate(CRITICAL_CORRECTIONS, 1):
            writer.writerow([
                f"CRITICAL_{i}",
                correction['schedule_num'],
                correction['current_source'],
                correction['master_source'],
                correction['description'],
                correction['confidence'],
                "UPDATE IMMEDIATELY"
            ])

    print(f"Correction plan saved: {filename}")
    return filename

def print_correction_summary():
    """Print summary of required corrections."""
    print("\n" + "="*60)
    print("CRITICAL SOURCE CORRECTIONS NEEDED")
    print("="*60)

    print("\nBased on comprehensive analysis, the following corrections are needed:")
    print("(These are cases where the SAME mitzvah has different sources)")

    for i, correction in enumerate(CRITICAL_CORRECTIONS, 1):
        print(f"\n{i}. Schedule #{correction['schedule_num']}: {correction['description']}")
        print(f"   Current Source: {correction['current_source']}")
        print(f"   Master Source:  {correction['master_source']}")
        print(f"   Confidence:     {correction['confidence']}")

    print(f"\nTOTAL CRITICAL CORRECTIONS: {len(CRITICAL_CORRECTIONS)}")
    print("\nRECOMMENDATION:")
    print("1. Verify these against authoritative Sefer HaMitzvot text")
    print("2. Update schedule with master list sources (more traditional)")
    print("3. Note that Sefer HaMitzvot may use different derivation methods")
    print("4. Consider creating a mapping between the two systems")

def main():
    """Generate correction plan and summary."""
    filename = create_correction_report()
    print_correction_summary()
    print(f"\nDetailed plan saved to: {filename}")

if __name__ == "__main__":
    main()