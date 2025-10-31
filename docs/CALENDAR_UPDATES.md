# Updating the Sefer HaMitzvos Calendar

This guide explains how to safely update the live, public calendar and what subscribers will experience.

## TL;DR

- Editing the existing calendar updates it for everyone who subscribed.
- Keep the same Calendar ID. Avoid creating a new calendar unless you want subscribers to re-subscribe.
- UI edits propagate quickly; iCal (ICS) subscribers may see changes with a delay depending on their app.

## Where to find the Calendar ID

- Google Calendar → Settings → Select your calendar → "Integrate calendar" → Copy Calendar ID
- Or check `calendar_setup_instructions.md` in the repo root (generated when the tool first created the calendar).

## Ways to update

### 1) Edit directly in Google Calendar (recommended for small changes)

- Open the calendar by its name.
- Edit event titles, times, descriptions, locations; or delete events.
- Saves apply to all subscribers. Google Calendar subscribers typically see changes within minutes.

### 2) Regenerate programmatically (advanced / bulk changes)

Current tool (`tools/calendar/create_google_calendar.py`) creates a new calendar and then inserts all events. Re-running it as-is will produce another calendar with a new Calendar ID.

If you need bulk updates but want to keep the same Calendar ID, consider these options:

- Manual UI edits (simple but time consuming)
- Implement an "update mode" that:
  - Uses the existing Calendar ID
  - Assigns stable event IDs (e.g., `mitzvah-YYYY-MM-DD`) or uses `extendedProperties`
  - Calls `events.update`/`events.patch` for changed fields and `events.delete` for removed items
  - Supports a "dry run" diff preview before applying changes

If you’d like this update mode, open an issue or request and we’ll add it.

## Subscriber experience

- Subscribed to the Google calendar (Subscribe link):
  - Live view of your calendar. Changes appear automatically.
- Subscribed via iCal URL (ICS):
  - Also receive updates, but refresh timing varies by app (from ~15 minutes to 24 hours or more).
- Imported a static ICS file once:
  - No updates are received. They must re-import or (better) subscribe via URL.

## Best practices

- Keep the same Calendar ID to avoid breaking subscriptions.
- Prefer updates (edit/delete) over delete-and-recreate to minimize notification noise.
- Communicate major schedule shifts:
  - Update the calendar description (visible in Calendar settings)
  - Optionally add a pinned informational event
  - Reflect changes on the project homepage

## Forcing the new OAuth consent (optional)

If you recently changed your OAuth consent (e.g., moved to Production) and want to re-consent locally:

```powershell
# From repo root
Remove-Item -Force .\token.pickle
```

Re-run your calendar tool; your browser will open with the new consent screen.

## Troubleshooting

- "I don’t see my edits": Make sure you’re editing the correct calendar (verify the Calendar ID).
- "Subscribers aren’t seeing updates": Confirm they subscribed (not imported) and check app refresh frequency.
- "I accidentally created a new calendar": Either delete the new one or switch your workflows back to the original Calendar ID.
