# NDSP P3 Controlled Reboot Drill — Preflight
DATE=2026-07-08T22:51:01+02:00
MODE=CONTROLLED_REBOOT_PREFLIGHT
WILL_REBOOT=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_SERVICE_DISABLE=1
NO_SERVICE_MASK=1
NO_DELETE=1

## 1) Required readiness lock
P3_BOOT_READINESS_LOCK=OK

## 2) Current system health before reboot
  UNIT                               LOAD   ACTIVE SUB    DESCRIPTION
● ndsp-market-prices-updater.service loaded failed failed NDSP Live Market Prices Updater

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
FAILED_UNITS_COUNT_BEFORE=1
nginx_active_before=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2_nawaf511_active_before=active
pm2_nawaf511_enabled_before=enabled

## 3) PM2 save and process check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 21s    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 70.9mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: 0% | [1mram usage[22m: [32m7.4%[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ 0mb/s [90m/[39m [1m[33m82.04%[39m[22m |
[32m[PM2] [39mSaving current process list...
[32m[PM2] [39mSuccessfully saved in /home/nawaf511/.pm2/dump.pm2
PM2_DUMP_READY=1 SIZE=11196 UPDATED=2026-07-08 22:51:03.242000000 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 4) Public endpoints before reboot
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 5) Disabled services expected state before reboot
ndip-api-new.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=activating FAILED_BEFORE=activating
testapp.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
signal-engine.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
subscription-watcher.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
fanno-comments.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
marketpulse.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
redis-replica.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
redis-sentinel.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive

## 6) Marker
MARKER=docs/05-runbooks/NDSP_P3_CONTROLLED_REBOOT_MARKER_20260708_225101.env

## 7) Final preflight decision
P3_CONTROLLED_REBOOT_PREFLIGHT_STATUS=CHECK_ALERTS
FINAL_STATUS=P3_CONTROLLED_REBOOT_PREFLIGHT_ABORTED_NO_REBOOT
REBOOT_NOT_EXECUTED=1
