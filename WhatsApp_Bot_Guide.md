# WhatsApp Bot for Daily Mitzvah Updates

## Overview

This guide shows how to create a WhatsApp bot that sends daily mitzvah updates based on your Schedule_Corrected.csv file.

## Method 1: Using WhatsApp Business API (Recommended)

### Prerequisites

- WhatsApp Business Account
- Meta Developer Account
- Phone number for business verification

### Setup Steps

1. **Register with Meta for WhatsApp Business API**

   - Visit: https://developers.facebook.com/docs/whatsapp
   - Create a Meta Developer account
   - Set up WhatsApp Business API

2. **Get API Credentials**
   - Phone Number ID
   - Access Token
   - WhatsApp Business Account ID

### Python Implementation

```python
# whatsapp_mitzvah_bot.py
import csv
import requests
import json
from datetime import datetime, timedelta
import schedule
import time
import os
from typing import List, Dict, Optional

class WhatsAppMitzvahBot:
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def load_schedule(self, csv_file: str) -> Dict[str, Dict]:
        """Load the mitzvah schedule from CSV file."""
        schedule_dict = {}
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row['Date'].strip()
                schedule_dict[date] = {
                    'mitzvos': row['Mitzvos'].strip(),
                    'title': row['English Title(s)'].strip(),
                    'source': row['Source'].strip()
                }
        return schedule_dict

    def get_today_mitzvah(self, schedule_dict: Dict) -> Optional[Dict]:
        """Get today's mitzvah from the schedule."""
        today = datetime.now().strftime('%Y-%m-%d')
        return schedule_dict.get(today)

    def format_message(self, mitzvah_data: Dict) -> str:
        """Format the daily mitzvah message."""
        if mitzvah_data['mitzvos'].startswith('Intro'):
            message = f"""🕊️ *Daily Mitzvah Study* 🕊️
📅 {datetime.now().strftime('%B %d, %Y')}

📖 *{mitzvah_data['mitzvos']}*
{mitzvah_data['title']}

📚 Source: {mitzvah_data['source']}

_May your study be blessed! 🙏_"""
        else:
            message = f"""🕊️ *Daily Mitzvah Study* 🕊️
📅 {datetime.now().strftime('%B %d, %Y')}

🔢 *Mitzvah #{mitzvah_data['mitzvos']}*
{mitzvah_data['title']}

📚 Source: {mitzvah_data['source']}

_Fulfill this mitzvah with joy! ✨_"""
        return message

    def send_message(self, recipient_number: str, message: str) -> bool:
        """Send a WhatsApp message to a recipient."""
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {"body": message}
        }

        try:
            response = requests.post(self.base_url,
                                   headers=self.headers,
                                   data=json.dumps(payload))
            response.raise_for_status()
            print(f"Message sent successfully to {recipient_number}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            return False

    def send_daily_update(self, recipients: List[str], csv_file: str):
        """Send daily mitzvah update to all recipients."""
        schedule_dict = self.load_schedule(csv_file)
        today_mitzvah = self.get_today_mitzvah(schedule_dict)

        if not today_mitzvah:
            print("No mitzvah scheduled for today")
            return

        message = self.format_message(today_mitzvah)

        for recipient in recipients:
            self.send_message(recipient, message)
            time.sleep(1)  # Rate limiting

# Usage Example
if __name__ == "__main__":
    # Configuration
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
    PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID_HERE"

    # Recipients (phone numbers in international format)
    RECIPIENTS = [
        "+1234567890",  # Replace with actual numbers
        "+9876543210"
    ]

    # Initialize bot
    bot = WhatsAppMitzvahBot(ACCESS_TOKEN, PHONE_NUMBER_ID)

    # Schedule daily messages
    schedule.every().day.at("08:00").do(
        bot.send_daily_update,
        RECIPIENTS,
        "Schedule_Corrected.csv"
    )

    print("WhatsApp Mitzvah Bot started...")
    print("Daily messages scheduled for 8:00 AM")

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Method 2: Using Twilio WhatsApp API (Easier Setup)

### Setup Steps

1. **Create Twilio Account**

   - Visit: https://www.twilio.com/whatsapp
   - Get Account SID, Auth Token, and WhatsApp number

2. **Python Implementation with Twilio**

```python
# twilio_whatsapp_bot.py
from twilio.rest import Client
import csv
from datetime import datetime
import schedule
import time

