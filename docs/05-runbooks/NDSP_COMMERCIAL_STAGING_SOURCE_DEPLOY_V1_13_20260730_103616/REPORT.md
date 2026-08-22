
## 0. Safety contract

# NDSP — Commercial Staging Source Deployment V1.13

- Date: 2026-07-30T10:36:16+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Locked source: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Production auth service: ndsp-auth-core-clean.service
- Staging DB/unit: ndsp_auth_commercial_staging / ndsp-commercial-auth-payment-staging.service
- Nginx/frontend/production mutation: FORBIDDEN
- External provider traffic: BLOCKED
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_13_20260730_103616/REPORT.md
- **SAFETY_CONTRACT:** `PASS` — Explicit confirmation, protected names, tools, identities and canonical paths validated.

## 1. Lock production process and source

- Auth PID: 2497988
- Interpreter: /usr/bin/nsolid
- Entrypoint: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7/server/dist/server.js
- Entrypoint SHA-256: a9b20d3614a1ccd268791ddc3caf5777c03d47b5803274064a336392a4e255ce
- Locked package: ndsp-clean-auth-core@2.4.0
- package.json SHA-256: 92c3c30b3a6032b6bbad06153f9720849a8360df89c9e0de768c86cd1a8142e6
- package-lock SHA-256: 48d43f189d8fac65217de3c73b137f1fd0f38394be04ab923c1b3b0180b4c347
- Source manifest SHA-256: 0aa854cd7e65321dff2138e2dc5766be778e143ff25a7ff714e2fab3afb0e3fa
- Automatic source selection: DISABLED
- **SOURCE_LOCK:** `PASS` — Active production entrypoint and audited source path match the expected package identity and hashes.

## 2. Discover production DB read-only without URL in argv

- Production DB: ndsp_auth (local, port 5432, oid 49245)
- Password column contract: password_hash
- Public tables: 104
- ndsp_guard functions: 4
- ndsp_guard data-bearing relations: 0
- Canonical public+ndsp_guard schema SHA-256: 8f10ec54e73a80111c17440e5d5eb85eab61e47214cfd24064ea3b27cf686abf
- Production URL in argv: NO
- Production row data copied: NO
- **PRODUCTION_DB_READ_ONLY:** `PASS` — Only public and ndsp_guard schema metadata were read; ndsp_guard contains functions but no data-bearing relations; archive schemas and all production rows were excluded.

## 3. Reject every existing staging resource

- **STAGING_POLICY:** `PASS` — No staging DB, role, OS user/group, unit, env, release root, state root or current link exists; automatic reset is disabled.

## 4. Create staging DB from schema only

- Removed conflicting CREATE SCHEMA public statements from restore stream: 1
- Preserved CREATE SCHEMA ndsp_guard statements in restore stream: 1
- Production/staging canonical public+ndsp_guard schema: 8f10ec54e73a80111c17440e5d5eb85eab61e47214cfd24064ea3b27cf686abf
- ndsp_guard functions restored: 4
- ndsp_guard data-bearing relations restored: 0
- Production rows copied: NO
- **STAGING_DATABASE:** `PASS` — Schema-only DB created; extensions restored via stdin; public and ndsp_guard were restored in dependency order; the pre-existing public schema conflict was filtered only from the restore stream; exact combined-schema round-trip passed.

## 5. Copy locked source and rebuild offline

- Dependency root locked: /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules
- Dependency bytes copied by value: 76225285
- Dependency regular-file manifest match: YES
- Internal dependency symlink manifest match: YES
- Internal dependency symlinks preserved and confined: 18
- External dependency links retained: NO
- Built staging entrypoint: /opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/source/server/dist/server.js
- Built SHA-256: a9b20d3614a1ccd268791ddc3caf5777c03d47b5803274064a336392a4e255ce
- Built staging UI index: /opt/ndsp-commercial-auth-payment-staging/releases/20260730_103616-source-staging-v1-13/source/ui-dist/index.html
- **SOURCE_BUILD:** `PASS` — Locked source rebuilt in an isolated no-network transient unit; server and UI outputs were verified with privileged traversal; production dist and secrets were not reused.

## 6. Generate environment and immutable private release

- **IMMUTABLE_RELEASE:** `PASS` — Release is root-owned, staging-group-readable, not world-readable and has no writable files.

## 7. Install private systemd service

- Staging PID: 3520574
- Private listener: 127.0.0.1:19094
- Public Nginx route: NONE
- Starts on reboot: NO
- **STAGING_SERVICE:** `PASS` — Service is active only inside a private network namespace, disabled at boot, with no Nginx route.

## 8. Smoke test private namespace

- **SMOKE_TEST:** `PASS` — Canonical session route answered inside the private namespace and the staging safety marker is valid.

## 9. Prove production untouched

- **PRODUCTION_UNTOUCHED:** `PASS` — Nginx, portal, canonical backend, locked source, production entrypoint and auth PID are unchanged.

## 10. Final manifest

- **FINAL:** `PASS` — Isolated source-built staging passed exact schema round-trip, private service smoke test and production freeze proof.

- PASS: 11
- FAIL: 0
- Staging database: ndsp_auth_commercial_staging
- Staging OS/DB identity: ndsp_commercial_staging
- Staging service: ndsp-commercial-auth-payment-staging.service
- Staging PID: 3520574
- Private namespace port: 19094
- Public Nginx route: NONE
- Starts automatically: NO
- Source lock: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Production DB writes/rows copied: NONE
- Production restart: NONE
- Portal/design changes: NONE
- FINAL_STATUS: `NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_13_PASS`
- REPORT: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_13_20260730_103616/REPORT.md
- GATES: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_13_20260730_103616/GATES.tsv
- MANIFEST: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_13_20260730_103616/MANIFEST.sha256
