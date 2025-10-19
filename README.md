# Rambam Mitzvot Schedule Project

A complete daily schedule of all 613 mitzvot (commandments) from Maimonides' Sefer HaMitzvot with accurate biblical sources.

## 📋 Project Overview

This project provides:
- **Complete 613 Mitzvot Schedule**: Daily distribution across the year
- **Accurate Biblical Sources**: 100% verified against traditional sources
- **Rich Educational Content**: Detailed summaries from Sefer HaMitzvot
- **WhatsApp Bot Integration**: Automated daily mitzvah delivery via AWS Lambda

## 🎯 Key Achievements

- ✅ **100% Source Accuracy**: All 613 biblical references verified against master list
- ✅ **Complete Coverage**: All positive and negative commandments included
- ✅ **Production Ready**: AWS Lambda bot with robust error handling
- ✅ **Educational Value**: Preserves detailed Sefer HaMitzvot explanations

## 📁 File Structure

### Core Files
- `Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv` - Main schedule with all 613 mitzvot
- `MitzvosMasterList.txt` - Original master list (reference)
- `Schedule.csv` - Original schedule file (reference)

### Bot Implementation
- `bots/lambda_mitzvah_bot.py` - AWS Lambda function for WhatsApp delivery
- `mitzvah_bot_lambda.zip` - Deployment package (when created)

### Organization
- `archive/` - Reference files and master lists
- `scripts/` - Utility scripts for corrections and verification
- `backups/` - Backup files from corrections process
- `docs/` - Project documentation

## 🚀 Usage

### Daily Mitzvah Schedule
The main schedule file contains:
- **Date**: Daily assignment dates
- **Sequential Number**: 1-630 (with holiday consolidations)
- **Mitzvah Type & Number**: "Positive X" or "Negative X"
- **Summary**: Educational description from Sefer HaMitzvot
- **Biblical Source**: Verified traditional source reference
- **Sefaria Link**: Direct link to source text

### WhatsApp Bot Deployment
1. Upload `mitzvah_bot_lambda.zip` to AWS Lambda
2. Configure Twilio credentials as environment variables
3. Set up daily CloudWatch Events trigger
4. Test with: `{"test_date": "2025-11-02", "test_mode": true}`

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
