# AWS System Overview – Sefer HaMitzvos Daily Bot

This document explains everything used in our AWS system, how components fit together, and the exact order of operations from commit → deploy → runtime. It serves as the single source of truth for ops.

---

## 1) High-level Architecture

- WhatsApp Daily Bot (AWS Lambda, Python 3.11)
- Consent Capture API (AWS Lambda Function URL)
- Subscribers Store (Amazon DynamoDB)
- Daily Schedule (Amazon EventBridge Scheduler)
- Infrastructure as Code (AWS SAM + CloudFormation)
- CI/CD (GitHub Actions with serialized workflows)
- Messaging Provider (Twilio WhatsApp Business)

---

## 2) AWS Resources (by logical name)

From `template.yaml`:

- Lambda: `DailyMitzvahBot`

  - Runtime: Python 3.11
  - Handler: `bots/lambda_mitzvah_bot.lambda_handler`
  - Env: `SUBSCRIBERS_TABLE`, `TWILIO_*`, `RECIPIENTS` (fallback)
  - Policies: DynamoDBRead for subscribers table
  - Function URL: Enabled (CORS open)

- Lambda: `ConsentHandler`

  - Runtime: Python 3.11
  - Handler: `bots/consent_handler.lambda_handler`
  - Env: `SUBSCRIBERS_TABLE`, `WEBHOOK_TOKEN` (optional)
  - Policies: DynamoDB CRUD for subscribers table
  - Function URL: Enabled (CORS open, public)

- DynamoDB: `SubscribersTable` (physical: `daily-mitzvah-bot-stack-subscribers`)

  - PK: `phone` (string)
  - Billing: PAY_PER_REQUEST

- EventBridge Scheduler: `DailyMitzvahSchedule`

  - Name: `daily-mitzvah-10am-chicago-${StackName}` (physical example: `daily-mitzvah-10am-chicago-daily-mitzvah-bot-stack`)
  - Expression: `cron(0 10 * * ? *)` timezone `America/Chicago`
  - Target: `DailyMitzvahBot`
  - Invoke Role: `SchedulerInvokeRole`

- IAM: `SchedulerInvokeRole`

  - Allows EventBridge to invoke `DailyMitzvahBot`

- Lambda Permission: `SchedulerInvokePermission`
  - Grants invoke permission to scheduler principal

---

## 3) Deployed Identifiers (current)

- Stack: `daily-mitzvah-bot-stack` (us-east-1)
- ConsentHandler Function URL:
  - `https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/`
- DailyMitzvahBot Function URL:
  - `https://edo3ijgbo2padqvuzlrvomht4y0zaiqt.lambda-url.us-east-1.on.aws/`
- DynamoDB Table:
  - `daily-mitzvah-bot-stack-subscribers`
- EventBridge Schedule (physical):
  - `arn:aws:scheduler:us-east-1:128700457130:schedule/default/daily-mitzvah-10am-chicago-daily-mitzvah-bot-stack`
- Twilio WhatsApp Number:
  - `+15558414026`

---

## 4) Source Code Layout

- `bots/lambda_mitzvah_bot.py` – sends daily message; loads opted-in recipients from DynamoDB when `SUBSCRIBERS_TABLE` is set; otherwise falls back to `RECIPIENTS` env.
- `bots/consent_handler.py` – handles two paths:
  - Twilio webhook: JOIN/STOP/UNSUBSCRIBE → writes consent changes to DynamoDB and returns TwiML response
  - Web opt-in: accepts JSON `{ phone, consent, action }` or form POST → writes subscriber to DynamoDB
- `web/optin.html` – simple opt-in page with form and `wa.me` join link.
- `template.yaml` – SAM template defining all AWS resources above.
- `.github/workflows/deploy-sam.yml` – builds and deploys SAM stack; includes preflight wait to avoid 409s; prints outputs.
- `.github/workflows/deploy-lambda.yml` – performs code-only updates after SAM completes; has polling/retry logic and no push trigger.
- `CONSENT.md` – detailed consent system documentation and testing guide.

---

## 5) CI/CD – Order of Operations

Commit to `main` → GitHub Actions runs in this strict order:

1. Workflow: "Deploy with AWS SAM" (`.github/workflows/deploy-sam.yml`)

   - Sets up Python, SAM, AWS credentials
   - If prior stack failed, cleans it up (delete ROLLBACK states)
   - `sam build`
   - Waits for any in-progress Lambda updates to finish (preflight)
   - `sam deploy` → creates/updates all resources (Lambdas, DynamoDB, Scheduler, Function URLs, IAM)
   - Warms up functions and prints outputs

2. Workflow: "Deploy Lambda Function" (`.github/workflows/deploy-lambda.yml`)
   - Triggered only after SAM workflow completes successfully
   - Checks stack is stable, waits if Lambda is in progress
   - Updates Lambda code via S3 upload, publishes version, manages alias (if configured)
   - Optionally updates environment variables when requested

Safeguards:

