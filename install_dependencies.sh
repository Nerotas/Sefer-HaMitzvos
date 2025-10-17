#!/bin/bash
echo "🔧 Installing Dependencies for Mitzvah Bots..."
echo

echo "Installing Python packages..."
pip install twilio==8.10.0
pip install python-dotenv==1.0.0
pip install pywhatkit==5.4
pip install python-telegram-bot==20.6
pip install schedule==1.2.0

echo
echo "✅ All dependencies installed successfully!"
echo
echo "📋 Available bots:"
echo "  - mitzvah_bot_cloud.py (Twilio WhatsApp - Recommended)"
echo "  - whatsapp_web_group_bot.py (WhatsApp Web - Free)"
echo "  - telegram_mitzvah_bot.py (Telegram - Free & Reliable)"
echo
echo "🚀 Ready to deploy to Railway!"