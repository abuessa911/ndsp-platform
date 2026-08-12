# NDSP Current Reality Lock — قالب تثبيت الواقع الحالي

> لا تعبئ هذا الملف بالتخمين. القيم تؤخذ من Audit أو السيرفر مباشرة.

## Frontend
FRONTEND_DIR=
FRONTEND_BASE=
LIVE_FRONTEND_DIR=

## Backend
BACKEND_DIR=
API_BASE=

## Nginx / Services
NGINX_SITE_FILE=
SYSTEMD_SERVICES=
PM2_SERVICES=

## Database
DATABASE_TYPE=
DATABASE_NAME=

## Domains
DOMAIN_FRONTEND=
DOMAIN_API=
SSL_STATUS=

## Decision API
DECISION_API_ENDPOINT=/api/decision/quality-live?symbol=ETHUSDT
DECISION_API_FIELDS=
- symbol
- live_price
- decision_quality
- scenario_state
- directional_context
- market_state
- reading_horizon
- horizon_strength
- caution_reason
- sanitized_summary

## Protected UI Elements
- Sidebar
- Radar
- Disclaimer
- Official page links

## Forbidden Output
- Buy Now
- Sell Now
- اشتر الآن
- بيع الآن
- ادخل صفقة
- ربح مضمون
