# 🚀 Google Calendar Setup Guide

This guide will help you set up Google Calendar integration for the Sefer HaMitzvos daily study calendar.

## 📋 Prerequisites

1. **Google Account** - You need a Google account with Google Calendar access
2. **Google Cloud Project** - For API access (free)
3. **Python Environment** - Already configured in this project

## 🔧 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Look for the project selector** in the top navigation bar:
   - It usually shows "Select a project" or an existing project name
   - It's typically located near the left side of the top bar, after the hamburger menu
3. **Click on the project dropdown** → Click "**NEW PROJECT**"
   - **Alternative locations to look:**
     - "+" icon next to the project name in the top bar
     - "CREATE PROJECT" button on the main dashboard
     - "Manage resources" link → "Create Project"
4. **Fill in project details:**
   - Project name: "Sefer HaMitzvos Calendar"
   - Organization: Choose your organization or leave as "No organization"
   - Location: Leave as default
5. Click "**CREATE**" and wait for the project to be created (may take 30-60 seconds)

### Step 2: Enable Google Calendar API

1. In your Google Cloud project, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "Sefer HaMitzvos Calendar"
   - Add your email as developer contact
   - Save and continue through the steps
4. Back to "Create OAuth client ID":
   - Application type: "Desktop application"
   - Name: "Sefer HaMitzvos Desktop App"
   - Click "Create"
5. Download the JSON file
6. Rename it to `credentials.json` and place it in this folder

### Step 4: Run the Calendar Creator

```bash
# Make sure you're in the project directory
cd C:\Github\Rambam

# Run the Google Calendar creator
python create_google_calendar.py
```

### Step 5: Authentication Flow

1. The script will open a browser window
2. Sign in to your Google account
3. Grant permission for calendar access
4. The browser will show "The authentication flow has completed"
5. Return to the terminal - the script will continue

## 📁 File Structure

After setup, you'll have:

```
C:\Github\Rambam\
├── credentials.json          # Your OAuth2 credentials (keep private!)
├── token.pickle             # Authentication token (auto-generated)
├── create_google_calendar.py # Main calendar creator
├── create_ics_calendar.py   # ICS file generator (alternative)
└── calendar_setup_instructions.md # Generated user instructions
```

## 🔒 Security Notes

- **Never commit `credentials.json` or `token.pickle` to version control**
- These files contain sensitive authentication information
- Add them to `.gitignore` if not already present

## 🎯 What the Script Does

1. **Authenticates** with Google Calendar API
2. **Creates** a new public calendar named "Sefer HaMitzvos Daily Study"
3. **Populates** the calendar with 629+ mitzvah study events
4. **Configures** proper sharing permissions for public access
5. **Generates** setup instructions for users

## 📅 Calendar Features

- **Daily Events**: 8:00 AM, 30-minute duration
- **Rich Content**: Mitzvah descriptions, biblical sources, Sefaria links
- **Reminders**: At event time, 15 minutes before, 1 hour email
- **Public Access**: Users can subscribe without special permissions
- **Mobile Integration**: Works with Google Calendar mobile app

## 🔄 Alternative: ICS File Generation

If you prefer not to use Google Calendar API, you can generate a standard ICS file:

```bash
python create_ics_calendar.py
```

This creates `sefer_hamitzvos_calendar.ics` that can be imported into any calendar application.

## 🛠 Troubleshooting

### Common Issues:

**0. "Can't find Create Project button"**
   - The Google Cloud Console interface changes frequently
   - **Most common locations:**
     - Top navigation bar: Click project dropdown → "NEW PROJECT"
     - Dashboard: Look for "CREATE PROJECT" button
     - IAM & Admin → Manage Resources → "CREATE PROJECT"
     - Navigation menu (hamburger) → "Home" → "CREATE PROJECT"
   - **If still not visible:** Try refreshing the page or using a different browser
   - **Alternative:** Go directly to https://console.cloud.google.com/projectcreate

1. **"credentials.json not found"**

   - Make sure you downloaded and renamed the OAuth2 credentials file
   - Place it in the same folder as the scripts

2. **"Authentication failed"**

   - Check that Google Calendar API is enabled in your project
   - Verify your OAuth2 credentials are correct
   - Try deleting `token.pickle` and re-authenticating

3. **"Rate limit exceeded"**

   - The script creates events in batches to avoid this
   - If it occurs, wait a few minutes and try again
   - Default quota is 1,000,000 requests per day (more than enough)

4. **"Calendar not showing up"**
   - Check that the calendar was created successfully
   - Look for the calendar ID in the terminal output
   - Try refreshing Google Calendar in your browser

### Support:

- Check the terminal output for detailed error messages
- Ensure you have a stable internet connection
- Verify your Google account has Calendar access
- Review the Google Cloud Console for API usage and errors

## 🎉 Success!

Once complete, you'll have:

- A fully populated Sefer HaMitzvos study calendar
- Public sharing links for users to subscribe
- Setup instructions for distribution
- A systematic daily Torah study schedule

The calendar can be shared with individuals, study groups, or entire communities to promote consistent Torah learning!

✡️ May your calendar bring structure and blessing to daily Torah study!
