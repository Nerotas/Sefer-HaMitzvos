#!/usr/bin/env python3
"""
Sefer HaMitzvos Google Calendar Creator
Creates a dedicated Google Calendar with daily mitzvah study events
"""

import os
import csv
import json
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Google Calendar API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeferHaMitzvosCalendar:
    """Manages the Sefer HaMitzvos Google Calendar"""

    # Google Calendar API scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle'):
        """
        Initialize the calendar manager

        Args:
            credentials_file: Path to Google OAuth2 credentials JSON file
            token_file: Path to store authentication token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.calendar_id = None
        self.mitzvos_data = []

        # Calendar configuration
        self.calendar_config = {
            'summary': 'Sefer HaMitzvos Daily Study',
            'description': '''📚 Daily study calendar for Maimonides' Sefer HaMitzvos (Book of Commandments).

This calendar provides systematic daily study of all 613 biblical commandments as enumerated and explained by the Rambam (Maimonides).

🕐 Daily Events: 8:00 AM (30 minutes)
📖 Content: Mitzvah description, biblical sources, and Sefaria study links
🔔 Reminders: At event time, 15 minutes before, and 1 hour email notification

✡️ Subscribe to this calendar to receive daily mitzvah study reminders and integrate Torah learning into your daily routine.

🔗 Related: This calendar complements the daily WhatsApp study group for discussions and community learning.''',
            'timeZone': 'America/Chicago',  # Adjust as needed
            'location': 'Your Study Space'
        }

        # Event timing configuration
        self.event_config = {
            'start_hour': 8,        # 8:00 AM
            'start_minute': 0,
            'duration_minutes': 30,  # 30 minute study session
            'color_id': '5',        # Yellow color for study
            'reminders': [
                {'method': 'popup', 'minutes': 0},      # At event time
                {'method': 'popup', 'minutes': 15},     # 15 min before
                {'method': 'email', 'minutes': 60},     # 1 hour before
            ]
        }

    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API

        Returns:
            True if authentication successful, False otherwise
        """
        creds = None

        # Check for existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {e}")
                    creds = None

            if not creds:
                if not os.path.exists(self.credentials_file):
                    logger.error(f"Credentials file not found: {self.credentials_file}")
                    logger.error("Please download OAuth2 credentials from Google Cloud Console")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        try:
            self.service = build('calendar', 'v3', credentials=creds)
            logger.info("✅ Google Calendar API authentication successful")
            return True
        except Exception as e:
            logger.error(f"Failed to build Calendar service: {e}")
            return False

    def load_mitzvos_data(self, csv_file: str = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'):
        """Load mitzvos data from CSV file"""
        self.mitzvos_data = []

        if not os.path.exists(csv_file):
            logger.error(f"CSV file not found: {csv_file}")
            return False

        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.mitzvos_data.append({
                        'date': row['Date'],
                        'mitzvah_type': row['Mitzvah_Type_Number'],
                        'summary': row['Summary'],
                        'biblical_source': row['Biblical_Source'],
                        'sefaria_link': row['Sefaria_Link']
                    })

            logger.info(f"✅ Loaded {len(self.mitzvos_data)} mitzvos from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading CSV data: {e}")
            return False

    def create_calendar(self) -> Optional[str]:
        """
        Create the Sefer HaMitzvos calendar

        Returns:
            Calendar ID if successful, None if failed
        """
        if not self.service:
            logger.error("Google Calendar service not initialized")
            return None

        try:
            calendar_body = {
                'summary': self.calendar_config['summary'],
                'description': self.calendar_config['description'],
                'timeZone': self.calendar_config['timeZone']
            }

            calendar = self.service.calendars().insert(body=calendar_body).execute()
            self.calendar_id = calendar['id']

            # Make calendar public for sharing
            rule = {
                'scope': {
                    'type': 'default'
                },
                'role': 'reader'
            }
            self.service.acl().insert(calendarId=self.calendar_id, body=rule).execute()

            logger.info(f"✅ Created calendar: {self.calendar_config['summary']}")
            logger.info(f"📅 Calendar ID: {self.calendar_id}")

            return self.calendar_id
        except HttpError as e:
            logger.error(f"Failed to create calendar: {e}")
            return None

    def create_event_from_mitzvah(self, mitzvah_data: Dict) -> Dict:
        """
        Create a Google Calendar event from mitzvah data

        Args:
            mitzvah_data: Dictionary with mitzvah information

        Returns:
            Google Calendar event dictionary
        """
        # Parse date and create event timing
        event_date = datetime.strptime(mitzvah_data['date'], '%Y-%m-%d')
        start_time = event_date.replace(
            hour=self.event_config['start_hour'],
            minute=self.event_config['start_minute'],
            second=0,
            microsecond=0
        )
        end_time = start_time + timedelta(minutes=self.event_config['duration_minutes'])

        # Format event title
        title = f"📚 Sefer HaMitzvos: {mitzvah_data['mitzvah_type']}"

        # Create rich description
        description_parts = [
            "📚 Daily Sefer HaMitzvos Study",
            "",
            f"🔢 Mitzvah: {mitzvah_data['mitzvah_type']}",
            f"📖 Description: {mitzvah_data['summary']}",
            ""
        ]

        # Add biblical source
        if mitzvah_data['biblical_source']:
            description_parts.append(f"📜 Biblical Source: {mitzvah_data['biblical_source']}")
        else:
            description_parts.append("📜 Biblical Source: Traditional Sources")

        # Add Sefaria link
        if mitzvah_data['sefaria_link']:
            description_parts.append(f"🔗 Study Link: {mitzvah_data['sefaria_link']}")

        description_parts.extend([
            "",
            "📱 Join our daily WhatsApp study group for discussions and community learning!",
            "",
            "✡️ May this mitzvah guide your day and bring blessing to your studies!"
        ])

        description = "\n".join(description_parts)

        # Create the event
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': self.calendar_config['timeZone'],
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': self.calendar_config['timeZone'],
            },
            'reminders': {
                'useDefault': False,
                'overrides': self.event_config['reminders']
            },
            'colorId': self.event_config['color_id'],
            'location': self.calendar_config['location']
        }

        return event

    def create_all_events(self, batch_size: int = 100) -> bool:
        """
        Create all mitzvah events in the calendar

        Args:
            batch_size: Number of events to create per batch

        Returns:
            True if successful, False otherwise
        """
        if not self.service or not self.calendar_id:
            logger.error("Calendar service or calendar ID not available")
            return False

        if not self.mitzvos_data:
            logger.error("No mitzvos data loaded")
            return False

        logger.info(f"Creating {len(self.mitzvos_data)} events in batches of {batch_size}...")

        created_count = 0
        failed_count = 0

        # Process in batches to avoid API limits
        for i in range(0, len(self.mitzvos_data), batch_size):
            batch = self.mitzvos_data[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}: events {i+1}-{min(i+batch_size, len(self.mitzvos_data))}")

            for mitzvah in batch:
                try:
                    event = self.create_event_from_mitzvah(mitzvah)

                    result = self.service.events().insert(
                        calendarId=self.calendar_id,
                        body=event
                    ).execute()

                    created_count += 1

                    # Log progress every 50 events
                    if created_count % 50 == 0:
                        logger.info(f"✅ Created {created_count} events so far...")

                except HttpError as e:
                    logger.error(f"Failed to create event for {mitzvah['date']} - {mitzvah['mitzvah_type']}: {e}")
                    failed_count += 1
                except Exception as e:
                    logger.error(f"Unexpected error creating event for {mitzvah['date']}: {e}")
                    failed_count += 1

        logger.info(f"✅ Event creation complete!")
        logger.info(f"📊 Created: {created_count} events")
        logger.info(f"❌ Failed: {failed_count} events")

        return failed_count == 0

    def get_calendar_info(self) -> Optional[Dict]:
        """Get calendar information and sharing links"""
        if not self.service or not self.calendar_id:
            return None

        try:
            calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()

            # Generate sharing URLs
            sharing_info = {
                'calendar_id': self.calendar_id,
                'calendar_name': calendar['summary'],
                'public_url': f"https://calendar.google.com/calendar/embed?src={self.calendar_id}",
                'subscribe_url': f"https://calendar.google.com/calendar/u/0?cid={self.calendar_id}",
                'ical_url': f"https://calendar.google.com/calendar/ical/{self.calendar_id}/public/basic.ics"
            }

            return sharing_info
        except Exception as e:
            logger.error(f"Error getting calendar info: {e}")
            return None

    def generate_setup_instructions(self, sharing_info: Dict) -> str:
        """Generate user setup instructions"""
        instructions = f"""
# 📅 Sefer HaMitzvos Daily Study Calendar

## 🎉 Calendar Successfully Created!

**Calendar Name:** {sharing_info['calendar_name']}
**Calendar ID:** {sharing_info['calendar_id']}

## 📲 How to Subscribe (Choose One Method):

### Method 1: Direct Subscribe Link (Recommended)
1. Click this link: {sharing_info['subscribe_url']}
2. Click "Add Calendar" or "Subscribe"
3. The calendar will appear in your Google Calendar

### Method 2: Manual Add by URL
1. Open Google Calendar (calendar.google.com)
2. Click the "+" next to "Other calendars"
3. Select "From URL"
4. Enter: {sharing_info['ical_url']}
5. Click "Add Calendar"

### Method 3: For Non-Google Calendar Apps
- **Apple Calendar/Outlook/Others:** Use this iCal URL:
  `{sharing_info['ical_url']}`

## 📱 Mobile Setup:
1. Subscribe using Method 1 above on your computer
2. Open Google Calendar app on your phone
3. The calendar will automatically sync to your mobile device
4. You'll receive notifications based on your phone's settings

## 🔔 Customizing Notifications:
1. In Google Calendar, click the calendar name
2. Select "Settings and sharing"
3. Adjust notification preferences under "Event notifications"

## 📋 What You'll Get:
- ⏰ Daily events at 8:00 AM (30 minutes)
- 📖 Complete mitzvah descriptions and biblical sources
- 🔗 Direct links to Sefaria.org for deeper study
- 🔔 Reminders: At time, 15 min before, 1 hour email
- 📱 Full mobile integration with native notifications

## 🎯 Next Steps:
1. Subscribe to the calendar using one of the methods above
2. Consider joining our WhatsApp study group for discussions
3. Adjust notification timing to fit your daily routine
4. Begin your systematic study of Sefer HaMitzvos!

✡️ May your daily Torah study bring wisdom and blessing!
        """

        return instructions.strip()

