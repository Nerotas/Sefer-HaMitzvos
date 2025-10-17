# AWS Account Setup Checklist

## ✅ Phase 1: Create AWS Account (15 minutes)

### Step 1: Sign Up

- [ ] Go to https://aws.amazon.com/
- [ ] Click "Create an AWS Account"
- [ ] Enter email and password
- [ ] Choose account name: `mitzvah-bot-aws`

### Step 2: Account Information

- [ ] Select "Personal" account type
- [ ] Fill in your contact information
- [ ] Enter phone number for verification

### Step 3: Payment Method

- [ ] Add credit card (required for verification)
- [ ] Note: You'll use free tier, charges will be ~$0

### Step 4: Identity Verification

- [ ] AWS will call/text you with verification code
- [ ] Enter the code when prompted

### Step 5: Support Plan

- [ ] Select "Basic Support - Free"
- [ ] Complete registration

### Step 6: Wait for Activation

- [ ] Account activation can take 5-10 minutes
- [ ] You'll get email confirmation when ready

## ✅ Phase 2: Prepare for Lambda (10 minutes)

### Step 1: Access Console

- [ ] Go to https://console.aws.amazon.com/
- [ ] Sign in with your new account
- [ ] Familiarize yourself with the interface

### Step 2: Create Deployment Package

- [ ] Run: `python scripts/create_lambda_package.py`
- [ ] This creates `mitzvah_bot_lambda.zip`
- [ ] Verify the ZIP file was created (~2-5 MB)

### Step 3: Gather Information

- [ ] Have your Twilio credentials ready:
  - [ ] TWILIO_ACCOUNT_SID: ACacbcea137ed0e7f090a4a31ea44cfd25
  - [ ] TWILIO_AUTH_TOKEN: bf2a52bbb93f15dec99777f07809377c
  - [ ] RECIPIENTS: +16613059259

## ✅ Phase 3: Deploy to Lambda (20 minutes)

### Step 1: Create Lambda Function

- [ ] In AWS Console, search "Lambda"
- [ ] Click "Create function"
- [ ] Function name: `daily-mitzvah-bot`
- [ ] Runtime: `Python 3.11`
- [ ] Create function

### Step 2: Upload Code

- [ ] Click "Upload from" → ".zip file"
- [ ] Upload your `mitzvah_bot_lambda.zip`
- [ ] Wait for upload to complete

### Step 3: Configure Environment Variables

- [ ] Go to Configuration → Environment variables
- [ ] Add all Twilio variables (see Phase 2, Step 3)
- [ ] Save configuration

### Step 4: Test Function

- [ ] Click "Test" button
- [ ] Create test event: `{}`
- [ ] Run test
- [ ] Verify success in logs

## ✅ Phase 4: Set Up Daily Schedule (10 minutes)

### Step 1: Create EventBridge Rule

- [ ] Search "EventBridge" in AWS Console
- [ ] Go to Rules → Create rule
- [ ] Name: `daily-mitzvah-schedule`
- [ ] Description: `Daily mitzvah at 1:10 PM CST`

### Step 2: Configure Schedule

- [ ] Event pattern: Schedule
- [ ] Schedule expression: `cron(10 18 * * ? *)`
- [ ] This runs at 6:10 PM UTC = 1:10 PM CST

### Step 3: Set Target

- [ ] Target type: AWS service
- [ ] Select: Lambda function
- [ ] Function: `daily-mitzvah-bot`
- [ ] Create rule

## ✅ Phase 5: Monitor and Verify (5 minutes)

### Step 1: Check CloudWatch Logs

- [ ] Go to CloudWatch → Log groups
- [ ] Find `/aws/lambda/daily-mitzvah-bot`
- [ ] Verify logs appear after test runs

### Step 2: Set Up Alerts (Optional)

- [ ] Create CloudWatch alarm for function errors
- [ ] Get email if function fails

### Step 3: Final Test

- [ ] Wait for scheduled time (1:10 PM CST)
- [ ] Check if message is received
- [ ] Verify in CloudWatch logs

## 💰 Cost Estimate

- **Setup**: Free
- **Monthly**: ~$0.00 (within free tier)
- **Per execution**: ~$0.0000002
- **Total annual cost**: Under $1

## 🆘 Troubleshooting

- Function fails? Check CloudWatch logs
- No message received? Verify Twilio sandbox setup
- Wrong time? Check timezone configuration
- Need help? Check AWS documentation or ask for assistance

## 🎯 Success Criteria

- [ ] Lambda function deploys successfully
- [ ] Test execution works
- [ ] Daily schedule is configured
- [ ] You receive daily mitzvah messages
- [ ] CloudWatch logs show successful executions

**Estimated Total Time**: 60 minutes
**Difficulty Level**: Beginner-friendly with step-by-step instructions
