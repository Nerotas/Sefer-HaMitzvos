#!/bin/bash

# WhatsApp Mitzvah Bot - Heroku Deployment Script
# Run this script to deploy your bot to Heroku

echo "🕊️ Deploying WhatsApp Mitzvah Bot to Heroku 🚀"
echo "=================================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - WhatsApp Mitzvah Bot"
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Get app name
read -p "📝 Enter your Heroku app name (e.g., my-mitzvah-bot): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name cannot be empty"
    exit 1
fi

# Create Heroku app
echo "🆕 Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

if [ $? -ne 0 ]; then
    echo "❌ Failed to create app. It might already exist."
    echo "🔄 Trying to add existing app..."
    heroku git:remote -a $APP_NAME
fi

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "You'll need your Twilio credentials from: https://console.twilio.com/"
echo

read -p "📱 Enter your TWILIO_ACCOUNT_SID: " ACCOUNT_SID
read -p "🔑 Enter your TWILIO_AUTH_TOKEN: " AUTH_TOKEN
read -p "📞 Enter your TWILIO_WHATSAPP_NUMBER (default: +14155238886): " WHATSAPP_NUMBER

# Use default if empty
if [ -z "$WHATSAPP_NUMBER" ]; then
    WHATSAPP_NUMBER="+14155238886"
fi

# Set environment variables on Heroku
heroku config:set TWILIO_ACCOUNT_SID="$ACCOUNT_SID" -a $APP_NAME
heroku config:set TWILIO_AUTH_TOKEN="$AUTH_TOKEN" -a $APP_NAME
heroku config:set TWILIO_WHATSAPP_NUMBER="$WHATSAPP_NUMBER" -a $APP_NAME

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy WhatsApp Mitzvah Bot" || echo "No changes to commit"
git push heroku main

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"

    # Scale the worker
    echo "⚡ Starting the bot worker..."
    heroku ps:scale worker=1 -a $APP_NAME

    echo "🎉 Your WhatsApp Mitzvah Bot is now running on Heroku!"
    echo "📊 Check logs with: heroku logs --tail -a $APP_NAME"
    echo "🛑 Stop the bot with: heroku ps:scale worker=0 -a $APP_NAME"
    echo "🔄 Restart the bot with: heroku restart -a $APP_NAME"
    echo
    echo "📱 Your bot will send daily messages at 8:00 AM UTC"
    echo "⚙️ To change recipients, edit the code and redeploy"

else
    echo "❌ Deployment failed. Check the errors above."
    exit 1
fi