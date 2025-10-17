# 🔧 AWS Lambda Timeout Fix Guide

## Issue Identified

Your Lambda function is timing out after 3 seconds during initialization. This is likely due to:

- Cold start delay when importing Twilio library
- Default Lambda timeout is too short (3 seconds)
- Twilio client initialization taking time

## Solution Package Created

📦 **mitzvah_bot_lambda_FIXED.zip** (8.6 MB)

### Fixes Applied:

1. **Module-level imports** - Twilio imported at module level to avoid cold start delays
2. **Enhanced logging** - Detailed logging at each step for debugging
3. **Timeout protection** - Better error handling for timeout scenarios
4. **Initialization logging** - Track exactly where the function gets stuck

## 🚀 Deployment Steps

### 1. Upload New Package

1. Go to AWS Lambda Console
2. Select your `daily-mitzvah-bot` function
3. In the **Code** tab, click "Upload from" → ".zip file"
4. Upload `mitzvah_bot_lambda_FIXED.zip`
5. Click **Deploy**

### 2. ⚠️ CRITICAL: Increase Timeout

**This is the most important step!**

1. Go to **Configuration** tab
2. Click **General configuration** → **Edit**
3. Change **Timeout** from `3 seconds` to `30 seconds`
4. Click **Save**

### 3. Verify Environment Variables

Make sure these are set in **Configuration** → **Environment variables**:

```
TWILIO_ACCOUNT_SID = ACacbcea137ed0e7f090a4a31ea44cfd25
TWILIO_AUTH_TOKEN = [your auth token]
TWILIO_PHONE_NUMBER = +16613059259
TARGET_PHONE_NUMBER = [your WhatsApp number in format +1234567890]
```

### 4. Test Function

1. Go to **Test** tab
2. Create test event with empty JSON: `{}`
3. Click **Test**
4. Check **Execution result** and **Logs**

## 📊 Expected Behavior After Fix

### Success Case:

```
INIT: Lambda starting...
INFO: Starting mitzvah bot execution
INFO: Twilio client created successfully
INFO: Environment variables loaded
INFO: Schedule loaded - 354 entries
INFO: Today is 2024-01-20, day number: 20
INFO: Today's mitzvah: [mitzvah details]
INFO: Message sent successfully
INFO: Bot execution completed
```

### If Still Timing Out:

Check CloudWatch logs for exactly where it stops. The detailed logging will show:

- Import completion
- Client creation
- API call timing

## 🕐 Scheduling Setup (After Testing)

Once the function works, set up daily execution:

1. Go to **Configuration** → **Triggers**
2. **Add trigger** → **EventBridge (CloudWatch Events)**
3. **Rule type**: Schedule expression
4. **Schedule expression**: `cron(10 18 * * ? *)`
   - This runs at 6:10 PM UTC = 1:10 PM CST
5. **Enable trigger**: Yes

## 💰 Cost Estimate

With 30-second timeout:

- **Execution time**: ~5-10 seconds per run
- **Daily cost**: ~$0.0000033
- **Monthly cost**: ~$0.0001 (practically free)

## 🔍 Troubleshooting

### If function still times out at 30 seconds:

1. Check CloudWatch logs for exact error
2. Verify Twilio credentials are correct
3. Test Twilio connection separately

### If "Module not found" errors:

1. Verify the ZIP was uploaded correctly
2. Check that `lambda_function.py` is at the root of the ZIP

### If "Environment variable not found":

1. Double-check environment variable names (case-sensitive)
2. Ensure TWILIO_AUTH_TOKEN is set correctly

## 📞 Support

If you encounter issues:

1. Check **CloudWatch Logs** for detailed error messages
2. Verify the function runs for at least 10-15 seconds before timing out
3. Test each environment variable is accessible

The new package should resolve the timeout issue. The key is increasing the timeout from 3 to 30 seconds!
