# GitHub Actions Auto-Deployment Setup

This repository is configured for automatic deployment to AWS Lambda using GitHub Actions.

## Setup Instructions

### 1. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add these secrets:

#### AWS Credentials

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_REGION`: Your AWS region (e.g., `us-east-1`)
- `LAMBDA_FUNCTION_NAME`: Your Lambda function name (e.g., `daily-mitzvah-bot`)

#### Twilio Credentials

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_WHATSAPP_NUMBER`: Your Twilio WhatsApp number (e.g., `+14155238886`)

#### Bot Configuration

- `RECIPIENTS`: Comma-separated list of WhatsApp numbers (e.g., `+1234567890,+0987654321`)

### 2. Create AWS IAM User for GitHub Actions

Create an IAM user with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:InvokeFunction",
        "lambda:GetFunction"
      ],
      "Resource": "arn:aws:lambda:*:*:function:daily-mitzvah-bot"
    }
  ]
}
```

### 3. How It Works

The workflow automatically triggers when:

- ✅ Code is pushed to the `main` branch
- ✅ Changes are made to `bots/lambda_mitzvah_bot.py`
- ✅ Changes are made to `Schedule.csv`
- ✅ Pull requests are opened targeting main branch

### 4. Deployment Process

1. **Build**: Creates a fresh Lambda package with latest code
2. **Deploy**: Updates your Lambda function with new code
3. **Configure**: Updates environment variables and timeout settings
4. **Test**: Invokes the function to verify deployment

### 5. Alternative: Manual Deployment

If you prefer manual deployment, you can still use:

```bash
.\create_lambda_package.bat
```

Then upload `mitzvah_bot_lambda.zip` manually to AWS Lambda.

## Troubleshooting

### Failed Deployment

- Check GitHub Actions logs for specific error messages
- Verify all secrets are correctly configured
- Ensure AWS IAM permissions are properly set

### Lambda Function Not Found

- Make sure `LAMBDA_FUNCTION_NAME` secret matches your actual function name
- Verify the function exists in the specified AWS region

### Environment Variables

- The workflow automatically updates environment variables
- Manual changes in AWS console may be overwritten

## Security Best Practices

- ✅ Use GitHub Secrets for all sensitive information
- ✅ Follow principle of least privilege for IAM permissions
- ✅ Regularly rotate AWS access keys
- ✅ Monitor CloudWatch logs for any issues
