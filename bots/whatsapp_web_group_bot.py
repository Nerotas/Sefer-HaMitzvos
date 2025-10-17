#!/usr/bin/env python3
"""
WhatsApp Web Group Bot - Free Alternative to Twilio
Uses browser automation to send messages to WhatsApp groups
No API keys or approvals required!
"""

import csv
import pywhatkit as kit
from datetime import datetime, timedelta
import time
import schedule
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppWebGroupBot:
    def __init__(self):
        # Configuration
        self.csv_file = 'Schedule_Corrected.csv'

        # Group configuration - replace with your actual group ID
        # Get group ID from WhatsApp Web: Open group -> F12 -> Console -> Store.Chat.getActive().id._serialized
        self.group_id = "JpwWqLb9Dv0K8KUQsX3KcO"  # Your group code from the invite link

        # Alternative: Individual phone numbers (international format)
        self.individual_recipients = [
            # "+12345678900",  # Add individual numbers if needed
            # "+19876543210"
        ]

        logging.info(f"WhatsApp Web Bot initialized for group: {self.group_id}")

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

    def send_to_group(self, message, hour=None, minute=None):
        """Send message to WhatsApp group using pywhatkit."""
        try:
            # If no time specified, send immediately (next minute)
            if hour is None or minute is None:
                now = datetime.now()
                hour = now.hour
                minute = now.minute + 2  # Send in 2 minutes to allow setup
                if minute >= 60:
                    hour += 1
                    minute -= 60

            logging.info(f"Scheduling message to group {self.group_id} at {hour:02d}:{minute:02d}")

            # Send to group
            kit.sendwhatmsg_to_group(
                group_id=self.group_id,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=15,  # Wait 15 seconds for WhatsApp Web to load
                tab_close=True  # Close tab after sending
            )

            logging.info("Message sent successfully to group!")
            return True

        except Exception as e:
            logging.error(f"Failed to send message to group: {e}")
            return False

    def send_to_individuals(self, message, hour=None, minute=None):
        """Send message to individual recipients."""
        if not self.individual_recipients:
            return True

        success_count = 0
        for recipient in self.individual_recipients:
            try:
                # If no time specified, send immediately
                if hour is None or minute is None:
                    now = datetime.now()
                    hour = now.hour
                    minute = now.minute + 2 + success_count  # Stagger sends
                    if minute >= 60:
                        hour += 1
                        minute -= 60

                kit.sendwhatmsg(
                    phone_no=recipient,
                    message=message,
                    time_hour=hour,
                    time_min=minute,
                    wait_time=15,
                    tab_close=True
                )

                success_count += 1
                logging.info(f"Message sent to {recipient}")
                time.sleep(5)  # Wait between sends

            except Exception as e:
                logging.error(f"Failed to send to {recipient}: {e}")

        return success_count > 0

    def send_daily_mitzvah(self, target_date=None):
        """Send today's mitzvah to group and individuals."""
        # Load today's mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)

        if not mitzvah_data:
            date_str = target_date or "today"
            logging.warning(f"No mitzvah found for {date_str}")
            return

        # Format message
        message = self.format_message(mitzvah_data)

        # Send to group
        group_success = self.send_to_group(message)

        # Send to individuals (if any)
        individual_success = self.send_to_individuals(message)

        if group_success or individual_success:
            logging.info("Daily mitzvah sent successfully!")
        else:
            logging.error("Failed to send daily mitzvah")

    def run_scheduler(self):
        """Run the daily scheduler."""
        # Schedule daily message at 8:00 AM
        schedule.every().day.at("11:30").do(self.send_daily_mitzvah)
        logging.info("Daily schedule set for 11:30 AM")

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """Main function."""
    logging.info("🕊️ WhatsApp Web Mitzvah Bot Starting...")

    try:
        # Initialize bot
        bot = WhatsAppWebGroupBot()

        # Check mode
        mode = os.getenv('BOT_MODE', 'test').lower()

        if mode == 'test':
            # Test mode - send one message
            logging.info("Running in TEST mode - sending one message")
            bot.send_daily_mitzvah()

        elif mode == 'scheduler':
            # Scheduler mode - run continuously
            logging.info("Running in SCHEDULER mode - daily messages at 8 AM")
            bot.run_scheduler()

        else:
            # Default - send today's message once
            logging.info("Sending today's message once")
            bot.send_daily_mitzvah()

    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot error: {e}")

if __name__ == "__main__":
    main()