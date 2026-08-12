# NDSP V1.6-F / P6-F Architecture Map Static Page
DATE=2026-07-09T11:52:57+02:00
MODE=CONTROLLED_STATIC_ARCHITECTURE_MAP_PATCH
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V16_F_ARCHITECTURE_MAP_STATIC_PAGE_20260709_115257.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V16_F_ARCHITECTURE_MAP_STATIC_PAGE_20260709_115257
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz

## 1) Required V1.6/P6 final lock
V16_P6_FINAL_LOCK=OK

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 12h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.7mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.8%[39m | [1mram usage[22m: [32m8.3%[39m | [1mlo[22m: ⇓ [32m0.011mb/s[39m ⇑ [32m0.011mb/s[39m | [1meth0[22m: ⇓ [32m0.11mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.304mb/s[39m ⇑ [32m0.244mb/s[39m [90m/[39m [1m[33m82.43%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline endpoint checks
HTTP_BASE_completed_live=200
HTTP_BASE_api_health=200
HTTP_BASE_quality_live=200
HTTP_BASE_v16_live_page=200
HTTP_BASE_my_home=200
HTTP_BASE_v15_completed=200
HTTP_BASE_completed_live_latest=200
HTTP_BASE_v16_completed=200
BASE_ENDPOINTS_OK=1

## 4) Backup target files
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/architecture-map.html
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/assets/ndsp-v16-architecture-map.svg
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/ndsp-architecture-map.json

## 5) Generate static architecture files
FILE=/var/www/ndsp-my/architecture-map.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=1043
FILE=/var/www/ndsp-my/assets/ndsp-v16-architecture-map.svg OWNER=nawaf511:nawaf511 MODE=644 SIZE=5549
FILE=/var/www/ndsp-my/data/ndsp-architecture-map.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=729

## 6) Post patch HTTP checks
HTTP_completed_live=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_architecture_json=200
HTTP_v16_live_page=200
HTTP_my_home=200
HTTP_v15_completed=200
HTTP_architecture_svg=200
HTTP_architecture_page=200
HTTP_v16_completed=200
LINK_INTEGRITY_OK=1

## 7) Runtime after patch
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 12h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.7mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.8%[39m | [1mram usage[22m: [32m8.3%[39m | [1mlo[22m: ⇓ [32m0.011mb/s[39m ⇑ [32m0.011mb/s[39m | [1meth0[22m: ⇓ [32m0.11mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.304mb/s[39m ⇑ [32m0.244mb/s[39m [90m/[39m [1m[33m82.43%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive

## 8) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_ARCHITECTURE_FILES=0
GLOBAL_SCRIPT_HITS_ARCHITECTURE_PAGE=0

## 9) Stage evidence package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz.sha256
57e586156e6ad46219e5641abb348ae92658e6cc3a7fb0848aa8744640114220  /home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz

## 10) Final Evaluation
OK_EVALUATION=1
V16_F_ARCHITECTURE_MAP_STATIC_PAGE_STATUS=OK
V16_F_ARCHITECTURE_MAP_PACKAGE_STATUS=CREATED
FINAL_STATUS=V16_F_ARCHITECTURE_MAP_STATIC_PAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V16_F_ARCHITECTURE_MAP_STATIC_PAGE_20260709_115257.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz.sha256
