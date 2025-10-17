# 🚀 Deployment Notifications Setup Guide

## 📱 **What Are Deployment Notifications?**

Your bot can now send WhatsApp messages whenever it's deployed, restarted, or encounters errors. This helps you monitor your bot's status in real-time!

## 💬 **Sample Deployment Message**

```
🚀 Bot Deployment Notification

⏰ Time: 2025-10-17 14:30:25 UTC
🤖 Status: Bot Started Successfully
🌐 Environment: Railway (production)
📝 Version: v2.0.0
🔧 Mode: SCHEDULER
👥 Recipients: 3

✅ Daily Mitzvah Bot is now running!

—Deployment Monitor
```

## ⚙️ **Environment Variables for Railway**

Add these to your Railway project variables:

```env
# Required for bot functionality
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_32_character_token
TWILIO_WHATSAPP_NUMBER=+14155238886
RECIPIENTS=JpwWqLb9Dv0K8KUQsX3KcO@g.us

# Deployment mode
DEPLOY_MODE=scheduler

# Deployment notifications (NEW)
SEND_DEPLOY_NOTIFICATIONS=true
BOT_VERSION=v2.0.0
```

## 🔧 **Configuration Options**

### **Enable/Disable Notifications**

```env
SEND_DEPLOY_NOTIFICATIONS=true   # Send deployment notifications
SEND_DEPLOY_NOTIFICATIONS=false  # Disable notifications
```

### **Version Tracking**

```env
BOT_VERSION=v2.0.0  # Shows in deployment messages
BOT_VERSION=v2.1.0  # Update when you make changes
```

## 📊 **Types of Notifications**

### **1. Deployment Success** 🚀

- Sent when bot starts successfully
- Shows environment, version, mode, recipient count
- Confirms bot is running

### **2. Error Notifications** ❌

- Sent when bot encounters errors
- Shows error message and timestamp
- Indicates bot will restart automatically

### **3. Shutdown Notifications** 🛑

- Sent when bot shuts down gracefully
- Only for WhatsApp Web bot (local version)
- Indicates planned restart

## 🌐 **Environment Detection**

The bot automatically detects where it's running:

| Platform | Detection             | Message Shows            |
| -------- | --------------------- | ------------------------ |
| Railway  | `RAILWAY_ENVIRONMENT` | `Railway (production)`   |
| Heroku   | `HEROKU_APP_NAME`     | `Heroku (your-app-name)` |
| Render   | `RENDER_SERVICE_NAME` | `Render (your-service)`  |
| Local    | OS detection          | `Local (Windows)`        |

## 🎯 **Setup for Different Bots**

### **Cloud Bot (Twilio) - Recommended**

- **File**: `bots/mitzvah_bot_cloud.py`
- **Notifications**: Via WhatsApp (Twilio API)
- **Environment Variables**: Add to Railway dashboard
- **Reliability**: High (API-based)

### **WhatsApp Web Bot (Local)**

- **File**: `bots/whatsapp_web_group_bot.py`
- **Notifications**: Via WhatsApp Web automation
- **Environment Variables**: Set locally or in `.env` file
- **Reliability**: Medium (browser-based)

## 📋 **Railway Setup Steps**

1. **Go to Railway Project** → Variables tab

2. **Add Notification Variables**:

   ```
   SEND_DEPLOY_NOTIFICATIONS = true
   BOT_VERSION = v2.0.0
   ```

3. **Deploy Your Bot** (it will redeploy automatically)

4. **Check Your WhatsApp** for deployment notification!

5. **Update Version** when making changes:
   ```
   BOT_VERSION = v2.1.0  # Update this for each deployment
   ```

## 🔄 **Testing Deployment Notifications**

### **Test Mode**

```env
DEPLOY_MODE=test
SEND_DEPLOY_NOTIFICATIONS=true
```

- Sends one deployment notification + one mitzvah message
- Good for testing notification format

### **Scheduler Mode**

```env
DEPLOY_MODE=scheduler
SEND_DEPLOY_NOTIFICATIONS=true
```

- Sends deployment notification on startup
- Runs continuously with daily messages at 8 AM

## ⚠️ **Important Notes**

### **Notification Frequency**

- ✅ **One per deployment** - Not spammy
- ✅ **Error notifications** - Only to first recipient
- ✅ **Rate limited** - 1 second between messages

### **Group vs Individual**

- **Groups**: Single notification to group
- **Multiple recipients**: Notification to each recipient
- **Error notifications**: Only to first recipient (avoids spam)

### **Cost Considerations**

- **Twilio**: Each notification costs ~$0.005
- **Daily cost**: Minimal (1-2 notifications per day max)
- **WhatsApp Web**: Completely free

## 🛠️ **Troubleshooting**

### **No Notifications Received**

1. **Check environment variable**: `SEND_DEPLOY_NOTIFICATIONS=true`
2. **Verify recipients**: Same as daily mitzvah recipients
3. **Check Railway logs**: Look for "Deployment notification sent"

### **Too Many Notifications**

```env
SEND_DEPLOY_NOTIFICATIONS=false  # Disable temporarily
```

### **Wrong Environment Shown**

- Railway should auto-detect correctly
- Manual override: `BOT_VERSION=v2.0.0-production`

## 📈 **Benefits**

✅ **Monitor Bot Health** - Know when deployments succeed/fail
✅ **Track Versions** - See which version is running
✅ **Error Alerts** - Get notified of issues immediately
✅ **Peace of Mind** - Confirm bot is working after deployments
✅ **Group Transparency** - Group members see bot status

## 🎉 **Ready to Deploy!**

Your bot now has enterprise-level deployment monitoring! Every time you:

- Deploy to Railway
- Update your code
- Change environment variables
- Bot restarts after errors

Your WhatsApp group will get a professional status update! 🚀📱✨

---

_Deployment notifications help ensure your daily Torah study never gets interrupted!_ 🕊️📚
