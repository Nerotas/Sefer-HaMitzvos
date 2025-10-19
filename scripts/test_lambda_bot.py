#!/usr/bin/env python3
"""
Lambda Bot Testing Utility
Allows testing the mitzvah bot with specific dates without deploying to AWS
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add the bots directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'bots'))

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
        # Import the bot class
        from lambda_mitzvah_bot import MitzvahLambdaBot

        # Create test bot instance with mock credentials
        print("📱 Initializing test bot...")

        # Set mock environment variables for testing
        os.environ['TWILIO_ACCOUNT_SID'] = 'test_account_sid'
        os.environ['TWILIO_AUTH_TOKEN'] = 'test_auth_token'
        os.environ['RECIPIENTS'] = '+1234567890'  # Mock recipient

        # Create a test version of the bot that doesn't actually send messages
        class TestMitzvahBot:
            def __init__(self):
                """Initialize test bot without Twilio client."""
                print("Setting up test bot (no Twilio client)...")

                # Load schedule data from CSV directly
                import csv
                self.schedule_data = []

                csv_path = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
                print(f"Loading from: {csv_path}")

                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.schedule_data.append({
                                'Date': row['Date'],
                                'Mitzvos': row['Mitzvah_Type_Number'],
                                'English Title(s)': row['Summary'],
                                'Source': 'Sefer HaMitzvot',
                                'Sefaria_Link': row['Sefaria_Link'],
                                'Biblical_Sources': [row.get('Biblical_Source', '')]
                            })
                    print(f"✅ Loaded {len(self.schedule_data)} schedule entries from CSV")
                except FileNotFoundError:
                    print(f"❌ CSV file not found: {csv_path}")
                    self.schedule_data = []
                except Exception as e:
                    print(f"❌ Error loading CSV: {e}")
                    self.schedule_data = []

                # Mock holiday data for testing
                self.holiday_data = []            def send_to_recipient(self, recipient, message):
                """Mock send function for testing."""
                print(f"\n📤 WOULD SEND TO: {recipient}")
                print("📨 MESSAGE CONTENT:")
                print("-" * 40)
                print(message)
                print("-" * 40)
                return True

        # Create test bot
        bot = TestMitzvahBot()

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

        if 'consolidation_reason' in mitzvah_data:
            print(f"🔗 Consolidation: {mitzvah_data['consolidation_reason']}")

        if mitzvah_data.get('biblical_sources'):
            print(f"📜 Biblical Sources: {', '.join(mitzvah_data['biblical_sources']) if isinstance(mitzvah_data['biblical_sources'], list) else mitzvah_data['biblical_sources']}")

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

    except ImportError as e:
        print(f"❌ Failed to import bot: {e}")
        print("💡 Make sure you're running this from the Rambam directory")
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

def main():
    """Main testing function."""
    print("Lambda Bot Testing Options:")
    print("1. Test specific date (interactive)")
    print("2. Test multiple predefined dates")
    print("3. Test with command line date")

    if len(sys.argv) > 1:
        # Command line date provided
        test_date = sys.argv[1]
        print(f"Testing with command line date: {test_date}")
        test_lambda_with_date(test_date)
    else:
        choice = input("\nChoose option (1-2): ").strip()

        if choice == '1':
            test_lambda_with_date()
        elif choice == '2':
            test_multiple_dates()
        else:
            print("Invalid choice. Using interactive mode.")
            test_lambda_with_date()

if __name__ == "__main__":
    main()