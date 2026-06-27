# ENG-001 — NDSP Service Framework

This is the internal service framework for NDSP Ecosystem.

It is the engineering foundation for future NDSP services.

## Status

Minimum Viable Framework (MVF)

## Provides

- createNDSPService()
- /health
- /version
- /about
- Logger
- Config loader
- Manifest loader
- Error handler
- Graceful shutdown

## Rule

New services must not bootstrap Express directly.

Use:

```js
const { createNDSPService } = require("../../framework");
```

## Ownership

- Component: ENG-001
- Product: SYS-001 NDSP Operating System
- Domain: Engineering Core
- Owner: NDSP Engineering
