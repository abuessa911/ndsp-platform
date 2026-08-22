# NDSP External Tool Prompt — Locked Release

You are working on NDSP — Nawaf Decision Support Platform.

Before doing anything, read:

- docs/05-runbooks/NDSP_EXTERNAL_TOOL_GUARDRAILS_20260707_110424.md
- docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md
- docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
- docs/05-runbooks/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.md

Current state:

- Release is locked.
- Production snapshot exists.
- Final release sweep passed.
- Official runtime is ndsp-portal.
- Do not modify Nginx, PM2, API gateway, or /api/decision/quality-live.
- Do not remove disclaimer gate.
- Do not remove sidebar/menu.
- Do not break radar.
- Do not replace canonical pages with fallback pages.
- Do not expose protected or hidden layers.
- Do not invent NMP from frontend.
- Do not invent scenario levels from frontend.
- Do not use buy/sell/execution/recommendation language in public UI.

Locked pages:

- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html
- /disclaimer.html

Locked assets:

- /assets/ndsp-radar-safe-clean.js
- /assets/ndsp-decision-support-bind.js
- /assets/ndsp-asset-view-live-bind.js
- /assets/ndsp-daily-brief-live-bind.js
- /assets/ndsp-settings-alerts-bind.js
- /assets/ndsp-disclaimer-gate.js
- /assets/ndsp-global-menu.js

Allowed work only:

- visual spacing polish
- mobile polish
- accessibility labels
- text cleanup
- performance cleanup
- browser smoke test

Before any patch:

1. create backup
2. create patch report
3. change only the smallest necessary file
4. run:

FRONTEND_DIR="/var/www/ndsp-my" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/tests/ndsp_post_patch_test_AR.sh

Patch is accepted only if:

- FINAL_STATUS=POST_PATCH_TEST_OK

If unsure, do not modify. Create an audit report only.
