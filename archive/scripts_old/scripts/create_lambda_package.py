#!/usr/bin/env python3
"""
AWS Lambda Deployment Package Creator
Creates a deployment package for AWS Lambda with all dependencies
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path

def create_lambda_package():
    """Create a deployment package for AWS Lambda."""
    print("🚀 Creating AWS Lambda deployment package...")

    # Create deployment directory
    deploy_dir = Path("lambda_deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    print("📦 Installing dependencies...")

    # Install dependencies to deployment directory
    subprocess.run([
        "pip", "install",
        "twilio",
        "--target", str(deploy_dir),
        "--upgrade"
    ], check=True)

    # Install Twilio dependencies
    print("📦 Installing additional dependencies...")
    subprocess.run([
        "pip", "install",
        "requests",
        "--target", str(deploy_dir),
        "--upgrade"
    ], check=True)

    print("📄 Copying bot code...")

    # Copy the Lambda bot code
    shutil.copy("bots/lambda_mitzvah_bot.py", deploy_dir / "lambda_function.py")

    # Embed the CSV data in the bot
    embed_schedule_data(deploy_dir / "lambda_function.py")

    print("🗜️ Creating ZIP package...")

    # Create ZIP file
    zip_path = "mitzvah_bot_lambda.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arc_path)

    # Clean up deployment directory
    shutil.rmtree(deploy_dir)

    print(f"✅ Lambda package created: {zip_path}")
    print(f"📊 Package size: {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB")

    return zip_path

def embed_schedule_data(lambda_file):
    """Embed the CSV schedule data directly in the Lambda function."""
    print("📅 Embedding schedule data...")

    # Read the current schedule
    schedule_data = []
    try:
        import csv
        with open('Schedule_Corrected.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                schedule_data.append({
                    'Date': row['Date'].strip(),
                    'Mitzvos': row['Mitzvos'].strip(),
                    'English Title(s)': row['English Title(s)'].strip(),
                    'Source': row['Source'].strip()
                })
    except FileNotFoundError:
        print("⚠️ Schedule_Corrected.csv not found, using sample data")
        schedule_data = [
            {
                'Date': '2025-10-17',
                'Mitzvos': 'Intro 2',
                'English Title(s)': 'Shorash 1: Belief in G-d',
                'Source': 'Sefer HaMitzvos Introduction'
            }
        ]

    # Read the Lambda function code
    with open(lambda_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace the embedded schedule data
    schedule_str = "[\n"
    for item in schedule_data:
        schedule_str += "            {\n"
        schedule_str += f"                'Date': '{item['Date']}',\n"
        schedule_str += f"                'Mitzvos': '{item['Mitzvos']}',\n"
        schedule_str += f"                'English Title(s)': '{item['English Title(s)']}',\n"
        schedule_str += f"                'Source': '{item['Source']}'\n"
        schedule_str += "            },\n"
    schedule_str += "        ]"

    # Replace the sample data
    import re
    pattern = r"return \[.*?\]"
    replacement = f"return {schedule_str}"
    code = re.sub(pattern, replacement, code, flags=re.DOTALL)

    # Write back the modified code
    with open(lambda_file, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f"✅ Embedded {len(schedule_data)} schedule entries")

def print_deployment_instructions(zip_path):
    """Print instructions for deploying to AWS Lambda."""
    print("\n" + "="*60)
    print("📋 AWS LAMBDA DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print()
    print("1. 🌐 Go to AWS Lambda Console:")
    print("   https://console.aws.amazon.com/lambda/")
    print()
    print("2. 📝 Create Function:")
    print("   - Click 'Create function'")
    print("   - Choose 'Author from scratch'")
    print("   - Function name: daily-mitzvah-bot")
    print("   - Runtime: Python 3.11")
    print("   - Create function")
    print()
    print("3. 📤 Upload Code:")
    print(f"   - In the function page, click 'Upload from'")
    print(f"   - Choose '.zip file'")
    print(f"   - Upload: {zip_path}")
    print()
    print("4. ⚙️ Configure Environment Variables:")
    print("   - Go to Configuration → Environment variables")
    print("   - Add:")
    print("     TWILIO_ACCOUNT_SID: your_twilio_sid")
    print("     TWILIO_AUTH_TOKEN: your_twilio_token")
    print("     TWILIO_WHATSAPP_NUMBER: +14155238886")
    print("     RECIPIENTS: +16613059259")
    print("     TZ: America/Chicago")
    print()
    print("5. ⏰ Set Up Schedule:")
    print("   - Go to EventBridge console")
    print("   - Create rule: daily-mitzvah-schedule")
    print("   - Cron expression: 10 18 * * ? *")
    print("   - Target: Your Lambda function")
    print()
    print("6. 🧪 Test:")
    print("   - In Lambda console, click 'Test'")
    print("   - Create test event: {}")
    print("   - Run test to verify")
    print()
    print("💰 Expected Cost: ~$0.00/month (free tier)")
    print("📊 Execution: Once daily at 1:10 PM CST")

if __name__ == "__main__":
    try:
        zip_path = create_lambda_package()
        print_deployment_instructions(zip_path)
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        print("Make sure you have pip and all dependencies installed.")