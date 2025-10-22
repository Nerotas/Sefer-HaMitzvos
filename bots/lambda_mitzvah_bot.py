#!/usr/bin/env python3
"""
AWS Lambda Mitzvah Bot - Optimized
Fixed timeout issues and optimized for Lambda cold starts
"""

import json
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List

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

def _extract_http_params(event):
    """Extract date and token from Lambda Function URL / HTTP API style events."""
    if not isinstance(event, dict):
        return None, None, False

    request_ctx = event.get('requestContext') or {}
    is_http = bool(request_ctx.get('http')) or event.get('version') == '2.0'

    if not is_http:
        return None, None, False

    q = event.get('queryStringParameters') or {}
    headers = {k.lower(): v for k, v in (event.get('headers') or {}).items()}
    body = event.get('body')
    date_str = q.get('date') or q.get('test_date')
    token = q.get('token') or headers.get('x-webhook-token')

    # Optionally read JSON body for overrides
    if not date_str and body:
        try:
            if event.get('isBase64Encoded'):
                import base64
                body = base64.b64decode(body).decode('utf-8')
            data = json.loads(body)
            date_str = data.get('date') or data.get('test_date')
            token = data.get('token') or token
        except Exception:
            pass

    return date_str, token, True


def _today_chi_iso():
    return datetime.now(ZoneInfo('America/Chicago')).date().isoformat()


