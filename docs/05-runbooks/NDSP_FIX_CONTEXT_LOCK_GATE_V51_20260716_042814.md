# NDSP Context Lock Gate Fix V51

- Date: 2026-07-16T04:28:15+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Portal: v50
- Mode: NORMALIZE_REGISTRY_PATCH_HELPERS_STRICT_BROWSER_GATE
- Backup: /home/nawaf511/ndsp_launch_backups/fix_context_lock_gate_v51_20260716_042814
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_CONTEXT_LOCK_GATE_V51_20260716_042814.md

== 1) Backup source and live files ==
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
BACKUP: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js
BACKUP: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/config/assets.json
BACKUP: /var/www/ndsp-my/portal-v50/config/assets.json

== 2) Normalize asset registry ==
UPDATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/config/assets.json
UPDATED: /var/www/ndsp-my/portal-v50/config/assets.json

== 3) Patch context helper functions ==
UPDATED: /home/nawaf511/empire-core-new/frontend/ndsp-user-portal-v50/assets/ndsp-portal-v50.js
UPDATED: /var/www/ndsp-my/portal-v50/assets/ndsp-portal-v50.js

== 4) Public route checks ==
HTTP 200: https://my.ndsp.app/analysis-center.html?v=20260716_042814
HTTP 200: https://my.ndsp.app/portal.html?v=20260716_042814
HTTP 200: https://my.ndsp.app/decision-support.html?v=20260716_042814
HTTP 200: https://my.ndsp.app/portal-v50/config/assets.json?v=20260716_042814
HTTP 200: https://my.ndsp.app/portal-v50/assets/ndsp-portal-v50.js?v=20260716_042814
ROOT_STATUS=302
ROOT_LOCATION=https://www.ndsp.app/

== 5) Strict browser context-lock gate ==
FINAL_URL=https://my.ndsp.app/portal.html?market=CRYPTO&symbol=ETHUSDT&timeframe=weekly&mode=speculative&view=beginner&session=NDSP-7257AC45-MRMW3KIL
SELECTED_MARKET=CRYPTO
CONTEXT_LOCKED=1
HAS_ETH=YES
QUERY_SYMBOL=ETHUSDT
QUERY_TIMEFRAME=weekly
QUERY_MODE=speculative
QUERY_VIEW=beginner
HAS_SESSION=YES
HAS_DECISION_LINK=3
STRICT_GATE=PASS
SCREENSHOT=/tmp/ndsp_context_lock_gate_v51_20260716_042814.png

== 6) Create rollback ==
ROLLBACK=/tmp/ndsp_rollback_fix_context_lock_gate_v51_20260716_042814.sh

== 7) Final summary ==
Landing redirect preserved.
Context lock proven in a real mobile browser flow.
FINAL_STATUS=OK
