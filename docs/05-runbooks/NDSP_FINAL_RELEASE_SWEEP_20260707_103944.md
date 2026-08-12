# NDSP Final Release Sweep
DATE=2026-07-07T10:39:44+02:00
FRONTEND=/var/www/ndsp-my

## 1) Official Pages
[200] size=884 https://my.ndsp.app/
[200] size=884 https://my.ndsp.app/index.html
[200] size=2610 https://my.ndsp.app/decision-support.html
[200] size=2854 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=3310 https://my.ndsp.app/NDSP_Command_Center.html
[200] size=2611 https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=2579 https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=4677 https://my.ndsp.app/disclaimer.html

## 2) Bind Assets
[200] size=9846 https://my.ndsp.app/assets/ndsp-radar-safe-clean.js?v=24-command-bind
[200] size=6709 https://my.ndsp.app/assets/ndsp-decision-support-bind.js?v=1
[200] size=10160 https://my.ndsp.app/assets/ndsp-asset-view-live-bind.js?v=1
[200] size=9632 https://my.ndsp.app/assets/ndsp-daily-brief-live-bind.js?v=1
[200] size=11545 https://my.ndsp.app/assets/ndsp-settings-alerts-bind.js?v=1
[200] size=500 https://my.ndsp.app/assets/ndsp-disclaimer-gate.js?v=1
[200] size=10444 https://my.ndsp.app/assets/ndsp-global-menu.js?v=25-canonical-page-match

## 3) API Samples
--- ETHUSDT ---
ok= True
symbol= ETHUSDT
live_price= 1771.24
quality= 86
scenario= UNDER_MONITORING
direction= قراءة أسبوعي · ضغط هابط
nmp= AVAILABLE 1583.4

--- BTCUSDT ---
ok= True
symbol= BTCUSDT
live_price= 63083.18
quality= 86
scenario= UNDER_MONITORING
direction= قراءة أسبوعي · ضغط هابط
nmp= AVAILABLE 61056.47

--- XAUUSD ---
ok= True
symbol= XAUUSD
live_price= 4149.5
quality= 60
scenario= UNDER_MONITORING
direction= قراءة أسبوعي · ضغط سفلي
nmp= UNAVAILABLE None

--- USOIL ---
ok= True
symbol= USOIL
live_price= 69.12000274658203
quality= 56
scenario= UNDER_MONITORING
direction= قراءة أسبوعي · ضغط سفلي
nmp= UNAVAILABLE None

## 4) Required Markers
RADAR_MARKERS=28
DECISION_SUPPORT_MARKERS=1
ASSET_VIEW_MARKERS=1
DAILY_BRIEF_MARKERS=1
SETTINGS_ALERTS_MARKERS=1
DISCLAIMER_MARKERS=23
MENU_MARKERS=24

## 5) PM2
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 44h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 8.3% | ram usage: 9.3% | lo: ⇓ 0.004mb/s ⇑ 0.004mb/s | eth0: ⇓ 0.019mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.21mb/s / 81.79% |

## 6) Official Post Patch Test
# NDSP Post Patch Test Report
DATE=20260707_103951
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
RADAR_FILE_COUNT=461
SIDEBAR_FILE_COUNT=55
DISCLAIMER_FILE_COUNT=679
[OK] Radar presence detected
[OK] Sidebar presence detected
[OK] Disclaimer presence detected

## 4) Forbidden Wording Scan
[OK] No forbidden public wording found

## 5) PM2 Runtime Check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 44h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 10.6% | ram usage: 9.3% | lo: ⇓ 0.022mb/s ⇑ 0.022mb/s | eth0: ⇓ 0.204mb/s ⇑ 0.008mb/s | disk: ⇓ 0mb/s ⇑ 0.187mb/s / 81.79% |

FINAL_STATUS=POST_PATCH_TEST_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103951.md

FINAL_STATUS=FINAL_RELEASE_SWEEP_DONE
REPORT=docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
