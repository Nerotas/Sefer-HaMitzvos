#!/usr/bin/env python3
"""
ICS Calendar File Generator for Sefer HaMitzvos
Creates a standard .ics file that can be imported into any calendar application
"""

import csv
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ICSGenerator:
    """Generates ICS (iCalendar) files for Sefer HaMitzvos schedule"""

    def __init__(self):
        self.events = []
        self.calendar_name = "Sefer HaMitzvos Daily Study"
        self.description = "Daily study calendar for Maimonides' Sefer HaMitzvos (Book of Commandments)"

    def load_mitzvos_data(self, csv_file: str | None = None) -> bool:
        """Load mitzvos data from CSV file

        Resolves default path relative to repo root to be robust to CWD.
        """
        if csv_file is None:
            repo_root = Path(__file__).resolve().parents[2]
            csv_path = repo_root / 'data' / 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
        else:
            csv_path = Path(csv_file)

        if not csv_path.exists():
            logger.error(f"CSV file not found: {csv_path}")
            return False

        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    event_date = datetime.strptime(row['Date'], '%Y-%m-%d')
                    start_time = event_date.replace(hour=8, minute=0, second=0)
                    end_time = start_time + timedelta(minutes=30)

                    # Create event data
                    event = {
                        'start': start_time,
                        'end': end_time,
                        'summary': f"📚 Sefer HaMitzvos: {row['Mitzvah_Type_Number']}",
                        'description': self._create_event_description(row),
                        'uid': f"sefer-hamitzvos-{row['Date']}-{row['Mitzvah_Type_Number'].replace(' ', '-').lower()}@rambam-study.com"
                    }
                    self.events.append(event)

            logger.info(f"Loaded {len(self.events)} events from {csv_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading CSV data: {e}")
            return False

    def _create_event_description(self, mitzvah_data: dict) -> str:
        """Create formatted event description"""
        parts = [
            "Daily Sefer HaMitzvos Study",
            "",
            f"Mitzvah: {mitzvah_data['Mitzvah_Type_Number']}",
            f"Description: {mitzvah_data['Summary']}",
            ""
        ]

        if mitzvah_data['Biblical_Source']:
            parts.append(f"Biblical Source: {mitzvah_data['Biblical_Source']}")
        else:
            parts.append("Biblical Source: Traditional Sources")

        if mitzvah_data['Sefaria_Link']:
            parts.append(f"Study Link: {mitzvah_data['Sefaria_Link']}")

        parts.extend([
            "",
            "Join our daily WhatsApp study group for discussions!",
            "",
            "May this mitzvah guide your day!"
        ])

        return "\\n".join(parts)

    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime for ICS format (UTC)"""
        # Convert to UTC for ICS compatibility
        return dt.strftime('%Y%m%dT%H%M%SZ')

    def _escape_text(self, text: str) -> str:
        """Escape special characters for ICS format"""
        if not text:
            return ""

        # ICS escaping rules
        text = text.replace('\\', '\\\\')
        text = text.replace(',', '\\,')
        text = text.replace(';', '\\;')
        text = text.replace('\n', '\\n')

        return text

    def generate_ics_file(self, output_file: str = 'sefer_hamitzvos_calendar.ics') -> bool:
        """Generate the ICS calendar file"""
        if not self.events:
            logger.error("No events to export")
            return False

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write ICS header
                f.write("BEGIN:VCALENDAR\n")
                f.write("VERSION:2.0\n")
                f.write("PRODID:-//Sefer HaMitzvos//Daily Study Calendar//EN\n")
                f.write(f"CALSCALE:GREGORIAN\n")
                f.write(f"X-WR-CALNAME:{self._escape_text(self.calendar_name)}\n")
                f.write(f"X-WR-CALDESC:{self._escape_text(self.description)}\n")
                f.write("X-WR-TIMEZONE:America/Chicago\n")

                # Write events
                for event in self.events:
                    f.write("BEGIN:VEVENT\n")
                    f.write(f"UID:{event['uid']}\n")
                    f.write(f"DTSTART:{self._format_datetime(event['start'])}\n")
                    f.write(f"DTEND:{self._format_datetime(event['end'])}\n")
                    f.write(f"SUMMARY:{self._escape_text(event['summary'])}\n")
                    f.write(f"DESCRIPTION:{self._escape_text(event['description'])}\n")
                    f.write(f"CREATED:{self._format_datetime(datetime.now())}\n")
                    f.write(f"LAST-MODIFIED:{self._format_datetime(datetime.now())}\n")
                    f.write("STATUS:CONFIRMED\n")
                    f.write("TRANSP:TRANSPARENT\n")

                    # Add reminders (alarms)
                    # Reminder at event time
                    f.write("BEGIN:VALARM\n")
                    f.write("TRIGGER:PT0M\n")
                    f.write("ACTION:DISPLAY\n")
                    f.write("DESCRIPTION:Time for Sefer HaMitzvos study!\n")
                    f.write("END:VALARM\n")

                    # Reminder 15 minutes before
                    f.write("BEGIN:VALARM\n")
                    f.write("TRIGGER:-PT15M\n")
                    f.write("ACTION:DISPLAY\n")
                    f.write("DESCRIPTION:Sefer HaMitzvos study in 15 minutes\n")
                    f.write("END:VALARM\n")

                    f.write("END:VEVENT\n")

                # Write ICS footer
                f.write("END:VCALENDAR\n")

            logger.info(f"✅ ICS file created: {output_file}")
            logger.info(f"📊 Events exported: {len(self.events)}")
            return True

        except Exception as e:
            logger.error(f"Error creating ICS file: {e}")
            return False

    def generate_instructions(self, ics_file: str) -> str:
        """Generate instructions for using the ICS file"""
        instructions = f"""
