# NDSP — Commercial Go-Live Readiness Audit V1

- Date: 2026-07-28T14:47:41+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Web root: /var/www/ndsp-my
- Domain: https://my.ndsp.app
- Mode: READ_ONLY

## 0. Preconditions

- **AUDIT_PRECONDITIONS:** `PASS` — Project and web root exist.

## 1. Governance and release architecture

- **DESIGN_FREEZE:** `PASS` — /home/nawaf511/empire-core-new/docs/00-governance/NDSP_FINAL_FRONTEND_GOVERNANCE_LOCK_V1/NDSP_FINAL_FRONTEND_GOVERNANCE_LOCK_V1.md
- **FINAL_RELEASE_ARCHITECTURE:** `PASS` — /portal-next/ HTTP=200
- **SOURCE_MAPS_DISABLED:** `PASS` — No source maps found.

## 2. Public routes

- **PAGE_COMPLETENESS_PUBLIC_ROUTES:** `PASS` — https://ndsp.app/=200;https://my.ndsp.app/login/=200;https://my.ndsp.app/register/=200;https://my.ndsp.app/forgot-password/=200;https://my.ndsp.app/reset-password/=200;https://my.ndsp.app/portal-next/=200;https://my.ndsp.app/support/=200;https://my.ndsp.app/subscribe/=200;

## 3. Trial and legal entry

- **TRIAL_16_DAYS:** `PASS` — duration_days=16
- **POST_TRIAL_TO_FREE:** `FAIL` — Automatic transition to Free not proven.
- **LEGAL_TRIAL_ACKNOWLEDGMENT:** `FAIL` — Legal/trial acknowledgment contract not proven.

## 4. Packages, payment and subscriptions

- **PACKAGES_PRICING_LIMITS:** `FAIL` — HTTP=200 paid=2 priced=0 limits=2 pricing_pending=False
- **PAYMENT_AND_BILLING:** `FAIL` — No proven production payment provider/billing lifecycle.
- **SUBSCRIPTION_API:** `FAIL` — Durable subscription API not found.

## 5. Decision core and live market data

- **DECISION_CORE_16_LAYERS_28_CAPABILITIES:** `PASS` — 16 layers, 28 capabilities, price and scenario returned.
- **LIVE_PRICE_AND_CHART_DATA:** `PASS` — /api/market/candles=200/2177;
- **COMPLETED_DECISIONS:** `FAIL` — HTTP=401 bytes=188

## 6. Portfolio, alerts and communications

- **PORTFOLIO:** `FAIL` — Persistent Portfolio/Watchlist CRUD not found.
- **ALERTS:** `FAIL` — source=NO SMTP=YES Telegram=YES
- **SUPPORT_OPERATIONS:** `WARN` — Support page live; ticket delivery and SLA drill not proven.

## 7. Localization and secrecy

- **AR_EN_LOCALIZATION:** `FAIL` — Arabic=NO English=NO
- **BEGINNER_PRO_MODE:** `FAIL` — Beginner/Professional mode not found.
- **INTERNAL_LAYER_SECRECY:** `FAIL` — Internal identifiers found in public files.

## 8. Security and hygiene

- **SECURITY_HEADERS:** `FAIL` — Missing: HSTS nosniff Referrer-Policy CSP 
- **PUBLIC_ARTIFACT_HYGIENE:** `PASS` — No obvious sensitive artifacts found.
- **NGINX_CONFIGURATION:** `PASS` — nginx -t passed.

## 9. Build, tests, accessibility and visual approval

