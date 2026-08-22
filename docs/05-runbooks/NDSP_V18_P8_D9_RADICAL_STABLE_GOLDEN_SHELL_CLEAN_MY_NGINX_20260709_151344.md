# NDSP V1.8 / P8-D9 — Radical Stable Golden Shell + Clean my.ndsp.app Nginx Route
DATE=2026-07-09T15:13:44+02:00
MODE=RADICAL_STABLE_STATIC_GOLDEN_SHELL_AND_MY_DOMAIN_NGINX_CANONICAL_ROUTE
LIVE=/var/www/ndsp-my
CANONICAL_MY_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
NO_API_BACKEND_CHANGE=1
NO_PM2_RESTART=1
NO_DB_SCHEMA_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_REBOOT=1
AUTH_PAGES_EXCLUDED=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_PACKAGE_20260709_151344.tar.gz

## 1) Required runtime lock reference
REALITY_LOCK_EXISTS=1

## 2) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Snapshot Nginx and current portal
NGINX_FULL_BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/nginx/etc_nginx_before_20260709_151344.tar.gz
NGINX_T_BEFORE=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/nginx/nginx_T_before.txt
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
BACKUP_V18_PRODUCTION=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/v18-production.before
BACKUP_V18_PREVIEW=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/v18-golden-preview.before

## 4) Build stable golden shell — no React bundle
STABLE_SHELL_CREATED=/tmp/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/ndsp-golden-stable-shell.html

## 5) Publish stable shell to all public pages
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/alerts-log.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/architecture-map.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/asset.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/asset-selector.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/command-center.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/completed-decisions.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/completed-decisions-review.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/daily-brief.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/data-freshness.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/decision-center.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/decision-guide.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/decision-radar.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/decision-room-guide.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/decision-support.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/guide.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/index.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/launch-readiness.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/market-assets.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/markets.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/my-watchlist.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/NDSP_Asset_View.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/NDSP_Command_Center.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/NDSP_Daily_Brief.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/NDSP_Settings_Alerts.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/nmp.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/phase.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/platform.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/radar.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/release-evidence.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/release-registry.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/settings.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/support-center.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/v13-experience.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/v14-experience.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/v14-final-evidence.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/v15-api-bridge.html
PUBLISHED_STABLE_GOLDEN_PAGE=/var/www/ndsp-my/v16-live-adapter.html
PUBLISHED_PUBLIC_PAGES_COUNT=37

## 6) Clean my.ndsp.app Nginx canonical route
CERT_FULLCHAIN=/etc/letsencrypt/live/my.ndsp.app/fullchain.pem
CERT_PRIVKEY=/etc/letsencrypt/live/my.ndsp.app/privkey.pem
CANONICAL_MY_CONF_WRITTEN=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
LEFT_NGINX_CONF_UNTOUCHED_SHARED_OR_OTHER_DOMAIN=/etc/nginx/conf.d/000-my.ndsp.app-final.conf
LEFT_NGINX_CONF_UNTOUCHED_SHARED_OR_OTHER_DOMAIN=/etc/nginx/conf.d/000-ndsp-main-redirect.conf.disabled_20260625_090629
QUARANTINED_MY_ONLY_NGINX_CONF_COUNT=0
2026/07/09 15:13:46 [warn] 3793687#3793687: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 15:13:46 [warn] 3793687#3793687: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 15:13:46 [warn] 3793687#3793687: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 15:13:46 [warn] 3793687#3793687: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
NGINX_RELOAD=OK

## 7) Rollback script
ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL_CLEAN_MY_NGINX_20260709_151344/ROLLBACK_V18_P8_D9_RADICAL_STABLE_GOLDEN_SHELL.sh

## 8) HTTP and content checks
HTTP_asset_selector=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_launch_readiness=200
HTTP_my_home=200
HTTP_decision_radar=200
HTTP_market_assets=200
HTTP_architecture_map=200
HTTP_CHECKS_OK=1
