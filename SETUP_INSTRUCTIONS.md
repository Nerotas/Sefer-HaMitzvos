# WhatsApp Mitzvah Bot Setup Instructions

## Quick Start Guide

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Twilio WhatsApp API (Easiest Method)

#### A. Create Twilio Account

1. Go to [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
2. Sign up for a free account
3. Verify your phone number

#### B. Get API Credentials

1. Go to [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token**
3. Go to WhatsApp Sandbox settings
4. Note your **WhatsApp number** (usually +14155238886)

#### C. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your Twilio credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Configure Recipients

Edit `mitzvah_whatsapp_bot.py` and add phone numbers to the recipients list:

```python
self.recipients = [
    '+12345678900',  # Replace with actual numbers
    '+19876543210'   # International format required
]
```

### 4. Test the Bot

```bash
python mitzvah_whatsapp_bot.py
```

Select option 1 to send a test message.

### 5. Run Daily Schedule

```bash
python mitzvah_whatsapp_bot.py
```

Select option 2 to start the daily scheduler.

## Deployment Options

### Option 1: Local Computer (Simplest)

- Keep your computer running
- Run the script daily
- Use Windows Task Scheduler or macOS/Linux cron

### Option 2: Cloud Deployment (Recommended)

#### Heroku (Free Tier)

```bash
# Install Heroku CLI
# Create Procfile:
echo "worker: python mitzvah_whatsapp_bot.py" > Procfile

# Deploy
heroku create your-mitzvah-bot
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
git push heroku main
```

#### AWS Lambda (Serverless)

1. Package your code with dependencies
2. Create Lambda function
3. Set environment variables
4. Use CloudWatch Events for scheduling

### Option 3: Raspberry Pi (24/7 at Home)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Set up cron job for daily execution
crontab -e
# Add: 0 8 * * * /usr/bin/python3 /home/pi/mitzvah_bot/mitzvah_whatsapp_bot.py
```

## Troubleshooting

### Common Issues

1. **"No module named 'twilio'"**

   ```bash
   pip install twilio
   ```

2. **"Authentication failed"**

   - Check your Account SID and Auth Token
   - Make sure they're correctly set in .env file

3. **"Invalid phone number format"**

   - Use international format: +1234567890
   - Include country code

4. **Messages not sending**
   - Verify WhatsApp sandbox setup
   - Check Twilio console logs
   - Ensure recipient numbers are verified in sandbox

### Twilio WhatsApp Sandbox Setup

1. Go to Twilio Console → WhatsApp → Sandbox
2. Send the join code to the sandbox number
3. Your number is now authorized to receive messages

### Environment Variables

Create `.env` file with:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
```

## Message Customization

Edit the `format_message()` function in `mitzvah_whatsapp_bot.py` to customize:

- Message format
- Emojis
- Additional content
- Language

## Scheduling Options

Default: 8:00 AM daily
To change time, edit this line:

```python
schedule.every().day.at("08:00").do(bot.send_daily_mitzvah)
```

Examples:

```python
# 7:30 AM
schedule.every().day.at("07:30").do(bot.send_daily_mitzvah)

# Multiple times per day
schedule.every().day.at("08:00").do(bot.send_daily_mitzvah)
schedule.every().day.at("20:00").do(bot.send_daily_mitzvah)

# Specific days
schedule.every().sunday.at("08:00").do(bot.send_daily_mitzvah)
```

## Cost Information

### Twilio WhatsApp Pricing

- **Sandbox**: Free for testing
- **Production**: ~$0.005 per message
- **Monthly cost** for daily messages: ~$1.50/month per recipient

### Hosting Costs

- **Local**: Free (electricity only)
- **Heroku**: Free tier available
- **AWS Lambda**: ~$1-2/month for daily execution
- **Raspberry Pi**: $35 one-time cost

## Security Best Practices

1. **Never commit .env file** to version control
2. **Use environment variables** for all credentials
3. **Regularly rotate** API tokens
4. **Limit recipient list** to trusted numbers
5. **Monitor usage** in Twilio console

## Support

For issues:

1. Check Twilio console logs
2. Review `mitzvah_bot.log` file
3. Test with single recipient first
4. Verify CSV file format matches Schedule_Corrected.csv

## Alternative Methods

If Twilio doesn't work for you:

1. **WhatsApp Business API** (more complex setup)
2. **WhatsApp Web automation** (pywhatkit library)
3. **Telegram Bot** (easier alternative)
4. **SMS instead of WhatsApp** (Twilio SMS is simpler)
