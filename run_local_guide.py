#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Twilio Bot Runner
Instructions for running the bot on your local computer 24/7
"""

print("🏠 Running Twilio Bot Locally (No Railway Needed)")
print()
print("✅ ADVANTAGES:")
print("- Free (no hosting costs)")
print("- Full control over when it runs")
print("- Easy to test and debug")
print("- Works with your existing Twilio sandbox")
print()
print("❌ DISADVANTAGES:")
print("- Your computer must stay on 24/7")
print("- Bot stops if computer sleeps/restarts")
print("- Uses your internet connection")
print()
print("📋 SETUP INSTRUCTIONS:")
print()
print("1. Make sure your .env file has Twilio credentials:")
print("   TWILIO_ACCOUNT_SID=your_account_sid")
print("   TWILIO_AUTH_TOKEN=your_auth_token")
print("   RECIPIENTS=+16613059259")
print("   BOT_MODE=scheduler")
print("   TZ=America/Chicago")
print()
print("2. Run the bot:")
print("   python bots/mitzvah_bot_cloud.py")
print()
print("3. Keep your computer running - the bot will send daily at 1:10 PM CST")

# Show current bot status
import os
from datetime import datetime

print("🔍 CURRENT CONFIGURATION:")
env_file_exists = os.path.exists('.env')
print(f"   .env file: {'✅ Found' if env_file_exists else '❌ Missing'}")

if env_file_exists:
    # Check if required variables are set
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            has_sid = 'TWILIO_ACCOUNT_SID' in env_content
            has_token = 'TWILIO_AUTH_TOKEN' in env_content
            has_recipients = 'RECIPIENTS' in env_content

            print(f"   Twilio SID: {'✅ Set' if has_sid else '❌ Missing'}")
            print(f"   Twilio Token: {'✅ Set' if has_token else '❌ Missing'}")
            print(f"   Recipients: {'✅ Set' if has_recipients else '❌ Missing'}")

    except Exception as e:
        print(f"   Error reading .env: {e}")

print(f"\n⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
print("   Next scheduled run: Daily at 1:10 PM CST")

print("""
🚀 READY TO RUN?
Just execute: python bots/mitzvah_bot_cloud.py

The bot will:
1. Start immediately
2. Wait until 1:10 PM CST
3. Send daily mitzvah message
4. Wait until next day's 1:10 PM
5. Repeat forever (until you stop it)
""")