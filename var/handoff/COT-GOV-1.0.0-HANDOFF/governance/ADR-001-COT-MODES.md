# ADR-001 — Separation of investment and speculation modes

## Decision

Investment and speculation modes are separate engines.

Investment:

- Positions determine total direction.
- Asset Manager Changes determine weekly support only.
- Timing is disabled.

Speculation:

- Changes determine direction.
- Day control is enabled.
- TDL timing is allowed.

## Consequence

Any code path that invokes speculation timing from investment mode is non-compliant.
