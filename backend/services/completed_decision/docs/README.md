# NDSP Completed Decision Service

This service is the official source for completed NDSP decisions.

It does not calculate decisions.
It stores, validates, publishes, and serves official completed decisions.

## Port

127.0.0.1:9078

## Endpoints

- GET /health
- GET /api/completed
- GET /api/completed/latest
- GET /api/completed/:symbol
- GET /api/completed/id/:decision_id
- GET /api/completed/id/:decision_id/timeline
- POST /api/completed/ingest
- POST /api/completed/:decision_id/publish
