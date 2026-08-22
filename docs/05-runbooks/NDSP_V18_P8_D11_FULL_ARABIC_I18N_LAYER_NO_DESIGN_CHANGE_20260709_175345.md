# NDSP V1.8 / P8-D11 — Full Arabic Language Layer, No Design Change
DATE=2026-07-09T17:53:45+02:00
MODE=FULL_ARABIC_I18N_RUNTIME_LAYER_NO_DESIGN_CHANGE
LIVE=/var/www/ndsp-my
I18N_FILE=/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js
NO_REACT_BUILD=1
NO_DESIGN_CSS_CHANGE=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_DB_CHANGE=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_MODIFY=1
NO_REBOOT=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_20260709_175345.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_20260709_175345
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz

## 1) Preflight runtime reference
FAILED_UNITS_COUNT_BEFORE=0
NGINX_ACTIVE_BEFORE=active
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.

## 2) Backup HTML pages and previous i18n file
HTML_FILES_COUNT=45

## 3) Create full Arabic runtime i18n layer
I18N_FILE_CREATED=/var/www/ndsp-my/approved-design/ndsp-full-ar-i18n-v18-d11.js
I18N_DICTIONARY_APPROX_COUNT=159

## 4) Inject i18n script into HTML pages only
I18N_INJECTED=/var/www/ndsp-my/alerts-log.html
I18N_INJECTED=/var/www/ndsp-my/architecture-map.html
I18N_INJECTED=/var/www/ndsp-my/asset.html
I18N_INJECTED=/var/www/ndsp-my/asset-selector.html
I18N_INJECTED=/var/www/ndsp-my/command-center.html
I18N_INJECTED=/var/www/ndsp-my/completed-decisions.html
I18N_INJECTED=/var/www/ndsp-my/completed-decisions-review.html
I18N_INJECTED=/var/www/ndsp-my/completed-decisions-v14.html
I18N_INJECTED=/var/www/ndsp-my/daily-brief.html
I18N_INJECTED=/var/www/ndsp-my/data-freshness.html
I18N_INJECTED=/var/www/ndsp-my/decision-center.html
I18N_INJECTED=/var/www/ndsp-my/decision-guide.html
I18N_INJECTED=/var/www/ndsp-my/decision-modes-guide.html
I18N_INJECTED=/var/www/ndsp-my/decision-radar.html
I18N_INJECTED=/var/www/ndsp-my/decision-room-guide.html
I18N_INJECTED=/var/www/ndsp-my/decision-support.html
I18N_INJECTED=/var/www/ndsp-my/disclaimer.html
I18N_INJECTED=/var/www/ndsp-my/dollar-impact.html
I18N_INJECTED=/var/www/ndsp-my/dollar-news.html
I18N_INJECTED=/var/www/ndsp-my/guide.html
I18N_INJECTED=/var/www/ndsp-my/index.html
I18N_INJECTED=/var/www/ndsp-my/launch-readiness.html
I18N_INJECTED=/var/www/ndsp-my/market-assets.html
I18N_INJECTED=/var/www/ndsp-my/markets.html
I18N_INJECTED=/var/www/ndsp-my/my-watchlist.html
I18N_INJECTED=/var/www/ndsp-my/NDSP_Asset_View.html
I18N_INJECTED=/var/www/ndsp-my/NDSP_Command_Center.html
I18N_INJECTED=/var/www/ndsp-my/NDSP_Daily_Brief.html
I18N_INJECTED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
I18N_INJECTED=/var/www/ndsp-my/nmp.html
I18N_INJECTED=/var/www/ndsp-my/phase.html
I18N_INJECTED=/var/www/ndsp-my/platform.html
I18N_INJECTED=/var/www/ndsp-my/pro-guide.html
I18N_INJECTED=/var/www/ndsp-my/radar.html
I18N_INJECTED=/var/www/ndsp-my/release-evidence.html
I18N_INJECTED=/var/www/ndsp-my/release-registry.html
I18N_INJECTED=/var/www/ndsp-my/settings.html
I18N_INJECTED=/var/www/ndsp-my/support-center.html
I18N_INJECTED=/var/www/ndsp-my/usd-pulse.html
I18N_INJECTED=/var/www/ndsp-my/user-guide.html
I18N_INJECTED=/var/www/ndsp-my/v13-experience.html
I18N_INJECTED=/var/www/ndsp-my/v14-experience.html
I18N_INJECTED=/var/www/ndsp-my/v14-final-evidence.html
I18N_INJECTED=/var/www/ndsp-my/v15-api-bridge.html
I18N_INJECTED=/var/www/ndsp-my/v16-live-adapter.html
I18N_INJECTED=/var/www/ndsp-my/approved-design/index.html
I18N_INJECTED_COUNT=46
I18N_ALREADY_PRESENT_COUNT=0

## 5) Verify script injection and HTTP
SCRIPT_TAG_HITS=46
I18N_MARKER_HITS=46
HTTP_register=200
HTTP_asset_selector=200
HTTP_api_health=200
HTTP_quality_live=200
HTTP_decision_guide=200
HTTP_i18n=200
HTTP_my_home=200
HTTP_completed_decisions=200
HTTP_decision_support=200
HTTP_decision_radar=200
HTTP_login=200
HTTP_market_assets=200
HTTP_admin=200
HTTP_nmp=200
HTTP_CHECKS_OK=1

## 6) Runtime after
FAILED_UNITS_COUNT_AFTER=0
NGINX_ACTIVE_AFTER=active
PM2_ACTIVE_AFTER=active
PM2_ENABLED_AFTER=enabled
MARKET_UPDATER_SERVICE_FAILED_AFTER=inactive
ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff  /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
e60cc1f0d100c833c43ba763422ff7de5a46a495fea34243da652f9e4e149633  /var/www/ndsp-my/assets/ndsp-global-menu.js
0c78267763a4b413fea671519ababf76e6bfe5f77b2e439cd42aa23f60b96d5a  /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 7) Rollback helper
ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_20260709_175345/ROLLBACK_V18_P8_D11_FULL_ARABIC_I18N_LAYER.sh

## 8) Stage package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz.sha256
c72f4d216c18073ccf2602e2a638079a6edd0b69965375dfb8076d0c13f227ae  /home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz

## 9) Final Evaluation
OK_EVALUATION=1
V18_P8_D11_FULL_ARABIC_I18N_LAYER_STATUS=OK
V18_P8_D11_NO_DESIGN_CHANGE_STATUS=OK
V18_P8_D11_LANGUAGE_BUTTON_STATUS=OK
V18_P8_D11_ROLLBACK_STATUS=AVAILABLE
V18_P8_D11_FINAL_PACKAGE_STATUS=CREATED
FINAL_STATUS=V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_20260709_175345.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D11_FULL_ARABIC_I18N_LAYER_NO_DESIGN_CHANGE_PACKAGE_20260709_175345.tar.gz.sha256
