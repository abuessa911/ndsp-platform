# NDSP Remaining Procedures Audit
DATE=2026-07-07T23:11:18+02:00
MODE=READ_ONLY_REPORT_ONLY
MODIFICATIONS=None_to_runtime_or_live_site
PROJECT=/home/nawaf511/empire-core-new
LIVE=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## 1) V1 Release Baseline
Release package:
-rw-rw-r-- 1 nawaf511 nawaf511 116K يوليو   7 23:01 /home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz

Release checksum:
1021596e6cc4fd1e36e375b1c4f67fe77426463902ad4c23c6020c1041671144  /home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz

## 2) Current Reality Lock Status
[OK] Reality Lock exists
1732:- AUTH_ROUTE_ALIAS_V1_STATUS=APPLIED
1783:- FINAL_V1_RELEASE_READINESS_STATUS=OK
1784:- RELEASE_RESULT=READY_WITH_GOVERNANCE_LOCK
1866:- V1_RELEASE_PACKAGE_STATUS=CREATED
1888:- FINAL_V1_RELEASE_READINESS_STATUS=OK
1889:- RELEASE_RESULT=READY_WITH_GOVERNANCE_LOCK
1890:- V1_RELEASE_PACKAGE_STATUS=CREATED

## 3) Required Control Documents Presence
[MISS] NDSP_MASTER_GOVERNANCE_RULES.md
[MISS] NDSP_PAGE_REGISTRY.md
[MISS] NDSP_API_CONTRACT.md
[MISS] NDSP_DATABASE_SCHEMA.md
[MISS] NDSP_DECISION_ENGINES_SPEC.md
[MISS] NDSP_SECURITY_POLICY.md
[MISS] NDSP_TEST_PLAN.md
[MISS] NDSP_DEPLOYMENT_RUNBOOK.md
[MISS] NDSP_ROLLBACK_PLAN.md
[MISS] NDSP_PROTECTED_FILES_AND_RULES.md
[MISS] NDSP_AI_BUILDER_PROMPT.md

## 4) Decision Room Contracts
[OK] docs/06-decision-room-contracts exists
docs/06-decision-room-contracts/NDSP_DECISION_ROOM_EXPERIENCE_CONTRACT_V1.json
docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_AR_v1.md
docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_EN_v1.md
SEVEN_CONTRACTS_MENTION_COUNT=45
AXIS_24_LOCK_MENTION_COUNT=4
GOVERNING_SENTENCE_COUNT=6

## 5) Practical Runbook Files
[OK] NDSP_V1_FREEZE_AR.md -> docs/05-runbooks/NDSP_V1_FREEZE_AR.md
[MISS] NDSP_V1_FREEZE_EN.md
[OK] NDSP_LEGAL_DISCLAIMER_MASTER_AR.md -> docs/04-legal/NDSP_LEGAL_DISCLAIMER_MASTER_AR.md
[MISS] NDSP_LEGAL_DISCLAIMER_MASTER_EN.md
[OK] NDSP_IMPLEMENTATION_TASKS_AR.md -> docs/05-runbooks/NDSP_IMPLEMENTATION_TASKS_AR.md
[MISS] NDSP_IMPLEMENTATION_TASKS_EN.md

## 6) Scripts Readiness
[OK] scripts/audit files=3
[OK] scripts/backup files=2
[OK] scripts/tests files=2
[OK] scripts/deploy files=0

## 7) Official Routes Quick Check
[200] https://my.ndsp.app/
[200] https://my.ndsp.app/index.html
[200] https://my.ndsp.app/decision-support.html
[200] https://my.ndsp.app/NDSP_Asset_View.html
[200] https://my.ndsp.app/NDSP_Command_Center.html
[200] https://my.ndsp.app/NDSP_Daily_Brief.html
[200] https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] https://my.ndsp.app/disclaimer.html
[200] https://my.ndsp.app/login
[200] https://my.ndsp.app/register
[200] https://my.ndsp.app/forgot-password
[200] https://my.ndsp.app/reset-password

## 8) Scenario Levels Readiness
[200] https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT
SYMBOL=ETHUSDT
[MISS] scenario/reference levels object

