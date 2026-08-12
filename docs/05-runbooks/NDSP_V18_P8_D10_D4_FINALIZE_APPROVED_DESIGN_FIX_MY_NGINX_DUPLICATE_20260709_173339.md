# NDSP V1.8 / P8-D10-D4 — Finalize Approved Design + Fix my.ndsp.app Nginx Duplicate
DATE=2026-07-09T17:33:39+02:00
MODE=FINALIZE_APPROVED_DESIGN_AND_FIX_MY_NDSP_APP_NGINX_DUPLICATE_ONLY
LIVE=/var/www/ndsp-my
CANONICAL_MY_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
LEGACY_MY_CONF=/etc/nginx/conf.d/000-my.ndsp.app-final.conf
NO_HTML_CHANGE=1
NO_REACT_BUILD=1
NO_APPROVED_DESIGN_CHANGE=1
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_20260709_173339.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_20260709_173339
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz

## 1) Verify D10-D3 approved design state before Nginx change
APPROVED_MARKER_OK=/var/www/ndsp-my/index.html
APPROVED_MARKER_OK=/var/www/ndsp-my/asset-selector.html
APPROVED_MARKER_OK=/var/www/ndsp-my/market-assets.html
APPROVED_MARKER_OK=/var/www/ndsp-my/decision-radar.html
APPROVED_MARKER_OK=/var/www/ndsp-my/architecture-map.html
APPROVED_MARKER_OK=/var/www/ndsp-my/launch-readiness.html
ROOT_MARKER_HITS=6
APPROVED_DIR_MARKER_HITS=3
OLD_DESIGN_LIVE_COUNT=0
ROOT_FORBIDDEN_HITS=0

## 2) Runtime reference before Nginx duplicate fix
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
2026/07/09 17:33:39 [warn] 157561#157561: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:33:39 [warn] 157561#157561: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:33:39 [warn] 157561#157561: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:33:39 [warn] 157561#157561: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Backup Nginx
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_20260709_173339/nginx/etc_nginx_before_d4_20260709_173339.tar.gz

## 4) Write safe canonical my.ndsp.app server block
CANONICAL_MY_CONF_WRITTEN=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf

## 5) Disable legacy duplicate my.ndsp.app file safely
LEGACY_SERVER_NAMES_BEGIN
my.ndsp.app
on
LEGACY_SERVER_NAMES_END
LEGACY_MY_CONF_DISABLED=/etc/nginx/conf.d/000-my.ndsp.app-final.conf.disabled_by_d10_d4_20260709_173339
DISABLED_LEGACY=1

## 6) Nginx test, rollback on failure, reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_RELOAD_AFTER_D4=OK
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
CONFLICT_WARNINGS_AFTER=0

## 7) HTTP and content checks
HTTP_asset_selector=200
HTTP_api_health=200
HTTP_login_html=200
HTTP_quality_live=200
HTTP_reset_alias=404
HTTP_register_html=200
HTTP_login_alias=404
HTTP_launch_readiness=200
HTTP_my_home=200
HTTP_forgot_alias=404
HTTP_register_alias=404
HTTP_approved_notes=200
HTTP_reset_html=200
HTTP_approved_design=200
HTTP_decision_radar=200
HTTP_market_assets=200
HTTP_admin_html=200
HTTP_forgot_html=200
HTTP_architecture_map=200
HTTP_CHECKS_OK=0
HEADER_MY_NDSP_PORTAL=x-ndsp-portal: approved-design-only-d10-d4
ROOT_MARKER_HITS_AFTER=6
APPROVED_DIR_MARKER_HITS_AFTER=3
ROOT_FORBIDDEN_HITS_AFTER=0
OLD_DESIGN_LIVE_COUNT_AFTER=0

## 8) Runtime after D4
FAILED_UNITS_COUNT_AFTER=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_AFTER=active
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 9) Rollback helper
ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_20260709_173339/ROLLBACK_V18_P8_D10_D4_NGINX_ONLY.sh

## 10) Stage package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz.sha256
0f18e51025dfc3fd82322da1cc0336dbb51b32c6082ab54cfed635b0edac3549  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz

## 11) Final Evaluation
OK_EVALUATION=0
V18_P8_D10_D4_STATUS=CHECK_ALERTS
V18_P8_D10_D4_FINAL_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V18_P8_D10_D4_WITH_ALERTS
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_20260709_173339.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D4_FINALIZE_APPROVED_DESIGN_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_173339.tar.gz.sha256
