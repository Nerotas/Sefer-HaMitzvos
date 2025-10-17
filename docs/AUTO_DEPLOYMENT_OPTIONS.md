# Auto-Deployment Options for Lambda Function

## 🚀 Overview

You now have **3 deployment options** for your Daily Mitzvah Bot:

## Option 1: GitHub Actions + AWS CLI (Recommended)

**File**: `.github/workflows/deploy-lambda.yml`

### ✅ Pros:

- Simple and straightforward
- Full control over deployment process
- Works with existing Lambda function
- Minimal setup required

### ❌ Cons:

- Manual IAM setup required
- Need to manage function configuration separately

### 🔧 Setup Steps:

1. Add GitHub secrets (see `GITHUB_ACTIONS_DEPLOYMENT.md`)
2. Create IAM user with Lambda permissions
3. Push code to trigger deployment

---

## Option 2: AWS SAM (Serverless Application Model)

**Files**: `template.yaml` + `.github/workflows/deploy-sam.yml`

### ✅ Pros:

- Infrastructure as Code (IaC)
- Automatic scheduling setup (CloudWatch Events)
- Proper resource management
- Built-in logging configuration
- Professional DevOps approach

### ❌ Cons:

- More complex initial setup
- Learning curve for SAM/CloudFormation
- May recreate existing resources

### 🔧 Setup Steps:

1. Install AWS SAM CLI locally (optional)
2. Add same GitHub secrets
3. Enable the SAM workflow (disable the other one)

---

## Option 3: Manual Deployment (Current)

**File**: `create_lambda_package.bat`

### ✅ Pros:

- Full manual control
- No additional setup required
- Good for testing

### ❌ Cons:

- Manual process every time
- Risk of forgetting to deploy
- No automation

---

## 🎯 Recommendation

For your use case, I recommend **Option 1: GitHub Actions + AWS CLI** because:

1. **Simple Setup**: Works with your existing Lambda function
2. **Proven Approach**: Most commonly used in the industry
3. **Immediate Benefits**: Auto-deploy on every push to main
4. **Low Risk**: Doesn't change your existing AWS setup

## 🛠️ Next Steps

### To Enable Auto-Deployment:

1. **Configure GitHub Secrets** (takes 5 minutes):

   ```
   AWS_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY
   AWS_REGION
   LAMBDA_FUNCTION_NAME
   TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN
   TWILIO_WHATSAPP_NUMBER
   RECIPIENTS
   ```

2. **Create AWS IAM User** with Lambda permissions

3. **Push code to main branch** → Automatic deployment! 🎉

### Example Workflow:

```bash
# Make changes to lambda_mitzvah_bot.py
git add .
git commit -m "Updated message format"
git push origin main
# → GitHub Actions automatically deploys to Lambda
```

## 🔍 Monitoring

After setup, you can:

- View deployment status in GitHub Actions tab
- Monitor function logs in AWS CloudWatch
- Get notifications on deployment failures

Would you like me to help you set up the GitHub secrets and IAM user?