[200] https://api.ndsp.app/api/decision/quality-live?symbol=BTCUSDT
SYMBOL=BTCUSDT
[MISS] scenario/reference levels object

[200] https://api.ndsp.app/api/decision/quality-live?symbol=XAUUSD
SYMBOL=XAUUSD
[MISS] scenario/reference levels object

[200] https://api.ndsp.app/api/decision/quality-live?symbol=USOIL
SYMBOL=USOIL
[MISS] scenario/reference levels object


## 9) Auth Functional Test Readiness
This audit does not create real users.
Need separate controlled test for:
- registration with new test email/phone
- duplicate email block
- duplicate phone block
- login success
- login failure safety
- forgot/reset password token flow
- disclaimer acceptance persistence

## 10) Alerts/API Readiness Probe
[200] https://api.ndsp.app/api/alerts
BODY: {"ok":true,"symbol":"BTCUSDT","alerts":[{"type":"caution","title":"تنبيه تحفظ","message":"انتظار ثبات السعر دون منطقة المراجعة."},{"type":"scenario","title":"ح[200] https://api.ndsp.app/api/settings
BODY: {"ok":true,"language":"ar","theme":"dark","direction":"rtl","data_mode":"live_backend","protected_layers_masked":true,"generated_at":"2026-07-07T21:11:26.737488+00:00"}[404] https://api.ndsp.app/api/assets
BODY: {"ok": false, "error": "NOT_FOUND", "path": "/api/assets", "service": "ndsp-platform-gateway-9002"}[200] https://api.ndsp.app/api/trial/status
BODY: {"ok": true, "source_mode": "ndsp_platform_gateway_9002_recovery", "trial": {"enabled": true, "duration_days": 16, "status": "ACTIVE", "registration_endpoint": "/api/trial/register/ordinary"}, "messag[404] https://api.ndsp.app/api/auth/me
BODY: <!DOCTYPE html>
BODY: <html lang="en">
BODY: <head>
BODY: <meta charset="utf-8">
BODY: <title>Error</title>
BODY: </head>
BODY: <body>
BODY: <pre>Cannot GET /api/auth/me</pre>
BODY: </body>
BODY: </html>

## 11) Monitoring Tools Probe
[OK] command found: docker -> /usr/bin/docker
[OK] command found: docker-compose -> /usr/bin/docker-compose
[MISS] command not found: uptime-kuma
[MISS] command not found: sentry-cli
[MISS] command not found: netdata
[OK] command found: logrotate -> /usr/sbin/logrotate
[MISS] netdata service not detected

## 12) Mobile/Visual Test Readiness
[OK] npx exists
[MISS] Playwright config/files not found

## 13) Admin Console Probe
[200] https://admin.ndsp.app
[200] https://my.ndsp.app/admin
[200] https://my.ndsp.app/admin.html

## 14) Recommended Remaining Backlog
P0 — Convert required control docs into standalone files if missing.
P0 — Install/normalize Decision Room contracts under docs/06-decision-room-contracts if missing.
P0 — Create README governance entry with governing sentence if missing.
P1 — Controlled Auth Functional Test with a test account.
P1 — Disclaimer Gate Functional Test.
P1 — Scenario Levels V1.2 plan and contract alignment.
P2 — Alerts V1.3 plan and API contract.
P2 — Monitoring pack: Uptime Kuma/Sentry/Netdata/cron backup/logrotate.
P2 — Mobile/RTL visual audit with screenshots or Playwright.
P3 — Admin Console V1.4 plan.

## 15) Final Evaluation
ROUTES_OK=1
MISSING_CONTROL_DOCS=11
SEVEN_CONTRACTS_MENTION_COUNT=45
AXIS_24_LOCK_MENTION_COUNT=4
GOVERNING_SENTENCE_COUNT=6
SCENARIO_LEVELS_OK=1
V1_RUNTIME_STATUS=OK
GOVERNANCE_DOCS_STATUS=NEEDS_NORMALIZATION

FINAL_STATUS=REMAINING_PROCEDURES_AUDIT_DONE
REPORT=docs/05-runbooks/NDSP_REMAINING_PROCEDURES_AUDIT_20260707_231118.md
