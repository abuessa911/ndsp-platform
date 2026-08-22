# DEV-012D — Install Systemd Units Without Restart

Generated: 20260628_152602
Branch: feature/ndsp-os
Head: 1accb4d docs(DEV-012C): prepare systemd local activation readiness
Previous Report: /home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012C-SYSTEMD-LOCAL-ACTIVATION-READINESS-20260628_152421.md

## Safety

NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SERVICE_RESTART=YES
NO_SYSTEMD_ENABLE=YES
NO_SYSTEMD_DISABLE=YES
SYSTEMD_DAEMON_RELOAD_ONLY=YES
NO_NGINX_CHANGE=YES

## Result

FAIL_COUNT=0
WARN_COUNT=0

READINESS=SYSTEMD_UNITS_INSTALLED_FOR_MANUAL_ACTIVATION
FINAL_STATUS=DEV012D_DONE_WITH_REVIEW

## Backup Directory

/home/nawaf511/ndsp_systemd_backups/dev012d_20260628_152602

## Next Step

DEV-012E — local health validation through systemd inventory. Still no nginx exposure.

## Raw Run Report

/home/nawaf511/ndsp_launch_reports/NDSP_DEV012D_INSTALL_SYSTEMD_UNITS_NO_RESTART_20260628_152602.md
# DEV-012D — Install Systemd Units Without Restart
ROOT=/home/nawaf511/empire-core-new
HEAD=1accb4d docs(DEV-012C): prepare systemd local activation readiness
BRANCH=feature/ndsp-os
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012D_INSTALL_SYSTEMD_UNITS_NO_RESTART_20260628_152602.md
REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012D-INSTALL-SYSTEMD-UNITS-NO-RESTART-20260628_152602.md
BACKUP_DIR=/home/nawaf511/ndsp_systemd_backups/dev012d_20260628_152602

== 1) SAFETY ==
NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SERVICE_RESTART=YES
NO_SYSTEMD_ENABLE=YES
NO_SYSTEMD_DISABLE=YES
SYSTEMD_DAEMON_RELOAD_ONLY=YES
NO_NGINX_CHANGE=YES
NO_PRODUCTION_ENDPOINT_CHANGE=YES

== 2) QUARANTINE UNTRACKED apps/user-portal IF EXISTS ==
PASS=QUARANTINED_apps_user_portal=/home/nawaf511/empire-core-new/backend/runtime/quarantine/apps-user-portal-20260628_152602/user-portal

== 3) CLEAN STATUS CHECK ==

PASS=WORKTREE_CLEAN

== 4) VERIFY DEV-012C EXISTS ==
PASS=DEV012C_REPORT_FOUND=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012C-SYSTEMD-LOCAL-ACTIVATION-READINESS-20260628_152421.md

== 5) SUDO CHECK ==
PASS=SUDO_NON_INTERACTIVE_AVAILABLE

