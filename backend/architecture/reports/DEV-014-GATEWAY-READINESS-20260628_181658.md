# DEV-014 — Service Promotion & Public Gateway Readiness

Generated: 20260628_181658  
Branch: feature/ndsp-os  
Head: 85bb51d ops(DEV-013): harden repo and systemd guardrails  

## Objective

Prepare NDSP core services for controlled public gateway promotion without applying live Nginx changes.

## Scope

This task creates contracts, registries, readiness tooling, and disabled Nginx examples only.

## Added

- backend/tools/ndsp/ndsp_gateway_readiness.sh
- backend/architecture/contracts/PUBLIC_GATEWAY_CONTRACT.md
- backend/architecture/registry/PUBLIC_GATEWAY_READINESS.md
- backend/gateway/README.md
- backend/gateway/routes/core-services.routes.md
- backend/gateway/nginx/disabled/api-ndsp-core-services-readiness.conf.example

## Public Exposure Decision

Allowed:
- GET /api/completed/latest
- GET /api/governance/health

Internal only:
- CTL-001
- BOT-001
- CDS-001 ingest/write
- DGC-001 submit/evaluate/write

## Result

Repo Guard: PASS  
Systemd Guard: PASS  
Gateway Readiness: PASS  

## Note

No production Nginx config was modified.
