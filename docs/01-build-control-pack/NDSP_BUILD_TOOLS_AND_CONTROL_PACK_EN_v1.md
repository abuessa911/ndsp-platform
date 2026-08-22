# NDSP System Build Tools & Control Pack

**Document Name:** NDSP Build Tools & Control Pack  
**Project:** NDSP — Nawaf Decision Support Platform  
**Owner:** Nawaf  
**System Type:** Decision Support Platform, not a trading execution or direct recommendation system  
**Version:** v1.0  
**Purpose:** Define the tools, documents, governance rules, and operating controls required to build NDSP correctly, safely, and without chaotic changes during development, deployment, or maintenance.

---

## 1. Purpose of This Pack

This pack is not a random tool list. Its purpose is to create a structured **production line** for building NDSP so that no AI builder, developer, or script modifies the system randomly.

The correct build path is:

```txt
Documentation → Design → Implementation → Testing → Deployment → Monitoring → Maintenance
```

Building without this chain can cause:

- Existing pages to break.
- The radar or side menu to disappear.
- Pages to be duplicated or renamed incorrectly.
- Hidden internal engines to be exposed.
- Backend files to be modified unnecessarily.
- Frontend pages to bind to incorrect API fields.
- Scripts to be stacked on top of older scripts.
- Rollback to become difficult or impossible.

---

## 2. Core Build Principle

A tool alone does not build a correct system.  
The correct order is:

```txt
System Catalog + Governance + Page Map + API Contract + Test Plan + Deployment Plan + Audit Script
```

Only after that should tools such as Codex, Cursor, or another builder be allowed to modify the project.

---

## 3. Required Documents After the System Build Catalog

After the **NDSP System Build & Readiness Catalog**, the project needs an operational control pack named:

```txt
NDSP_BUILD_CONTROL_PACK
```

It should contain the following documents:

```txt
NDSP_MASTER_GOVERNANCE_RULES.md
NDSP_PAGE_REGISTRY.md
NDSP_API_CONTRACT.md
NDSP_DATABASE_SCHEMA.md
NDSP_DECISION_ENGINES_SPEC.md
NDSP_SECURITY_POLICY.md
NDSP_TEST_PLAN.md
NDSP_DEPLOYMENT_RUNBOOK.md
NDSP_ROLLBACK_PLAN.md
NDSP_PROTECTED_FILES_AND_RULES.md
NDSP_AI_BUILDER_PROMPT.md
NDSP_SERVER_AUDIT_SCRIPT.sh
```

---

## 4. Master Governance Rules

**Suggested file name:**

```txt
NDSP_MASTER_GOVERNANCE_RULES.md
```

### Purpose

This document is the constitution of the project. Any AI tool or developer working on NDSP must follow it before touching the code.

### Core Rules

- NDSP is a decision support platform, not a trading execution system.
- Do not display direct Buy or Sell recommendations.
- Do not expose hidden internal engine names.
- Do not modify the backend unless there is a clear reason.
- Do not stack scripts or duplicate fixes over previous fixes.
- Every change must be preceded by a backup.
- Every change must produce a clear report.
- Do not randomly rename official pages.
- Do not remove the side menu, radar, or disclaimer.
- Every page must have a known data source.
- Every API must have a clear contract.
- Any design change must not break existing functionality.

### NDSP-Specific Rule

The **Devil’s Advocate Layer** is the only layer with final blocking authority inside the decision logic. Other layers may assist, warn, or score, but they do not block unless governance explicitly allows it.

---

## 5. Official Page Registry

**Suggested file name:**

```txt
NDSP_PAGE_REGISTRY.md
```

### Purpose

Prevent page duplication, accidental renaming, or broken navigation during changes.

### Proposed Core Pages

```txt
/index.html
Main landing page

/decision-support.html
Decision support page

/NDSP_Asset_View.html
Asset view page

/NDSP_Command_Center.html
Command center

/NDSP_Daily_Brief.html
Decision journal / daily brief

/NDSP_Settings_Alerts.html
Settings and alerts

/admin
Admin console
```

### Page Rules

- Do not rename an official page without a clear decision.
- Do not create a duplicate of an existing page.
- Do not remove a page from the side menu without documentation.
- Every page must have a clear purpose.
- Every data-driven page must declare its API source.

---

## 6. Official API Contract

**Suggested file name:**

```txt
NDSP_API_CONTRACT.md
```

### Purpose

Define how the frontend communicates with the backend and prevent guessing field names.

### Important Endpoint Example

```txt
GET /api/decision/quality-live?symbol=ETHUSDT
```

### Input

```json
{
  "symbol": "ETHUSDT"
}
```

### Expected Output

