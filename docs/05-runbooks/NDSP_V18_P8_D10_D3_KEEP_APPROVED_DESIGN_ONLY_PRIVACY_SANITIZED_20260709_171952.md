# NDSP V1.8 / P8-D10-D3 — Keep Approved Design Only + Privacy Terms Sanitizer
DATE=2026-07-09T17:19:52+02:00
MODE=APPROVED_DESIGN_ONLY_PRIVACY_TERMS_SANITIZED
LIVE=/var/www/ndsp-my
APPROVED_DIR=/var/www/ndsp-my/approved-design
ZIP_SOURCE=/tmp/ndsp_approved_design_source.zip
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
AUTH_PAGES_EXCLUDED=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz

## 1) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
2026/07/09 17:19:52 [warn] 101734#101734: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:19:52 [warn] 101734#101734: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:19:52 [warn] 101734#101734: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:19:52 [warn] 101734#101734: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=activating

## 2) Backup live pages, design dirs, and Nginx
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/nginx/etc_nginx_before_20260709_171952.tar.gz
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/alerts-log.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/architecture-map.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/asset.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/asset-selector.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/command-center.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/completed-decisions.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/completed-decisions-review.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/daily-brief.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/data-freshness.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/decision-center.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/decision-guide.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/decision-radar.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/decision-room-guide.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/decision-support.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/guide.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/index.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/launch-readiness.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/market-assets.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/markets.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/my-watchlist.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/NDSP_Asset_View.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/NDSP_Command_Center.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/NDSP_Daily_Brief.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/NDSP_Settings_Alerts.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/nmp.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/phase.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/platform.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/radar.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/release-evidence.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/release-registry.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/settings.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/support-center.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/v13-experience.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/v14-experience.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/v14-final-evidence.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/v15-api-bridge.html
BACKUP_PUBLIC_PAGE=/var/www/ndsp-my/v16-live-adapter.html
BACKUP_DESIGN_DIR=/var/www/ndsp-my/v18-production
BACKUP_DESIGN_DIR=/var/www/ndsp-my/v18-golden-preview

## 3) Extract approved design source
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/work/source

## 4) Patch source: routing + identity + privacy sanitizer
PATCHED=vite.config.ts BASE=/approved-design/ CHANGED=1
ROUTER_BASENAME_REMOVE_COUNT=0
APP_ROUTE_ALIASES_PATCHED=1
APP_ROUTE_ALIAS_LINES_ADDED=37
LAYOUT_NAV_LINKS_PATCHED=1
PUBLIC_TEXT_CLEANED=src/pages/Governance.tsx
PUBLIC_TEXT_CLEANED=src/pages/DataInfra.tsx
PUBLIC_TEXT_CLEANED=src/pages/Architecture.tsx
PUBLIC_TEXT_CLEANED=src/pages/StrategyLab.tsx
PUBLIC_TEXT_CLEANED=src/pages/Decisions.tsx
PUBLIC_TEXT_CLEANED=src/pages/PhaseEngine.tsx
PUBLIC_TEXT_CLEANED=src/pages/Intelligence.tsx
PUBLIC_TEXT_CLEANED=src/pages/Index.tsx
PUBLIC_TEXT_CLEANED=src/components/ui/sidebar.tsx
PUBLIC_TEXT_CLEANED=src/components/ui/StateBadges.tsx
PUBLIC_TEXT_CLEANED=src/components/layout/AppLayout.tsx
PUBLIC_TEXT_CLEANED=src/data/mockData.ts
PUBLIC_TEXT_CLEANED=src/index.css
PATCHED=index.html TITLE_META_MARKER=1
SOURCE_CHANGED_FILES_COUNT=13
D10_D3_NOTES_CREATED=1
FORBIDDEN_SOURCE_HITS=0
BASE_CHECK=1
ROUTE_ALIAS_CHECK=1
MARKER_SOURCE_CHECK=2

## 5) Build approved design
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
✓ 2478 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.36 kB │ gzip:   0.64 kB
dist/assets/index-OGqS1LGt.css   72.72 kB │ gzip:  12.69 kB
dist/assets/index-BC3JFIDB.js   826.39 kB │ gzip: 235.06 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 12.98s
NPM_RUN_BUILD_STATUS=OK
BUILD_ASSET_CHECK=2
BUILD_MARKER_CHECK=2
BUILT_FORBIDDEN_HITS=0
JS_COUNT=1

