
## 0. Safety contract

# NDSP — Commercial Staging Source Deployment V1.3

- Date: 2026-07-30T02:15:21+02:00
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
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_3_20260730_021521/REPORT.md
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
- Staging schema scope: public only
- Non-public/archive schemas copied: NONE
- Production row data copied: NONE
- Source origin: ACTIVE_RELEASE_SOURCE_PACKAGE
- Source provenance: No unique canonical project package matched; the active release contains buildable source.
- Candidate evidence: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_3_20260730_021521/work/source-candidates.tsv
- **SOURCE_PROVENANCE:** `PASS` — Buildable source was proven without treating dist/server.js as editable source. Origin=ACTIVE_RELEASE_SOURCE_PACKAGE; package=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7.

## 2. Read-only production database discovery

- Production DB: ndsp_auth
- Production DB port: 5432
- Active/local database identity match: YES
- Staging schema scope: public only
- Production public tables: 104
- User-installed extensions captured: 1
- Excluded non-public schemas: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_3_20260730_021521/work/excluded-production-schemas.txt
- Public schema SHA-256: 0c2a459d43c709024f9563376c5e1cefcee21b8c283f0bf0079a681b68e9fac7
- Production credentials printed: NO
- Production SQL mutation: NO
- **PRODUCTION_DB_READ_ONLY:** `PASS` — The active DB identity was matched locally and only public schema metadata was dumped read-only as postgres; archive schemas and all table data were excluded.

## 3. Existing staging resource policy

- **STAGING_RESOURCE_POLICY:** `PASS` — Only staging-scoped resources are new or explicitly reset; production resources are excluded.

## 4. Create isolated staging database from schema only


## Rollback

- Reason: UNEXPECTED_EXIT_CODE_1_AT_LINE_925
- Production database writes: NO
- Nginx changes/reloads: NO
- Portal/design changes: NO
- Production service restarts: NO
- FINAL_STATUS: `NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_3_FAILED`
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_3_20260730_021521/REPORT.md
