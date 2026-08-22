# NDSP V1.8 / P8-D4 — Fix SPA 404 + Arabic/English Toggle Preview
DATE=2026-07-09T13:38:49+02:00
MODE=ISOLATED_PREVIEW_ONLY_FIX_REACT_ROUTER_BASENAME_AND_I18N
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
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_20260709_133849.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_20260709_133849
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_PACKAGE_20260709_133849.tar.gz

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 14h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.9mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.2%[39m | [1mram usage[22m: [32m8.4%[39m | [1mlo[22m: ⇓ [32m0.01mb/s[39m ⇑ [32m0.01mb/s[39m | [1meth0[22m: ⇓ [32m0.095mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.246mb/s[39m [90m/[39m [1m[33m82.6%[39m[22m |
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
BACKUP_PREVIEW=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_20260709_133849/v18-golden-preview.before

## 5) Extract and detect Vite project
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_20260709_133849/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D4_FIX_SPA_404_ARABIC_TOGGLE_20260709_133849/work/source

## 6) Apply NDSP golden skin + basename + Arabic toggle patch
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_GOLDEN_RADAR_AND_LANG_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-golden-preview/
ROUTER_BASENAME_PATCHED=src/App.tsx
ROUTER_BASENAME_PATCH_COUNT=1
PATCHED=src/pages/PhaseEngine.tsx RADIAL_CLEAN=1
TEXT_CLEANED=src/pages/Governance.tsx
TEXT_CLEANED=src/pages/DataInfra.tsx
TEXT_CLEANED=src/pages/Architecture.tsx
TEXT_CLEANED=src/pages/StrategyLab.tsx
TEXT_CLEANED=src/pages/Decisions.tsx
TEXT_CLEANED=src/pages/Index.tsx
TEXT_CLEANED=src/components/ui/sidebar.tsx
TEXT_CLEANED=src/components/ui/StateBadges.tsx
TEXT_CLEANED=src/components/layout/AppLayout.tsx
TEXT_CLEANED=src/data/mockData.ts
PATCHED=index.html TITLE=1
I18N_FILE_CREATED=public/ndsp-i18n.js
PATCH_NOTES_CREATED=1
BASENAME_SOURCE_CHECK=1
I18N_SOURCE_CHECK=1
GOLD_SOURCE_CHECK=16

## 7) Build preview
NODE_VERSION=v22.22.2
NPM_VERSION=10.9.8
NPM_INSTALL_MODE=npm_install_lock_repair
npm warn deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm warn deprecated whatwg-encoding@2.0.0: Use @exodus/bytes instead for a more spec-conformant and faster implementation
npm warn deprecated domexception@4.0.0: Use your platform's native DOMException instead
npm warn deprecated recharts@2.15.0: 1.x and 2.x branches are no longer active. Bump to Recharts v3 to receive latest features and bugfixes. See https://github.com/recharts/recharts/wiki/3.0-migration-guide

added 485 packages in 28s
NPM_BUILD_MODE=npm_run_build

> vite_react_shadcn_ts@0.0.0 build
> vite build

vite v5.4.19 building for production...
transforming...
Browserslist: browsers data (caniuse-lite) is 13 months old. Please run:
  npx update-browserslist-db@latest
  Why you should do it regularly: https://github.com/browserslist/update-db#readme
✓ 2479 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.29 kB │ gzip:   0.60 kB
dist/assets/index-k7zRlH1k.css   73.44 kB │ gzip:  12.97 kB
dist/assets/index-8HYAbfWP.js   824.33 kB │ gzip: 234.88 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 14.88s
NPM_RUN_BUILD_STATUS=OK
BUILD_STATUS=OK
BUILD_I18N_CHECK=2

## 8) Publish isolated preview
PREVIEW_PUBLISHED=/var/www/ndsp-my/v18-golden-preview

## 9) Post publish tests
PREVIEW_HTTP=200
NOTES_HTTP=200
I18N_HTTP=200
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
V16_COMPLETED_HTTP=200
MY_HOME_HTTP=200
P7_LAUNCH_READINESS_HTTP=200
