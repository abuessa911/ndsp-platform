# NDSP Architecture Changelog

## 20260627_214146

Created NDSP Architecture Office v2.0.

Added:
- SYSTEM_ARCHITECTURE.md
- ENGINE_CATALOG.md
- GOVERNANCE_RULES.md
- SERVICE_REGISTRY.md
- APPLICATION_REGISTRY.md
- DATA_FLOW.md
- API_CONTRACTS.md
- DECISION_LIFECYCLE.md
- SECURITY_MODEL.md
- DEPLOYMENT_ARCHITECTURE.md

## 20260627_214934

Exposed safe public API routes through api.ndsp.app:

- GET /api/completed
- GET /api/completed/latest
- GET /api/completed/:symbol
- GET /api/completed/id/:decision_id
- GET /api/completed/id/:decision_id/timeline
- GET /api/governance/health
- POST /api/governance/evaluate

Blocked public write routes:

- POST /api/completed/ingest
- POST /api/completed/:decision_id/publish
- POST /api/governance/submit

## 20260627_220028

Created separate NDSP Bot Execution Service.

Product separation:
- NDSP — Nawaf Decision Support Platform produces Completed Decisions.
- NDSP Bot consumes Completed Decisions for execution workflows only.

Service:
- ndsp-bot-execution.service
- Internal port: 127.0.0.1:9080
- Mode: DRY_RUN

## 20260627_221734

Added Enterprise Architecture Registry:

- laws/ENTERPRISE_LAWS.md
- registry/PRODUCT_REGISTRY.md
- registry/SERVICE_REGISTRY_V2.md
- registry/API_REGISTRY.md
- contracts/COMPLETED_DECISION_CONTRACT.md
- adr/ADR-0001-product-separation.md
- adr/ADR-0002-completed-decision-ssot.md

Formalized:
- NDSP — Nawaf Decision Support Platform as decision owner.
- NDSP Bot as separate execution product.
- Completed Decision API as the only bridge.

## 20260627_231621

TSK-2.1A completed initial build for ENG-001 NDSP Service Framework MVF.

Added:
- backend/framework
- createNDSPService()
- shared health/version/about endpoints
- logger/config/error/lifecycle modules
- framework tests
- ADR-0003
- ENG-001 service registry entry
