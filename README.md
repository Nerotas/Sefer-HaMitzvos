# Rambam Daily Mitzvah System

A comprehensive system for managing and distributing daily Mitzvah notifications from Maimonides' Sefer HaMitzvos. The system includes WhatsApp Business integration, calendar generation tools, and Google Calendar integration.

## 🎯 Overview

This project provides multiple ways to engage with the 613 Mitzvot (commandments) from Maimonides' Sefer HaMitzvos through automated daily notifications and calendar systems.

### Key Features

- **WhatsApp Business Integration**: Automated daily Mitzvah notifications via Twilio
- **PDF Calendar Generation**: Professional calendar formats for printing and sharing
- **Google Calendar Integration**: Public calendar with automated event creation
- **ICS Export**: Universal calendar format compatible with all calendar applications
- **AWS Lambda Deployment**: Scalable serverless architecture

## 📁 Project Structure

```
├── bots/                    # WhatsApp bot implementation
├── calendar_outputs/        # Generated calendar files (PDF, ICS)
├── data/                    # CSV data files with Mitzvot schedules
├── docs/                    # Documentation and setup guides
├── lambda_deploy/           # AWS Lambda deployment files
├── scripts/                 # Utility scripts
├── tools/                   # Main tools and generators
│   ├── calendar/           # Google Calendar and ICS tools
│   └── pdf/               # PDF generation tools
├── web/                    # Web interface components
└── temp/                   # Temporary files and test data
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud Platform account (for calendar integration)
- Twilio account (for WhatsApp integration)
- AWS account (for Lambda deployment)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Rambam.git
cd Rambam
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r tools/requirements.txt
```

## �️ Available Tools

### PDF Calendar Generation

- **Schedule Format**: `tools/pdf/create_schedule_pdf.py`
  - Optimized daily schedule with grouped Mitzvot
  - Professional formatting with source citations
  - 350 unique dates instead of 629 individual entries

- **Calendar Grid Format**: `tools/pdf/create_calendar_pdf.py`
  - Traditional monthly calendar layout
  - Mitzvot displayed in calendar cells
  - Printable format for wall calendars

### Google Calendar Integration

- **Calendar Creator**: `tools/calendar/create_google_calendar.py`
  - Creates public Google Calendar
  - Bulk event creation with notifications
  - OAuth2 authentication flow

- **Analysis Tool**: `tools/calendar/google_calendar_analysis.py`
  - Comprehensive planning and analysis
  - Integration requirements assessment

### Universal Calendar Export

- **ICS Generator**: `tools/calendar/create_ics_calendar.py`
  - Creates standard .ics calendar files
  - Compatible with Outlook, Apple Calendar, etc.
  - No authentication required

## 📖 Documentation

### Setup Guides

- **Calendar Integration**: `docs/CALENDAR_README.md`
  - Comparison of all calendar methods
  - Feature matrix and recommendations
  - Usage instructions for each tool

- **Google Calendar Setup**: `docs/GOOGLE_CALENDAR_SETUP.md`
  - Complete Google Cloud Console configuration
  - OAuth2 setup and troubleshooting
  - Verification bypass for unverified apps

- **ICS Import Guide**: `docs/ics_import_instructions.md`
  - Step-by-step calendar application setup
  - Platform-specific import instructions

### System Documentation

- **AWS System**: `AWS-SYSTEM-README.md`
  - WhatsApp bot architecture
  - Lambda deployment process
  - Twilio integration details
## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token

# Google Calendar API
GOOGLE_CALENDAR_CREDENTIALS_FILE=credentials.json

# AWS Configuration
AWS_REGION=your_aws_region
```

### Google Calendar Setup

1. Follow `docs/GOOGLE_CALENDAR_SETUP.md`
2. Download `credentials.json` from Google Cloud Console
3. Place in project root (protected by `.gitignore`)

## 🚀 Deployment

### AWS Lambda (WhatsApp Bot)

```bash
# Package and deploy
.\create_lambda_package.ps1
# Deploy using AWS CLI or Console
```

### Local Development

```bash
# Run PDF generation
python tools/pdf/create_schedule_pdf.py

