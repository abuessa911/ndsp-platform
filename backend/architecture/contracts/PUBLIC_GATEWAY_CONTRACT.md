# NDSP Public Gateway Contract

## Purpose

This contract defines which internal NDSP services may be promoted through the public API gateway.

## Rule

Public gateway exposure must be explicit, read-only by default, and must not expose execution, secrets, internal ingestion, owner-only operations, or admin-only operations.

## Public Allowed Routes

| Public Route | Internal Service | Internal Target | Method | Exposure |
|---|---|---|---|---|
| /api/completed/latest | CDS-001 | http://127.0.0.1:9078/api/completed/latest | GET | Public read-only |
| /api/governance/health | DGC-001 | http://127.0.0.1:9079/health | GET | Public health |

## Internal Only

| Service | Reason |
|---|---|
| CTL-001 Workspace Identity | Internal platform identity |
| BOT-001 Execution Service | Execution layer must never be public |
| CDS-001 ingest routes | Internal write path only |
| DGC-001 submit/evaluate routes | Internal governance path only |

## Blocked By Default

- POST /api/completed/ingest
- POST /api/governance/submit
- POST /api/governance/evaluate
- Any BOT-001 execution endpoint
- Any route that requires admin key
- Any route that returns secrets or environment configuration

## Promotion Process

1. Add route to gateway contract.
2. Add route to gateway readiness report.
3. Test local service health.
4. Test Nginx syntax.
5. Apply Nginx route only in a separate controlled task.
6. Verify public endpoint.
7. Commit and tag.
