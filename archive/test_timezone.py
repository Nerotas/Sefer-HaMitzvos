#!/usr/bin/env python3
"""
Timezone Test for Railway Deployment
Tests that the bot correctly uses CST timezone
"""

import os
import time
from datetime import datetime

print("🕐 Timezone Configuration Test")
print("=" * 40)

# Check environment variables
tz_env = os.getenv('TZ')
print(f"TZ environment variable: {tz_env or 'Not set'}")

# Set timezone if specified
if tz_env:
    os.environ['TZ'] = tz_env
    if hasattr(time, 'tzset'):
        time.tzset()
        print(f"✅ Timezone set to: {tz_env}")
    else:
        print("⚠️  tzset() not available (Windows - timezone may not change)")

# Show current time information
current_time = datetime.now()
print(f"\nCurrent time: {current_time}")
print(f"Timezone names: {time.tzname}")
print(f"DST active: {bool(time.daylight)}")

# Show what 1:00 PM looks like
scheduled_time = current_time.replace(hour=13, minute=0, second=0, microsecond=0)
print(f"\n📅 Scheduled delivery time (1:00 PM): {scheduled_time}")

# Calculate next 1:00 PM
if current_time.hour >= 13:
    # If it's already past 1 PM today, show tomorrow's 1 PM
    from datetime import timedelta
    next_delivery = scheduled_time + timedelta(days=1)
    print(f"⏰ Next delivery: {next_delivery} (tomorrow)")
else:
    # If it's before 1 PM today, show today's 1 PM
    print(f"⏰ Next delivery: {scheduled_time} (today)")

print("\n" + "=" * 40)
print("For Railway deployment:")
print("1. Set TZ=America/Chicago in environment variables")
print("2. Bot will automatically use Central Time")
print("3. Messages will be sent at 1:00 PM CST/CDT daily")