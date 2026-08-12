# NDSP V1.5 / P5 D2 — Fix API Bridge Nginx Target + Final Package
DATE=2026-07-09T09:41:55+02:00
MODE=V15_P5_D2_FIX_API_BRIDGE_NGINX_TARGET_FINAL_PACKAGE
CONTROLLED_NGINX_CHANGE=1
STATIC_JSON_API_BRIDGE=1
NO_BACKEND_ENGINE_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_DB_SCHEMA_CHANGE=1
NO_PROTECTED_ASSET_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V15_P5_D2_FIX_API_BRIDGE_NGINX_TARGET_FINAL_PACKAGE_20260709_094155.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V15_P5_D2_FIX_API_BRIDGE_20260709_094155
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz

## 1) Required V1.4 final lock and previous V15 alert
V14_FINAL_LOCK=OK
LATEST_V15_ALERT_REPORT=docs/05-runbooks/NDSP_V15_P5_ONE_SHOT_READONLY_API_BRIDGE_FINAL_PACKAGE_20260709_092500.md
PREVIOUS_V15_ALERT_CONFIRMED=1

## 2) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 10h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.2mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.6%[39m | [1mram usage[22m: [32m8.2%[39m | [1mlo[22m: ⇓ [32m0.01mb/s[39m ⇑ [32m0.01mb/s[39m | [1meth0[22m: ⇓ [32m0.083mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.183mb/s[39m [90m/[39m [1m[33m82.42%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_BEFORE=active
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline endpoints
API_COMPLETED_DECISIONS_HTTP_BEFORE=404
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_HTTP_BEFORE=200
V15_JSON_HTTP_BEFORE=200
V15_PAGE_HTTP_BEFORE=200

## 4) Ensure V15 JSON and page exist
V15_D2_JSON_PAGE_ENSURED=1
V15_D2_ITEMS_COUNT=1
FILE=/var/www/ndsp-my/data/completed-decisions-v15-api.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=2747
FILE=/var/www/ndsp-my/v15-api-bridge.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=1597

## 5) Backup Nginx and collect loaded config
BACKUP_NGINX_DIR=/home/nawaf511/ndsp_backups/NDSP_V15_P5_D2_FIX_API_BRIDGE_20260709_094155/etc-nginx.before
NGINX_T_BEFORE=/tmp/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155/nginx_T_before.txt

## 6) Patch all loaded api.ndsp.app server blocks
LOADED_NGINX_FILES=13
API_NGINX_FILES_SEEN=5
API_SERVER_BLOCKS_TARGETED=6
MODIFIED_NGINX_FILES_COUNT=4
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-my.ndsp.app-final.conf
MODIFIED_NGINX_FILE=/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf
MODIFIED_NGINX_FILE=/etc/nginx/sites-enabled/bot.ndsp.app
NGINX_PATCH_PYTHON_EXIT=0

## 7) Nginx test and reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_TEST_AFTER_PATCH=OK
NGINX_RELOAD=OK

## 8) Post-patch endpoint tests
HTTP_api_health=200
HTTP_v15_page=200
HTTP_quality_live=200
HTTP_completed_decisions_v15=200
HTTP_completed_decisions_latest=200
HTTP_my_home=200
HTTP_completed_decisions=200
HTTP_v14_page=200
HTTP_v15_json=200
LINK_INTEGRITY_OK=1
V15_API_JSON_OK=1

## 9) Runtime after patch
FAILED_UNITS_COUNT_AFTER=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 10h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.2mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14.3%[39m | [1mram usage[22m: [32m8.1%[39m | [1mlo[22m: ⇓ [32m0.007mb/s[39m ⇑ [32m0.007mb/s[39m | [1meth0[22m: ⇓ [32m0.107mb/s[39m ⇑ [32m0.004mb/s[39m | [1mdisk[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.336mb/s[39m [90m/[39m [1m[33m82.42%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_AFTER=active
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive

## 10) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V15_FILES=0
GLOBAL_SCRIPT_HITS_V15_PAGE=0

## 11) Stage final package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz.sha256
c3a0d73e63f66f40475b44cafed16f80c9546cb9685b1c8dd4b0262ac1607b39  /home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz

## 12) Final Evaluation
OK_EVALUATION=1
V15_P5_D2_READONLY_PUBLIC_API_BRIDGE_STATUS=OK
V15_P5_D2_NGINX_API_ROUTE_STATUS=OK
V15_P5_D2_FINAL_AUDIT_PACKAGE_STATUS=CREATED
FINAL_STATUS=V15_P5_D2_READONLY_API_BRIDGE_FINAL_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V15_P5_D2_FIX_API_BRIDGE_NGINX_TARGET_FINAL_PACKAGE_20260709_094155.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz.sha256
