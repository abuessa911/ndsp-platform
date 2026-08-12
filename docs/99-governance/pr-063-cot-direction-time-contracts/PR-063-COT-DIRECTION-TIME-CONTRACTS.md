# PR-063 — COT Direction and Time Contracts

## Approved invariants

- `delta = long - short`
- `long > short` means `BULLISH`
- `short > long` means `BEARISH`
- `long == short` means `NEUTRAL`
- Investment official direction uses Asset Manager Positions.
- Investment weekly support uses Asset Manager Changes only.
- Investment Day Control is disabled.
- Investment TDL-M&L and TDL-S are disabled.
- Speculation uses Changes only.
- Time calculations use UTC only.
- The Tuesday report becomes effective the following Monday at `00:00:00Z`.
- The effective interval is `[effective_from,effective_until)`.
- CORE is the only public official result.
- EXPANDED remains internal in `SHADOW_MODE`.

## Scope

This PR freezes contracts and regression fixtures only. It does not change
runtime behavior, production services, public APIs, or result stores.

## Next step

PR-064 and PR-065 may implement the approved contracts after explicit
governance approval and unresolved-rule closure.
