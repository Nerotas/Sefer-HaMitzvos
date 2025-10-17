# 🕊️ Sefer HaMitzvos - AWS Lambda WhatsApp Bot

> _Serverless daily mitzvah study messages via WhatsApp using AWS Lambda_

## 📚 **Overview**

This project provides an AWS Lambda-powered WhatsApp bot that sends daily study messages from the Rambam's Sefer HaMitzvos (Book of Commandments), covering all 613 mitzvot in an organized 354-day cycle. Perfect for automated daily Torah study delivered to your WhatsApp.

## ✨ **Features**

- 🤖 **Serverless Architecture** - AWS Lambda for zero-maintenance automation
- 📱 **WhatsApp Integration** - Twilio API for reliable message delivery
- 📊 **354-Day Schedule** - All 613 mitzvot organized in annual cycle
- 🕐 **Custom Timing** - Configurable daily delivery (default: 1:10 PM CST)
- 💰 **Cost-Effective** - Runs for ~$0.001/month on AWS free tier
- 📖 **Hebrew Sources** - Biblical references with English translations
- 🔄 **Auto-Cycling** - Automatically restarts after completing all 613 mitzvot

## 🚀 **Quick Setup**

### **Prerequisites**

1. **AWS Account** - Free tier eligible
2. **Twilio Account** - WhatsApp sandbox access
3. **WhatsApp Number** - For receiving daily messages

### **Deployment**

1. **Upload** `mitzvah_bot_lambda_FIXED.zip` to AWS Lambda
2. **Configure** environment variables (Twilio credentials)
3. **Set** timeout to 30 seconds
4. **Schedule** daily execution with CloudWatch Events

## 📂 **Repository Structure**

```
├── 📁 bots/                           # Lambda bot implementation
│   └── lambda_mitzvah_bot.py          # AWS Lambda function (main bot)
├── 📁 docs/                           # Documentation
│   ├── AWS_LAMBDA_SETUP.md           # Complete Lambda setup guide
│   └── SCHEDULE_SETUP.md              # Daily scheduling configuration
├── 📁 archive/                        # Archived old implementations
│   ├── bots_old/                     # Previous bot versions
│   ├── docs_old/                     # Old documentation
│   └── deployment_old/               # Legacy deployment configs
├── 📊 MitzvosMasterList.csv           # Complete 613 mitzvot reference
├── 📅 Schedule.csv                    # 354-day mitzvot schedule (embedded in bot)
├── 📦 mitzvah_bot_lambda.zip          # Ready-to-deploy Lambda package
├── 🔧 create_lambda_package.bat       # Package creation script
├── 📋 requirements.txt                # Python dependencies
└── 🔐 .env.example                   # Environment variables template
```

## 💬 **Sample Message**

```
�️ Daily Mitzvah - Day 20 of 354

� Source: שמות כ:ב - אנכי ה' אלהיך

� Translation: To believe that God exists and is the source of all existence

#SeferHaMitzvos #DailyTorah
```

## 🛠️ **Technology Stack**

- **Platform**: AWS Lambda (Serverless)
- **Language**: Python 3.11
- **Messaging**: Twilio WhatsApp API
- **Scheduling**: CloudWatch Events (Cron)
- **Data**: Embedded CSV schedule (354 days)

## 💰 **Cost Breakdown**

- **AWS Lambda**: ~$0.001/month (free tier)
- **CloudWatch Events**: ~$0.00/month (free tier)
- **Twilio WhatsApp**: ~$0.005 per message sent
- **Total**: ~$0.15/month for daily messages

## 📖 **Documentation**

| Guide                                        | Description                      |
| -------------------------------------------- | -------------------------------- |
| [AWS Lambda Setup](docs/AWS_LAMBDA_SETUP.md) | Complete Lambda deployment guide |
| [Schedule Setup](docs/SCHEDULE_SETUP.md)     | Daily automation configuration   |

## 🚀 **Getting Started**

1. **Download** `mitzvah_bot_lambda.zip`
2. **Create** AWS Lambda function
3. **Upload** the package
4. **Configure** Twilio environment variables
5. **Set** 30-second timeout
6. **Schedule** daily execution
7. **Test** and enjoy daily mitzvah messages!

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
- **AWS** - For serverless infrastructure
- **Twilio** - For WhatsApp API

---

**_May your Torah study illuminate your path! ✨📚_**

_Built with ❤️ for daily Torah learning_
