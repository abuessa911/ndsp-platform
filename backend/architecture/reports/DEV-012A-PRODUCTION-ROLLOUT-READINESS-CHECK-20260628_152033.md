# DEV-012A — Production Rollout Readiness Check

Generated: 20260628_152033
Branch: feature/ndsp-os
Head: 5c2055b docs(DEV-011): close NDSP core services migration
Release Tag: v0.3-ndsp-core-services

## Safety

NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SYSTEMD_RELOAD=YES
NO_NGINX_RELOAD=YES
NO_PRODUCTION_WRITE=YES
REPORT_ONLY=YES

## Core Services

CTL-001=ENG-001_REFERENCE
CDS-001=ENG-001_CLOSED
DGC-001=ENG-001_CLOSED
BOT-001=ENG-001_CLOSED

## Validation Summary

FAIL_COUNT=0
WARN_COUNT=15

READINESS=READY_WITH_REVIEW_NOTES
FINAL_STATUS=DEV012A_READY_WITH_REVIEW

## Notes

This check does not deploy, reload, start, stop, or mutate production services.
Warnings usually mean the service is not currently installed/running under systemd or local endpoints are not active yet.

## Raw Run Report

/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_PRODUCTION_ROLLOUT_READINESS_CHECK_20260628_152033.md
# DEV-012A — Production Rollout Readiness Check
Generated=20260628_152033
ROOT=/home/nawaf511/empire-core-new
BRANCH=feature/ndsp-os
HEAD=5c2055b docs(DEV-011): close NDSP core services migration
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_PRODUCTION_ROLLOUT_READINESS_CHECK_20260628_152033.md
ARCH_REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012A-PRODUCTION-ROLLOUT-READINESS-CHECK-20260628_152033.md

== 0) SAFETY NOTICE ==
NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SYSTEMD_RELOAD=YES
NO_NGINX_RELOAD=YES
NO_PRODUCTION_WRITE=YES
REPORT_ONLY=YES

== 1) QUARANTINE UNTRACKED apps/user-portal IF EXISTS ==
PASS=QUARANTINED_apps_user_portal=/home/nawaf511/empire-core-new/backend/runtime/quarantine/apps-user-portal-20260628_152033/user-portal

== 2) CLEAN STATUS CHECK ==

PASS=WORKTREE_CLEAN

== 3) RELEASE TAG / GIT CHECK ==
PASS=TAG_EXISTS=v0.3-ndsp-core-services
PASS=TAG_AT_HEAD=v0.3-ndsp-core-services
5c2055b (HEAD -> feature/ndsp-os, tag: v0.3-ndsp-core-services, origin/feature/ndsp-os) docs(DEV-011): close NDSP core services migration
3e3a19a docs(DEV-010F): close bot execution migration
e1e07d6 test(DEV-010E): run bot execution safe runtime smoke
f17f044 test(DEV-010D): verify bot execution runtime dependencies
f222251 test(DEV-010C): smoke test bot execution adapter
92ca71a feat(DEV-010B): migrate bot execution service to ENG-001 adapter
193b591 docs(DEV-010A): snapshot bot execution service
b02cab8 docs(DEV-009F): close decision governance migration
9d68940 test(DEV-009E): run decision governance safe runtime smoke
6eea09f test(DEV-009D): verify decision governance runtime dependencies
5565807 test(DEV-009C): smoke test decision governance adapter
96942d9 feat(DEV-009B): migrate decision governance core to ENG-001 adapter

== 4) CORE SERVICE CLOSURE CHECK ==
CTL-001_PATH=backend/services/ctl-001-workspace-identity
CTL-001_FRAMEWORK=ENG-001
CTL-001_PORT=9081
CTL-001_SYSTEMD=ndsp-ctl-001-workspace-identity.service
PASS=CTL-001_FRAMEWORK_ENG001
CDS-001_PATH=backend/services/completed_decision
CDS-001_FRAMEWORK=ENG-001
CDS-001_PORT=9078
CDS-001_SYSTEMD=ndsp-completed_decision.service
PASS=CDS-001_FRAMEWORK_ENG001
PASS=CDS-001_MIGRATION_CLOSED
PASS=CDS-001_ADAPTER_EXISTS
DGC-001_PATH=backend/services/decision_governance_core
DGC-001_FRAMEWORK=ENG-001
DGC-001_PORT=9079
DGC-001_SYSTEMD=ndsp-decision_governance_core.service
PASS=DGC-001_FRAMEWORK_ENG001
PASS=DGC-001_MIGRATION_CLOSED
PASS=DGC-001_ADAPTER_EXISTS
BOT-001_PATH=backend/services/bot_execution
BOT-001_FRAMEWORK=ENG-001
BOT-001_PORT=9080
BOT-001_SYSTEMD=ndsp-bot_execution.service
PASS=BOT-001_FRAMEWORK_ENG001
PASS=BOT-001_MIGRATION_CLOSED
PASS=BOT-001_ADAPTER_EXISTS

