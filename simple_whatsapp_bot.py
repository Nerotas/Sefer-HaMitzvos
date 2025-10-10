#!/usr/bin/env python3
"""
Simple WhatsApp Bot using WhatsApp Web
No API keys required - uses browser automation
"""

import csv
import pywhatkit as kit
from datetime import datetime, timedelta
import time
import schedule
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleWhatsAppBot:
    def __init__(self):
        # Add your recipient phone numbers here (international format)
        self.recipients = [
            # "+12345678900",  # Example - replace with actual numbers
            # "+19876543210"
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
        except Exception as e:
            logging.error(f"Error reading schedule: {e}")
            return None

    def format_message(self, mitzvah_data):
        """Format the WhatsApp message."""
        date_formatted = datetime.strptime(mitzvah_data['date'], '%Y-%m-%d').strftime('%A, %B %d, %Y')

        if mitzvah_data['mitzvos'].startswith('Intro'):
            message = f"""🕊️ Sefer HaMitzvos Daily Study 📚

📅 {date_formatted}

📖 {mitzvah_data['mitzvos']}
{mitzvah_data['title']}

📚 {mitzvah_data['source']}

May your Torah study bring blessing! ✨🙏"""
        else:
            mitzvah_num = mitzvah_data['mitzvos']
            if ',' in mitzvah_num:
                prefix = f"Mitzvot #{mitzvah_num}"
            else:
                prefix = f"Mitzvah #{mitzvah_num}"

            message = f"""🕊️ Sefer HaMitzvos Daily Study 📚

📅 {date_formatted}

🔢 {prefix}
{mitzvah_data['title']}

📚 {mitzvah_data['source']}

Fulfill with joy and intention! 💫🙏"""

        return message

    def send_daily_mitzvah(self, target_date=None):
        """Send today's mitzvah to all recipients."""
        if not self.recipients:
            logging.warning("No recipients configured")
            print("⚠️ No recipients configured! Please add phone numbers to the recipients list.")
            return

        # Load mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)
        if not mitzvah_data:
            logging.warning(f"No mitzvah found for {target_date or 'today'}")
            return

        message = self.format_message(mitzvah_data)

        # Calculate send time (2 minutes from now)
        current_time = datetime.now()
        send_hour = current_time.hour
        send_minute = current_time.minute + 2

        if send_minute >= 60:
            send_hour += 1
            send_minute -= 60

        print(f"📤 Scheduling messages to be sent at {send_hour:02d}:{send_minute:02d}")

        # Send to each recipient
        for i, phone in enumerate(self.recipients):
            try:
                # Add 1 minute delay between each recipient
                actual_minute = send_minute + i
                actual_hour = send_hour

                if actual_minute >= 60:
                    actual_hour += 1
                    actual_minute -= 60

                kit.sendwhatmsg(phone, message, actual_hour, actual_minute, 15, True, 2)
                logging.info(f"Message scheduled for {phone} at {actual_hour:02d}:{actual_minute:02d}")

            except Exception as e:
                logging.error(f"Error sending to {phone}: {e}")

        print("✅ Messages scheduled! WhatsApp Web will open automatically.")

    def preview_message(self, target_date=None):
        """Preview message without sending."""
        mitzvah_data = self.load_mitzvah_for_date(target_date)
        if mitzvah_data:
            message = self.format_message(mitzvah_data)
            print("=" * 60)
            print("MESSAGE PREVIEW:")
            print("=" * 60)
            print(message)
            print("=" * 60)
        else:
            print(f"No mitzvah found for {target_date or 'today'}")

def main():
    print("🕊️ Simple WhatsApp Mitzvah Bot 📱")
    print("Uses WhatsApp Web - No API keys needed!")

    bot = SimpleWhatsAppBot()

    if not bot.recipients:
        print("\n⚠️ No recipients configured!")
        print("Please edit the script and add phone numbers to the recipients list.")
        print("Example: '+12345678900'")
        return

    print(f"\n📱 Recipients: {len(bot.recipients)} number(s)")

    # Show today's preview
    print("\n📖 Today's mitzvah:")
    bot.preview_message()

    print("\nOptions:")
    print("1. Send now")
    print("2. Preview tomorrow")
    print("3. Exit")

    choice = input("\nChoice (1-3): ").strip()

    if choice == '1':
        print("\n📤 Preparing to send...")
        print("⚠️ Make sure WhatsApp Web is logged in on your default browser!")
        input("Press Enter when ready...")
        bot.send_daily_mitzvah()

    elif choice == '2':
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"\n📖 Tomorrow's mitzvah ({tomorrow}):")
        bot.preview_message(tomorrow)

    else:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()