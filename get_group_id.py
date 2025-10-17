#!/usr/bin/env python3
"""
WhatsApp Group ID Finder
This script helps you find the correct group ID for your WhatsApp group.
"""

print("""
🔍 How to get your WhatsApp Group ID:

Method 1 - From Browser Console:
1. Open WhatsApp Web (web.whatsapp.com) in your browser
2. Open the group chat you want to send messages to
3. Press F12 to open Developer Tools
4. Go to the Console tab
5. Type: Store.Chat.getActive().id._serialized
6. Press Enter
7. Copy the ID (something like: "1234567890-1234567890@g.us")

Method 2 - From Invite Link:
Your current group ID: "JpwWqLb9Dv0K8KUQsX3KcO"
This looks like it's from an invite link, but you need the actual chat ID.

Method 3 - Test with a Simple Message:
If you're not sure, try sending to your own phone number first:
1. Replace group_id with your phone number (format: "+1234567890")
2. Use send_to_individuals() instead of send_to_group()

🔧 Current Configuration Check:
""")

import csv
from datetime import datetime

# Check if CSV file exists and has data
try:
    with open('Schedule_Corrected.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        today = datetime.now().strftime('%Y-%m-%d')

        for row in reader:
            if row['Date'].strip() == today:
                print(f"✅ Today's mitzvah found: {row['Mitzvos']} - {row['English Title(s)']}")
                break
        else:
            print(f"❌ No mitzvah found for today ({today})")

except Exception as e:
    print(f"❌ Error reading CSV: {e}")

print(f"""
🕐 Last run time: The bot scheduled a message for 11:52
   Did your browser open WhatsApp Web at that time?
   Were you logged into WhatsApp Web?

💡 Troubleshooting Tips:
1. Make sure you're logged into WhatsApp Web
2. Use the correct group ID from the browser console
3. Test with your own phone number first
4. Check if Chrome/your default browser opened automatically

""")