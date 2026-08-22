# PR-012 Governance Exceptions and Approvals Register

PR-012 establishes the canonical register for governance exceptions,
approvals, expiry conditions, review evidence, and closure decisions.

## Scope

- Governance documentation only.
- No application, service, configuration, deployment, or runtime changes.
- Existing PR-004 through PR-011 artifacts are validated but not modified.

## Register state

The initial register intentionally contains no active exceptions.

| State | Count |
|---|---:|
| Active exceptions | 0 |
| Expired exceptions | 0 |
| Closed exceptions | 0 |
| Pending approvals | 0 |
| Recorded approvals | 0 |

## Required exception controls

- Unique immutable exception identifier.
- Explicit affected scope.
- Named requester and owner.
- Documented business or technical justification.
- Documented risk assessment.
- Documented compensating controls.
- Named approvers and approval evidence.
- Effective, review, and expiry dates.
- Closure status and closure evidence.
- Full decision history retained after closure.

## Approval model

| Change type | Required approvers |
|---|---|
| Documentation correction | Maintainer |
| Governance extension | Artifact owner and maintainer |
| Policy exception | Governance owner and maintainer |
| Runtime-scope exception | Runtime owner, governance owner, and maintainer |

## Existing governance baseline

- Source commit: `142e0067fa5de9ea1d58227e235b40d6386d3423`
- Required prior packages: 8
- Missing packages: 0
- Invalid primary JSON artifacts: 0

## Artifacts

- `GOVERNANCE_EXCEPTIONS_REGISTER.json`
- `EXCEPTION_REQUEST_TEMPLATE.md`
- `PR012_SHA256SUMS.txt`

## Final declaration

- Active exceptions: 0
- Pending approvals: 0
- Runtime changes: none
- Validation: PASS
- Status: ACTIVE
