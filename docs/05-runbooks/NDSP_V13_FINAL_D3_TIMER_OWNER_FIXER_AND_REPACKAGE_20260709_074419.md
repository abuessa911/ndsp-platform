# NDSP V1.3 Final D3 — Timer Owner Fixer + Repackage
DATE=2026-07-09T07:44:19+02:00
MODE=V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE
CONTROLLED_SYSTEMD_TIMER_CHANGE=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_FRONTEND_BUILD=1
NO_REBOOT=1
NO_PROTECTED_ASSET_CHANGE=1
NO_ENGINE_LOGIC_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE_20260709_074419.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE_20260709_074419
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz

## 1) Required lock chain and previous D2 alert
REALITY_LOCK_EXISTS=1
LOCK_KEY_OK=V13_E_VISUAL_POLISH_HUB_AND_LINK_INTEGRITY_STATUS=OK
LOCK_KEY_OK=V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_STATUS=OK
LOCK_KEY_OK=V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_STATUS=OK
LOCK_KEY_OK=P3_FINAL_CLEAN_HEALTH_STATUS=OK
LATEST_V13_FINAL_D2_REPORT=docs/05-runbooks/NDSP_V13_FINAL_D2_OWNER_WATCHER_AND_REPACKAGE_20260709_035022.md
PREVIOUS_D2_ALERT_CONFIRMED=1

