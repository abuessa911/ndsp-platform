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

## 20260627_232733

TSK-2.1B created CTL-001 Workspace Identity.

Added:
- services/ctl-001-workspace-identity
- /identity endpoint
- systemd service ndsp-ctl-001-workspace-identity.service
- CTL-001 API contract
- CTL-001 service registry entry

## 20260627_235837

DEV-001 created NDSP Developer Toolkit.

Added:
- backend/sdk/devtoolkit
- backend/tools/ndsp
- backend/templates/service
- ndsp create service
- ndsp validate
- ndsp doctor
- ndsp registry

## 20260628_000901

DEV-002 introduced repository hygiene.

Added:
- .gitignore policy
- ADR-0005 repository hygiene
- DEV-002 repository hygiene contract

Rule:
- Do not use git add .
- Add only intentional paths.

## 20260628_175219 — DEV-013Z Fix Guard And Close

Fixed:
- Repo Guard false positives for .env.example files
- Repo Guard false positive for backend/app/runtime source files

Closed:
- DEV-013 Enterprise Hardening

## 20260628_181658 — DEV-014 Gateway Readiness

Added:
- Public gateway contract
- Public gateway readiness registry
- Gateway readiness tool
- Gateway route documentation
- Disabled Nginx example

No live Nginx route was installed.

## 20260628_193248 — DEV-015 Public Gateway Controlled Activation

Closed:
- Public read-only gateway activation
- Unified TLS verification
- BOT-001 and CTL-001 remain internal only

## 20260629_032831 — DEV-015 Public Gateway Controlled Activation

Closed:
- Public read-only gateway activation
- Unified TLS verification
- BOT-001 and CTL-001 remain internal only

## 20260629_035520 — DEV-016 Release Candidate Freeze

Closed:
- RC1 freeze
- Final Git/service/gateway/TLS/API checks
- Release candidate registry
- Release candidate freeze policy
