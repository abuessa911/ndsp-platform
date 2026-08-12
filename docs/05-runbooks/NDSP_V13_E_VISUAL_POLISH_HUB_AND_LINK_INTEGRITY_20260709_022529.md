# NDSP V1.3-E Visual Polish Hub + Link Integrity
DATE=2026-07-09T02:25:29+02:00
MODE=CONTROLLED_STATIC_READONLY_VISUAL_HUB_PATCH
PATCH=V13-E
MODIFICATION=Create v13-experience.html and data/v13-experience-hub.json only
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_SERVICE_CONTROL_FROM_UI=1
NO_SHELL_FROM_BROWSER=1
NO_PROTECTED_ASSET_CHANGE=1
NO_GLOBAL_SCRIPT_STACKING=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_E_VISUAL_POLISH_HUB_AND_LINK_INTEGRITY_20260709_022529

## 1) V13-D prerequisite
V13_D_LOCK=OK

## 2) Preflight runtime health
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 3h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.7%[39m | [1mram usage[22m: [32m7.4%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.283mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 3) Backup target files
BACKUP_PAGE=NO_EXISTING_PAGE
BACKUP_JSON=NO_EXISTING_JSON

## 4) Generate V13 experience hub JSON
JSON_CREATED=/var/www/ndsp-my/data/v13-experience-hub.json

## 5) Generate V13 experience hub HTML
PAGE_CREATED=/var/www/ndsp-my/v13-experience.html

## 6) Ownership and permissions
FILE=/var/www/ndsp-my/v13-experience.html OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=5552
FILE=/var/www/ndsp-my/data/v13-experience-hub.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=1709

## 7) Link integrity tests
HTTP_v13_experience_json=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_decision_room_copy_json=200
HTTP_completed_decisions_review=200
HTTP_completed_decisions_config_json=200
HTTP_release_evidence=200
HTTP_home=200
HTTP_decision_room_guide=200
HTTP_data_freshness=200
HTTP_admin=200
HTTP_data_freshness_json=200
HTTP_release_evidence_json=200
HTTP_v13_experience=200
LINK_INTEGRITY_OK=1

## 8) Runtime after patch
FAILED_UNITS_COUNT_AFTER=0
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 3h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.7%[39m | [1mram usage[22m: [32m7.4%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.004mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.283mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
MARKET_UPDATER_TIMER_ACTIVE_AFTER=active

## 9) Protected asset checksum check
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 10) Governance wording scan for new files
GOVERNANCE_HITS_NEW_FILES=0

## 11) Global script stacking check
