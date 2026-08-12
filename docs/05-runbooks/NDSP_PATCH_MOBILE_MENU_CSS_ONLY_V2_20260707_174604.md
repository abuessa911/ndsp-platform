# NDSP Mobile Menu CSS-only Patch V2
DATE=2026-07-07T17:46:04+02:00
MODE=CSS_ONLY
LIVE=/var/www/ndsp-my
CSS=/var/www/ndsp-my/assets/ndsp-global-menu.css
BACKUP=/home/nawaf511/ndsp_backups/NDSP_MOBILE_MENU_CSS_ONLY_V2_20260707_174604

## Purpose
- Improve menu readability after V1.
- Make menu panel less transparent.
- Increase item/text contrast.
- Keep scrollbar dark/gold.
- Do not modify JS, API, PM2, Nginx, radar logic, or disclaimer logic.

## Backup
-rw-rw-r-- 1 nawaf511 nawaf511 7.5K يوليو   7 17:22 /home/nawaf511/ndsp_backups/NDSP_MOBILE_MENU_CSS_ONLY_V2_20260707_174604/ndsp-global-menu.css.before

## Patch
OK: CSS V2 patch appended

## Cache bust CSS references
[OK] cache-busted index.html
[OK] cache-busted decision-support.html
[OK] cache-busted NDSP_Asset_View.html
[OK] cache-busted NDSP_Command_Center.html
[OK] cache-busted NDSP_Daily_Brief.html
[OK] cache-busted NDSP_Settings_Alerts.html

## Verify marker
338:/* NDSP_MOBILE_MENU_CSS_ONLY_V2_START */
443:/* NDSP_MOBILE_MENU_CSS_ONLY_V2_END */

## Post patch test
# NDSP Post Patch Test Report
DATE=20260707_174605
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
host metrics | cpu: 14% | ram usage: 9.7% | lo: ⇓ 0.013mb/s ⇑ 0.013mb/s | eth0: ⇓ 0.174mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.156mb/s / 81.95% |

FINAL_STATUS=POST_PATCH_TEST_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_174605.md

FINAL_STATUS=MOBILE_MENU_CSS_ONLY_V2_PATCH_APPLIED
POST_PATCH_STATUS=OK
