# 🕊️ Sefer HaMitzvos - WhatsApp Daily Study Bot

> _Automated daily mitzvah study messages via WhatsApp_

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Nerotas/Sefer-HaMitzvos)

## 📚 **Overview**

This project provides a WhatsApp bot that sends daily study messages from the Rambam's Sefer HaMitzvos (Book of Commandments), covering all 613 mitzvot in an organized schedule. Perfect for individuals or groups wanting to complete a systematic study of Jewish commandments.

## ✨ **Features**

- 🤖 **Automated Daily Messages** - Sends at 8 AM UTC daily
- 📱 **WhatsApp Integration** - Uses Twilio API for reliable delivery
- 📊 **Structured Schedule** - 613 mitzvot organized over ~1 year
- 🌍 **Multi-recipient** - Send to individuals or groups
- ☁️ **Cloud Ready** - Deploy free on Railway, Heroku, or Render
- 📖 **Hebrew Sources** - Biblical references in Hebrew (Shemos, Devarim, etc.)

## 🚀 **Quick Deploy**

### **1-Click Railway Deploy**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Nerotas/Sefer-HaMitzvos)

### **Manual Setup**

1. **Clone repository**
2. **Get Twilio credentials** (see [`docs/TWILIO_SETUP_GUIDE.md`](docs/TWILIO_SETUP_GUIDE.md))
3. **Deploy to cloud** (see [`docs/RAILWAY_DEPLOYMENT_PLAN.md`](docs/RAILWAY_DEPLOYMENT_PLAN.md))

## 📂 **Repository Structure**

```
├── 📁 bots/                    # WhatsApp bot implementations
│   ├── mitzvah_bot_cloud.py    # Production bot (recommended)
│   ├── mitzvah_whatsapp_bot.py # Local development version
│   └── simple_whatsapp_bot.py  # Browser-based alternative
├── 📁 deployment/              # Cloud deployment configurations
│   ├── railway.json           # Railway deployment config
│   ├── Procfile               # Heroku/Railway process file
│   ├── render.yaml            # Render deployment config
│   └── deploy_*.sh/.bat       # Automated deployment scripts
├── 📁 docs/                    # Documentation
│   ├── RAILWAY_DEPLOYMENT_PLAN.md  # Step-by-step Railway setup
│   ├── TWILIO_SETUP_GUIDE.md      # Twilio account & credentials
│   └── *.md                       # Additional guides
├── 📁 scripts/                 # Data processing utilities
│   ├── convert_to_csv.py       # Convert text to structured CSV
│   ├── convert_books_to_hebrew.py # Hebrew book name conversion
│   └── create_corrected_schedule.py # Generate aligned schedule
├── 📁 OLD/                     # Original source files
├── 📊 MitzvosMasterList.csv    # Complete 613 mitzvot list
├── 📅 Schedule.csv             # Original study schedule
├── ✅ Schedule_Corrected.csv   # Aligned schedule (bot uses this)
└── 📋 requirements.txt         # Python dependencies
```

## 💬 **Sample Message**

```
🕊️ Sefer HaMitzvos Daily Study 📚

📅 Friday, October 11, 2025

🔢 Mitzvah #1
_To believe that God exists and is the source of all existence_

📚 Source: Devarim 6:4

Fulfill this mitzvah with joy and intention! 💫🙏

—Daily Mitzvah Bot
```

## 🛠️ **Technology Stack**

- **Language**: Python 3.11+
- **Messaging**: Twilio WhatsApp API
- **Scheduling**: Python `schedule` library
- **Deployment**: Railway, Heroku, Render (free tiers available)
- **Data**: CSV-based mitzvot database

## 💰 **Cost**

- **Free Options**: Railway ($5/month credit), Twilio Sandbox
- **Production**: ~$5-10/month for unlimited recipients
- **Per Message**: ~$0.005 per WhatsApp message sent

## 📖 **Documentation**

| Guide                                                 | Description                       |
| ----------------------------------------------------- | --------------------------------- |
| [Railway Deployment](docs/RAILWAY_DEPLOYMENT_PLAN.md) | Complete Railway setup guide      |
| [Twilio Setup](docs/TWILIO_SETUP_GUIDE.md)            | Get WhatsApp API credentials      |
| [Cloud Deployment](docs/CLOUD_DEPLOYMENT_COMPLETE.md) | Multi-platform deployment options |

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push branch: `git push origin feature-name`
5. Open pull request

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Rambam (Maimonides)** - For the Sefer HaMitzvos
- **Twilio** - For WhatsApp API infrastructure
- **Railway** - For free cloud hosting

---

**_May your Torah study illuminate your path! ✨📚_**

_Built with ❤️ for daily Torah learning_
