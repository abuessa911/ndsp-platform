# NDSP V1.3-A Release Evidence Page
DATE=2026-07-09T00:01:10+02:00
MODE=CONTROLLED_STATIC_READONLY_PAGE_PATCH
PATCH=V13-A
MODIFICATION=Create release-evidence.html and data/release-evidence.json only
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_SERVICE_CONTROL_FROM_UI=1
NO_SHELL_FROM_BROWSER=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_A_RELEASE_EVIDENCE_PAGE_20260709_000110

## 1) Scope Freeze prerequisite
V13_SCOPE_FREEZE_LOCK=OK

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 39m    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 74.7mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.3%[39m | [1mram usage[22m: [32m7.5%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.01mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.3mb/s[39m [90m/[39m [1m[33m82.07%[39m[22m |
API_HEALTH_HTTP_BEFORE=200
QUALITY_LIVE_HTTP_BEFORE=200
MY_NDSP_HTTP_BEFORE=200
ADMIN_NDSP_HTTP_BEFORE=200

## 3) Backup target files
BACKUP_PAGE=NO_EXISTING_PAGE
BACKUP_JSON=NO_EXISTING_JSON

## 4) Generate release evidence JSON
JSON_CREATED=/var/www/ndsp-my/data/release-evidence.json

## 5) Generate release evidence HTML
PAGE_CREATED=/var/www/ndsp-my/release-evidence.html

## 6) Ownership and permissions
FILE=/var/www/ndsp-my/release-evidence.html OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=6962
FILE=/var/www/ndsp-my/data/release-evidence.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=8840

## 7) Post patch tests
PAGE_HTTP=200
JSON_HTTP=200
API_HEALTH_HTTP_AFTER=200
QUALITY_LIVE_HTTP_AFTER=200
MY_NDSP_HTTP_AFTER=200
ADMIN_NDSP_HTTP_AFTER=200
FAILED_UNITS_COUNT_AFTER=0
NGINX_ACTIVE_AFTER=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active

## 8) Protected asset checksum check
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 9) Governance wording scan for new files
GOVERNANCE_HITS_NEW_FILES=0

## 10) Final Evaluation
V13_A_RELEASE_EVIDENCE_PAGE_STATUS=OK
FINAL_STATUS=V13_A_RELEASE_EVIDENCE_PAGE_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_V13_A_RELEASE_EVIDENCE_PAGE_20260709_000110.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_A_RELEASE_EVIDENCE_PAGE_20260709_000110