```json
{
  "live_price": 0,
  "decision_quality": 0,
  "scenario_state": "UNDER_MONITORING",
  "directional_context": "NEUTRAL",
  "market_state": "UNKNOWN",
  "reading_horizon": "PENDING",
  "horizon_strength": "PENDING",
  "caution_reason": "Data under processing",
  "sanitized_summary": "Decision support reading only. Not financial advice."
}
```

### Pages Using This API

```txt
decision-support.html
NDSP_Asset_View.html
NDSP_Command_Center.html
NDSP_Daily_Brief.html
```

### API Rules

- The frontend must not depend on undocumented fields.
- Field names must not change unless the contract is updated.
- If the data provider fails, the API must return a clear state instead of breaking the page.
- Raw technical errors must not be shown to end users.

---

## 7. Database Schema Map

**Suggested file name:**

```txt
NDSP_DATABASE_SCHEMA.md
```

### Core Tables

```txt
users
subscriptions
trial_sessions
assets
market_prices
decision_readings
alerts
audit_logs
admin_actions
password_resets
```

### Example: users Table

```txt
users
- id
- email
- phone
- password_hash
- role
- trial_started_at
- trial_ends_at
- created_at
- updated_at
```

### Database Rules

- Email must be unique.
- Phone number must be unique after digit normalization.
- Passwords must never be stored as plain text.
- Important admin actions must be recorded in audit_logs.
- Production migrations must not run without a backup.

---

## 8. Decision Engines Specification

**Suggested file name:**

```txt
NDSP_DECISION_ENGINES_SPEC.md
```

### Core Engines and Layers

```txt
TDL Engine
NMP Engine
Market Direction Engine
Scenario Levels Engine
Momentum Engine
Macro USD Engine
Risk Engine
Devil’s Advocate Layer
Decision Quality Engine
Final State Engine
```

### Each Engine Must Define

- Purpose.
- Inputs.
- Outputs.
- Whether its name may be shown to the user.
- Whether it is public or protected.
- Whether it has blocking authority.
- How it connects to other engines.

### Display Rule

Allowed user-facing terms should be understandable, such as:

```txt
Decision Quality
Scenario State
Directional Context
Caution Reason
Under Monitoring
Allowed
Caution
Blocked
```

Forbidden user-facing terms:

```txt
Hidden engine names
Internal formula details
Protected layer names
Direct execution recommendations
```

---

## 9. Security Policy

**Suggested file name:**

```txt
NDSP_SECURITY_POLICY.md
```

### Core Areas

- Login protection.
- Password hashing.
- Password reset protection.
- Unique email and phone constraints.
- Admin console protection.
- API key protection.
- CORS configuration.
- Rate limiting.
- Hiding technical errors from users.
- Internal error logging.
- Avoiding exposure of system secrets in the console or frontend.

---

## 10. Test Plan

**Suggested file name:**

```txt
NDSP_TEST_PLAN.md
```

### Core Tests

```txt
Landing page load test
Side menu test
Decision support page test
Asset view page test
Command center test
Daily brief page test
Settings and alerts page test
Registration test
Login test
16-day trial test
Disclaimer test
Decision API test
Live price test
Radar test
Hidden engine exposure test
No Buy/Sell wording test
Mobile responsiveness test
SSL test
Nginx test
systemd services test
PM2 services test
Rollback readiness test
```

### Recommended Test Tools

```txt
curl
pytest
Playwright
Lighthouse
```

Given the preferred shell-based workflow, build sh scripts such as:

```txt
test_pages_200.sh
test_api_decision_live.sh
test_auth_flow.sh
test_ssl_nginx.sh
test_no_forbidden_terms.sh
test_mobile_render.sh
test_rollback_ready.sh
```

---

## 11. Deployment Runbook

**Suggested file name:**

```txt
NDSP_DEPLOYMENT_RUNBOOK.md
```

### It Must Include

- Official project path.
- Live frontend path.
- Backend path.
- systemd service names.
- PM2 service names.
- Nginx configuration.
- Domains.
- Build commands.
- Restart commands.
- Health checks.
- Report location.
- Backup location.

### Possible Service Examples

```txt
ndsp-api
ndip-api-new
ndsp-next
market-bridge
```

### Deployment Rule

No production deployment should happen without:

```txt
backup
build
test
restart
health check
report
```

---

## 12. Rollback Plan

**Suggested file name:**

```txt
NDSP_ROLLBACK_PLAN.md
```

### Purpose

Ensure the system can be restored if a change breaks a page, API, or design.

### It Must Include

- Where backups are stored.
- How to restore the frontend.
- How to restore Nginx configuration.
- How to restore service files.
- How to stop the new broken version.
- How to confirm the old version is working.

### Golden Rule

Any production change script without backup or rollback is unsafe.

---

## 13. Protected Files and Rules

**Suggested file name:**

```txt
NDSP_PROTECTED_FILES_AND_RULES.md
```

### Do Not Modify Without Explicit Instruction

