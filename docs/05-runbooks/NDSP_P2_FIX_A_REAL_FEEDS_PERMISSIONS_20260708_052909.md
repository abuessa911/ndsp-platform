# NDSP P2 Fix A — Real Feeds Permissions
DATE=2026-07-08T05:29:09+02:00
MODE=CONTROLLED_PERMISSION_FIX
TARGET=/var/www/ndsp-my/data
MODIFICATION=Allow nawaf511-owned real feed services to write generated JSON data
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_A_REAL_FEEDS_PERMISSIONS_20260708_052909

## 1) Pre-check
OWNER=root
GROUP=root
MODE=755
PATH=/var/www/ndsp-my/data
total 56
drwxr-xr-x 2 root     root      4096 يوليو   8 05:28 .
drwxrwxr-x 8 nawaf511 nawaf511  4096 يوليو   7 22:50 ..
-rw-r--r-- 1 root     root     46022 يوليو   8 05:28 command-center-real.json

## 2) Apply permission fix
OWNER=nawaf511 GROUP=nawaf511 MODE=775 PATH=/var/www/ndsp-my/data

## 3) Write permission smoke test as nawaf511
WRITE_SMOKE_TEST=OK

## 4) Run failed oneshot services once
REAL_SYNC_START_EXIT=0
CALENDAR_START_EXIT=0

## 5) Post-fix service status
REAL_SYNC_ACTIVE=inactive
CALENDAR_ACTIVE=inactive
○ ndsp-real-feeds-sync.service - NDSP Real Feeds Sync
     Loaded: loaded (/etc/systemd/system/ndsp-real-feeds-sync.service; static)
     Active: inactive (dead) since Wed 2026-07-08 05:29:09 CEST; 1s ago
TriggeredBy: ● ndsp-real-feeds-sync.timer
    Process: 3350130 ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/sync_real_feeds.py (code=exited, status=0/SUCCESS)
   Main PID: 3350130 (code=exited, status=0/SUCCESS)
        CPU: 161ms

يوليو 08 05:29:09 vmi2934783 systemd[1]: Starting ndsp-real-feeds-sync.service - NDSP Real Feeds Sync...
يوليو 08 05:29:09 vmi2934783 systemd[1]: ndsp-real-feeds-sync.service: Deactivated successfully.
يوليو 08 05:29:09 vmi2934783 systemd[1]: Finished ndsp-real-feeds-sync.service - NDSP Real Feeds Sync.
○ ndsp-tradingview-calendar.service - NDSP TradingView Live Economic Calendar
     Loaded: loaded (/etc/systemd/system/ndsp-tradingview-calendar.service; static)
     Active: inactive (dead) since Wed 2026-07-08 05:29:10 CEST; 2s ago
TriggeredBy: ● ndsp-tradingview-calendar.timer
    Process: 3350135 ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py (code=exited, status=0/SUCCESS)
   Main PID: 3350135 (code=exited, status=0/SUCCESS)
        CPU: 209ms

يوليو 08 05:29:09 vmi2934783 systemd[1]: Starting ndsp-tradingview-calendar.service - NDSP TradingView Live Economic Calendar...
يوليو 08 05:29:10 vmi2934783 python3[3350135]: ITEMS= 120
يوليو 08 05:29:10 vmi2934783 systemd[1]: ndsp-tradingview-calendar.service: Deactivated successfully.
يوليو 08 05:29:10 vmi2934783 systemd[1]: Finished ndsp-tradingview-calendar.service - NDSP TradingView Live Economic Calendar.

## 6) Output files check
total 108
drwxrwxr-x 2 nawaf511 nawaf511  4096 يوليو   8 05:29 .
drwxrwxr-x 8 nawaf511 nawaf511  4096 يوليو   7 22:50 ..
-rw-r--r-- 1 root     root     46022 يوليو   8 05:28 command-center-real.json
-rw-r--r-- 1 nawaf511 nawaf511   711 يوليو   8 05:29 data-quality.json
-rw-r--r-- 1 nawaf511 nawaf511 33081 يوليو   8 05:29 economic-calendar.json
-rw-r--r-- 1 nawaf511 nawaf511 11294 يوليو   8 05:29 news-impact.json
OWNER=nawaf511 GROUP=nawaf511 MODE=644 SIZE=11294 PATH=/var/www/ndsp-my/data/news-impact.json
OWNER=nawaf511 GROUP=nawaf511 MODE=644 SIZE=33081 PATH=/var/www/ndsp-my/data/economic-calendar.json
OWNER=root GROUP=root MODE=644 SIZE=46022 PATH=/var/www/ndsp-my/data/command-center-real.json

## 7) Critical runtime still OK
nginx=active
ndsp-quality-live-nmp-wrapper=active
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.7%[39m | [1mram usage[22m: [32m9.8%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.066mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.206mb/s[39m [90m/[39m [1m[33m82%[39m[22m |

## 8) Final Evaluation
P2_FIX_A_REAL_FEEDS_PERMISSIONS_STATUS=OK
FINAL_STATUS=P2_FIX_A_REAL_FEEDS_PERMISSIONS_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_A_REAL_FEEDS_PERMISSIONS_20260708_052909.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_A_REAL_FEEDS_PERMISSIONS_20260708_052909
