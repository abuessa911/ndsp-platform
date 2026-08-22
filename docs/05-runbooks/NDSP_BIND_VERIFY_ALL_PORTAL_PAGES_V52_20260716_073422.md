# NDSP Bind And Verify All Portal Pages V52

- Date: 2026-07-16T07:34:22+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Portal: v50
- Mode: STRICT_CONTEXT_BINDING_NO_FABRICATION_MULTI_PAGE_BROWSER_GATE
- Backup: /home/nawaf511/ndsp_launch_backups/bind_verify_all_portal_pages_v52_20260716_073422
- Output: /home/nawaf511/ndsp_launch_reports/NDSP_BIND_VERIFY_ALL_PORTAL_PAGES_V52_20260716_073422
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_BIND_VERIFY_ALL_PORTAL_PAGES_V52_20260716_073422.md

== 1) Current protected public state ==
ROOT_STATUS=302
ROOT_LOCATION=https://www.ndsp.app/
LOGIN_STATUS=200
REGISTER_STATUS=200

== 2) Backup source, live runtime and aliases ==
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
BACKUP: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/index.html
BACKUP: /var/www/ndsp-my/portal-v50/index.html
BACKUP: /var/www/ndsp-my/NDSP_Command_Center.html
BACKUP: /var/www/ndsp-my/analysis-center.html
BACKUP: /var/www/ndsp-my/asset-selector.html
BACKUP: /var/www/ndsp-my/command-center.html
BACKUP: /var/www/ndsp-my/completed-decisions-review.html
BACKUP: /var/www/ndsp-my/completed-decisions.html
BACKUP: /var/www/ndsp-my/dashboard.html
BACKUP: /var/www/ndsp-my/data-freshness.html
BACKUP: /var/www/ndsp-my/data-health.html
BACKUP: /var/www/ndsp-my/decision-center.html
BACKUP: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/decision-layers.html
BACKUP: /var/www/ndsp-my/decision-radar.html
BACKUP: /var/www/ndsp-my/decision-room.html
BACKUP: /var/www/ndsp-my/decision-support.html
BACKUP: /var/www/ndsp-my/governance.html
BACKUP: /var/www/ndsp-my/guide.html
BACKUP: /var/www/ndsp-my/market-assets.html
BACKUP: /var/www/ndsp-my/markets.html
BACKUP: /var/www/ndsp-my/my-watchlist.html
BACKUP: /var/www/ndsp-my/nmp.html
BACKUP: /var/www/ndsp-my/platform-capabilities.html
BACKUP: /var/www/ndsp-my/platform.html
BACKUP: /var/www/ndsp-my/portal-v50/capabilities/index.html
BACKUP: /var/www/ndsp-my/portal-v50/completed/index.html
BACKUP: /var/www/ndsp-my/portal-v50/data/index.html
BACKUP: /var/www/ndsp-my/portal-v50/decision/index.html
BACKUP: /var/www/ndsp-my/portal-v50/guide/index.html
BACKUP: /var/www/ndsp-my/portal-v50/home/index.html
BACKUP: /var/www/ndsp-my/portal-v50/index.html
BACKUP: /var/www/ndsp-my/portal-v50/layers/index.html
BACKUP: /var/www/ndsp-my/portal-v50/markets/index.html
BACKUP: /var/www/ndsp-my/portal-v50/risk/index.html
BACKUP: /var/www/ndsp-my/portal-v50/scenarios/index.html
BACKUP: /var/www/ndsp-my/portal-v50/selector/index.html
BACKUP: /var/www/ndsp-my/portal.html
BACKUP: /var/www/ndsp-my/radar.html
BACKUP: /var/www/ndsp-my/risk-governance.html
BACKUP: /var/www/ndsp-my/scenario-levels.html

== 3) Patch strict binding, translation and no-fabrication rules ==
UPDATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
UPDATED: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js

