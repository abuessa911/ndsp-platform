# PR-019 — Capability Discovery Audit

## Truth statement

The audit covers `origin/main`, local tracked modifications, local-only files,
untracked files, and read-only runtime evidence.

The original static pass produced `976` candidates. That raw number
is not treated as the final number of NDSP capabilities because it included
dependencies, backups, generated assets, localization files, generic symbols,
and host infrastructure.

## Quality-controlled result

- Active capability candidates: `526`
- Excluded candidates retained for reinspection: `450`
- Human review queue: `526`
- Full coverage claimed: `false`
- Runtime changes: `none`

No candidate was silently deleted. Every filtered candidate is retained in
`PR019_EXCLUDED_CANDIDATES.csv` with its exclusion classification and remains
available for reinspection.

## Preservation rule

Every active candidate has:

- `full_power_preservation=REQUIRED`
- `human_validation_status=PENDING`

No active capability may be omitted from design mapping until its source,
runtime service, real-data calculation, API contract, role, and UI
representation are validated or a governed exclusion is approved.

## Next stage

PR-020 must review the active catalog by priority:

1. `P0`: endpoints and high-value economic, trading, decision, quality, and
   analytics capabilities.
2. `P1`: local-only, locally modified, and runtime-only capabilities.
3. `P2`: remaining source candidates.

Status: `DISCOVERY_QUALITY_FILTERED_COVERAGE_NOT_CLAIMED`
