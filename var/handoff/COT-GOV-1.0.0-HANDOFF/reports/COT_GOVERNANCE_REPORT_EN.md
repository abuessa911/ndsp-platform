<div dir="ltr">

# Complete COT Direction, Timing, Governance, and Path-Migration Report

**Version:** COT-GOV-1.0.0  
**Canonical timezone:** UTC  
**Canonical project root:** `/home/nawaf511/empire-core-new`  
**Document status:** Logically approved specification — not yet integrated into production

---

## 1. Executive summary

The project separates:

1. Long-term investment analysis.
2. Short-term speculation analysis.
3. Direction logic.
4. Weekly support logic.
5. Timing and day-control logic.
6. Official CORE output.
7. Experimental EXPANDED output.
8. Current legacy implementation.
9. Canonical and legacy filesystem paths.

Positions and Changes must not be mixed. Speculation timing must never run inside investment mode.

---

## 2. Verified environment

The canonical project root is:

`/home/nawaf511/empire-core-new`

The project uses:

- Node.js and Express for primary services.
- Python and Uvicorn for selected data services.
- React and Vite for frontends.
- TypeScript for selected frontends and preferably all new governance interfaces.
- Candidate governance service:
  `backend/services/decision_governance_core`
- Raw COT gateway:
  `apps/ndsp-raw-cot-gateway`

Runtime references currently exist across:

- `/home/nawaf511/empire-core-new`
- `/opt/empire-core`
- `/root/empire-core`
- `/var/www`
- Additional independent `/opt` services

No legacy path may be deleted immediately.

---

## 3. Official terminology

### 3.1 Dominance delta

Dominance delta is the numerical difference between Long and Short values inside the same row or aggregated group:

`Dominance Delta = Long − Short`

It is not a time-series difference between reports.

Direction is determined by direct comparison:

- Long > Short: Bullish.
- Short > Long: Bearish.
- Long = Short: Neutral.

A difference of one contract is sufficient.

### 3.2 Direction, explicitness, and horizon

Official labels:

- Bullish explicit — extended horizon.
- Bearish explicit — extended horizon.
- Bullish non-explicit — narrow horizon.
- Bearish non-explicit — narrow horizon.
- Neutral only on exact equality.

Classification:

- Opposite signs:
  explicit — extended horizon.
- Same sign:
  non-explicit — narrow horizon.
- Exact equality:
  neutral.

The initial implementation classifies a zero/non-zero pair as non-explicit and narrow unless a later governance decision changes that boundary rule.

---

## 4. Investment mode

### 4.1 Official total direction

Investment mode compares:

`Asset Manager Positions Long`

against:

`Asset Manager Positions Short`

only.

Other Reportables do not participate in official investment CORE output.

### 4.2 Disabled components

The following are disabled in investment mode:

- Day Control.
- Daily Controller.
- TDL-M&L.
- TDL-S.
- Speculation Timing.
- Any controller selection based on weekday.

They must not be invoked even as secondary confirmation.

### 4.3 Weekly support

Investment mode compares:

`Asset Manager Changes Long`

against:

`Asset Manager Changes Short`

only to determine whether the weekly direction supports the total direction.

On agreement:

`weeklySupport = CONFIRMED`

On disagreement:

`weeklySupport = NOT_CONFIRMED`

Disagreement:

- Does not change total direction.
- Does not hide total direction.
- Does not reverse total direction.
- Does not upgrade or downgrade it.
- Displays:
  **Weekly support is not confirmed.**

### 4.4 July 21 example

Asset Manager Positions:

- Long: 4,684
- Short: 1,957
- Dominance delta: +2,727
- Result:
  **Bullish non-explicit — narrow horizon**

Asset Manager Changes:

- Long: -95
- Short: -7
- Dominance delta: -88
- Result:
  **Bearish non-explicit — narrow horizon**

Official investment output:

- Total direction:
  **Bullish non-explicit — narrow horizon**
- Weekly support:
  **Weekly support is not confirmed**

---

## 5. Speculation mode

### 5.1 Dataset

Speculation mode uses Changes only.

Positions must not determine speculation direction.

### 5.2 Controlling category

The engine identifies the controlling side according to the selected day-control perspective and then uses only the controlling category’s Changes.

### 5.3 CORE

Long-term controller:

- Asset Managers only.

Short-term controller:

- Leveraged Funds only.

### 5.4 EXPANDED

Long-term controller:

- Asset Managers + Other Reportables.

Short-term controller:

- Leveraged Funds + Dealer/Intermediary.

Long values are added to Long values, and Short values to Short values before comparison.

### 5.5 TDL-M&L and TDL-S

They are allowed only in speculation mode.

They are forbidden in investment mode.

Their rules must be configurable through explicit files and contracts rather than hidden inside engine code.

