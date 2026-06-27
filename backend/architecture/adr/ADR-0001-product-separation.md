# ADR-0001 — Product Separation

## Decision

NDSP consists of separate products:

1. NDSP — Nawaf Decision Support Platform
2. NDSP Bot
3. NDSP AI
4. NDSP SDK
5. NDSP Mobile

## Reason

The platform produces governed completed decisions.

The bot consumes completed decisions for execution workflows only.

## Consequence

NDSP Bot cannot access decision engines.

NDSP Bot cannot create, modify, or override official decisions.

The only official bridge is Completed Decision API.
