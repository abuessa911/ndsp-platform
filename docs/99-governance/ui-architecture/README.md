# UI and Backend Governance Policy

This directory contains the machine-readable governance policy for frontend,
backend, API, design-system, testing, security, CORE/EXPANDED separation,
visual identity, customer terminology exposure, subscription entitlement, and
confidentiality boundaries.

## Governing precedence

The governance stack is now:

1. `NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml` — **ACTIVE / MANDATORY V2 overlay** for visual identity, customer-facing terminology exposure, subscription presentation, 16-day trial exposure, and confidentiality boundaries.
2. `NDSP_UIUX_GOVERNING_REFERENCE_V2.md` — human-readable governing reference for the same V2 decisions.
3. `UI_BACKEND_GOVERNANCE_POLICY.yaml` — baseline normative technical policy. **All unique non-conflicting requirements remain mandatory.**

The merge rule is:

> **MERGE, NOT REWRITE. Preserve unique content. Consolidate only true duplication.**

When a design/exposure rule in the baseline conflicts with the V2 overlay, the
V2 overlay wins **only in its declared scope**. Backend ownership, database
ownership, service boundaries, existing contracts, canonical datasets,
security requirements, traceability, testing, and other non-conflicting
baseline rules remain unchanged.

## Confidential master artifact handling

The repository is public. The complete owner-approved master report contains
confidential architecture and proprietary analytical material and therefore is
**not committed to this public repository**. The public repository stores the
sanitized governing rules and frozen SHA-256 integrity anchors only.

The private master artifact set is:

- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.md`
  - SHA-256: `806be2bb2fbc72ae4192ec68d14d5b0e52162af4b5a9238ca9932b96c08c9d70`
- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.pdf`
  - SHA-256: `43ee65c41ee4451e7956c8242cc637ae80c2e3b28a72a27cf74593281365b3e5`
- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.docx`
  - SHA-256: `f6f7cdf097c827faa58c9a71e1a06cb4104fbe9ee0417d1bad6aa9ad0dff1bd8`

## Files

- `NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml`: controlling V2 design/exposure/confidentiality policy.
- `NDSP_UIUX_GOVERNING_REFERENCE_V2.md`: controlling human-readable V2 reference.
- `UI_BACKEND_GOVERNANCE_POLICY.yaml`: baseline normative technical policy.
- `UI_BACKEND_GOVERNANCE_VALIDATION_REPORT.json`: generated locally when the baseline validator is executed. The report does not need to be committed.
- `NDSP_UIUX_GOVERNANCE_V2_VALIDATION_REPORT.json`: generated locally when the V2 validator is executed. The report does not need to be committed.

## Machine enforcement

V2 is enforced by:

- `scripts/governance/validate_uiux_governance_v2.py`
- `scripts/governance/tests/test_validate_uiux_governance_v2.py`
- `.github/workflows/ui-backend-governance-policy.yml`

The V2 guard fails changed customer/public paths when a change attempts to:

- restore Indigo/Violet as the primary/brand identity;
- expose more than the five approved customer-visible names;
- introduce an unapproved customer-visible Decision Intelligence name;
- expose Decision Layers 01–16 as numbered customer-facing structure;
- serialize forbidden proprietary fields into customer/public API paths;
- commit one of the full confidential master artifacts into the public repository.

The pull-request and push jobs scan the changed-file set. A manual workflow run can optionally request a full-repository V2 source scan.

## Local validation

```bash
python3 -m pip install \
  -r scripts/governance/requirements-ui-backend-governance.txt

python3 scripts/governance/validate_ui_backend_governance_policy.py \
  --repo-root .

python3 scripts/governance/validate_uiux_governance_v2.py \
  --repo-root . \
  --policy-only

python3 -m unittest \
  scripts/governance/tests/test_validate_uiux_governance_v2.py
```

To scan a prepared changed-file list:

```bash
python3 scripts/governance/validate_uiux_governance_v2.py \
  --repo-root . \
  --changed-files /tmp/ndsp-uiux-v2-changed-files.txt
```

To run the V2 guard over the whole repository:

```bash
python3 scripts/governance/validate_uiux_governance_v2.py \
  --repo-root . \
  --full-source-scan
```

Validate the baseline YAML structure only:

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

The baseline validator supports narrow inline exceptions for its heuristic source scans.

```ts
// governance-allow: direct-fetch
const response = await fetch(url);
```

```ts
// governance-allow: expanded-public-reference
```

Exceptions must be justified in an Architecture Decision Record and reviewed
during pull-request approval. The comments do not override structural policy
requirements such as CORE/EXPANDED separation or the V2 confidentiality and
entitlement boundaries. V2 secrecy and customer-exposure failures intentionally
have no inline bypass comment.

## Expected output

Successful baseline validation:

```text
validation=PASS
status=UI_BACKEND_GOVERNANCE_POLICY_VALID
```

Successful V2 validation:

```text
validation=PASS
status=UIUX_GOVERNANCE_V2_VALID
```

Failed V2 validation:

```text
validation=FAIL
status=UIUX_GOVERNANCE_V2_INVALID
```

## TypeScript migration

The incremental migration plan is documented in
[`FRONTEND_TYPESCRIPT_MIGRATION_PLAN.md`](./FRONTEND_TYPESCRIPT_MIGRATION_PLAN.md).