```txt
Auth files
Registration files
Password reset files
Database migration files
Nginx files
systemd files
Decision engine core files
Secrets and .env files
```

### Do Not Delete

```txt
Side menu
Radar
Disclaimer
Official page links
Decision API binding
Financial non-advice messages
Official page names
```

---

## 14. AI Builder Prompt

**Suggested file name:**

```txt
NDSP_AI_BUILDER_PROMPT.md
```

### Purpose

Use this with Codex, Cursor, or any builder tool so it does not act randomly.

### Short Instruction Prompt

```txt
You are working on NDSP — Nawaf Decision Support Platform.
This system is a decision support platform, not a trading recommendation or execution platform.
You must follow the system catalog, governance documents, page registry, and API contract.
Do not expose hidden engine names.
Do not add Buy/Sell recommendations.
Do not remove the radar, side menu, or disclaimer.
Do not rename official pages.
Do not modify the backend unless the task clearly requires it.
Before any change, create a backup.
After any change, create a report listing modified files and completed tests.
Every change must be rollback-ready.
```

---

## 15. Server Audit Script

**Suggested file name:**

```txt
NDSP_SERVER_AUDIT_SCRIPT.sh
```

### Purpose

Extract the current project state from the server before any build or modification.

### What the Script Should Check

```txt
Project paths
Frontend files
Backend files
systemd services
PM2 services
Nginx configuration
SSL status
Domains
Page responses
API responses
Disk and memory
Recent errors
Backup existence
Previous reports
```

---

## 16. Recommended Tools for Building NDSP

### Documentation

```txt
Markdown inside /docs
```

This keeps documentation close to the codebase.

### Project Management

```txt
GitHub Projects
```

For tasks, bugs, releases, and roadmap tracking.

### Code and Version Control

```txt
GitHub
Git
```

There is no safe build process without Git.

### AI Coding Assistance

```txt
Codex CLI
Cursor
ChatGPT
```

Suggested usage:

```txt
Codex CLI for implementation inside the project
Cursor for visual review and editing
ChatGPT for planning, governance, and scripts
```

### Design and Visual Identity

```txt
Figma
Canva
```

Warning: Canva is for design and marketing assets, not production code modification.

### API Testing

```txt
curl
Postman
Insomnia
```

For the current workflow, the best choice is:

```txt
curl + sh scripts
```

### Frontend Testing

```txt
Playwright
Lighthouse
```

### Backend

```txt
FastAPI
PostgreSQL
```

### Deployment

```txt
Nginx
systemd
PM2
Certbot
bash scripts
```

### Monitoring

```txt
Uptime Kuma
Sentry
Netdata
Grafana later
```

---

## 17. Ideal NDSP Toolchain

```txt
Documentation:
/docs/*.md

Project management:
GitHub Projects

Code:
GitHub Repository

AI coding support:
Codex CLI + ChatGPT + Cursor

Frontend:
Next.js or Vite/HTML depending on the current version

Backend:
FastAPI

Database:
PostgreSQL

Testing:
pytest + curl scripts + Playwright

Deployment:
Nginx + systemd + PM2 + Certbot

Monitoring:
Uptime Kuma + Sentry + Netdata

Design:
Figma/Canva for visual identity and marketing assets only
```

---

## 18. Information to Lock Before Building

Before running any builder tool, collect and lock the following:

```txt
1. Official project path on the server
2. Official live frontend path
3. Official backend path
4. systemd service names
5. PM2 service names
6. Current Nginx configuration
7. Final page list
8. Final API list
9. Field names returned by the decision API
10. Engine names allowed to be shown
11. Engine names that must remain hidden
12. No Buy/Sell rule
13. Disclaimer rule
14. Registration and 16-day trial process
15. Admin Console scope
16. Backup method
17. Rollback method
```

---

## 19. Correct Execution Order

```txt
1. Lock the main system catalog
2. Create NDSP_BUILD_CONTROL_PACK
3. Run the server audit script
4. Extract paths, services, pages, and APIs
5. Lock the Page Registry
6. Lock the API Contract
7. Lock the Protected Files Rules
8. Prepare the Test Plan
9. Implement only the requested change
10. Run tests
11. Deploy the change
12. Create a report
13. Monitor after deployment
```

---

## 20. Executive Summary

The best way to build NDSP is not through one tool. The correct stack is:

```txt
GitHub for version control
Codex CLI for implementation
ChatGPT for planning, governance, and scripts
Cursor for review and editing
Figma/Canva for design only
curl/pytest/Playwright for testing
Nginx/systemd/PM2 for deployment
Uptime Kuma/Sentry/Netdata for monitoring
```

But before using any implementation tool, prepare:

```txt
NDSP_BUILD_CONTROL_PACK
```

This pack protects the project from chaos and turns the build process from random attempts into a clear, maintainable, and scalable system.
