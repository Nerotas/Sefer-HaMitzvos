# WhatsApp Consent & Opt-In System

This project includes a compliant consent capture system for WhatsApp messaging, consisting of a Lambda function, DynamoDB table, and web opt-in page.

## Architecture

- **ConsentHandler Lambda**: `daily-mitzvah-bot-stack-ConsentHandler-1QnQEujF4Goa`

  - Function URL: `https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/`
  - Handles Twilio webhooks (keyword opt-in/out) and web form submissions
  - Source: `bots/consent_handler.py`

- **SubscribersTable (DynamoDB)**: `daily-mitzvah-bot-stack-subscribers`

  - Partition key: `phone` (string)
  - Attributes: `consent_status`, `channel`, `source`, `evidence`, `timestamp_iso`
  - Billing: PAY_PER_REQUEST

- **DailyMitzvahBot Lambda**: `daily-mitzvah-bot-stack-DailyMitzvahBot-FIJT0KdQy1L2`
  - Function URL: `https://edo3ijgbo2padqvuzlrvomht4y0zaiqt.lambda-url.us-east-1.on.aws/`
  - Updated to load recipients from DynamoDB when `SUBSCRIBERS_TABLE` env var is set
  - Falls back to `RECIPIENTS` env var if table not configured
  - Source: `bots/lambda_mitzvah_bot.py`

## Opt-In Methods

### 1. WhatsApp Keyword Opt-In

Users can send keywords to your WhatsApp number: `+15558414026`

**Supported keywords:**

- **JOIN MITZVAH** - Opt in to daily messages
- **STOP** / **UNSUBSCRIBE** - Opt out from messages

**Twilio Configuration:**

- Navigate to your Twilio Console → Messaging → WhatsApp sender `+15558414026`
- Set **"When a message comes in"** webhook to:
  ```
  https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/
  ```
- Method: `POST`

**How it works:**

1. User sends "JOIN MITZVAH" to `+15558414026`
2. Twilio sends webhook POST to ConsentHandler
3. ConsentHandler parses keyword and stores opt-in in DynamoDB
4. Returns TwiML response confirming subscription

### 2. Web Form Opt-In

Users can opt in via the web page: `web/optin.html`

**How to use:**

1. Host `web/optin.html` on your website or open it locally
2. Users enter phone number and check consent checkbox
3. Form POSTs to ConsentHandler Function URL
4. Subscriber record created in DynamoDB

**Configuration (already set):**

```javascript
const CONSENT_URL =
  "https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/";
const WHATSAPP_NUMBER = "+15558414026";
```

**WhatsApp link generation:**
The page includes a `wa.me` link that pre-fills "JOIN MITZVAH" message:

```
https://wa.me/15558414026?text=JOIN%20MITZVAH
```

## DynamoDB Schema

Each subscriber record contains:

```json
{
  "phone": "+15551234567", // Partition key, E.164 format
  "consent_status": "opted_in", // "opted_in" or "opted_out"
  "channel": "whatsapp", // "whatsapp" or "web"
  "source": "twilio_keyword", // "twilio_keyword" or "web_form"
  "evidence": "JOIN MITZVAH", // Keyword sent or form data
  "timestamp_iso": "2025-10-20T19:45:30.123456+00:00"
}
```

## Consent Handler Endpoints

### Twilio Webhook (POST)

**Request format** (form-encoded from Twilio):

```
Body=JOIN MITZVAH
From=whatsapp:+15551234567
```

**Response** (TwiML):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>You're subscribed to Daily Mitzvah! Reply STOP to unsubscribe.</Message>
</Response>
```

### Web Form (POST)

**Request format** (JSON):

```json
{
  "phone": "+15551234567",
  "consent": true,
  "action": "optin"
}
```

**Response**:

```json
{
  "message": "Subscribed successfully",
  "phone": "+15551234567",
  "status": "opted_in"
}
```

## Testing

### Test WhatsApp Opt-In

1. Send "JOIN MITZVAH" to `+15558414026` via WhatsApp
2. You should receive confirmation: "You're subscribed to Daily Mitzvah! Reply STOP to unsubscribe."
3. Verify record in DynamoDB:
   ```powershell
   aws dynamodb get-item `
     --table-name daily-mitzvah-bot-stack-subscribers `
     --key '{"phone":{"S":"+15551234567"}}' `
     --region us-east-1
   ```

