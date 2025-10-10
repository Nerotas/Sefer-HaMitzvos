#!/usr/bin/env python3
"""
WhatsApp Mitzvah Bot - Cloud Optimized Version
Loads recipients from environment variables for easy cloud deployment
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
        logging.StreamHandler()
    ]
)

class MitzvahWhatsAppBotCloud:
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

        # Load recipients from environment variables
        self.recipients = self.load_recipients_from_env()

        if not self.recipients:
            logging.warning("No recipients configured")
        else:
            logging.info(f"Loaded {len(self.recipients)} recipients")

        self.csv_file = 'Schedule_Corrected.csv'

    def load_recipients_from_env(self):
        """Load recipient phone numbers from environment variables."""
        recipients = []

        # Load from RECIPIENTS (comma-separated)
        recipients_env = os.getenv('RECIPIENTS', '')
        if recipients_env:
            recipients.extend([r.strip() for r in recipients_env.split(',') if r.strip()])

        # Load from individual RECIPIENT_N variables
        i = 1
        while True:
            recipient = os.getenv(f'RECIPIENT_{i}')
            if recipient:
                recipients.append(recipient.strip())
                i += 1
            else:
                break

        # Remove duplicates while preserving order
        seen = set()
        unique_recipients = []
        for r in recipients:
            if r not in seen:
                seen.add(r)
                unique_recipients.append(r)

        return unique_recipients

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

    def run_scheduler(self):
        """Run the daily scheduler."""
        # Schedule daily message at 8:00 AM
        schedule.every().day.at("08:00").do(self.send_daily_mitzvah)
        logging.info("Daily schedule set for 8:00 AM UTC")

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """Main function optimized for cloud deployment."""
    logging.info("🕊️ Mitzvah WhatsApp Bot (Cloud Version) Starting...")

    try:
        # Initialize bot
        bot = MitzvahWhatsAppBotCloud()

        # Check deployment mode
        deploy_mode = os.getenv('DEPLOY_MODE', 'scheduler').lower()

        if deploy_mode == 'test':
            # Test mode - send one message and exit
            logging.info("Running in TEST mode")
            bot.send_daily_mitzvah()

        elif deploy_mode == 'once':
            # Send today's message once and exit
            logging.info("Running in ONCE mode")
            bot.send_daily_mitzvah()

        else:
            # Default scheduler mode
            logging.info("Running in SCHEDULER mode")
            logging.info("Bot will send daily messages at 8:00 AM UTC")
            bot.run_scheduler()

    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot error: {e}")
        raise

if __name__ == "__main__":
    main()