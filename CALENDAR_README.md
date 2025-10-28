# 📅 Sefer HaMitzvos Google Calendar Integration

This project provides multiple ways to integrate the complete Sefer HaMitzvos study schedule into Google Calendar and other calendar applications.

## 🎯 Quick Start Options

### Option 1: ICS File Import (Easiest - No Setup Required)
```bash
python create_ics_calendar.py
```
- ✅ **Works immediately** - no Google API setup needed
- ✅ **Universal compatibility** - works with any calendar app
- ✅ **Offline access** once imported
- 📄 Creates: `sefer_hamitzvos_calendar.ics` (560KB, 629 events)

### Option 2: Google Calendar API (Advanced - Public Calendar)
```bash
# See GOOGLE_CALENDAR_SETUP.md for detailed setup
python create_google_calendar.py
```
- ✅ **Creates public shareable calendar**
- ✅ **Users can subscribe** with one click
- ✅ **Automatic updates** if you modify events
- 🔧 Requires: Google Cloud Project + OAuth2 setup

## 📋 What's Included in Both Methods

### 📅 **Calendar Events (629 Total):**
- **Principles (Shorashim):** Introduction concepts 1-14
- **Positive Commandments:** 248 mitzvot we're commanded to do
- **Negative Commandments:** 365 mitzvot we're commanded not to do

### ⏰ **Event Details:**
- **Time:** 8:00 AM daily (30-minute study session)
- **Title:** "📚 Sefer HaMitzvos: [Mitzvah Type]"
- **Description:** 
  - Complete mitzvah explanation
  - Biblical source when available
  - Direct Sefaria.org study link
  - Integration with WhatsApp study group

### 🔔 **Reminders:**
- At event time (8:00 AM)
- 15 minutes before (7:45 AM)
- 1 hour before via email (7:00 AM)

## 🛠️ Setup Instructions

### For ICS File Method:
1. Run `python create_ics_calendar.py`
2. Import the generated `sefer_hamitzvos_calendar.ics` into your calendar app
3. Follow the instructions in `ics_import_instructions.md`

### For Google Calendar API Method:
1. Follow the complete setup guide in `GOOGLE_CALENDAR_SETUP.md`
2. Run `python create_google_calendar.py`
3. Share the generated calendar link with your community

## 📊 Comparison: ICS vs Google Calendar API

| Feature | ICS File | Google Calendar API |
|---------|----------|---------------------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Advanced |
| **User Experience** | Import once | Subscribe link |
| **Updates** | Manual re-import | Automatic |
| **Sharing** | Send file | Send link |
| **Compatibility** | All calendar apps | Google-focused |
| **Maintenance** | None | Minimal |
| **Privacy** | Fully local | Uses Google services |

## 🎯 Recommended Usage

### **For Personal Use:**
- Use ICS file method - simple and private

### **For Community/Organization:**
- Use Google Calendar API method for easy sharing
- Create shareable public calendar
- Members subscribe with one click
- Centralized updates when needed

### **For Study Groups:**
- Combine with existing WhatsApp bot
- Calendar provides timing structure
- WhatsApp provides community discussion
- Perfect integration for consistent learning

## 📁 Generated Files

After running the scripts, you'll have:

```
📄 sefer_hamitzvos_calendar.ics    # Universal calendar file
📋 ics_import_instructions.md      # User instructions for ICS
📋 calendar_setup_instructions.md  # User instructions for Google Calendar
🔧 GOOGLE_CALENDAR_SETUP.md       # Developer setup guide
```

## 🔐 Security & Privacy

### ICS Method:
- ✅ Completely offline after import
- ✅ No external dependencies
- ✅ Full user control

### Google Calendar Method:
- 🔒 Requires Google authentication
- 📋 Uses secure OAuth2 flow
- 🌐 Creates public calendar (read-only for subscribers)
- 🔑 Credentials stored locally (`credentials.json` - never commit!)

## 🎉 Success Examples

### Individual Learner:
"I imported the ICS file into my iPhone calendar. Now I get daily reminders at 8 AM to study the mitzvah of the day. The Sefaria links make it easy to dive deeper!"

### Study Group:
"We created a public Google Calendar that all 50 members subscribe to. Combined with our WhatsApp bot, everyone stays synchronized with the daily learning schedule."

### Educational Institution:
"We embedded the public calendar on our website. Students and faculty can easily see the daily mitzvah schedule and plan their learning accordingly."

## 🛠️ Advanced Customization

Both scripts can be modified to:
- **Change event timing** (modify `event_config` in scripts)
- **Adjust time zones** (update `timeZone` settings)
- **Customize descriptions** (modify event formatting functions)
- **Add additional reminders** (extend reminder configurations)
- **Include Hebrew text** (enhance with Hebrew mitzvah names)

## 🤝 Integration with Existing Tools

### WhatsApp Bot Integration:
- Calendar provides **timing structure**
- WhatsApp bot provides **daily content delivery**
- Community discussion complements individual calendar study
- Perfect synchronization of learning schedule

### Sefaria Integration:
- Every event includes direct study links
- Deep learning resources readily accessible
- Seamless transition from calendar reminder to study material

## 📞 Support & Troubleshooting

### Common Issues:
1. **ICS Import Problems:** Check app-specific instructions in generated MD file
2. **Google API Errors:** Follow troubleshooting guide in setup documentation
3. **Time Zone Issues:** Verify time zone settings in calendar apps
4. **Missing Reminders:** Check calendar app notification permissions

### Getting Help:
- Review the detailed setup guides
- Check terminal output for specific error messages
- Verify all prerequisites are met
- Ensure stable internet connection for Google Calendar API

## 🎯 Future Enhancements

Potential improvements for future versions:
- **Multi-language support** (Hebrew, Aramaic descriptions)
- **Holiday adjustments** (automatic Shabbat/Yom Tov handling)
- **Progress tracking** (mark completed mitzvot)
- **Community features** (shared notes, discussions)
- **Mobile app integration** (dedicated study app)

## ✡️ The Vision

This calendar integration transforms abstract learning goals into concrete daily practice. By providing systematic reminders, easy access to study materials, and community synchronization, we make the profound wisdom of Sefer HaMitzvos accessible to modern learners.

**May your daily calendar become a gateway to deeper Torah understanding and observance!**

---

*Part of the Sefer HaMitzvos Daily Study Project*  
*Bringing ancient wisdom to modern schedules* 📚✡️