### Test WhatsApp Opt-Out

1. Send "STOP" to `+15558414026`
2. You should receive: "You've been unsubscribed from Daily Mitzvah."
3. DynamoDB record updated to `consent_status: "opted_out"`

### Test Web Form

1. Open `web/optin.html` in browser
2. Enter phone number (E.164 format: `+15551234567`)
3. Check consent checkbox
4. Click "Subscribe"
5. Should see "Saved" status message

### Verify DynamoDB Records

```powershell
# Scan all subscribers
aws dynamodb scan `
  --table-name daily-mitzvah-bot-stack-subscribers `
  --region us-east-1

# Get specific subscriber
aws dynamodb get-item `
  --table-name daily-mitzvah-bot-stack-subscribers `
  --key '{"phone":{"S":"+15551234567"}}' `
  --region us-east-1
```

## How DailyMitzvahBot Uses Subscribers

The bot checks for the `SUBSCRIBERS_TABLE` environment variable:

**With DynamoDB** (current setup):

```python
# Scans DynamoDB for all opted-in WhatsApp subscribers
subscribers = dynamodb.scan(
    TableName='daily-mitzvah-bot-stack-subscribers',
    FilterExpression='consent_status = :status AND channel = :channel',
    ExpressionAttributeValues={
        ':status': {'S': 'opted_in'},
        ':channel': {'S': 'whatsapp'}
    }
)
```

**Fallback to static recipients**:
If `SUBSCRIBERS_TABLE` is not set, falls back to `RECIPIENTS` environment variable (comma-separated phone numbers).

## Compliance Notes

This system provides:

- ✅ **Express consent**: Users must actively opt in via keyword or form
- ✅ **Evidence storage**: All opt-ins stored with timestamp, source, and evidence
- ✅ **Easy opt-out**: Users can send STOP at any time
- ✅ **Audit trail**: DynamoDB records include full consent history
- ✅ **Channel tracking**: Separate tracking for WhatsApp vs web opt-ins

## Deployment

The consent system is deployed via AWS SAM:

- Template: `template.yaml`
- Stack: `daily-mitzvah-bot-stack`
- Region: `us-east-1`
- Workflows: `.github/workflows/deploy-sam.yml` and `.github/workflows/deploy-lambda.yml`

**GitHub Secrets Required:**

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER` (set to `+15558414026`)
- `RECIPIENTS` (optional, fallback if DynamoDB not used)
- `WEBHOOK_TOKEN` (optional)

## Troubleshooting

### Webhook not receiving messages

- Verify Twilio webhook URL is set correctly
- Check ConsentHandler CloudWatch logs: `/aws/lambda/daily-mitzvah-bot-stack-ConsentHandler-1QnQEujF4Goa`
- Test Function URL directly with curl:
  ```powershell
  curl -X POST https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/ `
    -d "Body=JOIN MITZVAH&From=whatsapp:+15551234567"
  ```

### Web form not working

- Check browser console for CORS errors
- Verify ConsentHandler has CORS enabled (it does)
- Check network tab for 4xx/5xx responses

### Subscribers not appearing in DynamoDB

- Verify table exists: `daily-mitzvah-bot-stack-subscribers`
- Check ConsentHandler has DynamoDB write permissions (DynamoDBCrudPolicy)
- Review Lambda logs for permission errors

### Bot not sending to opted-in users

- Verify `SUBSCRIBERS_TABLE` env var is set on DailyMitzvahBot
- Check bot has DynamoDB read permissions (DynamoDBReadPolicy)
- Review Lambda logs during scheduled run
