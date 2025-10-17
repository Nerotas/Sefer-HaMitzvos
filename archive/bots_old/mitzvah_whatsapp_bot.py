#!/usr/bin/env python3
"""
WhatsApp Mitzvah Bot - Daily Schedule Sender
Simple implementation using Twilio WhatsApp API
"""

import csv
import os
from datetime import datetime, timedelta
from twilio.rest import Client
import schedule
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mitzvah_bot.log'),
        logging.StreamHandler()
    ]
)

class MitzvahWhatsAppBot:
    def __init__(self):
        # Load configuration from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', '+14155238886')

        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            logging.info("Twilio client initialized successfully")
        else:
            logging.error("Missing Twilio credentials in environment variables")
            raise ValueError("Missing Twilio credentials")

        # Recipients list (add your phone numbers here)
        self.recipients = [
            # Add phone numbers in international format, e.g.:
            # '+12345678900',
            # '+19876543210'
        ]

        self.csv_file = 'Schedule_Corrected.csv'

    def load_mitzvah_for_date(self, target_date=None):
        """Load mitzvah for specific date or today."""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')

        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Date'].strip() == target_date:
                        return {
                            'date': row['Date'].strip(),
                            'mitzvos': row['Mitzvos'].strip(),
                            'title': row['English Title(s)'].strip(),
                            'source': row['Source'].strip()
                        }
            return None
        except FileNotFoundError:
            logging.error(f"Schedule file {self.csv_file} not found")
            return None
        except Exception as e:
            logging.error(f"Error reading schedule file: {e}")
            return None

    def format_message(self, mitzvah_data):
        """Format the WhatsApp message."""
        date_formatted = datetime.strptime(mitzvah_data['date'], '%Y-%m-%d').strftime('%A, %B %d, %Y')

        if mitzvah_data['mitzvos'].startswith('Intro'):
            # Introduction/Shorashim message
            message = f"""🕊️ *Sefer HaMitzvos Daily Study* 📚

📅 {date_formatted}

📖 *{mitzvah_data['mitzvos']}*
_{mitzvah_data['title']}_

📚 Source: {mitzvah_data['source']}

May your Torah study illuminate your path! ✨🙏

_—Daily Mitzvah Bot_"""
        else:
            # Regular mitzvah message
            mitzvah_num = mitzvah_data['mitzvos']
            if ',' in mitzvah_num:
                mitzvah_text = f"*Mitzvot #{mitzvah_num}*"
            else:
                mitzvah_text = f"*Mitzvah #{mitzvah_num}*"

            message = f"""🕊️ *Sefer HaMitzvos Daily Study* 📚

📅 {date_formatted}

🔢 {mitzvah_text}
_{mitzvah_data['title']}_

📚 Source: {mitzvah_data['source']}

Fulfill this mitzvah with joy and intention! 💫🙏

_—Daily Mitzvah Bot_"""

        return message

    def send_to_recipient(self, recipient, message):
        """Send message to a single recipient."""
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{recipient}'
            )
            logging.info(f"Message sent successfully to {recipient}. SID: {message_obj.sid}")
            return True
        except Exception as e:
            logging.error(f"Failed to send message to {recipient}: {e}")
            return False

    def send_daily_mitzvah(self, target_date=None):
        """Send today's mitzvah to all recipients."""
        if not self.recipients:
            logging.warning("No recipients configured")
            return

        # Load today's mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)

        if not mitzvah_data:
            date_str = target_date or "today"
            logging.warning(f"No mitzvah found for {date_str}")
            return

        # Format message
        message = self.format_message(mitzvah_data)

        # Send to all recipients
        success_count = 0
        for recipient in self.recipients:
            if self.send_to_recipient(recipient, message):
                success_count += 1
            time.sleep(2)  # Rate limiting between messages

        logging.info(f"Daily mitzvah sent to {success_count}/{len(self.recipients)} recipients")

    def test_bot(self):
        """Test the bot with today's mitzvah."""
        logging.info("Testing bot...")
        self.send_daily_mitzvah()

    def preview_message(self, target_date=None):
        """Preview the message without sending."""
        mitzvah_data = self.load_mitzvah_for_date(target_date)
        if mitzvah_data:
            message = self.format_message(mitzvah_data)
            print("=" * 50)
            print("MESSAGE PREVIEW:")
            print("=" * 50)
            print(message)
            print("=" * 50)
        else:
            date_str = target_date or "today"
            print(f"No mitzvah found for {date_str}")

def setup_schedule(bot):
    """Setup the daily schedule."""
    # Schedule daily message at 8:00 AM
    schedule.every().day.at("08:00").do(bot.send_daily_mitzvah)
    logging.info("Daily schedule set for 8:00 AM")

def main():
    """Main function to run the bot."""
    print("🕊️ Mitzvah WhatsApp Bot Starting... 📱")

    try:
        # Initialize bot
        bot = MitzvahWhatsAppBot()

        # Check if we have recipients
        if not bot.recipients:
            print("\n⚠️  No recipients configured!")
            print("Please edit the script and add phone numbers to the recipients list.")
            print("Example: '+12345678900'")
            return

        # Show preview for today
        print("\n📱 Today's message preview:")
        bot.preview_message()

        # Ask user what to do
        print("\nOptions:")
        print("1. Send test message now")
        print("2. Start daily scheduler")
        print("3. Preview tomorrow's message")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            print("\n📤 Sending test message...")
            bot.test_bot()
        elif choice == '2':
            setup_schedule(bot)
            print("\n🔄 Bot is running! Daily messages will be sent at 8:00 AM.")
            print("Press Ctrl+C to stop.")

            # Keep running
            while True:
                schedule.run_pending()
                time.sleep(60)
        elif choice == '3':
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            print(f"\n📱 Tomorrow's message ({tomorrow}):")
            bot.preview_message(tomorrow)
        elif choice == '4':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()