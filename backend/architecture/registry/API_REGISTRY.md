# NDSP API Registry

## Completed Decision API

Owner: NDSP — Nawaf Decision Support Platform  
Service: Completed Decision Service  
Internal Port: 9078

Public safe routes:

- GET /api/completed
- GET /api/completed/latest
- GET /api/completed/:symbol
- GET /api/completed/id/:decision_id
- GET /api/completed/id/:decision_id/timeline

Blocked public write routes:

- POST /api/completed/ingest
- POST /api/completed/:decision_id/publish

---

## Governance API

Owner: NDSP — Nawaf Decision Support Platform  
Service: Decision Governance Core  
Internal Port: 9079

Public safe routes:

- GET /api/governance/health
- POST /api/governance/evaluate

Internal-only routes:

- POST /api/governance/submit

---

## Bot API

Owner: NDSP Bot  
Service: Bot Execution Engine  
Internal Port: 9080

Current mode:

- DRY_RUN only
- No real broker execution

Routes:

- GET /health
- GET /api/bot/latest
- GET /api/bot/:symbol
- POST /api/bot/simulate
