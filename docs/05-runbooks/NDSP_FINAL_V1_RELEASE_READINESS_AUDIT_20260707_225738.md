# NDSP Final V1 Release Readiness Audit
DATE=2026-07-07T22:57:38+02:00
MODE=READ_ONLY
MODIFICATIONS=None
LIVE=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) Official Priority Pages HTTP
[200] https://my.ndsp.app/
[200] https://my.ndsp.app/index.html
[200] https://my.ndsp.app/decision-support.html
[200] https://my.ndsp.app/NDSP_Asset_View.html
[200] https://my.ndsp.app/NDSP_Command_Center.html
[200] https://my.ndsp.app/NDSP_Daily_Brief.html
[200] https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] https://my.ndsp.app/disclaimer.html

## 2) Alias Pages HTTP
[200] https://my.ndsp.app/decision-center.html
[200] https://my.ndsp.app/asset-selector.html
[200] https://my.ndsp.app/decision-radar.html
[200] https://my.ndsp.app/daily-brief.html
[200] https://my.ndsp.app/settings.html

## 3) Auth Routes HTTP
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

## 4) API Health
[200] https://api.ndsp.app/api/health
BODY: {"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
[200] https://api.ndsp.app/health
BODY: {"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
[200] https://api.ndsp.app/api/status
BODY: {"ok": true, "service": "ndsp-platform-gateway-9002", "status": "LISTENING", "port": 9002, "updated_at": "2026-07-07T20:57:39Z"}

## 5) Decision API Required Fields
[200] https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT
[OK] ETHUSDT symbol=ETHUSDT
[OK] ETHUSDT live_price=1790.45
[OK] ETHUSDT decision_quality=86
[OK] ETHUSDT scenario_state=UNDER_MONITORING
[OK] ETHUSDT directional_context=قراءة أسبوعي · ضغط هابط
[OK] ETHUSDT nmp_status=AVAILABLE

[200] https://api.ndsp.app/api/decision/quality-live?symbol=BTCUSDT
[OK] BTCUSDT symbol=BTCUSDT
[OK] BTCUSDT live_price=63817.99
[OK] BTCUSDT decision_quality=86
[OK] BTCUSDT scenario_state=UNDER_MONITORING
[OK] BTCUSDT directional_context=قراءة أسبوعي · ضغط هابط
[OK] BTCUSDT nmp_status=AVAILABLE

[200] https://api.ndsp.app/api/decision/quality-live?symbol=XAUUSD
[OK] XAUUSD symbol=XAUUSD
[OK] XAUUSD live_price=4116.10009765625
[OK] XAUUSD decision_quality=60
[OK] XAUUSD scenario_state=UNDER_MONITORING
[OK] XAUUSD directional_context=قراءة أسبوعي · ضغط سفلي
[OK] XAUUSD nmp_status=UNAVAILABLE

[200] https://api.ndsp.app/api/decision/quality-live?symbol=USOIL
[OK] USOIL symbol=USOIL
[OK] USOIL live_price=72.26000213623047
[OK] USOIL decision_quality=55
[OK] USOIL scenario_state=UNDER_MONITORING
[OK] USOIL directional_context=قراءة أسبوعي · ضغط سفلي
[OK] USOIL nmp_status=UNAVAILABLE


## 6) Protected UI + Content Markers
radar=29
sidebar=22
disclaimer=27
NDSP_DECISION_SUPPORT_CONTENT_V1=2
NDSP_ASSET_VIEW_CONTENT_V1=2
NDSP_DAILY_BRIEF_CONTENT_V1=2
NDSP_COMMAND_CENTER_CONTENT_V1=2
NDSP_SETTINGS_ALERTS_CONTENT_V1=2
NDSP_AUTH_ROUTE_ALIAS_V1=4

## 7) Forbidden Public Wording Scan
FORBIDDEN_PUBLIC_WORDING_COUNT=0
[OK] No forbidden public wording found

## 8) Runtime
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11.3% | ram usage: 9.7% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.169mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.312mb/s / 81.98% |
[OK] ndsp-portal online

## 9) Final Evaluation
OFFICIAL_OK=1
ALIAS_OK=1
AUTH_OK=1
API_OK=1
DECISION_OK=1
MARKERS_OK=1
FORBIDDEN_PUBLIC_WORDING_COUNT=0
PM2_OK=1

FINAL_STATUS=FINAL_V1_RELEASE_READINESS_OK
RELEASE_RESULT=READY_WITH_GOVERNANCE_LOCK
REPORT=docs/05-runbooks/NDSP_FINAL_V1_RELEASE_READINESS_AUDIT_20260707_225738.md
