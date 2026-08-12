
## 0. Safety contract

# NDSP — Commercial Staging Source Deployment V1.2

- Date: 2026-07-30T02:07:40+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Production auth service: ndsp-auth-core-clean.service
- Staging database: ndsp_auth_commercial_staging
- Staging service: ndsp-commercial-auth-payment-staging.service
- Staging root: /opt/ndsp-commercial-auth-payment-staging
- Nginx mutation: FORBIDDEN
- Frontend/design mutation: FORBIDDEN
- Production database mutation: FORBIDDEN
- External payment-provider traffic: BLOCKED
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_2_20260730_020740/REPORT.md
- **SAFETY_CONTRACT:** `PASS` — Explicit confirmation, protected production names, required tools and canonical paths validated.

## 1. Freeze proof and source provenance

- Production auth PID: 2497988
- Active interpreter: /usr/bin/nsolid
- Active entrypoint: /opt/ndsp-auth-core-clean/current/server/dist/server.js
- Resolved active entrypoint: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7/server/dist/server.js
- Active entrypoint SHA-256: a9b20d3614a1ccd268791ddc3caf5777c03d47b5803274064a336392a4e255ce
- Active package root: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Active package: ndsp-clean-auth-core@2.4.0
- Entrypoint relative path: server/dist/server.js
- Selected source package root: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Selected source copy root: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Source package relative path: .
- Source origin: ACTIVE_RELEASE_SOURCE_PACKAGE
- Source provenance: No unique canonical project package matched; the active release contains buildable source.
- Candidate evidence: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_2_20260730_020740/work/source-candidates.tsv
- **SOURCE_PROVENANCE:** `PASS` — Buildable source was proven without treating dist/server.js as editable source. Origin=ACTIVE_RELEASE_SOURCE_PACKAGE; package=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7.

## 2. Read-only production database discovery


## Rollback

- Reason: UNEXPECTED_EXIT_CODE_1_AT_LINE_705
- Production database writes: NO
- Nginx changes/reloads: NO
- Portal/design changes: NO
- Production service restarts: NO
- FINAL_STATUS: `NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_2_FAILED`
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_2_20260730_020740/REPORT.md
