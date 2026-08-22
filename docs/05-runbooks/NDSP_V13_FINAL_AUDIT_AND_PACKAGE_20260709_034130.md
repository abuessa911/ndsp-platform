# NDSP V1.3 Final Audit + Release Package
DATE=2026-07-09T03:41:30+02:00
MODE=V13_FINAL_AUDIT_AND_PACKAGE
MODIFICATIONS=docs_and_release_package_only
NO_RUNTIME_CHANGE=1
NO_REBOOT=1
NO_RESTART=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_CHANGE=1
NO_BUILD=1
STAGE=/tmp/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz

## 1) Required lock chain
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=P3_FINAL_CLEAN_HEALTH_STATUS=OK
LOCK_KEY_OK=P3_FINAL_RELEASE_PACKAGE_STATUS=CREATED
LOCK_KEY_OK=V13_SCOPE_FREEZE_STATUS=CREATED
LOCK_KEY_OK=V13_IMPLEMENTATION_PLAN_STATUS=CREATED
LOCK_KEY_OK=V13_A_RELEASE_EVIDENCE_PAGE_STATUS=OK
LOCK_KEY_OK=V13_B_DATA_FRESHNESS_TRUST_PANEL_STATUS=OK
LOCK_KEY_OK=V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_STATUS=OK
LOCK_KEY_OK=V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_STATUS=OK
LOCK_KEY_OK=V13_C_DECISION_ROOM_UX_COPY_GUIDE_STATUS=OK
LOCK_KEY_OK=V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_STATUS=OK
LOCK_KEY_OK=V13_E_VISUAL_POLISH_HUB_AND_LINK_INTEGRITY_STATUS=OK

## 2) Runtime final health
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE=active
PM2_ENABLED=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 4h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.1%[39m | [1mram usage[22m: [32m7.6%[39m | [1mlo[22m: ⇓ [32m0.013mb/s[39m ⇑ [32m0.013mb/s[39m | [1meth0[22m: ⇓ [32m0.175mb/s[39m ⇑ [32m0.008mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.264mb/s[39m [90m/[39m [1m[33m82.1%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED=inactive
MARKET_UPDATER_TIMER_ACTIVE=active
NDIP_ACTIVE=inactive
NDIP_FAILED=inactive
NDIP_RESTART=no
PM2_NDSP_PORTAL_ONLINE=1

## 3) Endpoint final health
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

## 4) Data freshness final check
COMMAND_CENTER=/var/www/ndsp-my/data/command-center-real.json OWNER=root GROUP=root MODE=-rw-r--r-- SIZE=46314
COMMAND_CENTER_OWNER=root:root
FRESHNESS_OVERALL=ok
FILES_CHECKED=5
STALE_COUNT=0
MISSING_REQUIRED_COUNT=0
OWNERSHIP_WARNINGS=0
READ_ERRORS=0
RUNTIME_FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
PM2_SERVICE_ACTIVE=active
OWNERSHIP_WARNINGS_FINAL=0
READ_ERRORS_FINAL=0

## 5) Protected assets final checksum
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 6) Governance and global script checks
GOVERNANCE_HITS_V13=0
GLOBAL_SCRIPT_HITS_V13_NEW_PAGES=0

## 7) Stage release package
STAGE_CREATED=/tmp/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130

## 8) Create package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz.sha256
a433faadfddbd346ca259994bf4c1bc8f1f13c8c418f68c72380a046b4b6cc58  /home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz

## 9) Final Evaluation
OK_EVALUATION=0
V13_FINAL_CLEAN_HEALTH_STATUS=CHECK_ALERTS
V13_FINAL_RELEASE_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V13_FINAL_AUDIT_AND_PACKAGE_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_V13_FINAL_AUDIT_AND_PACKAGE_20260709_034130.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_RELEASE_PACKAGE_20260709_034130.tar.gz.sha256