# 📅 Sefer HaMitzvos Calendar - ICS Import Instructions

## 📄 File Created: {ics_file}

This file contains all {len(self.events)} Sefer HaMitzvos study events and can be imported into any calendar application.

## 📲 How to Import:

### Google Calendar:
1. Open Google Calendar (calendar.google.com)
2. Click the gear icon → "Settings"
3. Click "Import & Export" in the left sidebar
4. Click "Select file from your computer"
5. Choose the {ics_file} file
6. Select which calendar to add events to
7. Click "Import"

### Apple Calendar (Mac/iPhone/iPad):
1. **Mac:** Double-click the {ics_file} file, or drag it into Calendar app
2. **iPhone/iPad:** Email the file to yourself, then tap it and select "Add to Calendar"
3. Choose which calendar to add events to

### Microsoft Outlook:
1. **Desktop:** File → Open & Export → Import/Export → Import iCalendar (.ics) file
2. **Web:** Go to Outlook.com → Calendar → Add calendar → Upload from file
3. **Mobile:** Email the file to yourself, open in Outlook app

### Other Calendar Apps:
- **Thunderbird:** Events & Tasks → Import → Select the .ics file
- **Fantastical:** File → Import → Select the .ics file
- **Any app:** Look for "Import Calendar" or "Import ICS" option

## 🔔 Setting Up Reminders:
After importing, you may want to:
1. Check that reminders are enabled (some apps disable imported alarms)
2. Adjust reminder timing to your preference
3. Set up notification sounds/vibrations on mobile

## 📋 What's Included:
- ⏰ Daily events at 8:00 AM (30 minutes)
- 📖 Complete mitzvah descriptions
- 📜 Biblical sources when available
- 🔗 Direct links to Sefaria.org for study
- 🔔 Built-in reminders (at time and 15 min before)

## 💡 Tips:
- Import into a separate calendar to keep mitzvah studies organized
- Consider sharing the calendar with study partners or family
- The file works offline once imported
- Re-import if you want updates (this will create duplicate events)

✡️ May your daily Torah study bring wisdom and blessing!
        """
        return instructions.strip()

def main():
    """Main function to generate ICS calendar file"""
    print("📄 Sefer HaMitzvos ICS Calendar Generator")
    print("=" * 45)

    generator = ICSGenerator()

    # Load the mitzvos data
    print("\n📚 Loading Sefer HaMitzvos data...")
    if not generator.load_mitzvos_data():
        print("❌ Failed to load data")
        return False

    # Generate ICS file
    print("\n📅 Generating ICS calendar file...")
    ics_filename = 'sefer_hamitzvos_calendar.ics'
    if not generator.generate_ics_file(ics_filename):
        print("❌ Failed to generate ICS file")
        return False

    # Generate and save instructions
    instructions = generator.generate_instructions(ics_filename)
    instructions_file = 'ics_import_instructions.md'

    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

    print(instructions)
    print(f"\n💾 Instructions saved to: {instructions_file}")
    print(f"📄 ICS file created: {ics_filename}")
    print("\n🎉 SUCCESS! Your ICS calendar file is ready for import!")

    return True

if __name__ == "__main__":
    main()