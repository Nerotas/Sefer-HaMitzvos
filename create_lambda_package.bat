@echo off
echo 🚀 Creating AWS Lambda deployment package...

REM Create deployment directory
if exist lambda_deploy rmdir /s /q lambda_deploy
mkdir lambda_deploy

echo 📦 Installing Twilio for Lambda...

REM Install twilio without user packages
python -m pip install twilio --target lambda_deploy --no-user

echo 📄 Copying bot code...

REM Copy Lambda bot code
copy bots\lambda_mitzvah_bot.py lambda_deploy\lambda_function.py

echo 🗜️ Creating ZIP package...

REM Create ZIP using PowerShell
powershell -command "Compress-Archive -Path lambda_deploy\* -DestinationPath mitzvah_bot_lambda.zip -Force"

echo ✅ Lambda package created: mitzvah_bot_lambda.zip

REM Show package size
for %%I in (mitzvah_bot_lambda.zip) do echo 📊 Package size: %%~zI bytes

echo.
echo 📋 Next Steps:
echo 1. Create AWS account at https://aws.amazon.com/
echo 2. Go to AWS Lambda console
echo 3. Create function named: daily-mitzvah-bot
echo 4. Upload mitzvah_bot_lambda.zip
echo 5. Set environment variables for Twilio credentials
echo 6. Set up CloudWatch Events for daily schedule

REM Clean up
rmdir /s /q lambda_deploy

pause