== 5) ADAPTER LOAD CHECK ==
PASS=CDS-001_ADAPTER_LOAD
CDS-001_FRAMEWORK_ID=ENG-001
PASS=DGC-001_ADAPTER_LOAD
DGC-001_FRAMEWORK_ID=ENG-001
PASS=BOT-001_ADAPTER_LOAD
BOT-001_FRAMEWORK_ID=ENG-001
PASS=ADAPTER_LOAD_CHECK

== 6) TOOLKIT AND PROJECT VALIDATOR ==
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
PASS=NDSP_DOCTOR
VALIDATING=/home/nawaf511/empire-core-new/backend/services/bot_execution
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/bot_execution
VALIDATING=/home/nawaf511/empire-core-new/backend/services/completed_decision
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/completed_decision
VALIDATING=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity
VALIDATING=/home/nawaf511/empire-core-new/backend/services/decision_governance_core
VALIDATION_PASS=/home/nawaf511/empire-core-new/backend/services/decision_governance_core
PASS=NDSP_VALIDATE_ALL
# DEV-003 — NDSP Project Validator
Generated=20260628_152035
ROOT=/home/nawaf511/empire-core-new
HEAD=5c2055b docs(DEV-011): close NDSP core services migration
BRANCH=feature/ndsp-os
== 1) GIT STATUS ==
?? backend/architecture/reports/DEV-012A-PRODUCTION-ROLLOUT-READINESS-CHECK-20260628_152033.md.validator.md
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
PASS=PROJECT_VALIDATOR

== 7) SYSTEMD READINESS CHECK ==
CTL-001_SYSTEMD_UNIT=ndsp-ctl-001-workspace-identity.service
WARN=CTL-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
PASS=CTL-001_SYSTEMD_ACTIVE
PASS=CTL-001_SYSTEMD_ENABLED
PASS=CTL-001_PORT_LISTENING_9081
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1359,fd=32))   
CDS-001_SYSTEMD_UNIT=ndsp-completed_decision.service
WARN=CDS-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
WARN=CDS-001_SYSTEMD_NOT_ACTIVE
WARN=CDS-001_SYSTEMD_NOT_ENABLED
PASS=CDS-001_PORT_LISTENING_9078
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1923,fd=33))   
DGC-001_SYSTEMD_UNIT=ndsp-decision_governance_core.service
WARN=DGC-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
WARN=DGC-001_SYSTEMD_NOT_ACTIVE
WARN=DGC-001_SYSTEMD_NOT_ENABLED
PASS=DGC-001_PORT_LISTENING_9079
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1939,fd=32))   
BOT-001_SYSTEMD_UNIT=ndsp-bot_execution.service
WARN=BOT-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
WARN=BOT-001_SYSTEMD_NOT_ACTIVE
WARN=BOT-001_SYSTEMD_NOT_ENABLED
PASS=BOT-001_PORT_LISTENING_9080
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1930,fd=32))   

