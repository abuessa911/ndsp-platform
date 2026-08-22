# NDSP Core Services Gateway Routes

## Approved Existing / Readiness Routes

```text
GET /api/completed/latest
  -> CDS-001 http://127.0.0.1:9078/api/completed/latest

GET /api/governance/health
  -> DGC-001 http://127.0.0.1:9079/health
```

## Internal Only

```text
CTL-001 127.0.0.1:9081
BOT-001 127.0.0.1:9080
```

## Governance

Do not expose bot execution endpoints publicly.
Do not expose write endpoints publicly unless a future signed internal gateway is created.
