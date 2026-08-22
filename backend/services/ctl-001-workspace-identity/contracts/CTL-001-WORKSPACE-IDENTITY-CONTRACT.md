# CTL-001 — Workspace Identity API Contract

## Purpose

CTL-001 identifies the NDSP Workspace and proves that NDSP-OS services can be built on top of ENG-001.

## Endpoints

- GET /health
- GET /version
- GET /about
- GET /identity

## Identity Response

```json
{
  "ok": true,
  "service": "CTL-001",
  "service_name": "Workspace Identity",
  "product": "SYS-001",
  "workspace": "NDSP",
  "ecosystem": "NDSP Ecosystem",
  "operating_system": "NDSP-OS",
  "release": "REL-1.1",
  "framework": "ENG-001",
  "status": "ACTIVE"
}
```

## Non-responsibilities

- No decision logic
- No trading logic
- No market logic
- No registry/discovery logic yet
