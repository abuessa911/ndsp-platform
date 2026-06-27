# NDSP API Contracts

## Future Completed Decision API

GET /api/completed
GET /api/completed/latest
GET /api/completed/:symbol
GET /api/completed/:id/timeline
GET /api/completed/:id/explain

## Future Copilot API

POST /api/copilot/chat
GET /api/copilot/explain/:decision_id
GET /api/copilot/timeline/:decision_id
GET /api/copilot/compare?left=BTCUSDT&right=XAUUSD

## Rule

Copilot must answer from Completed Decision Service only.
