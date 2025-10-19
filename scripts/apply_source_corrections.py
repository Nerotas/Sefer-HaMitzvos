#!/usr/bin/env python3
"""
Schedule Source Correction Tool
Updates biblical sources to match the master list for consistency
Optionally updates summaries to use shorter master list descriptions
"""

import csv
import shutil
from datetime import datetime
import os

# High-confidence source corrections from our analysis
CONFIRMED_SOURCE_CORRECTIONS = {
    # Schedule_Num: (Current_Source, Correct_Source, Master_List_Number, Master_Description)
    28: ("Devarim 10:19", "Bamidbar 15:38", 84, "To have Tzitzit on four-cornered garments"),
    19: ("Devarim 10:20", "Shemos 23:25", 77, "To serve the Almighty with prayer daily"),
    33: ("Vayikra 19:16", "Devarim 8:10", 85, "To bless the Almighty after eating"),
    139: ("Bereishis 1:28", "Shemos 23:19", 270, "To set aside the first fruits and bring them to the Temple"),
    94: ("Devarim 6:8", "Bamidbar 18:15", 276, "To redeem the firstborn sons and give the money to a Kohen"),
    104: ("Shemos 16:29", "Shemos 30:19", 331, "A Kohen must wash his hands and feet before service"),
    98: ("Bamidbar 15:38", "Devarim 12:11", 369, "To offer all sacrifices in the Temple"),
    158: ("Vayikra 18:10", "Devarim 18:4", 275, "To give the first shearing of sheep to a Kohen"),
    173: ("Vayikra 18:14", "Vayikra 23:8", 96, "To rest on the first day of Passover"),
    174: ("Vayikra 18:20", "Vayikra 23:8", 98, "To rest on the seventh day of Passover"),
}

