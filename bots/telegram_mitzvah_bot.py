#!/usr/bin/env python3
"""
Telegram Mitzvah Bot - Free and Reliable Alternative
100% free, no sandbox limitations, easy group support
"""

import csv
import os
from datetime import datetime, timedelta
import schedule
import time
import logging
import asyncio

# Telegram bot library - install with: pip install python-telegram-bot
from telegram import Bot
from telegram.ext import Application

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TelegramMitzvahBot:
    def __init__(self):
        # Get bot token from environment variable
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable required")

        # Initialize bot
        self.bot = Bot(token=self.bot_token)

        # Load chat IDs from environment
        self.chat_ids = self.load_chat_ids_from_env()

        self.csv_file = 'Schedule_Corrected.csv'
        logging.info(f"Telegram bot initialized with {len(self.chat_ids)} recipients")

    def load_chat_ids_from_env(self):
        """Load Telegram chat IDs from environment variables."""
        chat_ids = []

        # Load from TELEGRAM_CHATS (comma-separated)
        chats_env = os.getenv('TELEGRAM_CHATS', '')
        if chats_env:
            chat_ids.extend([c.strip() for c in chats_env.split(',') if c.strip()])

        # Load from individual TELEGRAM_CHAT_N variables
        i = 1
        while True:
            chat = os.getenv(f'TELEGRAM_CHAT_{i}')
            if chat:
                chat_ids.append(chat.strip())
                i += 1
            else:
                break

        return chat_ids

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
        """Format the Telegram message with Markdown."""
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

    async def send_to_chat(self, chat_id, message):
        """Send message to a single chat."""
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logging.info(f"Message sent successfully to chat {chat_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to send message to {chat_id}: {e}")
            return False

    async def send_daily_mitzvah(self, target_date=None):
        """Send today's mitzvah to all chats."""
        if not self.chat_ids:
            logging.warning("No chat IDs configured")
            return

        # Load today's mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)

        if not mitzvah_data:
            date_str = target_date or "today"
            logging.warning(f"No mitzvah found for {date_str}")
            return

        # Format message
        message = self.format_message(mitzvah_data)

        # Send to all chats
        success_count = 0
        for chat_id in self.chat_ids:
            if await self.send_to_chat(chat_id, message):
                success_count += 1
            await asyncio.sleep(1)  # Rate limiting

        logging.info(f"Daily mitzvah sent to {success_count}/{len(self.chat_ids)} chats")

    def run_scheduler(self):
        """Run the daily scheduler."""
        async def scheduled_send():
            await self.send_daily_mitzvah()

        def sync_send():
            asyncio.run(scheduled_send())

        # Schedule daily message at 8:00 AM
        schedule.every().day.at("08:00").do(sync_send)
        logging.info("Daily schedule set for 8:00 AM UTC")

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """Main function."""
    logging.info("🕊️ Telegram Mitzvah Bot Starting...")

    try:
        # Initialize bot
        bot = TelegramMitzvahBot()

        # Check deployment mode
        deploy_mode = os.getenv('DEPLOY_MODE', 'scheduler').lower()

        if deploy_mode == 'test':
            # Test mode - send one message and exit
            logging.info("Running in TEST mode")
            asyncio.run(bot.send_daily_mitzvah())

        elif deploy_mode == 'once':
            # Send today's message once and exit
            logging.info("Running in ONCE mode")
            asyncio.run(bot.send_daily_mitzvah())

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