def main():
    """Main function to create the Sefer HaMitzvos calendar"""
    print("📅 Sefer HaMitzvos Google Calendar Creator")
    print("=" * 50)

    # Initialize the calendar manager
    calendar_manager = SeferHaMitzvosCalendar()

    # Step 1: Authenticate
    print("\n🔐 Step 1: Authenticating with Google Calendar...")
    if not calendar_manager.authenticate():
        print("❌ Authentication failed. Please check your credentials.")
        return False

    # Step 2: Load mitzvos data
    print("\n📚 Step 2: Loading Sefer HaMitzvos data...")
    if not calendar_manager.load_mitzvos_data():
        print("❌ Failed to load mitzvos data.")
        return False

    # Step 3: Create calendar
    print("\n📅 Step 3: Creating the calendar...")
    calendar_id = calendar_manager.create_calendar()
    if not calendar_id:
        print("❌ Failed to create calendar.")
        return False

    # Step 4: Create all events
    print("\n⚡ Step 4: Creating all mitzvah events...")
    print("This may take a few minutes for 629+ events...")

    if not calendar_manager.create_all_events():
        print("⚠️ Some events failed to create, but calendar is functional.")

    # Step 5: Generate sharing information
    print("\n🔗 Step 5: Generating sharing information...")
    sharing_info = calendar_manager.get_calendar_info()

    if sharing_info:
        instructions = calendar_manager.generate_setup_instructions(sharing_info)

        # Save instructions to file
        with open('calendar_setup_instructions.md', 'w', encoding='utf-8') as f:
            f.write(instructions)

        print(instructions)
        print(f"\n💾 Setup instructions saved to: calendar_setup_instructions.md")

    print("\n🎉 SUCCESS! Your Sefer HaMitzvos calendar is ready!")
    return True

if __name__ == "__main__":
    main()