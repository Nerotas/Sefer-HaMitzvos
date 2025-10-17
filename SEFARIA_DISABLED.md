# 🔗 Sefaria Links - Temporarily Disabled

## ⚠️ **Status: Disabled for Accuracy Review**

The Sefaria integration has been temporarily commented out in the Lambda bot code until we can ensure 100% accuracy of the links with their corresponding mitzvot.

## 🔧 **What Was Done**

### Lambda Bot (`bots/lambda_mitzvah_bot.py`)

- **Commented out** `generate_sefaria_link()` function
- **Removed** Sefaria links from message templates
- **Added TODO comments** for future re-enablement

### Current Message Format (Without Sefaria Links)

```
🕊️ Sefer HaMitzvos Daily Study 📚

📅 Thursday, October 17, 2025

🔢 Mitzvah #1
To know there is a G‑d

📚 Source: Shemos 20:2

Fulfill this mitzvah with joy and intention! 💫🙏

—Daily Mitzvah Bot (AWS Lambda)
```

## 📋 **Schedule.csv Status**

- The `Schedule.csv` still contains the Sefaria links in the data
- These are **not used** by the Lambda bot currently
- Links remain available for future verification and re-enablement

## 🔄 **Re-enabling Process**

When ready to re-enable Sefaria links:

1. **Verify Link Accuracy** - Check each link matches its mitzvah
2. **Uncomment Code** - Remove comment blocks in `lambda_mitzvah_bot.py`
3. **Test Thoroughly** - Verify all link types work correctly:
   - Single mitzvot (e.g., "1")
   - Multiple mitzvot (e.g., "612, 613")
   - Introduction/Shorashim (e.g., "Intro 1")
4. **Update Documentation** - Add Sefaria feature back to README
5. **Regenerate Package** - Create new Lambda deployment package

## 💡 **Link Structure Reference**

For future verification, the intended structure was:

- **Shorashim**: `Sefer_HaMitzvot%2C_Shorashim.{number}`
- **Positive Commandments**: `Sefer_HaMitzvot%2C_Positive_Commandments.{number}`
- **Negative Commandments**: `Sefer_HaMitzvot%2C_Negative_Commandments.{number}`

### Traditional Sefer HaMitzvot Structure

- **Positive**: 1-248
- **Negative**: 249-613 (mapped to 1-365 in Sefaria)

---

**The bot continues to work perfectly without Sefaria links, focusing on delivering accurate daily mitzvah content! 📚✨**
