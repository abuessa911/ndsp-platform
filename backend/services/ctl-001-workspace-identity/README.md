# CTL-001 — Workspace Identity

First production service built on ENG-001 NDSP Service Framework.

## Product

SYS-001 — NDSP Operating System

## Domain

Operating System

## Endpoints

- GET /health
- GET /version
- GET /about
- GET /identity

## Internal Port

127.0.0.1:9081

## Systemd

ndsp-ctl-001-workspace-identity.service

## Rule

This service must not import Express directly. It must use ENG-001:

```js
const { createNDSPService } = require("../../framework");
```
