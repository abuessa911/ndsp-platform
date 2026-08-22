# NDSP V1.3 — Official Scope Freeze

Freeze date: 20260708_235303  
Status: SCOPE_FREEZE  
Approved previous phase: P3 Final  
Baseline reference: docs/05-runbooks/NDSP_V13_PLANNING_BASELINE_AUDIT_READONLY_20260708_234638.md  
Draft reference: docs/05-runbooks/NDSP_V13_SCOPE_DRAFT_20260708_234638.md  

---

## 1) V1.3 Definition

V1.3 is not a rescue phase and not an emergency repair phase.  
V1.3 is a controlled product-improvement phase built on a clean and closed P3 runtime.

Phase rule:

> No code patch before Backup + Report + Post Patch Test.

---

## 2) Approved Baseline

The following baseline is accepted:

- P3 Final is closed.
- systemctl --failed = 0.
- Nginx active.
- PM2 active/enabled.
- ndsp-portal online.
- API health = 200.
- quality-live = 200.
- my.ndsp.app = 200.
- admin.ndsp.app = 200.
- port 9001 listening.
- Protected assets were checksummed.
- User portal pages were indexed.
- Data files were indexed.
- Release packages were archived and indexed.

---

## 3) Baseline Notes

The baseline reported:

- command-center-real.json owned by root:root.
- GOVERNANCE_WORDING_HITS=11.

Classification:

- Current wording hits are not treated as direct failures because they appear to come from words such as "direction/trend" and asset/energy naming inside data/assets.
- command-center-real.json root ownership requires a separate ownership review patch only if it affects data refresh.

No changes are made inside Scope Freeze.

---

## 4) Approved V1.3 Scope

### 4.1 Decision Room UX Completion

Allowed:

- Improve page titles.
- Improve explanation of reading states.
- Improve navigation.
- Improve loading/empty/error states.
- Improve Beginner vs Advanced separation.
- Explain readings without changing decision logic.

Forbidden:

- Changing TDL/NMP/Golden/Risk/Devil logic.
- Adding trading recommendations.
- Adding Buy/Sell wording.
- Adding execution instructions.

---

### 4.2 Data Freshness and Trust Panel

Allowed:

- Show data-quality.json summary.
- Show last update time.
- Show source health.
- Warn when data is stale.
- Explain that readings depend on data freshness.

Forbidden:

- Hiding stale data.
- Faking freshness.
- Showing unsupported trust levels.

---

### 4.3 Completed Decisions Viewer Hardening

Allowed:

- Filter by asset.
- Filter by state.
- Show readiness vs strength.
- Show why_not_completed.
- Show scenario levels.
- Show caution or objection reasons.

Forbidden:

- Execution buttons.
- Bot trading controls inside NDSP core.
- Turning completed decisions into trading orders.

---

### 4.4 Admin Release Evidence Page

Allowed:

- Show latest Release Package.
- Show SHA256.
- Show latest Report.
- Show Reality Lock status.
- Read-only administrative evidence view.

Forbidden:

- Browser shell execution.
- Restart/stop/disable buttons from UI.
- Direct service control from UI.

---

### 4.5 Visual Polish Without Script Stacking

Allowed:

- CSS-only refinements.
- Improve cards and tables.
- Improve Arabic/English language.
- Remove visual duplication.
- Unify button and heading style.

Forbidden:

- Replacing protected scripts:
  - ndsp-radar-safe-clean.js
  - ndsp-global-menu.js
  - ndsp-disclaimer-gate.js
- Adding new global scripts without a removal plan.
- Radar changes that break menu or pages.

---

## 5) Out of Scope

- No bot integration inside NDSP core.
- No enabling ndip-api-new.service.
- No enabling disabled legacy services.
- No Nginx change unless in a separate patch.
- No reboot unless in a separate Reboot Drill.
- No direct trading advice.
- No Buy/Sell wording.
- No execution workflow.
- No engine logic changes.
- No DB schema change without a separate migration plan.

---

## 6) Approved Execution Order

V1.3 must run as small patches:

1. V13-A: Evidence/Admin Release Page Docs and UI.
2. V13-B: Data Freshness and Trust Panel.
3. V13-C: Decision Room UX Copy Cleanup.
4. V13-D: Completed Decisions Viewer Hardening.
5. V13-E: Visual Polish and Duplicate Cleanup.

Each patch must include:

- Backup.
- Patch Report.
- Runtime health test.
- Endpoint test.
- Governance wording scan.
- Reality Lock update on success.

---

## 7) Closure Rule

V1.3 cannot be closed without:

- V13 final audit.
- systemctl --failed = 0.
- Nginx active.
- PM2 active.
- ndsp-portal online.
- API health 200.
- quality-live 200.
- my/admin 200.
- package + sha256.
- local download + sha256 verification.

