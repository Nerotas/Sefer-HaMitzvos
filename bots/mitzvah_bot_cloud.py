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

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logging.warning("python-dotenv not installed, using system environment variables only")

# Set timezone for Railway deployment
if os.getenv('TZ'):
    os.environ['TZ'] = os.getenv('TZ')
    time.tzset() if hasattr(time, 'tzset') else None

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

        # Log timezone info for debugging
        current_time = datetime.now()
        logging.info(f"Current local time: {current_time}")
        logging.info(f"Timezone: {time.tzname}")
        logging.info(f"Scheduled delivery: 1:00 PM daily ({current_time.strftime('%Z')} timezone)")

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

    def send_deployment_notification(self):
        """Send a notification when the bot is deployed/started."""
        if not self.recipients:
            return

        try:
            deploy_info = self.get_deployment_info()
            message = f"""🚀 *Bot Deployment Notification*

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🤖 Status: Bot Started Successfully
🌐 Environment: {deploy_info['environment']}
📝 Version: {deploy_info['version']}
🔧 Mode: {deploy_info['mode']}
👥 Recipients: {len(self.recipients)}

✅ Daily Mitzvah Bot is now running!

_—Deployment Monitor_"""

            # Send to all recipients
            success_count = 0
            for recipient in self.recipients:
                if self.send_to_recipient(recipient, message):
                    success_count += 1
                time.sleep(1)  # Rate limiting

            logging.info(f"Deployment notification sent to {success_count}/{len(self.recipients)} recipients")

        except Exception as e:
            logging.error(f"Error sending deployment notification: {e}")

    def get_deployment_info(self):
        """Get deployment information for notifications."""
        import platform

        # Detect environment
        environment = "Unknown"
        if os.getenv('RAILWAY_ENVIRONMENT'):
            environment = f"Railway ({os.getenv('RAILWAY_ENVIRONMENT', 'production')})"
        elif os.getenv('HEROKU_APP_NAME'):
            environment = f"Heroku ({os.getenv('HEROKU_APP_NAME')})"
        elif os.getenv('RENDER_SERVICE_NAME'):
            environment = f"Render ({os.getenv('RENDER_SERVICE_NAME')})"
        elif os.getenv('VERCEL_ENV'):
            environment = f"Vercel ({os.getenv('VERCEL_ENV')})"
        else:
            environment = f"Local ({platform.system()})"

        # Get version info
        version = os.getenv('BOT_VERSION', 'v1.0.0')

        # Get mode
        mode = os.getenv('DEPLOY_MODE', 'scheduler').upper()

        return {
            'environment': environment,
            'version': version,
            'mode': mode,
            'timestamp': datetime.now().isoformat()
        }

    def send_error_notification(self, error_message):
        """Send notification when an error occurs."""
        if not self.recipients:
            return

        try:
            message = f"""❌ *Bot Error Notification*

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🚨 Error: {str(error_message)[:100]}...
🔄 Status: Bot will restart automatically

_—Error Monitor_"""

            # Send to first recipient only to avoid spam
            if self.recipients:
                self.send_to_recipient(self.recipients[0], message)

        except Exception as e:
            logging.error(f"Error sending error notification: {e}")

    def run_scheduler(self):
        """Run the daily scheduler."""
        # Send deployment notification on startup
        if os.getenv('SEND_DEPLOY_NOTIFICATIONS', 'true').lower() == 'true':
            self.send_deployment_notification()

        # Schedule daily message at 1:08 PM CST (TEST - 2 minutes from now)
        schedule.every().day.at("13:08").do(self.send_daily_mitzvah)
        logging.info("Daily schedule set for 1:08 PM CST (TEST MODE)")

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
        send_notifications = os.getenv('SEND_DEPLOY_NOTIFICATIONS', 'true').lower() == 'true'

        if deploy_mode == 'test':
            # Test mode - send one message and exit
            logging.info("Running in TEST mode")
            if send_notifications:
                bot.send_deployment_notification()
            bot.send_daily_mitzvah()

        elif deploy_mode == 'once':
            # Send today's message once and exit
            logging.info("Running in ONCE mode")
            if send_notifications:
                bot.send_deployment_notification()
            bot.send_daily_mitzvah()

        else:
            # Default scheduler mode
            logging.info("Running in SCHEDULER mode")
            logging.info("Bot will send daily messages at 8:00 AM UTC")
            bot.run_scheduler()  # This will send deployment notification internally

    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot error: {e}")
        try:
            if send_notifications and 'bot' in locals():
                bot.send_error_notification(e)
        except:
            pass
        raise

if __name__ == "__main__":
    main()