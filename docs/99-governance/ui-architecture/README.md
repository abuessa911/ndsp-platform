# UI and Backend Governance Policy

This directory contains the machine-readable governance policy for frontend,
backend, API, design-system, testing, security, and CORE/EXPANDED separation.

## Files

- `UI_BACKEND_GOVERNANCE_POLICY.yaml`: normative policy.
- `UI_BACKEND_GOVERNANCE_VALIDATION_REPORT.json`: generated locally when the
  validator is executed. The report does not need to be committed.

## Local validation

```bash
python3 -m pip install \
  -r scripts/governance/requirements-ui-backend-governance.txt

python3 scripts/governance/validate_ui_backend_governance_policy.py \
  --repo-root .
```

Validate the YAML structure only:

```bash
python3 scripts/governance/validate_ui_backend_governance_policy.py \
  --repo-root . \
  --policy-only
```

Treat warnings as failures:

```bash
python3 scripts/governance/validate_ui_backend_governance_policy.py \
  --repo-root . \
  --strict-warnings
```

## Explicit exceptions

The validator supports narrow inline exceptions for heuristic source scans.

```ts
// governance-allow: direct-fetch
const response = await fetch(url);
```

```ts
// governance-allow: expanded-public-reference
```

Exceptions must be justified in an Architecture Decision Record and reviewed
during pull-request approval. The comments do not override structural policy
requirements such as CORE/EXPANDED separation.

## Expected output

Successful validation:

```text
validation=PASS
status=UI_BACKEND_GOVERNANCE_POLICY_VALID
```

Failed validation:

```text
validation=FAIL
status=UI_BACKEND_GOVERNANCE_POLICY_INVALID
```

## TypeScript migration

The incremental migration plan is documented in
[`FRONTEND_TYPESCRIPT_MIGRATION_PLAN.md`](./FRONTEND_TYPESCRIPT_MIGRATION_PLAN.md).
