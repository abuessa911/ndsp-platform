# NDSP Context-First Multi-Page User Portal v50

- Date: 2026-07-16T02:27:24+02:00
- Project: /home/nawaf511/empire-core-new
- Live root: /var/www/ndsp-my
- Source: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50
- Live portal: /var/www/ndsp-my/portal-v50
- Mode: ADDITIVE_MULTI_PAGE_CONTEXT_LOCK_NO_BACKEND_LOGIC_CHANGE
- Backup: /home/nawaf511/ndsp_launch_backups/context_first_portal_v50_20260716_022724
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_INSTALL_CONTEXT_FIRST_PORTAL_V50_20260716_022724.md

== 1) Create governed context contract ==
CREATED: /home/nawaf511/empire-core-new/docs/03-contracts/NDSP_ANALYSIS_CONTEXT_LOCK_CONTRACT_V1.json
CREATED: /home/nawaf511/empire-core-new/docs/02-user-guide/NDSP_USER_PORTAL_INFORMATION_ARCHITECTURE_V50_AR.md

== 2) Create canonical display registries ==
COPIED CANONICAL: /home/nawaf511/empire-core-new/docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json
COPIED CANONICAL: /home/nawaf511/empire-core-new/docs/03-contracts/NDSP_PLATFORM_CAPABILITY_REGISTRY_V1.json
COPIED CANONICAL: /home/nawaf511/empire-core-new/docs/03-contracts/NDSP_ASSET_MASTER_REGISTRY_V1.json

== 3) Create portal HTML ==
CREATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/index.html

== 4) Create professional responsive CSS ==
CREATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.css

== 5) Create context-locked multi-page JavaScript ==
CREATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js

== 6) Validate source syntax ==
OK: JS and JSON syntax passed.

== 7) Backup current live targets ==
BACKUP: /var/www/ndsp-my/decision-guide.html
BACKUP: /var/www/ndsp-my/guide.html

== 8) Deploy portal source to live ==
DEPLOYED: /var/www/ndsp-my/portal-v50
ALIAS: /analysis-center.html
ALIAS: /asset-selector.html
ALIAS: /portal.html
ALIAS: /dashboard.html
ALIAS: /platform.html
ALIAS: /command-center.html
ALIAS: /NDSP_Command_Center.html
ALIAS: /market-assets.html
ALIAS: /markets.html
ALIAS: /my-watchlist.html
ALIAS: /decision-support.html
ALIAS: /decision-center.html
ALIAS: /decision-room.html
ALIAS: /decision-layers.html
ALIAS: /decision-radar.html
ALIAS: /radar.html
ALIAS: /platform-capabilities.html
ALIAS: /scenario-levels.html
ALIAS: /nmp.html
ALIAS: /risk-governance.html
ALIAS: /governance.html
ALIAS: /completed-decisions.html
ALIAS: /completed-decisions-review.html
ALIAS: /data-health.html
ALIAS: /data-freshness.html
ALIAS: /decision-guide.html
ALIAS: /guide.html

== 9) Preserve landing root and authentication pages ==
ROOT_STATUS=302
ROOT_LOCATION=https://www.ndsp.app/
LOGIN_HTTP=200
REGISTER_HTTP=200

== 10) HTTP route checks ==
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

== 11) Browser context-lock gate ==
FINAL_URL=https://my.ndsp.app/analysis-center.html?v=1784161649755
CONTEXT_LOCKED=0
HAS_ETH=NO
HAS_DECISION_LINK=3
SCREENSHOT=/tmp/ndsp_context_first_portal_mobile.png

== 12) Create rollback script ==
ROLLBACK=/tmp/ndsp_rollback_context_first_portal_v50_20260716_022724.sh

== 13) Final summary ==
Landing root remains controlled separately: https://my.ndsp.app/
New first step: https://my.ndsp.app/analysis-center.html
New decision room: https://my.ndsp.app/decision-support.html
New user home: https://my.ndsp.app/portal.html
Context contract: /home/nawaf511/empire-core-new/docs/03-contracts/NDSP_ANALYSIS_CONTEXT_LOCK_CONTRACT_V1.json
Source of truth: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50

FINAL_STATUS=OK
