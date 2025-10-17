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

        # Group configuration - disabled for personal messagings
        # Get group ID from WhatsApp Web: Open group -> F12 -> Console -> Store.Chat.getActive().id._serialized
        self.group_id = None  # Disabled - using personal number instead

        # Personal phone number (international format) - REPLACE WITH YOUR NUMBER
        self.individual_recipients = [
            "+16613059259",  # Replace with your actual phone number (include country code)
        ]

        logging.info(f"WhatsApp Web Bot initialized for personal messaging to: {self.individual_recipients}")

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
        """Send today's mitzvah to personal number."""
        # Load today's mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)

        if not mitzvah_data:
            date_str = target_date or "today"
            logging.warning(f"No mitzvah found for {date_str}")
            return

        # Format message
        message = self.format_message(mitzvah_data)

        # Send to personal number
        individual_success = self.send_to_individuals(message)

        if individual_success:
            logging.info(f"Daily mitzvah sent to {len(self.individual_recipients)}/{len(self.individual_recipients)} recipients")
        else:
            logging.error("Failed to send daily mitzvah")

    def send_deployment_notification(self):
        """Send a notification when the bot is deployed/started."""
        try:
            deploy_info = self.get_deployment_info()
            message = f"""🚀 *Bot Deployment Notification*

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🤖 Status: Bot Started Successfully
🌐 Environment: {deploy_info['environment']}
📝 Version: {deploy_info['version']}
🔧 Mode: {deploy_info['mode']}

✅ Daily Mitzvah Bot is now running!

_—Deployment Monitor_"""

            # Send immediately (in 1 minute to ensure WhatsApp Web loads)
            success = self.send_to_individuals(message)
            if success:
                logging.info("Deployment notification sent successfully!")
            else:
                logging.warning("Failed to send deployment notification")

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
        mode = os.getenv('BOT_MODE', 'test').upper()

        return {
            'environment': environment,
            'version': version,
            'mode': mode,
            'timestamp': datetime.now().isoformat()
        }

    def send_shutdown_notification(self):
        """Send notification when bot is shutting down."""
        try:
            message = f"""🛑 *Bot Shutdown Notification*

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🤖 Status: Bot Shutting Down
📊 Reason: Graceful Shutdown

ℹ️ Daily Mitzvah Bot will restart automatically.

_—Deployment Monitor_"""

            # Send immediately
            self.send_to_individuals(message)
            logging.info("Shutdown notification sent")

        except Exception as e:
            logging.error(f"Error sending shutdown notification: {e}")

    def run_scheduler(self):
        """Run the daily scheduler."""
        # Send deployment notification on startup
        if os.getenv('SEND_DEPLOY_NOTIFICATIONS', 'true').lower() == 'true':
            self.send_deployment_notification()

        # Schedule daily message at 8:00 AM
        schedule.every().day.at("08:00").do(self.send_daily_mitzvah)
        logging.info("Daily schedule set for 8:00 AM")

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
        send_notifications = os.getenv('SEND_DEPLOY_NOTIFICATIONS', 'true').lower() == 'true'

        if mode == 'test':
            # Test mode - send one message
            logging.info("Running in TEST mode - sending one message")
            if send_notifications:
                bot.send_deployment_notification()
            bot.send_daily_mitzvah()

        elif mode == 'scheduler':
            # Scheduler mode - run continuously
            logging.info("Running in SCHEDULER mode - daily messages at 8 AM")
            bot.run_scheduler()  # This will send deployment notification internally

        else:
            # Default - send today's message once
            logging.info("Sending today's message once")
            if send_notifications:
                bot.send_deployment_notification()
            bot.send_daily_mitzvah()

    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
        try:
            if send_notifications:
                bot.send_shutdown_notification()
        except:
            pass
    except Exception as e:
        logging.error(f"Bot error: {e}")
        try:
            if send_notifications and 'bot' in locals():
                error_message = f"""❌ *Bot Error Notification*

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🚨 Error: {str(e)[:100]}...
🔄 Status: Bot will restart automatically

_—Error Monitor_"""
                bot.send_to_group(error_message)
        except:
            pass
        raise

if __name__ == "__main__":
    main()