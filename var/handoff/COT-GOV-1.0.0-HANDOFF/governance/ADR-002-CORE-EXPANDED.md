# ADR-002 — CORE and EXPANDED isolation

## Decision

CORE is official and public.

EXPANDED is shadow-only and internal.

## Requirements

- Separate result objects.
- Separate storage or enforceable write permissions.
- No automatic promotion.
- No public API exposure.
- EXPANDED failure must not interrupt CORE.
