# NDSP V1.8 / P8 Golden Visual Skin Preview
DATE=2026-07-09T12:51:03+02:00
MODE=ISOLATED_VISUAL_PREVIEW_ONLY
ZIP_SOURCE=/tmp/ndsp_v18_golden_skin_source.zip
PREVIEW_DIR=/var/www/ndsp-my/v18-golden-preview
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_PRODUCTION_BUILD_CHANGE=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=docs/05-runbooks/NDSP_V18_P8_GOLDEN_VISUAL_SKIN_PREVIEW_20260709_125103.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_GOLDEN_VISUAL_SKIN_PREVIEW_20260709_125103
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_GOLDEN_VISUAL_SKIN_PREVIEW_PACKAGE_20260709_125103.tar.gz

## 1) Required P7 final lock
V17_P7_FINAL_LOCK=OK

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 13h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.5mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.5%[39m | [1mram usage[22m: [32m8.2%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.178mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.273mb/s[39m [90m/[39m [1m[33m82.45%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline endpoints
HTTP_BASE_completed_live=200
HTTP_BASE_api_health=200
HTTP_BASE_quality_live=200
HTTP_BASE_launch_readiness=200
HTTP_BASE_my_home=200
HTTP_BASE_release_registry=200
HTTP_BASE_architecture_map=200
HTTP_BASE_v16_completed=200
BASE_ENDPOINTS_OK=1

## 4) Backup existing preview if any
BACKUP_PREVIEW=NO_EXISTING_PREVIEW

## 5) Extract and detect Vite project
