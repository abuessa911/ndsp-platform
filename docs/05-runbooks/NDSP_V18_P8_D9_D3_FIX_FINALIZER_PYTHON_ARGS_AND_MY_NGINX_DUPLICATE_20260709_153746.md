# NDSP V1.8 / P8-D9-D3 — Fix Finalizer Python Args + Remove Exact my.ndsp.app Duplicate
DATE=2026-07-09T15:37:46+02:00
MODE=FIX_D2_PYTHON_INVOCATION_AND_EXACT_MY_NDSP_APP_DUPLICATE
LIVE=/var/www/ndsp-my
CANONICAL_MY_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
NO_HTML_CHANGE=1
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
NO_BUILD=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz

## 1) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
2026/07/09 15:37:46 [warn] 3886121#3886121: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:37:46 [warn] 3886121#3886121: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:37:46 [warn] 3886121#3886121: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:37:46 [warn] 3886121#3886121: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 2) Verify stable shell pages
MARKER_OK=/var/www/ndsp-my/index.html
MARKER_OK=/var/www/ndsp-my/asset-selector.html
MARKER_OK=/var/www/ndsp-my/market-assets.html
MARKER_OK=/var/www/ndsp-my/decision-radar.html
MARKER_OK=/var/www/ndsp-my/architecture-map.html
MARKER_OK=/var/www/ndsp-my/launch-readiness.html
STABLE_SHELL_MARKER_HITS=6

## 3) Backup Nginx before exact duplicate fix
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746/nginx/etc_nginx_before_d3_20260709_153746.tar.gz
NGINX_T_BEFORE=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746/nginx/nginx_T_before_d3.txt

## 4) Disable exact duplicate my.ndsp.app-only Nginx configs
PY_DISABLED_DUPLICATE_COUNT=0
PY_LEFT_COUNT=2
PY_LEFT=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf reason=canonical
PY_LEFT=/etc/nginx/conf.d/000-my.ndsp.app-final.conf reason=shared_server_names=my.ndsp.app,on
EXACT_DUPLICATE_MY_NGINX_DISABLED_COUNT=0

## 5) Nginx test and reload
2026/07/09 15:37:47 [warn] 3886201#3886201: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:37:47 [warn] 3886201#3886201: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:37:47 [warn] 3886201#3886201: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:37:47 [warn] 3886201#3886201: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_RELOAD_AFTER_D3=OK
2026/07/09 15:37:47 [warn] 3886213#3886213: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:37:47 [warn] 3886213#3886213: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:37:47 [warn] 3886213#3886213: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:37:47 [warn] 3886213#3886213: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
CONFLICT_WARNINGS_AFTER=4

## 6) HTTP and content checks
HTTP_asset_selector=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_launch_readiness=200
HTTP_my_home=200
HTTP_decision_radar=200
HTTP_market_assets=200
HTTP_architecture_map=200
HTTP_CHECKS_OK=1
FORBIDDEN_PUBLIC_TERMS_HITS=0
HEADER_MY_NDSP_PORTAL=x-ndsp-portal: golden-stable-d9

## 7) Runtime after D3
FAILED_UNITS_COUNT_AFTER=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_AFTER=active
2026/07/09 15:37:50 [warn] 3886409#3886409: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:37:50 [warn] 3886409#3886409: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:37:50 [warn] 3886409#3886409: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:37:50 [warn] 3886409#3886409: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 8) Rollback helper
ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746/ROLLBACK_V18_P8_D9_D3_MY_NGINX_DUPLICATE.sh

## 9) Stage package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz.sha256
154d40ffe6fbce1eb93e4f742b40f3ad8b43b9e4a7c3f4dc1fa06aa7b2974552  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz

## 10) Final Evaluation
OK_EVALUATION=0
V18_P8_D9_D3_STATUS=CHECK_ALERTS
V18_P8_D9_D3_FINAL_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V18_P8_D9_D3_WITH_ALERTS
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_20260709_153746.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D3_FIX_FINALIZER_PYTHON_ARGS_AND_MY_NGINX_DUPLICATE_PACKAGE_20260709_153746.tar.gz.sha256
