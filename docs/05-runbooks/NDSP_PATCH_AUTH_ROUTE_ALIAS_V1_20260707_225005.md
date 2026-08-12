# NDSP Auth Route Alias Patch V1
DATE=2026-07-07T22:50:05+02:00
MODE=STATIC_ROUTE_ALIAS_ONLY
LIVE=/var/www/ndsp-my
BACKUP=/home/nawaf511/ndsp_backups/NDSP_AUTH_ROUTE_ALIAS_PATCH_V1_20260707_225005

## Scope
- Create safe static route aliases only.
- /login -> /login.html
- /register -> /register.html
- /forgot-password -> /forgot-password.html
- /reset-password -> /reset-password.html
- Preserve query string and hash through JavaScript redirect.
- No Nginx changes.
- No PM2 restart.
- No API changes.
- No Backend changes.
- No Priority 1 internal page changes.

[OK] No existing dir, will create: /var/www/ndsp-my/login
[OK] Alias created: /login -> /login.html
[OK] No existing dir, will create: /var/www/ndsp-my/register
[OK] Alias created: /register -> /register.html
[OK] No existing dir, will create: /var/www/ndsp-my/forgot-password
[OK] Alias created: /forgot-password -> /forgot-password.html
[OK] No existing dir, will create: /var/www/ndsp-my/reset-password
[OK] Alias created: /reset-password -> /reset-password.html

## Marker Verification
--- login/index.html ---
8:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_START -->
15:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_END -->
--- register/index.html ---
8:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_START -->
15:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_END -->
--- forgot-password/index.html ---
8:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_START -->
15:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_END -->
--- reset-password/index.html ---
8:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_START -->
15:  <!-- NDSP_AUTH_ROUTE_ALIAS_V1_END -->

## HTTP Status After Patch
[200] https://my.ndsp.app/login
[200] https://my.ndsp.app/login.html
[200] https://my.ndsp.app/register
[200] https://my.ndsp.app/register.html
[200] https://my.ndsp.app/forgot-password
[200] https://my.ndsp.app/forgot-password.html
[200] https://my.ndsp.app/reset-password
[200] https://my.ndsp.app/reset-password.html
[200] https://my.ndsp.app/password-reset
[200] https://my.ndsp.app/password-reset.html

## Forbidden Wording Scan In Alias Files
[OK] no sensitive terms

## PM2 Check Before Post Patch
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 8.5% | ram usage: 9.5% | lo: ⇓ 0.002mb/s ⇑ 0.002mb/s | eth0: ⇓ 0.006mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.27mb/s / 81.98% |

== Post Patch Test ==
# NDSP Post Patch Test Report
DATE=20260707_225006
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
RADAR_FILE_COUNT=468
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
host metrics | cpu: 16.1% | ram usage: 9.8% | lo: ⇓ 0.018mb/s ⇑ 0.018mb/s | eth0: ⇓ 0.178mb/s ⇑ 0.006mb/s | disk: ⇓ 15.806mb/s ⇑ 0.22mb/s / 81.98% |

FINAL_STATUS=POST_PATCH_TEST_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_225006.md
[OK] Auth alias 200: /login
[OK] Auth alias 200: /register
[OK] Auth alias 200: /forgot-password
[OK] Auth alias 200: /reset-password
FINAL_STATUS=AUTH_ROUTE_ALIAS_V1_PATCH_APPLIED
POST_PATCH_STATUS=OK
