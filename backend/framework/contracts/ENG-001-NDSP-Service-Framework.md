# ENG-001 — NDSP Service Framework Contract

## Purpose

Provide a shared service bootstrap layer for all NDSP services.

## Public API provided to services

```js
const { createNDSPService } = require("../../framework");

const service = createNDSPService({
  serviceId: "CTL-001",
  serviceName: "Workspace Identity",
  product: "SYS-001",
  domain: "Operating System",
  version: "1.0.0"
});

service.start();
```

## Automatic endpoints

- GET /health
- GET /version
- GET /about

## Framework responsibilities

- Express bootstrap
- Security middleware
- JSON middleware
- Logger
- Health endpoint
- Version endpoint
- About endpoint
- Error handler
- Graceful shutdown
- Config loader
- Manifest loader

## Framework non-responsibilities

- No market logic
- No trading logic
- No decision logic
- No broker logic
- No business-specific behavior