== 8) LOCAL ENDPOINT READINESS CHECK ==
PASS=CTL-001_health_HTTP_OK http://127.0.0.1:9081/health
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","product":"SYS-001","domain":"Operating System","version":"1.0.0","release":"REL-1.1","uptime_seconds":2563,"timestamp":"2026-06-28T13:20:39.726Z","status":"UP"}
PASS=CTL-001_version_HTTP_OK http://127.0.0.1:9081/version
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","version":"1.0.0","build":"1.0.0","release":"REL-1.1","git_commit":null,"timestamp":"2026-06-28T13:20:39.778Z"}
PASS=CTL-001_about_HTTP_OK http://127.0.0.1:9081/about
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","component":"CTL-001","product":"SYS-001","domain":"Operating System","owner":"NDSP Engineering","description":"NDSP-OS workspace identity service. Provides identity, health, version and about endpoints.","documentation_version":"1.0.0","framework":{"id":"ENG-001","name":"NDSP Service Framework","version":"1.0.0"},"timestamp":"2026-06-28T13:20:39.806Z"}
PASS=CDS-001_health_HTTP_OK http://127.0.0.1:9078/health
{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T13:20:39.887Z","database":true}
PASS=CDS-001_version_HTTP_OK http://127.0.0.1:9078/version
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=CDS-001_about_HTTP_OK http://127.0.0.1:9078/about
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","description":"Official NDSP completed decision source of truth.","role":"single_source_of_truth_for_completed_decisions","decision_policy":"decision_support_only","not_financial_advice":true,"not_execution_instruction":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard metadata endpoints."},"endpoints":["GET /health","GET /version","GET /about","GET /api/completed","
PASS=DGC-001_health_HTTP_OK http://127.0.0.1:9079/health
{"ok":true,"service":"ndsp-decision-governance-core","port":9079,"completed_decision_service":{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T13:20:40.056Z","database":true}}
WARN=DGC-001_version_HTTP_NOT_READY http://127.0.0.1:9079/version
WARN=DGC-001_about_HTTP_NOT_READY http://127.0.0.1:9079/about
PASS=BOT-001_health_HTTP_OK http://127.0.0.1:9080/health
{"ok":true,"service":"ndsp-bot-execution-service","product":"NDSP Bot","connected_platform":"NDSP — Nawaf Decision Support Platform","port":9080,"mode":"DRY_RUN","completed_decision_url":"http://127.0.0.1:9078"}
WARN=BOT-001_version_HTTP_NOT_READY http://127.0.0.1:9080/version
WARN=BOT-001_about_HTTP_NOT_READY http://127.0.0.1:9080/about

== 9) NGINX READINESS SCAN ==
PASS=NGINX_BINARY_EXISTS
WARN=NGINX_CONFIG_TEST_FAILED
2026/06/28 15:20:40 [warn] 286917#286917: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
2026/06/28 15:20:40 [emerg] 286917#286917: open() "/run/nginx.pid" failed (13: Permission denied)
nginx: configuration file /etc/nginx/nginx.conf test failed
NGINX_PORT_REFERENCES_SCAN
/etc/nginx/sites-available/bot.ndsp.app:4:    server_name bot.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app:12:    server_name bot.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app:14:    ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/sites-available/bot.ndsp.app:15:    ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;
/etc/nginx/sites-available/bot.ndsp.app:17:    root /var/www/bot.ndsp.app;
/etc/nginx/sites-available/bot.ndsp.app:20:    access_log /var/log/nginx/bot.ndsp.app.access.log;
/etc/nginx/sites-available/bot.ndsp.app:21:    error_log /var/log/nginx/bot.ndsp.app.error.log;
/etc/nginx/sites-available/ndsp:3:    server_name 161.97.144.189; # يمكنك وضع الدومين ndsp.app هنا لاحقاً
/etc/nginx/sites-available/ndsp-trading-bot.conf:6:#     server_name bot.ndsp.app;
/etc/nginx/sites-available/ndsp-trading-bot.conf:17:#     server_name bot.ndsp.app;
/etc/nginx/sites-available/ndsp-trading-bot.conf:19:#     ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/sites-available/ndsp-trading-bot.conf:20:#     ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;
/etc/nginx/sites-available/bot.ndsp.app.conf.disabled.20260611_174628:5:#     server_name bot.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:130:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:137:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:138:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:200:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:203:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:204:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202800:252:    # NDSP launch alias: expose governed live decision quality on api.ndsp.app
/etc/nginx/backup-disabled-20260610_220759/000-my-ndsp-app-latest-only.conf.disabled_20260610_220422:3:    server_name my.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/000-my-ndsp-app-latest-only.conf.disabled_20260610_220422:9:    server_name my.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/000-my-ndsp-app-latest-only.conf.disabled_20260610_220422:11:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/000-my-ndsp-app-latest-only.conf.disabled_20260610_220422:12:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:109:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:116:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:117:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:179:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:182:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_register_conf_d_exact_20260609_155436:183:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:109:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:116:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:117:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:179:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:182:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_fix_password_reset_20260610_202313:183:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:58:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:63:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:64:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:143:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:150:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:151:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:213:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:216:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_force_pwd_all_20260610_214454:217:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/bot.ndsp.app.bak_20260610_220658:3:    server_name bot.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/bot.ndsp.app.bak_20260610_220658:27:    ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/bot.ndsp.app.bak_20260610_220658:28:    ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:109:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:112:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:113:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:175:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:178:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_admin_basic_auth_20260608_190942:179:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:136:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:143:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:144:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:206:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:209:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_clean_pwd_20260610_214406:210:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:65:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:70:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:71:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:171:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:178:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:179:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:262:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:265:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_20260610_215823:266:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:116:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:123:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:124:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:186:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:189:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_standalone_20260610_202941:190:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:116:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:123:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:124:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:186:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:189:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_pwd_reset_20260610_214323:190:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:37:    server_name ndsp.app www.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:42:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:43:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:130:    server_name admin.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:137:    ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:138:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:200:    server_name api.ndsp.app;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:203:ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/backup-disabled-20260610_220759/ndsp.conf.bak_deep_fix_20260610_202622:204:    ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.broken_before_register_repair_20260618_054043.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v6_20260618_054914.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v3_20260618_054418.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:73:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:77:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:81:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_public_landing_20260618_045740.disabled_prelaunch_20260618_060236:85:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:73:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:77:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:81:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_landing_only_20260618_044157.disabled_prelaunch_20260618_060236:85:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v4_20260618_054554.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_rebuild_register_proxy_v5_20260618_054743.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:3:    server_name my.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:8:return 301 https://my.ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:127:    server_name my.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:133:ssl_certificate /etc/letsencrypt/live/my.ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:134:    ssl_certificate_key /etc/letsencrypt/live/my.ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:259:        return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:271:        return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-my-ndsp-app-canonical-only.conf.bak_exact_root_20260618_043550:275:        return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/bot.ndsp.app.disabled.20260611_174628:4:#     server_name bot.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/bot.ndsp.app.disabled.20260611_174628:27:#     ssl_certificate /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/bot.ndsp.app.disabled.20260611_174628:28:#     ssl_certificate_key /etc/letsencrypt/live/bot.ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:78:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:82:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_same_origin_register_20260618_053911.disabled_prelaunch_20260618_060236:86:#         return 302 https://my.ndsp.app/login;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:4:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:5:#     return 301 https://ndsp.app$request_uri;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:23:#     server_name ndsp.app www.ndsp.app;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:25:#     ssl_certificate /etc/letsencrypt/live/ndsp.app/fullchain.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:26:#     ssl_certificate_key /etc/letsencrypt/live/ndsp.app/privkey.pem;
/etc/nginx/ndsp-disabled-conf-20260618_062549/000-ndsp-app-public-canonical-only.conf.bak_register_v2_20260618_054216.disabled_prelaunch_20260618_060236:74:#         return 302 https://my.ndsp.app/login;

== 10) PRODUCTION SAFETY SCAN ==
SAFETY_SCAN=backend/services/completed_decision
backend/services/completed_decision/contracts/CDS-001-ENG-001-ADAPTER-CONTRACT.md:37:NOT_BUY_SELL_RECOMMENDATION=YES
backend/services/completed_decision/main.cjs:201:      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
backend/services/completed_decision/main.cjs:218:      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
backend/services/completed_decision/main.cjs:234:      ORDER BY COALESCE(published_at, completed_at, created_at) DESC
backend/services/completed_decision/main.cjs:263:      ORDER BY created_at ASC, id ASC
backend/services/completed_decision/framework-adapter.cjs:47:      decision_policy: 'decision_support_only',
backend/services/completed_decision/framework-adapter.cjs:48:      not_financial_advice: true,
backend/services/completed_decision/node_modules/pg-types/lib/builtins.js:4: SELECT json_object_agg(UPPER(PT.typname), PT.oid::int4 ORDER BY pt.oid)
backend/services/completed_decision/MIGRATION_STATUS.md:37:NOT_BUY_SELL_RECOMMENDATION=YES
SAFETY_SCAN=backend/services/decision_governance_core
backend/services/decision_governance_core/contracts/DGC-001-ENG-001-ADAPTER-CONTRACT.md:27:NOT_BUY_SELL_RECOMMENDATION=YES
backend/services/decision_governance_core/framework-adapter.cjs:47:      decision_policy: 'decision_support_only',
backend/services/decision_governance_core/framework-adapter.cjs:48:      not_financial_advice: true,
backend/services/decision_governance_core/framework-adapter.cjs:49:      not_buy_sell_recommendation: true,
backend/services/decision_governance_core/MIGRATION_STATUS.md:35:NOT_BUY_SELL_RECOMMENDATION=YES
SAFETY_SCAN=backend/services/bot_execution
backend/services/bot_execution/contracts/BOT-001-ENG-001-ADAPTER-CONTRACT.md:23:NO_EXTERNAL_ORDER_ROUTING_DURING_MIGRATION=YES
backend/services/bot_execution/framework-adapter.cjs:48:      not_financial_advice: true,
backend/services/bot_execution/framework-adapter.cjs:49:      not_buy_sell_recommendation: true,
backend/services/bot_execution/framework-adapter.cjs:51:      dry_run_required_during_migration: true,
backend/services/bot_execution/MIGRATION_STATUS.md:34:NO_EXTERNAL_ORDER_ROUTING_DURING_MIGRATION=YES

== 11) WRITE ARCH REPORT ==
