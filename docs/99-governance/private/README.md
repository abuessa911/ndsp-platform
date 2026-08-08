# NDSP Private Governance Artifacts

This directory is reserved for **local/private project copies only** of confidential governance artifacts.

The repository is public, so confidential master artifacts must **not** be committed. The nested `.gitignore` intentionally ignores everything in this directory except this README and the ignore rule itself.

## Canonical V2 private target

Install the owner-approved UI/UX Architecture Governance V2 master set under:

`docs/99-governance/private/uiux-v2/`

Expected files:

- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.md`
- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.pdf`
- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.docx`
- `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_SHA256SUMS.txt`

The authoritative hashes and governance registration are stored in:

`docs/99-governance/ui-architecture/NDSP_UIUX_PRIVATE_MASTER_MANIFEST_V2.yaml`

Use:

```bash
scripts/governance/install_uiux_private_master_v2.sh /path/to/source-directory
```

The installer verifies all SHA-256 hashes before accepting the files and writes a local installation stamp. A mismatch fails closed.

## Governance precedence

The private full master is the canonical content source. The sanitized V2 overlay remains the canonical machine-enforcement source for the public repository. All unique non-conflicting baseline requirements remain mandatory.
