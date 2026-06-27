# NDSP Product Registry

## PRD-001 — NDSP — Nawaf Decision Support Platform

Role: Decision Support Platform  
Responsibility: Produce, govern, store, and publish completed decisions.

Owns:

- Decision Engines
- Governance Core
- Completed Decision Service
- User Portal
- Admin Portal
- Platform API
- Alerts
- Packages
- Users

Does not execute trades.

---

## PRD-002 — NDSP Bot

Role: Execution Product  
Responsibility: Consume completed decisions and manage execution workflows.

Owns:

- Bot API Gateway
- Execution Engine
- Broker Manager
- Risk Manager
- Position Manager
- Portfolio Manager
- Trade Journal
- Monitoring

Does not analyze markets and does not access decision engines.

---

## PRD-003 — NDSP AI

Role: Explainability Product  
Responsibility: Explain completed decisions only.

Does not create decisions.

---

## PRD-004 — NDSP SDK

Role: Integration Product  
Responsibility: Provide official developer access to Completed Decision API.

Does not access engines.
