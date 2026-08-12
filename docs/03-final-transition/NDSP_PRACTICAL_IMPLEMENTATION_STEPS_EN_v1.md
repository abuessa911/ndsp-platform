# NDSP Practical Implementation Steps
## Final Practical Steps to Close Planning and Start Implementation

**Project:** NDSP — Nawaf Decision Support Platform  
**Version:** v1.0  
**Date:** 2026-07-06  
**Purpose:** This is the final file before moving to the second tool. It provides ordered practical steps to install the documentation into the project, run audit, lock the real state, take backup, and begin the first safe patch.

---

# 0. Golden Rule

No code modification starts before this sequence is completed:

```txt
1. Install governance and catalog files inside the project.
2. Run Audit.
3. Lock real paths and services.
4. Create V1 Freeze.
5. Run Backup.
6. Execute the first small patch.
7. Run Post Patch Test.
8. Save the report.
```

Any tool that skips these steps should not be allowed to modify the project.

---

# 1. Prepare the Working Folders

Log in to the server and enter the main project path.

> If the project path is different, change `PROJECT_DIR` only.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"

cd "$PROJECT_DIR"

mkdir -p docs/00-build-catalog
mkdir -p docs/01-build-control-pack
mkdir -p docs/02-execution-ready-pack
mkdir -p docs/03-final-transition
mkdir -p docs/04-legal
mkdir -p docs/05-runbooks

mkdir -p scripts/audit
mkdir -p scripts/backup
mkdir -p scripts/tests
mkdir -p scripts/deploy

echo "OK: NDSP docs/scripts folders prepared inside: $PROJECT_DIR"
```

---

# 2. Import Previous Packs Into the Project

Upload the previously prepared ZIP files to the server, for example:

```txt
/tmp/ndsp-docs/
```

Then extract them into the project.

Practical example:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
UPLOAD_DIR="/tmp/ndsp-docs"

cd "$PROJECT_DIR"

mkdir -p "$UPLOAD_DIR"
mkdir -p docs/00-build-catalog docs/01-build-control-pack docs/02-execution-ready-pack docs/03-final-transition
mkdir -p scripts/audit scripts/backup scripts/tests scripts/deploy

# Adjust file names based on what exists in /tmp/ndsp-docs
if [ -f "$UPLOAD_DIR/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_EN_v1.zip" -d docs/00-build-catalog/
fi

if [ -f "$UPLOAD_DIR/NDSP_BUILD_TOOLS_AND_CONTROL_PACK_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_BUILD_TOOLS_AND_CONTROL_PACK_AR_EN_v1.zip" -d docs/01-build-control-pack/
fi

if [ -f "$UPLOAD_DIR/NDSP_EXECUTION_READY_PACK_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_EXECUTION_READY_PACK_AR_EN_v1.zip" -d docs/02-execution-ready-pack/
fi

if [ -f "$UPLOAD_DIR/NDSP_FINAL_PRE_IMPLEMENTATION_TRANSITION_PLAN_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_FINAL_PRE_IMPLEMENTATION_TRANSITION_PLAN_AR_EN_v1.zip" -d docs/03-final-transition/
fi

echo "OK: NDSP documentation packs imported."
```

---

# 3. Extract Audit, Backup, and Test Scripts

After extracting the Execution Ready Pack, copy the scripts to the `scripts` folder.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

find docs/02-execution-ready-pack -type f -name "ndsp_server_and_project_audit_EN.sh" -exec cp -f {} scripts/audit/ \;
find docs/02-execution-ready-pack -type f -name "ndsp_safe_backup_before_patch_EN.sh" -exec cp -f {} scripts/backup/ \;
find docs/02-execution-ready-pack -type f -name "ndsp_post_patch_test_EN.sh" -exec cp -f {} scripts/tests/ \;

