# NDSP Release Handoff

DATE=2026-07-07T10:47:41+02:00
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/var/www/ndsp-my
PUBLIC_DOMAIN=https://my.ndsp.app
API_DOMAIN=https://api.ndsp.app

## Final Status

- RELEASE_STATUS=LOCKED
- FINAL_RELEASE_SWEEP=PASSED
- FINAL_RELEASE_SWEEP_REPORT=docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
- FINAL_POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103951.md
- OFFICIAL_RUNTIME=ndsp-portal
- PM2_STATUS=online
- PUBLIC_FORBIDDEN_WORDING=clean

## Locked Pages

- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html
- /disclaimer.html

## Locked Live Bind Assets

- /assets/ndsp-radar-safe-clean.js
- /assets/ndsp-decision-support-bind.js
- /assets/ndsp-asset-view-live-bind.js
- /assets/ndsp-daily-brief-live-bind.js
- /assets/ndsp-settings-alerts-bind.js
- /assets/ndsp-disclaimer-gate.js
- /assets/ndsp-global-menu.js

## Core Governance

NDSP is a decision support platform only.

It is not:

- a trading platform
- an execution system
- a financial recommendation engine
- a buy/sell signal bot

## Forbidden Public Behavior

- do not issue buy/sell commands
- do not expose hidden protected layers
- do not invent NMP from frontend
- do not invent scenario levels from frontend
- do not remove disclaimer gate
- do not remove sidebar/menu
- do not replace canonical pages with fallback pages
- do not add extra PM2 runtimes without governance approval

## Official Runtime

- PM2 process: ndsp-portal
- Other PM2 runtimes are not part of the locked release unless explicitly governed later.

## Data Source Rule

Frontend pages must display only backend-computed fields from:

- /api/decision/quality-live?symbol=...

Asset list source:

- /assets/ndsp-assets.json

## Locked Reports

- docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md
- docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
- docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103951.md
- docs/05-runbooks/NDSP_PATCH_COMMAND_CENTER_RADAR_BIND_V24_20260707_100000.md
- docs/05-runbooks/NDSP_PATCH_DECISION_SUPPORT_BIND_V1_20260707_100626.md
- docs/05-runbooks/NDSP_PATCH_ASSET_VIEW_LIVE_BIND_V1_20260707_101304.md
- docs/05-runbooks/NDSP_PATCH_DAILY_BRIEF_LIVE_BIND_V1_20260707_102950.md
- docs/05-runbooks/NDSP_PATCH_SETTINGS_ALERTS_BIND_V1_20260707_103642.md

## Rollback Policy

Every patch created a backup under:

- /home/nawaf511/ndsp_backups/

Rollback must use the exact rollback line inside each patch report.
Do not rollback blindly unless the relevant page/API/runtime fails.

## Final Rule

This handoff is the release baseline.

Any future modification must preserve:

- official routes
- disclaimer gate
- sidebar/menu
- radar
- live bind assets
- API field contract
- PM2 runtime cleanliness
- public language governance