## 6) Quarantine old live design folders and publish approved design only
QUARANTINED_OLD_DESIGN_DIR=/var/www/ndsp-my/v18-production -> /home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/quarantined_live_designs/v18-production
QUARANTINED_OLD_DESIGN_DIR=/var/www/ndsp-my/v18-golden-preview -> /home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/quarantined_live_designs/v18-golden-preview
OLD_DESIGN_DIR_NOT_PRESENT=/var/www/ndsp-my/__clean_preview
APPROVED_DESIGN_PUBLISHED=/var/www/ndsp-my/approved-design

## 7) Replace all public pages with approved design index
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/alerts-log.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/architecture-map.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/asset.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/asset-selector.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/command-center.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/completed-decisions.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/completed-decisions-review.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/daily-brief.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/data-freshness.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/decision-center.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/decision-guide.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/decision-radar.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/decision-room-guide.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/decision-support.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/guide.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/index.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/launch-readiness.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/market-assets.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/markets.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/my-watchlist.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/NDSP_Asset_View.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/NDSP_Command_Center.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/NDSP_Daily_Brief.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/NDSP_Settings_Alerts.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/nmp.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/phase.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/platform.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/radar.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/release-evidence.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/release-registry.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/settings.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/support-center.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/v13-experience.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/v14-experience.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/v14-final-evidence.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/v15-api-bridge.html
PUBLIC_PAGE_NOW_APPROVED_DESIGN=/var/www/ndsp-my/v16-live-adapter.html
PUBLISHED_APPROVED_PUBLIC_PAGES_COUNT=37
AUTH_ADMIN_PAGE_EXCLUDED_NOT_TOUCHED=/var/www/ndsp-my/login.html
AUTH_ADMIN_PAGE_EXCLUDED_NOT_TOUCHED=/var/www/ndsp-my/register.html
AUTH_ADMIN_PAGE_EXCLUDED_NOT_TOUCHED=/var/www/ndsp-my/forgot-password.html
AUTH_ADMIN_PAGE_EXCLUDED_NOT_TOUCHED=/var/www/ndsp-my/reset-password.html
AUTH_ADMIN_PAGE_EXCLUDED_NOT_TOUCHED=/var/www/ndsp-my/admin.html

## 8) Clean my.ndsp.app exact duplicate Nginx configs
PY_DISABLED_MY_ONLY_DUPLICATES=0
PY_LEFT_COUNT=2
PY_LEFT=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf reason=canonical
PY_LEFT=/etc/nginx/conf.d/000-my.ndsp.app-final.conf reason=shared_server_names=my.ndsp.app,on
MY_ONLY_NGINX_DUPLICATES_DISABLED_COUNT=0
2026/07/09 17:20:36 [warn] 105185#105185: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:20:36 [warn] 105185#105185: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:20:36 [warn] 105185#105185: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:20:36 [warn] 105185#105185: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_RELOAD_AFTER_D10_D3=OK
2026/07/09 17:20:36 [warn] 105196#105196: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:20:36 [warn] 105196#105196: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:20:36 [warn] 105196#105196: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:20:36 [warn] 105196#105196: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
CONFLICT_WARNINGS_AFTER=4

## 9) HTTP and content checks
HTTP_asset_selector=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_launch_readiness=200
HTTP_my_home=200
HTTP_approved_notes=200
HTTP_approved_design=200
HTTP_decision_radar=200
HTTP_market_assets=200
HTTP_architecture_map=200
HTTP_CHECKS_OK=1
ROOT_MARKER_HITS=6
APPROVED_DIR_MARKER_HITS=3
OLD_DESIGN_LIVE_COUNT=0
ROOT_FORBIDDEN_HITS=0
HEADER_MY_NDSP_PORTAL=x-ndsp-portal: approved-design-only-d10-d3

## 10) Runtime after D10-D3
FAILED_UNITS_COUNT_AFTER=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_AFTER=active
2026/07/09 17:20:39 [warn] 105377#105377: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:20:39 [warn] 105377#105377: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:20:39 [warn] 105377#105377: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:20:39 [warn] 105377#105377: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 11) Rollback helper
ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952/ROLLBACK_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED.sh

## 12) Stage package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz.sha256
199dcb46dee3cfbe4dbf14fdbc67c633200c25d789a6fc87a623020afbaf0cb6  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz

## 13) Final Evaluation
OK_EVALUATION=0
V18_P8_D10_D3_STATUS=CHECK_ALERTS
V18_P8_D10_D3_FINAL_PACKAGE_STATUS=CREATED_OR_PARTIAL
FINAL_STATUS=V18_P8_D10_D3_WITH_ALERTS
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_171952.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D3_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_171952.tar.gz.sha256
