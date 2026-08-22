# DEV-012C — Systemd Local Activation Readiness Report

Generated: 20260628_152421
Branch: feature/ndsp-os
Head: 4f0cff4 docs(DEV-012B): plan controlled production rollout
Previous Plan: /home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012B-CONTROLLED-PRODUCTION-ROLLOUT-PLAN-20260628_152255.md

## Safety

NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SYSTEMD_RELOAD=YES
NO_SYSTEMD_ENABLE=YES
NO_SYSTEMD_DISABLE=YES
NO_NGINX_CHANGE=YES
PLAN_AND_READINESS_ONLY=YES

## Summary

FAIL_COUNT=0
WARN_COUNT=7

READINESS=READY_FOR_MANUAL_SYSTEMD_ACTIVATION
FINAL_STATUS=DEV012C_READY_WITH_REVIEW

## Proposed Commands

# DEV-012C — Proposed Local Activation Commands

Generated: 20260628_152421

These commands are NOT executed by DEV-012C.
Run only after manual review.


## CTL-001

Repository unit:
/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/systemd/ndsp-ctl-001-workspace-identity.service

Install / refresh unit:
sudo cp '/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/systemd/ndsp-ctl-001-workspace-identity.service' '/etc/systemd/system/ndsp-ctl-001-workspace-identity.service'
sudo systemctl daemon-reload
sudo systemctl enable 'ndsp-ctl-001-workspace-identity.service'
sudo systemctl restart 'ndsp-ctl-001-workspace-identity.service'
sudo systemctl status 'ndsp-ctl-001-workspace-identity.service' --no-pager -l
curl -fsS 'http://127.0.0.1:9081/health'
curl -fsS 'http://127.0.0.1:9081/version'
curl -fsS 'http://127.0.0.1:9081/about'

## CDS-001

Repository unit:
/home/nawaf511/empire-core-new/backend/services/completed_decision/systemd/ndsp-completed_decision.service

Install / refresh unit:
sudo cp '/home/nawaf511/empire-core-new/backend/services/completed_decision/systemd/ndsp-completed_decision.service' '/etc/systemd/system/ndsp-completed_decision.service'
sudo systemctl daemon-reload
sudo systemctl enable 'ndsp-completed_decision.service'
sudo systemctl restart 'ndsp-completed_decision.service'
sudo systemctl status 'ndsp-completed_decision.service' --no-pager -l
curl -fsS 'http://127.0.0.1:9078/health'
curl -fsS 'http://127.0.0.1:9078/version'
curl -fsS 'http://127.0.0.1:9078/about'

## DGC-001

Repository unit:
/home/nawaf511/empire-core-new/backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service

Install / refresh unit:
sudo cp '/home/nawaf511/empire-core-new/backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service' '/etc/systemd/system/ndsp-decision_governance_core.service'
sudo systemctl daemon-reload
sudo systemctl enable 'ndsp-decision_governance_core.service'
sudo systemctl restart 'ndsp-decision_governance_core.service'
sudo systemctl status 'ndsp-decision_governance_core.service' --no-pager -l
curl -fsS 'http://127.0.0.1:9079/health'
curl -fsS 'http://127.0.0.1:9079/version'
curl -fsS 'http://127.0.0.1:9079/about'

## BOT-001

Repository unit:
/home/nawaf511/empire-core-new/backend/services/bot_execution/systemd/ndsp-bot_execution.service

Install / refresh unit:
sudo cp '/home/nawaf511/empire-core-new/backend/services/bot_execution/systemd/ndsp-bot_execution.service' '/etc/systemd/system/ndsp-bot_execution.service'
sudo systemctl daemon-reload
sudo systemctl enable 'ndsp-bot_execution.service'
sudo systemctl restart 'ndsp-bot_execution.service'
sudo systemctl status 'ndsp-bot_execution.service' --no-pager -l
curl -fsS 'http://127.0.0.1:9080/health'
curl -fsS 'http://127.0.0.1:9080/version'
curl -fsS 'http://127.0.0.1:9080/about'

## Raw Run Report

/home/nawaf511/ndsp_launch_reports/NDSP_DEV012C_SYSTEMD_LOCAL_ACTIVATION_READINESS_20260628_152421.md
# DEV-012C — Systemd Local Activation Readiness
ROOT=/home/nawaf511/empire-core-new
HEAD=4f0cff4 docs(DEV-012B): plan controlled production rollout
BRANCH=feature/ndsp-os
RUN_REPORT=/home/nawaf511/ndsp_launch_reports/NDSP_DEV012C_SYSTEMD_LOCAL_ACTIVATION_READINESS_20260628_152421.md
REPORT=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012C-SYSTEMD-LOCAL-ACTIVATION-READINESS-20260628_152421.md

