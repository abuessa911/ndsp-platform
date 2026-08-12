# NDSP V1.8 / P8-D10-D2 — Keep Approved Design Only + Privacy Terms Sanitizer
DATE=2026-07-09T17:08:10+02:00
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
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_170810.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_170810
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_PACKAGE_20260709_170810.tar.gz

## 1) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
2026/07/09 17:08:11 [warn] 53742#53742: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 17:08:11 [warn] 53742#53742: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 17:08:11 [warn] 53742#53742: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 17:08:11 [warn] 53742#53742: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 2) Backup live pages, design dirs, and Nginx
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_170810/nginx/etc_nginx_before_20260709_170810.tar.gz
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
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_170810/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D10_D2_KEEP_APPROVED_DESIGN_ONLY_PRIVACY_SANITIZED_20260709_170810/work/source

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
D10_D2_NOTES_CREATED=1
FORBIDDEN_SOURCE_HITS=1
FORBIDDEN_SOURCE_SAMPLE_BEGIN
src/pages/Architecture.tsx:15:    components: ["Market Data Gateway", "Network Measurement Layer (Network Measurement Source)", "Institutional Positioning Intake (Institutional Positioning)", "Macro (Institutional Macro/Institutional Macro)", "Sentiment Reading Stream", "Data Quality & Continuity", "Data Data Normalization Layer"],
FORBIDDEN_SOURCE_SAMPLE_END
BASE_CHECK=1
ROUTE_ALIAS_CHECK=1
MARKER_SOURCE_CHECK=2
FINAL_STATUS=ABORTED_FORBIDDEN_SOURCE_TERMS_REMAIN
