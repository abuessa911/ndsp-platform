# NDSP SaaS Database Source of Truth

PostgreSQL is the active production database for NDSP SaaS.

Active tables used by the API:
- saas_subscriptions
- saas_payments
- saas_subscription_invites
- saas_subscription_leads
- saas_telegram_users
- saas_audit_events

The old SQLite file `data/ndsp_saas.sqlite3` is retained only as a legacy backup/reference.
Do not write new production SaaS data to SQLite.
Do not delete SQLite until production has been stable for a full verification period.
