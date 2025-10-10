# 📱 How to Get Your Twilio Credentials for WhatsApp Bot

## 🚀 **Step-by-Step Twilio Setup**

### **Step 1: Create Your Free Twilio Account**

1. **Go to Twilio**: https://www.twilio.com/try-twilio
2. **Click "Start your free trial"**
3. **Fill out the form**:
   - First Name, Last Name
   - Email address
   - Password
   - Phone number (for verification)
4. **Verify your phone number** via SMS or call
5. **Complete the "Tell us about your project" questions**:
   - Choose: "Alerts & Notifications"
   - Choose: "With my customers"
   - Choose: "Python" as programming language

---

### **Step 2: Get Your Account SID and Auth Token**

**Method 1: From Console Dashboard (2024+ Interface)**
1. **After logging in**, look for a section called **"Account Info"** or **"API Keys & Tokens"**
2. **If not visible on main page**: Click your **Profile Icon** (top right) → **"API keys & tokens"**
3. **Alternative**: Go to **Console → Account → API keys & tokens**

**Method 2: Direct URL**
1. **Go directly to**: https://console.twilio.com/us1/account/keys-credentials/api-keys
2. **You'll see**:
   - **Account SID**: Starts with `AC...` (always visible)
   - **Auth Token**: Shows as dots `••••••••••••••••••••••••••••••••`
   - **Click "Show"** or **"Reveal"** button next to the Auth Token

**Method 3: Create New Auth Token (if needed)**
1. **If you can't find the Auth Token**: Click **"Create API Key"** or **"Reset Auth Token"**
2. **Copy the new token immediately** (it won't be shown again)

**What you're looking for:**
```
Account SID: ACf1234567890abcdef1234567890abcdef (34 characters total)
Auth Token: abc123def456ghi789jkl012mno345pqr (32 characters total)
```

### **Step 3: Set Up WhatsApp Sandbox (Free Testing)**

1. **Navigate to**: Console → Develop → Messaging → Try it out → Send a WhatsApp message
2. **Sandbox Settings**:
   - **From Number**: `+1 415 523 8886` (Twilio's sandbox number)
   - **To Number**: Your phone number in international format (e.g., `+1234567890`)
3. **Join the Sandbox**:
   - Send a WhatsApp message to `+1 415 523 8886`
   - Message content: `join <your-sandbox-code>` (Twilio will show you the exact code)
   - Example: `join bicycle-lamp` or `join purple-dog`

---

### **Step 4: Test Your Setup**

After joining the sandbox, test with this simple message:

1. **Go to**: Console → Develop → Messaging → Try it out → Send a WhatsApp message
2. **Send a test message** to verify everything works
3. **Check your phone** - you should receive the test message

---

### **Step 5: Copy Your Credentials for Railway**

**Your credentials will look like this:**

```env
TWILIO_ACCOUNT_SID=ACf1234567890abcdef1234567890abcdef
TWILIO_AUTH_TOKEN=abc123def456ghi789jkl012mno345pqr
TWILIO_WHATSAPP_NUMBER=+14155238886
```

**Important Notes:**
- ✅ **Account SID**: Always starts with `AC` followed by 32 characters
- ✅ **Auth Token**: Exactly 32 characters (letters and numbers)
- ✅ **WhatsApp Number**: Use `+14155238886` for sandbox testing
- ❌ **Never share** these credentials publicly or commit them to git

---

### **Step 6: Add Recipients to Environment Variables**

**Format your phone numbers correctly:**

```env
RECIPIENTS=+1234567890,+9876543210,+5551234567
```

**Phone Number Rules:**
- ✅ Include country code: `+1` (US), `+44` (UK), `+972` (Israel)
- ✅ No spaces or dashes: `+1234567890`
- ✅ Comma-separated for multiple: `+1111111111,+2222222222`
- ❌ Don't use: `123-456-7890` or `(123) 456-7890`

---

## 🔧 **Quick Verification**

**Test your credentials before deploying:**

1. **Create a test file** `test_twilio.py`:
```python
from twilio.rest import Client

# Your credentials
account_sid = 'ACf1234567890abcdef1234567890abcdef'  # Replace with yours
auth_token = 'abc123def456ghi789jkl012mno345pqr'    # Replace with yours

# Test connection
client = Client(account_sid, auth_token)
print("✅ Twilio connection successful!")

# Test message (optional)
message = client.messages.create(
    body='🕊️ Test message from your Mitzvah Bot!',
    from_='whatsapp:+14155238886',
    to='whatsapp:+1234567890'  # Replace with your number
)
print(f"✅ Test message sent! SID: {message.sid}")
```

2. **Run the test**:
```bash
pip install twilio
python test_twilio.py
```

---

## 🚨 **Troubleshooting**

### **Can't Find Auth Token? Try These:**

**If you don't see the Auth Token on the main dashboard:**

1. **Navigate manually**: 
   - Click **"Console"** (top left)
   - Click **"Account"** in left sidebar
   - Click **"API keys & tokens"**

2. **Direct URL method**:
   - Go to: https://console.twilio.com/us1/account/keys-credentials/api-keys
   - Look for **"Live credentials"** section

3. **Create new token**:
   - If token is not visible, click **"Create API Key"**
   - Choose **"Standard"** key type
   - **Copy the Secret immediately** (this becomes your Auth Token)

4. **Reset existing token**:
   - Find **"Auth Token"** section
   - Click **"Reset Auth Token"**
   - **Copy the new token immediately**

### **Common Issues:**

| Problem | Solution |
|---------|----------|
| "Auth Token not visible" | Try the direct URL or create new API key method above |
| "Account SID not found" | Look for "Account SID" in Account → Settings → General |
| "Invalid Auth Token" | Make sure it's exactly 32 characters, no spaces |
| "Sandbox not joined" | Send `join <code>` message to +1 415 523 8886 first |
| "Invalid phone number" | Ensure format: `+1234567890` (include country code) |
| "Message not received" | Check if recipient joined sandbox, verify phone format |

### **Where to Find Help:**
- **Twilio Console**: https://console.twilio.com/
- **Twilio Support**: https://help.twilio.com/
- **WhatsApp Sandbox**: Console → Develop → Messaging → Try it out

---

## 🎯 **Ready for Railway!**

Once you have your credentials:

1. **Go to Railway.app**
2. **Deploy your GitHub repository**: `Nerotas/Sefer-HaMitzvos`
3. **Add environment variables**:
   ```env
   TWILIO_ACCOUNT_SID=ACf1234567890abcdef1234567890abcdef
   TWILIO_AUTH_TOKEN=abc123def456ghi789jkl012mno345pqr
   TWILIO_WHATSAPP_NUMBER=+14155238886
   RECIPIENTS=+1234567890,+9876543210
   DEPLOY_MODE=test
   ```
4. **Deploy and test!**

---

## 💰 **Free Tier Limits**

**Twilio Free Trial includes:**
- ✅ $15.50 in free credit
- ✅ WhatsApp sandbox (unlimited testing)
- ✅ SMS and voice capabilities
- ✅ Full API access

**WhatsApp Costs:**
- 📱 **Sandbox**: Completely free
- 📱 **Production**: ~$0.005 per message (after approval)

Your daily mitzvah bot will cost less than $5/month even with 30 recipients! 🕊️📚

---

*Need help? The Twilio Console has excellent documentation and support chat!*