class ScheduleSourceCorrector:
    def __init__(self, schedule_file='Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'):
        self.schedule_file = schedule_file
        self.backup_file = None
        self.corrections_applied = []
        self.corrections_skipped = []

    def create_backup(self):
        """Create a backup of the current schedule file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_file = f"Schedule_BACKUP_before_source_corrections_{timestamp}.csv"

        shutil.copy2(self.schedule_file, self.backup_file)
        print(f"✅ Backup created: {self.backup_file}")

    def load_schedule_data(self):
        """Load the current schedule data."""
        schedule_data = []

        try:
            with open(self.schedule_file, 'r', encoding='utf-8-sig') as f:  # Handle BOM
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, 1):
                    row['_row_number'] = i
                    schedule_data.append(row)

            print(f"📄 Loaded {len(schedule_data)} entries from {self.schedule_file}")
            return schedule_data

        except Exception as e:
            print(f"❌ Error loading schedule: {e}")
            return []

    def find_entry_by_sequential_number(self, schedule_data, seq_num):
        """Find schedule entry by sequential number."""
        for entry in schedule_data:
            if int(entry['Sequential_Number']) == seq_num:
                return entry
        return None

    def apply_source_corrections(self, schedule_data, update_summaries=False):
        """Apply source corrections to the schedule data."""
        print(f"\n🔧 Applying source corrections...")
        print(f"📋 Total corrections to apply: {len(CONFIRMED_SOURCE_CORRECTIONS)}")
        print(f"📝 Update summaries: {'Yes' if update_summaries else 'No'}")

        corrections_made = 0

        for seq_num, (current_source, correct_source, master_num, master_desc) in CONFIRMED_SOURCE_CORRECTIONS.items():
            entry = self.find_entry_by_sequential_number(schedule_data, seq_num)

            if not entry:
                self.corrections_skipped.append(f"Sequential #{seq_num}: Entry not found")
                continue

            # Get current values
            current_biblical_source = entry.get('Biblical_Source', '').strip()
            current_summary = entry.get('Summary', '').strip()

            # Check if source correction is needed
            if current_biblical_source == current_source:
                # Apply source correction
                entry['Biblical_Source'] = correct_source

                correction_info = {
                    'seq_num': seq_num,
                    'mitzvah_type': entry['Mitzvah_Type_Number'],
                    'old_source': current_source,
                    'new_source': correct_source,
                    'master_num': master_num,
                    'summary_updated': False
                }

                # Optionally update summary to use master list description
                if update_summaries:
                    entry['Summary'] = master_desc
                    correction_info['old_summary'] = current_summary
                    correction_info['new_summary'] = master_desc
                    correction_info['summary_updated'] = True

                self.corrections_applied.append(correction_info)
                corrections_made += 1

                print(f"✅ #{seq_num} ({entry['Mitzvah_Type_Number']}): {current_source} → {correct_source}")
                if update_summaries:
                    print(f"   Summary: {current_summary[:50]}... → {master_desc[:50]}...")

            else:
                self.corrections_skipped.append(f"Sequential #{seq_num}: Source mismatch - expected '{current_source}', found '{current_biblical_source}'")

        print(f"\n📊 Applied {corrections_made} source corrections")
        return schedule_data

    def save_corrected_schedule(self, schedule_data, output_file=None):
        """Save the corrected schedule data."""
        if output_file is None:
            output_file = self.schedule_file

        try:
            # Get original fieldnames
            with open(self.schedule_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames

            # Write corrected data
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for row in schedule_data:
                    # Remove internal tracking fields
                    output_row = {k: v for k, v in row.items() if not k.startswith('_')}
                    writer.writerow(output_row)

            print(f"💾 Saved corrected schedule to: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error saving schedule: {e}")
            return False

    def generate_correction_report(self):
        """Generate a detailed report of corrections applied."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"source_corrections_report_{timestamp}.csv"

        with open(report_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Sequential_Number', 'Mitzvah_Type', 'Old_Source', 'New_Source',
                'Master_List_Number', 'Summary_Updated', 'Old_Summary', 'New_Summary'
            ])

            # Applied corrections
            for correction in self.corrections_applied:
                writer.writerow([
                    correction['seq_num'],
                    correction['mitzvah_type'],
                    correction['old_source'],
                    correction['new_source'],
                    correction['master_num'],
                    correction['summary_updated'],
                    correction.get('old_summary', ''),
                    correction.get('new_summary', '')
                ])

        print(f"📋 Correction report saved: {report_file}")

        # Also print summary
        print(f"\n📈 CORRECTION SUMMARY:")
        print(f"   Applied: {len(self.corrections_applied)} corrections")
        print(f"   Skipped: {len(self.corrections_skipped)} corrections")

        if self.corrections_skipped:
            print(f"\n⚠️  SKIPPED CORRECTIONS:")
            for skip in self.corrections_skipped:
                print(f"   - {skip}")

    def preview_corrections(self, update_summaries=False):
        """Preview what corrections would be made without applying them."""
        print("🔍 PREVIEW MODE: No changes will be made")
        print("="*60)

        schedule_data = self.load_schedule_data()
        if not schedule_data:
            return False

        print(f"\n📋 Corrections that would be applied:")
        print(f"📝 Update summaries: {'Yes' if update_summaries else 'No'}")

        for seq_num, (current_source, correct_source, master_num, master_desc) in CONFIRMED_SOURCE_CORRECTIONS.items():
            entry = self.find_entry_by_sequential_number(schedule_data, seq_num)

            if entry:
                current_biblical_source = entry.get('Biblical_Source', '').strip()
                current_summary = entry.get('Summary', '').strip()

                print(f"\n#{seq_num} ({entry['Mitzvah_Type_Number']}):")
                print(f"  Source: {current_biblical_source} → {correct_source}")
                if current_biblical_source != current_source:
                    print(f"  ⚠️  WARNING: Expected source '{current_source}', found '{current_biblical_source}'")

                if update_summaries:
                    print(f"  Summary: {current_summary[:80]}...")
                    print(f"        → {master_desc}")
            else:
                print(f"\n#{seq_num}: ❌ Entry not found")

        return True

    def apply_corrections(self, update_summaries=False, preview_only=False):
        """Main method to apply corrections."""
        print("🔧 Schedule Source Correction Tool")
        print("="*50)

        if preview_only:
            return self.preview_corrections(update_summaries)

        # Load data
        schedule_data = self.load_schedule_data()
        if not schedule_data:
            return False

        # Create backup
        self.create_backup()

        # Apply corrections
        corrected_data = self.apply_source_corrections(schedule_data, update_summaries)

        # Save corrected data
        success = self.save_corrected_schedule(corrected_data)

        if success:
            # Generate report
            self.generate_correction_report()
            print(f"\n✅ Source corrections completed successfully!")
            print(f"📄 Backup available at: {self.backup_file}")
            return True
        else:
            print(f"\n❌ Failed to save corrections")
            return False

def main():
    """Main execution function."""
    import sys

    corrector = ScheduleSourceCorrector()

    print("Schedule Source Correction Options:")
    print("1. Preview corrections (sources only)")
    print("2. Preview corrections (sources + summaries)")
    print("3. Apply source corrections only")
    print("4. Apply source corrections + update summaries")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nChoose option (1-4): ").strip()

    if choice == '1':
        corrector.apply_corrections(update_summaries=False, preview_only=True)
    elif choice == '2':
        corrector.apply_corrections(update_summaries=True, preview_only=True)
    elif choice == '3':
        print("\n⚠️  This will modify your schedule file!")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            corrector.apply_corrections(update_summaries=False, preview_only=False)
    elif choice == '4':
        print("\n⚠️  This will modify your schedule file AND replace summaries!")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            corrector.apply_corrections(update_summaries=True, preview_only=False)
    else:
        print("Invalid choice. Use 1-4.")

if __name__ == "__main__":
    main()