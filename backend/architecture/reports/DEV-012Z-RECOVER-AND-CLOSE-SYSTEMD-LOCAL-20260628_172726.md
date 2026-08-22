# DEV-012Z — Recover And Close Systemd Local Rollout

Generated: 20260628_172726
Branch: feature/ndsp-os
Head: 4155074 test(DEV-012E): check local health and process ownership

## Summary

FAIL_COUNT=6
WARN_COUNT=5
NGINX_OK=1

FINAL_STATUS=DEV012_SYSTEMD_LOCAL_BLOCKED

## Backup Directory
/home/nawaf511/ndsp_systemd_backups/dev012_recover_20260628_172726

## Raw Run Report
/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_RECOVER_AND_CLOSE_SYSTEMD_LOCAL_20260628_172726.md
# DEV-012Z — Recover And Close Systemd Local Rollout
ROOT=/home/nawaf511/empire-core-new
HEAD=4155074 test(DEV-012E): check local health and process ownership
BRANCH=feature/ndsp-os
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012_RECOVER_AND_CLOSE_SYSTEMD_LOCAL_20260628_172726.md
REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012Z-RECOVER-AND-CLOSE-SYSTEMD-LOCAL-20260628_172726.md
BACKUP_DIR=/home/nawaf511/ndsp_systemd_backups/dev012_recover_20260628_172726

== 1) QUARANTINE apps/user-portal ==
PASS=QUARANTINED_apps_user_portal=/home/nawaf511/empire-core-new/backend/runtime/quarantine/apps-user-portal-20260628_172726/user-portal

== 2) CLEAN STATUS ==

PASS=WORKTREE_CLEAN

== 3) CTL PRECHECK ==
PASS=CTL_ACTIVE
PASS=CTL-001_health_HTTP_OK=http://127.0.0.1:9081/health
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","product":"SYS-001","domain":"Operating System","version":"1.0.0","release":"REL-1.1","uptime_seconds":10170,"timestamp":"2026-06-28T15:27:26.308Z","status":"UP"}
PASS=CTL-001_version_HTTP_OK=http://127.0.0.1:9081/version
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","version":"1.0.0","build":"1.0.0","release":"REL-1.1","git_commit":null,"timestamp":"2026-06-28T15:27:26.346Z"}
PASS=CTL-001_about_HTTP_OK=http://127.0.0.1:9081/about
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","component":"CTL-001","product":"SYS-001","domain":"Operating System","owner":"NDSP Engineering","description":"NDSP-OS workspace identity service. Provides identity, health, version and about endpoints.","documentation_version":"1.0.0","framework":{"id":"ENG-001","name":"NDSP Service Framework","version":"1.0.0"},"timestamp":"2026-06-28T15:27:26.378Z"}

== 4) ADOPT CDS DGC BOT ==

== ADOPT CDS-001 ==
CDS-001_UNIT=ndsp-completed_decision.service
CDS-001_PORT=9078
CDS-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/completed_decision/systemd/ndsp-completed_decision.service
CDS-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-completed_decision.service
PASS=CDS-001_REPO_UNIT_TYPE_SIMPLE
PASS=CDS-001_INSTALLED_UNIT_REFRESHED=/etc/systemd/system/ndsp-completed_decision.service
CDS-001_BEFORE_PORT_PID=433889
CDS-001_BEFORE_MAINPID=1135350
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=433889,fd=33))                                                                                                                                                                                                                       
WARN=CDS-001_STOPPING_EXISTING_SYSTEMD_STATE
WARN=CDS-001_KILLING_PORT_OWNER=433889
 433889 nawaf511    01:45:53 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs
