# NDSP UI/UX Private Master Approval Lock V2

- **Status:** FROZEN / AUTHORITATIVE / ACTIVE / MANDATORY
- **Effective date:** 2026-08-08
- **Owner approval:** Explicit owner instruction
- **Repository:** `abuessa911/ndsp-platform`
- **Repository visibility:** PUBLIC
- **Confidentiality classification:** CONFIDENTIAL / PROPRIETARY

## Governing decision

The complete V2 UI/UX + Architecture Governance master set is the **canonical private content source** for NDSP. It is registered in project governance by:

- `NDSP_UIUX_PRIVATE_MASTER_MANIFEST_V2.yaml`
- `NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml`
- `NDSP_UIUX_GOVERNANCE_APPROVAL_RECORD_V2.md`
- `NDSP_UIUX_GOVERNING_REFERENCE_V2.md`

The public repository must not contain the confidential full master bytes. The project-local private target is:

`docs/99-governance/private/uiux-v2/`

That target is intentionally git-ignored. The full files may exist there on a private/local checkout or server, but must never be committed to the public repository.

## Canonical artifact set

```text
806be2bb2fbc72ae4192ec68d14d5b0e52162af4b5a9238ca9932b96c08c9d70  NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.md
43ee65c41ee4451e7956c8242cc637ae80c2e3b28a72a27cf74593281365b3e5  NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.pdf
f6f7cdf097c827faa58c9a71e1a06cb4104fbe9ee0417d1bad6aa9ad0dff1bd8  NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.docx
a5005e2c70c9bc4cff6287bea4420984ad9a7bebee1ad7cbc62bc4ba81e45a60  NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_SHA256SUMS.txt
```

Any file with the same name but a different hash is **NOT** the approved reference.

## Installation rule

Use:

```bash
scripts/governance/install_uiux_private_master_v2.sh /path/to/source-directory
```

The installer:

1. verifies all source SHA-256 hashes;
2. verifies the private target is git-ignored;
3. copies the artifacts with private permissions;
4. re-verifies hashes after copy;
5. writes `INSTALLATION_LOCK_V2.txt` as local installation evidence;
6. fails closed on any mismatch.

## Precedence

1. **Private full master** — canonical content source.
2. **V2 Supersession policy** — canonical machine-enforcement source for design, customer exposure, subscription presentation, trial exposure, and confidentiality.
3. **Baseline UI/Backend governance** — preserved for all unique non-conflicting technical requirements.

The merge rule remains:

> **MERGE, NOT REWRITE. Preserve unique content. Consolidate only true duplication.**

## Confidentiality rule

Public-safe governance artifacts may contain approved aliases, hashes, and enforcement rules. They must not reproduce proprietary logic, formulas, hidden layer names, internal contracts, internal data relationships, or confidential master content.

## Final lock

`NDSP_UIUX_PRIVATE_MASTER_V2=FROZEN_AUTHORITATIVE`

A future replacement requires explicit owner approval, a new version, new hashes, governance change record, validation evidence, and rollback path. Silent replacement is forbidden.
