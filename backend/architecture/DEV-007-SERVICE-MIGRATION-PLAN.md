# DEV-007 — NDSP Service Migration Plan

Generated: 20260628_054150
Branch: feature/ndsp-os
Head: fdabdca chore(DEV-005): make validator zero-warning clean

## Current State

```text
BOT-001 | port=9080 | framework=LEGACY | path=backend/services/bot_execution | name=NDSP Bot Execution Service
CDS-001 | port=9078 | framework=LEGACY | path=backend/services/completed_decision | name=Completed Decision Service
CTL-001 | port=9081 | framework=ENG-001 | path=backend/services/ctl-001-workspace-identity | name=Workspace Identity Service
DGC-001 | port=9079 | framework=LEGACY | path=backend/services/decision_governance_core | name=Decision Governance Core
```

## Migration Order

```text
1. CDS-001 Completed Decision Service
   Reason: This is the SSOT output contract. It must be stabilized first.

2. DGC-001 Decision Governance Core
   Reason: Governance validates and explains decisions. It depends on stable completed-decision contracts.

3. BOT-001 NDSP Bot Execution Service
   Reason: Bot must remain last because it consumes completed decisions and must not drive architecture.

4. CTL-001 Workspace Identity
   Reason: Already framework-compliant. Use as reference implementation.
```

## Non-Negotiable Migration Rules

```text
NO_BEHAVIOR_BREAK=YES
PRESERVE_SERVICE_ID=YES
PRESERVE_PUBLIC_CONTRACTS=YES
PRESERVE_PORTS_UNLESS_EXPLICITLY_APPROVED=YES
ONE_SERVICE_PER_COMMIT=YES
VALIDATOR_MUST_PASS_AFTER_EACH_SERVICE=YES
NO_REAL_ENV_FILES=YES
NO_SECRETS_IN_GIT=YES
NO_BOT_FIRST_MIGRATION=YES
```

## Required Migration Pattern Per Legacy Service

```text
1. Snapshot current routes / health / expected payloads.
2. Add framework bootstrap using backend/framework createNDSPService.
3. Preserve old service behavior behind same service ID.
4. Add /health, /version, /about consistency if missing.
5. Keep legacy adapter until tests pass.
6. Update service.yaml framework from LEGACY to ENG-001 only after validation.
7. Run ./backend/tools/ndsp_project_validator.sh.
8. Commit only the migrated service and its report.
```

## DEV-008 Candidate

```text
DEV-008 — Migrate CDS-001 Completed Decision Service to ENG-001 framework
```

## Safety Result

```text
PLAN_ONLY=YES
NO_SERVICE_CODE_CHANGED=YES
VALIDATOR_BEFORE_PLAN=PASS
```
