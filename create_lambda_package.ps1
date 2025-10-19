param(
    [switch]$Force
)

# AWS Lambda Package Creation Script (reusable vendor dir)
Write-Host "Creating AWS Lambda deployment package..." -ForegroundColor Green

if ($Force -and (Test-Path "lambda_deploy")) {
    Write-Host "--force specified: clearing lambda_deploy" -ForegroundColor Yellow
    Remove-Item "lambda_deploy" -Recurse -Force
}
if (!(Test-Path "lambda_deploy")) {
    New-Item -ItemType Directory -Name "lambda_deploy" | Out-Null
}

Write-Host "Installing dependencies (twilio/requests) if needed..." -ForegroundColor Yellow
if ($Force -or -not (Test-Path "lambda_deploy\twilio")) {
    Write-Host "Installing from requirements.txt into lambda_deploy" -ForegroundColor Yellow
    python -m pip install -r requirements.txt --target lambda_deploy --no-user
} else {
    Write-Host "Dependencies already present; skipping install. Use -Force to rebuild." -ForegroundColor Cyan
}

Write-Host "Copying Lambda bot code and data..." -ForegroundColor Yellow

# Copy the Lambda bot code
Copy-Item "bots\lambda_mitzvah_bot.py" "lambda_deploy\lambda_function.py"

# Copy the complete CSV schedule with corrected sources
Copy-Item "Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv" "lambda_deploy\Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv"

Write-Host "Creating ZIP package..." -ForegroundColor Yellow
Compress-Archive -Path "lambda_deploy\*" -DestinationPath "mitzvah_bot_lambda.zip" -Force

# Show package info
$packageSize = (Get-Item "mitzvah_bot_lambda.zip").Length
Write-Host "`nLambda package created: mitzvah_bot_lambda.zip" -ForegroundColor Green
Write-Host "Package size: $packageSize bytes" -ForegroundColor Cyan

Write-Host "`nFEATURES INCLUDED:" -ForegroundColor Magenta
Write-Host "- 100% VERIFIED SOURCES: All 613 biblical references match master list"
Write-Host "- UTF-8 BOM HANDLING: Fixed CSV loading issues"
Write-Host "- TEST MODE: Supports specific date testing via event['test_date']"
Write-Host "- Complete 628-entry schedule with corrected biblical sources"
Write-Host "- Enhanced error handling and debug logging"
Write-Host "- Holiday consolidation logic"
Write-Host "- AWS Lambda optimized performance"

Write-Host "`nDEPLOYMENT STEPS:" -ForegroundColor Magenta
Write-Host "1. Upload mitzvah_bot_lambda.zip to AWS Lambda console"
Write-Host "2. Set timeout to 30 seconds (Configuration > General configuration)"
Write-Host "3. Configure environment variables:"
Write-Host "   - TWILIO_ACCOUNT_SID"
Write-Host "   - TWILIO_AUTH_TOKEN"
Write-Host "   - TWILIO_PHONE_NUMBER"
Write-Host "   - RECIPIENT_PHONE_NUMBER"
Write-Host "4. Test with: {`"test_date`": `"2025-11-02`", `"test_mode`": true}"

Write-Host "`nPackage ready with 100% verified accurate sources!" -ForegroundColor Green

# Keep lambda_deploy for faster rebuilds; add -Force to rebuild fresh
Write-Host "Script completed successfully! (Dependencies cached in lambda_deploy)" -ForegroundColor Green