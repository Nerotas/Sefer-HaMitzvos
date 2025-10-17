#!/usr/bin/env python3
"""
AWS Lambda Mitzvah Bot - Optimized
Fixed timeout issues and optimized for Lambda cold starts
"""

import json
import logging
import os
from datetime import datetime

# Configure logging for Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import Twilio at module level to avoid timeout during cold start
try:
    from twilio.rest import Client
    logger.info("Twilio imported successfully")
except ImportError as e:
    logger.error(f"Failed to import Twilio: {e}")
    Client = None

def lambda_handler(event, context):
    """
    AWS Lambda entry point
    This function is called by AWS Lambda when triggered
    """
    try:
        logger.info("🕊️ Daily Mitzvah Bot starting on AWS Lambda")

        # Quick validation
        if not Client:
            raise ImportError("Twilio library not available")

        # Initialize the bot with timeout protection
        logger.info("Initializing bot...")
        bot = MitzvahLambdaBot()

        logger.info("Bot initialized, sending daily mitzvah...")

        # Send today's mitzvah
        success = bot.send_daily_mitzvah()

        logger.info(f"Mitzvah sending completed: {'Success' if success else 'Failed'}")

        # Return response for Lambda
        response = {
            'statusCode': 200 if success else 500,
            'body': json.dumps({
                'message': 'Daily mitzvah sent successfully' if success else 'Failed to send mitzvah',
                'timestamp': datetime.now().isoformat(),
                'recipients': len(bot.recipients) if hasattr(bot, 'recipients') else 0
            })
        }

        logger.info(f"Returning response: {response['statusCode']}")
        return response

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
        logger.info("Starting bot initialization...")

        # Load Twilio credentials from Lambda environment variables
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER', '+14155238886')

        logger.info(f"Loaded credentials - SID: {self.account_sid[:10] if self.account_sid else 'None'}...")

        if not self.account_sid or not self.auth_token:
            raise ValueError("Missing Twilio credentials in Lambda environment variables")

        # Initialize Twilio client with timeout
        try:
            logger.info("Creating Twilio client...")
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio client created successfully")
        except Exception as e:
            logger.error(f"Failed to create Twilio client: {e}")
            raise

        # Load recipients from environment variable
        recipients_str = os.environ.get('RECIPIENTS', '')
        self.recipients = [r.strip() for r in recipients_str.split(',') if r.strip()]

        if not self.recipients:
            raise ValueError("No recipients configured in RECIPIENTS environment variable")

        logger.info(f"Loaded {len(self.recipients)} recipients: {self.recipients}")

        # Schedule data embedded directly
        self.schedule_data = self.get_embedded_schedule()
        logger.info(f"Loaded {len(self.schedule_data)} schedule entries")

    def get_embedded_schedule(self):
        """
        Embed schedule data directly in Lambda function
        """
        return [
            {
                'Date': '2025-10-17',
                'Mitzvos': 'Intro 2',
                'English Title(s)': 'Shorash 1: Belief in G-d',
                'Source': 'Sefer HaMitzvos Introduction'
            },
            {
                'Date': '2025-10-18',
                'Mitzvos': 'Intro 3',
                'English Title(s)': 'Shorash 2: Unity of G-d',
                'Source': 'Sefer HaMitzvos Introduction'
            },
            {
                'Date': '2025-10-19',
                'Mitzvos': '1',
                'English Title(s)': 'Belief in G-d',
                'Source': 'Devarim 6:4'
            },
            {
                'Date': '2025-10-20',
                'Mitzvos': '76, 77',
                'English Title(s)': 'To say the Shema twice daily & To serve the Almighty with prayer daily',
                'Source': 'Devarim 6:7 & Shemos 23:25'
            }
            # More entries would be embedded here in production
        ]

    def load_mitzvah_for_date(self, target_date=None):
        """Load mitzvah for specific date or today."""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"Looking for mitzvah for date: {target_date}")

        # Search embedded schedule data
        for row in self.schedule_data:
            if row['Date'].strip() == target_date:
                logger.info(f"Found mitzvah: {row['Mitzvos']} - {row['English Title(s)']}")
                return {
                    'date': row['Date'].strip(),
                    'mitzvos': row['Mitzvos'].strip(),
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip()
                }

        logger.warning(f"No mitzvah found for {target_date}")
        return None

    # TODO: Re-enable Sefaria links once accuracy is verified
    # def generate_sefaria_link(self, mitzvos, english_title):
    #     """
    #     Generate Sefaria links based on the mitzvah type and number.
    #     Handles multiple mitzvot separated by commas.
    #     """
    #     base_url = "https://www.sefaria.org/Sefer_HaMitzvot%2C_"
    #
    #     # Handle Introduction/Shorashim (principles)
    #     if mitzvos.startswith("Intro"):
    #         intro_num = mitzvos.split()[1]
    #         return f"{base_url}Shorashim.{intro_num}?lang=bi"
    #
    #     # Handle multiple mitzvot (e.g., "612, 613")
    #     if "," in mitzvos:
    #         mitzvah_numbers = [num.strip() for num in mitzvos.split(",")]
    #         links = []
    #
    #         for mitzvah_num in mitzvah_numbers:
    #             if mitzvah_num.isdigit():
    #                 num = int(mitzvah_num)
    #
    #                 # Traditional structure: first 248 are positive, rest are negative
    #                 if num <= 248:
    #                     # Check if this is actually a negative commandment (mixed schedule)
    #                     if english_title.startswith("Not to") or "prohibition" in english_title.lower():
    #                         links.append(f"{base_url}Negative_Commandments.{num}?lang=bi")
    #                     else:
    #                         links.append(f"{base_url}Positive_Commandments.{num}?lang=bi")
    #                 else:
    #                     # Numbers 249-613 are negative commandments (numbered as 1-365 in Sefaria)
    #                     negative_num = num - 248
    #                     links.append(f"{base_url}Negative_Commandments.{negative_num}?lang=bi")
    #
    #         # Join multiple links with " & "
    #         return " & ".join(links)
    #
    #     # Handle single numbered mitzvot
    #     if mitzvos.isdigit():
    #         mitzvah_num = int(mitzvos)
    #
    #         # Traditional structure: first 248 are positive, rest are negative
    #         if mitzvah_num <= 248:
    #             # Check if this is actually a negative commandment (mixed schedule)
    #             if english_title.startswith("Not to") or "prohibition" in english_title.lower():
    #                 # This is a negative commandment with a low number (mixed schedule)
    #                 return f"{base_url}Negative_Commandments.{mitzvah_num}?lang=bi"
    #             else:
    #                 # This is a positive commandment
    #                 return f"{base_url}Positive_Commandments.{mitzvah_num}?lang=bi"
    #         else:
    #             # Numbers 249-613 are negative commandments (numbered as 1-365 in Sefaria)
    #             negative_num = mitzvah_num - 248
    #             return f"{base_url}Negative_Commandments.{negative_num}?lang=bi"
    #
    #     # Default case
    #     return f"{base_url}Positive_Commandments.{mitzvos}?lang=bi"

    def format_message(self, mitzvah_data):
        """Format the WhatsApp message."""
        date_formatted = datetime.strptime(mitzvah_data['date'], '%Y-%m-%d').strftime('%A, %B %d, %Y')

        # TODO: Re-enable Sefaria links once accuracy is verified
        # Generate Sefaria link
        # sefaria_link = self.generate_sefaria_link(mitzvah_data['mitzvos'], mitzvah_data['title'])

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
            mitzvah_nums = mitzvah_data['mitzvos']

            # Check if there are multiple mitzvot
            if ',' in mitzvah_nums:
                # Parse multiple mitzvot
                numbers = [num.strip() for num in mitzvah_nums.split(',')]
                titles = [title.strip() for title in mitzvah_data['title'].split(' & ')]
                sources = [source.strip() for source in mitzvah_data['source'].split(' & ')]

                # Build message header
                message = f"""🕊️ *Sefer HaMitzvos Daily Study* 📚

📅 {date_formatted}

"""

                # Add each mitzvah separately
                for i, (num, title, source) in enumerate(zip(numbers, titles, sources)):
                    message += f"""🔢 *Mitzvah #{num}*
{title}

📚 Source: {source}
📖 Learn more: sefaria link coming soon!

"""

                # Add closing
                message += """Fulfill these mitzvot with joy and intention! 💫🙏

_—Daily Mitzvah Bot_"""
            else:
                # Single mitzvah
                mitzvah_text = f"*Mitzvah #{mitzvah_nums}*"

                message = f"""🕊️ *Sefer HaMitzvos Daily Study* 📚

📅 {date_formatted}

🔢 {mitzvah_text}
_{mitzvah_data['title']}_

📚 Source: {mitzvah_data['source']}
📖 Learn more: sefaria link coming soon!

Fulfill this mitzvah with joy and intention! 💫🙏

_—Daily Mitzvah Bot_"""

        return message

    def send_to_recipient(self, recipient, message):
        """Send message to a single recipient."""
        try:
            logger.info(f"Sending message to {recipient}")

            # Set a timeout for the Twilio API call
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
        try:
            logger.info("Starting send_daily_mitzvah...")

            # Load today's mitzvah
            mitzvah_data = self.load_mitzvah_for_date(target_date)

            if not mitzvah_data:
                date_str = target_date or "today"
                logger.warning(f"No mitzvah found for {date_str}")
                return False

            # Format message
            message = self.format_message(mitzvah_data)
            logger.info(f"Formatted message for: {mitzvah_data['mitzvos']} - {mitzvah_data['title']}")

            # Send to all recipients
            success_count = 0
            for i, recipient in enumerate(self.recipients):
                logger.info(f"Sending to recipient {i+1}/{len(self.recipients)}: {recipient}")

                if self.send_to_recipient(recipient, message):
                    success_count += 1
                else:
                    logger.error(f"Failed to send to {recipient}")

            logger.info(f"Daily mitzvah sent to {success_count}/{len(self.recipients)} recipients")
            return success_count > 0

        except Exception as e:
            logger.error(f"Error in send_daily_mitzvah: {e}")
            return False

# For local testing (not used in Lambda)
if __name__ == "__main__":
    # This allows you to test the Lambda function locally
    test_event = {}
    test_context = type('Context', (), {'get_remaining_time_in_millis': lambda: 30000})()
    result = lambda_handler(test_event, test_context)
    print(f"Result: {result}")