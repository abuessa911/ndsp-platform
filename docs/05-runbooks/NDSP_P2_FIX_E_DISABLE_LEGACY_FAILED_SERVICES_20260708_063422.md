# NDSP P2 Fix E — Disable Legacy Failed Services
DATE=2026-07-08T06:34:22+02:00
MODE=CONTROLLED_DISABLE_LEGACY_FAILED_SERVICES
MODIFICATION=Disable only legacy failed services with zero project/nginx refs
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_DELETE=1
NO_MASK=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422

## 1) Pre-check critical runtime
nginx=active
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.7%[39m | [1mram usage[22m: [32m10.2%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.172mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.215mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Backup target unit files and validate zero refs

---- TARGET=fanno-comments.service ----
FRAGMENT=/etc/systemd/system/fanno-comments.service
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422/fanno-comments.service.unit.before
PROJECT_REFS_COUNT=0
NGINX_REFS_COUNT=0

---- TARGET=marketpulse.service ----
FRAGMENT=/etc/systemd/system/marketpulse.service
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422/marketpulse.service.unit.before
PROJECT_REFS_COUNT=0
NGINX_REFS_COUNT=0

---- TARGET=redis-replica.service ----
FRAGMENT=/etc/systemd/system/redis-replica.service
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422/redis-replica.service.unit.before
PROJECT_REFS_COUNT=0
NGINX_REFS_COUNT=0

---- TARGET=redis-sentinel.service ----
FRAGMENT=/etc/systemd/system/redis-sentinel.service
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422/redis-sentinel.service.unit.before
PROJECT_REFS_COUNT=0
NGINX_REFS_COUNT=0

## 3) Confirm hold-review services are not modified
HOLD_REVIEW=ndip-api-new.service ENABLED=disabled ACTIVE=failed FAILED=failed
HOLD_REVIEW=signal-engine.service ENABLED=enabled ACTIVE=failed FAILED=failed
HOLD_REVIEW=subscription-watcher.service ENABLED=enabled ACTIVE=failed FAILED=failed
HOLD_REVIEW=testapp.service ENABLED=enabled ACTIVE=failed FAILED=failed

## 4) Disable targets only — no mask, no delete

DISABLING=fanno-comments.service
Removed "/etc/systemd/system/multi-user.target.wants/fanno-comments.service".

DISABLING=marketpulse.service
Removed "/etc/systemd/system/multi-user.target.wants/marketpulse.service".

DISABLING=redis-replica.service
Removed "/etc/systemd/system/multi-user.target.wants/redis-replica.service".

DISABLING=redis-sentinel.service
Removed "/etc/systemd/system/multi-user.target.wants/redis-sentinel.service".

## 5) Post-check target states
fanno-comments.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
marketpulse.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
redis-replica.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
redis-sentinel.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive

service                 enabled_after  active_after  failed_after
fanno-comments.service  disabled       inactive      inactive
marketpulse.service     disabled       inactive      inactive
redis-replica.service   disabled       inactive      inactive
redis-sentinel.service  disabled       inactive      inactive

## 6) Confirm hold-review services remain untouched
HOLD_REVIEW_UNTOUCHED=ndip-api-new.service ENABLED=disabled ACTIVE=failed FAILED=failed
HOLD_REVIEW_UNTOUCHED=signal-engine.service ENABLED=enabled ACTIVE=failed FAILED=failed
HOLD_REVIEW_UNTOUCHED=subscription-watcher.service ENABLED=enabled ACTIVE=failed FAILED=failed
HOLD_REVIEW_UNTOUCHED=testapp.service ENABLED=enabled ACTIVE=failed FAILED=failed

## 7) Failed units after reset
  UNIT                         LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service         loaded failed failed NDIP API - New Backend
● signal-engine.service        loaded failed failed Empire Core Signal Engine
● subscription-watcher.service loaded failed failed Subscription Expiry Watcher
● testapp.service              loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

4 loaded units listed.

## 8) Critical runtime safety after change
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.4%[39m | [1mram usage[22m: [32m10%[39m | [1mlo[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.004mb/s[39m | [1meth0[22m: ⇓ [32m0.027mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.259mb/s[39m [90m/[39m [1m[33m82.01%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 9) Final Evaluation
NGINX_ACTIVE_FINAL=active
PM2_ACTIVE_FINAL=active
P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_STATUS=OK
FINAL_STATUS=P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422
