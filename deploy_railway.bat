@echo off
REM Quick Railway Deployment Script for WhatsApp Mitzvah Bot

echo 🚀 Setting up WhatsApp Mitzvah Bot for Railway deployment...

REM Check if git is initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    git branch -M main
)

REM Add all files
echo Adding files to git...
git add .

REM Check if there are changes to commit
git diff --staged --quiet
if %ERRORLEVEL% neq 0 (
    echo Committing changes...
    git commit -m "Deploy WhatsApp Mitzvah Bot to Railway"
) else (
    echo No changes to commit.
)

echo ✅ Repository ready for Railway deployment!
echo.
echo Next steps:
echo 1. Create repository on GitHub:
echo    - Go to https://github.com/new
echo    - Create repository named 'mitzvah-bot'
echo    - Copy the remote URL
echo.
echo 2. Push to GitHub:
echo    git remote add origin https://github.com/YOURUSERNAME/mitzvah-bot.git
echo    git push -u origin main
echo.
echo 3. Deploy on Railway:
echo    - Go to https://railway.app
echo    - Sign up with GitHub
echo    - Click 'Deploy from GitHub repo'
echo    - Select your mitzvah-bot repository
echo.
echo 4. Set Environment Variables in Railway Dashboard:
echo    TWILIO_ACCOUNT_SID=your_account_sid
echo    TWILIO_AUTH_TOKEN=your_auth_token
echo    RECIPIENTS=+1234567890,+9876543210
echo    DEPLOY_MODE=scheduler
echo.
echo 🎯 Recommended: Start with DEPLOY_MODE=test to verify setup!
echo 📚 Full guide: See CLOUD_DEPLOYMENT_COMPLETE.md

pause