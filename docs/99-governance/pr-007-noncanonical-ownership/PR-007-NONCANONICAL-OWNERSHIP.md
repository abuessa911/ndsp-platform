# PR-007 Final Non-Canonical Ownership Resolution

## Final status

`FINALIZED`

- Total records: `42`
- Manual decisions applied: `12`
- Unresolved records: `0`
- Manual review required: `0`
- Runtime changes: `none`

## Governance conclusion

All non-canonical listener records inherited from PR-006 now have an explicit governance ownership decision.

These decisions classify observed runtime components for documentation and ownership planning only. Promotion, deprecation, retirement, or shared-infrastructure classification does not itself perform any runtime or deployment action.

## Decision counts

- `DEPRECATED`: `1`
- `PROMOTE_TO_CANONICAL`: `20`
- `SHARED_INFRASTRUCTURE`: `21`

## Owner counts

- `NDSP platform`: `16`
- `nawaf511`: `26`

## Promote to canonical

| ID | Component | Port | Unit | Owner | Decision | Confidence |
|---|---|---:|---|---|---|---|
| `PR007-002` | `ndsp-news-ticker` | `8097` | `ndsp-news-ticker.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-010` | `ndsp-access-guard-9024` | `9024` | `ndsp-access-guard-9024.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-013` | `ndsp-access-guard-final` | `9030` | `ndsp-access-guard-final.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-014` | `ndsp-admin-users-official` | `9031` | `ndsp-admin-users-official.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-015` | `ndsp-live-market-adapter` | `9033` | `ndsp-live-market-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-016` | `ndsp-scenario-levels-adapter` | `9034` | `ndsp-scenario-levels-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-017` | `ndsp-governance-bridge` | `9044` | `ndsp-governance-bridge.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-018` | `ndsp-portal-real-data-api` | `9047` | `ndsp-portal-real-data-api.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-019` | `ndsp-decision-package-v1` | `9061` | `ndsp-decision-package-v1.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-020` | `ndsp-layers-api` | `9065` | `ndsp-layers-api.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-023` | `ndsp-admin-user-ops` | `9068` | `ndsp-admin-user-ops.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-026` | `ndsp-current-user-display` | `9074` | `ndsp-current-user-display.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-028` | `ndsp-16-layers` | `9077` | `ndsp-16-layers.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-031` | `ndsp-v52-contract` | `9083` | `ndsp-v52-contract.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-033` | `ndsp-canonical-live-runtime-v30` | `9085` | `ndsp-canonical-live-runtime-v30.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-034` | `ndsp-canonical-live-runtime-v33` | `9086` | `ndsp-canonical-live-runtime-v33.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-035` | `ndsp-completed-decisions-evidence-v35` | `9087` | `ndsp-completed-decisions-evidence-v35.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-036` | `ndsp-completed-decisions-history-v36` | `9088` | `ndsp-completed-decisions-history-v36.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-038` | `ndsp-public-summary-v548` | `9092` | `ndsp-public-summary-v548.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-040` | `ndsp-business-ops` | `9094` | `ndsp-business-ops.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |

## Shared infrastructure

| ID | Component | Port | Unit | Owner | Decision | Confidence |
|---|---|---:|---|---|---|---|
| `PR007-001` | `pm2-nawaf511` | `3000` | `pm2-nawaf511.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-003` | `ndsp-platform-gateway` | `9001` | `ndsp-platform-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-004` | `ndsp-platform-gateway-9002` | `9002` | `ndsp-platform-gateway-9002.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-005` | `ndsp-admin-actions` | `9017` | `ndsp-admin-actions.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-006` | `ndsp-trial-register` | `9019` | `ndsp-trial-register.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-007` | `ndsp-user-dashboard` | `9021` | `ndsp-user-dashboard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-008` | `ndsp-api-compat` | `9022` | `ndsp-api-compat.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-009` | `ndsp-admin-ui-proxy` | `9023` | `ndsp-admin-ui-proxy.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-011` | `ndsp-register-compat-gateway` | `9028` | `ndsp-register-compat-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-012` | `ndsp-registration-consent-v42` | `9029` | `ndsp-registration-consent-v42.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-021` | `ndsp-ui-bridge-api` | `9066` | `ndsp-ui-bridge-api.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-024` | `ndsp-change-password-gateway` | `9069` | `ndsp-change-password-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-025` | `ndsp-trial-fingerprint-guard` | `9070` | `ndsp-trial-fingerprint-guard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-027` | `ndsp-raw-cot-gateway` | `9076` | `ndsp-raw-cot-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-029` | `ndsp-ctl-001-workspace-identity` | `9081` | `ndsp-ctl-001-workspace-identity.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-030` | `ndsp-quality-live-nmp-wrapper` | `9082` | `ndsp-quality-live-nmp-wrapper.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-032` | `ndsp-v53-bridge` | `9084` | `ndsp-v53-bridge.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-037` | `pm2-nawaf511` | `9091` | `pm2-nawaf511.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-039` | `ndsp-v3-portal-gateway` | `9093` | `ndsp-v3-portal-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-041` | `ndsp-market-data-bridge-v2` | `9095` | `ndsp-market-data-bridge-v2.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-042` | `ndsp-auth-core-clean` | `19091` | `ndsp-auth-core-clean.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |

## Deprecated

