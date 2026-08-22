# NDSP P2 Fix F — Disable Two Hold-Review Legacy Services
DATE=2026-07-08T22:04:47+02:00
MODE=CONTROLLED_DISABLE_TWO_HOLD_REVIEW_LEGACY_SERVICES
MODIFICATION=Disable signal-engine.service and subscription-watcher.service only
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_DELETE=1
NO_MASK=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447

LATEST_DEEP_AUDIT=docs/05-runbooks/NDSP_P2_HOLD_REVIEW_SERVICES_DEEP_AUDIT_READONLY_20260708_065452.md
LATEST_DECISION_MATRIX=docs/05-runbooks/NDSP_P2_HOLD_REVIEW_DECISION_MATRIX_READONLY_20260708_215212.md

## 1) Runtime safety before change
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.7%[39m | [1mram usage[22m: [32m10.5%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.12mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.259mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Validate targets from latest Deep Audit and live refs

---- TARGET=signal-engine.service ----
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
FRAGMENT=/etc/systemd/system/signal-engine.service
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447/signal-engine.service.unit.before
PROJECT_REFS_LIVE=0
NGINX_REFS_LIVE=0

---- TARGET=subscription-watcher.service ----
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
FRAGMENT=/etc/systemd/system/subscription-watcher.service
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447/subscription-watcher.service.unit.before
PROJECT_REFS_LIVE=0
NGINX_REFS_LIVE=0

## 3) Confirm untouched services
HOLD_UNTOUCHED_BEFORE=ndip-api-new.service ENABLED=disabled ACTIVE=failed FAILED=failed
HOLD_UNTOUCHED_BEFORE=testapp.service ENABLED=enabled ACTIVE=failed FAILED=failed

## 4) Disable targets only — no mask, no delete

DISABLING=signal-engine.service
Removed "/etc/systemd/system/multi-user.target.wants/signal-engine.service".

DISABLING=subscription-watcher.service
Removed "/etc/systemd/system/multi-user.target.wants/subscription-watcher.service".

## 5) Post-check target states
signal-engine.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
subscription-watcher.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
service                       enabled_after  active_after  failed_after
signal-engine.service         disabled       inactive      inactive
subscription-watcher.service  disabled       inactive      inactive

## 6) Confirm untouched services remained untouched
HOLD_UNTOUCHED_AFTER=ndip-api-new.service ENABLED=disabled ACTIVE=failed FAILED=failed
HOLD_UNTOUCHED_AFTER=testapp.service ENABLED=enabled ACTIVE=failed FAILED=failed

## 7) Failed units after Fix F
  UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service loaded failed failed NDIP API - New Backend
● testapp.service      loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

2 loaded units listed.

## 8) Runtime safety after change
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m21.1%[39m | [1mram usage[22m: [32m10.4%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.193mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ [1m[33m16.528mb/s[39m[22m ⇑ [32m0.493mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 9) Final Evaluation
NGINX_ACTIVE_FINAL=active
PM2_ACTIVE_FINAL=active
API_HTTP_FINAL=200
QUALITY_LIVE_HTTP_FINAL=200
MY_NDSP_HTTP_FINAL=200
P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_STATUS=OK
FINAL_STATUS=P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447
