# PR-007 Non-Canonical Ownership Resolution

## Status

`COMPLETE_WITH_MANUAL_REVIEW`

- Records: `42`
- Manual review records: `12`
- Runtime changes: `none`

## Decision counts

- `DEPRECATED`: `1`
- `PROMOTE_TO_CANONICAL`: `13`
- `REVIEW_REQUIRED`: `12`
- `SHARED_INFRASTRUCTURE`: `16`

## Ownership map

| ID | Component | Port | Process | Unit | Owner | Decision | Confidence | Review |
|---|---|---:|---|---|---|---|---|---|
| `PR007-001` | `pm2-nawaf511` | `3000` | `node` | `pm2-nawaf511.service` | `nawaf511` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-002` | `ndsp-news-ticker` | `8097` | `node` | `ndsp-news-ticker.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-003` | `ndsp-platform-gateway` | `9001` | `node` | `ndsp-platform-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-004` | `ndsp-platform-gateway-9002` | `9002` | `python3` | `ndsp-platform-gateway-9002.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-005` | `ndsp-admin-actions` | `9017` | `node` | `ndsp-admin-actions.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-006` | `ndsp-trial-register` | `9019` | `node` | `ndsp-trial-register.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-007` | `ndsp-user-dashboard` | `9021` | `node` | `ndsp-user-dashboard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-008` | `ndsp-api-compat` | `9022` | `node` | `ndsp-api-compat.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-009` | `ndsp-admin-ui-proxy` | `9023` | `node` | `ndsp-admin-ui-proxy.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-010` | `ndsp-access-guard-9024` | `9024` | `node` | `ndsp-access-guard-9024.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-011` | `ndsp-register-compat-gateway` | `9028` | `node` | `ndsp-register-compat-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-012` | `ndsp-registration-consent-v42` | `9029` | `node` | `ndsp-registration-consent-v42.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-013` | `ndsp-access-guard-final` | `9030` | `node` | `ndsp-access-guard-final.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-014` | `ndsp-admin-users-official` | `9031` | `node` | `ndsp-admin-users-official.service` | `nawaf511` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-015` | `ndsp-live-market-adapter` | `9033` | `node` | `ndsp-live-market-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-016` | `ndsp-scenario-levels-adapter` | `9034` | `node` | `ndsp-scenario-levels-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-017` | `ndsp-governance-bridge` | `9044` | `node` | `ndsp-governance-bridge.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-018` | `ndsp-portal-real-data-api` | `9047` | `python3` | `ndsp-portal-real-data-api.service` | `nawaf511` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-019` | `ndsp-decision-package-v1` | `9061` | `uvicorn` | `ndsp-decision-package-v1.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-020` | `ndsp-layers-api` | `9065` | `uvicorn` | `ndsp-layers-api.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-021` | `ndsp-ui-bridge-api` | `9066` | `python3` | `ndsp-ui-bridge-api.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-022` | `ndsp-quality-live-golden-wrapper` | `9067` | `python3` | `ndsp-quality-live-golden-wrapper.service` | `nawaf511` | `DEPRECATED` | `MEDIUM` | `RESOLVED` |
| `PR007-023` | `ndsp-admin-user-ops` | `9068` | `python3` | `ndsp-admin-user-ops.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-024` | `ndsp-change-password-gateway` | `9069` | `uvicorn` | `ndsp-change-password-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-025` | `ndsp-trial-fingerprint-guard` | `9070` | `node` | `ndsp-trial-fingerprint-guard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-026` | `ndsp-current-user-display` | `9074` | `uvicorn` | `ndsp-current-user-display.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-027` | `ndsp-raw-cot-gateway` | `9076` | `uvicorn` | `ndsp-raw-cot-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-028` | `ndsp-16-layers` | `9077` | `node` | `ndsp-16-layers.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-029` | `ndsp-ctl-001-workspace-identity` | `9081` | `node` | `ndsp-ctl-001-workspace-identity.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-030` | `ndsp-quality-live-nmp-wrapper` | `9082` | `python3` | `ndsp-quality-live-nmp-wrapper.service` | `nawaf511` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-031` | `ndsp-v52-contract` | `9083` | `python3` | `ndsp-v52-contract.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-032` | `ndsp-v53-bridge` | `9084` | `python3` | `ndsp-v53-bridge.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-033` | `ndsp-canonical-live-runtime-v30` | `9085` | `python3` | `ndsp-canonical-live-runtime-v30.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-034` | `ndsp-canonical-live-runtime-v33` | `9086` | `python3` | `ndsp-canonical-live-runtime-v33.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-035` | `ndsp-completed-decisions-evidence-v35` | `9087` | `python3` | `ndsp-completed-decisions-evidence-v35.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-036` | `ndsp-completed-decisions-history-v36` | `9088` | `python3` | `ndsp-completed-decisions-history-v36.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-037` | `pm2-nawaf511` | `9091` | `python3` | `pm2-nawaf511.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-038` | `ndsp-public-summary-v548` | `9092` | `python3` | `ndsp-public-summary-v548.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` | `RESOLVED` |
| `PR007-039` | `ndsp-v3-portal-gateway` | `9093` | `python3` | `ndsp-v3-portal-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |
| `PR007-040` | `ndsp-business-ops` | `9094` | `python3` | `ndsp-business-ops.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-041` | `ndsp-market-data-bridge-v2` | `9095` | `python3` | `ndsp-market-data-bridge-v2.service` | `NDSP platform` | `REVIEW_REQUIRED` | `LOW` | `MANUAL_REVIEW_REQUIRED` |
| `PR007-042` | `ndsp-auth-core-clean` | `19091` | `nsolid` | `ndsp-auth-core-clean.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` | `RESOLVED` |

## Governance boundary

The classifications in this document are governance proposals derived from read-only runtime evidence.

No service lifecycle action, configuration change, source-code change, firewall change, routing change, or deployment action was performed.
