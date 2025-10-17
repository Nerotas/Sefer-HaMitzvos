#!/usr/bin/env python3
"""
AWS Lambda Mitzvah Bot
Optimized for serverless execution on AWS Lambda
Triggered by CloudWatch Events daily at 1:10 PM CST
"""

import csv
import json
import logging
import os
from datetime import datetime
from io import StringIO

# Configure logging for Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda entry point
    This function is called by AWS Lambda when triggered
    """
    try:
        logger.info("🕊️ Daily Mitzvah Bot starting on AWS Lambda")

        # Initialize the bot
        bot = MitzvahLambdaBot()

        # Send today's mitzvah
        success = bot.send_daily_mitzvah()

        # Return response for Lambda
        return {
            'statusCode': 200 if success else 500,
            'body': json.dumps({
                'message': 'Daily mitzvah sent successfully' if success else 'Failed to send mitzvah',
                'timestamp': datetime.now().isoformat(),
                'recipients': len(bot.recipients)
            })
        }

    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

class MitzvahLambdaBot:
    def __init__(self):
        """Initialize the Lambda bot with environment variables."""
        # Load Twilio credentials from Lambda environment variables
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER', '+14155238886')

        if not self.account_sid or not self.auth_token:
            raise ValueError("Missing Twilio credentials in Lambda environment variables")

        # Initialize Twilio client
        from twilio.rest import Client
        self.client = Client(self.account_sid, self.auth_token)
        logger.info("Twilio client initialized successfully")

        # Load recipients from environment variable
        recipients_str = os.environ.get('RECIPIENTS', '')
        self.recipients = [r.strip() for r in recipients_str.split(',') if r.strip()]

        if not self.recipients:
            raise ValueError("No recipients configured in RECIPIENTS environment variable")

        logger.info(f"Loaded {len(self.recipients)} recipients")

        # CSV data is embedded in the function (Lambda limitation)
        self.schedule_data = self.get_embedded_schedule()

    def get_embedded_schedule(self):
        """
        Embed schedule data directly in Lambda function
        Lambda has limited file system access, so we embed the CSV data
        """
        # This will be populated with your schedule data
        # For now, return a sample - we'll update this with your actual CSV
        return [
            {
                'Date': '2025-10-17',
                'Mitzvos': 'Intro 2',
                'English Title(s)': 'Shorash 1: Belief in G-d',
                'Source': 'Sefer HaMitzvos Introduction'
            }
            # Additional entries will be added here
        ]

    def load_mitzvah_for_date(self, target_date=None):
        """Load mitzvah for specific date or today."""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')

        # Search embedded schedule data
        for row in self.schedule_data:
            if row['Date'].strip() == target_date:
                return {
                    'date': row['Date'].strip(),
                    'mitzvos': row['Mitzvos'].strip(),
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip()
                }

        logger.warning(f"No mitzvah found for {target_date}")
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

_—Daily Mitzvah Bot (AWS Lambda)_"""
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

_—Daily Mitzvah Bot (AWS Lambda)_"""

        return message

    def send_to_recipient(self, recipient, message):
        """Send message to a single recipient."""
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{recipient}'
            )
            logger.info(f"Message sent successfully to {recipient}. SID: {message_obj.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {recipient}: {e}")
            return False

    def send_daily_mitzvah(self, target_date=None):
        """Send today's mitzvah to all recipients."""
        # Load today's mitzvah
        mitzvah_data = self.load_mitzvah_for_date(target_date)

        if not mitzvah_data:
            date_str = target_date or "today"
            logger.warning(f"No mitzvah found for {date_str}")
            return False

        # Format message
        message = self.format_message(mitzvah_data)
        logger.info(f"Sending mitzvah: {mitzvah_data['mitzvos']} - {mitzvah_data['title']}")

        # Send to all recipients
        success_count = 0
        for recipient in self.recipients:
            if self.send_to_recipient(recipient, message):
                success_count += 1

        logger.info(f"Daily mitzvah sent to {success_count}/{len(self.recipients)} recipients")
        return success_count > 0

# For local testing (not used in Lambda)
if __name__ == "__main__":
    # This allows you to test the Lambda function locally
    test_event = {}
    test_context = {}
    result = lambda_handler(test_event, test_context)
    print(f"Result: {result}")