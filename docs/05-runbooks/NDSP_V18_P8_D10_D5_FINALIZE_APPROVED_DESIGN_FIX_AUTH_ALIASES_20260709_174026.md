# NDSP V1.8 / P8-D10-D5 — Finalize Approved Design + Fix Auth Route Aliases
DATE=2026-07-09T17:40:26+02:00
MODE=FINALIZE_APPROVED_DESIGN_FIX_AUTH_ALIASES_ONLY
LIVE=/var/www/ndsp-my
CANONICAL_MY_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
NO_HTML_PUBLIC_DESIGN_CHANGE=1
NO_REACT_BUILD=1
NO_APPROVED_DESIGN_CHANGE=1
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D5_FINALIZE_APPROVED_DESIGN_FIX_AUTH_ALIASES_20260709_174026.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D5_FINALIZE_APPROVED_DESIGN_FIX_AUTH_ALIASES_20260709_174026
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D5_FINALIZE_APPROVED_DESIGN_FIX_AUTH_ALIASES_PACKAGE_20260709_174026.tar.gz

## 1) Verify approved design state before alias fix
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

## 2) Runtime reference before alias fix
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Backup Nginx and current auth alias files
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D5_FINALIZE_APPROVED_DESIGN_FIX_AUTH_ALIASES_20260709_174026/nginx/etc_nginx_before_d5_20260709_174026.tar.gz
BACKUP_EXISTING_ALIAS=/var/www/ndsp-my/login
BACKUP_EXISTING_ALIAS=/var/www/ndsp-my/register
BACKUP_EXISTING_ALIAS=/var/www/ndsp-my/forgot-password
BACKUP_EXISTING_ALIAS=/var/www/ndsp-my/reset-password

## 4) Create extensionless auth/admin alias files
FINAL_STATUS=ABORTED_AUTH_SOURCE_MISSING_register.html