== 6) INSTALL / REFRESH UNIT FILES ONLY ==
CTL-001_UNIT=ndsp-ctl-001-workspace-identity.service
CTL-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/systemd/ndsp-ctl-001-workspace-identity.service
CTL-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-ctl-001-workspace-identity.service
CTL-001_PORT=9081
PASS=CTL-001_EXISTING_UNIT_BACKED_UP=/home/nawaf511/ndsp_systemd_backups/dev012d_20260628_152602/ndsp-ctl-001-workspace-identity.service.before_dev012d
PASS=CTL-001_UNIT_INSTALLED_OR_REFRESHED=/etc/systemd/system/ndsp-ctl-001-workspace-identity.service
PASS=CTL-001_PORT_STILL_LISTENING_9081
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1359,fd=32))   
CDS-001_UNIT=ndsp-completed_decision.service
CDS-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/completed_decision/systemd/ndsp-completed_decision.service
CDS-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-completed_decision.service
CDS-001_PORT=9078
PASS=CDS-001_INSTALLED_UNIT_WAS_MISSING
PASS=CDS-001_UNIT_INSTALLED_OR_REFRESHED=/etc/systemd/system/ndsp-completed_decision.service
PASS=CDS-001_PORT_STILL_LISTENING_9078
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1923,fd=33))   
DGC-001_UNIT=ndsp-decision_governance_core.service
DGC-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service
DGC-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-decision_governance_core.service
DGC-001_PORT=9079
PASS=DGC-001_INSTALLED_UNIT_WAS_MISSING
PASS=DGC-001_UNIT_INSTALLED_OR_REFRESHED=/etc/systemd/system/ndsp-decision_governance_core.service
PASS=DGC-001_PORT_STILL_LISTENING_9079
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1939,fd=32))   
BOT-001_UNIT=ndsp-bot_execution.service
BOT-001_REPO_UNIT=/home/nawaf511/empire-core-new/backend/services/bot_execution/systemd/ndsp-bot_execution.service
BOT-001_INSTALLED_UNIT=/etc/systemd/system/ndsp-bot_execution.service
BOT-001_PORT=9080
PASS=BOT-001_INSTALLED_UNIT_WAS_MISSING
PASS=BOT-001_UNIT_INSTALLED_OR_REFRESHED=/etc/systemd/system/ndsp-bot_execution.service
PASS=BOT-001_PORT_STILL_LISTENING_9080
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1930,fd=32))   

== 7) SYSTEMD DAEMON RELOAD ONLY ==
PASS=SYSTEMD_DAEMON_RELOAD_DONE

== 8) VERIFY INSTALLED UNITS ==
PASS=CTL-001_INSTALLED_UNIT_EXISTS=/etc/systemd/system/ndsp-ctl-001-workspace-identity.service
● ndsp-ctl-001-workspace-identity.service - NDSP CTL-001 Workspace Identity
     Loaded: loaded (/etc/systemd/system/ndsp-ctl-001-workspace-identity.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-06-28 14:37:55 CEST; 48min ago
   Main PID: 1359 (node)
      Tasks: 8 (limit: 28792)
     Memory: 25.3M (peak: 37.5M)
        CPU: 3.861s
     CGroup: /system.slice/ndsp-ctl-001-workspace-identity.service
             └─1359 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/main.cjs

يونيو 28 14:37:57 vmi2934783 node[1359]: {"timestamp":"2026-06-28T12:37:56.984Z","level":"info","message":"service_started","service_id":"CTL-001","service_name":"Workspace Identity","component":"CTL-001","host":"127.0.0.1","port":9081}
Warning: journal has been rotated since unit was started and some journal files were not opened due to insufficient permissions, output may be incomplete.
PASS=CDS-001_INSTALLED_UNIT_EXISTS=/etc/systemd/system/ndsp-completed_decision.service
○ ndsp-completed_decision.service - NDSP CDS-001 Completed Decision Service
     Loaded: loaded (/etc/systemd/system/ndsp-completed_decision.service; disabled; preset: enabled)
     Active: inactive (dead)
PASS=DGC-001_INSTALLED_UNIT_EXISTS=/etc/systemd/system/ndsp-decision_governance_core.service
○ ndsp-decision_governance_core.service - NDSP DGC-001 Decision Governance Core
     Loaded: loaded (/etc/systemd/system/ndsp-decision_governance_core.service; disabled; preset: enabled)
     Active: inactive (dead)
PASS=BOT-001_INSTALLED_UNIT_EXISTS=/etc/systemd/system/ndsp-bot_execution.service
○ ndsp-bot_execution.service - NDSP BOT-001 NDSP Bot Execution Service
     Loaded: loaded (/etc/systemd/system/ndsp-bot_execution.service; disabled; preset: enabled)
     Active: inactive (dead)

== 9) VERIFY NO SERVICE ACTION WAS TAKEN ==
NO_SERVICE_START_CONFIRMED=YES
NO_SERVICE_STOP_CONFIRMED=YES
NO_SERVICE_RESTART_CONFIRMED=YES
NO_SYSTEMD_ENABLE_CONFIRMED=YES

== 10) WRITE REPORT ==
