# 📱 WhatsApp Message Template Setup Guide

Complete instructions for creating and implementing WhatsApp Business API Message Templates for the Rambam Mitzvah Bot.

## 🎯 **Why Templates Are Needed**

WhatsApp Business API requires **pre-approved message templates** for:

- Messages sent outside the 24-hour conversation window
- Automated/bot-initiated messages (like daily mitzvot)
- Messages longer than SMS limits

**Benefits:**

- ✅ Send full educational content (no 160-character limit)
- ✅ No 24-hour window restrictions
- ✅ Professional WhatsApp Business integration
- ✅ Message delivery reliability

---

## 📋 **Step 1: Create Message Template in Twilio Console**

### **Navigate to Templates**

1. **Go to**: https://console.twilio.com
2. **Navigate**: Messaging → WhatsApp → Message Templates
3. **Click**: "Create new template" or "+" button

### **Template Configuration**

#### **Basic Information:**

```
Template Name: daily_mitzvah_rambam
Display Name: Daily Mitzvah - Rambam
Category: UTILITY
Language: English (US)
```

#### **Template Body:**

```
🕊️ Daily Mitzvah - {{1}}

📋 {{2}}
📖 {{3}}

📜 Source: {{4}}

🔗 Learn more: {{5}}

May this mitzvah illuminate your path! ✨🙏
```

#### **Variable Definitions:**

- **{{1}}**: Date (e.g., "November 6, 2025")
- **{{2}}**: Mitzvah Numbers (e.g., "Positive 21, Positive 22")
- **{{3}}**: Full Description (complete educational summary)
- **{{4}}**: Biblical Sources (e.g., "Vayikra 19:18, Bamidbar 18:5")
- **{{5}}**: Study Links (Sefaria URLs)

### **Sample Preview:**

```
🕊️ Daily Mitzvah - November 6, 2025

📋 Positive 21, Positive 22
📖 Not to bear a grudge & We are commanded to guard the Temple and to constantly walk around it, to honor it, to exalt it and to aggrandize it.

📜 Source: Vayikra 19:18, Bamidbar 18:5

🔗 Learn more: https://www.sefaria.org/Sefer_HaMitzvot...

May this mitzvah illuminate your path! ✨🙏
```

---

## ⏳ **Step 2: Template Approval Process**

### **Submission Requirements:**

- **Use Case**: Daily educational religious content delivery
- **Frequency**: Once per day
- **Audience**: Subscribed users only
- **Content Type**: Educational/informational

### **Expected Timeline:**

- **Submission**: Immediate
- **Review**: 24-48 hours (weekdays)
- **Approval**: Email notification from Twilio
- **Status**: Check in Twilio Console

### **Approval Tips:**

1. **Clear Purpose**: Specify it's for daily religious education
2. **User Consent**: Mention users have opted in
3. **Educational Value**: Emphasize learning and spiritual growth
4. **Regular Schedule**: Daily delivery at consistent time

---

## 🔧 **Step 3: Get Template Details After Approval**

### **Find Template SID:**

1. **Go to**: Twilio Console → Messaging → WhatsApp → Message Templates
2. **Find**: "daily_mitzvah_rambam" (approved status)
3. **Copy**: Template SID (starts with `HX...`)
4. **Example**: `HXabcd1234567890abcd1234567890abcd`

### **Test Template (Optional):**

```bash
# Using Twilio CLI (if installed)
twilio api:messaging:v1:messages:create \
  --content-sid HXabcd1234567890abcd1234567890abcd \
  --content-variables '{"1":"November 6, 2025","2":"Positive 21","3":"Test description","4":"Test source","5":"Test link"}' \
  --from whatsapp:+YOUR_TWILIO_NUMBER \
  --to whatsapp:+YOUR_TEST_NUMBER
```

---

## 💻 **Step 4: Update Lambda Bot Code**

### **Update Environment Variables:**

Add to AWS Lambda Configuration → Environment variables:

