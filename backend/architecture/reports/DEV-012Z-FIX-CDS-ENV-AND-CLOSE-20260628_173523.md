# DEV-012Z — Fix CDS Env And Close

Generated: 20260628_173523
Branch: feature/ndsp-os
Head: 3085a36 ops(DEV-012): recover and close systemd local rollout

## Summary

FAIL_COUNT=0
WARN_COUNT=1
NGINX_OK=1

FINAL_STATUS=DEV012_SYSTEMD_LOCAL_DONE

## Runtime Env
/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env

## Backup Directory
/home/nawaf511/ndsp_systemd_backups/dev012_fix_env_20260628_173523

## Raw Run Report
/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_FIX_CDS_ENV_AND_CLOSE_20260628_173523.md
# DEV-012Z — Fix CDS Env And Close
ROOT=/home/nawaf511/empire-core-new
HEAD=3085a36 ops(DEV-012): recover and close systemd local rollout
BRANCH=feature/ndsp-os
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_FIX_CDS_ENV_AND_CLOSE_20260628_173523.md
REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012Z-FIX-CDS-ENV-AND-CLOSE-20260628_173523.md
ENV_FILE=/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env

== 1) QUARANTINE ==
PASS=QUARANTINED_apps_user_portal=/home/nawaf511/empire-core-new/backend/runtime/quarantine/apps-user-portal-20260628_173523/user-portal

== 2) CLEAN STATUS ==

PASS=WORKTREE_CLEAN

== 3) CAPTURE WORKING CDS ENV ==
CDS-001_CAPTURE_ENV_FROM_PID=1139916
PASS=CDS-001_ENV_DB_KEYS_CAPTURED
PASS=ENV_FILE_WRITTEN=/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env

== 4) PATCH UNITS WITH RUNTIME ENVFILE ==
PASS=CDS-001_REPO_UNIT_ENVFILE_ADDED
PASS=CDS-001_INSTALLED_UNIT_PATCHED=/etc/systemd/system/ndsp-completed_decision.service
PASS=DGC-001_REPO_UNIT_ENVFILE_ADDED
PASS=DGC-001_INSTALLED_UNIT_PATCHED=/etc/systemd/system/ndsp-decision_governance_core.service
PASS=BOT-001_REPO_UNIT_ENVFILE_ADDED
PASS=BOT-001_INSTALLED_UNIT_PATCHED=/etc/systemd/system/ndsp-bot_execution.service

== 5) START VERIFY CDS DGC BOT ==

== START_VERIFY CDS-001 ==
WARN=CDS-001_KILLING_EXISTING_PORT_PID=1139916
PASS=CDS-001_ACTIVE_OWNED_HEALTHY
CDS-001_MAINPID=1193192
CDS-001_PORT_PID=1193192
PASS=CDS-001_health_HTTP_OK=http://127.0.0.1:9078/health
PASS=CDS-001_version_HTTP_OK=http://127.0.0.1:9078/version
PASS=CDS-001_about_HTTP_OK=http://127.0.0.1:9078/about

== START_VERIFY DGC-001 ==
PASS=DGC-001_ACTIVE_OWNED_HEALTHY
DGC-001_MAINPID=1193555
DGC-001_PORT_PID=1193555
PASS=DGC-001_health_HTTP_OK=http://127.0.0.1:9079/health
PASS=DGC-001_version_HTTP_OK=http://127.0.0.1:9079/version
PASS=DGC-001_about_HTTP_OK=http://127.0.0.1:9079/about

== START_VERIFY BOT-001 ==
PASS=BOT-001_ACTIVE_OWNED_HEALTHY
BOT-001_MAINPID=1193947
BOT-001_PORT_PID=1193947
PASS=BOT-001_health_HTTP_OK=http://127.0.0.1:9080/health
PASS=BOT-001_version_HTTP_OK=http://127.0.0.1:9080/version
PASS=BOT-001_about_HTTP_OK=http://127.0.0.1:9080/about

== 6) ENABLE SERVICES ==
PASS=ndsp-ctl-001-workspace-identity.service_ENABLED
PASS=ndsp-completed_decision.service_ENABLED
PASS=ndsp-decision_governance_core.service_ENABLED
PASS=ndsp-bot_execution.service_ENABLED

== 7) FINAL CHAIN CHECK ==
PASS=CDS-001_completed_latest_HTTP_OK=http://127.0.0.1:9078/api/completed/latest
PASS=DGC-001_governance_evaluate_HTTP_OK

== 8) FINAL OWNERSHIP ==
CTL-001_MAINPID=1359
CTL-001_PORT_PID=1359
PASS=CTL-001_ACTIVE
PASS=CTL-001_ENABLED
PASS=CTL-001_OWNERSHIP_OK
CDS-001_MAINPID=1193192
CDS-001_PORT_PID=1193192
PASS=CDS-001_ACTIVE
PASS=CDS-001_ENABLED
PASS=CDS-001_OWNERSHIP_OK
DGC-001_MAINPID=1193555
DGC-001_PORT_PID=1193555
PASS=DGC-001_ACTIVE
PASS=DGC-001_ENABLED
PASS=DGC-001_OWNERSHIP_OK
BOT-001_MAINPID=1193947
BOT-001_PORT_PID=1193947
PASS=BOT-001_ACTIVE
PASS=BOT-001_ENABLED
PASS=BOT-001_OWNERSHIP_OK

== 9) NGINX TEST ==
PASS=NGINX_TEST_OK
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

== 10) REPORT VALIDATOR ==
# DEV-003 — NDSP Project Validator
Generated=20260628_173536
ROOT=/home/nawaf511/empire-core-new
HEAD=3085a36 ops(DEV-012): recover and close systemd local rollout
BRANCH=feature/ndsp-os
== 1) GIT STATUS ==
 M backend/services/bot_execution/systemd/ndsp-bot_execution.service
 M backend/services/completed_decision/systemd/ndsp-completed_decision.service
 M backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service
?? backend/architecture/reports/DEV-012Z-FIX-CDS-ENV-AND-CLOSE-20260628_173523.md
?? backend/architecture/reports/DEV-012Z-FIX-CDS-ENV-AND-CLOSE-20260628_173523.md.validator.md
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
PASS=VALIDATOR_OK
