# NDSP V1.3-B2 Data Freshness Stabilization Audit — Read-only
DATE=2026-07-09T00:37:52+02:00
MODE=READ_ONLY_STABILIZATION_AUDIT
PATCH=V13-B2
MODIFICATIONS=Report_only
NO_UPDATER_START=1
NO_RESET_FAILED=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1

## 1) Required D2 lock
V13_B1_D2_LOCK=OK

## 2) Stabilization wait
WAIT_SECONDS=120

## 3) systemd state after wait
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_AFTER_WAIT=0
MARKET_UPDATER_SERVICE_ACTIVE_AFTER_WAIT=inactive
MARKET_UPDATER_SERVICE_FAILED_AFTER_WAIT=inactive
MARKET_UPDATER_TIMER_ACTIVE_AFTER_WAIT=active
MARKET_UPDATER_TIMER_ENABLED_AFTER_WAIT=enabled
○ ndsp-market-prices-updater.service - NDSP Live Market Prices Updater
     Loaded: loaded (/etc/systemd/system/ndsp-market-prices-updater.service; static)
    Drop-In: /etc/systemd/system/ndsp-market-prices-updater.service.d
             └─30-ndsp-official-runtime-source.conf, 40-ndsp-p3-after-postgresql.conf, 50-ndsp-v13-command-center-owner.conf
     Active: inactive (dead) since Thu 2026-07-09 00:39:08 CEST; 44s ago
TriggeredBy: ● ndsp-market-prices-updater.timer
    Process: 324143 ExecStart=/usr/bin/python3 /usr/local/bin/ndsp_live_market_prices_updater.py (code=exited, status=0/SUCCESS)
    Process: 324201 ExecStartPost=/bin/sh -c if [ -f "/var/www/ndsp-my/data/command-center-real.json" ]; then /usr/bin/chown nawaf511:nawaf511 "/var/www/ndsp-my/data/command-center-real.json"; /usr/bin/chmod 0644 "/var/www/ndsp-my/data/command-center-real.json"; fi (code=exited, status=0/SUCCESS)
   Main PID: 324143 (code=exited, status=0/SUCCESS)
        CPU: 558ms

يوليو 09 00:39:06 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 09 00:39:06 vmi2934783 sudo[324154]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 09 00:39:06 vmi2934783 sudo[324154]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 09 00:39:06 vmi2934783 sudo[324154]: pam_unix(sudo:session): session closed for user postgres
يوليو 09 00:39:08 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 09 00:39:08 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
● ndsp-market-prices-updater.timer - Run NDSP Live Market Prices Updater every minute
     Loaded: loaded (/etc/systemd/system/ndsp-market-prices-updater.timer; enabled; preset: enabled)
     Active: active (waiting) since Wed 2026-07-08 23:21:45 CEST; 1h 18min ago
    Trigger: Thu 2026-07-09 00:40:06 CEST; 13s left
   Triggers: ● ndsp-market-prices-updater.service

يوليو 08 23:21:45 vmi2934783 systemd[1]: Started ndsp-market-prices-updater.timer - Run NDSP Live Market Prices Updater every minute.
MARKET_UPDATER_STILL_ACTIVATING_ALERT=0

## 4) Ownership and freshness
TARGET=/var/www/ndsp-my/data/command-center-real.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=46316
TARGET_OWNER=nawaf511:nawaf511
FRESHNESS_OVERALL=ok
FILES_CHECKED=5
STALE_COUNT=0
MISSING_REQUIRED_COUNT=0
OWNERSHIP_WARNINGS=0
READ_ERRORS=0
RUNTIME_FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
PM2_SERVICE_ACTIVE=active
DATA_FILE=data_quality STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=234
DATA_FILE=news_impact STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=235
DATA_FILE=economic_calendar STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=234
DATA_FILE=command_center_real STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=36
DATA_FILE=release_evidence STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=1790
FRESHNESS_OVERALL_FINAL=ok
OWNERSHIP_WARNINGS_FINAL=0
READ_ERRORS_FINAL=0

## 5) Runtime endpoints
NGINX_ACTIVE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE=active
PM2_ENABLED=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 77m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.2mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.8%[39m | [1mram usage[22m: [32m7.6%[39m | [1mlo[22m: ⇓ [32m0.007mb/s[39m ⇑ [32m0.007mb/s[39m | [1meth0[22m: ⇓ [32m0.108mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.221mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200
RELEASE_EVIDENCE_HTTP=200
DATA_FRESHNESS_PAGE_HTTP=200
DATA_FRESHNESS_JSON_HTTP=200

## 6) Protected asset checksum check
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 7) Final Evaluation
OK_EVALUATION=1
V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_STATUS=OK
FINAL_STATUS=V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_READONLY_20260709_003752.md
