# NDSP Public Gateway Readiness Registry

Generated: 20260628_181658  
Task: DEV-014  
Branch: feature/ndsp-os  
Head: 85bb51d ops(DEV-013): harden repo and systemd guardrails  

## Current Core Services

| ID | Name | Port | Gateway Status |
|---|---|---:|---|
| CTL-001 | Workspace Identity | 9081 | Internal only |
| CDS-001 | Completed Decision | 9078 | Partial read-only public |
| DGC-001 | Decision Governance Core | 9079 | Health public only |
| BOT-001 | Bot Execution | 9080 | Internal only |

## Approved Public Surfaces

- CDS-001 latest completed decision read endpoint
- DGC-001 health endpoint

## Not Approved For Public Exposure

- Bot execution endpoints
- Internal ingestion endpoints
- Internal governance submission endpoints
- Environment/configuration endpoints
- Admin-only routes
