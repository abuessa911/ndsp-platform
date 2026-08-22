# NDSP Stability-First Transformation Governance

**Official name:** NDSP — Nawaf Decision Support Platform  
**Document ID:** `NDSP-STABILITY-GOV-001`  
**Version:** `1.0.0`  
**Effective date:** `2026-07-11`  
**Owner and final authority:** Nawaf  
**Status:** `GOVERNING`  
**Scope:** source, production, services, data, contracts, security, decision evidence, historical replay, and future intelligence layers.

---

## 1. Purpose

This document is the governing reference for NDSP work after the current-reality audit. It prevents uncontrolled expansion, protects the live system, and directs every engineering effort toward stability, auditability, recoverability, and commercial and scientific readiness.

This is not a conceptual note. It is an enforceable operating rule for every change, build, cleanup, and deployment.

---

## 2. Product identity and boundaries

NDSP is a **decision-support platform**. It is not an execution platform, trading bot, or direct recommendation service.

Permanent rules:

1. Deterministic engines compute the decision.
2. AI explains the decision; it does not own it.
3. News provides context; it does not own direction.
4. NDSP Bot consumes completed decisions only through an external integration gateway.
5. No UI, bot, or narrative layer may bypass decision governance.
6. Proprietary formulas, secrets, and internal administration paths must not be exposed publicly.

---

## 3. Supreme rule

> **From this point forward, every unit of effort must increase stability, not complexity.**

Operational meaning:

- No new layer before the current system is protected.
- No production change without backup and rollback testing.
- No backup is trusted until restoration is proven.
- No service, file, or version is removed before non-use is demonstrated.
- No direct editing of live deployment files except a documented emergency.
- No JSON contract change without versioning and compatibility planning.
- No decision-engine change hidden inside a UI change.
- No global expansion before stability and product value are proven.

---

## 4. Mandatory transformation order

The order may only be changed by a documented owner decision.

### Phase 0 — Safe freeze and current-reality lock

Required outputs:

- `NDSP_CURRENT_PRODUCTION_REALITY_LOCK`
- Canonical-source map.
- Domain and Nginx map.
- Service, port, and runtime-user registry.
- Database and storage registry.
- `/home`, `/opt`, `/var/www`, and `/etc` runtime map.
- Temporary do-not-touch list.
- P0, P1, and P2 risk register.

**Exit gate:** no material uncertainty remains about the production source or service responsible for each domain.

### Phase 1 — Full backup and restore verification

Required outputs:

- `NDSP_PRE_CHANGE_FULL_BACKUP`
- `NDSP_BACKUP_MANIFEST`
- `NDSP_SECRETS_ENCRYPTED_BACKUP`
- Consistent database dumps.
- Source and Git snapshot.
- `/opt` runtime snapshot.
- `/var/www` snapshot.
- Nginx, systemd, PM2, cron, and Docker snapshot.
- `SHA256SUMS`
- `RESTORE_INSTRUCTIONS`
- `NDSP_FULL_RESTORE_VERIFICATION_OK`

Rules:

1. Three copies, two media types, one off-server copy.
2. Secrets are stored in a separate encrypted package.
3. User data and secrets are never shared in chat.
4. Restore testing occurs in an isolated path or environment.
5. Backup success is not accepted without practical restore evidence.

**Exit gate:** documented restoration of source, configuration, database, and a non-production runtime sample.

### Phase 2 — Canonical-source lock

Required outputs:

- `NDSP_CANONICAL_SOURCE_LOCK`
- Official repository and production branch.
- Real source path for every application.
- Build and deployment paths.
- Every service mapped to Git-managed source.
- Protection against unverified `rsync --delete`.
- Git commit recorded for every release.
- No manual `dist` or `/var/www` edits except documented emergencies.

Canonical flow:

```text
SOURCE → BUILD → VALIDATE → PREVIEW/STAGING → APPROVE → DEPLOY → VERIFY
```

Rejected flow:

```text
EDIT LIVE FILES → TRY TO REMEMBER LATER
```

**Exit gate:** the live release can be rebuilt from a known commit using documented commands.

### Phase 3 — Service and version consolidation

Required outputs:

- `NDSP_SERVICE_REGISTRY`
- `NDSP_PORT_REGISTRY`
- `NDSP_DEPENDENCY_MAP`
- Classification of every service: governing, supporting, legacy, retirement candidate, or unknown.
- Actual consumers for each gateway and port.
- Controlled consolidation of duplicate responsibilities.
- Important `/opt` services moved under governed source or formally registered.
- Reduction of root-privileged services.
- Removal only after observation and rollback readiness.

Deletion rule:

> Never delete because of name or age. Deletion requires proof of no consumers, backup, a controlled disablement window, and rollback.

