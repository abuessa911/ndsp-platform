# NDSP V1.3-B1 D2 Safe Ownership Stabilizer — No Updater Run
DATE=2026-07-09T00:30:57+02:00
MODE=SAFE_SYSTEMD_DROPIN_REPAIR_AND_DATA_OWNERSHIP_PATCH
PATCH=V13-B1-D2
TARGET=/var/www/ndsp-my/data/command-center-real.json
SERVICE=ndsp-market-prices-updater.service
DROPIN=/etc/systemd/system/ndsp-market-prices-updater.service.d/50-ndsp-v13-command-center-owner.conf
NO_UPDATER_START=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_PROTECTED_ASSET_CHANGE=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057

## 1) Detect previous B1 partial state
LATEST_B1_REPORT=docs/05-runbooks/NDSP_V13_B1_COMMAND_CENTER_OWNERSHIP_STABILIZER_20260709_002357.md
PREVIOUS_B1_PARTIAL_ABORT=DETECTED

## 2) Preflight runtime health
FAILED_UNITS_COUNT_BEFORE=1
  UNIT                               LOAD   ACTIVE SUB    DESCRIPTION
● ndsp-market-prices-updater.service loaded failed failed NDSP Live Market Prices Updater

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_ACTIVE_BEFORE=failed
MARKET_UPDATER_SERVICE_FAILED_BEFORE=failed
MARKET_UPDATER_TIMER_ACTIVE_BEFORE=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 69m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.7mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.4%[39m | [1mram usage[22m: [32m7.4%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.197mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200
DATA_FRESHNESS_HTTP_BEFORE=200
DATA_FRESHNESS_JSON_HTTP_BEFORE=200

## 3) Backup current state
699f2d9337412ff62590b3e96ec4dd31c5b0011c9da8debdbb17e78caa6c8cd6  /var/www/ndsp-my/data/command-center-real.json
TARGET_BEFORE=/var/www/ndsp-my/data/command-center-real.json OWNER=root GROUP=root MODE=-rw-r--r-- SIZE=46316
BACKUP_FRESHNESS_JSON=/home/nawaf511/ndsp_backups/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057/data-freshness-panel.json.before
BACKUP_EXISTING_DROPIN=/home/nawaf511/ndsp_backups/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057/systemd/50-ndsp-v13-command-center-owner.conf.before
EXISTING_DROPIN_CONTENT_BEGIN
[Service]
ExecStartPost=/usr/bin/test ! -f /var/www/ndsp-my/data/command-center-real.json || /usr/bin/chown nawaf511:nawaf511 /var/www/ndsp-my/data/command-center-real.json
ExecStartPost=/usr/bin/test ! -f /var/www/ndsp-my/data/command-center-real.json || /usr/bin/chmod 0644 /var/www/ndsp-my/data/command-center-real.json
EXISTING_DROPIN_CONTENT_END

## 4) Install safe best-effort drop-in
SAFE_DROPIN_INSTALLED=/etc/systemd/system/ndsp-market-prices-updater.service.d/50-ndsp-v13-command-center-owner.conf
[Service]
ExecStartPost=-/bin/sh -c 'if [ -f "/var/www/ndsp-my/data/command-center-real.json" ]; then /usr/bin/chown nawaf511:nawaf511 "/var/www/ndsp-my/data/command-center-real.json"; /usr/bin/chmod 0644 "/var/www/ndsp-my/data/command-center-real.json"; fi'

## 5) Directly correct current file ownership without running updater
DIRECT_CHOWN_TARGET=OK

## 6) daemon-reload and clean failed state
DAEMON_RELOAD=OK
RESET_FAILED_SERVICE_DONE=ndsp-market-prices-updater.service

## 7) Post ownership state
699f2d9337412ff62590b3e96ec4dd31c5b0011c9da8debdbb17e78caa6c8cd6  /var/www/ndsp-my/data/command-center-real.json
TARGET_AFTER=/var/www/ndsp-my/data/command-center-real.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=46316
TARGET_OWNER_AFTER=nawaf511:nawaf511
TARGET_MODE_AFTER=644

## 8) Regenerate freshness JSON
FRESHNESS_JSON_REGENERATED=/var/www/ndsp-my/data/data-freshness-panel.json

## 9) Freshness JSON summary after D2
OVERALL_STATUS_AFTER_D2=ok
FILES_CHECKED_AFTER_D2=5
STALE_COUNT_AFTER_D2=0
MISSING_REQUIRED_COUNT_AFTER_D2=0
OWNERSHIP_WARNINGS_AFTER_D2=0
READ_ERRORS_AFTER_D2=0
RUNTIME_FAILED_UNITS_COUNT_AFTER_D2=0
NGINX_ACTIVE_AFTER_D2=active
PM2_SERVICE_ACTIVE_AFTER_D2=active
DATA_FILE=data_quality STATUS=fresh AGE_SECONDS=234 OWNER=nawaf511:nawaf511
DATA_FILE=news_impact STATUS=fresh AGE_SECONDS=235 OWNER=nawaf511:nawaf511
DATA_FILE=economic_calendar STATUS=fresh AGE_SECONDS=234 OWNER=nawaf511:nawaf511
DATA_FILE=command_center_real STATUS=fresh AGE_SECONDS=36 OWNER=nawaf511:nawaf511
DATA_FILE=release_evidence STATUS=fresh AGE_SECONDS=1790 OWNER=nawaf511:nawaf511

## 10) Post patch runtime tests
PAGE_HTTP=200
JSON_HTTP=200
RELEASE_EVIDENCE_HTTP_AFTER=200
API_HEALTH_HTTP_AFTER=200
QUALITY_LIVE_HTTP_AFTER=200
MY_NDSP_HTTP_AFTER=200
ADMIN_NDSP_HTTP_AFTER=200
FAILED_UNITS_COUNT_AFTER=0
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
MARKET_UPDATER_SERVICE_ACTIVE_AFTER=activating
MARKET_UPDATER_SERVICE_FAILED_AFTER=activating
MARKET_UPDATER_TIMER_ACTIVE_AFTER=active

## 11) Protected asset checksum check
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 12) Governance wording scan for touched files
GOVERNANCE_HITS_TOUCHED_FILES=0

## 13) Final Evaluation
FRESHNESS_OVERALL_FINAL=ok
OWNERSHIP_WARNINGS_FINAL=0
V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_STATUS=OK
FINAL_STATUS=V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057
