# ☁️ Cloud Deployment Guide for WhatsApp Mitzvah Bot

## 🚀 Quick Setup for Free Cloud Hosting

### Prerequisites

- GitHub account
- Twilio account (free tier available)
- WhatsApp Business API approved (or use Twilio Sandbox)

---

## 📱 Twilio Setup (Required for all platforms)

1. **Create Twilio Account**: https://www.twilio.com/try-twilio
2. **Get Credentials**:
   - Account SID (starts with AC...)
   - Auth Token (32-character string)
3. **WhatsApp Setup**:
   - **Sandbox Mode** (Immediate): Use +1 415 523 8886
   - **Production**: Request WhatsApp Business API approval
4. **Test Phone Numbers**: Add your number to Twilio Console → Phone Numbers → Verified Caller IDs

---

## 🔥 Method 1: Railway (Recommended - Easiest)

### Why Railway?

- ✅ $5 free credit monthly
- ✅ Automatic deploys from GitHub
- ✅ Built-in environment variables
- ✅ No credit card required initially

### Setup Steps:

1. **Push to GitHub**:

```bash
git init
git add .
git commit -m "Initial WhatsApp bot"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/mitzvah-bot.git
git push -u origin main
```

2. **Deploy on Railway**:

   - Go to https://railway.app
   - Sign up with GitHub
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Choose `mitzvah_bot_cloud.py`

3. **Set Environment Variables** in Railway Dashboard:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_32_character_token
RECIPIENTS=+1234567890,+9876543210
DEPLOY_MODE=scheduler
```

4. **Configure Startup**:
   - Railway auto-detects Python
   - Uses `Procfile`: `worker: python mitzvah_bot_cloud.py`

---

## 🚢 Method 2: Render (Free Tier)

### Setup:

1. **Connect GitHub**: https://render.com → New → Web Service
2. **Environment Variables**:
   - Same as Railway above
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python mitzvah_bot_cloud.py`

---

## ⚡ Method 3: Heroku (Free Tier Ended, but still popular)

### If you have Heroku credits:

```bash
# Install Heroku CLI
heroku create mitzvah-bot-yourname
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxx...
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set RECIPIENTS="+1234567890,+9876543210"
heroku config:set DEPLOY_MODE=scheduler
git push heroku main
```

---

## 🐍 Method 4: PythonAnywhere (Free Tier)

### Setup:

1. **Upload Files**: Use file browser to upload bot files
2. **Install Packages**:

```bash
pip3.10 install --user twilio schedule
```

3. **Create Task**: Dashboard → My Files → New Console
4. **Schedule**: Dashboard → Tasks → Create scheduled task
   - Command: `python3.10 /home/yourusername/mitzvah_bot_cloud.py`
   - Hour: 8, Minute: 0 (for 8 AM UTC)

---

## 📋 Configuration Options

### Environment Variables:

| Variable                 | Description                   | Example                   |
| ------------------------ | ----------------------------- | ------------------------- |
| `TWILIO_ACCOUNT_SID`     | Your Twilio Account SID       | `ACxxxxxxxxxxxxx`         |
| `TWILIO_AUTH_TOKEN`      | Your Twilio Auth Token        | `32-character-string`     |
| `TWILIO_WHATSAPP_NUMBER` | Twilio WhatsApp number        | `+14155238886`            |
| `RECIPIENTS`             | Comma-separated phone numbers | `+1234567890,+9876543210` |
| `DEPLOY_MODE`            | Bot operation mode            | `scheduler`               |

### Phone Number Format:

- ✅ `+1234567890` (with country code)
- ❌ `1234567890` (missing +)
- ❌ `123-456-7890` (with dashes)

### Deploy Modes:

- `scheduler`: Runs continuously, sends at 8 AM UTC daily
- `test`: Send one message and exit (for testing)
- `once`: Send today's message once and exit

---

## 🔧 Testing Your Deployment

### 1. Test Mode (Recommended first):

```bash
# Set environment variable
DEPLOY_MODE=test

# This will send one message and exit
```

### 2. Check Logs:

- **Railway**: Dashboard → Deployments → View Logs
- **Render**: Dashboard → Logs tab
- **Heroku**: `heroku logs --tail`

### 3. Verify Message Format:

```
🕊️ Sefer HaMitzvos Daily Study 📚

📅 Wednesday, December 18, 2024

🔢 Mitzvah #1
_To believe that God exists and is the source of all existence_

📚 Source: Devarim 6:4

Fulfill this mitzvah with joy and intention! 💫🙏

—Daily Mitzvah Bot
```

---

## ⚠️ Troubleshooting

### Common Issues:

1. **"Missing Twilio credentials"**:

   - Check environment variables are set correctly
   - Verify no extra spaces in variable values

2. **"Invalid phone number"**:

   - Ensure format: `+1234567890`
   - Add numbers to Twilio verified caller IDs for testing

3. **"Schedule file not found"**:

   - Make sure `Schedule_Corrected.csv` is in same directory
   - Check file permissions

4. **Messages not sending**:
   - Verify Twilio balance (sandbox is free)
   - Check WhatsApp sandbox setup
   - Review Twilio logs in console

### Debug Commands:

```bash
# Test Twilio connection
python -c "from twilio.rest import Client; print('Twilio imports successfully')"

# Check environment variables
python -c "import os; print(f'SID: {os.getenv(\"TWILIO_ACCOUNT_SID\", \"Not Set\")}')"
```

---

## 💰 Cost Breakdown

### Free Options:

1. **Railway**: $5/month credit (sufficient for this bot)
2. **Render**: 750 hours/month free
3. **PythonAnywhere**: Limited free tier
4. **Twilio Sandbox**: Free WhatsApp testing

### Paid (when you scale):

- **Twilio WhatsApp**: ~$0.005 per message
- **Cloud hosting**: $5-20/month for always-on

---

## 🎯 Recommended Setup

For beginners: **Railway** + **Twilio Sandbox**

- Easiest deployment
- No credit card required initially
- Good free tier
- Automatic deployments from GitHub

### Quick Railway Setup:

1. Fork this repository
2. Sign up at railway.app with GitHub
3. Deploy from your forked repo
4. Set environment variables in Railway dashboard
5. Done! ✨

---

## 📞 Support

If you need help:

1. Check logs first
2. Verify all environment variables
3. Test with `DEPLOY_MODE=test`
4. Review Twilio console for delivery status

Happy Torah learning! 🕊️📚