== 4) Break stale HTML module cache without touching landing/auth ==
UPDATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/index.html
UPDATED: /var/www/ndsp-my/portal-v50/index.html
UPDATED: /var/www/ndsp-my/NDSP_Command_Center.html
UPDATED: /var/www/ndsp-my/analysis-center.html
UPDATED: /var/www/ndsp-my/asset-selector.html
UPDATED: /var/www/ndsp-my/command-center.html
UPDATED: /var/www/ndsp-my/completed-decisions-review.html
UPDATED: /var/www/ndsp-my/completed-decisions.html
UPDATED: /var/www/ndsp-my/dashboard.html
UPDATED: /var/www/ndsp-my/data-freshness.html
UPDATED: /var/www/ndsp-my/data-health.html
UPDATED: /var/www/ndsp-my/decision-center.html
UPDATED: /var/www/ndsp-my/decision-guide.html
UPDATED: /var/www/ndsp-my/decision-layers.html
UPDATED: /var/www/ndsp-my/decision-radar.html
UPDATED: /var/www/ndsp-my/decision-room.html
UPDATED: /var/www/ndsp-my/decision-support.html
UPDATED: /var/www/ndsp-my/governance.html
UPDATED: /var/www/ndsp-my/guide.html
UPDATED: /var/www/ndsp-my/market-assets.html
UPDATED: /var/www/ndsp-my/markets.html
UPDATED: /var/www/ndsp-my/my-watchlist.html
UPDATED: /var/www/ndsp-my/nmp.html
UPDATED: /var/www/ndsp-my/platform-capabilities.html
UPDATED: /var/www/ndsp-my/platform.html
UPDATED: /var/www/ndsp-my/portal-v50/capabilities/index.html
UPDATED: /var/www/ndsp-my/portal-v50/completed/index.html
UPDATED: /var/www/ndsp-my/portal-v50/data/index.html
UPDATED: /var/www/ndsp-my/portal-v50/decision/index.html
UPDATED: /var/www/ndsp-my/portal-v50/guide/index.html
UPDATED: /var/www/ndsp-my/portal-v50/home/index.html
NO_CHANGE: /var/www/ndsp-my/portal-v50/index.html
UPDATED: /var/www/ndsp-my/portal-v50/layers/index.html
UPDATED: /var/www/ndsp-my/portal-v50/markets/index.html
UPDATED: /var/www/ndsp-my/portal-v50/risk/index.html
UPDATED: /var/www/ndsp-my/portal-v50/scenarios/index.html
UPDATED: /var/www/ndsp-my/portal-v50/selector/index.html
UPDATED: /var/www/ndsp-my/portal.html
UPDATED: /var/www/ndsp-my/radar.html
UPDATED: /var/www/ndsp-my/risk-governance.html
UPDATED: /var/www/ndsp-my/scenario-levels.html

== 5) Static registry and runtime gates ==
CAPABILITY_COUNT=28
HTTP 200: /analysis-center.html
HTTP 200: /portal.html
HTTP 200: /market-assets.html
HTTP 200: /decision-support.html
HTTP 200: /decision-layers.html
HTTP 200: /platform-capabilities.html
HTTP 200: /scenario-levels.html
HTTP 200: /risk-governance.html
HTTP 200: /completed-decisions.html
HTTP 200: /data-health.html
HTTP 200: /decision-guide.html

== 6) Comprehensive mobile and desktop browser gate ==
SELECTED_MARKET=CRYPTO
CANONICAL_CONTEXT={"market":"CRYPTO","symbol":"ETHUSDT","timeframe":"weekly","mode":"speculative","view":"beginner","session":"NDSP-7257AC45-MRN2R26O"}
COMPREHENSIVE_GATE_ERROR=page.evaluate: SyntaxError: Failed to execute 'json' on 'Response': Unexpected token '<', "<html>
<h"... is not valid JSON
    at eval (eval at evaluate (:303:30), <anonymous>:8:27)
    at async <anonymous>:329:30
    at /tmp/ndsp_bind_verify_all_portal_pages_v52_20260716_073422.js:79:33
