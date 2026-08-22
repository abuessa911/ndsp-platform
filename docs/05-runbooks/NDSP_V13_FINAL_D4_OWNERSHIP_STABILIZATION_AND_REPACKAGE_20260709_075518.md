# NDSP V1.3 Final D4 — Ownership Stabilization + Repackage
DATE=2026-07-09T07:55:18+02:00
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
REPORT=docs/05-runbooks/NDSP_V13_FINAL_D4_OWNERSHIP_STABILIZATION_AND_REPACKAGE_20260709_075518.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz

## 1) Preflight
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 8h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 71.5mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.5%[39m | [1mram usage[22m: [32m7.7%[39m | [1mlo[22m: ⇓ [32m0.005mb/s[39m ⇑ [32m0.005mb/s[39m | [1meth0[22m: ⇓ [32m0.023mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.243mb/s[39m [90m/[39m [1m[33m82.11%[39m[22m |

## 2) Backup
COMMAND_CENTER_BEFORE=/var/www/ndsp-my/data/command-center-real.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=46290

## 3) Install safe timer fixer and market updater postfix
FIXER_SERVICE_INSTALLED=/etc/systemd/system/ndsp-command-center-owner-fixer.service
FIXER_TIMER_INSTALLED=/etc/systemd/system/ndsp-command-center-owner-fixer.timer
MARKET_POSTFIX_DROPIN_INSTALLED=/etc/systemd/system/ndsp-market-prices-updater.service.d/95-ndsp-command-center-owner-postfix.conf
Failed to disable unit: Unit file ndsp-command-center-owner-fixer.path does not exist.
Failed to reset failed state of unit ndsp-command-center-owner-fixer.path: Unit ndsp-command-center-owner-fixer.path not loaded.
OWNER_FIXER_TIMER_ENABLE_NOW=OK

## 4) Stabilization loop
STABILIZATION_ATTEMPT=1
STABILIZATION_OWNER_AFTER_ATTEMPT_1=nawaf511:nawaf511
COMMAND_CENTER_OWNER_AFTER_STABILIZATION=root:root
COMMAND_CENTER_MODE_AFTER_STABILIZATION=644
OWNER_FIXER_TIMER_ACTIVE=active
OWNER_FIXER_TIMER_ENABLED=enabled
OWNER_FIXER_SERVICE_FAILED=inactive

## 5) Regenerate freshness JSON after final owner correction
FRESHNESS_OVERALL=warning
FILES_CHECKED=5
STALE_COUNT=0
MISSING_REQUIRED_COUNT=0
OWNERSHIP_WARNINGS=1
READ_ERRORS=0
RUNTIME_FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
PM2_SERVICE_ACTIVE=active
DATA_FILE=data_quality STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=177
DATA_FILE=news_impact STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=177
DATA_FILE=economic_calendar STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=177
DATA_FILE=command_center_real STATUS=fresh_with_ownership_warning OWNER=root:root AGE_SECONDS=1
DATA_FILE=release_evidence STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=28456
OWNERSHIP_WARNINGS_FINAL=1
READ_ERRORS_FINAL=0
RUNTIME_FAILED_IN_FRESHNESS_JSON=0

## 6) Endpoint and runtime final audit
HTTP_v13_experience_json=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_decision_room_copy_json=200
HTTP_admin_home=200
HTTP_my_home=200
HTTP_completed_decisions_review=200
HTTP_completed_decisions_config_json=200
HTTP_release_evidence=200
HTTP_decision_room_guide=200
HTTP_data_freshness=200
HTTP_data_freshness_json=200
HTTP_release_evidence_json=200
HTTP_v13_experience=200
LINK_INTEGRITY_OK=1
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 8h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 71.5mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m15.6%[39m | [1mram usage[22m: [32m7.8%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.156mb/s[39m ⇑ [32m0.008mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.369mb/s[39m [90m/[39m [1m[33m82.11%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED=inactive
MARKET_UPDATER_TIMER_ACTIVE=active
NDIP_ACTIVE=inactive
NDIP_FAILED=inactive
NDIP_RESTART=no

## 7) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V13=0
GLOBAL_SCRIPT_HITS_V13_NEW_PAGES=0

## 8) Stage release package
STAGE_CREATED=/tmp/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518

## 9) Create D4 package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz.sha256
6f8c22349987b8890b32ea9a8f3359d11b0383ef153dcb9dfdb440109b402caa  /home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz

## 10) Final Evaluation
OK_EVALUATION=0
V13_FINAL_D4_CLEAN_HEALTH_STATUS=CHECK_ALERTS
V13_FINAL_RELEASE_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V13_FINAL_D4_AUDIT_AND_PACKAGE_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_V13_FINAL_D4_OWNERSHIP_STABILIZATION_AND_REPACKAGE_20260709_075518.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D4_RELEASE_PACKAGE_20260709_075518.tar.gz.sha256