chmod +x scripts/audit/*.sh scripts/backup/*.sh scripts/tests/*.sh

echo "OK: audit/backup/test scripts installed."
```

---

# 4. Run Audit to Discover the Real Current State

This step reveals the current state before any modification.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$PROJECT_DIR" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/audit/ndsp_server_and_project_audit_EN.sh
```

## Required Audit Outputs
The report should show:

```txt
- Page status.
- API status.
- Nginx status.
- SSL status.
- systemd status.
- PM2 status.
- Radar presence.
- Sidebar presence.
- Disclaimer presence.
- Forbidden wording presence.
```

---

# 5. Create Current Reality Lock

After reading the Audit report, create:

```txt
docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_EN.md
```

Use this template:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_EN.md <<'EOF'
# NDSP Current Reality Lock

## Frontend
FRONTEND_DIR=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app

## Backend
BACKEND_DIR=$HOME/empire-core-new
API_BASE=https://api.ndsp.app

## Official Pages
- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html

## Services
- ndsp-api
- ndip-api-new
- ndsp-next or PM2 service according to real state

## Decision API
/api/decision/quality-live?symbol=ETHUSDT

## Required Decision Fields
- symbol
- live_price
- decision_quality
- scenario_state
- directional_context
- market_state
- reading_horizon
- horizon_strength
- caution_reason
- sanitized_summary

## Protected UI Elements
- Sidebar
- Radar
- Disclaimer
- Official page links

## Forbidden Output
- Buy Now
- Sell Now
- اشتر الآن
- بيع الآن
- Enter trade
- Guaranteed profit
EOF

echo "OK: Current reality lock created."
```

> After creating the file, update values based on the actual Audit report. Do not guess.

---

# 6. Create V1 Freeze

This file prevents new ideas from expanding the scope before V1 is complete.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_V1_FREEZE_EN.md <<'EOF'
# NDSP V1 Freeze

## Rule
This is V1. Anything outside scope is deferred until V1 is complete and acceptance tests pass.

## Inside V1
- Landing page
- Registration
- Login
- 16-day trial
- Disclaimer
- User portal
- Decision support page
- Asset view page
- Command center
- Daily brief
- Settings and alerts
- Live decision API
- Live price
- Radar
- Sidebar
- No Buy/Sell
- Hidden secret engines

## Outside V1
- Trading bot
- Trade execution
- Native mobile app
- Full engine disclosure
- Broker integration
- Direct financial recommendations
- Complex enterprise system

## Forbidden During V1
- Do not rename official pages.
- Do not remove radar.
- Do not remove sidebar.
- Do not expose secret layers.
- Do not add buy or sell commands.
- Do not modify backend for a frontend issue unless the need is proven.
EOF

echo "OK: V1 freeze created."
```

---

# 7. Create Final Legal Disclaimer

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/04-legal/NDSP_LEGAL_DISCLAIMER_MASTER_EN.md <<'EOF'
# NDSP Legal Disclaimer

NDSP — Nawaf Decision Support Platform is a decision-support and analytical platform. It is not a financial recommendation platform and does not provide trade execution instructions.

By using the platform, you acknowledge that:
- The platform does not provide buy or sell recommendations.
- The platform does not guarantee profits or outcomes.
- The displayed readings are analytical and supportive only.
- Data may be delayed, interrupted, or differ by source.
- The user is fully responsible for their own financial and investment decisions.
- Any financial decision should be based on the user's own judgment and, when needed, consultation with a licensed professional.
- NDSP is not responsible for losses resulting from the use or misunderstanding of its readings.

This disclaimer must be accepted before entering the user portal.
EOF

echo "OK: legal disclaimer created."
```

---

# 8. Create Implementation Backlog

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_IMPLEMENTATION_TASKS_EN.md <<'EOF'
# NDSP Implementation Tasks

## TASK-001 — Install documentation inside the project
Objective: Make docs the source of truth in the repository.
Test: docs and scripts folders exist with the correct structure.
Rollback: remove newly created folders only if they contain no important changes.

## TASK-002 — Run Audit
Objective: know the current state before modification.
Test: Audit report exists.
Rollback: none; audit is read-only.

## TASK-003 — Lock real paths
Objective: document paths, services, and domains.
Test: Current Reality Lock file is complete.
Rollback: correct the file values.

## TASK-004 — Create V1 Freeze
Objective: prevent scope expansion.
Test: V1 Freeze file exists.
Rollback: review the file; do not delete governance.

## TASK-005 — Run Backup before first patch
Objective: preserve rollback point.
Test: BACKUP_DIR and REPORT exist.
Rollback: use backup if patch fails.

## TASK-006 — Stabilize disclaimer
Objective: prevent portal entry without disclaimer acceptance.
Test: disclaimer appears before portal.

## TASK-007 — Stabilize sidebar
Objective: prevent navigation loss.
Test: sidebar exists on official pages.

## TASK-008 — Stabilize radar
Objective: prevent radar disappearance on data failure.
Test: radar exists or clear fallback is shown.

## TASK-009 — Stabilize decision API
Objective: match JSON fields with frontend.
Test: curl returns required fields.

## TASK-010 — Stabilize live price
Objective: display price without disappearing when provider fails.
Test: LIVE, STALE, or UNAVAILABLE is clearly shown.

## TASK-011 — Prevent Buy/Sell language
Objective: protect platform from execution recommendations.
Test: grep finds no direct trading commands.

## TASK-012 — Hide secret engines
Objective: protected layers are not exposed.
Test: secret layer names are not visible in frontend.

## TASK-013 — Mobile test
Objective: ensure cards, sidebar, and radar do not overlap.
Test: manual check or Playwright later.

## TASK-014 — Post Patch Test
Objective: test after every patch.
Test: post patch script passes.

## TASK-015 — Deploy V1
Objective: release stable V1.
Test: pages 200, API works, SSL works, no critical errors.
EOF

echo "OK: implementation tasks created."
```

---

# 9. Run Backup Before the First Patch

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$PROJECT_DIR" \
scripts/backup/ndsp_safe_backup_before_patch_EN.sh
```

Do not move to modification unless you see:

```txt
BACKUP_DIR=...
REPORT=...
```

---

# 10. First Allowed Patch After Readiness

The first patch should not be large.  
Best first patch:

```txt
Stabilize the disclaimer and verify the sidebar and radar do not disappear.
```

Do not start with a large integration or rebuild. Start with a small, testable patch.

---

# 11. Run Post Patch Test

After the first patch:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/tests/ndsp_post_patch_test_EN.sh
```

If the test fails:
```txt
1. Do not deploy over the failure.
2. Review the report.
3. Fix the cause if simple.
4. Or rollback to backup.
```

---

# 12. Ready Prompt for the Second Tool

Copy this text to the second tool:

```txt
You are working on NDSP — Nawaf Decision Support Platform.

The current task is to apply the closing stage and start implementation, not to build new features.

Execute in order:
1. Create docs and scripts folders according to the official structure.
2. Import previous documentation packs into docs.
3. Copy audit/backup/test scripts into scripts.
4. Run Audit Script.
5. Extract real values from the Audit report.
6. Create NDSP_CURRENT_REALITY_LOCK_EN.md.
7. Create NDSP_V1_FREEZE_EN.md.
8. Create NDSP_LEGAL_DISCLAIMER_MASTER_EN.md.
9. Create NDSP_IMPLEMENTATION_TASKS_EN.md.
10. Run Backup Script.
11. Do not start code changes before the previous steps pass.
12. Then start with the first small patch: stabilize disclaimer while preserving sidebar and radar.
13. After the patch, run Post Patch Test.

Forbidden:
- Deleting pages.
- Changing global design.
- Modifying API without proven need.
- Exposing secret engines.
- Adding Buy/Sell language.
- Starting a large patch before Audit and Backup.
- Stacking undocumented scripts.

Required output:
- Audit report.
- Backup path.
- Four Runbook files.
- Post Patch Test result if the first patch was executed.
```

---

# 13. Closing Point

After executing this document, planning is closed and implementation starts.

Correct transition:

```txt
Planning Closed
→ Documentation Installed
→ Audit Done
→ Reality Locked
→ V1 Frozen
→ Backup Ready
→ First Patch
→ Post Patch Test
→ Continue V1 Tasks
```

This is the launch point for the second tool.
