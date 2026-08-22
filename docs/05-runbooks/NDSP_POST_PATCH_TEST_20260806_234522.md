# NDSP Post Patch Test Report
DATE=20260806_234522
PROJECT_DIR=/home/nawaf511/empire-core-new
FRONTEND_DIR=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) Required Pages HTTP
[ALERT] HTTP 302 https://my.ndsp.app/
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
RADAR_FILE_COUNT=155
SIDEBAR_FILE_COUNT=85
DISCLAIMER_FILE_COUNT=645
[OK] Radar presence detected
[OK] Sidebar presence detected
[OK] Disclaimer presence detected

## 4) Forbidden Wording Scan
[ALERT] Forbidden public wording count: 0
[ALERT] Unsafe execution-order wording count: 1

## 5) PM2 Runtime Check
┌────┬─────────────────────────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name                                │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────────────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 2  │ ndsp-launch-control-v167            │ default     │ 1.0.0   │ fork    │ 4508     │ 3D     │ 0    │ online    │ 0%       │ 27.5mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal                         │ default     │ 0.39.7  │ fork    │ 4474     │ 3D     │ 0    │ online    │ 0%       │ 78.0mb   │ root     │ disabled │
│ 3  │ ndsp-telegram-notifications-v182    │ default     │ 1.0.0   │ fork    │ 4521     │ 3D     │ 0    │ online    │ 0%       │ 24.4mb   │ nawaf511 │ disabled │
│ 1  │ ndsp-trial-clock-v164               │ default     │ 1.0.0   │ fork    │ 4498     │ 3D     │ 0    │ online    │ 0%       │ 21.6mb   │ nawaf511 │ disabled │
└────┴─────────────────────────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 12.2% | ram usage: 12.9% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.071mb/s ⇑ 0.002mb/s | disk: ⇓ 4.948mb/s ⇑ 0.192mb/s / 76.85% |

FINAL_STATUS=POST_PATCH_TEST_WITH_ALERTS
ALERTS=3
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_POST_PATCH_TEST_20260806_234522.md
