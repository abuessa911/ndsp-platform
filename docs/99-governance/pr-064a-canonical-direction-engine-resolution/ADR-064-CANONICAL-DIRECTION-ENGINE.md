# ADR-064 — Canonical Direction Engine

## Status

**Proposed for human approval**

## Context

PR-062 identified 24 direction/time-related impact records,
including 7 high-risk records. PR-063 froze versioned
direction, timing, CORE, and EXPANDED contracts but explicitly retained human
approval before implementation.

The path `backend/services/decision_governance_core/` is not currently present in the repository.
Therefore this ADR proposes the path but does not create runtime code there.

## Decision

1. The proposed canonical owner is `decision_governance_core`.
2. The proposed canonical path is `backend/services/decision_governance_core/`.
3. The raw COT gateway remains raw-data-only.
4. CORE is the sole public official result.
5. EXPANDED remains internal and shadow-only.
6. Investment Day Control, TDL-M&L, and TDL-S are disabled.
7. Speculation TDL and Day Control remain disabled until separate semantics
   approval.
8. PR-064A changes governance artifacts only.
9. PR-064 implementation is prohibited until human approval and physical
   result-store decisions are recorded.

## Consequences

- No product or runtime change occurs in this PR.
- Existing high-risk integration points require WRAP or REPLACE review.
- Physical Official and Experimental Result Stores remain pending.
- No TDL semantics are invented.
- The decision package may be merged as evidence, but it does not authorize
  implementation.

## Approval gate

Implementation may begin only after a separately recorded approval confirms:

- canonical engine path;
- logic owner;
- physical result stores;
- public and internal API writers;
- TDL and Day Control policy;
- rollback and shadow deployment plan.
