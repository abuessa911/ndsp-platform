# NDSP Enterprise Laws

## Law 1 — Service Identity

Every service must have:

- Owner
- Version
- Contract
- Health endpoint
- Systemd service
- Documentation
- Architecture registration

## Law 2 — Gateway First

No service should be consumed directly by public clients.

Public access must pass through the official gateway.

## Law 3 — Engine Isolation

Only NDSP — Nawaf Decision Support Platform can access decision engines.

External products consume Completed Decision API only.

## Law 4 — Official Decision Flow

No official decision exists unless it passes:

Decision Engines
↓
Decision Governance Core
↓
Completed Decision Service
↓
Consumer

## Law 5 — Architecture Registration

No new service may be created unless registered first in Architecture Office.
