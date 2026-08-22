# NDSP Final Pre-Implementation Transition Plan
## Final Transition Before Starting Implementation

**Project:** NDSP — Nawaf Decision Support Platform  
**Version:** v1.0  
**Date:** 2026-07-06  
**Purpose:** Convert the previous packs from standalone documents into an operating system inside the project, then begin implementation safely and systematically.

---

# 1. Current Status Summary

The following core packs have been prepared:

```txt
1. System Build & Readiness Catalog
2. Build Tools & Control Pack
3. Execution Ready Pack
```

These packs mean the project no longer needs more general planning.  
The next stage is to place the packs inside the project, run the audit, document the real current state, and start implementation phase by phase.

---

# 2. Is Anything Left Before Implementation?

Yes. A few transition steps remain, and they are critical:

```txt
1. Place all files inside the repository/project.
2. Run the server and project audit.
3. Fill in the real paths and service values.
4. Freeze V1 scope.
5. Convert the plan into implementation tasks.
6. Prepare a simple test gate before deployment.
7. Approve the final legal disclaimer.
8. Begin implementation only after audit and backup succeed.
```

After these steps, real implementation can begin.

---

# 3. Mandatory Rule

No new code modification starts before the following are completed:

```txt
1. Move/copy the documentation files into the project.
2. Run the Audit Script.
3. Read the audit report.
4. Lock the real paths and services.
5. Run the Backup Script.
6. Execute one small scoped change.
7. Run the Post Patch Test.
```

Any AI tool or developer who skips these steps is working outside governance.

---

# 4. Where to Place the Files

The packs must be placed under `docs` and `scripts` like this:

```txt
ndsp/
├── docs/
│   ├── 00-build-catalog/
│   ├── 01-build-control-pack/
│   ├── 02-execution-ready-pack/
│   ├── 03-final-transition/
│   ├── 04-legal/
│   └── 05-runbooks/
├── scripts/
│   ├── audit/
│   ├── backup/
│   ├── tests/
│   └── deploy/
├── frontend/
├── backend/
├── .env.example
└── README.md
```

If the current project has a different structure, do not rebuild it from scratch.  
Only add documentation and script folders without breaking what already exists.

---

# 5. Project Source of Truth

After the files are added, these folders become the source of truth:

```txt
docs/00-build-catalog/
docs/01-build-control-pack/
docs/02-execution-ready-pack/
docs/03-final-transition/
```

Every AI coding tool must read them before modifying code.

---

# 6. Real Values to Lock

Extract and document these values from the server:

```txt
FRONTEND_DIR=
BACKEND_DIR=
LIVE_FRONTEND_DIR=
API_BASE=
FRONTEND_BASE=
NGINX_SITE_FILE=
SYSTEMD_SERVICES=
PM2_SERVICES=
DATABASE_TYPE=
DATABASE_NAME=
DECISION_API_ENDPOINT=
DECISION_API_FIELDS=
DOMAIN_FRONTEND=
DOMAIN_API=
SSL_STATUS=
```

Do not guess these values.  
They must come from the audit report or the server directly.

---

# 7. Current-State Audit Command

Run the audit script from the Execution Ready Pack:

```bash
chmod +x scripts/audit/ndsp_server_and_project_audit_EN.sh
FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$HOME/empire-core-new" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/audit/ndsp_server_and_project_audit_EN.sh
```

If paths are different, adjust only the variables. Do not modify the script directly.

---

# 8. Backup Command Before the First Change

```bash
chmod +x scripts/backup/ndsp_safe_backup_before_patch_EN.sh
FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$HOME/empire-core-new" \
scripts/backup/ndsp_safe_backup_before_patch_EN.sh
```

No modification is allowed without a clear backup report.

---

# 9. Post-Patch Test Command

```bash
chmod +x scripts/tests/ndsp_post_patch_test_EN.sh
FRONTEND_DIR="/var/www/ndsp-my" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/tests/ndsp_post_patch_test_EN.sh
```

If the test fails, do not deploy over the failure.  
Fix the cause or rollback to the backup.

---

# 10. V1 Scope Freeze

Before implementation, declare V1 Freeze:

```txt
This is V1.
Anything outside scope is deferred.
No new additions until V1 is completed and acceptance tests pass.
```

## Inside V1
```txt
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
```

