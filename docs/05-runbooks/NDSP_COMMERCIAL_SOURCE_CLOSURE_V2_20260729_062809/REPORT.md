
## 0. Safety and discovery

# NDSP Commercial Source Closure V2
- Date: 2026-07-29T06:28:09+02:00
- Project: /home/nawaf511/empire-core-new
- Domain: https://my.ndsp.app
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_SOURCE_CLOSURE_V2_20260729_062809/REPORT.md
- **SAFETY_AND_SOURCE_DISCOVERY:** `PASS` — Nginx=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf; portal=/home/nawaf511/empire-core-new/frontend/user-portal-vite; active DB resolved without printing credentials.

## 1. Required business and provider inputs

- **COMMERCIAL_INPUTS:** `FAIL` — Missing/invalid: NDSP_PAID_PLAN_PRICES_JSON NDSP_STRIPE_PRICE_IDS_JSON NDSP_STRIPE_SECRET_KEY NDSP_STRIPE_WEBHOOK_SECRET NDSP_LEGAL_DOCUMENT_VERSION NDSP_LEGAL_DOCUMENT_SHA256 NDSP_LEGAL_APPROVAL_REFERENCE NDSP_SMTP_HOST NDSP_SMTP_PORT NDSP_SMTP_USER NDSP_SMTP_PASS NDSP_SMTP_FROM NDSP_TELEGRAM_BOT_TOKEN NDSP_TELEGRAM_TEST_CHAT_ID NDSP_ADMIN_EMAIL NDSP_ADMIN_PASSWORD VALID_LEGAL_SHA256 VALID_PLAN_JSON. See /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_SOURCE_CLOSURE_V2_20260729_062809/REQUIRED_INPUTS.env.example
- No mutation performed.
- FINAL_STATUS: `NDSP_COMMERCIAL_SOURCE_CLOSURE_V2_BLOCKED_INPUTS`
