# NDSP 16-Layer Decision Core and Future-Layer Integration Blueprint

**Official name:** NDSP — Nawaf Decision Support Platform
**Document ID:** `NDSP-16-CORE-INTEGRATION-001`
**Version:** `1.0.0`
**Effective date:** `2026-07-11`
**Status:** `GOVERNING BLUEPRINT — does not authorize calculation changes before source lock`
**Owner:** Nawaf

---

## 1. Purpose

This document defines the position of the current 16 layers inside NDSP’s future architecture and prevents treating them as 16 mandatory microservices or merging them arbitrarily.

Governing rule:

> **The current 16 layers are the decision core. Future layers protect their inputs, coordinate context around them, and prove, explain, and evaluate their outputs.**

---

## 2. What this document does not mean

- It does not create 56 decision engines.
- It does not make every layer a microservice.
- It does not change TDL, NMP, or risk formulas.
- It does not replace canonical-source verification.
- It does not authorize deleting or merging services without consumer evidence.
- It does not authorize future-layer development before backup, restore, source lock, and P0 closure.

---

## 3. Governing registry of the 16 current layers

IDs `NDSP-CORE-L01` through `NDSP-CORE-L16` are permanent even if a display name or runtime location changes.

| ID | Governing name | Family | Function | Can block |
|---|---|---|---|---|
| NDSP-CORE-L01 | Temporal Decision Logic — Medium & Long | DIRECTION_AND_TIME | Determines medium- and long-horizon directional context using governed TDL category rules. | Yes |
| NDSP-CORE-L02 | Temporal Decision Logic — Short & Speculative | DIRECTION_AND_TIME | Determines short/speculative direction and holding horizon under weekly-close governance. | Yes |
| NDSP-CORE-L03 | Governing Market Direction | DIRECTION_AND_TIME | Normalizes directional outputs into one governed context consumed by downstream layers. | Yes |
| NDSP-CORE-L04 | Correction Gate | DIRECTION_AND_TIME | Verifies the mandatory correction condition before transition to ALLOWED. | Yes |
| NDSP-CORE-L05 | Divergence Engine | DIRECTION_AND_TIME | Evaluates regular and hidden divergence using the governed indicator set. | No |
| NDSP-CORE-L06 | Temporal and Day Logic | DIRECTION_AND_TIME | Applies Day Logic V2, timeframe governance, and decision horizon rules. | Yes |
| NDSP-CORE-L07 | Scenario Levels | STRUCTURE_AND_SCENARIO | Computes activation, arrival, review, and invalidation levels per asset and timeframe. | Yes |
| NDSP-CORE-L08 | NMP Confluence Point | STRUCTURE_AND_SCENARIO | Determines the critical confluence zone and confirmation required for automated execution. | Yes |
| NDSP-CORE-L09 | Momentum Engine | CONFIRMATION_AND_CONVERGENCE | Measures movement strength and consistency with the governed scenario. | No |
| NDSP-CORE-L10 | Liquidity and Structure Confirmation | CONFIRMATION_AND_CONVERGENCE | Evaluates structure and liquidity behavior around scenario levels without creating a separate direction. | No |
| NDSP-CORE-L11 | USD and Macro Filter | RISK_AND_OPPOSITION | Adds contextual support or pressure from USD and macro conditions without directly changing TDL. | No |
| NDSP-CORE-L12 | Risk Engine | RISK_AND_OPPOSITION | Measures market, operational, and temporal risk and reduces readiness when required. | Yes |
| NDSP-CORE-L13 | Nawaf Golden Signal | CONFIRMATION_AND_CONVERGENCE | Represents governed convergence across core layers; exposed only as partial or under monitoring when appropriate. | No |
| NDSP-CORE-L14 | Enhanced Nawaf Golden Signal | CONFIRMATION_AND_CONVERGENCE | Enhanced convergence requiring additional governed conditions; never an independent execution order. | No |
| NDSP-CORE-L15 | Devil’s Advocate | RISK_AND_OPPOSITION | Stress-tests the reading against objections and conflicts after macro and risk assessment. | Yes |
| NDSP-CORE-L16 | Readiness and Decision State Machine | READINESS_AND_FINAL_STATE | Aggregates outputs and determines strength, readiness, maturity, and final decision state. | Yes |

