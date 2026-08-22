# DEV-012E — Local Health + Process Ownership Check

Generated: 20260628_152910
Branch: feature/ndsp-os
Head: cc1e313 ops(DEV-012D): install systemd units without restart
Previous Report: /home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012D-INSTALL-SYSTEMD-UNITS-NO-RESTART-20260628_152602.md

## Safety

NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SERVICE_RESTART=YES
NO_SYSTEMD_ENABLE=YES
NO_NGINX_CHANGE=YES
READ_ONLY_CHECK=YES

## Summary

FAIL_COUNT=0
WARN_COUNT=13

READINESS=READY_FOR_CONTROLLED_SYSTEMD_ADOPTION
FINAL_STATUS=DEV012E_READY_WITH_REVIEW

## Ownership Notes
- CDS-001 adoption required: port 9078 is listening by PID 1923 but ndsp-completed_decision.service is inactive.
- DGC-001 adoption required: port 9079 is listening by PID 1939 but ndsp-decision_governance_core.service is inactive.
- BOT-001 adoption required: port 9080 is listening by PID 1930 but ndsp-bot_execution.service is inactive.

## Important Interpretation

Some services may be healthy on their ports but not owned by systemd yet.
That means the next step is controlled adoption, not nginx exposure.

## Next Step
DEV-012F — controlled systemd adoption for CDS then DGC then BOT, one service at a time.

## Raw Run Report
/home/nawaf511/ndsp_launch_reports/NDSP_DEV012E_LOCAL_HEALTH_PROCESS_OWNERSHIP_CHECK_FIX_20260628_152910.md
# DEV-012E — Local Health + Process Ownership Check — FIXED
ROOT=/home/nawaf511/empire-core-new
HEAD=cc1e313 ops(DEV-012D): install systemd units without restart
BRANCH=feature/ndsp-os
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012E_LOCAL_HEALTH_PROCESS_OWNERSHIP_CHECK_FIX_20260628_152910.md
REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012E-LOCAL-HEALTH-PROCESS-OWNERSHIP-CHECK-20260628_152910.md

== 1) SAFETY ==
NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SERVICE_RESTART=YES
NO_SYSTEMD_ENABLE=YES
NO_NGINX_CHANGE=YES
READ_ONLY_CHECK=YES

== 2) QUARANTINE UNTRACKED apps/user-portal IF EXISTS ==
PASS=QUARANTINED_NONE

== 3) CLEAN STATUS CHECK ==

PASS=WORKTREE_CLEAN

== 4) VERIFY DEV-012D EXISTS ==
PASS=DEV012D_REPORT_FOUND=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012D-INSTALL-SYSTEMD-UNITS-NO-RESTART-20260628_152602.md

== 5) LOCAL SERVICE HEALTH AND PROCESS OWNERSHIP ==
CTL-001_UNIT=ndsp-ctl-001-workspace-identity.service
CTL-001_PORT=9081
PASS=CTL-001_UNIT_INSTALLED
PASS=CTL-001_SYSTEMD_ACTIVE
CTL-001_SYSTEMD_MAINPID=1359
PASS=CTL-001_SYSTEMD_ENABLED
PASS=CTL-001_PORT_LISTENING_9081
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1359,fd=32))   
CTL-001_PORT_PID=1359
PASS=CTL-001_PORT_OWNED_BY_SYSTEMD_UNIT
PASS=CTL-001_health_HTTP_OK=http://127.0.0.1:9081/health
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","product":"SYS-001","domain":"Operating System","version":"1.0.0","release":"REL-1.1","uptime_seconds":3075,"timestamp":"2026-06-28T13:29:11.403Z","status":"UP"}
PASS=CTL-001_version_HTTP_OK=http://127.0.0.1:9081/version
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","version":"1.0.0","build":"1.0.0","release":"REL-1.1","git_commit":null,"timestamp":"2026-06-28T13:29:11.452Z"}
PASS=CTL-001_about_HTTP_OK=http://127.0.0.1:9081/about
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","component":"CTL-001","product":"SYS-001","domain":"Operating System","owner":"NDSP Engineering","description":"NDSP-OS workspace identity service. Provides identity, health, version and about endpoints.","documentation_version":"1.0.0","framework":{"id":"ENG-001","name":"NDSP Service Framework","version":"1.0.0"},"timestamp":"2026-06-28T13:29:11.501Z"}
CDS-001_UNIT=ndsp-completed_decision.service
CDS-001_PORT=9078
PASS=CDS-001_UNIT_INSTALLED
WARN=CDS-001_SYSTEMD_NOT_ACTIVE
WARN=CDS-001_SYSTEMD_NOT_ENABLED
PASS=CDS-001_PORT_LISTENING_9078
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1923,fd=33))   
CDS-001_PORT_PID=1923
WARN=CDS-001_PORT_LISTENING_BUT_UNIT_INACTIVE_ADOPTION_REQUIRED
PASS=CDS-001_health_HTTP_OK=http://127.0.0.1:9078/health
{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T13:29:11.780Z","database":true}
PASS=CDS-001_version_HTTP_OK=http://127.0.0.1:9078/version
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=CDS-001_about_HTTP_OK=http://127.0.0.1:9078/about
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","description":"Official NDSP completed decision source of truth.","role":"single_source_of_truth_for_completed_decisions","decision_policy":"decision_support_only","not_financial_advice":true,"not_execution_instruction":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard
DGC-001_UNIT=ndsp-decision_governance_core.service
DGC-001_PORT=9079
PASS=DGC-001_UNIT_INSTALLED
WARN=DGC-001_SYSTEMD_NOT_ACTIVE
WARN=DGC-001_SYSTEMD_NOT_ENABLED
PASS=DGC-001_PORT_LISTENING_9079
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1939,fd=32))   
DGC-001_PORT_PID=1939
WARN=DGC-001_PORT_LISTENING_BUT_UNIT_INACTIVE_ADOPTION_REQUIRED
PASS=DGC-001_health_HTTP_OK=http://127.0.0.1:9079/health
{"ok":true,"service":"ndsp-decision-governance-core","port":9079,"completed_decision_service":{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T13:29:12.110Z","database":true}}
WARN=DGC-001_version_HTTP_NOT_READY=http://127.0.0.1:9079/version
WARN=DGC-001_about_HTTP_NOT_READY=http://127.0.0.1:9079/about
BOT-001_UNIT=ndsp-bot_execution.service
BOT-001_PORT=9080
PASS=BOT-001_UNIT_INSTALLED
WARN=BOT-001_SYSTEMD_NOT_ACTIVE
WARN=BOT-001_SYSTEMD_NOT_ENABLED
PASS=BOT-001_PORT_LISTENING_9080
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1930,fd=32))   
BOT-001_PORT_PID=1930
WARN=BOT-001_PORT_LISTENING_BUT_UNIT_INACTIVE_ADOPTION_REQUIRED
PASS=BOT-001_health_HTTP_OK=http://127.0.0.1:9080/health
{"ok":true,"service":"ndsp-bot-execution-service","product":"NDSP Bot","connected_platform":"NDSP — Nawaf Decision Support Platform","port":9080,"mode":"DRY_RUN","completed_decision_url":"http://127.0.0.1:9078"}
WARN=BOT-001_version_HTTP_NOT_READY=http://127.0.0.1:9080/version
WARN=BOT-001_about_HTTP_NOT_READY=http://127.0.0.1:9080/about

== 6) DEPENDENCY ROUTE LOCAL CHECK ==
PASS=CDS-001_completed_latest_HTTP_OK=http://127.0.0.1:9078/api/completed/latest
{"ok":true,"source":"completed_decision_service","decision":{"id":"CD-9DE55F6380381D8E","symbol":"ETHUSDT","market":"CRYPTO","decision_state":"Completed","decision_quality":88,"scenario_state":"UNDER_MONITORING","direction_context":"Governed completed context","levels":{"activation":"3400","arrival":"3650","review_zone":"3300-3340","invalidation":"3180","nmp_zone":"3410-3440"},"risk_status":"CAUTION","devil_advocate_status":"PASSED","visibility":"private","completed_at":"2026-06-27T19:47:44.784Z
PASS=DGC-001_governance_evaluate_HTTP_OK
{"ok":true,"source":"decision_governance_core","validation":{"ok":true,"errors":[],"warnings":[],"symbol":"BTCUSDT","quality":85},"decision_state":"Completed","publishable":true,"rule":"Decision is official only after Completed Decision Service accepts it."}

== 7) WRITE REPORT ==
