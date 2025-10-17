# AWS Lambda Setup Guide for Daily Mitzvah Bot

## Why AWS Lambda is Perfect for This:

- **Cost**: ~$0.01-0.05 per month (practically free)
- **Reliability**: AWS handles all infrastructure
- **Scheduling**: Built-in CloudWatch Events for daily triggers
- **No Server Management**: Truly serverless
- **Auto-scaling**: Handles any load automatically

## Step 1: Create AWS Account

### 1.1 Sign Up for AWS

1. Go to: https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Enter email address and password
4. Choose "Personal" account type
5. Fill in contact information
6. **Payment Method**: Enter credit card (required, but you'll use free tier)
7. **Phone Verification**: AWS will call/text you to verify
8. **Support Plan**: Choose "Basic Support - Free"
9. Wait for account activation (can take a few minutes)

### 1.2 Sign in to AWS Console

1. Go to: https://console.aws.amazon.com/
2. Sign in with your new account
3. You'll see the AWS Management Console

## Step 2: Configure AWS for Lambda

### 2.1 Create IAM User (Security Best Practice)

1. In AWS Console, search for "IAM"
2. Click "Users" → "Create user"
3. Username: `mitzvah-bot-user`
4. Select "Programmatic access"
5. Permissions: "Attach existing policies directly"
6. Search and select: `AWSLambdaFullAccess`
7. Also add: `CloudWatchEventsFullAccess`
8. Create user
9. **IMPORTANT**: Save the Access Key ID and Secret Access Key

### 2.2 Install AWS CLI (Optional but Helpful)

```powershell
# On Windows with Chocolatey
choco install awscli

# Or download from: https://aws.amazon.com/cli/
```

## Step 3: Prepare Your Code for Lambda

### 3.1 Create Lambda-Optimized Bot

The bot needs slight modifications for Lambda environment.

### 3.2 Package Dependencies

Lambda needs all dependencies packaged together.

## Step 4: Deploy to Lambda

### 4.1 Create Lambda Function

1. In AWS Console, search for "Lambda"
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `daily-mitzvah-bot`
5. Runtime: `Python 3.11`
6. Architecture: `x86_64`
7. Create function

### 4.2 Configure Environment Variables

In your Lambda function:

1. Go to "Configuration" → "Environment variables"
2. Add these variables:
   - `TWILIO_ACCOUNT_SID`: your_twilio_sid
   - `TWILIO_AUTH_TOKEN`: your_twilio_token
   - `TWILIO_WHATSAPP_NUMBER`: +14155238886
   - `RECIPIENTS`: +16613059259
   - `TZ`: America/Chicago

### 4.3 Set Up CloudWatch Events (Scheduler)

1. In AWS Console, search for "EventBridge"
2. Click "Rules" → "Create rule"
3. Name: `daily-mitzvah-schedule`
4. Description: `Triggers mitzvah bot daily at 1:10 PM CST`
5. Event bus: `default`
6. Rule type: `Schedule`
7. Schedule pattern: `Cron expression`
8. Cron: `10 18 * * ? *` (1:10 PM CST = 6:10 PM UTC)
9. Target: Your Lambda function
10. Create rule

## Step 5: Cost Breakdown

### AWS Lambda Pricing (2025):

- **Free Tier**: 1M requests/month + 400,000 GB-seconds compute
- **Your Usage**: ~30 executions/month (daily)
- **Estimated Cost**: $0.00 (well within free tier)

### Comparison:

- **Local Computer**: $50-200/month electricity
- **Railway**: $5/month minimum
- **Lambda**: Practically free

## Step 6: Testing and Monitoring

### 6.1 Test Your Lambda

1. In Lambda console, click "Test"
2. Create test event (empty JSON: `{}`)
3. Run test to verify it works

### 6.2 Monitor Execution

1. CloudWatch Logs automatically capture output
2. Can see success/failure of each execution
3. Get email alerts if function fails

## Timezone Considerations

### UTC vs CST:

- Lambda runs in UTC time
- 1:10 PM CST = 6:10 PM UTC (standard time)
- 1:10 PM CDT = 6:10 PM UTC (daylight time)
- Cron expression: `10 18 * * ? *`

## Next Steps After This Guide:

1. Create AWS account
2. I'll help you create the Lambda-optimized code
3. I'll help you package and deploy it
4. Set up the schedule
5. Test it works

Would you like me to start with creating the Lambda-optimized version of your bot?
