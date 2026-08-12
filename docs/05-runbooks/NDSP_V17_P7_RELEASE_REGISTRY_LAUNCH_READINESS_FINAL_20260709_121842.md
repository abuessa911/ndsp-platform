# NDSP V1.7 / P7 One-Shot — Release Registry + Launch Readiness Center + Final Package
DATE=2026-07-09T12:18:42+02:00
MODE=V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL
MODIFICATIONS=static_pages_json_docs_package_only
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz

## 1) Required locks
REALITY_LOCK_EXISTS=1
REALITY_LOCK_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842/NDSP_CURRENT_REALITY_LOCK_AR.before
V14_FINAL_LOCK=1
V15_FINAL_LOCK=1
V16_FINAL_LOCK=1
V16F_FINAL_LOCK=1

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 12h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.5%[39m | [1mram usage[22m: [32m8.3%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ [32m0.019mb/s[39m ⇑ [32m0.265mb/s[39m [90m/[39m [1m[33m82.44%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_BEFORE=active
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Endpoint readiness matrix
HTTP_completed_live=200
HTTP_api_health=200
HTTP_admin_home=200
HTTP_v16_live_adapter_page=200
HTTP_v14_hub=200
HTTP_my_home=200
HTTP_completed_decisions_review=200
HTTP_v15_completed=200
HTTP_release_evidence=200
HTTP_architecture_map_svg=200
HTTP_completed_live_latest=200
HTTP_architecture_map_json=200
HTTP_quality_live_ETHUSDT=200
HTTP_decision_room_guide=200
HTTP_data_freshness=200
HTTP_v15_completed_latest=200
HTTP_architecture_map_page=200
HTTP_v15_completed_v15=200
HTTP_v16_completed=200
HTTP_v15_api_bridge_page=200
ENDPOINTS_OK=1

## 4) Backup target pages/json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/launch-readiness.html
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/release-registry.html
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/launch-readiness.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/release-registry.json

## 5) Release package registry verification
PACKAGE_TOTAL=19
PACKAGE_SHA_OK=19
PACKAGE_SHA_MISSING=0
PACKAGE_SHA_BAD=0
PACKAGE_MATRIX=/tmp/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842/checks/package_matrix.tsv

## 6) Generate Release Registry and Launch Readiness pages
RELEASE_REGISTRY_JSON_CREATED=1
LAUNCH_READINESS_JSON_CREATED=1
RELEASE_REGISTRY_PAGE_CREATED=1
LAUNCH_READINESS_PAGE_CREATED=1
REGISTRY_PACKAGES_TOTAL=19
REGISTRY_PACKAGE_SHA_BAD=0
LAUNCH_ENDPOINT_TOTAL=20
LAUNCH_ENDPOINT_OK_COUNT=20
FILE=/var/www/ndsp-my/launch-readiness.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=6648
FILE=/var/www/ndsp-my/release-registry.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=4576
FILE=/var/www/ndsp-my/data/launch-readiness.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=4810
FILE=/var/www/ndsp-my/data/release-registry.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=10189

## 7) Post patch endpoint checks
HTTP_POST_completed_live=200
HTTP_POST_release_registry_page=200
HTTP_POST_api_health=200
HTTP_POST_quality_live=200
HTTP_POST_my_home=200
HTTP_POST_release_registry_json=200
HTTP_POST_launch_readiness_page=200
HTTP_POST_launch_readiness_json=200
HTTP_POST_architecture_map_page=200
HTTP_POST_v16_completed=200
NEW_ENDPOINTS_OK=1

## 8) Runtime after patch
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 12h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.5%[39m | [1mram usage[22m: [32m8.3%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ [32m0.019mb/s[39m ⇑ [32m0.265mb/s[39m [90m/[39m [1m[33m82.44%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_AFTER=active
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive

## 9) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V17_FILES=0
GLOBAL_SCRIPT_HITS_V17_PAGES=0

## 10) Stage final P7 package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz.sha256
e1259288c9d788a9615bd3e48f9ccf805924f8ecf1427ad0e0a2f80a69f3b1d2  /home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz

## 11) Final Evaluation
OK_EVALUATION=1
V17_P7_RELEASE_REGISTRY_STATUS=OK
V17_P7_LAUNCH_READINESS_CENTER_STATUS=OK
V17_P7_FINAL_PACKAGE_STATUS=CREATED
FINAL_STATUS=V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz.sha256