The existing detailed semantics have not yet been supplied. The reference implementation therefore exposes injectable timing adapters and does not invent undocumented TDL behavior.

---

## 6. Day-control perspectives

### 6.1 D1

- Monday: Long-term.
- Friday: Long-term.
- Tuesday: Short-term.
- Wednesday: Short-term.
- Thursday: Short-term.
- Saturday: Short-term.
- Sunday: Short-term.

### 6.2 D2

- Thursday: Long-term.
- Friday: Long-term.
- Monday: Short-term.
- Tuesday: Short-term.
- Wednesday: Short-term.
- Saturday: Short-term.
- Sunday: Short-term.

Monday and Thursday are the main discriminating days.

---

## 7. Canonical timing

### 7.1 UTC

UTC is the sole reference for:

- Day boundaries.
- Week boundaries.
- Day control.
- Report activation.
- Price measurement.
- Storage.
- Contracts.
- Logs.
- Tests.
- Audit records.

Local time is display-only.

### 7.2 Week boundary

- Week begins Monday at 00:00:00Z.
- Week ends at the next Monday boundary.
- Half-open interval:
  `effectiveFrom <= timestamp < effectiveUntil`

### 7.3 Report activation

A Tuesday COT report becomes effective on the following Monday at 00:00 UTC.

Example:

- Report date: 2026-07-21.
- Effective from: 2026-07-27T00:00:00Z.
- Effective until: 2026-08-03T00:00:00Z.

---

## 8. CORE and EXPANDED

### 8.1 CORE

CORE is the temporary official model.

Investment:

- Asset Manager Positions only.
- Asset Manager Changes for weekly support only.

Speculation:

- Asset Manager Changes under long-term control.
- Leveraged Funds Changes under short-term control.

CORE alone:

- Produces official direction.
- Writes official results.
- Appears to users.
- Is exposed through Public API.

### 8.2 EXPANDED

EXPANDED is a parallel experiment.

Experimental investment:

- Asset Managers + Other Reportables.

Experimental speculation:

- Asset Managers + Other Reportables.
- Leveraged Funds + Dealer/Intermediary.

Execution mode:

`SHADOW_MODE`

Restrictions:

- Cannot modify CORE.
- Cannot write official results.
- Cannot appear to users.
- Cannot send public notifications.
- Cannot execute decisions.
- Cannot promote automatically.

### 8.3 Visibility

End user:

- CORE only.

Administrators and developers:

- CORE.
- EXPANDED.
- Experiment status.
- Agreement/disagreement.
- Versions and audit records.

---

## 9. Structural isolation

Official path:

CORE Engine  
→ Official Result Store  
→ Public API  
→ User Interface

Experimental path:

EXPANDED Shadow Engine  
→ Experimental Result Store  
→ Internal Admin API  
→ Admin Dashboard

No path may connect EXPANDED to Public API.

EXPANDED failure must not interrupt CORE.

Promotion requires:

1. Completed test.
2. Comparison report.
3. Governance approval.
4. New release.
5. Acceptance tests.
6. Rollback plan.

---

## 10. Legacy backend review

Before changing files:

1. Create a dedicated Git branch.
2. Record the current commit.
3. Create a pre-change tag.
4. Back up governance and raw-COT services.
5. Search all direction and timing code.
6. Identify consumers.
7. Build an impact map.

Search terms include:

- direction
- trend
- bias
- bullish
- bearish
- positions
- changes
- asset manager
- leveraged funds
- other reportables
- dealer
- delta
- TDL-M&L
- TDL-S
- day control
- controller
- timezone
- UTC
- effective week
- report activation

Legacy code is classified as:

- Compatible.
- Wrappable.
- Used legacy.
- Unused legacy.
- Unknown and requiring investigation.

No legacy engine is deleted before CORE_V1 runs in shadow and is compared.

---

## 11. Delivery phases

### Phase 0 — Protect current state

Status: Not started.

### Phase 1 — Backend logic audit

Status: Not started.

### Phase 2 — Legacy path audit

Status:

- Legacy references confirmed.
- Migration-grade inventory not yet produced.

### Phase 3 — Governance and contracts

Status:

- Rules approved.
- Reference files included in this package.
- Not integrated into production.

### Phase 4 — Dominance engine

Status:

- Reference implementation included.
- Requires review and integration.

### Phase 5 — Investment engine

Status:

- Reference implementation included.
- Requires source and storage integration.

### Phase 6 — Speculation engine

Status:

- Direction and day-control reference implementation included.
- Existing TDL behavior must still be extracted.

### Phase 7 — CORE and EXPANDED execution

Status: Not started.

### Phase 8 — Historical testing

Status: Not started.

Preferred sample:

- 26 to 52 reports.

### Phase 9 — Forward shadow testing

Status: Not started.

Initial duration:

- One full month.