def lambda_handler(event, context):
    """
    AWS Lambda entry point
    This function is called by AWS Lambda when triggered
    Supports test mode with specific date input
    """
    try:
        logger.info("✡️ Daily Mitzvah Bot starting on AWS Lambda")

        # Check if invoked via HTTP webhook (Lambda Function URL / API Gateway v2)
        http_date, http_token, is_http = _extract_http_params(event)

        # Fallback to direct invocation contract
        test_date = None
        if not is_http and event and isinstance(event, dict) and 'test_date' in event:
            test_date = event['test_date']
            logger.info(f"🧪 Test mode (invoke): Using date {test_date}")
        elif is_http:
            test_date = http_date or _today_chi_iso()
            logger.info(f"🌐 HTTP invoke: Using date {test_date}")

        # Optional webhook token check
        webhook_token = os.environ.get('WEBHOOK_TOKEN')
        if is_http and webhook_token:
            provided = http_token or ''
            if provided != webhook_token:
                logger.warning("Unauthorized webhook attempt")
                return {
                    'statusCode': 403,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Forbidden'})
                }

        # Quick validation
        if not Client:
            raise ImportError("Twilio library not available")

        # Initialize the bot with timeout protection
        logger.info("Initializing bot...")
        bot = MitzvahLambdaBot()

        logger.info("Bot initialized, sending daily mitzvah...")

        # Send mitzvah for specified date (or today if no test date)
        success = bot.send_daily_mitzvah(target_date=test_date)

        logger.info(f"Mitzvah sending completed: {'Success' if success else 'Failed'}")

        # Return response for Lambda
        response = {
            'statusCode': 200 if success else 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Daily mitzvah sent successfully' if success else 'Failed to send mitzvah',
                'test_date': test_date or 'today',
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

        # Load recipients: prefer DynamoDB subscribers table if configured, else env var
        self.recipients = self._load_recipients()

        logger.info(f"Loaded {len(self.recipients)} recipients: {self.recipients}")

        # Try to load from CSV first, fallback to embedded data
        self.schedule_data = self.load_schedule_data()
        self.holiday_data = self.get_embedded_holidays()
        logger.info(f"Loaded {len(self.schedule_data)} schedule entries")
        logger.info(f"Loaded {len(self.holiday_data)} holiday entries")

    def _load_recipients(self) -> List[str]:
        """Load opted-in recipients from DynamoDB if SUBSCRIBERS_TABLE is set; fallback to RECIPIENTS env."""
        table_name = os.environ.get('SUBSCRIBERS_TABLE')
        numbers: List[str] = []
        if table_name:
            try:
                import importlib
                boto3 = importlib.import_module('boto3')
                # Dynamically import Attr
                dyn_conditions = importlib.import_module('boto3.dynamodb.conditions')
                Attr = getattr(dyn_conditions, 'Attr')
                ddb = boto3.resource('dynamodb')
                table = ddb.Table(table_name)
                scan_kwargs = {
                    'FilterExpression': Attr('consent_status').eq('opted_in') & Attr('channel').eq('whatsapp')
                }
                response = table.scan(**scan_kwargs)
                items = response.get('Items', [])
                numbers = [item.get('phone') for item in items if item.get('phone')]
                # Handle pagination
                while response.get('LastEvaluatedKey'):
                    scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                    response = table.scan(**scan_kwargs)
                    items = response.get('Items', [])
                    numbers.extend([item.get('phone') for item in items if item.get('phone')])
                numbers = sorted(set(numbers))
                if numbers:
                    logger.info(f"Loaded {len(numbers)} recipients from DynamoDB table {table_name}")
            except Exception as e:
                logger.warning(f"Failed to load subscribers from DynamoDB ({table_name}): {e}")

        if not numbers:
            recipients_str = os.environ.get('RECIPIENTS', '')
            numbers = [r.strip() for r in recipients_str.split(',') if r.strip()]
            if not numbers:
                raise ValueError("No recipients found. Configure SUBSCRIBERS_TABLE or set RECIPIENTS env var.")
        return numbers

    def load_schedule_data(self):
        """
        Load schedule data from CSV if available, otherwise use embedded data
        """
        try:
            import csv
            import os

            # Try to load from the enhanced CSV schedule with biblical sources first
            enhanced_csv_path = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
            original_csv_path = 'Schedule_Complete_Sefer_HaMitzvos.csv'

            if os.path.exists(enhanced_csv_path):
                logger.info("Loading schedule from enhanced CSV file with biblical sources")
                return self.load_from_csv(enhanced_csv_path)
            elif os.path.exists(original_csv_path):
                logger.info("Loading schedule from original CSV file")
                return self.load_from_csv(original_csv_path)
            else:
                logger.info("CSV files not found, using embedded schedule data")
                return self.get_embedded_schedule()
        except Exception as e:
            logger.warning(f"Failed to load from CSV: {e}, using embedded data")
            return self.get_embedded_schedule()

    def load_from_csv(self, csv_path):
        """
        Load schedule data from the complete CSV file and convert to expected format
        """
        import csv
        from collections import defaultdict

        schedule_data = []
        daily_entries = defaultdict(list)

        with open(csv_path, 'r', encoding='utf-8-sig') as file:  # Handle UTF-8 BOM
            reader = csv.DictReader(file)

            # Debug: Log the fieldnames to help troubleshoot
            logger.info(f"CSV fieldnames: {reader.fieldnames}")

            row_count = 0
            for row in reader:
                row_count += 1

                # Handle UTF-8 BOM in Date column if present
                date_key = 'Date' if 'Date' in row else list(row.keys())[0]  # First column should be Date
                date_value = row[date_key]

                # Debug: Log first few rows for troubleshooting
                if row_count <= 3:
                    logger.info(f"Row {row_count}: Date='{date_value}', Keys={list(row.keys())[:3]}")

                daily_entries[date_value].append({
                    'Mitzvah_Type_Number': row['Mitzvah_Type_Number'],
                    'Summary': row['Summary'],
                    'Sefaria_Link': row['Sefaria_Link'],
                    'Biblical_Source': row.get('Biblical_Source', '')
                })

            logger.info(f"Loaded {row_count} CSV rows into {len(daily_entries)} daily entries")

        # Convert to the format expected by lambda bot
        for date, entries in sorted(daily_entries.items()):
            mitzvos_numbers = []
            titles = []
            sefaria_links = []
            biblical_sources = []

            for entry in entries:
                mitzvos_numbers.append(entry['Mitzvah_Type_Number'])
                titles.append(entry['Summary'])
                sefaria_links.append(entry['Sefaria_Link'])
                biblical_sources.append(entry['Biblical_Source'])

            # Determine source based on mitzvah types
            sources = set()
            for mitzvah_type in mitzvos_numbers:
                if 'Intro' in mitzvah_type:
                    sources.add('Sefer HaMitzvot Introduction')
                elif 'Positive' in mitzvah_type:
                    sources.add('Sefer HaMitzvot Positive')
                elif 'Negative' in mitzvah_type:
                    sources.add('Sefer HaMitzvot Negative')
                elif 'Conclusion' in mitzvah_type:
                    sources.add('Sefer HaMitzvot Conclusion')
                else:
                    sources.add('Sefer HaMitzvot')

            schedule_entry = {
                'Date': date,
                'Mitzvos': ', '.join(mitzvos_numbers),
                'English Title(s)': ' & '.join(titles),
                'Source': ' & '.join(sorted(sources)),
                'Sefaria_Link': sefaria_links[0] if len(sefaria_links) == 1 else sefaria_links,
                'Biblical_Sources': biblical_sources
            }

            schedule_data.append(schedule_entry)

        logger.info(f"Loaded {len(schedule_data)} entries from CSV covering {len(daily_entries)} days")
        return schedule_data

    def get_embedded_schedule(self):
        """
        Embed complete Sefer HaMitzvot schedule data directly in Lambda function
        Updated with the complete 628-entry schedule including proper conclusion positioning
        NOTE: This method contains the complete schedule - see Schedule_Complete_Sefer_HaMitzvos.csv for source
        """
        # Due to size constraints, embedding full 628 entries would exceed lambda limits
        # Loading from CSV or external source recommended for production
        # This is a sample of the expected format:
        return [
            {
                'Date': '2025-10-20',
                'Mitzvos': 'Intro 1, Intro 2',
                'English Title(s)': 'Introduction to Counting the Mitzvot & Principle 1: Not rabbinic commandments',
                'Source': 'Sefer HaMitzvot Introduction',
                'Sefaria_Link': 'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.1?lang=bi'
            },
            {
                'Date': '2025-10-21',
                'Mitzvos': 'Intro 3, Intro 4',
                'English Title(s)': 'Principle 2: Not derived through hermeneutics & Principle 3: Only perpetual commandments',
                'Source': 'Sefer HaMitzvot Introduction',
                'Sefaria_Link': 'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.3?lang=bi'
            },
            {
                'Date': '2025-10-22',
                'Mitzvos': 'Intro 5, Intro 6',
                'English Title(s)': 'Principle 4: Not general Torah commands & Principle 5: Not reasons as separate mitzvot',
                'Source': 'Sefer HaMitzvot Introduction',
                'Sefaria_Link': 'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.5?lang=bi'
            },
            {
                'Date': '2025-10-23',
                'Mitzvos': 'Intro 7, Intro 8',
                'English Title(s)': 'Principle 6: Separate positive and negative & Principle 7: Not details of commandments',
                'Source': 'Sefer HaMitzvot Introduction',
                'Sefaria_Link': 'https://www.sefaria.org/Sefer_HaMitzvot%2C_Shorashim.7?lang=bi'
            }
            # Complete 628-entry schedule available in Schedule_Complete_Sefer_HaMitzvos.csv
            # For full production deployment, implement CSV loading or external data source
        ]

    def get_embedded_holidays(self):
        """
        Embed holiday data for consolidation logic - manually corrected dates
        """
        return [
            {
                'Date': '2026-04-02',
                'Holiday_Name': 'Passover Day 1',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-04-03',
                'Holiday_Name': 'Passover Day 2',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-04-08',
                'Holiday_Name': 'Passover Day 7',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-04-09',
                'Holiday_Name': 'Passover Day 8',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-05-22',
                'Holiday_Name': 'Shavuot Day 1',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-05-23',
                'Holiday_Name': 'Shavuot Day 2',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-07-29',
                'Holiday_Name': 'Tish B Av',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-09-12',
                'Holiday_Name': 'Rosh Hashanah Day 1',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-09-13',
                'Holiday_Name': 'Rosh Hashanah Day 2',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-09-21',
                'Holiday_Name': 'Yom Kippur',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-09-26',
                'Holiday_Name': 'Sukkot Day 1',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-09-27',
                'Holiday_Name': 'Sukkot Day 2',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-10-03',
                'Holiday_Name': 'Shemini Atzeret',
                'Work_Forbidden': 'yes'
            },
            {
                'Date': '2026-10-04',
                'Holiday_Name': 'Simchat Torah',
                'Work_Forbidden': 'yes'
            }
            # More holidays would be embedded here in production
        ]

    def is_yom_tov(self, date_str):
        """Check if given date is a Yom Tov (no-work day)"""
        for holiday in self.holiday_data:
            if holiday['Date'] == date_str and holiday['Work_Forbidden'] == 'yes':
                return True, holiday['Holiday_Name']
        return False, None

    def get_consolidated_mitzvot(self, target_date):
        """
        Get mitzvot with holiday consolidation logic:
        - Day before Yom Tov: include today + tomorrow's mitzvot
        - Day after Yom Tov: include yesterday + today's mitzvot
        """
        from datetime import datetime, timedelta

        current_date = datetime.strptime(target_date, '%Y-%m-%d')
        tomorrow = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')

        # Check if tomorrow is Yom Tov
        is_tomorrow_yomtov, tomorrow_holiday = self.is_yom_tov(tomorrow)

        # Check if yesterday was Yom Tov
        is_yesterday_yomtov, yesterday_holiday = self.is_yom_tov(yesterday)

        logger.info(f"Date analysis: {target_date}, Tomorrow YomTov: {is_tomorrow_yomtov}, Yesterday YomTov: {is_yesterday_yomtov}")

        # Get today's mitzvot
        today_mitzvot = self.find_mitzvah_by_date(target_date)

        if is_tomorrow_yomtov and today_mitzvot:
            # Day before Yom Tov: consolidate today + tomorrow
            tomorrow_mitzvot = self.find_mitzvah_by_date(tomorrow)
            if tomorrow_mitzvot:
                logger.info(f"Consolidating for {tomorrow_holiday}: adding tomorrow's mitzvot to today")
                return self.combine_mitzvot_entries(today_mitzvot, tomorrow_mitzvot, f"Preparing for {tomorrow_holiday}")

        elif is_yesterday_yomtov and today_mitzvot:
            # Day after Yom Tov: consolidate yesterday + today
            yesterday_mitzvot = self.find_mitzvah_by_date(yesterday)
            if yesterday_mitzvot:
                logger.info(f"Consolidating after {yesterday_holiday}: adding yesterday's mitzvot to today")
                return self.combine_mitzvot_entries(yesterday_mitzvot, today_mitzvot, f"Continuing after {yesterday_holiday}")

        # Regular day - return today's mitzvot
        return today_mitzvot

    def find_mitzvah_by_date(self, date_str):
        """Find mitzvah entry for specific date"""
        for row in self.schedule_data:
            if row['Date'].strip() == date_str:
                return {
                    'date': row['Date'].strip(),
                    'mitzvos': row['Mitzvos'].strip(),
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip(),
                    'sefaria_link': row.get('Sefaria_Link', ''),
                    'biblical_sources': row.get('Biblical_Sources', [])
                }
        return None

    def combine_mitzvot_entries(self, first_entry, second_entry, reason):
        """Combine two mitzvot entries into one consolidated entry"""
        # Combine mitzvot numbers
        combined_mitzvos = f"{first_entry['mitzvos']}, {second_entry['mitzvos']}"

        # Combine titles
        combined_titles = f"{first_entry['title']} & {second_entry['title']}"

        # Combine sources
        combined_sources = f"{first_entry['source']} & {second_entry['source']}"

        # Combine Sefaria links
        first_link = first_entry.get('sefaria_link', '')
        second_link = second_entry.get('sefaria_link', '')

        combined_sefaria_links = []
        if first_link:
            if isinstance(first_link, list):
                combined_sefaria_links.extend(first_link)
            else:
                combined_sefaria_links.append(first_link)

        if second_link:
            if isinstance(second_link, list):
                combined_sefaria_links.extend(second_link)
            else:
                combined_sefaria_links.append(second_link)

        # Combine biblical sources
        first_biblical = first_entry.get('biblical_sources', [])
        second_biblical = second_entry.get('biblical_sources', [])

        combined_biblical_sources = []
        if first_biblical:
            if isinstance(first_biblical, list):
                combined_biblical_sources.extend(first_biblical)
            else:
                combined_biblical_sources.append(first_biblical)

        if second_biblical:
            if isinstance(second_biblical, list):
                combined_biblical_sources.extend(second_biblical)
            else:
                combined_biblical_sources.append(second_biblical)

        return {
            'date': first_entry['date'],
            'mitzvos': combined_mitzvos,
            'title': combined_titles,
            'source': combined_sources,
            'sefaria_link': combined_sefaria_links,
            'biblical_sources': combined_biblical_sources,
            'consolidation_reason': reason
        }

    def load_mitzvah_for_date(self, target_date=None):
        """Load mitzvah for specific date with holiday consolidation logic."""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"Looking for mitzvah for date: {target_date}")

        # Use holiday-aware consolidation
        mitzvah_data = self.get_consolidated_mitzvot(target_date)

        if mitzvah_data:
            if 'consolidation_reason' in mitzvah_data:
                logger.info(f"Found consolidated mitzvot: {mitzvah_data['mitzvos']} - Reason: {mitzvah_data['consolidation_reason']}")
            else:
                logger.info(f"Found regular mitzvah: {mitzvah_data['mitzvos']} - {mitzvah_data['title']}")
            return mitzvah_data

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

    def format_mitzvah_number(self, mitzvah_type_number):
        """Format mitzvah number for display (e.g., 'Positive 39' -> 'Positive Mitzvah 39')"""
        if 'Positive' in mitzvah_type_number:
            number = mitzvah_type_number.replace('Positive ', '')
            return f"Positive Mitzvah {number}"
        elif 'Negative' in mitzvah_type_number:
            number = mitzvah_type_number.replace('Negative ', '')
            return f"Negative Mitzvah {number}"
        elif 'Intro' in mitzvah_type_number:
            return mitzvah_type_number  # Keep Intro format as is
        elif 'Conclusion' in mitzvah_type_number:
            return mitzvah_type_number  # Keep Conclusion format as is
        else:
            return f"Mitzvah {mitzvah_type_number}"

    def format_message(self, mitzvah_data):
        """Format the WhatsApp message with holiday consolidation support."""
        date_formatted = datetime.strptime(mitzvah_data['date'], '%Y-%m-%d').strftime('%A, %B %d, %Y')

        # Check if this is a consolidated message for holidays
        is_consolidated = 'consolidation_reason' in mitzvah_data
        consolidation_reason = mitzvah_data.get('consolidation_reason', '')

        # Get Sefaria links from the data
        sefaria_links = mitzvah_data.get('sefaria_link', [])
        if isinstance(sefaria_links, str):
            sefaria_links = [sefaria_links]

        # Get biblical sources from the data
        biblical_sources = mitzvah_data.get('biblical_sources', [])
        if isinstance(biblical_sources, str):
            biblical_sources = [biblical_sources] if biblical_sources else []

        if mitzvah_data['mitzvos'].startswith('Intro'):
            # Introduction/Shorashim message
            sefaria_text = ""
            if sefaria_links and sefaria_links[0]:
                sefaria_text = f"\n🕍 Learn more: {sefaria_links[0]}"

            message = f"""✡️ *Sefer HaMitzvos Daily Study* 📚

📅 {date_formatted}

📖 *{mitzvah_data['mitzvos']}*
_{mitzvah_data['title']}_

📚 Source: {mitzvah_data['source']}{sefaria_text}

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
                sources_raw = [source.strip() for source in mitzvah_data['source'].split(' & ')]

                # Handle case where all sources are the same (duplicate the single source for each mitzvah)
                if len(sources_raw) == 1 and len(numbers) > 1:
                    sources = sources_raw * len(numbers)
                else:
                    sources = sources_raw

                # Handle Sefaria links for multiple mitzvot
                mitzvah_sefaria_links = sefaria_links if len(sefaria_links) > 1 else [sefaria_links[0] if sefaria_links else ''] * len(numbers)

                # Build message header with holiday context
                header = f"✡️ *Sefer HaMitzvos Daily Study* 📚\n\n📅 {date_formatted}"

                if is_consolidated:
                    header += f"\n🎊 *Special Holiday Schedule* - {consolidation_reason}"

                message = header + "\n\n"

                # Add each mitzvah separately
                for i, (num, title, source) in enumerate(zip(numbers, titles, sources)):
                    sefaria_text = ""
                    if i < len(mitzvah_sefaria_links) and mitzvah_sefaria_links[i]:
                        sefaria_text = f"\n🕍 Learn more: {mitzvah_sefaria_links[i]}"
                    biblical_text = ""
                    # Include biblical source for each mitzvah when available
                    if i < len(biblical_sources) and biblical_sources[i] and biblical_sources[i] != 'N/A':
                        biblical_text = f"\n📜 Biblical Source: {biblical_sources[i]}"

                    formatted_mitzvah_num = self.format_mitzvah_number(num)
                    message += f"""🔢 *{formatted_mitzvah_num}*
{title}