**Exit gate:** every service has an owner, source, port, runtime user, health check, consumers, and rollback plan.

### Phase 4 — Secrets and network protection

Required outputs:

- `NDSP_SECURITY_AND_SECRETS_GOVERNANCE`
- Rotation of database, JWT, SMTP, and administrative secrets.
- Git-history secret scan.
- Secrets externalized from source.
- PostgreSQL, Redis, and administration interfaces limited to localhost or private networks.
- XRDP, SSH, and SMTP review.
- Documented firewall rules.
- Rate limiting and login protection.
- Service accounts and least privilege.
- Protection of `/data/` and internal files.
- Signed webhooks and idempotency for sensitive operations.

**Exit gate:** no secret remains in source, and no sensitive port is exposed without documented approval.

### Phase 5 — Contract and logging unification

Required outputs:

- `NDSP_DATA_AND_DECISION_CONTRACT_GOVERNANCE`
- Registry for every JSON Schema.
- Explicit `contract_version`.
- Unified asset IDs and symbols.
- Unified state and error codes.
- OpenAPI for REST.
- AsyncAPI or CloudEvents for events.
- Standard log envelope containing:
  - `timestamp`
  - `service`
  - `environment`
  - `trace_id`
  - `request_id`
  - `decision_id`
  - `asset_id`
  - `contract_version`
  - `engine_version`
  - `error_code`
- Deprecation and backward-compatibility policy.
- Removal of duplicate or conflicting contracts.

**Exit gate:** every producer and consumer uses a known, validated, versioned contract.

### Phase 6 — Decision Evidence Ledger

Governing output:

- `NDSP_DECISION_EVIDENCE_LEDGER`

Each decision records:

- Decision ID.
- Asset, timeframe, and time.
- Snapshot of every input.
- Data sources and retrieval time.
- TDL, NMP, momentum, risk, and Devil’s Advocate versions.
- State-transition history.
- Activation, arrival, review, and invalidation levels.
- Manual override usage.
- Record hash and Git commit.
- Append-only history.

Rule:

> A changed decision creates a new event; the old truth is never rewritten.

**Exit gate:** any decision can be explained and reproduced using its original inputs and engine versions.

### Phase 7 — Historical Replay Laboratory

Governing output:

- `NDSP_HISTORICAL_REPLAY_LAB`

Requirements:

- Only data available at the original time.
- No unclosed candles.
- No later-revised economic values.
- No later-published news.
- Original engine versions.
- Future-leakage detection.
- Strict versus Adaptive comparisons.
- Evaluation of direction, readiness, confidence, risk, and timing.

States:

```text
REPLAY_EXACT
REPLAY_APPROXIMATE
REPLAY_INCOMPLETE
FUTURE_LEAKAGE_DETECTED
SOURCE_SNAPSHOT_MISSING
```

**Exit gate:** a representative historical set can be replayed without future leakage.

### Phase 8 — Data, news, and explanation layers

Start only after previous phases pass.

Order:

1. Asset Master Registry
2. Source Registry
3. Market Data Ingestion
4. Data Quality & Reconciliation
5. Data Lineage
6. Economic Event Layer
7. News & Narrative Intelligence
8. Cross-Layer Conflict Engine
9. Decision Explainability
10. Decision Evaluation & Calibration

Rules:

- News never changes TDL directly.
- AI explains a decision contract; it does not calculate the final decision.
- Unapproved data never enters engines.
- Material conflicts reduce readiness and invoke Devil’s Advocate.
- Beginner and professional explanations derive from the same contract.

---

## 5. Production change gate

No production change without:

```text
1. CHANGE_REQUEST
2. IMPACT_ANALYSIS
3. PRE_CHANGE_BACKUP
4. IMPLEMENTATION_PLAN
5. TEST_PLAN
6. ROLLBACK_PLAN
7. OWNER_APPROVAL
8. POST_DEPLOYMENT_VERIFICATION
9. CHANGE_REPORT
```

Execution sequence:

```text
REQUEST
→ ANALYZE
→ BACKUP
→ IMPLEMENT OUTSIDE PRODUCTION
→ TEST
→ PREVIEW/STAGING
→ APPROVE
→ DEPLOY
→ VERIFY
→ LOCK OR ROLLBACK
```

---

## 6. Change classes

- **P0 Emergency:** active breach, data loss, total outage, or database corruption.
- **P1 Critical:** exposed sensitive port, unsafe deployment, conflicting service, or unprotected authentication path.
- **P2 Foundational improvement:** contract unification, observability, privilege reduction, and log governance.
- **P3 Feature or UX improvement:** pages, design, language, and optional reports.

P0 and P1 risks take priority over new features.