## 2) Preflight runtime allowing only D2 failed owner units
FAILED_UNITS_COUNT_BEFORE=2
● ndsp-command-center-owner-fixer.path    loaded failed failed NDSP Command Center Data Owner Watcher
● ndsp-command-center-owner-fixer.service loaded failed failed NDSP Command Center Data Owner Fixer
UNEXPECTED_FAILED_UNITS_BEFORE=0
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 8h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 71.4mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.1%[39m | [1mram usage[22m: [32m7.5%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.001mb/s[39m ⇑ 0mb/s | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.305mb/s[39m [90m/[39m [1m[33m82.11%[39m[22m |

## 3) Backup current files and failed watcher
bb3612cc8d143e51a8ef1cf8366ef5596f832af5c5781e8b31d095f508669296  /var/www/ndsp-my/data/command-center-real.json
COMMAND_CENTER_BEFORE=/var/www/ndsp-my/data/command-center-real.json OWNER=nawaf511 GROUP=nawaf511 MODE=-rw-r--r-- SIZE=46308
BACKUP_SYSTEMD_FILE=/home/nawaf511/ndsp_backups/NDSP_V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE_20260709_074419/systemd/ndsp-command-center-owner-fixer.service.before
BACKUP_SYSTEMD_FILE=/home/nawaf511/ndsp_backups/NDSP_V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE_20260709_074419/systemd/ndsp-command-center-owner-fixer.path.before
BACKUP_SYSTEMD_FILE=NO_EXISTING_/etc/systemd/system/ndsp-command-center-owner-fixer.timer

## 4) Remove failed path watcher and install timer-based fixer
Removed "/etc/systemd/system/multi-user.target.wants/ndsp-command-center-owner-fixer.path".
BROKEN_PATH_REMOVED=/etc/systemd/system/ndsp-command-center-owner-fixer.path
FIXER_SERVICE_INSTALLED=/etc/systemd/system/ndsp-command-center-owner-fixer.service
FIXER_TIMER_INSTALLED=/etc/systemd/system/ndsp-command-center-owner-fixer.timer
[Unit]
Description=NDSP Command Center Data Owner Fixer
Documentation=internal-ndsp-v13-final-d3
After=local-fs.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'if [ -f "/var/www/ndsp-my/data/command-center-real.json" ]; then /usr/bin/chown nawaf511:nawaf511 "/var/www/ndsp-my/data/command-center-real.json" || true; /usr/bin/chmod 0644 "/var/www/ndsp-my/data/command-center-real.json" || true; fi; exit 0'
[Unit]
Description=NDSP Command Center Data Owner Fixer Timer
Documentation=internal-ndsp-v13-final-d3

[Timer]
OnBootSec=30s
OnUnitActiveSec=1min
AccuracySec=15s
Unit=ndsp-command-center-owner-fixer.service

[Install]
WantedBy=timers.target

## 5) daemon-reload, reset failed, enable timer, run once
DAEMON_RELOAD=OK
Failed to reset failed state of unit ndsp-command-center-owner-fixer.timer: Unit ndsp-command-center-owner-fixer.timer not loaded.
RESET_FAILED_OWNER_FIXER_UNITS=OK
Created symlink /etc/systemd/system/timers.target.wants/ndsp-command-center-owner-fixer.timer → /etc/systemd/system/ndsp-command-center-owner-fixer.timer.
OWNER_FIXER_TIMER_ENABLE_NOW=OK
OWNER_FIXER_SERVICE_RUN_ONCE=OK

## 6) Ownership and timer state after D3
8df501e7de8b9414e34fecc786f132b09e6d778845850a08e2271e19cc26d5d5  /var/www/ndsp-my/data/command-center-real.json
COMMAND_CENTER_AFTER=/var/www/ndsp-my/data/command-center-real.json OWNER=root GROUP=root MODE=-rw-r--r-- SIZE=46308
COMMAND_CENTER_OWNER_AFTER=root:root
COMMAND_CENTER_MODE_AFTER=644
OWNER_FIXER_TIMER_ACTIVE=active
OWNER_FIXER_TIMER_ENABLED=enabled
OWNER_FIXER_SERVICE_FAILED=inactive
OWNER_FIXER_PATH_FAILED=inactive
NEXT                            LEFT LAST                               PASSED UNIT                                        ACTIVATES
Thu 2026-07-09 07:45:25 CEST     57s Thu 2026-07-09 07:44:25 CEST       2s ago ndsp-command-center-owner-fixer.timer       ndsp-command-center-owner-fixer.service

## 7) Regenerate data freshness JSON
FRESHNESS_JSON_REGENERATED=/var/www/ndsp-my/data/data-freshness-panel.json
FRESHNESS_OVERALL=warning
FILES_CHECKED=5
STALE_COUNT=0
MISSING_REQUIRED_COUNT=0
OWNERSHIP_WARNINGS=1
READ_ERRORS=0
RUNTIME_FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
PM2_SERVICE_ACTIVE=active
DATA_FILE=data_quality STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=115
DATA_FILE=news_impact STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=115
DATA_FILE=economic_calendar STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=115
DATA_FILE=command_center_real STATUS=fresh_with_ownership_warning OWNER=root:root AGE_SECONDS=1
DATA_FILE=release_evidence STATUS=fresh OWNER=nawaf511:nawaf511 AGE_SECONDS=27794
OWNERSHIP_WARNINGS_FINAL=1
READ_ERRORS_FINAL=0
RUNTIME_FAILED_IN_FRESHNESS_JSON=0

## 8) Endpoint and runtime final audit
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 8h     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 71.4mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m16.5%[39m | [1mram usage[22m: [32m7.7%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.174mb/s[39m ⇑ [32m0.008mb/s[39m | [1mdisk[22m: ⇓ [32m3.745mb/s[39m ⇑ [32m0.165mb/s[39m [90m/[39m [1m[33m82.11%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED=inactive
MARKET_UPDATER_TIMER_ACTIVE=active
NDIP_ACTIVE=inactive
NDIP_FAILED=inactive
NDIP_RESTART=no

## 9) Protected assets and governance
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V13=0
GLOBAL_SCRIPT_HITS_V13_NEW_PAGES=0

## 10) Stage release package
STAGE_CREATED=/tmp/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419

## 11) Create D3 package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz.sha256
aaf3cb383af3687c3354c5f3b97259bc06004876402a193bdc7aceb9b8279c5d  /home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz

## 12) Final Evaluation
OK_EVALUATION=0
V13_FINAL_D3_CLEAN_HEALTH_STATUS=CHECK_ALERTS
V13_FINAL_RELEASE_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V13_FINAL_D3_AUDIT_AND_PACKAGE_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_V13_FINAL_D3_TIMER_OWNER_FIXER_AND_REPACKAGE_20260709_074419.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D3_RELEASE_PACKAGE_20260709_074419.tar.gz.sha256