| ID | Component | Port | Unit | Owner | Decision | Confidence |
|---|---|---:|---|---|---|---|
| `PR007-022` | `ndsp-quality-live-golden-wrapper` | `9067` | `ndsp-quality-live-golden-wrapper.service` | `nawaf511` | `DEPRECATED` | `MEDIUM` |

## Source only

No records.

## Retired

No records.

## Complete ownership map

| ID | Component | Port | Unit | Owner | Decision | Confidence |
|---|---|---:|---|---|---|---|
| `PR007-001` | `pm2-nawaf511` | `3000` | `pm2-nawaf511.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-002` | `ndsp-news-ticker` | `8097` | `ndsp-news-ticker.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-003` | `ndsp-platform-gateway` | `9001` | `ndsp-platform-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-004` | `ndsp-platform-gateway-9002` | `9002` | `ndsp-platform-gateway-9002.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-005` | `ndsp-admin-actions` | `9017` | `ndsp-admin-actions.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-006` | `ndsp-trial-register` | `9019` | `ndsp-trial-register.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-007` | `ndsp-user-dashboard` | `9021` | `ndsp-user-dashboard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-008` | `ndsp-api-compat` | `9022` | `ndsp-api-compat.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-009` | `ndsp-admin-ui-proxy` | `9023` | `ndsp-admin-ui-proxy.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-010` | `ndsp-access-guard-9024` | `9024` | `ndsp-access-guard-9024.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-011` | `ndsp-register-compat-gateway` | `9028` | `ndsp-register-compat-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-012` | `ndsp-registration-consent-v42` | `9029` | `ndsp-registration-consent-v42.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-013` | `ndsp-access-guard-final` | `9030` | `ndsp-access-guard-final.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-014` | `ndsp-admin-users-official` | `9031` | `ndsp-admin-users-official.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-015` | `ndsp-live-market-adapter` | `9033` | `ndsp-live-market-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-016` | `ndsp-scenario-levels-adapter` | `9034` | `ndsp-scenario-levels-adapter.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-017` | `ndsp-governance-bridge` | `9044` | `ndsp-governance-bridge.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-018` | `ndsp-portal-real-data-api` | `9047` | `ndsp-portal-real-data-api.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-019` | `ndsp-decision-package-v1` | `9061` | `ndsp-decision-package-v1.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-020` | `ndsp-layers-api` | `9065` | `ndsp-layers-api.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-021` | `ndsp-ui-bridge-api` | `9066` | `ndsp-ui-bridge-api.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-022` | `ndsp-quality-live-golden-wrapper` | `9067` | `ndsp-quality-live-golden-wrapper.service` | `nawaf511` | `DEPRECATED` | `MEDIUM` |
| `PR007-023` | `ndsp-admin-user-ops` | `9068` | `ndsp-admin-user-ops.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-024` | `ndsp-change-password-gateway` | `9069` | `ndsp-change-password-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-025` | `ndsp-trial-fingerprint-guard` | `9070` | `ndsp-trial-fingerprint-guard.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-026` | `ndsp-current-user-display` | `9074` | `ndsp-current-user-display.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-027` | `ndsp-raw-cot-gateway` | `9076` | `ndsp-raw-cot-gateway.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-028` | `ndsp-16-layers` | `9077` | `ndsp-16-layers.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-029` | `ndsp-ctl-001-workspace-identity` | `9081` | `ndsp-ctl-001-workspace-identity.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-030` | `ndsp-quality-live-nmp-wrapper` | `9082` | `ndsp-quality-live-nmp-wrapper.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-031` | `ndsp-v52-contract` | `9083` | `ndsp-v52-contract.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-032` | `ndsp-v53-bridge` | `9084` | `ndsp-v53-bridge.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-033` | `ndsp-canonical-live-runtime-v30` | `9085` | `ndsp-canonical-live-runtime-v30.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-034` | `ndsp-canonical-live-runtime-v33` | `9086` | `ndsp-canonical-live-runtime-v33.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-035` | `ndsp-completed-decisions-evidence-v35` | `9087` | `ndsp-completed-decisions-evidence-v35.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-036` | `ndsp-completed-decisions-history-v36` | `9088` | `ndsp-completed-decisions-history-v36.service` | `nawaf511` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-037` | `pm2-nawaf511` | `9091` | `pm2-nawaf511.service` | `nawaf511` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-038` | `ndsp-public-summary-v548` | `9092` | `ndsp-public-summary-v548.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `MEDIUM` |
| `PR007-039` | `ndsp-v3-portal-gateway` | `9093` | `ndsp-v3-portal-gateway.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |
| `PR007-040` | `ndsp-business-ops` | `9094` | `ndsp-business-ops.service` | `NDSP platform` | `PROMOTE_TO_CANONICAL` | `GOVERNANCE_APPROVED` |
| `PR007-041` | `ndsp-market-data-bridge-v2` | `9095` | `ndsp-market-data-bridge-v2.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `GOVERNANCE_APPROVED` |
| `PR007-042` | `ndsp-auth-core-clean` | `19091` | `ndsp-auth-core-clean.service` | `NDSP platform` | `SHARED_INFRASTRUCTURE` | `MEDIUM` |

## Governance boundary

No services were started, stopped, restarted, enabled, disabled, or reconfigured.

No application source, firewall, Nginx configuration, container, routing, database, or deployment state was changed.
