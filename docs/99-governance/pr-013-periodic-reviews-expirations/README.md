# PR-013 Governance Periodic Reviews and Expirations

PR-013 establishes the canonical process for scheduling, completing,
escalating, and closing periodic governance reviews.

## Scope

- Governance documentation only.
- No runtime, application, deployment, service, or configuration changes.
- Existing PR-004 through PR-012 artifacts are validated but not modified.

## Initial register state

| State | Count |
|---|---:|
| Tracked packages | 9 |
| Completed reviews | 0 |
| Scheduled reviews | 0 |
| Overdue reviews | 0 |
| Expired artifacts | 0 |
| Pending owner assignments | 9 |

## Default review frequencies

| Artifact category | Frequency |
|---|---|
| Network exposure | Monthly |
| Governance index | Monthly |
| Exceptions and approvals | Monthly |
| Dependencies and ownership | Quarterly |
| Integrity audit | Quarterly |
| Update policy | Annual |
| Closure and historical manifests | Annual |

## Review controls

- Every tracked artifact requires a named review owner.
- Every review requires a defined scope and evidence.
- Next review dates must respect the configured frequency.
- Overdue reviews require escalation.
- Expired artifacts must not be treated as current evidence.
- Material findings require governed remediation.
- Frequency exceptions must be recorded through PR-012.
- Runtime changes remain outside governance-only review PRs.

## Existing governance baseline

- Source commit: `ac64bee821e694c3b2200cdd4b8f337c323ad43e`
- Required prior packages: 9
- Missing packages: 0
- Invalid primary JSON artifacts: 0

## Artifacts

- `GOVERNANCE_PERIODIC_REVIEWS_REGISTER.json`
- `PERIODIC_REVIEW_TEMPLATE.md`
- `PR013_SHA256SUMS.txt`

## Final declaration

- Tracked governance packages: 9
- Completed reviews: 0
- Overdue reviews: 0
- Runtime changes: none
- Validation: PASS
- Status: ACTIVE
