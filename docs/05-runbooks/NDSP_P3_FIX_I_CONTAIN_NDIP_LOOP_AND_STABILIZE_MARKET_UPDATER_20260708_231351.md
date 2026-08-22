# NDSP P3 Fix I — Contain ndip Restart Loop + Stabilize Market Updater Boot
DATE=2026-07-08T23:13:51+02:00
MODE=CONTROLLED_SYSTEMD_CONTAINMENT_PATCH
MODIFICATION=systemd drop-ins + stop/disable ndip reverse dependencies + reset-failed
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_PM2_CHANGE=1
NO_DB_CHANGE=1
NO_DELETE=1
NO_MASK=1
NO_REBOOT=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351

LATEST_H_REPORT=docs/05-runbooks/NDSP_P3_ALERT_RESOLVER_H_POST_REBOOT_FAILED_UNITS_READONLY_20260708_225727.md

## 1) Preflight runtime safety
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 23m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.6mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.1%[39m | [1mram usage[22m: [32m7.5%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.303mb/s[39m [90m/[39m [1m[33m82.05%[39m[22m |
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 2) Validate H evidence
H_EVIDENCE_OK=1

## 3) Backup target units
BACKUP_FRAGMENT_ndsp-market-prices-updater.service=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351/ndsp-market-prices-updater.service/fragment.before
BACKUP_FRAGMENT_ndsp-market-prices-updater.timer=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351/ndsp-market-prices-updater.timer/fragment.before
BACKUP_FRAGMENT_ndip-api-new.service=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351/ndip-api-new.service/fragment.before
BACKUP_FRAGMENT_ndip-health-monitor.service=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351/ndip-health-monitor.service/fragment.before
BACKUP_FRAGMENT_ndip-telegram-decision-worker.service=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351/ndip-telegram-decision-worker.service/fragment.before

## 4) Apply market updater boot stabilization
MARKET_UPDATER_DROPIN=/etc/systemd/system/ndsp-market-prices-updater.service.d/40-ndsp-p3-after-postgresql.conf

## 5) Apply ndip containment drop-in
NDIP_CONTAINMENT_DROPIN=/etc/systemd/system/ndip-api-new.service.d/99-ndsp-p3-contain-disabled-legacy.conf

## 6) daemon-reload

## 7) Stop/disable ndip reverse dependency services

---- REVERSE_SERVICE=ndip-health-monitor.service ----
ndip-health-monitor.service LOAD_STATE=loaded ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive
ndip-health-monitor.service REFERENCES_NDIP_API_NEW=1
ACTION=disable_now_ndip-health-monitor.service
Failed to reset failed state of unit ndip-health-monitor.service: Unit ndip-health-monitor.service not loaded.

---- REVERSE_SERVICE=ndip-telegram-decision-worker.service ----
ndip-telegram-decision-worker.service LOAD_STATE=loaded ENABLED_BEFORE=disabled ACTIVE_BEFORE=inactive
ndip-telegram-decision-worker.service REFERENCES_NDIP_API_NEW=1
ACTION=disable_now_ndip-telegram-decision-worker.service
Failed to reset failed state of unit ndip-telegram-decision-worker.service: Unit ndip-telegram-decision-worker.service not loaded.

## 8) Stop and reset ndip-api-new.service loop
ACTION=stop_ndip_api_new
ACTION=reset_failed_ndip_api_new

## 9) Cleanup market updater failed state only

## 10) Post-fix stabilization wait
WAIT_SECONDS=25

## 11) Post-check systemd
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_AFTER_FIX_I=0
ndip-api-new.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndip-health-monitor.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndip-telegram-decision-worker.service ENABLED=disabled ACTIVE=inactive FAILED=inactive RESTART=always NRESTARTS=0
ndsp-market-prices-updater.service ENABLED=static ACTIVE=inactive FAILED=inactive RESTART=no NRESTARTS=0
ndsp-market-prices-updater.timer ENABLED=enabled ACTIVE=active FAILED=active RESTART= NRESTARTS=

## 12) Verify ndip process loop stopped
 107674 root           00:00 grep -E ndip-api-new|app.main:app --host 127.0.0.1 --port 9000|uvicorn app.main
NDIP_ACTIVE_FINAL=inactive
NDIP_FAILED_FINAL=inactive
NDIP_RESTART_POLICY_FINAL=no

## 13) Runtime health after Fix I
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 23m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.6mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m16.2%[39m | [1mram usage[22m: [32m7.5%[39m | [1mlo[22m: ⇓ [32m0.015mb/s[39m ⇑ [32m0.015mb/s[39m | [1meth0[22m: ⇓ [32m0.183mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.194mb/s[39m [90m/[39m [1m[33m82.05%[39m[22m |
API_HEALTH_HTTP_AFTER=200
QUALITY_LIVE_HTTP_AFTER=200
MY_NDSP_HTTP_AFTER=200
ADMIN_NDSP_HTTP_AFTER=200

## 14) Final Evaluation
MARKET_TIMER_ACTIVE_FINAL=active
MARKET_SERVICE_FAILED_FINAL=inactive
NDIP_HEALTH_MONITOR_ACTIVE_FINAL=inactive
NDIP_TELEGRAM_WORKER_ACTIVE_FINAL=inactive
P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_STATUS=OK
FINAL_STATUS=P3_FIX_I_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351
