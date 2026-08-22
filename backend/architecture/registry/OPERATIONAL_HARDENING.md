# NDSP Operational Hardening Registry

Generated: 20260628_175219  
Release: REL-1.2-pre  
Task: DEV-013  
Branch: feature/ndsp-os

## Hardening Rules

1. Runtime files must never be tracked in Git.
2. Real secrets and real environment files must remain outside Git.
3. Example environment files are allowed only when they contain placeholders.
4. Every service must have a unique service_id.
5. Every service must have a unique internal port.
6. Services must expose:
   - /health
   - /version
   - /about
7. Core services must be managed by systemd.
8. Git commits must be scoped and avoid blanket git add.

## Guard Tools

- backend/tools/ndsp/ndsp_repo_guard.sh
- backend/tools/ndsp/ndsp_systemd_guard.sh

## Core Services

| ID | Unit | Port |
|---|---|---:|
| CTL-001 | ndsp-ctl-001-workspace-identity.service | 9081 |
| CDS-001 | ndsp-completed_decision.service | 9078 |
| DGC-001 | ndsp-decision_governance_core.service | 9079 |
| BOT-001 | ndsp-bot_execution.service | 9080 |
