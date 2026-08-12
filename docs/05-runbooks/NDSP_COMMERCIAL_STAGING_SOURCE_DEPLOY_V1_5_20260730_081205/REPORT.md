
## 0. Safety contract

# NDSP — Commercial Staging Source Deployment V1.5

- Date: 2026-07-30T08:12:05+02:00
- Host: vmi2934783.contaboserver.net
- Project: /home/nawaf511/empire-core-new
- Locked source: /opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
- Production auth service: ndsp-auth-core-clean.service
- Staging DB/unit: ndsp_auth_commercial_staging / ndsp-commercial-auth-payment-staging.service
- Nginx/frontend/production mutation: FORBIDDEN
- External provider traffic: BLOCKED
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_STAGING_SOURCE_DEPLOY_V1_5_20260730_081205/REPORT.md
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
- Public tables: 104
- Canonical schema SHA-256: 2fb0361b93f760c83d9cec23a367719f551195fdc1fc81ad2e7aa2fc15cca3ab
- Production URL in argv: NO
- Production row data copied: NO
- **PRODUCTION_DB_READ_ONLY:** `PASS` — Only public schema metadata was read; archive schemas and all production rows were excluded.

## 3. Reject every existing staging resource

- **STAGING_POLICY:** `PASS` — No staging DB, role, unit, env, release root, state root or current link exists; automatic reset is disabled.

## 4. Create staging DB from schema only

