# NDSP V1.8 / P8-D8 — Remove Legacy Designs + Force Golden Production
DATE=2026-07-09T14:51:29+02:00
MODE=REMOVE_LEGACY_PUBLIC_DESIGN_VISIBILITY_FORCE_GOLDEN
ZIP_SOURCE=/tmp/ndsp_v18_golden_skin_source.zip
PROD_DIR=/var/www/ndsp-my/v18-production
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
AUTH_PAGES_EXCLUDED=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_20260709_145129.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_20260709_145129
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_PACKAGE_20260709_145129.tar.gz

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
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 15h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 76.9mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m13.2%[39m | [1mram usage[22m: [32m8.4%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.175mb/s[39m ⇑ [32m0.007mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.31mb/s[39m [90m/[39m [1m[33m82.82%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Public production targets
TARGETS_COUNT=37
EXCLUDED_COUNT=5

## 4) Baseline endpoint checks
HTTP_BASE_asset_selector=200
HTTP_BASE_completed_live=200
HTTP_BASE_api_health=200
HTTP_BASE_quality_live=200
HTTP_BASE_my_home=200
HTTP_BASE_market_assets=200
HTTP_BASE_v16_completed=200
BASE_ENDPOINTS_OK=1

## 5) Backup current public pages and v18-production
BACKUP_PROD_DIR=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_20260709_145129/v18-production.before
BACKUP_PAGE=/var/www/ndsp-my/alerts-log.html
BACKUP_PAGE=/var/www/ndsp-my/architecture-map.html
BACKUP_PAGE=/var/www/ndsp-my/asset.html
BACKUP_PAGE=/var/www/ndsp-my/asset-selector.html
BACKUP_PAGE=/var/www/ndsp-my/command-center.html
BACKUP_PAGE=/var/www/ndsp-my/completed-decisions.html
BACKUP_PAGE=/var/www/ndsp-my/completed-decisions-review.html
BACKUP_PAGE=/var/www/ndsp-my/daily-brief.html
BACKUP_PAGE=/var/www/ndsp-my/data-freshness.html
BACKUP_PAGE=/var/www/ndsp-my/decision-center.html
BACKUP_PAGE=/var/www/ndsp-my/decision-guide.html
BACKUP_PAGE=/var/www/ndsp-my/decision-radar.html
BACKUP_PAGE=/var/www/ndsp-my/decision-room-guide.html
BACKUP_PAGE=/var/www/ndsp-my/decision-support.html
BACKUP_PAGE=/var/www/ndsp-my/guide.html
BACKUP_PAGE=/var/www/ndsp-my/index.html
BACKUP_PAGE=/var/www/ndsp-my/launch-readiness.html
BACKUP_PAGE=/var/www/ndsp-my/market-assets.html
BACKUP_PAGE=/var/www/ndsp-my/markets.html
BACKUP_PAGE=/var/www/ndsp-my/my-watchlist.html
BACKUP_PAGE=/var/www/ndsp-my/NDSP_Asset_View.html
BACKUP_PAGE=/var/www/ndsp-my/NDSP_Command_Center.html
BACKUP_PAGE=/var/www/ndsp-my/NDSP_Daily_Brief.html
BACKUP_PAGE=/var/www/ndsp-my/NDSP_Settings_Alerts.html
BACKUP_PAGE=/var/www/ndsp-my/nmp.html
BACKUP_PAGE=/var/www/ndsp-my/phase.html
BACKUP_PAGE=/var/www/ndsp-my/platform.html
BACKUP_PAGE=/var/www/ndsp-my/radar.html
BACKUP_PAGE=/var/www/ndsp-my/release-evidence.html
BACKUP_PAGE=/var/www/ndsp-my/release-registry.html
BACKUP_PAGE=/var/www/ndsp-my/settings.html
BACKUP_PAGE=/var/www/ndsp-my/support-center.html
BACKUP_PAGE=/var/www/ndsp-my/v13-experience.html
BACKUP_PAGE=/var/www/ndsp-my/v14-experience.html
BACKUP_PAGE=/var/www/ndsp-my/v14-final-evidence.html
BACKUP_PAGE=/var/www/ndsp-my/v15-api-bridge.html
BACKUP_PAGE=/var/www/ndsp-my/v16-live-adapter.html

## 6) Extract clean source
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_20260709_145129/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D8_REMOVE_LEGACY_DESIGNS_FORCE_GOLDEN_PRODUCTION_20260709_145129/work/source

## 7) Patch clean source for golden production
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_D8_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-production/
ROUTER_BASENAME_REMOVE_COUNT=0
APP_ROUTE_ALIASES_PATCHED=1
APP_ROUTE_ALIAS_LINES_ADDED=37
LAYOUT_NAV_PATCHED=1
PATCHED=src/pages/PhaseEngine.tsx RADIAL_CLEAN=1
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
D8_PATCH_NOTES_CREATED=1
GOLD_SOURCE_CHECK=16
I18N_SOURCE_CHECK=1
BASE_SOURCE_CHECK=1
ROUTE_ALIAS_CHECK=1
FORBIDDEN_SOURCE_HITS=3
FINAL_STATUS=ABORTED_FORBIDDEN_SOURCE_TERMS_REMAIN