== 1) SAFETY ==
NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SYSTEMD_RELOAD=YES
NO_SYSTEMD_ENABLE=YES
NO_SYSTEMD_DISABLE=YES
NO_NGINX_CHANGE=YES
PLAN_AND_READINESS_ONLY=YES

== 2) QUARANTINE UNTRACKED apps/user-portal IF EXISTS ==
PASS=QUARANTINED_NONE

== 3) CLEAN STATUS CHECK ==

PASS=WORKTREE_CLEAN

== 4) VERIFY DEV-012B EXISTS ==
PASS=DEV012B_REPORT_FOUND=/home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012B-CONTROLLED-PRODUCTION-ROLLOUT-PLAN-20260628_152255.md

== 5) SERVICE SYSTEMD INVENTORY ==
CTL-001_PATH=backend/services/ctl-001-workspace-identity
CTL-001_UNIT=ndsp-ctl-001-workspace-identity.service
CTL-001_PORT=9081
CTL-001_FRAMEWORK=ENG-001
PASS=CTL-001_FRAMEWORK_ENG001
PASS=CTL-001_REPO_UNIT_EXISTS=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/systemd/ndsp-ctl-001-workspace-identity.service
PASS=CTL-001_INSTALLED_UNIT_EXISTS=/etc/systemd/system/ndsp-ctl-001-workspace-identity.service
CTL-001_INSTALLED_UNIT_HEAD_BEGIN
[Unit]
Description=NDSP CTL-001 Workspace Identity
After=network.target

[Service]
Type=simple
User=nawaf511
WorkingDirectory=/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity
Environment=NODE_ENV=production
Environment=NDSP_PORT=9081
Environment=NDSP_HOST=127.0.0.1
EnvironmentFile=-/home/nawaf511/empire-core-new/backend/.env
ExecStart=/usr/bin/node /home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/main.cjs
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
CTL-001_INSTALLED_UNIT_HEAD_END
PASS=CTL-001_REPO_UNIT_EXECSTART_PRESENT
PASS=CTL-001_REPO_UNIT_WORKDIR_PRESENT
WARN=CTL-001_PORT_ALREADY_LISTENING_9081
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1359,fd=32))   
CDS-001_PATH=backend/services/completed_decision
CDS-001_UNIT=ndsp-completed_decision.service
CDS-001_PORT=9078
CDS-001_FRAMEWORK=ENG-001
PASS=CDS-001_FRAMEWORK_ENG001
PASS=CDS-001_REPO_UNIT_EXISTS=/home/nawaf511/empire-core-new/backend/services/completed_decision/systemd/ndsp-completed_decision.service
WARN=CDS-001_INSTALLED_UNIT_MISSING=/etc/systemd/system/ndsp-completed_decision.service
PASS=CDS-001_REPO_UNIT_EXECSTART_PRESENT
PASS=CDS-001_REPO_UNIT_WORKDIR_PRESENT
WARN=CDS-001_PORT_ALREADY_LISTENING_9078
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1923,fd=33))   
DGC-001_PATH=backend/services/decision_governance_core
DGC-001_UNIT=ndsp-decision_governance_core.service
DGC-001_PORT=9079
DGC-001_FRAMEWORK=ENG-001
PASS=DGC-001_FRAMEWORK_ENG001
PASS=DGC-001_REPO_UNIT_EXISTS=/home/nawaf511/empire-core-new/backend/services/decision_governance_core/systemd/ndsp-decision_governance_core.service
WARN=DGC-001_INSTALLED_UNIT_MISSING=/etc/systemd/system/ndsp-decision_governance_core.service
PASS=DGC-001_REPO_UNIT_EXECSTART_PRESENT
PASS=DGC-001_REPO_UNIT_WORKDIR_PRESENT
WARN=DGC-001_PORT_ALREADY_LISTENING_9079
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1939,fd=32))   
BOT-001_PATH=backend/services/bot_execution
BOT-001_UNIT=ndsp-bot_execution.service
BOT-001_PORT=9080
BOT-001_FRAMEWORK=ENG-001
PASS=BOT-001_FRAMEWORK_ENG001
PASS=BOT-001_REPO_UNIT_EXISTS=/home/nawaf511/empire-core-new/backend/services/bot_execution/systemd/ndsp-bot_execution.service
WARN=BOT-001_INSTALLED_UNIT_MISSING=/etc/systemd/system/ndsp-bot_execution.service
PASS=BOT-001_REPO_UNIT_EXECSTART_PRESENT
PASS=BOT-001_REPO_UNIT_WORKDIR_PRESENT
WARN=BOT-001_PORT_ALREADY_LISTENING_9080
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1930,fd=32))   

== 6) DEPENDENCY ORDER CHECK ==
PASS=ROLL_OUT_ORDER_CTL_THEN_CDS_THEN_DGC_THEN_BOT
PASS=BOT_LAST_REQUIRED

== 7) WRITE REPORT ==
