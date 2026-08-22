# NDSP V1 Functional Audit — Read Only
DATE=2026-07-07T22:01:25+02:00
MODE=READ_ONLY
MODIFICATIONS=None
LIVE=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) Official Pages HTTP
[200] https://my.ndsp.app/
[200] https://my.ndsp.app/index.html
[200] https://my.ndsp.app/decision-support.html
[200] https://my.ndsp.app/NDSP_Asset_View.html
[200] https://my.ndsp.app/NDSP_Command_Center.html
[200] https://my.ndsp.app/NDSP_Daily_Brief.html
[200] https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] https://my.ndsp.app/disclaimer.html

## 2) Known Alias Pages HTTP
[200] https://my.ndsp.app/decision-center.html
[200] https://my.ndsp.app/asset-selector.html
[200] https://my.ndsp.app/decision-radar.html
[200] https://my.ndsp.app/daily-brief.html
[200] https://my.ndsp.app/settings.html

## 3) Portal Entry / Auth Candidate Pages
[404] https://my.ndsp.app/login
[200] https://my.ndsp.app/login.html
[404] https://my.ndsp.app/register
[200] https://my.ndsp.app/register.html
[404] https://my.ndsp.app/forgot-password
[404] https://my.ndsp.app/reset-password

## 4) API Health Candidates
[200] https://api.ndsp.app/api/health
BODY: {"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
[200] https://api.ndsp.app/health
BODY: {"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
[200] https://api.ndsp.app/api/status
BODY: {"ok": true, "service": "ndsp-platform-gateway-9002", "status": "LISTENING", "port": 9002, "updated_at": "2026-07-07T20:01:26Z"}

## 5) Decision API Samples
[200] https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT
[OK] ETHUSDT symbol=ETHUSDT
[OK] ETHUSDT live_price=1790.45
[OK] ETHUSDT decision_quality=86
[OK] ETHUSDT scenario_state=UNDER_MONITORING
[OK] ETHUSDT directional_context=قراءة أسبوعي · ضغط هابط
[OK] ETHUSDT nmp_status=AVAILABLE
[OK] ETHUSDT nmp_level=1583.4

[200] https://api.ndsp.app/api/decision/quality-live?symbol=BTCUSDT
[OK] BTCUSDT symbol=BTCUSDT
[OK] BTCUSDT live_price=63817.99
[OK] BTCUSDT decision_quality=86
[OK] BTCUSDT scenario_state=UNDER_MONITORING
[OK] BTCUSDT directional_context=قراءة أسبوعي · ضغط هابط
[OK] BTCUSDT nmp_status=AVAILABLE
[OK] BTCUSDT nmp_level=61056.47

[200] https://api.ndsp.app/api/decision/quality-live?symbol=XAUUSD
[OK] XAUUSD symbol=XAUUSD
[OK] XAUUSD live_price=4122.60009765625
[OK] XAUUSD decision_quality=60
[OK] XAUUSD scenario_state=UNDER_MONITORING
[OK] XAUUSD directional_context=قراءة أسبوعي · ضغط سفلي
[OK] XAUUSD nmp_status=UNAVAILABLE
[MISS] XAUUSD nmp_level=None

[200] https://api.ndsp.app/api/decision/quality-live?symbol=USOIL
[OK] USOIL symbol=USOIL
[OK] USOIL live_price=71.91000366210938
[OK] USOIL decision_quality=55
[OK] USOIL scenario_state=UNDER_MONITORING
[OK] USOIL directional_context=قراءة أسبوعي · ضغط سفلي
[OK] USOIL nmp_status=UNAVAILABLE
[MISS] USOIL nmp_level=None


## 6) Protected UI Presence in Live Files
radar=29
sidebar=22
disclaimer=27
NDSP_DECISION_SUPPORT_CONTENT_V1=2
NDSP_ASSET_VIEW_CONTENT_V1=2
NDSP_DAILY_BRIEF_CONTENT_V1=2
NDSP_COMMAND_CENTER_CONTENT_V1=2
NDSP_SETTINGS_ALERTS_CONTENT_V1=2

## 7) Forbidden Public Wording Scan

## 7B) Forbidden Public Wording Scan — Completion
FORBIDDEN_PUBLIC_WORDING_COUNT=0
[OK] No forbidden public wording found

## 8) Runtime Check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11% | ram usage: 9.5% | lo: ⇓ 0.007mb/s ⇑ 0.007mb/s | eth0: ⇓ 0.132mb/s ⇑ 0.004mb/s | disk: ⇓ 0mb/s ⇑ 0.158mb/s / 81.97% |

## 9) Audit Summary
- Official pages: checked in previous sections
- Alias pages: checked in previous sections
- API health: checked in previous sections
- Decision API samples: checked in previous sections
- Protected UI markers: checked in previous sections
- Forbidden wording: 0
- Runtime: checked

FINAL_STATUS=V1_FUNCTIONAL_AUDIT_READONLY_DONE
AUDIT_RESULT=OK_WITH_NOTES
REPORT=docs/05-runbooks/NDSP_V1_FUNCTIONAL_AUDIT_READONLY_20260707_220125.md
