# NDSP V1.4 BCDE-D2 — Reconcile V14-A D2 Lock + Static Completion + Final Package
DATE=2026-07-09T09:07:10+02:00
MODE=V14_BCDE_D2_RECONCILE_A_D2_LOCK_AND_FINAL_PACKAGE
MODIFICATIONS=static_pages_json_docs_lock_package_only
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V14_BCDE_D2_RECONCILE_A_D2_LOCK_AND_FINAL_PACKAGE_20260709_090710.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V14_BCDE_D2_STATIC_COMPLETION_20260709_090710
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz

## 1) Reconcile V14-A D2 lock from evidence if missing
LOCK_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V14_BCDE_D2_STATIC_COMPLETION_20260709_090710/NDSP_CURRENT_REALITY_LOCK_AR.before
V14_A_D2_LOCK=OK
LATEST_A_D2_REPORT=docs/05-runbooks/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_READONLY_FAST_20260709_084807.md
LATEST_A_D2_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_FAST_20260709_084807.tar.gz
LATEST_A_D2_SHA_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_FAST_20260709_084807.tar.gz.sha256
A_D2_REPORT_EXISTS=1
DISCOVERY_RECOMMENDATION=STATIC_OR_FILE_ADAPTER_CANDIDATE
NEXT_PATCH_RECOMMENDATION=V14-B_STATIC_JSON_ADAPTER_AFTER_MANUAL_REVIEW
V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_STATUS=OK
V14_A_D2_EVIDENCE_PACKAGE_STATUS=CREATED
FINAL_STATUS=V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_READONLY_OK
REALITY_LOCK_STATUS=UPDATED
A_D2_REPORT_FINAL_STATUS_OK=1
A_D2_PACKAGE_EXISTS=1
A_D2_SHA_ACTUAL=cbe1b718b371e2d19eb77eb8f2d9f1e49a410140234839a9df3ae45a8cad7ded
A_D2_SHA_EXPECTED=cbe1b718b371e2d19eb77eb8f2d9f1e49a410140234839a9df3ae45a8cad7ded
A_D2_SHA_MATCH=1

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 9h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 72.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.7%[39m | [1mram usage[22m: [32m8.1%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.168mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.195mb/s[39m [90m/[39m [1m[33m82.41%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_BEFORE=active
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Backup target files
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/completed-decisions-v14-adapter.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/completed-decisions-v14.html
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/v14-experience.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/v14-experience.html
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/v14-error-states.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/data/v14-final-evidence.json
BACKUP_FILE=NO_EXISTING_/var/www/ndsp-my/v14-final-evidence.html

## 4) Generate V14 static adapter, hub, UX states, and final evidence shell
STATIC_GENERATION_STATUS=OK
FILE=/var/www/ndsp-my/data/completed-decisions-v14-adapter.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=3576
FILE=/var/www/ndsp-my/completed-decisions-v14.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=3738
FILE=/var/www/ndsp-my/data/v14-experience.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=953
FILE=/var/www/ndsp-my/v14-experience.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=2957
FILE=/var/www/ndsp-my/data/v14-error-states.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=804
FILE=/var/www/ndsp-my/data/v14-final-evidence.json OWNER=nawaf511:nawaf511 MODE=644 SIZE=421
FILE=/var/www/ndsp-my/v14-final-evidence.html OWNER=nawaf511:nawaf511 MODE=644 SIZE=2615

## 5) Post-patch HTTP tests
HTTP_completed_v14_json=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_admin_home=200
HTTP_v14_final_json=200
HTTP_v13_completed_review=200
HTTP_my_home=200
HTTP_release_evidence=200
HTTP_completed_v14_page=200
HTTP_v14_hub_json=200
HTTP_v14_final_page=200
HTTP_v14_hub_page=200
HTTP_data_freshness=200
HTTP_v14_error_json=200
LINK_INTEGRITY_OK=1

## 6) Runtime after patch
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 9h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 72.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.7%[39m | [1mram usage[22m: [32m8.1%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.168mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.195mb/s[39m [90m/[39m [1m[33m82.41%[39m[22m |
MARKET_UPDATER_TIMER_ACTIVE_AFTER=active
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive

## 7) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_NEW_V14_FILES=0
GLOBAL_SCRIPT_HITS_NEW_V14_PAGES=0

## 8) Update final evidence JSON after audit
FINAL_EVIDENCE_JSON_UPDATED=OK

## 9) Stage V14 final package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz.sha256
99e03b6413c6037293485b290d1ad4643e71cf7067ef4b2079a2a29438e7485a  /home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz

## 10) Final Evaluation
OK_EVALUATION=1
V14_A_D2_LOCK_RECONCILE_STATUS=OK
V14_B_STATIC_COMPLETED_DECISIONS_ADAPTER_STATUS=OK
V14_C_PORTAL_HUB_STATUS=OK
V14_D_EMPTY_ERROR_STATE_POLISH_STATUS=OK
V14_E_FINAL_AUDIT_PACKAGE_STATUS=CREATED
FINAL_STATUS=V14_BCDE_D2_STATIC_COMPLETION_FINAL_PACKAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V14_BCDE_D2_RECONCILE_A_D2_LOCK_AND_FINAL_PACKAGE_20260709_090710.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz.sha256
