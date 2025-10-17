# 🕐 Daily Scheduling Setup for Mitzvah Bot

## Status: Lambda Function Working ✅

- Lambda function successfully deployed and tested
- Bot can send WhatsApp messages via Twilio
- Ready for daily automation

## 📅 Schedule Configuration

### Target Time: 1:10 PM CST Daily

### AWS CloudWatch Events Setup:

1. **In AWS Lambda Console:**

   - Go to your `daily-mitzvah-bot` function
   - Click **Configuration** → **Triggers**
   - Click **Add trigger**

2. **Configure the Trigger:**
   - **Source**: EventBridge (CloudWatch Events)
   - **Rule type**: Schedule expression
   - **Schedule expression**: `cron(10 18 * * ? *)`
     - This runs at 6:10 PM UTC = 1:10 PM CST
   - **Enable trigger**: ✅ Yes
   - Click **Add**

## 🎯 What This Achieves

Once scheduled, the bot will automatically:

- **Run daily at 1:10 PM CST**
- Calculate current day number in the 354-day cycle
- Look up today's mitzvah from Schedule_Corrected.csv
- Send WhatsApp message with:
  - Hebrew source text
  - English translation
  - Day number and mitzvah details

## 💰 Cost Estimate

- **Execution time**: ~5-10 seconds per day
- **Daily cost**: ~$0.0000033
- **Monthly cost**: ~$0.0001 (practically free)
- **Annual cost**: ~$0.001

## 🔍 Monitoring Options

### CloudWatch Logs

- **Log Group**: `/aws/lambda/daily-mitzvah-bot`
- **View execution details**: Success/failure status
- **Debug information**: Detailed logging from lambda_mitzvah_bot_fixed.py

### Lambda Metrics

- **Invocations**: Track daily executions
- **Duration**: Monitor execution time
- **Errors**: Alert on failures

### Optional: Set Up Alerts

Create CloudWatch alarms for:

- Failed executions
- Timeout errors
- Unusual execution patterns

## 📱 Message Format

Daily messages will include:

```
🕯️ Daily Mitzvah - Day [X] of 354

📖 Source: [Hebrew text]

📝 Translation: [English explanation]

#SeferHaMitzvos #DailyTorah
```

## 🔧 Troubleshooting

### If messages stop:

1. Check CloudWatch logs for errors
2. Verify Twilio sandbox status
3. Confirm environment variables are set
4. Test function manually

### Common Issues:

- **Twilio sandbox expiration**: Reactivate sandbox
- **Environment variables**: Check TWILIO_AUTH_TOKEN
- **Phone number format**: Ensure +1234567890 format

## 📋 Implementation Checklist

- [ ] Set up CloudWatch trigger
- [ ] Test first scheduled execution
- [ ] Monitor logs for first week
- [ ] Verify message delivery timing
- [ ] Set up failure alerts (optional)

Ready to implement when you decide to activate daily scheduling!