## Outside V1
```txt
- Trading bot
- Trade execution
- Native mobile app
- Full engine disclosure
- Broker integration
- Direct financial recommendations
- Complex enterprise system
```

---

# 11. Convert the Plan Into Tasks

After the audit, create an implementation backlog:

```txt
TASK-001 Add documents into project
TASK-002 Run Audit Script
TASK-003 Lock real paths
TASK-004 Create V1 Freeze
TASK-005 Check official pages
TASK-006 Check decision API
TASK-007 Stabilize disclaimer
TASK-008 Stabilize sidebar
TASK-009 Stabilize radar
TASK-010 Stabilize live price binding
TASK-011 Remove/forbid Buy/Sell language
TASK-012 Hide secret engines
TASK-013 Mobile test
TASK-014 Post-patch test
TASK-015 Deploy V1
```

Each task must include:

```txt
- Objective
- Affected files
- Prohibitions
- Required test
- Rollback method
```

---

# 12. Simple Test and Deployment Gate

At the beginning, complex CI/CD is not required.  
A simple pre-deploy gate is enough:

```txt
1. npm build if Node/Next/Vite frontend exists.
2. Python/FastAPI tests if backend tests exist.
3. HTTP 200 page checks.
4. Decision API check.
5. Radar and sidebar check.
6. No Buy/Sell language check.
7. SSL and Nginx check.
```

Later these steps can be moved to GitHub Actions.

---

# 13. Post-Launch Monitoring

After V1 launch, set up basic monitoring:

```txt
Uptime Kuma  for domains and API uptime.
Sentry       for frontend/backend errors.
Netdata      for server monitoring.
Cron Backup  for backup automation.
Logrotate    to prevent log growth.
```

Top priorities:

```txt
1. Is my.ndsp.app up?
2. Is api.ndsp.app up?
3. Does /api/decision/quality-live work?
4. Does live price display?
5. Does login work?
6. Is disk space safe?
```

---

# 14. Final Legal Disclaimer

Create this file:

```txt
docs/04-legal/NDSP_LEGAL_DISCLAIMER_MASTER_EN.md
```

It must include:

```txt
- NDSP is decision support only.
- It is not financial advice.
- It does not provide buy or sell instructions.
- It does not guarantee profit or results.
- Data may be delayed or unavailable.
- The user is responsible for their own decisions.
- Readings are analytical, educational, and supportive only.
```

Users must not enter the portal before accepting this disclaimer.

---

# 15. AI Tool Command for This Stage

Copy this text into any AI coding tool:

```txt
You are working on NDSP.
The current task is not to build a new feature. It is to execute the final transition stage before implementation.

Do only the following:
1. Place the packs under docs and scripts according to the defined structure.
2. Do not modify frontend or backend yet.
3. Run the Audit Script or prepare the command if execution permission is unavailable.
4. Extract real paths and services from the report.
5. Create V1_FREEZE.md.
6. Create an initial implementation backlog.
7. Prepare Backup and Post Patch Test paths.
8. Do not start code modification before audit and backup pass.

Forbidden:
- Deleting pages.
- Changing design.
- Modifying API.
- Exposing secret engines.
- Adding Buy/Sell language.
- Building anything new before audit completion.
```

---

# 16. When Does Implementation Actually Start?

Implementation starts after these are true:

```txt
[ ] Packs are inside the project.
[ ] Audit Report exists.
[ ] Real paths are documented.
[ ] V1 Freeze is written.
[ ] Implementation backlog is written.
[ ] Backup Script is ready.
[ ] Post Patch Test is ready.
[ ] Legal Disclaimer is written.
[ ] First implementation task is selected.
```

Then start with one small safe change.

---

# 17. Recommended First Change After Readiness

After this document is added and the audit runs, the first change should not be large.  
The best first change is:

```txt
Stabilize the disclaimer and verify that official pages do not lose the sidebar or radar.
```

This change is important, clear, and testable.

---

# 18. Final Summary

Yes, after this document there is probably no major foundational item left.  
The next stage is practical implementation in this order:

```txt
1. Add documentation to the project.
2. Run the audit.
3. Lock the current real state.
4. Create backup.
5. Execute the first change.
6. Run post-patch test.
7. Repeat phase by phase until V1 is complete.
```

This is the transition point from planning to implementation.
