@echo off
echo 🚀 Creating FIXED AWS Lambda deployment package...

REM Create deployment directory
if exist lambda_deploy rmdir /s /q lambda_deploy
mkdir lambda_deploy

echo 📦 Installing Twilio for Lambda...

REM Install twilio without user packages
python -m pip install twilio --target lambda_deploy --no-user

echo 📄 Copying FIXED bot code...

REM Copy the FIXED Lambda bot code
copy bots\lambda_mitzvah_bot_fixed.py lambda_deploy\lambda_function.py

echo 🗜️ Creating ZIP package...

REM Create ZIP using PowerShell
powershell -command "Compress-Archive -Path lambda_deploy\* -DestinationPath mitzvah_bot_lambda_FIXED.zip -Force"

echo ✅ FIXED Lambda package created: mitzvah_bot_lambda_FIXED.zip

REM Show package size
for %%I in (mitzvah_bot_lambda_FIXED.zip) do echo 📊 Package size: %%~zI bytes

echo.
echo 🔧 FIXES APPLIED:
echo - Added detailed logging at each step
echo - Moved Twilio import to module level
echo - Added timeout protection
echo - Improved error handling
echo - Added initialization logging
echo.
echo 📋 Next Steps:
echo 1. In AWS Lambda console, upload mitzvah_bot_lambda_FIXED.zip
echo 2. IMPORTANT: Increase timeout to 30 seconds:
echo    - Go to Configuration ^> General configuration
echo    - Change Timeout from 3 seconds to 30 seconds
echo    - Save changes
echo 3. Test again - should see detailed logs
echo 4. Check CloudWatch logs for detailed execution info

REM Clean up
rmdir /s /q lambda_deploy

pause