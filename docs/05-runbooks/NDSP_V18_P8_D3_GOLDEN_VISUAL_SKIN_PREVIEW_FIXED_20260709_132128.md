# NDSP V1.8 / P8-D3 Golden Visual Skin Preview Fixed
DATE=2026-07-09T13:21:29+02:00
MODE=ISOLATED_VISUAL_PREVIEW_ONLY_D3_NPM_INSTALL_FIXED_ABSOLUTE_REPORT_PATH
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
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 13h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12%[39m | [1mram usage[22m: [32m8.2%[39m | [1mlo[22m: ⇓ [32m0.008mb/s[39m ⇑ [32m0.008mb/s[39m | [1meth0[22m: ⇓ [32m0.088mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.315mb/s[39m ⇑ [32m0.294mb/s[39m [90m/[39m [1m[33m82.46%[39m[22m |
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
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128/work/source

## 6) Apply NDSP golden skin patch
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_GOLDEN_RADAR_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-golden-preview/
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
PATCH_NOTES_CREATED=1

## 7) Build preview
NODE_VERSION=v22.22.2
NPM_VERSION=10.9.8
NPM_INSTALL_MODE=npm_install_lock_repair
NPM_CI_DISABLED_REASON=package_lock_out_of_sync_in_source_zip
npm warn deprecated whatwg-encoding@2.0.0: Use @exodus/bytes instead for a more spec-conformant and faster implementation
npm warn deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm warn deprecated domexception@4.0.0: Use your platform's native DOMException instead
npm warn deprecated recharts@2.15.0: 1.x and 2.x branches are no longer active. Bump to Recharts v3 to receive latest features and bugfixes. See https://github.com/recharts/recharts/wiki/3.0-migration-guide

added 485 packages in 38s
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
dist/index.html                   1.30 kB │ gzip:   0.58 kB
dist/assets/index-BDHcAFy2.css   73.09 kB │ gzip:  12.82 kB
dist/assets/index-cd1JPSCw.js   824.30 kB │ gzip: 234.86 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 14.21s
NPM_RUN_BUILD_STATUS=OK
BUILD_STATUS=OK

## 8) Publish isolated preview
PREVIEW_PUBLISHED=/var/www/ndsp-my/v18-golden-preview

## 9) Post publish tests
PREVIEW_HTTP=200
NOTES_HTTP=200
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
V16_COMPLETED_HTTP=200
MY_HOME_HTTP=200
P7_LAUNCH_READINESS_HTTP=200

## 10) Runtime and governance after preview
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 14h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m27.2%[39m | [1mram usage[22m: [32m8.6%[39m | [1mlo[22m: ⇓ [32m0.009mb/s[39m ⇑ [32m0.009mb/s[39m | [1meth0[22m: ⇓ [32m0.08mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.343mb/s[39m ⇑ [1m[33m11.424mb/s[39m[22m [90m/[39m [1m[33m82.57%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V18_D2_PREVIEW_SOURCE=0
GOLD_TOKEN_CHECK_COUNT=14

## 11) Stage evidence package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz.sha256
64a9a9d9350af2eec2f7c797a60e95e746ef86fa2ea6a0b9a9a78bb22382a6d7  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz

## 12) Final Evaluation
OK_EVALUATION=1
V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_STATUS=OK
V18_P8_PREVIEW_URL=https://my.ndsp.app/v18-golden-preview/
V18_P8_D3_FINAL_PACKAGE_STATUS=CREATED
FINAL_STATUS=V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz.sha256
