#!/usr/bin/env python3
"""
Personal WhatsApp Setup Helper
This script helps you configure your personal phone number for the WhatsApp bot.
"""

print("""
📱 Setting up Personal WhatsApp Bot

Before we start, you need to update your phone number in the bot.

1. Open: bots/whatsapp_web_group_bot.py
2. Find line with: "+1234567890"
3. Replace with your actual phone number in international format

Examples:
- US number (555) 123-4567 → "+15551234567"
- UK number 07700 900123 → "+447700900123"
- Israel number 050-123-4567 → "+972501234567"

Format: +[country code][phone number without leading zeros]

❗ Important Notes:
- Include the + sign
- Include country code
- Remove any spaces, dashes, or parentheses
- Remove leading zeros from the phone number part

Ready to test? Press Enter when you've updated your number...
""")

input()

print("""
🧪 Testing Personal WhatsApp Bot

The bot will:
1. Open your default browser
2. Navigate to WhatsApp Web
3. Wait 15 seconds for you to scan QR code (if needed)
4. Send today's mitzvah to your phone

Make sure:
✅ You have WhatsApp installed on your phone
✅ Your phone has internet connection
✅ You're ready to scan QR code if needed

Starting test in 3 seconds...
""")

import time
time.sleep(3)

import os
import subprocess

# Set test environment
os.environ['BOT_MODE'] = 'test'
os.environ['SEND_DEPLOY_NOTIFICATIONS'] = 'false'

# Run the bot
try:
    result = subprocess.run(['python', 'bots/whatsapp_web_group_bot.py'],
                          capture_output=True, text=True)

    print("Bot output:")
    print(result.stdout)

    if result.stderr:
        print("Errors:")
        print(result.stderr)

except Exception as e:
    print(f"Error running bot: {e}")

print("""
🔍 What to check:

1. Did your browser open automatically?
2. Did you see WhatsApp Web load?
3. If you weren't logged in, did you scan the QR code?
4. Did you receive a message on your phone?

If you didn't receive the message:
- Check if you entered your phone number correctly
- Make sure you're logged into WhatsApp Web
- Try running the test again

Next steps:
- If it worked: Set BOT_MODE=scheduler for daily messages
- If it didn't work: Double-check your phone number format
""")