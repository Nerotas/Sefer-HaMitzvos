@echo off
echo 🚀 Creating AWS Lambda deployment package...

REM Create deployment directory
if exist lambda_deploy rmdir /s /q lambda_deploy
mkdir lambda_deploy

echo 📦 Installing Twilio for Lambda...

REM Install twilio without user packages
python -m pip install twilio --target lambda_deploy --no-user

echo 📄 Copying Lambda bot code...

REM Copy the Lambda bot code
copy bots\lambda_mitzvah_bot.py lambda_deploy\lambda_function.py

echo 🗜️ Creating ZIP package...

REM Create ZIP using PowerShell
powershell -command "Compress-Archive -Path lambda_deploy\* -DestinationPath mitzvah_bot_lambda.zip -Force"

echo ✅ Lambda package created: mitzvah_bot_lambda.zip

REM Show package size
for %%I in (mitzvah_bot_lambda.zip) do echo 📊 Package size: %%~zI bytes

echo.
echo 🔧 FEATURES INCLUDED:
echo - Detailed logging at each step
echo - Module-level Twilio imports for performance
echo - Timeout protection and error handling
echo - Embedded 354-day schedule
echo - AWS Lambda optimized code
echo.
echo 📋 Next Steps:
echo 1. In AWS Lambda console, upload mitzvah_bot_lambda.zip
echo 2. IMPORTANT: Increase timeout to 30 seconds:
echo    - Go to Configuration ^> General configuration
echo    - Change Timeout from 3 seconds to 30 seconds
echo    - Save changes
echo 3. Test the function - should see detailed logs
echo 4. Set up daily scheduling with CloudWatch Events

REM Clean up
rmdir /s /q lambda_deploy

pause