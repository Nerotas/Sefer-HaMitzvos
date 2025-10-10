# 🚀 Railway Deployment Plan for WhatsApp Mitzvah Bot

## ✅ **Completed Steps**

### **Repository Consolidation** 
- ✅ Moved all contents from `Sefer-HaMitzvos` subdirectory to main `Rambam` directory
- ✅ Consolidated all CSV files, scripts, and bot files
- ✅ Created `Schedule_Corrected.csv` with 354 entries (613 mitzvot properly aligned)
- ✅ Initialized git repository and committed all files
- ✅ Force pushed consolidated repository to GitHub: `Nerotas/Sefer-HaMitzvos`

### **Files Ready for Deployment**
- ✅ `mitzvah_bot_cloud.py` - Cloud-optimized bot with environment variable configuration
- ✅ `railway.json` - Railway deployment configuration
- ✅ `requirements.txt` - All Python dependencies (twilio, schedule, python-dotenv)
- ✅ `Procfile` - Process configuration for cloud deployment
- ✅ `Schedule_Corrected.csv` - Aligned schedule with Master List (100% accuracy verified)
- ✅ `MitzvosMasterList.csv` - Complete 613 mitzvot with Hebrew book names

---

## 🎯 **Next Steps: Railway Deployment**

### **Step 1: Deploy on Railway** 
1. **Go to Railway**: https://railway.app
2. **Sign in** with your existing Railway account
3. **Create New Project** → **Deploy from GitHub repo**
4. **Select Repository**: `Nerotas/Sefer-HaMitzvos`
5. **Railway Auto-Detection**: Will automatically detect Python and use `railway.json` config

### **Step 2: Set Up Twilio Account (Required)**
**WhatsApp messaging requires Twilio API:**

1. **Create Free Account**: https://www.twilio.com/try-twilio
2. **Get Credentials** from Twilio Console:
   - **Account SID**: Starts with `AC...` (example: `ACxxxxxxxxxxxxxxxxxxxxx`)
   - **Auth Token**: 32-character string
3. **WhatsApp Setup Options**:
   - **Sandbox Mode** (Immediate): Use `+14155238886` for testing
   - **Production Mode**: Request WhatsApp Business API approval (takes 1-3 days)

### **Step 3: Configure Environment Variables in Railway**
**In Railway Project Dashboard → Variables tab, add:**

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_32_character_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
RECIPIENTS=+1234567890,+9876543210
DEPLOY_MODE=test
```

**Important Configuration Notes:**
- **Phone Numbers**: Use international format with `+` (e.g., `+1234567890`)
- **Multiple Recipients**: Comma-separated, no spaces
- **DEPLOY_MODE Options**:
  - `test` - Send one message and exit (recommended for first deployment)
  - `scheduler` - Run continuously, send daily at 8 AM UTC
  - `once` - Send today's message once and exit

### **Step 4: Test Deployment**
1. **First Deploy**: Use `DEPLOY_MODE=test` 
2. **Check Railway Logs**: Verify message sent successfully
3. **Verify WhatsApp**: Confirm message received with proper formatting
4. **Switch to Production**: Change `DEPLOY_MODE=scheduler`

---

## 📱 **Expected Message Format**

```
🕊️ Sefer HaMitzvos Daily Study 📚

📅 Friday, October 11, 2025

🔢 Mitzvah #1
_To believe that God exists and is the source of all existence_

📚 Source: Devarim 6:4

Fulfill this mitzvah with joy and intention! 💫🙏

—Daily Mitzvah Bot
```

---

## 🔧 **Troubleshooting Guide**

### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| "Missing Twilio credentials" | Verify environment variables set correctly in Railway |
| "Invalid phone number" | Ensure format: `+1234567890` (include country code) |
| Messages not sending | Check Twilio console logs, verify sandbox setup |
| "Schedule file not found" | Ensure `Schedule_Corrected.csv` deployed with code |
| Bot keeps restarting | Check Railway logs for specific error messages |

### **Verification Commands** (for debugging)
```bash
# Test Twilio connection
python -c "from twilio.rest import Client; print('Twilio imports successfully')"

# Check environment variables  
python -c "import os; print(f'SID: {os.getenv(\"TWILIO_ACCOUNT_SID\", \"Not Set\")}')"

# Verify schedule file
python -c "import csv; print(len(list(csv.DictReader(open('Schedule_Corrected.csv')))))"
```

---

## 💰 **Cost Breakdown**

### **Free Tier Usage**
- **Railway**: $5/month free credit (sufficient for this bot)
- **Twilio Sandbox**: Free WhatsApp testing
- **GitHub**: Free public repository

### **Production Costs** (when scaling)
- **Railway**: ~$2-5/month for continuous deployment
- **Twilio WhatsApp**: ~$0.005 per message sent
- **Monthly Example**: 30 recipients × 30 days × $0.005 = $4.50/month

---

## 📋 **Deployment Checklist**

### **Pre-Deployment** ✅
- [x] Repository consolidated and pushed to GitHub
- [x] Railway configuration files ready
- [x] Schedule file created and verified (354 entries, 613 mitzvot)
- [x] Cloud-optimized bot code ready

### **During Deployment**
- [ ] Railway account connected to GitHub repository
- [ ] Twilio account created and credentials obtained
- [ ] Environment variables configured in Railway
- [ ] Test deployment completed successfully
- [ ] WhatsApp message format verified

### **Post-Deployment**
- [ ] Switch to `DEPLOY_MODE=scheduler` for daily messages
- [ ] Monitor Railway logs for first few days
- [ ] Verify daily messages arrive at 8 AM UTC
- [ ] Add/remove recipients as needed via Railway environment variables

---

## 🎯 **Success Metrics**

**Deployment Complete When:**
1. ✅ Railway shows "Deployed" status
2. ✅ Test message sends successfully via WhatsApp
3. ✅ Railway logs show no errors
4. ✅ Recipients receive properly formatted message
5. ✅ Daily scheduler activates (8 AM UTC)

---

## 📞 **Support Resources**

- **Railway Documentation**: https://docs.railway.app/
- **Twilio WhatsApp API**: https://www.twilio.com/docs/whatsapp
- **Project Repository**: https://github.com/Nerotas/Sefer-HaMitzvos
- **Railway Dashboard**: Your project at railway.app

---

## 🕊️ **Ready to Launch!**

Your WhatsApp Mitzvah Bot is fully prepared for deployment. The next step is simply:

1. **Deploy on Railway** (5 minutes)
2. **Set up Twilio** (10 minutes)  
3. **Configure environment variables** (2 minutes)
4. **Send test message** (instant verification)

**Total setup time**: ~20 minutes to daily automated Torah study! 📚✨

---

*Generated: October 10, 2025*  
*Repository: Nerotas/Sefer-HaMitzvos*  
*Deployment Target: Railway.app*