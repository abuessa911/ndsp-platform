# NDSP P3 Reboot After Fix I — Preflight
DATE=2026-07-08T23:21:14+02:00
MODE=P3_REBOOT_AFTER_FIX_I_PREFLIGHT
WILL_REBOOT=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_PM2_CHANGE_EXCEPT_SAVE=1
NO_DELETE=1
NO_MASK=1

## 1) Required Fix I lock
FIX_I_LOCK=OK

## 2) Preflight failed units
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_BEFORE_REBOOT=0

## 3) Preflight target services
ndip-api-new.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndip-health-monitor.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndip-telegram-decision-worker.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndsp-market-prices-updater.service ENABLED=static ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndsp-market-prices-updater.timer ENABLED=enabled ACTIVE=active FAILED=active RESTART= NRESTARTS=

## 4) Core runtime before reboot
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 30m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m15.4%[39m | [1mram usage[22m: [32m7.7%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.192mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ [32m0.318mb/s[39m ⇑ [32m0.259mb/s[39m [90m/[39m [1m[33m82.05%[39m[22m |
[32m[PM2] [39mSaving current process list...
[32m[PM2] [39mSuccessfully saved in /home/nawaf511/.pm2/dump.pm2

## 5) Public endpoints before reboot
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 6) Marker
MARKER=docs/05-runbooks/NDSP_P3_REBOOT_AFTER_FIX_I_MARKER_20260708_232114.env

## 7) Final preflight decision
P3_REBOOT_AFTER_FIX_I_PREFLIGHT_STATUS=OK
FINAL_STATUS=P3_REBOOT_AFTER_FIX_I_PREFLIGHT_OK
REBOOT_COMMAND=systemctl reboot
NOTE=SSH will disconnect now.
REALITY_LOCK_STATUS=UPDATED