- Concurrency group prevents overlaps in each workflow
- No push trigger on the direct Lambda deployer (prevents races)
- Custom polling loops replace flaky waiters (CloudFormation and Lambda)

---

## 6) Runtime – Order of Operations

A) Daily send (EventBridge → Lambda):

1. EventBridge Scheduler triggers at 10:00 America/Chicago
2. AWS invokes `DailyMitzvahBot`
3. Function loads recipients:
   - If `SUBSCRIBERS_TABLE` is set → Scan DynamoDB for `consent_status = 'opted_in' AND channel = 'whatsapp'`
   - Else → Use `RECIPIENTS` env var (comma-separated E.164 numbers)
4. For each recipient → send WhatsApp message via Twilio API using `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_WHATSAPP_NUMBER`
5. Logs results; errors retried per Lambda runtime policy

B) Consent capture (Two entry points):

1. Twilio inbound webhook → `ConsentHandler` Function URL
   - Parses keywords: JOIN MITZVAH → `opted_in`; STOP/UNSUBSCRIBE → `opted_out`
   - Writes record to DynamoDB with evidence and timestamp
   - Returns TwiML confirmation message
2. Web form/JSON → `ConsentHandler` Function URL
   - Validates phone and consent
   - Writes/updates DynamoDB record
   - Returns JSON status

---

## 7) Environment Variables and Secrets

Lambda environment variables (configured via workflows or SAM):

- `SUBSCRIBERS_TABLE` = `daily-mitzvah-bot-stack-subscribers`
- `TWILIO_ACCOUNT_SID` = e.g., `ACxxxxxxxx...` (GitHub secret)
- `TWILIO_AUTH_TOKEN` = e.g., `xxxxxxxx` (GitHub secret)
- `TWILIO_WHATSAPP_NUMBER` = `+15558414026` (GitHub secret)
- `RECIPIENTS` = optional fallback (comma-separated E.164 numbers)
- `WEBHOOK_TOKEN` = optional shared secret for web form submissions

GitHub Actions secrets required:

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER`
- `RECIPIENTS` (optional), `WEBHOOK_TOKEN` (optional)

---

## 8) Twilio Wiring

- WhatsApp Business Number: `+15558414026`
- Inbound webhook ("A message comes in"):
  - URL: `https://xjphbign6fi6xoafhqznx2lxme0rlfnp.lambda-url.us-east-1.on.aws/`
  - Method: POST
- Outbound messages are sent from `TWILIO_WHATSAPP_NUMBER`.

---

## 9) Observability and Logs

- ConsentHandler logs: `/aws/lambda/daily-mitzvah-bot-stack-ConsentHandler-*`
- DailyMitzvahBot logs: `/aws/lambda/daily-mitzvah-bot-stack-DailyMitzvahBot-*`
- CloudWatch Logs retention is managed by the SAM template/workflow
- Use `aws logs tail --follow` to watch in real time

---

## 10) Troubleshooting and Recovery

- If CloudFormation stack is stuck (e.g., UPDATE_ROLLBACK_FAILED):
  - Use the workflow’s built-in cleanup or run:
    ```powershell
    aws cloudformation continue-update-rollback --stack-name daily-mitzvah-bot-stack --region us-east-1
    ```
- If Lambda updates fail with 409 (InProgress):
  - The workflows wait automatically; avoid manual concurrent deploys
- If `ConsentFunctionUrl` output shows an ARN:
  - Use `aws lambda get-function-url-config` to retrieve actual URL
- To hotfix code only:
  - Manually dispatch "Deploy Lambda Function" workflow

---

## 11) Manual Test Commands

- Get stack status:

  ```powershell
  aws cloudformation describe-stacks --stack-name daily-mitzvah-bot-stack --query "Stacks[0].StackStatus" --output text --region us-east-1
  ```

- Get function URLs:

  ```powershell
  aws lambda get-function-url-config --function-name daily-mitzvah-bot-stack-ConsentHandler-1QnQEujF4Goa --query FunctionUrl --output text --region us-east-1
  aws lambda get-function-url-config --function-name daily-mitzvah-bot-stack-DailyMitzvahBot-FIJT0KdQy1L2 --query FunctionUrl --output text --region us-east-1
  ```

- List subscribers:
  ```powershell
  aws dynamodb scan --table-name daily-mitzvah-bot-stack-subscribers --region us-east-1 --query "Items[*].[phone.S, consent_status.S, source.S, timestamp_iso.S]" --output table
  ```

---

## 12) Security Notes

- Function URLs are public; consent handler does not expose sensitive data and supports optional `WEBHOOK_TOKEN` for web submissions.
- DynamoDB table stores minimal PII (phone number only) and consent metadata; no message content is stored.
- AWS credentials and Twilio tokens live only in GitHub Secrets.

---

## 13) Future Enhancements

- Add CloudFormation Outputs with correct `!GetAtt` to expose Function URLs directly
- Add SES or email fallback channel
- Add per-user delivery windows or pause mechanisms
- Add API Gateway in front of Function URLs if stricter auth is needed
