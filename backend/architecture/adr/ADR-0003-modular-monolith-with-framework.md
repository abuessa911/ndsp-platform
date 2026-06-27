# ADR-0003 — Modular Monolith with Microservice Boundaries and ENG-001 Framework

## Status

Accepted

## Decision

NDSP will use a Modular Monolith with clear service and domain boundaries during Release 1.x.

All new services must use ENG-001 NDSP Service Framework.

## Reason

This keeps development simpler now while preserving the ability to extract domains into microservices later.

## Consequences

- Services share a common framework.
- Express bootstrapping is centralized.
- Health/version/about endpoints are standardized.
- Future services follow the same lifecycle.
