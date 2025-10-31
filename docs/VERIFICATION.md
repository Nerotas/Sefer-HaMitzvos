# Google OAuth Verification: Authorized Domain + Public Pages

This guide helps you complete Google OAuth verification by adding an Authorized domain and publishing minimal pages Google reviewers expect.

## 1) Pick a domain you control

- You must verify domain ownership in Google Search Console
- Use your primary site or a subdomain (e.g., study.example.com)

## 2) Publish two public pages

Host these pages on your domain (HTTPS):

- Homepage (overview): `/` (we provide `web/index.html`)
- Privacy Policy: `/privacy` (we provide `web/privacy.html`)

Ways to host:

- GitHub Pages (simple):
  - Option A: Set repo “Pages” to serve from `/docs` and copy pages there
  - Option B: Use a separate repo for your public site
  - Option C: Build & deploy to your own hosting
- Any HTTPS hosting works as long as URLs are public

Update links in the files:

- `web/index.html`: update contact email and any project links
- `web/privacy.html`: update contact email

## 3) Verify domain ownership

- Open https://search.google.com/search-console
- Add property for your domain
- Follow the verification steps (DNS TXT record is common)

## 4) Configure OAuth consent screen

In Google Cloud Console → APIs & Services → OAuth consent screen:

- App domain: set your site’s base URL (e.g., https://study.example.com)
- Links:
  - Homepage: https://study.example.com/
  - Privacy Policy: https://study.example.com/privacy
- Authorized domains: add your root domain (example.com)
- Scopes: keep minimal → https://www.googleapis.com/auth/calendar
- Add testers (in Audience/Test users) if remaining in Testing
- Publish app to move to “In production” when ready

## 5) Submit for verification (if required)

Provide:

- Scope justification: you only need Calendar scope to create a study calendar and events for the user
- Unlisted demo video: show OAuth consent and creating the calendar/events
- Working public links to homepage and privacy policy

## 6) After approval

- Long‑lived tokens (no 7‑day expiry for testers)
- No “unverified app” warning
- You can allow more people to run the creation tool if desired

## Templates included here

- `web/index.html` — Homepage with subscribe links
- `web/privacy.html` — Simple privacy policy

Tip: If you prefer, host pages on an existing site and just copy the text from these templates.