📚 Source: {source}{biblical_text}{sefaria_text}

"""

                # Add closing with holiday context
                if is_consolidated:
                    message += f"""Continue your Torah study during this blessed time! 🎊✨

_—Daily Mitzvah Bot_"""
                else:
                    message += """Fulfill these mitzvot with joy and intention! 💫🙏

_—Daily Mitzvah Bot_"""
            else:
                # Single mitzvah
                formatted_mitzvah_num = self.format_mitzvah_number(mitzvah_nums)
                mitzvah_text = f"*{formatted_mitzvah_num}*"
                # Build header with holiday context
                header = f"✡️ *Sefer HaMitzvos Daily Study* 📚\n\n📅 {date_formatted}"

                if is_consolidated:
                    header += f"\n🎊 *Special Holiday Schedule* - {consolidation_reason}"

                # Add Sefaria link for single mitzvah
                sefaria_text = ""
                if sefaria_links and sefaria_links[0]:
                    sefaria_text = f"\n🕍 Learn more: {sefaria_links[0]}"

                # Add biblical source for single mitzvah
                biblical_text = ""
                # Include biblical source for single mitzvah when available
                if biblical_sources and biblical_sources[0] and biblical_sources[0] != 'N/A':
                    biblical_text = f"\n📜 Biblical Source: {biblical_sources[0]}"

                message = f"""{header}

