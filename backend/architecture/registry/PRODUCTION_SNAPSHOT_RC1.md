# NDSP Production Snapshot RC1

Generated: 20260629_083955

## Git

- Branch: feature/ndsp-os
- Head: c221ce1 (HEAD -> feature/ndsp-os, tag: v0.3.5-ndsp-rc1, origin/feature/ndsp-os) release(DEV-016): freeze release candidate rc1
- Head SHA: c221ce116f452f070bec2fe2d6465afdb7bee31d
- RC1 Tag: v0.3.5-ndsp-rc1

## Services

- CTL-001 Workspace Identity: internal
- CDS-001 Completed Decision Service: active
- DGC-001 Decision Governance Core: active
- BOT-001 Bot Execution Service: internal / dry-run only

## Public Surface

Read-only:
- GET https://api.ndsp.app/api/completed/latest
- GET https://api.ndsp.app/api/governance/health

Blocked write routes:
- POST https://api.ndsp.app/api/completed/ingest
- POST https://api.ndsp.app/api/governance/submit
- POST https://api.ndsp.app/api/governance/evaluate

## TLS

Unified certificate validated for:
- ndsp.app
- www.ndsp.app
- api.ndsp.app
- my.ndsp.app
- bot.ndsp.app

## Snapshot Decision

RC1 production smoke test passed.
No feature changes were introduced.
No Certbot command was executed.
No Nginx configuration edit was applied.
