@echo off
REM WhatsApp Mitzvah Bot - Heroku Deployment Script (Windows)
REM Run this script to deploy your bot to Heroku

echo 🕊️ Deploying WhatsApp Mitzvah Bot to Heroku 🚀
echo ==================================================

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI not found. Please install it first:
    echo    https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - WhatsApp Mitzvah Bot"
)

REM Login to Heroku
echo 🔐 Logging into Heroku...
heroku login

REM Get app name
set /p APP_NAME="📝 Enter your Heroku app name (e.g., my-mitzvah-bot): "

if "%APP_NAME%"=="" (
    echo ❌ App name cannot be empty
    pause
    exit /b 1
)

REM Create Heroku app
echo 🆕 Creating Heroku app: %APP_NAME%
heroku create %APP_NAME%

if errorlevel 1 (
    echo ❌ Failed to create app. It might already exist.
    echo 🔄 Trying to add existing app...
    heroku git:remote -a %APP_NAME%
)

REM Set environment variables
echo 🔧 Setting up environment variables...
echo You'll need your Twilio credentials from: https://console.twilio.com/
echo.

set /p ACCOUNT_SID="📱 Enter your TWILIO_ACCOUNT_SID: "
set /p AUTH_TOKEN="🔑 Enter your TWILIO_AUTH_TOKEN: "
set /p WHATSAPP_NUMBER="📞 Enter your TWILIO_WHATSAPP_NUMBER (default: +14155238886): "

REM Use default if empty
if "%WHATSAPP_NUMBER%"=="" set WHATSAPP_NUMBER=+14155238886

REM Set environment variables on Heroku
heroku config:set TWILIO_ACCOUNT_SID=%ACCOUNT_SID% -a %APP_NAME%
heroku config:set TWILIO_AUTH_TOKEN=%AUTH_TOKEN% -a %APP_NAME%
heroku config:set TWILIO_WHATSAPP_NUMBER=%WHATSAPP_NUMBER% -a %APP_NAME%

REM Deploy
echo 🚀 Deploying to Heroku...
git add .
git commit -m "Deploy WhatsApp Mitzvah Bot"
git push heroku main

if not errorlevel 1 (
    echo ✅ Deployment successful!

    REM Scale the worker
    echo ⚡ Starting the bot worker...
    heroku ps:scale worker=1 -a %APP_NAME%

    echo 🎉 Your WhatsApp Mitzvah Bot is now running on Heroku!
    echo 📊 Check logs with: heroku logs --tail -a %APP_NAME%
    echo 🛑 Stop the bot with: heroku ps:scale worker=0 -a %APP_NAME%
    echo 🔄 Restart the bot with: heroku restart -a %APP_NAME%
    echo.
    echo 📱 Your bot will send daily messages at 8:00 AM UTC
    echo ⚙️ To change recipients, edit the code and redeploy
) else (
    echo ❌ Deployment failed. Check the errors above.
)

pause