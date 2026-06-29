# NDSP Production Snapshot RC1 Final

Generated: 20260629_084803

## Git

- Branch: feature/ndsp-os
- Current Head: 77b6636 (HEAD -> feature/ndsp-os, tag: v0.3.6-ndsp-rc1-smoke, origin/feature/ndsp-os) test(DEV-017): production smoke test and snapshot
- Current Head SHA: 77b6636e66c919aebbd9183905d587367572f0ee
- RC1 Tag: v0.3.5-ndsp-rc1
- Smoke Tag: v0.3.6-ndsp-rc1-smoke

## Services

- CTL-001 Workspace Identity: active / internal
- CDS-001 Completed Decision Service: active
- DGC-001 Decision Governance Core: active
- BOT-001 Bot Execution Service: active / internal / dry-run only

## Public API Surface

Allowed read-only:
- GET https://api.ndsp.app/api/completed/latest
- GET https://api.ndsp.app/api/governance/health

Blocked write:
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

## Server Snapshot

- Date UTC: 2026-06-29 06:48:10 UTC
- Hostname: vmi2934783
- Kernel: Linux vmi2934783 6.8.0-124-generic #124-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 13:00:45 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
- Disk Root: /dev/sda1       387G  229G  159G  60% /
- Memory: Mem:            23Gi       1.9Gi        20Gi        45Mi       1.2Gi        21Gi
- Load:  08:48:10 up 18:10,  2 users,  load average: 2.18, 2.30, 2.26

## Decision

DEV-017 production smoke and snapshot completed.
No Certbot command executed.
No Nginx edit applied.
No public write route enabled.