---

## 7. Currently prohibited actions

Until backup restoration and canonical-source lock are complete:

- Run deployment scripts using `--delete`.
- Delete or disable a service based only on a similar name.
- Edit `/var/www` directly.
- Change TDL or NMP inside a UI fix.
- Open new ports.
- place secrets in Git or chat.
- Delete old backups before indexing them.
- Merge `/opt` services before identifying consumers.
- Rebuild authentication without migration and compatibility tests.
- Add news or AI as a governing decision owner.
- Launch wide global paid marketing before stability and compliance.

---

## 8. Engine and decision governance

Every engine has an owner, version, inputs, outputs, tests, commit, effective date, and rollback version.

Permanent decision rules include:

- No entry without correction under the approved policy.
- NMP is mandatory for automated execution and optional only for owner manual override.
- Risk and USD Macro precede Devil’s Advocate.
- Strength is not readiness.
- Direction is not confidence.
- Public visibility follows the experience visibility matrix.
- No text or news layer issues direct execution instructions.

---

## 9. UI and experience governance

- Beginner is default.
- Professional exposes detail without leaking IP.
- Admin controls authorized operations.
- Owner controls structural changes and manual override.
- The side menu is the navigation authority.
- No duplicate navigation between header and menu.
- Arabic, English, and French use shared translation keys.
- No new hard-coded user-facing strings.
- Every page has an owner, route, data contract, and acceptance test.
- Design never changes the decision contract.

---

## 10. Observability

Unify metrics, traces, logs, and alerts.

Trace path:

```text
REQUEST
→ ASSET RESOLUTION
→ DATA SOURCE
→ QUALITY GATE
→ TDL
→ NMP
→ RISK
→ CONTEXT
→ GOVERNANCE
→ RESPONSE
```

No actionable alert without `error_code`, `service`, and `trace_id`.

---

## 11. Release management

Semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Every production release records:

```text
release_id
git_commit
contract_versions
engine_versions
database_migrations
backup_id
rollback_id
deployed_at
approved_by
verification_result
```

---

## 12. Required governance files

The project must maintain:

```text
NDSP_CURRENT_PRODUCTION_REALITY_LOCK
NDSP_PRODUCTION_BUILD_AND_CHANGE_GOVERNANCE
NDSP_BACKUP_RESTORE_AND_DISASTER_RECOVERY_GOVERNANCE
NDSP_RELEASE_AND_DEPLOYMENT_RUNBOOK
NDSP_SECURITY_AND_SECRETS_GOVERNANCE
NDSP_DATA_AND_DECISION_CONTRACT_GOVERNANCE
NDSP_SERVICE_AND_PORT_REGISTRY
NDSP_SOURCE_AND_ASSET_REGISTRY
NDSP_DECISION_EVIDENCE_LEDGER_SPEC
NDSP_HISTORICAL_REPLAY_LAB_SPEC
NDSP_TESTING_AND_RELEASE_GATES
NDSP_INCIDENT_RESPONSE_RUNBOOK
```

---

## 13. Success measures

Success is not the number of files, services, engines, or pages.

Governing measures:

- Proven restoration.
- Fewer duplicate services.
- Fewer root-privileged processes.
- Zero secrets in source.
- Zero unjustified exposed sensitive ports.
- Versioned and validated contracts.
- Traceable decisions.
- Historical replay without leakage.
- Fewer deployment failures.
- Stronger retention and product trust.
- Production rebuildable from governed source.

---

## 14. Feature expansion gate

No advanced intelligence expansion or global rollout until:

```text
BACKUP_RESTORE = VERIFIED
CANONICAL_SOURCE = LOCKED
P0_RISKS = CLOSED
SERVICE_REGISTRY = COMPLETE
SECRETS = ROTATED_AND_EXTERNALIZED
CONTRACTS = VERSIONED
OBSERVABILITY = ACTIVE
DECISION_LEDGER = OPERATIONAL
```

---

## 15. Project-work-page pinned statement

> **NDSP follows a stability-first operating model. The mandatory order is: full backup and restore verification; canonical-source lock; service and version consolidation; secrets and port protection; contract and logging unification; Decision Evidence Ledger; Historical Replay Laboratory; then data, news, and explanation layers. No production change occurs without backup, test, rollback, approval, and post-deployment verification. No service is removed or merged before proving that it has no consumers. Every new unit of effort must increase stability and auditability, not complexity.**

---

## 16. Approval

This document is effective immediately and overrides older scripts or instructions that conflict with it.

Exceptions require an ADR containing the reason, duration, risks, owner, and return plan.

**Final status:** `NDSP_STABILITY_FIRST_GOVERNANCE_ACTIVE`
