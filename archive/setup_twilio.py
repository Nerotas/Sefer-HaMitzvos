#!/usr/bin/env python3
"""
Twilio WhatsApp Setup Guide
Step-by-step instructions to get your Twilio WhatsApp bot working
"""

print("""
🔧 Twilio WhatsApp Setup Guide

📋 STEP 1: Create Twilio Account
1. Go to: https://www.twilio.com/
2. Sign up for a free account
3. Verify your phone number

📋 STEP 2: Get Your Credentials
1. Go to Twilio Console: https://console.twilio.com/
2. Find your Account SID and Auth Token
3. Copy both values (we'll need them)

📋 STEP 3: Set Up WhatsApp Sandbox
1. In Twilio Console, go to: Messaging > Try it out > Send a WhatsApp message
2. You'll see a sandbox number like: +1 415 523 8886
3. Send the sandbox code from your phone to that number
   Example: Send "join <your-code>" to +14155238886

📋 STEP 4: Configure Environment Variables
We'll create a .env file with your credentials:

TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
RECIPIENTS=+16613059259

📋 STEP 5: Test the Bot
We'll run the Twilio bot instead of the WhatsApp Web bot

Ready to start? (y/n): """, end="")

response = input().lower()

if response == 'y':
    print("""
💾 Let's create your .env file step by step:

1. What is your Twilio Account SID?
   (Starts with 'AC' - found in Twilio Console)
""")

    account_sid = input("Account SID: ").strip()

    print("""
2. What is your Twilio Auth Token?
   (Found in Twilio Console, might be hidden - click to reveal)
""")

    auth_token = input("Auth Token: ").strip()

    print(f"""
3. Your phone number: +16613059259
   Is this correct? (y/n): """, end="")

    phone_correct = input().lower()
    if phone_correct != 'y':
        phone = input("Enter your correct phone number (with +1): ").strip()
    else:
        phone = "+16613059259"

    # Create .env file
    env_content = f"""# Twilio WhatsApp Bot Configuration
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_WHATSAPP_NUMBER=+14155238886
RECIPIENTS={phone}
BOT_MODE=test
SEND_DEPLOY_NOTIFICATIONS=false
"""

    try:
        with open('.env', 'w') as f:
            f.write(env_content)

        print(f"""
✅ .env file created successfully!

📱 IMPORTANT: Before testing, you must:
1. Send this message from your phone ({phone}) to +14155238886:
   "join <your-sandbox-code>"

2. Wait for confirmation from Twilio

3. Then run the test

🧪 Ready to test the Twilio bot? (y/n): """, end="")

        test_response = input().lower()
        if test_response == 'y':
            print("\n🚀 Testing Twilio bot...\n")
            import subprocess
            import os

            # Load environment variables
            if os.path.exists('.env'):
                from dotenv import load_dotenv
                load_dotenv()

            try:
                result = subprocess.run(['python', 'bots/mitzvah_bot_cloud.py'],
                                      capture_output=True, text=True)

                print("Bot output:")
                print(result.stdout)

                if result.stderr:
                    print("Errors:")
                    print(result.stderr)

            except Exception as e:
                print(f"Error running bot: {e}")
                print("\nTry running manually: python bots/mitzvah_bot_cloud.py")

    except Exception as e:
        print(f"Error creating .env file: {e}")

else:
    print("""
📖 Manual Setup Instructions:

1. Create Twilio account: https://www.twilio.com/
2. Get credentials from: https://console.twilio.com/
3. Set up WhatsApp sandbox: Messaging > Try it out > Send a WhatsApp message
4. Create .env file with your credentials
5. Test with: python bots/mitzvah_bot_cloud.py

The .env file should contain:
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
RECIPIENTS=+16613059259
""")