### Phase 10 — Admin UI

Status:

- Requirements defined.
- Implementation incomplete.

### Phase 11 — Canonical path migration

Status:

- Decision approved.
- Migration not performed.

### Phase 12 — systemd migration

Status: Not started.

### Phase 13 — Nginx migration

Status: Not started.

### Phase 14 — Parallel runtime monitoring

Status: Not started.

### Phase 15 — Legacy path retirement

Status: Not started.

---

## 12. Canonical project root

Official root:

`/home/nawaf511/empire-core-new`

The goal is to keep within it:

- Source code.
- Services.
- Frontend source.
- Built frontend assets.
- Nginx templates.
- systemd templates.
- Contracts.
- Governance.
- Tests.
- Reports.
- Non-secret runtime data.
- Evidence.
- Experiment results.

Legacy paths to retire:

- `/opt/empire-core`
- `/root/empire-core`
- `/var/www/ndsp`
- `/var/www/ndsp-my`
- `/var/www/ndsp-admin`
- `/var/www/ndsp-public-gateway`

This does not mean deleting `/var/www` system-wide. It means ending this project’s dependency on it after verifying all consumers.

---

## 13. Files that remain outside the repository

Runtime files managed by the operating system remain in:

- `/etc/nginx`
- `/etc/systemd/system`
- `/etc/ndsp`

Source-controlled templates are stored in:

- `deploy/nginx`
- `deploy/systemd`
- `deploy/env-templates`

Secrets must not be committed.

---

## 14. systemd and Nginx migration

### systemd

Replace legacy WorkingDirectory and ExecStart paths one service at a time.

Each change requires:

- Backup.
- Dry run.
- systemd-analyze verify.
- daemon-reload.
- Health check.
- Rollback.

### Nginx

Replace project-specific `/var/www` root and alias references with paths under:

`/home/nawaf511/empire-core-new/deploy/static`

Requirements:

- Minimal read permissions.
- ACL where necessary.
- `nginx -t`.
- Domain and route testing.
- Do not expose the entire user home.

---

## 15. Interface design

References:

- Stripe for public landing experience.
- Linear for administration.
- Vercel for service and settings organization.
- Figma for dialogs and forms.
- Notion for documentation.

Public users see:

- Official direction.
- Analysis mode.
- Effective week.
- Report date.
- Dominance delta.
- Weekly support status.
- Last update in UTC.

Public users do not see:

- EXPANDED.
- Experiment status.
- Internal disagreements.
- Governance settings.

Admin routes:

- Overview.
- Reports.
- Daily Control.
- Experiments.
- Comparisons.
- Governance.
- Audit Logs.
- Contracts.
- Settings.

Arabic is RTL and English is LTR at component level.

---

## 16. Mandatory tests

- One-contract Long advantage is bullish.
- One-contract Short advantage is bearish.
- Exact equality is neutral.
- Opposite signs produce explicit extended.
- Same signs produce non-explicit narrow.
- Investment uses Asset Manager Positions only.
- Changes cannot alter investment total direction.
- Investment never calls Day Control.
- Investment never calls TDL-M&L.
- Investment never calls TDL-S.
- Speculation never uses Positions.
- D1 and D2 use UTC.
- July 21 report becomes effective on July 27 UTC.
- EXPANDED cannot reach Public API.
- EXPANDED failure cannot stop CORE.
- Legacy paths cannot return after migration.

---

## 17. Definition of done

- Investment total direction uses Asset Manager Positions only.
- Weekly support uses Asset Manager Changes only.
- Disagreement displays “Weekly support is not confirmed.”
- Timing is disabled in investment.
- Timing runs only in speculation.
- CORE alone appears to users.
- EXPANDED is isolated and hidden.
- All calculations use UTC.
- Contracts validate.
- Tests pass.
- No active `/opt/empire-core` project references.
- No active project-specific `/var/www` references.
- All project services run from the canonical root.
- Rollback is tested.

---

## 18. Required uploads in the next conversation

Upload:

1. This complete package.
2. Full project detection report.
3. Strategic interface report.
4. `UI_BACKEND_GOVERNANCE_POLICY.yaml`
5. `ui-backend-governance-bundle.zip`
6. `backend/services/decision_governance_core/package.json`
7. `backend/services/decision_governance_core/main.cjs`
8. `apps/ndsp-raw-cot-gateway/app.py`
9. `apps/ndsp-raw-cot-gateway/requirements.txt`
10. Generated COT backend audit report.
11. Every file identified by the audit as implementing TDL, direction, or timing.

---

## 19. Status warning

“Completed” in prior discussions means:

- Approved.
- Defined as a governance rule.

It does not necessarily mean:

- Implemented in code.
- Deployed.
- Production-tested.
- Nginx or systemd migrated.
- Legacy paths deleted.

</div>
