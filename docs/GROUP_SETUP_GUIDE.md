# 👥 Adding Your Mitzvah Bot to WhatsApp Groups

## 🎯 **Overview**

Your WhatsApp Mitzvah Bot can send daily messages to WhatsApp groups, making it perfect for:

- Study groups and chavrutas
- Synagogue communities
- Family Torah study
- Online learning communities

## 🔧 **Setup Methods**

### **Method 1: Group Admin Adds Bot Number (Recommended)**

**Steps for Group Admin:**

1. **Get the Bot's WhatsApp Number**:

   - **Sandbox**: `+1 415 523 8886` (Twilio's number)
   - **Production**: Your approved WhatsApp Business number

2. **Add to Group**:

   - Open your WhatsApp group
   - Tap group name → "Add participants"
   - Add the bot's phone number
   - The bot will appear as a group member

3. **Configure Bot Recipients**:
   - Get the **Group Chat ID** (see instructions below)
   - Add Group ID to Railway environment variables

### **Method 2: Bot Joins via Group Invite Link**

**If you have group admin access:**

1. **Create Group Invite Link**:

   - Open WhatsApp group
   - Tap group name → "Invite to group via link"
   - Copy the invite link

2. **Program Bot to Join** (requires custom code modification)

---

## 🆔 **Getting WhatsApp Group ID**

### **Method 1: Using Twilio Console (Easiest)**

1. **Send test message to group**:

   - Go to Twilio Console → Messaging → Try it out
   - Send message to the group using bot number
   - Check message logs in Twilio Console

2. **Find Group ID in logs**:
   - Group IDs look like: `120363XXXXXXXXXX@g.us`
   - Individual numbers look like: `+1234567890`

### **Method 2: WhatsApp Web Developer Tools**

1. **Open WhatsApp Web**: https://web.whatsapp.com
2. **Open group chat**
3. **Press F12** (Developer Tools)
4. **Console tab** → Type:
   ```javascript
   Store.Chat.getActive().id._serialized;
   ```
5. **Copy the Group ID** (format: `120363XXXXXXXXXX@g.us`)

### **Method 3: Using Python Script**

```python
# Add this to your bot for one-time group ID discovery
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Send a message and capture the response
message = client.messages.create(
    body='Getting group ID...',
    from_='whatsapp:+14155238886',
    to='whatsapp:+1234567890'  # Send to yourself first
)

print(f"Message SID: {message.sid}")
# Check Twilio logs for the actual group ID format
```

---

## ⚙️ **Configuring Bot for Groups**

### **Update Railway Environment Variables**

Instead of individual phone numbers, use group IDs:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_32_character_token
TWILIO_WHATSAPP_NUMBER=+14155238886
RECIPIENTS=120363XXXXXXXXXX@g.us,120363YYYYYYYYYY@g.us
DEPLOY_MODE=scheduler
```

### **Mixed Recipients (Individuals + Groups)**

You can send to both individuals and groups:

```env
RECIPIENTS=+1234567890,120363XXXXXXXXXX@g.us,+9876543210
```

**Format Rules:**

- ✅ **Individual**: `+1234567890`
- ✅ **Group**: `120363XXXXXXXXXX@g.us`
- ✅ **Multiple**: Comma-separated, no spaces

---

## 🔄 **Bot Code Compatibility**

✅ **Good News!** Your current bot (`bots/mitzvah_bot_cloud.py`) already supports groups automatically!

The `send_to_recipient` method works with both:

- **Individual numbers**: `+1234567890`
- **Group IDs**: `120363XXXXXXXXXX@g.us`

**No code changes needed!** Just add the group IDs to your `RECIPIENTS` environment variable.

---

## 📱 **Group Setup Walkthrough**

### **Step 1: Prepare Your WhatsApp Group**

1. **Create or use existing group**
2. **Make sure you're an admin** (to add the bot)
3. **Inform group members** about the daily mitzvah messages

### **Step 2: Add Bot to Group**

**Using Twilio Sandbox:**

1. **All group members must join sandbox first**:
   - Send `join [code]` to `+1 415 523 8886`
   - Each person gets their own join code
2. **Group admin adds** `+1 415 523 8886` to the group

**Using Production WhatsApp Business:**

1. **Simply add your bot's number** to the group
2. **No sandbox setup required**

### **Step 3: Get Group ID**

**Easiest Method - Send Test Message:**

1. **Go to Twilio Console** → Messaging → Try it out
2. **Send test message**:
   - From: `+14155238886`
   - To: `+1234567890` (your number in the group)
3. **Check Twilio logs** for the actual group format used

### **Step 4: Update Railway Configuration**

1. **Go to Railway project** → Variables
2. **Update RECIPIENTS**:
   ```env
   RECIPIENTS=120363XXXXXXXXXX@g.us
   ```
3. **Deploy changes**

---

## 🎯 **Testing Your Group Setup**

### **Test Message Process:**

1. **Set test mode**:

   ```env
   DEPLOY_MODE=test
   RECIPIENTS=120363XXXXXXXXXX@g.us
   ```

2. **Deploy and check**:

   - Group should receive one test message
   - Verify formatting looks good in group chat
   - Check Railway logs for success

3. **Switch to production**:
   ```env
   DEPLOY_MODE=scheduler
   ```

### **Expected Group Message:**

```
🕊️ Sefer HaMitzvos Daily Study 📚

📅 Friday, October 11, 2025

🔢 Mitzvah #1
_To believe that God exists and is the source of all existence_

📚 Source: Devarim 6:4

Fulfill this mitzvah with joy and intention! 💫🙏

—Daily Mitzvah Bot
```

---

## ⚠️ **Important Considerations**

### **Sandbox Limitations:**

- ✅ **Free testing**
- ❌ **All recipients must join sandbox individually**
- ❌ **Limited to verified numbers**

### **Production Benefits:**

- ✅ **Send to any group member**
- ✅ **No sandbox joining required**
- ✅ **Professional appearance**
- 💰 **~$0.005 per message**

### **Group Etiquette:**

- 📢 **Announce bot addition** to group members
- ⏰ **Inform about daily message timing** (8 AM UTC)
- 🚫 **Provide opt-out instructions** if needed
- 📋 **Consider creating dedicated study groups**

---

## 🔧 **Troubleshooting Groups**

| Issue                          | Solution                                                  |
| ------------------------------ | --------------------------------------------------------- |
| "Group not receiving messages" | Verify group ID format: `120363XXXXXXXXXX@g.us`           |
| "Bot not in group"             | Check if bot number was successfully added as participant |
| "Sandbox errors"               | Ensure all group members joined sandbox individually      |
| "Permission denied"            | Verify you're group admin to add bot number               |
| "Wrong group ID"               | Use Twilio Console logs to get correct group format       |

### **Getting Help:**

1. **Check Railway logs** for specific error messages
2. **Verify group ID** in Twilio Console message logs
3. **Test with individual numbers first** before groups
4. **Use `DEPLOY_MODE=test`** for debugging

---

## 🎊 **Success Checklist**

- [ ] Bot added to WhatsApp group successfully
- [ ] Group ID obtained and formatted correctly
- [ ] Railway environment variables updated
- [ ] Test message sent and received in group
- [ ] Daily scheduler activated (`DEPLOY_MODE=scheduler`)
- [ ] Group members informed about daily messages

**Your group is now ready for daily Torah study! 🕊️📚**

---

## 💡 **Pro Tips**

### **Multiple Groups:**

```env
RECIPIENTS=120363GROUP1@g.us,120363GROUP2@g.us,+1234567890
```

### **Dedicated Study Groups:**

- Create separate groups for different learning levels
- Use descriptive group names: "Daily Sefer HaMitzvos Study"
- Pin the group description explaining the bot's purpose

### **Engagement Ideas:**

- Encourage group discussion about each mitzvah
- Share additional Torah sources related to daily mitzvah
- Create study partnerships within the group

**May your group Torah study flourish! ✨📖👥**
