# NDSP V1.3 — Implementation Plan

Created: 20260708_235303  
Mode: controlled small patches  
Runtime changes in this document: none  

---

## Principle

V1.3 starts only after Scope Freeze.  
No direct patching from draft notes.

---

## Patch Sequence

### V13-A — Release Evidence Read-only Page

Objective:
Create a read-only admin evidence page that exposes current release state.

Inputs:
- Latest P3 package path.
- Latest sha256.
- Latest P3 report.
- Reality Lock status.

Expected output:
- Static/read-only page or documented endpoint.
- No shell execution.
- No service controls.

Tests:
- Page HTTP 200.
- No exposed secrets.
- No service-control buttons.
- Governance scan OK.

---

### V13-B — Data Freshness and Trust Panel

Objective:
Show freshness status from existing data files.

Inputs:
- /var/www/ndsp-my/data/data-quality.json
- /var/www/ndsp-my/data/news-impact.json
- /var/www/ndsp-my/data/economic-calendar.json
- command-center-real.json ownership review if needed.

Expected output:
- User sees last update.
- User sees source health.
- User sees stale warning.

Tests:
- Existing data pages still render.
- No fake freshness.
- API endpoints remain 200.

---

### V13-C — Decision Room UX Copy Cleanup

Objective:
Improve labels and explanations without changing backend logic.

Inputs:
- Existing pages under /var/www/ndsp-my.
- Protected asset checksums from baseline.

Expected output:
- Better page copy.
- Better empty/loading/error states.
- Beginner/Advanced clarity.

Tests:
- Protected asset checksums unchanged unless explicitly approved.
- No Buy/Sell wording.
- No execution wording.

---

### V13-D — Completed Decisions Viewer Hardening

Objective:
Improve completed decisions review experience.

Expected output:
- Filters by asset/state.
- Readiness vs strength.
- why_not_completed display.
- scenario levels display.

Tests:
- completed-decisions page HTTP 200.
- API health OK.
- No execution controls.

---

### V13-E — Visual Polish and Duplicate Cleanup

Objective:
Clean visual duplication and improve consistency.

Expected output:
- CSS/component improvements.
- No global script stacking.
- No duplicate navigation/menu behavior.

Tests:
- All portal pages HTTP 200.
- Menu works.
- Radar works.
- Disclaimer gate works.
- Governance wording scan OK.

---

## Mandatory Test Block For Every Patch

Each V1.3 patch must run:

- systemctl --failed
- nginx -t
- systemctl is-active nginx
- systemctl is-active pm2-nawaf511.service
- pm2 list as nawaf511
- curl https://api.ndsp.app/api/health
- curl https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT
- curl https://my.ndsp.app/
- curl https://admin.ndsp.app/
- protected assets checksum check
- governance wording scan
- report creation
- Reality Lock update on success

---

## Backout Rule

Every V1.3 patch must have a backup path and a rollback command.
If any critical endpoint fails, rollback first, then diagnose.

---

## No-Go Conditions

Do not patch if:

- systemctl --failed is not 0.
- nginx -t fails.
- pm2-nawaf511 is not active.
- ndsp-portal is not online.
- P3 Reality Lock is missing.
- Scope Freeze files are missing.
- Backup cannot be created.

