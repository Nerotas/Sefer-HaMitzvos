#!/bin/bash
echo "🕊️ Mitzvah WhatsApp Bot Installer 📱"
echo

echo "Installing required packages..."
pip3 install -r requirements.txt

echo
echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your Twilio credentials to .env"
echo "3. Edit mitzvah_whatsapp_bot.py to add recipient phone numbers"
echo "4. Run: python3 mitzvah_whatsapp_bot.py"
echo