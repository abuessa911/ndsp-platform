# CDS-001 — ENG-001 Adapter Contract

Generated: 20260628_062252

## Purpose

CDS-001 is migrated from LEGACY compatibility toward ENG-001 using a transitional Express adapter.

## Preserved Behavior

NO_BEHAVIOR_BREAK=YES
PRESERVE_PORT=9078
PRESERVE_EXISTING_EXPRESS_APP=YES
PRESERVE_COMPLETED_DECISION_ENDPOINTS=YES
PRESERVE_DATABASE_SCHEMA=YES

## ENG-001 Standard Endpoints

GET /health
GET /version
GET /about

## Existing CDS Endpoints

GET /api/completed
GET /api/completed/latest
GET /api/completed/:symbol
GET /api/completed/id/:decision_id
GET /api/completed/id/:decision_id/timeline
POST /api/completed/ingest
POST /api/completed/:decision_id/publish

## Governance

DECISION_SUPPORT_ONLY=YES
NOT_FINANCIAL_ADVICE=YES
NOT_BUY_SELL_RECOMMENDATION=YES
NOT_EXECUTION_INSTRUCTION=YES

## Migration Mode

FRAMEWORK=ENG-001
MIGRATION_MODE=transitional_express_adapter
USES_FRAMEWORK_FACTORY_REFERENCE=createNDSPService
