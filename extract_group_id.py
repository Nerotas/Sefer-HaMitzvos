#!/usr/bin/env python3
"""
WhatsApp Group ID Extractor and Configuration Helper
Extracts group ID from invite link and provides Railway configuration
"""

import re

def extract_group_id_from_link(invite_link):
    """Extract WhatsApp group ID from invite link."""
    # WhatsApp invite links format: https://chat.whatsapp.com/GROUPCODE
    pattern = r'https://chat\.whatsapp\.com/([A-Za-z0-9]+)'
    match = re.search(pattern, invite_link)

    if match:
        group_code = match.group(1)
        # Convert to proper WhatsApp group ID format
        # Note: The actual format may vary, this is the most common
        group_id = f"{group_code}@g.us"
        return group_code, group_id
    return None, None

def main():
    # Your group invite link
    invite_link = "https://chat.whatsapp.com/JpwWqLb9Dv0K8KUQsX3KcO?mode=wwt"

    print("🕊️ WhatsApp Mitzvah Bot - Group Configuration")
    print("=" * 50)
    print(f"Group Invite Link: {invite_link}")
    print()

    # Extract group information
    group_code, group_id = extract_group_id_from_link(invite_link)

    if group_code:
        print("✅ Group Information Extracted:")
        print(f"   Group Code: {group_code}")
        print(f"   Estimated Group ID: {group_id}")
        print()

        print("🚀 Railway Environment Variables:")
        print("   Add these to your Railway project variables:")
        print()
        print("   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx")
        print("   TWILIO_AUTH_TOKEN=your_32_character_token")
        print("   TWILIO_WHATSAPP_NUMBER=+14155238886")
        print(f"   RECIPIENTS={group_id}")
        print("   DEPLOY_MODE=test")
        print()

        print("⚠️  IMPORTANT STEPS:")
        print("1. 🤖 Add bot to group first:")
        print(f"   - Open the group: {invite_link}")
        print("   - Add participant: +1 415 523 8886 (Twilio sandbox)")
        print("   - OR use your WhatsApp Business number if approved")
        print()
        print("2. 👥 Group members must join Twilio sandbox:")
        print("   - Send 'join [code]' to +1 415 523 8886")
        print("   - Each member gets their own join code from Twilio Console")
        print()
        print("3. ✅ Verify Group ID:")
        print("   - Send test message via Twilio Console to the group")
        print("   - Check Twilio logs for actual Group ID format")
        print("   - Group IDs may look like: 120363XXXXXXXXXX@g.us")
        print()
        print("4. 🧪 Test Configuration:")
        print("   - Use DEPLOY_MODE=test first")
        print("   - Verify message appears in group")
        print("   - Switch to DEPLOY_MODE=scheduler for daily messages")
        print()

        print("📋 Alternative Group ID Formats to Try:")
        print(f"   Option 1: {group_id}")
        print(f"   Option 2: 120363{group_code}@g.us")
        print(f"   Option 3: {group_code}@c.us")
        print()
        print("💡 Pro Tip: The exact format will be visible in Twilio Console logs")
        print("   after sending the first test message to the group!")

    else:
        print("❌ Could not extract group code from invite link")
        print("   Please check the link format")

if __name__ == "__main__":
    main()