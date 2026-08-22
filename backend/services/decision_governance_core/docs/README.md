# NDSP Decision Governance Core

This service is the official bridge between NDSP decision engines and Completed Decision Service.

It validates engine output, assigns decision state, and forwards only Completed/Published decisions.

## Port

127.0.0.1:9079

## Endpoints

- GET /health
- POST /api/governance/evaluate
- POST /api/governance/submit

## Rule

Decision engines must not write directly to Completed Decision Service.
