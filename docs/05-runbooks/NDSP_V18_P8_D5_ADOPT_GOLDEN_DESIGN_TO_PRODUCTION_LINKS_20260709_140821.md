# NDSP V1.8 / P8-D5 — Adopt Golden Design To Production Links
DATE=2026-07-09T14:08:21+02:00
MODE=CONTROLLED_PRODUCTION_LINKS_VISUAL_ADOPTION
ZIP_SOURCE=/tmp/ndsp_v18_golden_skin_source.zip
PROD_ASSET_DIR=/var/www/ndsp-my/v18-production
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
AUTH_PAGES_EXCLUDED=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz

## 1) Required locks
V17_P7_FINAL_LOCK=OK
V18_P8_D3_PREVIEW_LOCK=OK

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 14h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 76.2mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.3%[39m | [1mram usage[22m: [32m8.5%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.018mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.159mb/s[39m [90m/[39m [1m[33m82.69%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline endpoints before adoption
HTTP_BASE_asset_selector=200
HTTP_BASE_completed_live=200
HTTP_BASE_api_health=200
HTTP_BASE_quality_live=200
HTTP_BASE_launch_readiness=200
HTTP_BASE_my_home=200
HTTP_BASE_release_registry=200
HTTP_BASE_market_assets=200
HTTP_BASE_v16_completed=200
BASE_ENDPOINTS_OK=1

## 4) Extract and detect Vite project
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821/work/source

## 5) Apply production golden skin + legacy route aliases + Arabic toggle
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_D5_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-production/
APP_ROUTE_ALIASES_PATCHED=1
APP_ROUTE_ALIAS_COUNT=28
LAYOUT_NAV_PATCHED=1
PATCHED=src/pages/PhaseEngine.tsx RADIAL_CLEAN=1
TEXT_CLEANED=src/pages/Governance.tsx
TEXT_CLEANED=src/pages/DataInfra.tsx
TEXT_CLEANED=src/pages/Architecture.tsx
TEXT_CLEANED=src/pages/StrategyLab.tsx
TEXT_CLEANED=src/pages/Decisions.tsx
TEXT_CLEANED=src/pages/Index.tsx
TEXT_CLEANED=src/components/ui/sidebar.tsx
TEXT_CLEANED=src/components/ui/StateBadges.tsx
TEXT_CLEANED=src/data/mockData.ts
PATCHED=index.html TITLE=1
I18N_FILE_CREATED=public/ndsp-i18n.js
PATCH_NOTES_CREATED=1
ROUTE_ALIAS_CHECK=1
NAV_LINK_CHECK=1
I18N_SOURCE_CHECK=1
GOLD_SOURCE_CHECK=16
BASE_SOURCE_CHECK=1

## 6) Build production golden design
NODE_VERSION=v22.22.2
NPM_VERSION=10.9.8
NPM_INSTALL_MODE=npm_install_lock_repair
npm warn deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm warn deprecated whatwg-encoding@2.0.0: Use @exodus/bytes instead for a more spec-conformant and faster implementation
npm warn deprecated domexception@4.0.0: Use your platform's native DOMException instead
npm warn deprecated recharts@2.15.0: 1.x and 2.x branches are no longer active. Bump to Recharts v3 to receive latest features and bugfixes. See https://github.com/recharts/recharts/wiki/3.0-migration-guide

added 485 packages in 26s
NPM_BUILD_MODE=npm_run_build

> vite_react_shadcn_ts@0.0.0 build
> vite build

vite v5.4.19 building for production...
transforming...
Browserslist: browsers data (caniuse-lite) is 13 months old. Please run:
  npx update-browserslist-db@latest
  Why you should do it regularly: https://github.com/browserslist/update-db#readme
✓ 2478 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.28 kB │ gzip:   0.60 kB
dist/assets/index-k7zRlH1k.css   73.44 kB │ gzip:  12.97 kB
dist/assets/index-BLNLZX0G.js   825.45 kB │ gzip: 235.17 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 13.57s
NPM_RUN_BUILD_STATUS=OK
BUILD_STATUS=OK
BUILD_I18N_CHECK=2
BUILD_ASSET_BASE_CHECK=2

## 7) Backup and publish production assets + HTML links
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/index.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/platform.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/asset.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/asset-selector.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/market-assets.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/my-watchlist.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/markets.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/NDSP_Asset_View.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/radar.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/decision-radar.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/decision-center.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/decision-support.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/completed-decisions.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/completed-decisions-review.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/NDSP_Command_Center.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/command-center.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/NDSP_Daily_Brief.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/daily-brief.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/settings.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/alerts-log.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/support-center.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/guide.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/decision-guide.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/nmp.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/phase.html
PRODUCTION_PAGE_ADOPTED=/var/www/ndsp-my/data-freshness.html
AUTH_ADMIN_PAGE_EXCLUDED=/var/www/ndsp-my/login.html
AUTH_ADMIN_PAGE_EXCLUDED=/var/www/ndsp-my/register.html
AUTH_ADMIN_PAGE_EXCLUDED=/var/www/ndsp-my/forgot-password.html
AUTH_ADMIN_PAGE_EXCLUDED=/var/www/ndsp-my/reset-password.html
AUTH_ADMIN_PAGE_EXCLUDED=/var/www/ndsp-my/admin.html
ROLLBACK_SCRIPT=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821/ROLLBACK_V18_P8_D5.sh

## 8) Post-adoption HTTP tests
HTTP_POST_asset_selector=200
HTTP_POST_completed_live=200
HTTP_POST_api_health=200
HTTP_POST_settings=200
HTTP_POST_production_assets=200
HTTP_POST_quality_live=200
HTTP_POST_i18n=200
HTTP_POST_my_home=200
HTTP_POST_decision_support=200
HTTP_POST_decision_radar=200
HTTP_POST_market_assets=200
HTTP_POST_guide=200
HTTP_POST_production_notes=200
HTTP_POST_v16_completed=200
HTTP_POST_nmp=200
POST_ENDPOINTS_OK=1
HTML_ASSET_REF_COUNT=6
HTML_I18N_REF_COUNT=3
AUTH_BACKUP_NOT_TOUCHED_COUNT=0

## 9) Runtime and governance after adoption
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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 14h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 76.2mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m29.6%[39m | [1mram usage[22m: [32m9.9%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1mdisk[22m: ⇓ [32m0.127mb/s[39m ⇑ [1m[33m11.298mb/s[39m[22m [90m/[39m [1m[33m82.79%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js
GOVERNANCE_HITS_V18_D5_SOURCE=0
GOLD_TOKEN_CHECK_COUNT=16
ROUTE_ALIAS_FINAL_CHECK=1
I18N_FINAL_CHECK=1

## 10) Stage evidence package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz.sha256
c8794d56a67bd910387f2030121586564e22e7a77507ed3af5b3b9e2f1e78b92  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz

## 11) Final Evaluation
OK_EVALUATION=1
V18_P8_D5_PRODUCTION_LINKS_ADOPTION_STATUS=OK
V18_P8_D5_PRODUCTION_ASSETS_STATUS=OK
V18_P8_D5_AUTH_PAGES_EXCLUDED_STATUS=OK
V18_P8_D5_ROLLBACK_STATUS=AVAILABLE
V18_P8_D5_FINAL_PACKAGE_STATUS=CREATED
FINAL_STATUS=V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz.sha256
