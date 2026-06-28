# DEV-003 — NDSP Project Validator
Generated=20260628_151212
ROOT=/home/nawaf511/empire-core-new
HEAD=f17f044 test(DEV-010D): verify bot execution runtime dependencies
BRANCH=feature/ndsp-os
== 1) GIT STATUS ==
?? backend/architecture/reports/DEV-010E-BOT-SAFE-RUNTIME-SMOKE-20260628_151156.md
== 2) REAL ENV TRACKING CHECK ==
REAL_ENV_TRACKED=PASS
REAL_ENV_HISTORY=PASS
== 3) LITERAL SECRET SCAN HEAD ==
LITERAL_SECRET_SCAN=PASS
== 4) GENERATED ARTIFACTS TRACKING CHECK ==
GENERATED_ARTIFACTS_TRACKED=PASS
== 5) REQUIRED ARCHITECTURE FILES CHECK ==
REQUIRED_PATH_PASS=backend/framework
REQUIRED_PATH_PASS=backend/services
REQUIRED_PATH_PASS=backend/tools/ndsp
REQUIRED_PATH_PASS=backend/architecture
REQUIRED_PATH_PASS=frontend/user-portal-vite
SERVICE_REGISTRY_PATH_PASS=NDSP_DOCTOR_AUTHORITY
SERVICE_REGISTRY_AUTHORITY=NDSP_DOCTOR
== 6) NDSP TOOLKIT CHECK ==
NDSP_DOCTOR=START
ROOT=/home/nawaf511/empire-core-new/backend
ENG001=OK
SERVICES_DIR=OK
SERVICE_REGISTRY=OK
== SERVICE COUNT ==
4
== SERVICE IDS ==
CTL-001 port=9081 file=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/service.yaml
CDS-001 port=9078 file=/home/nawaf511/empire-core-new/backend/services/completed_decision/service.yaml
DGC-001 port=9079 file=/home/nawaf511/empire-core-new/backend/services/decision_governance_core/service.yaml
BOT-001 port=9080 file=/home/nawaf511/empire-core-new/backend/services/bot_execution/service.yaml
== DUPLICATE SERVICE IDS ==
== DUPLICATE PORTS ==
NDSP_DOCTOR=DONE
NDSP_DOCTOR=PASS
VALIDATING=/home/nawaf511/empire-core-new/backend/services/bot_execution
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/bot_execution
VALIDATING=/home/nawaf511/empire-core-new/backend/services/completed_decision
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/completed_decision
VALIDATING=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity
VALIDATING=/home/nawaf511/empire-core-new/backend/services/decision_governance_core
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/decision_governance_core
NDSP_VALIDATE_ALL=PASS
== 7) FRONTEND BUILD CHECK ==

> ndsp-user-portal-vite@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 27 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.44 kB │ gzip:  0.33 kB
dist/assets/index-B87m92fc.css    4.78 kB │ gzip:  1.69 kB
dist/assets/index-CFyGcz_Q.js   150.58 kB │ gzip: 48.46 kB
✓ built in 1.53s
FRONTEND_BUILD=PASS
== 8) IGNORED LOCAL ARTIFACTS ==
!! backend/runtime/
!! ndsp_checkout_plans_package/
!! run_local_ndsp.py
!! runtime/
== 9) SUMMARY ==
FAIL_COUNT=0
WARN_COUNT=0
FINAL_STATUS=OK

# DEV-010E — BOT-001 Safe Runtime Smoke Report

Generated: 20260628_151156

Result:
SAFE_HOST=127.0.0.1
BOT_SAFE_PORT=19080
MOCK_DGC_PORT=19089
MOCK_DGC_READY=YES
BOT_SERVICE_READY=YES
BOT_VERSION_CHECK=PASS
BOT_ABOUT_CHECK=PASS
BOT_HEALTH_CHECK=PASS_OR_OPTIONAL
VALIDATOR_DEV010E=PASS

Safety:
PRODUCTION_BOT_PORT_NOT_USED=YES
REAL_ORDER_ENDPOINT_NOT_CALLED=YES
EXTERNAL_ORDER_ROUTING_DISABLED=YES
DRY_RUN_ENV_ENABLED=YES
MOCK_GOVERNANCE_USED=YES
BINANCE_KEYS_NOT_USED=YES
BYBIT_KEYS_NOT_USED=YES

Next:
DEV-010F close BOT migration.
