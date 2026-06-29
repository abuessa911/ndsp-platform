# DEV-018B — Remove Bot Mentions and Reset Rejected Canary

Generated: 20260629_093055

## Reason

The DEV-018 canary design was rejected.

The public NDSP decision-support platform must not expose the bot because the bot is intended to be private, personal, and not publicly announced. It may be offered separately through Telegram.

## Actions

- Removed rejected public canary pages from my.ndsp.app.
- Removed public bot preview page.
- Removed public launchpad page that linked platform and bot.
- Scrubbed bot/execution wording from public HTML pages.
- Removed rejected canary UI artifacts from repo.
- Added public platform bot privacy boundary policy.

## Final Product Rule

Public NDSP platform must show only decision-support experience.

No bot mention.
No execution mention.
No Telegram private bot mention.
No customer-facing bot navigation.

## Final Status

DEV018B_PUBLIC_BOT_PRIVACY_RESET_READY
