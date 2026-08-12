# NDSP P3 Controlled Reboot Drill — Preflight
DATE=2026-07-08T22:49:43+02:00
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
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_BEFORE=0
nginx_active_before=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2_nawaf511_active_before=active
pm2_nawaf511_enabled_before=enabled

## 3) PM2 save and process check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.8%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.004mb/s[39m | [1meth0[22m: ⇓ [32m0.029mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.193mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
[32m[PM2] [39mSaving current process list...
[32m[PM2] [39mSuccessfully saved in /home/nawaf511/.pm2/dump.pm2
PM2_DUMP_READY=1 SIZE=11195 UPDATED=2026-07-08 22:49:44.433069123 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

## 4) Public endpoints before reboot
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 5) Disabled services expected state before reboot
ndip-api-new.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
testapp.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
signal-engine.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
subscription-watcher.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
fanno-comments.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
marketpulse.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
redis-replica.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive
redis-sentinel.service ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive FAILED_BEFORE=inactive

## 6) Marker
MARKER=docs/05-runbooks/NDSP_P3_CONTROLLED_REBOOT_MARKER_20260708_224943.env

## 7) Final preflight decision
P3_CONTROLLED_REBOOT_PREFLIGHT_STATUS=OK
FINAL_STATUS=P3_CONTROLLED_REBOOT_PREFLIGHT_OK
REBOOT_COMMAND=systemctl reboot
NOTE=SSH will disconnect now.
REALITY_LOCK_STATUS=UPDATED
