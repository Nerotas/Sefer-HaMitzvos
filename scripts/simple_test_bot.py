#!/usr/bin/env python3
"""
Lambda Bot Testing Utility - Simple Version
Allows testing the mitzvah bot with specific dates without deploying to AWS
"""

import csv
import sys
import os
from datetime import datetime, timedelta

class TestMitzvahBot:
    def __init__(self):
        """Initialize test bot without Twilio client."""
        print("Setting up test bot (no Twilio client)...")

        # Load schedule data from CSV directly
        self.schedule_data = []

        csv_path = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
        print(f"Loading from: {csv_path}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                daily_entries = {}

                for row in reader:
                    # Handle UTF-8 BOM in the Date column
                    date_key = 'Date' if 'Date' in row else '\ufeffDate'
                    date = row[date_key].strip()

                    if date not in daily_entries:
                        daily_entries[date] = {
                            'Date': date,
                            'Mitzvos': [],
                            'Titles': [],
                            'Sources': [],
                            'Links': []
                        }

                    daily_entries[date]['Mitzvos'].append(row['Mitzvah_Type_Number'])
                    daily_entries[date]['Titles'].append(row['Summary'])
                    daily_entries[date]['Sources'].append(row.get('Biblical_Source', ''))
                    daily_entries[date]['Links'].append(row['Sefaria_Link'])

                # Convert to expected format
                for date, data in daily_entries.items():
                    self.schedule_data.append({
                        'Date': date,
                        'Mitzvos': ', '.join(data['Mitzvos']),
                        'English Title(s)': ' & '.join(data['Titles']),
                        'Source': 'Sefer HaMitzvot',
                        'Sefaria_Link': data['Links'][0] if len(data['Links']) == 1 else data['Links'],
                        'Biblical_Sources': data['Sources']
                    })

            print(f"✅ Loaded {len(self.schedule_data)} schedule entries from CSV")
        except FileNotFoundError:
            print(f"❌ CSV file not found: {csv_path}")
            self.schedule_data = []
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            import traceback
            traceback.print_exc()
            self.schedule_data = []

    def find_mitzvah_by_date(self, date_str):
        """Find mitzvah entry for specific date"""
        for row in self.schedule_data:
            if row['Date'].strip() == date_str:
                return {
                    'date': row['Date'].strip(),
                    'mitzvos': row['Mitzvos'].strip(),
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip(),
                    'sefaria_link': row.get('Sefaria_Link', ''),
                    'biblical_sources': row.get('Biblical_Sources', [])
                }
        return None

    def load_mitzvah_for_date(self, target_date=None):
        """Load mitzvah for specific date."""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')

        return self.find_mitzvah_by_date(target_date)

    def format_message(self, mitzvah_data):
        """Format WhatsApp message."""
        date_str = mitzvah_data['date']
        mitzvos = mitzvah_data['mitzvos']
        title = mitzvah_data['title']

        # Basic message formatting (simplified version)
        message = f"🕊️ Daily Mitzvah - {date_str}\n\n"
        message += f"📋 {mitzvos}\n"
        message += f"📖 {title}\n\n"

        if mitzvah_data.get('biblical_sources') and mitzvah_data['biblical_sources'][0]:
            message += f"📜 Source: {mitzvah_data['biblical_sources'][0]}\n\n"

        if mitzvah_data.get('sefaria_link'):
            message += f"🔗 Learn more: {mitzvah_data['sefaria_link']}"

        return message

    def send_to_recipient(self, recipient, message):
        """Mock send function for testing."""
        print(f"\n📤 WOULD SEND TO: {recipient}")
        print("📨 MESSAGE CONTENT:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        return True

def test_lambda_with_date(test_date=None):
    """Test the Lambda bot with a specific date."""

    print("🧪 Lambda Bot Date Testing Utility")
    print("=" * 50)

    if test_date is None:
        # Interactive mode - ask for date
        print("\nEnter a date to test (YYYY-MM-DD format)")
        print("Examples: 2025-10-20, 2025-11-02, 2025-12-15")
        print("Or press Enter for today's date")

        user_input = input("\nDate: ").strip()

        if not user_input:
            test_date = datetime.now().strftime('%Y-%m-%d')
            print(f"Using today's date: {test_date}")
        else:
            # Validate date format
            try:
                datetime.strptime(user_input, '%Y-%m-%d')
                test_date = user_input
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD")
                return False

    print(f"\n🗓️  Testing date: {test_date}")

    try:
        # Create test bot
        bot = TestMitzvahBot()

        if not bot.schedule_data:
            print("❌ No schedule data loaded. Cannot proceed with test.")
            return False

        # Load mitzvah for the specified date
        print(f"\n🔍 Looking up mitzvah for {test_date}...")
        mitzvah_data = bot.load_mitzvah_for_date(test_date)

        if not mitzvah_data:
            print(f"❌ No mitzvah found for {test_date}")

            # Suggest nearby dates
            print("\n💡 Checking nearby dates:")
            for offset in [-1, 1, -2, 2]:
                check_date = (datetime.strptime(test_date, '%Y-%m-%d') + timedelta(days=offset)).strftime('%Y-%m-%d')
                check_data = bot.load_mitzvah_for_date(check_date)
                if check_data:
                    print(f"   {check_date}: {check_data['mitzvos']} - {check_data['title'][:60]}...")

            return False

        # Display mitzvah information
        print(f"✅ Found mitzvah for {test_date}")
        print(f"📋 Mitzvah Number(s): {mitzvah_data['mitzvos']}")
        print(f"📖 Title: {mitzvah_data['title']}")
        print(f"🏛️  Source: {mitzvah_data['source']}")

        if mitzvah_data.get('biblical_sources') and mitzvah_data['biblical_sources'][0]:
            print(f"📜 Biblical Sources: {mitzvah_data['biblical_sources'][0]}")

        # Format and display the message that would be sent
        print(f"\n📱 Formatting WhatsApp message...")
        message = bot.format_message(mitzvah_data)

        # Test sending (mock)
        print(f"\n🧪 Testing message send (mock)...")
        success = bot.send_to_recipient('+1234567890', message)

        if success:
            print("✅ Test completed successfully!")
            return True
        else:
            print("❌ Test failed during message formatting")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_dates():
    """Test multiple dates at once."""
    print("🧪 Testing Multiple Dates")
    print("=" * 30)

    test_dates = [
        '2025-10-20',  # Start date
        '2025-11-02',  # Tzitzit date (from our analysis)
        '2025-12-25',  # Mid-schedule
        '2026-03-15',  # Near end
    ]

    for test_date in test_dates:
        print(f"\n{'='*20} {test_date} {'='*20}")
        success = test_lambda_with_date(test_date)
        if not success:
            print(f"⚠️  Failed to get mitzvah for {test_date}")

def create_lambda_test_event(test_date):
    """Create a test event JSON for AWS Lambda testing."""
    import json

    event = {
        "test_date": test_date,
        "test_mode": True
    }

    filename = f"lambda_test_event_{test_date.replace('-', '_')}.json"

    with open(filename, 'w') as f:
        json.dump(event, f, indent=2)

    print(f"📝 Created Lambda test event file: {filename}")
    print(f"📋 Contents: {json.dumps(event, indent=2)}")

    return filename

def main():
    """Main testing function."""
    print("Lambda Bot Testing Options:")
    print("1. Test specific date (interactive)")
    print("2. Test multiple predefined dates")
    print("3. Test with command line date")
    print("4. Create Lambda test event JSON")

    if len(sys.argv) > 1:
        # Command line date provided
        test_date = sys.argv[1]
        print(f"Testing with command line date: {test_date}")

        # Validate date format
        try:
            datetime.strptime(test_date, '%Y-%m-%d')

            # Test locally and create Lambda event
            print("\n" + "="*50)
            print("LOCAL TEST")
            print("="*50)
            test_lambda_with_date(test_date)

            print("\n" + "="*50)
            print("LAMBDA EVENT CREATION")
            print("="*50)
            create_lambda_test_event(test_date)

        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD")

    else:
        choice = input("\nChoose option (1-4): ").strip()

        if choice == '1':
            test_lambda_with_date()
        elif choice == '2':
            test_multiple_dates()
        elif choice == '3':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            test_lambda_with_date(date)
        elif choice == '4':
            date = input("Enter date for Lambda test event (YYYY-MM-DD): ").strip()
            create_lambda_test_event(date)
        else:
            print("Invalid choice. Using interactive mode.")
            test_lambda_with_date()

if __name__ == "__main__":
    main()