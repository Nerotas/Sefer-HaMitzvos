@echo off
echo 🚀 Creating AWS Lambda deployment package...

REM Create deployment directory
if exist lambda_deploy rmdir /s /q lambda_deploy
mkdir lambda_deploy

echo 📦 Installing Twilio for Lambda...

REM Install twilio without user packages
python -m pip install twilio --target lambda_deploy --no-user

echo 📄 Copying Lambda bot code and data...

REM Copy the Lambda bot code
copy bots\lambda_mitzvah_bot.py lambda_deploy\lambda_function.py

REM Copy the complete CSV schedule for external data loading (optional - bot has embedded data)
copy Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv lambda_deploy\Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv

echo 🗜️ Creating ZIP package...

REM Create ZIP using PowerShell
powershell -command "Compress-Archive -Path lambda_deploy\* -DestinationPath mitzvah_bot_lambda.zip -Force"

echo ✅ Lambda package created: mitzvah_bot_lambda.zip

REM Show package size
for %%I in (mitzvah_bot_lambda.zip) do echo 📊 Package size: %%~zI bytes

echo.
echo 🔧 FEATURES INCLUDED:
echo - TEST MODE: Supports specific date testing via event['test_date']
echo - Complete 630-entry schedule with biblical sources
echo - Detailed logging at each step
echo - Module-level Twilio imports for performance
echo - Timeout protection and error handling
echo - Holiday consolidation logic
echo - Enhanced CSV data loading with biblical sources
echo - AWS Lambda optimized code
echo.
echo 📋 Next Steps:
echo 1. In AWS Lambda console, upload mitzvah_bot_lambda.zip
echo 2. IMPORTANT: Increase timeout to 30 seconds:
echo    - Go to Configuration ^> General configuration
echo    - Change Timeout from 3 seconds to 30 seconds
echo    - Save changes
echo 3. Set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, RECIPIENTS
echo 4. Test with specific date using event: {"test_date": "2025-11-02"}
echo 5. Test normal operation without test_date
echo 6. Set up daily scheduling with CloudWatch Events
echo.
echo 🧪 LOCAL TESTING AVAILABLE:
echo - Run: python simple_test_bot.py 2025-11-02
echo - Interactive: python simple_test_bot.py
echo - See LAMBDA_TESTING_GUIDE.md for details
echo.
echo 📁 DEVELOPMENT FILES (not in Lambda package):
echo - simple_test_bot.py: Local testing utility
echo - comprehensive_mitzvah_analysis.py: Source verification analysis
echo - source_correction_plan.py: Planned corrections
echo - LAMBDA_TESTING_GUIDE.md: Complete testing documentation
echo - lambda_test_event_*.json: Generated AWS test events

REM Clean up
rmdir /s /q lambda_deploy

echo Script completed successfully!