# Run Google Calendar integration
python tools/calendar/create_google_calendar.py

# Generate ICS file
python tools/calendar/create_ics_calendar.py
```

## 📊 Data Sources

- **Primary Dataset**: `data/Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv`
  - 629 Mitzvot entries with dates and sources
  - Complete Sefer HaMitzvos coverage
  - Biblical and Rabbinic classifications

- **Master List**: `data/MitzvosMasterList.csv`
  - Reference list of all 613 Mitzvot
  - Categorization and indexing

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Maimonides (Rambam) for the Sefer HaMitzvos
- ReportLab for PDF generation capabilities
- Google Calendar API for integration support
- Twilio for WhatsApp Business messaging

## 📞 Support

For questions or support:

1. Check the documentation in `docs/`
2. Review troubleshooting guides
3. Open an issue on GitHub
4. Contact the maintainers

---

*"The goal of the Torah's commandments is to bring mercy, loving-kindness, and peace to the world."* - Maimonides

1. Upload `mitzvah_bot_lambda.zip` to AWS Lambda
2. Configure Twilio credentials as environment variables
3. Set up daily CloudWatch Events trigger
4. Test with: `{"test_date": "2025-11-02", "test_mode": true}`

### Consent capture (optional, recommended)

This repo includes a simple consent flow:

- `ConsentHandler` Lambda with a Function URL (HTTP) to capture opt-ins via:
  - WhatsApp keyword (reply "JOIN MITZVAH" to your WhatsApp number)
  - Web form posting to the Function URL
- DynamoDB table `${STACK}-subscribers` to store consent records.

How to use:

1. Deploy with SAM (the workflow does this). Note the output `ConsentFunctionUrl`.
2. Set your site’s `web/optin.html` constants:
   - CONSENT_URL = the `ConsentFunctionUrl`
   - WHATSAPP_NUMBER = your WhatsApp E.164 number (e.g., +15551234567)
3. Point your Twilio WhatsApp sender’s incoming webhook to `ConsentFunctionUrl` to accept JOIN/STOP.
4. To send to opted-in users, set env `SUBSCRIBERS_TABLE` on the sending Lambda (the template wires it automatically) and omit `RECIPIENTS`, or keep both (DynamoDB takes precedence).

Data model (DynamoDB):

- Partition key `phone` (E.164)
- Attributes: `channel`, `consent_purpose`, `consent_status`, `source`, `evidence`, `timestamp_iso`, `updated_by`

## 🔍 Verification Process

Source accuracy verified through comprehensive comparison:

- **Master List Sources**: Traditional biblical references (613 mitzvot)
- **Schedule Sources**: Corrected to match master list (100% accuracy)
- **Verification Scripts**: Automated tools ensure ongoing consistency

## 📊 Statistics

- **Total Mitzvot**: 613 (248 positive, 365 negative)
- **Schedule Entries**: 628 (with holiday consolidations)
- **Source Match Rate**: 100.0%
- **Coverage Period**: Full year (365 days)
- **Holiday Integration**: Special entries for major holidays

## 🛠️ Development

### Technical Features

- **UTF-8 BOM Handling**: Robust CSV loading across platforms
- **Test Mode Support**: Date-specific testing capabilities
- **Error Recovery**: Fallback mechanisms for reliability
- **Debug Logging**: Comprehensive troubleshooting information

## 📜 Sources

- **Maimonides' Sefer HaMitzvot**: Educational summaries and structure
- **Traditional Biblical Sources**: Verified against authoritative lists
- **Sefaria Integration**: Direct links to source texts

---

**Project Status**: ✅ Complete - All sources verified, bot deployed, schedule ready for production use.

**Last Updated**: October 2025
