#!/usr/bin/env python3
"""
Bot Scheduling Visualization
Shows exactly how the scheduling works
"""

import schedule
import time
from datetime import datetime, timedelta

print("🤖 Bot Scheduling Process Visualization")
print("=" * 50)

# Simulate what the bot does
def mock_send_message():
    print(f"📨 MESSAGE SENT at {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    return "Message sent successfully!"

# Set up the same schedule as the bot
schedule.every().day.at("13:00").do(mock_send_message)

print("✅ Schedule created: Daily message at 13:00 (1:00 PM)")
print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Show next scheduled run
next_run = schedule.next_run()
print(f"📅 Next scheduled run: {next_run}")

# Calculate time until next run
now = datetime.now()
time_until = next_run - now
hours = int(time_until.total_seconds() // 3600)
minutes = int((time_until.total_seconds() % 3600) // 60)
print(f"⏳ Time until next message: {hours} hours, {minutes} minutes")

print("\n🔄 Bot Process (what happens on Railway):")
print("1. Railway starts: python bots/whatsapp_web_group_bot.py")
print("2. Bot reads BOT_MODE=scheduler")
print("3. Bot calls run_scheduler()")
print("4. Bot creates schedule: every day at 13:00")
print("5. Bot enters infinite loop:")
print("   while True:")
print("       schedule.run_pending()  # Check if it's 1:00 PM")
print("       time.sleep(60)          # Wait 1 minute")
print("6. At 1:00 PM CST: send_daily_mitzvah() is called")
print("7. Message is sent via WhatsApp Web")
print("8. Bot continues loop, waiting for next day")

print(f"\n📊 Schedule Status:")
print(f"   Jobs in queue: {len(schedule.get_jobs())}")
for job in schedule.get_jobs():
    print(f"   - {job}")

print("\n🌐 On Railway:")
print("- Railway keeps the bot running 24/7")
print("- Bot automatically handles the scheduling")
print("- No manual intervention needed")
print("- Timezone: America/Chicago (set via TZ environment variable)")