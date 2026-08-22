# NDSP Asset View Content Patch V1
DATE=2026-07-07T20:46:02+02:00
MODE=HTML_CONTENT_ONLY
TARGETS=NDSP_Asset_View.html, asset-selector.html
BACKUP=/home/nawaf511/ndsp_backups/NDSP_ASSET_VIEW_CONTENT_PATCH_V1_20260707_204602

## Scope
- Add explanatory asset-selection content block.
- No API changes.
- No PM2 changes.
- No Nginx changes.
- No JS changes.
- No route rename/delete.

[OK] Backup NDSP_Asset_View.html
[OK] Backup asset-selector.html

## Marker verification
--- NDSP_Asset_View.html ---
61:<!-- NDSP_ASSET_VIEW_CONTENT_V1_START -->
109:<!-- NDSP_ASSET_VIEW_CONTENT_V1_END -->
--- asset-selector.html ---
60:<!-- NDSP_ASSET_VIEW_CONTENT_V1_START -->
108:<!-- NDSP_ASSET_VIEW_CONTENT_V1_END -->

## Sensitive wording check in target pages
--- NDSP_Asset_View.html ---
[OK] no sensitive terms
--- asset-selector.html ---
[OK] no sensitive terms

== Post Patch Test ==
# NDSP Post Patch Test Report
DATE=20260707_204602
PROJECT_DIR=/home/nawaf511/empire-core-new
FRONTEND_DIR=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) Required Pages HTTP
[200] https://my.ndsp.app/
[200] https://my.ndsp.app/index.html
[200] https://my.ndsp.app/decision-support.html
[200] https://my.ndsp.app/NDSP_Asset_View.html
[200] https://my.ndsp.app/NDSP_Command_Center.html
[200] https://my.ndsp.app/NDSP_Daily_Brief.html
[200] https://my.ndsp.app/NDSP_Settings_Alerts.html

## 2) Decision API Required Fields
[OK] field: symbol via instrument.symbol
[OK] field: live_price via instrument.live_price
[OK] field: decision_quality via allowed_public_outputs.decision_quality
[OK] field: scenario_state via scenario.scenario_state
[OK] field: directional_context via scenario.scenario_directional_context
[OK] field: nmp_status via scenario.nmp_status
[OK] field: nmp_level via scenario.nmp_level

## 3) Protected UI Elements
RADAR_FILE_COUNT=462
SIDEBAR_FILE_COUNT=55
DISCLAIMER_FILE_COUNT=680
[OK] Radar presence detected
[OK] Sidebar presence detected
[OK] Disclaimer presence detected

## 4) Forbidden Wording Scan
[OK] No forbidden public wording found

## 5) PM2 Runtime Check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11.1% | ram usage: 9.5% | lo: ⇓ 0.012mb/s ⇑ 0.012mb/s | eth0: ⇓ 0.174mb/s ⇑ 0.007mb/s | disk: ⇓ 0mb/s ⇑ 0.265mb/s / 81.97% |

FINAL_STATUS=POST_PATCH_TEST_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_204602.md
FINAL_STATUS=ASSET_VIEW_CONTENT_V1_PATCH_APPLIED
POST_PATCH_STATUS=OK
