# NDSP V1.8 / P8-D9-D2 — Finalize Stable Shell + Fix my.ndsp.app Nginx Duplicate
DATE=2026-07-09T15:20:48+02:00
MODE=FINALIZE_D9_STABLE_SHELL_AND_FIX_MY_NDSP_APP_DUPLICATE_NGINX
LIVE=/var/www/ndsp-my
CANONICAL_MY_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
NO_BUILD=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D9_D2_FINALIZE_STABLE_SHELL_FIX_MY_NGINX_DUPLICATE_20260709_152048.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D2_FINALIZE_STABLE_SHELL_FIX_MY_NGINX_DUPLICATE_20260709_152048
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_D2_FINALIZE_STABLE_SHELL_FIX_MY_NGINX_DUPLICATE_PACKAGE_20260709_152048.tar.gz

## 1) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
2026/07/09 15:20:49 [warn] 3821199#3821199: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:20:49 [warn] 3821199#3821199: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:20:49 [warn] 3821199#3821199: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:20:49 [warn] 3821199#3821199: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 2) Verify D9 stable shell pages are already published
MARKER_OK=/var/www/ndsp-my/index.html
MARKER_OK=/var/www/ndsp-my/asset-selector.html
MARKER_OK=/var/www/ndsp-my/market-assets.html
MARKER_OK=/var/www/ndsp-my/decision-radar.html
MARKER_OK=/var/www/ndsp-my/architecture-map.html
MARKER_OK=/var/www/ndsp-my/launch-readiness.html
STABLE_SHELL_MARKER_HITS=6

## 3) Backup current Nginx
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D2_FINALIZE_STABLE_SHELL_FIX_MY_NGINX_DUPLICATE_20260709_152048/nginx/etc_nginx_before_d2_20260709_152048.tar.gz
NGINX_T_BEFORE=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_D2_FINALIZE_STABLE_SHELL_FIX_MY_NGINX_DUPLICATE_20260709_152048/nginx/nginx_T_before_d2.txt
CANONICAL_MY_CONF_EXISTS=1

## 4) Disable safe duplicate my.ndsp.app-only Nginx configs