> **Governance note:** this is a functional governing registry. During `NDSP_CANONICAL_SOURCE_LOCK`, each layer must be mapped to its real source path, service, contract, version, tests, and Git commit. This document does not authorize calculation changes before that mapping.

---

## 4. Five functional families

### 4.1 Direction and Time

`L01–L06` answer:

- What is the direction?
- For which horizon?
- Which category governs?
- Is correction present?
- Is divergence present?
- Are day and timeframe rules applied?

News does not directly change this family.

### 4.2 Structure and Scenario

`L07–L08` answer:

- Where does the scenario activate?
- Where is arrival?
- When is review required?
- When is it invalidated?
- Is NMP confirmed?

### 4.3 Confirmation and Convergence

`L09–L10` and `L13–L14` answer:

- Do momentum and structure support the reading?
- Is convergence partial or enhanced?
- Is the signal under monitoring?
- Has reading quality improved?

### 4.4 Risk and Opposition

`L11–L12` and `L15`.

Mandatory order:

```text
USD / MACRO CONTEXT
        ↓
RISK ENGINE
        ↓
DEVIL'S ADVOCATE
```

### 4.5 Readiness and Final State

`L16` aggregates outputs without recalculating them.

```text
BLOCKED → ALLOWED → ARMED → EXECUTED
```

NDSP remains a decision-support platform, not an execution system.

---

## 5. Position of future layers

### 5.1 Before the core — truth and data plane

```text
Asset Master Registry
Source Registry
Market Data Ingestion
Immutable Raw Snapshot Store
Normalization
Data Quality Gate
Provider Reconciliation
Freshness Control
Data Lineage
Economic Calendar Normalization
```

These layers never create a decision. They ensure that core inputs are trusted and traceable.

```text
NO APPROVED DATA = NO DECISION COMPUTATION
```

### 5.2 Around the core — context plane

```text
Economic Event Layer
News & Narrative Intelligence
Macro Context
Cross-Asset Transmission
Market Regime
Liquidity Context
```

Rules:

- News never changes TDL directly.
- Economic events can reduce readiness or increase caution.
- USD context feeds `L11`.
- Risk feeds `L12`.
- objections feed `L15`.
- explanation may use context after the contract is complete.

### 5.3 Above the core — coordination and governance plane

```text
Cross-Layer Conflict Engine
Reading Strength
Decision Readiness
Reading Maturity
Completion Checklist
Decision Governance
```

These consume the 16 outputs; they do not recompute them.

### 5.4 After the core — evidence and evaluation plane

```text
Decision Evidence Ledger
Historical Replay Lab
Outcome Evaluation
Confidence Calibration
Engine and Model Registry
Audit Trail
```

These preserve, replay, and evaluate decisions without rewriting historical truth.

### 5.5 Explanation and experience plane

```text
Decision Explainability
Beginner View
Professional View
Admin View
Owner View
Arabic / English / French Localization
Reports
Share Cards
Alerts
Watchlists
```

All consume only the final decision contract.

### 5.6 External integration plane

```text
External Integration Gateway
Partner API
Webhooks
Notification Delivery
Subscription and Entitlements
NDSP Bot
```

Correct flow:

```text
16-Layer Core
→ Decision Governance
→ Completed Decision Contract
→ External Integration Gateway
→ Bot / Partner / Alert
```

---

## 6. Governing execution order

```text
APPROVED DATA
→ L01 / L02
→ L03
→ L04 / L05 / L06
→ L07
→ L08
→ L09 / L10
→ L11
→ L12
→ L13
→ L14
→ L15
→ L16
→ COMPLETED DECISION CONTRACT
→ EVIDENCE LEDGER
→ EXPLANATION / ALERTS / INTEGRATIONS
```

Parallel work is allowed only when independent inputs are proven by contract.

---

## 7. What may be consolidated?

### 7.1 Presentation consolidation

Beginner users see five cards:

1. Direction.
2. Scenario.
3. Confirmation.
4. Risk.
5. Decision.

This does not merge calculation logic.

### 7.2 Runtime consolidation

Multiple layers may run in one runtime while preserving separate outputs.

```text
One Service ≠ One Layer
One Layer ≠ One Microservice
```

