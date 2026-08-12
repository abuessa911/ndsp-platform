# NDSP P3 Post-Reboot After Fix I Verification
DATE=2026-07-08T23:25:20+02:00
MODE=P3_POST_REBOOT_AFTER_FIX_I_VERIFICATION
MODIFICATIONS=None
NO_REBOOT=1
NO_RESTART=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1

## 1) Boot identity
up 3 minutes
         system boot  2026-07-08 23:21
SYSTEM_RUNNING_STATE=running

## 2) Stabilization wait
WAIT_SECONDS=90

## 3) Failed units after reboot and wait
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_AFTER_REBOOT_FIX_I=0

## 4) Fix I target services after reboot
ndip-api-new.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive RESTART=no NRESTARTS=0
ndip-health-monitor.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive RESTART=always NRESTARTS=0
ndip-telegram-decision-worker.service ENABLED_AFTER_REBOOT=disabled ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive RESTART=always NRESTARTS=0
ndsp-market-prices-updater.service ENABLED_AFTER_REBOOT=static ACTIVE_AFTER_REBOOT=inactive FAILED_AFTER_REBOOT=inactive RESTART=no NRESTARTS=0
ndsp-market-prices-updater.timer ENABLED_AFTER_REBOOT=enabled ACTIVE_AFTER_REBOOT=active FAILED_AFTER_REBOOT=active RESTART= NRESTARTS=
NDIP_ACTIVE_FINAL_AFTER_REBOOT=inactive
NDIP_FAILED_FINAL_AFTER_REBOOT=inactive
NDIP_RESTART_POLICY_FINAL_AFTER_REBOOT=no
MARKET_TIMER_ACTIVE_FINAL_AFTER_REBOOT=active
MARKET_SERVICE_FAILED_FINAL_AFTER_REBOOT=inactive
NDIP_HEALTH_MONITOR_ACTIVE_FINAL_AFTER_REBOOT=inactive
NDIP_TELEGRAM_WORKER_ACTIVE_FINAL_AFTER_REBOOT=inactive

## 5) Core runtime after reboot
NGINX_ACTIVE_AFTER_REBOOT=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER_REBOOT=active
PM2_ENABLED_AFTER_REBOOT=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 4m     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14.3%[39m | [1mram usage[22m: [32m7.4%[39m | [1mlo[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.005mb/s[39m | [1meth0[22m: ⇓ [32m0.119mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.244mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
PM2_TOTAL_PROCESS_COUNT_AFTER_FIX_I_REBOOT=1
PM2_NDSP_PORTAL_COUNT_AFTER_FIX_I_REBOOT=1
PM2_NDSP_PORTAL_ONLINE_AFTER_FIX_I_REBOOT=1

## 6) Public endpoints after reboot
API_HEALTH_HTTP_AFTER_FIX_I_REBOOT=200
QUALITY_LIVE_HTTP_AFTER_FIX_I_REBOOT=200
MY_NDSP_HTTP_AFTER_FIX_I_REBOOT=200
ADMIN_NDSP_HTTP_AFTER_FIX_I_REBOOT=200

## 7) Gateway and feeds after reboot
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1328,fd=32))                                                                                                                                                                                                         
PORT_9001_LISTENING_AFTER_FIX_I_REBOOT=1
drwxrwxr-x 2 nawaf511 nawaf511 4096 يوليو   8 23:26 /var/www/ndsp-my/data
-rw-r--r-- nawaf511 nawaf511 711 2026-07-08 23:22 /var/www/ndsp-my/data/data-quality.json
-rw-r--r-- nawaf511 nawaf511 11270 2026-07-08 23:22 /var/www/ndsp-my/data/news-impact.json
-rw-r--r-- nawaf511 nawaf511 33119 2026-07-08 23:22 /var/www/ndsp-my/data/economic-calendar.json

## 8) Final Evaluation
P3_CONTROLLED_REBOOT_AFTER_FIX_I_STATUS=OK
FINAL_STATUS=P3_CONTROLLED_REBOOT_AFTER_FIX_I_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P3_POST_REBOOT_AFTER_FIX_I_VERIFICATION_20260708_232520.md
