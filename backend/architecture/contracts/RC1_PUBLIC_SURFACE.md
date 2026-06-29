# RC1 Public Surface Contract

## Allowed Public Routes

Only the following API routes are public in RC1:

1. GET /api/completed/latest
2. GET /api/governance/health

## Blocked Public Write Routes

The following routes must remain blocked from the public gateway:

1. POST /api/completed/ingest
2. POST /api/governance/submit
3. POST /api/governance/evaluate

## Internal Services

The following services are not public execution surfaces:

- CTL-001
- BOT-001

## Bot Rule

BOT-001 remains execution-only and dry-run unless a separate controlled DEV task changes that state.