### 7.3 Shared-library consolidation

Allowed shared components include:

- Symbol resolution.
- Timeframe utilities.
- Closed-candle validation.
- Shared indicators.
- Contract validation.
- Logging and observability.

Decision logic is not merged without equivalence testing.

---

## 8. When may two calculation layers be merged?

Only after:

```text
Freeze contracts
→ Capture baseline outputs
→ Parallel run
→ Historical replay
→ Shadow production
→ Compare
→ Prove equivalence or improvement
→ Owner approval
→ Deprecation window
→ Rollback readiness
```

---

## 9. Standard layer contract

```json
{
  "layer_id": "NDSP-CORE-L08",
  "canonical_name": "nmp_confirmation",
  "layer_version": "1.4.0",
  "contract_version": "1.0.0",
  "asset_id": "NDSP-CRYPTO-BTC-USD",
  "timeframe": "1W",
  "as_of_utc": "2026-07-11T00:00:00Z",
  "state": "PENDING",
  "value": null,
  "confidence": 0.72,
  "blocking": true,
  "readiness_effect": -18,
  "reason_codes": ["NMP_NOT_CONFIRMED"],
  "source_snapshot_ids": [],
  "engine_commit": "git-commit",
  "trace_id": "trace-id"
}
```

Rules:

- Consumers never mutate outputs.
- Every layer declares its version.
- Every reason uses a reason code.
- Time is UTC.
- Assets use canonical `asset_id`.
- Invalid outputs enter quarantine.

---

## 10. Core aggregation contract

```json
{
  "decision_id": "ndsp-decision-id",
  "asset_id": "NDSP-CRYPTO-BTC-USD",
  "contract_version": "1.0.0",
  "core_registry_version": "1.0.0",
  "layers": {
    "NDSP-CORE-L01": {},
    "NDSP-CORE-L02": {},
    "NDSP-CORE-L03": {},
    "NDSP-CORE-L04": {},
    "NDSP-CORE-L05": {},
    "NDSP-CORE-L06": {},
    "NDSP-CORE-L07": {},
    "NDSP-CORE-L08": {},
    "NDSP-CORE-L09": {},
    "NDSP-CORE-L10": {},
    "NDSP-CORE-L11": {},
    "NDSP-CORE-L12": {},
    "NDSP-CORE-L13": {},
    "NDSP-CORE-L14": {},
    "NDSP-CORE-L15": {},
    "NDSP-CORE-L16": {}
  },
  "final_state": "ALLOWED",
  "direction": "BULLISH",
  "strength": 74,
  "readiness": 52,
  "maturity": "PARTIAL",
  "conflict_state": "MATERIAL_CONFLICT",
  "completed_at_utc": null
}
```

---

## 11. Visibility matrix

| Role | Visibility |
|---|---|
| Beginner | Five groups, simplified explanation, caution reasons, levels, final state |
| Professional | Permitted 16-layer outputs, conflicts, effects, contract versions |
| Admin | Service, contract, and data health without proprietary formulas |
| Owner | Full registry, evidence, versions, and authorized manual override |

Public names remain governed by the visibility policy.

---

## 12. Required canonical-source mapping

Each layer must receive:

```text
source_path
runtime_service
runtime_user
port
health_endpoint
input_contract
output_contract
engine_version
git_commit
test_suite
owner
consumers
rollback_version
status
```

A layer is not fully verified until these fields are populated.

---

## 13. Acceptance gates

- Layer-to-code match.
- No duplicate semantic layers.
- No unknown runtime service.
- Validatable JSON contracts.
- Unit test per layer.
- Core integration test.
- Reference historical replay.
- Conflict tests.
- BLOCKED, ALLOWED, and ARMED state tests.
- Proof that explanation does not alter decisions.

---

## 14. Activation condition

This blueprint preserves the target architecture but does not authorize calculation changes until:

```text
BACKUP_RESTORE = VERIFIED
CANONICAL_SOURCE = LOCKED
P0_RISKS = CLOSED
CURRENT_16_LAYER_REGISTRY = VERIFIED_AGAINST_SOURCE
```

**Final status:** `NDSP_16_LAYER_CORE_INTEGRATION_BLUEPRINT_ACTIVE`
