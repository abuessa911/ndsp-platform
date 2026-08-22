# NDSP Technical Debt Register

هذا السجل هو المصدر الرسمي الوحيد للديون التقنية المفتوحة في منصة NDSP.

## Status Model

- OPEN
- IN_PROGRESS
- BLOCKED
- RESOLVED
- ACCEPTED

---

## NDSP-DEBT-DEC-001

**Title:** Consolidate duplicated decision output governance functions
**Status:** OPEN
**Priority:** P1
**Domain:** Decision Governance
**Owner:** Decision Engine Sprint
**Detected:** 2026-08-06

### Affected Component

`backend/app/ndsp_governance/decision_output_policy.py`

### Problem

The module contains multiple runtime redefinitions of:

- `govern_decision_output`
- `govern_any_response`
- `contains_forbidden_public_terms`
- `should_drop_key`

In Python, later definitions replace earlier definitions at module scope, making the effective behavior difficult to audit and maintain.

### Risks

- Hidden behavioral overrides.
- Conflicting governance rules.
- Unsafe refactoring.
- Difficulty proving public-output compatibility.
- Increased regression risk.

### Required Remediation

1. Add characterization tests for the effective current behavior.
2. Identify the final runtime implementation of every duplicated function.
3. Consolidate each public function into one canonical definition.
4. Preserve compatibility through explicit internal helpers when required.
5. Verify Decision API V1/V2 output compatibility.
6. Remove superseded definitions only after tests prove equivalence.

### Closure Criteria

- One module-level definition per public function.
- Characterization and regression tests pass.
- Decision API contracts remain compatible.
- Governance validation passes.
- Architecture CHANGELOG is updated.
- No direct decision logic is moved into the Raw COT Gateway.

### Related Architecture Decisions

- `backend/architecture/adr/ADR-0002-completed-decision-ssot.md`
- `backend/architecture/adr/ADR-0003-modular-monolith-with-framework.md`
