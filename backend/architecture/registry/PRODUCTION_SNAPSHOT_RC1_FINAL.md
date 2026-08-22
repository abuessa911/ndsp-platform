# NDSP Production Snapshot RC1 Final

Generated: 20260629_085022

## Git

- Branch: feature/ndsp-os
- Current Head: a3e30a6 (HEAD -> feature/ndsp-os, tag: v0.3.6-ndsp-rc1-smoke, origin/feature/ndsp-os) test(DEV-017): finalize rc1 production smoke snapshot
- Current Head SHA: a3e30a654cbc1762286953726fde3a169593f39f
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

- Date UTC: 2026-06-29 06:50:28 UTC
- Hostname: vmi2934783
- Kernel: Linux vmi2934783 6.8.0-124-generic #124-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 13:00:45 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
- Disk Root: /dev/sda1       387G  229G  159G  60% /
- Memory: Mem:            23Gi       2.0Gi        20Gi        45Mi       1.2Gi        21Gi
- Load:  08:50:28 up 18:12,  2 users,  load average: 2.05, 2.26, 2.25

## Decision

DEV-017 production smoke and snapshot completed.
No Certbot command executed.
No Nginx edit applied.
No public write route enabled.
