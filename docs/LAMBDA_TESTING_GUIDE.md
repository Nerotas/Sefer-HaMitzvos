# Lambda Bot Testing Guide

## Overview

You now have two ways to test your Lambda mitzvah bot with specific dates:

## Method 1: Local Testing (Recommended for Quick Testing)

### Command Line Testing

```bash
python simple_test_bot.py 2025-11-02
```

### Interactive Testing

```bash
python simple_test_bot.py
# Then choose option 1 and enter a date
```

### What You'll See:

- ✅ Loads your complete CSV schedule
- 🔍 Finds the mitzvah(s) for your specified date
- 📱 Shows exactly what WhatsApp message would be sent
- 📋 Displays mitzvah numbers, titles, and sources

## Method 2: AWS Lambda Testing

### Step 1: Use the Test Event JSON

The local test creates a JSON file like `lambda_test_event_2025_11_02.json` with:

```json
{
  "test_date": "2025-11-02",
  "test_mode": true
}
```

### Step 2: In AWS Lambda Console

1. Go to your Lambda function
2. Click "Test"
3. Create new test event
4. Paste the JSON content from the generated file
5. Run the test

### Modified Lambda Handler

Your Lambda function now accepts a `test_date` parameter:

- If `event['test_date']` is provided, it uses that date
- Otherwise, it uses today's date (normal operation)

## Examples from Your Schedule

### Tzitzit Example (Your Specific Case)

```bash
python simple_test_bot.py 2025-11-02
```

**Result**:

- Positive 13: Hand Tefillin
- Positive 14: Tzitzit (fringes) ← This is the example you mentioned!
- Source discrepancy: `Devarim 10:19` vs `Bamidbar 15:38` (Master List)

### Schedule Start

```bash
python simple_test_bot.py 2025-10-20
```

**Result**: Introduction principles (Intro 1, Intro 2)

### Prayer Mitzvah

```bash
python simple_test_bot.py 2025-10-29
```

**Result**: Positive 5 - Prayer to G-d

## Key Features

### ✅ What Works:

- Tests any date in your schedule (2025-10-20 to 2026+ range)
- Shows combined mitzvot when multiple are scheduled for one day
- Displays biblical sources (the ones we found discrepancies with)
- Formats exact WhatsApp message content
- Creates AWS Lambda test events

### 🔍 What You Can Verify:

- Source accuracy (compare with your master list findings)
- Message formatting
- Date coverage
- Holiday logic (if implemented)

## Quick Date References from Analysis

Based on our source mismatch analysis:

- **2025-11-02**: Tzitzit - Source mismatch identified
- **2025-10-29**: Prayer - Source mismatch identified
- **2025-11-05**: Blessing after eating - Source mismatch identified

## Usage Tips

1. **Test Before Deployment**: Always test dates locally first
2. **Verify Sources**: Cross-reference with master list for accuracy
3. **Check Edge Cases**: Test holiday dates and schedule boundaries
4. **AWS Lambda Testing**: Use generated JSON files for cloud testing

## Files Created

- `simple_test_bot.py` - Local testing utility
- `lambda_test_event_*.json` - AWS Lambda test events
- Modified `bots/lambda_mitzvah_bot.py` - Enhanced with test date support
