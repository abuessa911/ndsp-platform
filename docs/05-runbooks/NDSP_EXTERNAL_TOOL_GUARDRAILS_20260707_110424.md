# NDSP External Tool Guardrails

## Purpose

This document is mandatory for any external AI tool, developer, or automation working on NDSP after the locked release.

NDSP is currently in a locked production snapshot state.

## Current Release Status

- RELEASE_STATUS=LOCKED
- FINAL_RELEASE_SWEEP=PASSED
- PRODUCTION_SNAPSHOT=CREATED
- OFFICIAL_RUNTIME=ndsp-portal
- PM2_STATUS=online
- PUBLIC_LANGUAGE_STATUS=clean
- SNAPSHOT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz
- SNAPSHOT_SHA256=ab006cc5201bbde45da508366a78a23b7ec66cbc78db10fcaad881f43a6118ef

## Absolute Rules

Do not modify these unless the owner explicitly approves:

- Nginx
- PM2 runtime
- API gateway
- /api/decision/quality-live
- disclaimer gate
- sidebar/menu
- radar
- canonical page routes
- protected layer names
- hidden decision layers

## Locked Official Pages

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

## Product Identity

NDSP is a decision support platform only.

NDSP is not:

- a trading platform
- an execution system
- a financial recommendation engine
- a buy/sell signal bot

## Forbidden Public Language

Do not show public UI phrases that imply:

- buy
- sell
- enter trade
- exit trade
- execute
- guaranteed profit
- financial recommendation

Allowed public language:

- reading
- monitoring
- scenario state
- decision quality
- directional context
- caution reason
- NMP status
- support decision

## Data Binding Rule

Frontend must not invent data.

Frontend may display only backend-computed fields from:

- /api/decision/quality-live?symbol=...

Asset list source:

- /assets/ndsp-assets.json

## NMP Rule

NMP must remain backend-computed only.

Frontend may display:

- nmp_status
- nmp_level

Frontend must not calculate or infer NMP.

## Scenario Levels Rule

Scenario levels must remain backend-computed only.

Frontend may display:

- scenario_activation_level
- scenario_arrival_level
- scenario_review_zone
- scenario_invalidation_level

Frontend must not invent scenario levels.

## Safe Future Work

Allowed only with backup and post-patch test:

1. visual spacing polish
2. mobile rendering polish
3. accessibility labels
4. text cleanup
5. performance cleanup
6. browser smoke test

## Required Before Any Patch

Before changing anything, create a backup.

After changing anything, run:

FRONTEND_DIR="/var/www/ndsp-my" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/tests/ndsp_post_patch_test_AR.sh

The patch is not accepted unless:

- FINAL_STATUS=POST_PATCH_TEST_OK

## Rollback

Use rollback lines inside patch reports under:

- docs/05-runbooks/

Backups are under:

- /home/nawaf511/ndsp_backups/

Do not rollback blindly.

## Final Instruction To External Tools

If you are unsure, do not modify runtime or frontend.
Create an audit report first.