class TwilioWhatsAppBot:
    def __init__(self, account_sid: str, auth_token: str, whatsapp_number: str):
        self.client = Client(account_sid, auth_token)
        self.whatsapp_number = whatsapp_number

    def send_daily_mitzvah(self, recipients: list, csv_file: str):
        # Load today's mitzvah
        today = datetime.now().strftime('%Y-%m-%d')

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Date'].strip() == today:
                    message = f"""🕊️ Daily Mitzvah Study 🕊️
📅 {datetime.now().strftime('%B %d, %Y')}

🔢 Mitzvah #{row['Mitzvos']}
{row['English Title(s)']}

📚 {row['Source']}

May your study bring you closer to Hashem! 🙏"""

                    for recipient in recipients:
                        try:
                            self.client.messages.create(
                                body=message,
                                from_=f'whatsapp:{self.whatsapp_number}',
                                to=f'whatsapp:{recipient}'
                            )
                            print(f"Sent to {recipient}")
                        except Exception as e:
                            print(f"Error sending to {recipient}: {e}")
                    break

# Configuration
ACCOUNT_SID = 'your_twilio_account_sid'
AUTH_TOKEN = 'your_twilio_auth_token'
WHATSAPP_NUMBER = '+14155238886'  # Twilio WhatsApp sandbox number

bot = TwilioWhatsAppBot(ACCOUNT_SID, AUTH_TOKEN, WHATSAPP_NUMBER)

# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(
    bot.send_daily_mitzvah,
    ['+1234567890'],  # Your phone numbers
    'Schedule_Corrected.csv'
)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Method 3: Simple WhatsApp Web Automation (No API needed)

```python
# whatsapp_web_bot.py
import csv
from datetime import datetime
import pywhatkit as kit
import time

def send_daily_mitzvah():
    today = datetime.now().strftime('%Y-%m-%d')

    # Load today's mitzvah
    with open('Schedule_Corrected.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Date'].strip() == today:
                message = f"""🕊️ Daily Mitzvah Study 🕊️

📅 {datetime.now().strftime('%B %d, %Y')}
🔢 Mitzvah #{row['Mitzvos']}

{row['English Title(s)']}

📚 Source: {row['Source']}

_B'hatzlacha in your studies! 📖✨_"""

                # Send to phone numbers
                phone_numbers = ["+1234567890", "+9876543210"]  # Add your numbers

                current_time = datetime.now()
                send_hour = current_time.hour
                send_minute = current_time.minute + 2  # Send in 2 minutes

                for phone in phone_numbers:
                    kit.sendwhatmsg(phone, message, send_hour, send_minute)
                    time.sleep(10)  # Wait between sends
                break

# Run daily
send_daily_mitzvah()
```

## Installation Requirements

```bash
# For WhatsApp Business API method
pip install requests schedule

# For Twilio method
pip install twilio schedule

# For WhatsApp Web automation
pip install pywhatkit schedule
```

## Deployment Options

### 1. **Local Computer (Simplest)**

- Run the script on your computer
- Keep it running 24/7
- Use Task Scheduler (Windows) or cron (Mac/Linux)

### 2. **Cloud Service (Recommended)**

- **Heroku**: Free tier available
- **AWS Lambda**: Serverless, cost-effective
- **Google Cloud Functions**: Pay per use
- **DigitalOcean**: $5/month droplet

### 3. **Raspberry Pi (Budget Option)**

- One-time $35 cost
- Runs 24/7 at home
- Perfect for personal use

## Configuration File Setup

```python
# config.py
import os

# WhatsApp Business API Configuration
WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Recipients
RECIPIENTS = [
    "+1234567890",  # Add your phone numbers here
    "+9876543210"
]

# Schedule
SEND_TIME = "08:00"  # 8:00 AM daily
CSV_FILE = "Schedule_Corrected.csv"
```

## Security Best Practices

1. **Use Environment Variables** for API keys
2. **Never commit credentials** to version control
3. **Validate phone numbers** before sending
4. **Implement rate limiting** to avoid API limits
5. **Add error handling** and logging

## Next Steps

1. **Choose your preferred method** (I recommend Twilio for ease of use)
2. **Set up the API credentials**
3. **Test with your phone number first**
4. **Deploy to a cloud service** for reliability
5. **Add your recipients** to the list

Would you like me to help you implement any specific method or need help with the deployment?