PASS=CDS-001_PORT_FREE_BEFORE_START=9078
PASS=CDS-001_SYSTEMD_ACTIVE
PASS=CDS-001_PORT_LISTENING=9078
CDS-001_AFTER_MAINPID=0
CDS-001_AFTER_PORT_PID=1139916
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1139916,fd=33))                                                                                                                                                                                                                      
FAIL=CDS-001_PORT_NOT_OWNED_BY_SYSTEMD
CDS-001_STATUS_BEGIN
● ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service
     Loaded: loaded (/etc/systemd/system/ndsp-completed_decision.service; disabled; preset: enabled)
     Active: active (running) since Sun 2026-06-28 17:28:05 CEST; 20ms ago
   Main PID: 1140036 (node)
      Tasks: 7 (limit: 28792)
     Memory: 4.6M (peak: 4.6M)
        CPU: 17ms
     CGroup: /system.slice/ndsp-completed_decision.service
             └─1140036 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs

يونيو 28 17:28:02 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:28:02 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:28:05 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1.
يونيو 28 17:28:05 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
CDS-001_STATUS_END
CDS-001_JOURNAL_BEGIN
يونيو 28 17:26:52 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1745.
يونيو 28 17:26:52 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:26:52 vmi2934783 node[1130939]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:26:52 vmi2934783 node[1130939]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:26:52 vmi2934783 node[1130939]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:26:52 vmi2934783 node[1130939]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:26:52 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:26:52 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:26:55 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1746.
يونيو 28 17:26:55 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:26:56 vmi2934783 node[1132076]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:26:56 vmi2934783 node[1132076]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:26:56 vmi2934783 node[1132076]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:26:56 vmi2934783 node[1132076]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:26:56 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:26:56 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:26:59 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1747.
يونيو 28 17:26:59 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:00 vmi2934783 node[1132337]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:00 vmi2934783 node[1132337]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:00 vmi2934783 node[1132337]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:00 vmi2934783 node[1132337]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:00 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:00 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:03 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1748.
يونيو 28 17:27:03 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:03 vmi2934783 node[1132569]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:03 vmi2934783 node[1132569]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:03 vmi2934783 node[1132569]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:03 vmi2934783 node[1132569]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:03 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:03 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:06 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1749.
يونيو 28 17:27:06 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:07 vmi2934783 node[1132825]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:07 vmi2934783 node[1132825]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:07 vmi2934783 node[1132825]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:07 vmi2934783 node[1132825]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:07 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:07 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:10 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1750.
يونيو 28 17:27:10 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:10 vmi2934783 node[1133049]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:10 vmi2934783 node[1133049]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:10 vmi2934783 node[1133049]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:10 vmi2934783 node[1133049]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:10 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:10 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:13 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1751.
يونيو 28 17:27:13 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:14 vmi2934783 node[1133283]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:14 vmi2934783 node[1133283]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:14 vmi2934783 node[1133283]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:14 vmi2934783 node[1133283]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:14 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:14 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:17 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1752.
يونيو 28 17:27:17 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:17 vmi2934783 node[1134420]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:17 vmi2934783 node[1134420]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:17 vmi2934783 node[1134420]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:17 vmi2934783 node[1134420]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:17 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:17 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:21 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1753.
يونيو 28 17:27:21 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:21 vmi2934783 node[1134655]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:21 vmi2934783 node[1134655]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:21 vmi2934783 node[1134655]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:21 vmi2934783 node[1134655]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:21 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:21 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:24 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1754.
يونيو 28 17:27:24 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:24 vmi2934783 node[1134885]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:27:24 vmi2934783 node[1134885]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:27:24 vmi2934783 node[1134885]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:27:24 vmi2934783 node[1134885]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:27:25 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:27:25 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:27:28 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1.
يونيو 28 17:27:28 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:27:28 vmi2934783 systemd[1]: Stopping ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service...
يونيو 28 17:27:28 vmi2934783 systemd[1]: ndsp-completed_decision.service: Deactivated successfully.
يونيو 28 17:27:28 vmi2934783 systemd[1]: Stopped ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:28:01 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:28:02 vmi2934783 node[1139699]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:28:02 vmi2934783 node[1139699]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:28:02 vmi2934783 node[1139699]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:28:02 vmi2934783 node[1139699]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:28:02 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:28:02 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
يونيو 28 17:28:05 vmi2934783 systemd[1]: ndsp-completed_decision.service: Scheduled restart job, restart counter is at 1.
يونيو 28 17:28:05 vmi2934783 systemd[1]: Started ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service.
يونيو 28 17:28:05 vmi2934783 node[1140036]: [NDSP] Completed Decision Service failed to initialize: Error: SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string
يونيو 28 17:28:05 vmi2934783 node[1140036]:     at /home/nawaf511/empire-core-new/backend/services/completed_decision/node_modules/pg-pool/index.js:45:11
يونيو 28 17:28:05 vmi2934783 node[1140036]:     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
يونيو 28 17:28:05 vmi2934783 node[1140036]:     at async initDb (/home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs:63:3)
يونيو 28 17:28:05 vmi2934783 systemd[1]: ndsp-completed_decision.service: Main process exited, code=exited, status=1/FAILURE
يونيو 28 17:28:05 vmi2934783 systemd[1]: ndsp-completed_decision.service: Failed with result 'exit-code'.
CDS-001_JOURNAL_END

