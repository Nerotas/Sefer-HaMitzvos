# Free Cloud Deployment Guide for WhatsApp Mitzvah Bot

## 🆓 Best Free Cloud Options

### 1. **Heroku (Recommended - Easiest)**

- **Free tier**: 550-1000 dyno hours/month
- **Perfect for**: 24/7 bots with scheduling
- **Cost**: Free (with credit card verification)

### 2. **Railway**

- **Free tier**: $5 credit/month (lasts ~2-3 months for small bots)
- **Easier than Heroku**: Modern interface
- **Cost**: Effectively free for several months

### 3. **Render**

- **Free tier**: Limited but sufficient for bots
- **Good alternative**: If Heroku is full
- **Cost**: Free

### 4. **PythonAnywhere**

- **Free tier**: Limited always-on tasks
- **Good for**: Simple scheduled scripts
- **Cost**: Free (with limitations)

---

## 🚀 Method 1: Heroku Deployment (Recommended)

### Prerequisites

- Heroku account (free)
- Git installed on your computer
- Credit card (for verification - won't be charged)

### Step 1: Prepare Your Bot for Heroku

First, let's create the necessary Heroku files:

#### Create `Procfile`:

```
worker: python mitzvah_whatsapp_bot.py
```

#### Create `runtime.txt`:

```
python-3.11.6
```

#### Update `requirements.txt` to include gunicorn:

```
twilio==8.10.0
schedule==1.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

### Step 2: Install Heroku CLI

**Windows:**

```bash
# Download and install from: https://devcenter.heroku.com/articles/heroku-cli
```

**Mac:**

```bash
brew install heroku/brew/heroku
```

**Linux:**

```bash
sudo snap install --classic heroku
```

### Step 3: Deploy to Heroku

```bash
# 1. Login to Heroku
heroku login

# 2. Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# 3. Create Heroku app
heroku create your-mitzvah-bot-name

# 4. Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_account_sid_here
heroku config:set TWILIO_AUTH_TOKEN=your_auth_token_here
heroku config:set TWILIO_WHATSAPP_NUMBER=+14155238886

# 5. Deploy
git push heroku main

# 6. Scale the worker (start the bot)
heroku ps:scale worker=1

# 7. Check logs
heroku logs --tail
```

---

## 🚂 Method 2: Railway Deployment (Modern & Easy)

### Step 1: Prepare Files

Create these files in your project:

#### `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python mitzvah_whatsapp_bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up** with GitHub
3. **Click "Deploy from GitHub repo"**
4. **Select your repository**
5. **Add environment variables**:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER`
6. **Deploy!**

---

## 🎨 Method 3: Render Deployment

### Step 1: Create `render.yaml`

```yaml
services:
  - type: worker
    name: mitzvah-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python mitzvah_whatsapp_bot.py
    envVars:
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: TWILIO_WHATSAPP_NUMBER
        value: "+14155238886"
```

### Step 2: Deploy to Render

1. **Go to [Render.com](https://render.com)**
2. **Connect GitHub account**
3. **Create new "Background Worker"**
4. **Select your repository**
5. **Add environment variables**
6. **Deploy**

---

## 🐍 Method 4: PythonAnywhere (Limited Free)

### Setup

1. **Go to [PythonAnywhere.com](https://www.pythonanywhere.com)**
2. **Create free account**
3. **Upload files** via web interface
4. **Install dependencies** in console:
   ```bash
   pip3.10 install --user twilio schedule python-dotenv
   ```
5. **Create scheduled task**:
   - Go to Dashboard → Tasks
   - Add: `python3.10 /home/yourusername/mitzvah_whatsapp_bot.py`
   - Schedule: Daily at 08:00

---

## 📁 Deployment Files to Create

Let me create all the necessary deployment files for you:

### For All Platforms:
