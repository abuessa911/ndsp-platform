
## 0. Safety contract

# NDSP — Commercial Staging Source Deployment V1

- Date: 2026-07-30T01:40:30+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Production auth service: ndsp-auth-core-clean.service
- Staging database: ndsp_auth_commercial_staging
- Staging service: ndsp-commercial-auth-payment-staging.service
- Staging root: /opt/ndsp-commercial-auth-payment-staging
- Nginx mutation: FORBIDDEN
- Frontend/design mutation: FORBIDDEN
- Production database mutation: FORBIDDEN
- External payment-provider traffic: BLOCKED
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_20260730_014030/REPORT.md
- **SAFETY_CONTRACT:** `PASS` — Explicit confirmation, protected production names, required tools and canonical paths validated.

## 1. Freeze proof for Nginx, design and production services