== ADOPT DGC-001 ==
DGC-001_UNIT=ndsp-decision_governance_core.service
DGC-001_PORT=9079
DGC-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service
DGC-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-decision_governance_core.service
PASS=DGC-001_REPO_UNIT_TYPE_SIMPLE
PASS=DGC-001_INSTALLED_UNIT_REFRESHED=/etc/systemd/system/ndsp-decision_governance_core.service
DGC-001_BEFORE_PORT_PID=1939
DGC-001_BEFORE_MAINPID=0
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1939,fd=32))                                                                                                                                                                                                                         
WARN=DGC-001_KILLING_PORT_OWNER=1939
   1939 nawaf511    02:50:41 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/decision_governance_core/main.cjs
PASS=DGC-001_PORT_FREE_BEFORE_START=9079
PASS=DGC-001_SYSTEMD_ACTIVE
PASS=DGC-001_PORT_LISTENING=9079
DGC-001_AFTER_MAINPID=1144808
DGC-001_AFTER_PORT_PID=1144808
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1144808,fd=32))                                                                                                                                                                                                                      
PASS=DGC-001_PORT_OWNED_BY_SYSTEMD
PASS=DGC-001_health_HTTP_OK=http://127.0.0.1:9079/health
{"ok":true,"service":"ndsp-decision-governance-core","port":9079,"completed_decision_service":{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T15:28:41.981Z","database":true}}
PASS=DGC-001_version_HTTP_OK=http://127.0.0.1:9079/version
{"ok":true,"service":"DGC-001","name":"Decision Governance Core","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"DGC preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=DGC-001_about_HTTP_OK=http://127.0.0.1:9079/about
{"ok":true,"service":"DGC-001","name":"Decision Governance Core","description":"Official NDSP decision governance validation service.","role":"governance_validation_before_completed_decision","decision_policy":"decision_support_only","not_financial_advice":true,"not_buy_sell_recommendation":true,"not_execution_instruction":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"DGC preserves existing Express 
PASS=DGC-001_ADOPTED_OK

== ADOPT BOT-001 ==
BOT-001_UNIT=ndsp-bot_execution.service
BOT-001_PORT=9080
BOT-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/bot_execution/systemd/ndsp-bot_execution.service
BOT-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-bot_execution.service
PASS=BOT-001_REPO_UNIT_TYPE_SIMPLE
PASS=BOT-001_INSTALLED_UNIT_REFRESHED=/etc/systemd/system/ndsp-bot_execution.service
BOT-001_BEFORE_PORT_PID=1930
BOT-001_BEFORE_MAINPID=0
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1930,fd=32))                                                                                                                                                                                                                         
WARN=BOT-001_KILLING_PORT_OWNER=1930
   1930 nawaf511    02:51:16 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/bot_execution/main.cjs
PASS=BOT-001_PORT_FREE_BEFORE_START=9080
PASS=BOT-001_SYSTEMD_ACTIVE
PASS=BOT-001_PORT_LISTENING=9080
BOT-001_AFTER_MAINPID=1148881
BOT-001_AFTER_PORT_PID=1148881
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1148881,fd=32))                                                                                                                                                                                                                      
PASS=BOT-001_PORT_OWNED_BY_SYSTEMD
PASS=BOT-001_health_HTTP_OK=http://127.0.0.1:9080/health
{"ok":true,"service":"ndsp-bot-execution-service","product":"NDSP Bot","connected_platform":"NDSP — Nawaf Decision Support Platform","port":9080,"mode":"DRY_RUN","completed_decision_url":"http://127.0.0.1:9078"}
PASS=BOT-001_version_HTTP_OK=http://127.0.0.1:9080/version
{"ok":true,"service":"BOT-001","name":"NDSP Bot Execution Service","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"BOT preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=BOT-001_about_HTTP_OK=http://127.0.0.1:9080/about
{"ok":true,"service":"BOT-001","name":"NDSP Bot Execution Service","description":"NDSP bot execution boundary service.","role":"bot_execution_boundary_after_completed_decision","decision_policy":"execution_boundary_only_after_governed_completed_decision","not_financial_advice":true,"not_buy_sell_recommendation":true,"not_manual_execution_instruction":true,"dry_run_required_during_migration":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"
PASS=BOT-001_ADOPTED_OK

== 5) ENABLE SERVICES ==
WARN=ENABLE_SKIPPED_DUE_TO_FAILURES

== 6) FINAL HEALTH ==
PASS=CTL-001_health_final_HTTP_OK=http://127.0.0.1:9081/health
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","product":"SYS-001","domain":"Operating System","version":"1.0.0","release":"REL-1.1","uptime_seconds":10281,"timestamp":"2026-06-28T15:29:17.855Z","status":"UP"}
PASS=CTL-001_version_final_HTTP_OK=http://127.0.0.1:9081/version
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","version":"1.0.0","build":"1.0.0","release":"REL-1.1","git_commit":null,"timestamp":"2026-06-28T15:29:17.883Z"}
PASS=CTL-001_about_final_HTTP_OK=http://127.0.0.1:9081/about
{"ok":true,"service":"CTL-001","service_name":"Workspace Identity","component":"CTL-001","product":"SYS-001","domain":"Operating System","owner":"NDSP Engineering","description":"NDSP-OS workspace identity service. Provides identity, health, version and about endpoints.","documentation_version":"1.0.0","framework":{"id":"ENG-001","name":"NDSP Service Framework","version":"1.0.0"},"timestamp":"2026-06-28T15:29:17.909Z"}
PASS=CDS-001_health_final_HTTP_OK=http://127.0.0.1:9078/health
{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T15:29:17.957Z","database":true}
PASS=CDS-001_version_final_HTTP_OK=http://127.0.0.1:9078/version
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=CDS-001_about_final_HTTP_OK=http://127.0.0.1:9078/about
{"ok":true,"service":"CDS-001","name":"Completed Decision Service","description":"Official NDSP completed decision source of truth.","role":"single_source_of_truth_for_completed_decisions","decision_policy":"decision_support_only","not_financial_advice":true,"not_execution_instruction":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"CDS preserves existing Express routes while exposing ENG-001 standard
PASS=DGC-001_health_final_HTTP_OK=http://127.0.0.1:9079/health
{"ok":true,"service":"ndsp-decision-governance-core","port":9079,"completed_decision_service":{"ok":true,"service":"ndsp-completed-decision-service","port":9078,"time":"2026-06-28T15:29:18.068Z","database":true}}
PASS=DGC-001_version_final_HTTP_OK=http://127.0.0.1:9079/version
{"ok":true,"service":"DGC-001","name":"Decision Governance Core","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"DGC preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=DGC-001_about_final_HTTP_OK=http://127.0.0.1:9079/about
{"ok":true,"service":"DGC-001","name":"Decision Governance Core","description":"Official NDSP decision governance validation service.","role":"governance_validation_before_completed_decision","decision_policy":"decision_support_only","not_financial_advice":true,"not_buy_sell_recommendation":true,"not_execution_instruction":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"DGC preserves existing Express 
PASS=BOT-001_health_final_HTTP_OK=http://127.0.0.1:9080/health
{"ok":true,"service":"ndsp-bot-execution-service","product":"NDSP Bot","connected_platform":"NDSP — Nawaf Decision Support Platform","port":9080,"mode":"DRY_RUN","completed_decision_url":"http://127.0.0.1:9078"}
PASS=BOT-001_version_final_HTTP_OK=http://127.0.0.1:9080/version
{"ok":true,"service":"BOT-001","name":"NDSP Bot Execution Service","version":"1.0.0","build":"1.0.0","framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"transitional_express_adapter","note":"BOT preserves existing Express routes while exposing ENG-001 standard metadata endpoints."}}
PASS=BOT-001_about_final_HTTP_OK=http://127.0.0.1:9080/about
{"ok":true,"service":"BOT-001","name":"NDSP Bot Execution Service","description":"NDSP bot execution boundary service.","role":"bot_execution_boundary_after_completed_decision","decision_policy":"execution_boundary_only_after_governed_completed_decision","not_financial_advice":true,"not_buy_sell_recommendation":true,"not_manual_execution_instruction":true,"dry_run_required_during_migration":true,"framework":{"id":"ENG-001","factory":"createNDSPService","factory_available":true,"migration_mode":"
PASS=CDS-001_completed_latest_HTTP_OK=http://127.0.0.1:9078/api/completed/latest
{"ok":true,"source":"completed_decision_service","decision":{"id":"CD-9DE55F6380381D8E","symbol":"ETHUSDT","market":"CRYPTO","decision_state":"Completed","decision_quality":88,"scenario_state":"UNDER_MONITORING","direction_context":"Governed completed context","levels":{"activation":"3400","arrival":"3650","review_zone":"3300-3340","invalidation":"3180","nmp_zone":"3410-3440"},"risk_status":"CAUTION","devil_advocate_status":"PASSED","visibility":"private","completed_at":"2026-06-27T19:47:44.784Z
PASS=DGC-001_governance_evaluate_HTTP_OK

== 7) FINAL OWNERSHIP ==
CTL-001_UNIT=ndsp-ctl-001-workspace-identity.service
CTL-001_MAINPID=1359
CTL-001_PORT_PID=1359
PASS=CTL-001_ACTIVE
PASS=CTL-001_ENABLED
PASS=CTL-001_OWNERSHIP_OK
CDS-001_UNIT=ndsp-completed_decision.service
CDS-001_MAINPID=0
CDS-001_PORT_PID=1139916
FAIL=CDS-001_NOT_ACTIVE
FAIL=CDS-001_NOT_ENABLED
FAIL=CDS-001_OWNERSHIP_BAD
DGC-001_UNIT=ndsp-decision_governance_core.service
DGC-001_MAINPID=1144808
DGC-001_PORT_PID=1144808
PASS=DGC-001_ACTIVE
FAIL=DGC-001_NOT_ENABLED
PASS=DGC-001_OWNERSHIP_OK
BOT-001_UNIT=ndsp-bot_execution.service
BOT-001_MAINPID=1148881
BOT-001_PORT_PID=1148881
PASS=BOT-001_ACTIVE
FAIL=BOT-001_NOT_ENABLED
PASS=BOT-001_OWNERSHIP_OK

== 8) NGINX TEST ONLY ==
PASS=NGINX_TEST_OK
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

== 9) WRITE REPORT + VALIDATOR ==
# DEV-003 — NDSP Project Validator
Generated=20260628_172919
ROOT=/home/nawaf511/empire-core-new
HEAD=4155074 test(DEV-012E): check local health and process ownership
BRANCH=feature/ndsp-os
== 1) GIT STATUS ==
?? backend/architecture/reports/DEV-012Z-RECOVER-AND-CLOSE-SYSTEMD-LOCAL-20260628_172726.md
?? backend/architecture/reports/DEV-012Z-RECOVER-AND-CLOSE-SYSTEMD-LOCAL-20260628_172726.md.validator.md
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