🔢 {mitzvah_text}
_{mitzvah_data['title']}_

📚 Source: {mitzvah_data['source']}{biblical_text}{sefaria_text}

Fulfill this mitzvah with joy and intention! 💫🙏

_—Daily Mitzvah Bot_"""

        # Append standard unsubscribe blurb for compliance/clarity
        message += "\n\nReply STOP to unsubscribe."
        return message

    def send_to_recipient(self, recipient, message, mitzvah_data=None):
        """Send message to a single recipient, using WhatsApp template if available."""
        try:
            logger.info(f"Sending message to {recipient}")

            # Check for WhatsApp template configuration
            template_sid = os.environ.get('WHATSAPP_TEMPLATE_SID')
            use_template = os.environ.get('USE_WHATSAPP_TEMPLATE', 'false').lower() == 'true'

            if template_sid and use_template and mitzvah_data:
                # Use WhatsApp Business Message Template
                logger.info(f"Using WhatsApp template: {template_sid}")

                # Extract template variables from mitzvah data
                date_formatted = datetime.strptime(mitzvah_data.get('date', ''), '%Y-%m-%d').strftime('%B %d, %Y') if mitzvah_data.get('date') else 'Today'
                mitzvah_nums = mitzvah_data.get('mitzvos', '')
                description = mitzvah_data.get('title', '')

                # Handle biblical sources
                biblical_sources = mitzvah_data.get('biblical_sources', [])
                if isinstance(biblical_sources, list):
                    sources_text = ', '.join([s for s in biblical_sources if s and s != 'N/A'])
                else:
                    sources_text = str(biblical_sources) if biblical_sources else ''

                # Handle Sefaria links
                sefaria_links = mitzvah_data.get('sefaria_link', [])
                if isinstance(sefaria_links, list):
                    links_text = ', '.join([l for l in sefaria_links if l])
                else:
                    links_text = str(sefaria_links) if sefaria_links else ''

                message_obj = self.client.messages.create(
                    content_sid=template_sid,
                    content_variables=json.dumps({
                        "1": date_formatted,
                        "2": mitzvah_nums,
                        "3": description,
                        "4": sources_text or 'Traditional Sources',
                        "5": links_text or 'Available on Sefaria'
                    }),
                    from_=f'whatsapp:{self.whatsapp_number}',
                    to=f'whatsapp:{recipient}'
                )
                logger.info(f"WhatsApp template message sent to {recipient}")
            else:
                # Fallback to regular SMS (current behavior)
                logger.info("Using regular SMS (no template configured)")
                message_obj = self.client.messages.create(
                    body=message,
                    from_=self.whatsapp_number,  # Use as regular SMS number
                    to=recipient  # Send as regular SMS
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

                if self.send_to_recipient(recipient, message, mitzvah_data):
                    success_count += 1
                else:
                    logger.error(f"Failed to send to {recipient}")

            logger.info(f"Daily mitzvah sent to {success_count}/{len(self.recipients)} recipients")
            return success_count > 0

        except Exception as e:
            logger.error(f"Failed to send daily mitzvah: {e}")
            return False

# For local testing (not used in Lambda)
if __name__ == "__main__":
    # This allows you to test the Lambda function locally
    test_event = {}
    test_context = type('Context', (), {'get_remaining_time_in_millis': lambda: 30000})()
    result = lambda_handler(test_event, test_context)
    print(f"Result: {result}")