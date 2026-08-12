# NDSP V1.8 / P8-D7 — Rebuild From Clean Source To Fix Blank Page
DATE=2026-07-09T14:36:36+02:00
MODE=REBUILD_FROM_CLEAN_SOURCE_NO_DIRECT_BUNDLE_REWRITE
ZIP_SOURCE=/tmp/ndsp_v18_golden_skin_source.zip
PREVIEW_DIR=/var/www/ndsp-my/v18-golden-preview
PROD_DIR=/var/www/ndsp-my/v18-production
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_20260709_143636.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_20260709_143636
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_PACKAGE_20260709_143636.tar.gz

## 1) Required P7 lock
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 15h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 76.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14.7%[39m | [1mram usage[22m: [32m8.3%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.184mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.284mb/s[39m [90m/[39m [1m[33m82.82%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Backup current preview/production
BACKUP_PREVIEW=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_20260709_143636/v18-golden-preview.before
BACKUP_PRODUCTION=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_20260709_143636/v18-production.before

## 4) Extract clean source
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D7_REBUILD_FROM_CLEAN_SOURCE_FIX_BLANK_PAGE_20260709_143636/extract/empire-core-ndip

## 5) Build preview from clean source

## BUILD MODE: preview
MODE_BASE=/v18-golden-preview/
MODE_BASENAME=/v18-golden-preview
MODE_OUT_DIR=/var/www/ndsp-my/v18-golden-preview
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_D7_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-golden-preview/
ROUTER_PATCHED=src/App.tsx
ROUTER_PATCH_COUNT=1
APP_ROUTE_ALIASES_PATCHED=1
LAYOUT_NAV_PATCHED=1
TEXT_CLEANED=src/pages/Governance.tsx
TEXT_CLEANED=src/pages/DataInfra.tsx
TEXT_CLEANED=src/pages/Architecture.tsx
TEXT_CLEANED=src/pages/StrategyLab.tsx
TEXT_CLEANED=src/pages/Decisions.tsx
TEXT_CLEANED=src/pages/PhaseEngine.tsx
TEXT_CLEANED=src/pages/Index.tsx
TEXT_CLEANED=src/components/ui/sidebar.tsx
TEXT_CLEANED=src/components/ui/StateBadges.tsx
TEXT_CLEANED=src/data/mockData.ts
PATCHED=index.html TITLE=1
D7_PATCH_NOTES_CREATED=1
preview_GOLD_SOURCE_CHECK=16
preview_I18N_SOURCE_CHECK=1
preview_FORBIDDEN_SOURCE_HITS=3
FINAL_STATUS=ABORTED_preview_FORBIDDEN_SOURCE_TERMS_REMAIN
