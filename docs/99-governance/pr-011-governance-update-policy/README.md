# PR-011 Governance Update Policy

PR-011 defines the controlled lifecycle for future governance documentation
changes after completion of PR-004 through PR-010.

## Scope

- Governance documentation only.
- No application, service, deployment, configuration, or runtime changes.
- Existing governance artifacts are validated but not modified.

## Policy objectives

1. Keep governance and runtime changes isolated.
2. Require explicit change classification and ownership.
3. Require reproducible validation evidence.
4. Prevent silent modification of canonical artifacts.
5. Verify every governance merge on `origin/main`.
6. Remove temporary branches and worktrees after completion.

## Change classes

| Class | Purpose | Required review |
|---|---|---|
| Correction | Fix inaccurate documentation without changing intent | One maintainer |
| Extension | Add governed components or evidence | Owner and maintainer |
| Policy change | Change governance requirements or approval rules | Governance owner and maintainer |
| Closure | Record completion or integrity state | Maintainer |

## Required PR controls

- One clearly defined governance objective.
- Changes limited to `docs/99-governance/` unless explicitly approved.
- No undocumented deletions.
- Valid JSON for machine-readable artifacts.
- Verified SHA-256 checksums.
- Clean and intentional commit scope.
- Mergeable pull request targeting `main`.
- Merge commit verified on `origin/main`.
- Temporary branches and worktrees removed.

## Existing governance baseline

- Source commit: `640327b806d40f87783c42029862a0b79417da02`
- Required prior packages: 7
- Missing packages: 0
- Invalid primary JSON artifacts: 0

## Artifacts

- `GOVERNANCE_UPDATE_POLICY.json`
- `GOVERNANCE_UPDATE_CHECKLIST.md`
- `PR011_SHA256SUMS.txt`

## Final declaration

- Runtime changes: none
- Validation: PASS
- Status: ACTIVE