```
WHATSAPP_TEMPLATE_SID = HXabcd1234567890abcd1234567890abcd
USE_WHATSAPP_TEMPLATE = true
```

### **Code Update Required:**

The Lambda bot needs modification to use templates. After approval, I'll update the `send_to_recipient` method to:

```python
def send_to_recipient(self, recipient, message, mitzvah_data=None):
    """Send message using WhatsApp template if available."""
    try:
        template_sid = os.environ.get('WHATSAPP_TEMPLATE_SID')
        use_template = os.environ.get('USE_WHATSAPP_TEMPLATE', 'false').lower() == 'true'

        if template_sid and use_template and mitzvah_data:
            # Use WhatsApp template
            message_obj = self.client.messages.create(
                content_sid=template_sid,
                content_variables=json.dumps({
                    "1": mitzvah_data.get('date', ''),
                    "2": mitzvah_data.get('mitzvos', ''),
                    "3": mitzvah_data.get('title', ''),
                    "4": ', '.join(mitzvah_data.get('biblical_sources', [])),
                    "5": ', '.join(mitzvah_data.get('sefaria_link', []))
                }),
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{recipient}'
            )
        else:
            # Fallback to regular SMS
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=recipient
            )
```

---

## 🧪 **Step 5: Testing Process**

### **After Template Approval:**

1. **Update Lambda Environment Variables**
2. **Deploy Updated Code**
3. **Test with Lambda Event:**
   ```json
   {
     "test_date": "2025-11-06"
   }
   ```

### **Expected Results:**

- ✅ **Status Code**: 201 (success)
- ✅ **Message Type**: WhatsApp Business Message
- ✅ **Full Content**: Complete mitzvah description
- ✅ **Professional Format**: Template structure
- ✅ **No Length Limits**: Full educational content

---

## 🚀 **Step 6: Production Deployment**

### **Daily Schedule Setup:**

1. **CloudWatch Events**: Create rule for daily trigger
2. **Time**: Set preferred delivery time (e.g., 8:00 AM)
3. **Target**: Your Lambda function
4. **Event**: `{}` (no test_date = use current date)

### **Monitoring:**

- **CloudWatch Logs**: Monitor daily execution
- **Twilio Console**: Check message delivery status
- **Template Usage**: Monitor template performance

---

## 📋 **Quick Checklist**

### **Template Creation:**

- [ ] Template submitted in Twilio Console
- [ ] Category: UTILITY
- [ ] 5 variables defined correctly
- [ ] Clear use case description provided

### **Approval Phase:**

- [ ] Template status: "Approved"
- [ ] Template SID copied (HX...)
- [ ] Test message sent successfully

### **Lambda Integration:**

- [ ] Environment variables updated
- [ ] Code updated for template support
- [ ] New package deployed to Lambda
- [ ] Test execution successful

### **Production Ready:**

- [ ] Daily schedule configured
- [ ] Monitoring set up
- [ ] Full WhatsApp messages delivered

---

## 🆘 **Troubleshooting**

### **Common Issues:**

**Template Rejected:**

- Review rejection reason in email
- Modify content/use case description
- Resubmit with changes

**Template Variables Not Working:**

- Check JSON format in content_variables
- Verify variable numbers (1-5)
- Ensure all required variables provided

**Messages Still Truncated:**

- Verify USE_WHATSAPP_TEMPLATE=true
- Check template SID is correct
- Confirm code is using template path

**Delivery Failures:**

- Check WhatsApp Business account status
- Verify recipient number is valid
- Confirm from number is template-approved

---

## 🎯 **Success Metrics**

Once fully implemented, you'll have:

- ✅ **Professional WhatsApp delivery** (not SMS)
- ✅ **Complete educational content** (no truncation)
- ✅ **Reliable daily delivery** (no window restrictions)
- ✅ **Scalable system** (approved for multiple recipients)

**This setup provides the ultimate daily mitzvah delivery experience!** 📚✨

---

**Next Step**: Create the template in Twilio Console and wait for approval. Once approved, provide the Template SID and I'll update the Lambda code immediately!
