# NDSP Release Candidate RC1

Generated: 20260629_035520

## Release Candidate

- RC: v0.3.5-ndsp-rc1
- Branch: feature/ndsp-os
- Base Head: 07c968c ops(DEV-015): close controlled public gateway activation

## Frozen Scope

Included:
- DEV-012 systemd local rollout
- DEV-013 enterprise hardening
- DEV-014 gateway readiness
- DEV-015 controlled public gateway activation

Frozen public read-only routes:
- GET /api/completed/latest
- GET /api/governance/health

Internal only:
- CTL-001
- BOT-001

## Freeze Decision

No new features are included in this freeze.
No Nginx edits were applied in DEV-016.
No Certbot command was executed in DEV-016.
