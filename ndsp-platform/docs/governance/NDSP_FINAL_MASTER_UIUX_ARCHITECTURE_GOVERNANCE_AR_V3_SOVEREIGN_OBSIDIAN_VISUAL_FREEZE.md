# NDSP — Final Master UI/UX + Architecture Governance (AR)

## Merge resolution - Owner Revision 2026-08-08
MERGE, NOT REWRITE. All unique non-design requirements are preserved. The owner-approved visual identity in this revision replaces superseded legacy design language. True duplicates are consolidated into one canonical statement only. No business/backend/contracts/database ownership/runtime changes are inferred.

### Controlling revision summary
- Logo complexity: **3/10**.
- Official palette: **Deep Charcoal / Near Black + Warm Refined Metallic Gold + Controlled Sky Blue + White / Off-White**.
- Indigo/Violet is no longer the primary brand accent; Purple remains a controlled semantic color for Review/Experimental states where needed.
- The internal **16 logical Decision Layers** remain preserved and protected.
- Customer-facing UI may expose only **five approved names**, and only as **NAME-ONLY exposure**: **TDL, NMP, Nawaf Golden Signal, Enhanced Nawaf Golden Signal, Devil's Advocate**.
- The remaining **11 internal names** are not exposed to customers.
- The customer-facing plan presentation is standardized to **Free / Pro / Elite / Institutional**.
- The **16-Day Trial** may show the five approved names; after trial, visibility is controlled by the selected plan and server-side entitlement.
- Name visibility never authorizes disclosure of formulas, logic, weights, inputs, internal state, raw values, layer-level outputs, sources, producers, contracts, dependencies, or internal relationships.


## PART I — Revised Level 1 Architecture

# Revised Level 1 Repository Tree

```
```

```
ndsp-platform/
│
├── backend/
│   │
│   ├── api/
│   │   ├── public/
│   │   │   └── core_public_projection/
│   │   │
│   │   ├── admin_review/
│   │   │   ├── admin/
│   │   │   └── review/
│   │   │
│   │   ├── internal/
│   │   ├── health/
│   │   └── operations/
│   │
│   ├── exposure/
│   │   ├── public/
│   │   │   └── core_public_projection/
│   │   │
│   │   └── admin_review/
│   │       ├── analytical_projection/
│   │       ├── tdl/
│   │       ├── nmp/
│   │       │   └── experimental_review/
│   │       ├── shadow/
│   │       └── review/
│   │
│   ├── access/
│   │   ├── authentication/
│   │   ├── authorization/
│   │   ├── rbac/
│   │   ├── public_access/
│   │   ├── admin_access/
│   │   └── review_access/
│   │
│   ├── domains/
│   │   │
│   │   ├── data_foundation/
│   │   │   ├── providers/
│   │   │   │   ├── market_data/
│   │   │   │   ├── cftc/
│   │   │   │   ├── cot/
│   │   │   │   ├── tff/
│   │   │   │   ├── economic_calendar/
│   │   │   │   ├── macro_data/
│   │   │   │   ├── tradingview/
│   │   │   │   ├── investing/
│   │   │   │   └── other_verified_providers/
│   │   │   │
│   │   │   ├── ingestion/
│   │   │   ├── raw/
│   │   │   ├── normalization/
│   │   │   ├── canonical/
│   │   │   │   ├── instruments/
│   │   │   │   ├── market/
│   │   │   │   ├── cot/
│   │   │   │   ├── macro/
│   │   │   │   └── economic/
│   │   │   ├── freshness/
│   │   │   ├── quality/
│   │   │   └── lineage/
│   │   │
│   │   ├── market_intelligence/
│   │   │   ├── market_state/
│   │   │   ├── price_structure/
│   │   │   ├── trend/
│   │   │   ├── momentum/
│   │   │   ├── volatility/
│   │   │   ├── correction/
│   │   │   ├── cross_timeframe_state/
│   │   │   ├── market_regime/
│   │   │   ├── liquidity/
│   │   │   ├── macro_pressure/
│   │   │   ├── usd_pressure/
│   │   │   ├── asset_context/
│   │   │   ├── evidence/
│   │   │   ├── state/
│   │   │   └── history/
│   │   │
│   │   ├── institutional_intelligence/
│   │   │   ├── cftc_cot_tff/
│   │   │   │   ├── current_report/
│   │   │   │   ├── previous_report/
│   │   │   │   ├── historical_weekly_series/
│   │   │   │   └── normalized_tff_structure/
│   │   │   ├── asset_managers/
│   │   │   │   ├── overall/
│   │   │   │   └── weekly/
│   │   │   ├── leveraged_funds/
│   │   │   │   ├── overall/
│   │   │   │   └── weekly/
│   │   │   ├── evidence/
│   │   │   ├── state/
│   │   │   └── history/
│   │   │
│   │   ├── theory_engines/
│   │   │   ├── correction/
│   │   │   │   ├── engine/
│   │   │   │   ├── inputs/
│   │   │   │   ├── state/
│   │   │   │   ├── output/
│   │   │   │   ├── evidence/
│   │   │   │   ├── health/
│   │   │   │   └── explainability/
│   │   │   ├── momentum/
│   │   │   │   ├── engine/
│   │   │   │   ├── inputs/
│   │   │   │   ├── state/
│   │   │   │   ├── output/
│   │   │   │   ├── evidence/
│   │   │   │   ├── health/
│   │   │   │   └── explainability/
│   │   │   ├── macro/
│   │   │   │   ├── engine/
│   │   │   │   ├── inputs/
│   │   │   │   ├── state/
│   │   │   │   ├── output/
│   │   │   │   ├── evidence/
│   │   │   │   ├── health/
│   │   │   │   └── explainability/
│   │   │   └── other_verified_theories/
│   │   │       ├── engines/
│   │   │       ├── inputs/
│   │   │       ├── state/
│   │   │       ├── output/
│   │   │       ├── evidence/
│   │   │       ├── health/
│   │   │       └── explainability/
│   │   │
│   │   ├── tdl/
│   │   │   ├── modes/
│   │   │   │   ├── investment_mode/
│   │   │   │   │   └── TBD__behavior_and_contract_require_technical_freeze_evidence/
│   │   │   │   └── speculation_mode/
│   │   │   │       └── TBD__behavior_and_contract_require_technical_freeze_evidence/
│   │   │   ├── temporal_state/
│   │   │   ├── alignment/
│   │   │   ├── alignment_score/
│   │   │   ├── timeframe/
│   │   │   ├── same_timeframe_integrity/
│   │   │   ├── temporal_conflict/
│   │   │   ├── temporal_confirmation/
│   │   │   ├── evidence/
│   │   │   └── history/
│   │   │
│   │   ├── scenario_intelligence/
│   │   │   ├── positive_scenario/
│   │   │   ├── negative_scenario/
│   │   │   ├── preferred_scenario/
│   │   │   ├── conflict/
│   │   │   ├── strength/
│   │   │   ├── levels/
│   │   │   ├── evidence/
│   │   │   ├── drivers/
│   │   │   ├── invalidation/
│   │   │   └── evolution/
│   │   │
│   │   ├── nmp/
│   │   │   ├── FROZEN__NO_NEW_DEVELOPMENT/
│   │   │   ├── engine/
│   │   │   ├── state/
│   │   │   ├── value/
│   │   │   ├── level/
│   │   │   ├── timeframe/
│   │   │   ├── source/
│   │   │   ├── status/
│   │   │   ├── evidence/
│   │   │   ├── history/
│   │   │   └── explainability/
│   │   │
│   │   ├── golden/
│   │   │   ├── alignment/
│   │   │   ├── signal/
│   │   │   ├── status/
│   │   │   ├── name/
│   │   │   ├── spotlight/
│   │   │   ├── evidence/
│   │   │   ├── reason/
│   │   │   ├── missing_inputs/
│   │   │   ├── history/
│   │   │   └── explainability/
│   │   │
│   │   ├── core_official_direction/
│   │   │   ├── authority_boundary/
│   │   │   ├── producer/
│   │   │   │   └── TBD__requires_technical_freeze_evidence/
│   │   │   ├── source/
│   │   │   │   └── TBD__requires_technical_freeze_evidence/
│   │   │   └── contract/
│   │   │       └── TBD__requires_technical_freeze_evidence/
│   │   │
│   │   ├── decision_intelligence/
│   │   │   ├── orchestration/
│   │   │   ├── layers/
│   │   │   │   ├── layer_01/
│   │   │   │   ├── layer_02/
│   │   │   │   ├── layer_03/
│   │   │   │   ├── layer_04/
│   │   │   │   ├── layer_05/
│   │   │   │   ├── layer_06/
│   │   │   │   ├── layer_07/
│   │   │   │   ├── layer_08/
│   │   │   │   ├── layer_09/
│   │   │   │   ├── layer_10/
│   │   │   │   ├── layer_11/
│   │   │   │   ├── layer_12/
│   │   │   │   ├── layer_13/
│   │   │   │   ├── layer_14/
│   │   │   │   ├── layer_15/
│   │   │   │   └── layer_16/
│   │   │   ├── conflicts/
│   │   │   ├── alignment/
│   │   │   ├── evidence/
│   │   │   ├── state/
│   │   │   └── history/
│   │   │
│   │   ├── scoring/
│   │   │   ├── inputs/
│   │   │   ├── raw_score/
│   │   │   ├── commercial_score/
│   │   │   ├── score_band/
│   │   │   ├── calculation_status/
│   │   │   ├── missing_components/
│   │   │   ├── blocking_gates/
│   │   │   ├── eligibility/
│   │   │   └── history/
│   │   │
│   │   ├── governance/
│   │   │   ├── governing_inputs/
│   │   │   ├── gates/
│   │   │   ├── policies/
│   │   │   ├── freshness/
│   │   │   ├── completeness/
│   │   │   ├── blockers/
│   │   │   ├── eligibility/
│   │   │   ├── evidence/
│   │   │   ├── public_output/
│   │   │   └── launch_readiness/
│   │   │
│   │   ├── shadow/
│   │   │   └── TBD__internal_business_logic_requires_technical_freeze_evidence/
│   │   │
│   │   ├── review/
│   │   │   └── TBD__internal_business_logic_requires_technical_freeze_evidence/
│   │   │
│   │   ├── public_projection/
│   │   │   ├── core_governance_authorized_output/
│   │   │   ├── public_contract_projection/
│   │   │   ├── current_state/
│   │   │   └── history/
│   │   │
│   │   └── admin_review_projection/
│   │       ├── authorization_control/
│   │       ├── tdl/
│   │       ├── nmp_experimental_review/
│   │       ├── shadow/
│   │       ├── review/
│   │       ├── current_state/
│   │       └── history/
│   │
│   ├── capabilities/
│   │   ├── registry/
│   │   ├── runtime/
│   │   ├── dependencies/
│   │   ├── health/
│   │   ├── exposure/
│   │   └── components/
│   │       ├── capability_01/
│   │       ├── capability_02/
│   │       ├── capability_03/
│   │       ├── capability_04/
│   │       ├── capability_05/
│   │       ├── capability_06/
│   │       ├── capability_07/
│   │       ├── capability_08/
│   │       ├── capability_09/
│   │       ├── capability_10/
│   │       ├── capability_11/
│   │       ├── capability_12/
│   │       ├── capability_13/
│   │       ├── capability_14/
│   │       ├── capability_15/
│   │       ├── capability_16/
│   │       ├── capability_17/
│   │       ├── capability_18/
│   │       ├── capability_19/
│   │       ├── capability_20/
│   │       ├── capability_21/
│   │       ├── capability_22/
│   │       ├── capability_23/
│   │       ├── capability_24/
│   │       ├── capability_25/
│   │       ├── capability_26/
│   │       ├── capability_27/
│   │       └── capability_28/
│   │
│   ├── explainability/
│   │   ├── market/
│   │   ├── institutional/
│   │   ├── theories/
│   │   ├── tdl/
│   │   ├── scenarios/
│   │   ├── nmp/
│   │   ├── golden/
│   │   ├── decision/
│   │   ├── scoring/
│   │   ├── governance/
│   │   └── data_quality/
│   │
│   ├── security/
│   │   ├── authentication/
│   │   ├── authorization/
│   │   ├── rbac/
│   │   ├── secrets_management/
│   │   ├── configuration/
│   │   ├── api_separation/
│   │   └── operational_permissions/
│   │
│   ├── orchestration/
│   │   ├── pipelines/
│   │   ├── dependency_graph/
│   │   └── runtime/
│   │
│   └── shared/
│       ├── types/
│       ├── validation/
│       └── technical_utilities/
│
├── frontend/
│   ├── public/
│   │   ├── app/
│   │   ├── layouts/
│   │   ├── components/
│   │   ├── services/
│   │   ├── state/
│   │   ├── contracts/
│   │   └── features/
│   │       └── core_public_projection/
│   │
│   └── admin_review/
│       ├── app/
│       ├── layouts/
│       ├── components/
│       ├── services/
│       ├── state/
│       ├── contracts/
│       └── features/
│           ├── command_center/
│           ├── market_intelligence/
│           ├── institutional_intelligence/
│           ├── theory_lab/
│           ├── tdl/
│           ├── scenario_intelligence/
│           ├── nmp/
│           │   └── experimental_review/
│           ├── golden_alignment/
│           ├── decision_intelligence/
│           ├── capability_matrix/
│           ├── data_intelligence/
│           ├── governance_center/
│           ├── score_intelligence/
│           ├── explainability/
│           ├── shadow/
│           ├── review/
│           └── platform_health/
│
├── database/
│   ├── raw/
│   │   ├── market/
│   │   ├── cftc/
│   │   ├── macro/
│   │   ├── economic/
│   │   └── providers/
│   ├── normalized/
│   │   ├── market/
│   │   ├── institutional/
│   │   ├── macro/
│   │   └── economic/
│   ├── canonical/
│   │   ├── instruments/
│   │   ├── market/
│   │   ├── cot/
│   │   ├── macro/
│   │   └── economic/
│   ├── intelligence/
│   │   ├── market/
│   │   ├── institutional/
│   │   ├── theories/
│   │   ├── tdl/
│   │   ├── scenarios/
│   │   ├── nmp/
│   │   └── golden/
│   ├── decision/
│   │   ├── runs/
│   │   ├── layers/
│   │   ├── conflicts/
│   │   └── evidence/
│   ├── scoring/
│   │   ├── inputs/
│   │   ├── results/
│   │   └── history/
│   ├── governance/
│   │   ├── inputs/
│   │   ├── gates/
│   │   ├── blockers/
│   │   ├── eligibility/
│   │   └── history/
│   ├── public_projection/
│   │   ├── core/
│   │   ├── current/
│   │   └── history/
│   ├── admin_review_projection/
│   │   ├── current/
│   │   └── history/
│   ├── core_official_direction/
│   │   └── TBD__ownership_and_storage_require_technical_freeze_evidence/
│   ├── shadow/
│   │   └── TBD__ownership_requires_technical_freeze_evidence/
│   ├── review/
│   │   └── TBD__ownership_requires_technical_freeze_evidence/
│   ├── explainability/
│   │   ├── evidence/
│   │   ├── reasons/
│   │   └── relationships/
│   ├── platform/
│   │   ├── capabilities/
│   │   ├── runtime_state/
│   │   └── health/
│   ├── current_state/
│   ├── history/
│   ├── audit/
│   ├── lineage/
│   ├── cache/
│   └── archive/
│
├── contracts/
│   ├── internal/
│   ├── canonical/
│   ├── governance/
│   ├── public/
│   │   └── core_public_projection/
│   ├── admin_review/
│   ├── core_official_direction/
│   │   └── TBD__requires_technical_freeze_evidence/
│   └── versions/
│
├── jobs/
│   ├── ingestion/
│   ├── synchronization/
│   ├── canonicalization/
│   ├── calculations/
│   ├── quality/
│   ├── scheduled_evaluation/
│   └── maintenance/
│
├── infrastructure/
│   ├── systemd/
│   ├── timers/
│   ├── scheduling/
│   ├── reverse_proxy/
│   ├── deployment/
│   ├── environment/
│   ├── runtime_users/
│   ├── service_ownership/
│   ├── backup/
│   └── health_monitoring/
│
├── observability/
│   ├── service_health/
│   ├── provider_health/
│   ├── data_freshness/
│   ├── engine_health/
│   ├── capability_health/
│   ├── api_health/
│   ├── governance_health/
│   ├── job_health/
│   ├── metrics/
│   ├── logs/
│   ├── diagnostics/
│   └── alerts/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contracts/
│   ├── theories/
│   ├── data_quality/
│   ├── governance/
│   ├── authorization/
│   ├── exposure_boundaries/
│   ├── regression/
│   └── end_to_end/
│
├── docs/
│   ├── architecture/
│   ├── contracts/
│   ├── theories/
│   ├── governance/
│   ├── data/
│   └── operations/
│
├── config/
├── tools/
│
└── var/
    ├── runtime/
    ├── audits/
    ├── snapshots/
    └── archives/
```

# Revised Service Boundary Diagram









```
```

```
External Providers
        │
        ▼
Data Foundation
 ├─ Raw / Normalized / Canonical / Quality / Lineage
 └─ ONE Canonical COT Dataset
        │
        ├──────────────► Market Intelligence
        ├──────────────► Institutional Intelligence
        │                 └─ CFTC / COT / TFF analytics
        ├──────────────► Theory Engines
        └──────────────► TDL
                          ├─ Investment Mode
                          └─ Speculation Mode
                             behavior/contracts:
                             TBD — requires technical freeze evidence

Market + Institutional + Theory + TDL
                  │
                  ▼
              Scenarios
                  │
            ┌─────┴─────┐
            ▼           ▼
          NMP          Golden
  FROZEN / NO NEW       │
     DEVELOPMENT        │
            │           │
            └─────┬─────┘
                  │
 Market ──────────┤
 Institutional ───┤
 Theory Engines ──┤
 TDL ─────────────┤
 Scenarios ───────┤
                  ▼
        Decision Intelligence
        ├─ Orchestration
        ├─ Decision Layers 01–16
        │  [logical components only]
        ├─ Conflict / Alignment
        ├─ Evidence
        └─ State / History
                  │
                  ├────────────► Scoring
                  │
                  ▼
    CORE Official Direction Authority
    Producer: TBD
    Source: TBD
    Contract: TBD
    — requires technical freeze evidence
                  │
                  ▼
              Governance
              /        \
             /          \
            ▼            ▼
 CORE Public Projection  Admin / Review Projection
 Public-authorized only  Authorization-controlled
            │            ├─ TDL
            │            ├─ NMP [Experimental/Review]
            │            ├─ Shadow
            │            └─ Review
            ▼
       Public API

Capabilities 01–28 remain logical components only.
No 1:1 Capability → microservice assumption.
```

# Revised Backend-to-Database Mapping

- **Data Foundation →** **`database/raw/`****\*\*\*\*,** **`database/normalized/`****\*\*\*\*,** **`database/canonical/`**. It remains the authoritative owner of financial canonical data. `database/canonical/cot/` remains the **ONE Canonical COT Dataset**. Institutional Intelligence consumes it; it does not write a competing canonical COT dataset.
- **Market Intelligence →** **`database/intelligence/market/`**. Owns market-derived state and history only. It does not own canonical market observations.
- **Institutional Intelligence →** **`database/intelligence/institutional/`**. Owns derived CFTC/COT/TFF intelligence, including current/previous/historical analytical state. Its authoritative upstream institutional dataset remains `database/canonical/cot/`.
- **Theory Engines →** **`database/intelligence/theories/`**. Own theory state, results, evidence and history within the theory boundary. No assumption is made that each theory is a separate service.
- **TDL →** **`database/intelligence/tdl/`**. Existing TDL ownership is preserved. Investment Mode and Speculation Mode are architectural operating modes inside the TDL boundary. Their formulas, behavioral differences, persistence subdivision and contracts remain `TBD — requires technical freeze evidence`.
- **Scenario Intelligence →** **`database/intelligence/scenarios/`**. Owns scenario state, evidence, levels, drivers, invalidation and evolution.
- **NMP →** **`database/intelligence/nmp/`**. Existing ownership is preserved, but the domain is now explicitly **`FROZEN / NO NEW DEVELOPMENT`**. Existing state/history may remain readable internally. No new architecture-stage feature development is assigned to NMP.
- **Golden →** **`database/intelligence/golden/`**. Existing Golden ownership is unchanged.
- **CORE Official Direction Authority →** **`database/core_official_direction/`** **only as an unresolved ownership placeholder**. Authoritative producer, upstream source, storage authority and contract are `TBD — requires technical freeze evidence`. No competing producer or derived authority is assigned.
- **Decision Intelligence →** **`database/decision/`**. Owns decision runs, the state of **16 logical Decision Layers**, conflicts and evidence. The 16 layers remain logical components, not 16 databases or microservices.
- **Scoring →** **`database/scoring/`**. Owns score-input representations, calculation results and scoring history; it does not acquire ownership of upstream TDL, Scenario, NMP, Golden or Theory state.
- **Governance →** **`database/governance/`**. Remains the authoritative owner of governance evaluations, gates, blockers and eligibility. It is the mandatory boundary before any public exposure.
- **Public Projection →** **`database/public_projection/core/`****\*\*\*\*,** **`current/`****\*\*\*\*,** **`history/`**. This store may contain only **governance-authorized CORE public projection**. NMP, TDL, Shadow and Review data are prohibited from entering this public projection.
- **Admin/Review Projection →** **`database/admin_review_projection/`**. This is a separate read/exposure projection for authorized internal surfaces. It may expose TDL, frozen NMP, Shadow and Review information according to authorization. NMP is explicitly labeled **Experimental/Review** here.
- **Shadow →** **`database/shadow/`** **ownership remains** **`TBD — requires technical freeze evidence`**. The boundary exists; internal business logic and final data-authority rules are not invented at Level 1.
- **Review →** **`database/review/`** **ownership remains** **`TBD — requires technical freeze evidence`**. The boundary exists; internal business logic and final state ownership remain unresolved.
- **Capabilities →** **`database/platform/capabilities/`****\*\*\*\*,** **`runtime_state/`****\*\*\*\*,** **`health/`**. All **28 logical Capabilities** remain within capability architecture; there is no automatic database or service per capability.
- **Explainability / Evidence →** **`database/explainability/`**. Cross-domain relationships remain traceable as Result → Why → Evidence → Source without moving authoritative business state into Explainability.
- **Audit →** **`database/audit/`**, **Lineage →** **`database/lineage/`**, **History →** **`database/history/`**, **Cache →** **`database/cache/`**, **Archive →** **`database/archive/`** preserve their prior roles. Cache remains read acceleration, never source of truth.
- **Frontend has zero direct database ownership or read path.** Both Public and Admin/Review frontends consume backend API/projection boundaries only. Direct frontend → internal intelligence database access remains prohibited.

# Public vs Admin/Review Exposure Diagram









```
```

```
                         RBAC / AUTHORIZATION
                         /                  \
                        /                    \
                       ▼                      ▼

                PUBLIC EXPOSURE        ADMIN / REVIEW EXPOSURE
                ───────────────        ───────────────────────

CORE Official Direction               TDL
Authority Boundary                    ├─ Investment Mode
        │                              └─ Speculation Mode
        ▼
    Governance                        NMP
        │                             ├─ FROZEN
        │                             └─ Experimental / Review
        ▼
Governance-authorized                 Shadow
CORE Public Projection                └─ Internal logic TBD
        │
        ▼                             Review
    Public API                        └─ Internal logic TBD
        │
        ▼                                  │
 Public Frontend                           ▼
                                          Admin / Review
 ONLY CORE public                          Projection
 projection may                           │
 reach this path.                         ▼
                                     Admin / Review API
                                          │
                                          ▼
                                     Admin / Review
                                        Frontend


PROHIBITED PUBLIC FLOWS
───────────────────────
TDL ──────────────X──► CORE Public Projection
NMP ──────────────X──► CORE Public Projection
Shadow ───────────X──► CORE Public Projection
Review ───────────X──► CORE Public Projection

NMP ──────────────X──► Public API
Internal DB ──────X──► Public Frontend
Internal DB ──────X──► Admin/Review Frontend

AUTHORIZED INTERNAL FLOW
────────────────────────
TDL / NMP / Shadow / Review
        │
        ▼
authorization + governance controls
        │
        ▼
Admin / Review Projection
        │
        ▼
Admin / Review API
        │
        ▼
Admin / Review Frontend
```

# TBD items requiring technical freeze verification

- **CORE Official Direction authoritative producer** — `TBD — requires technical freeze evidence`.
- **CORE Official Direction authoritative source and ownership/storage location** — `TBD — requires technical freeze evidence`.
- **CORE Official Direction internal/authoritative contract** — `TBD — requires technical freeze evidence`.
- **Exact TDL Investment Mode behavior, formulas, activation rules and contract** — `TBD — requires technical freeze evidence`.
- **Exact TDL Speculation Mode behavior, formulas, activation rules and contract** — `TBD — requires technical freeze evidence`.
- **Exact Shadow internal business logic, producer, contract and data ownership** — `TBD — requires technical freeze evidence`.
- **Exact Review internal business logic, producer, contract and data ownership** — `TBD — requires technical freeze evidence`.
- **Detailed RBAC role/permission matrix for Public vs Admin vs Review identities** — `TBD — requires technical freeze evidence`; only the architectural separation and authorization requirement are frozen at this level.
- **Exact Admin/Review projection contract contents beyond the mandated inclusion class of authorized TDL, Experimental/Review NMP, Shadow and Review information** — `TBD — requires technical freeze evidence`.

## PART II — Final UI/UX + Visual Design Governance

# NDSP — حوكمة معمارية تجربة المستخدم والتصميم البصري وتصميم الصفحات

**الحالة:** مرجع حوكمة معتمد للتصميم  
**النطاق:** UI/UX، Information Architecture، Page Design، Visual Design System، Navigation، Exposure Boundaries  
**التطبيق:** Public Experience + Public User Workspace + Admin / Review Experience  
**القاعدة:** لا تعدّل هذه الوثيقة العقود التقنية أو منطق الأعمال أو ملكية البيانات المثبتة في التقرير الرئيسي.

---

# 1. قاعدة الدمج مع التقرير الرئيسي

هذا القسم يضاف إلى التقرير الاستراتيجي الشامل دون حذف محتوياته.

عند وجود تعارض بين تصميم UI/UX قديم في التقرير وبين هذا المرجع، يعتمد هذا المرجع في **موضوع التصميم فقط**.

لا يغيّر هذا المرجع:

- Backend Architecture
- Database Ownership
- Service Boundaries
- ONE Canonical COT Dataset
- Decision Layers 01–16
- Capabilities 01–28
- Governance Authority
- Existing Contracts
- Runtime Evidence
- Security Contracts
- Deployment Architecture

أي معلومة تقنية غير مثبتة تبقى:

`TBD — requires technical freeze evidence`

---

# 2. الرؤية البصرية العليا

## 2.1 الهوية الجديدة الحاكمة

يجب ألا يبدو NDSP كلوحة تداول تقليدية.

الهوية البصرية الرسمية الجديدة:

- **Deep Charcoal / Near Black**: الأساس المؤسسي المسيطر.
- **Warm Refined Metallic Gold**: سلطة العلامة، الفخامة الهادئة، وSelective CORE emphasis.
- **Controlled Sky Blue / Light Cyan-Blue**: التحليل، البيانات، Evidence، والسياق التقني كعنصر ثانوي.
- **White / Off-White**: النصوص والتباين العالي.

**Logo complexity = 3/10.** القوة تأتي من geometry، proportion، negative space، typography، وprecision، لا من كثرة التفاصيل.

لا يُستخدم Indigo/Violet كـPrimary Brand Accent في التصميم الجديد. يبقى Purple/Violet فقط كدلالة semantic محدودة لـReview/Experimental عند الحاجة.


الهوية المستهدفة هي:

**Institutional Decision Intelligence Platform**

وتجمع بين:

- Financial Intelligence Terminal
- Decision Intelligence Platform
- Research System
- Governed Analytical Engine

اللغة البصرية يجب أن تكون:

- مؤسسية
- فاخرة بهدوء
- تحليلية
- دقيقة
- عالية الثقة
- غير استعراضية
- منظمة حتى عند ارتفاع كثافة المعلومات

السلطة والوضوح أهم من الزخرفة.

---

# 3. الفصل الأساسي للتجربة

يتكون NDSP من ثلاثة أسطح:

```text
NDSP
│
├── Public Experience
│
├── Authenticated Public User Workspace
│
└── Admin / Review Experience
````

هذا الفصل ليس مجرد Navigation أو CSS.

بل هو:

**Feature Boundary + Route Boundary + API Boundary + Exposure Boundary + Authorization Boundary**

---

# 4. مسار Public الحاكم

```
```

```
Internal Intelligence
        ↓
Decision Intelligence
        ↓
Scoring
        ↓
CORE Official Direction Authority
        ↓
Governance
        ↓
Authorized Public Output
        ↓
CORE Public Projection
        ↓
Public API
        ↓
Public Frontend
```

ولا يجوز:

```
```

```
Public Frontend → Internal Intelligence Database
```

ولا:

```
```

```
Decision → Public Projection directly
```

ولا:

```
```

```
Scoring → Public Projection directly
```

Governance هو حد النشر النهائي.

---

# 5. Public Experience

Public Experience يجب أن يكون:

-  هادئًا 
-  بسيطًا 
-  Executive-oriented 
-  أقل كثافة من Admin 
-  Mobile-first / Mobile-friendly 
-  متمحورًا حول CORE 
-  خاليًا من المصطلحات الداخلية المحمية 

ولا يكون نسخة مصغرة من Admin.

---

# 6. Landing Page

الصفحة الأولى تبدأ بـHeader بسيط يحتوي على:

-  NDSP Brand 
-  Public Navigation 
-  Sign In 
-  Language Switcher 
-  Public System Status إذا سمحت Governance 

ثم Hero رئيسي.

## CORE Hero

أعلى عنصر بصري في Public يجب أن يكون:

**CORE Official Direction**

ويمكن أن يحتوي، حسب Public Contract:

-  Asset / Symbol 
-  Current Official Direction 
-  Timestamp 
-  Freshness 
-  Governance Status 
-  Public Evidence Indicator 
-  Public Explainability Summary 

ولا يعرض:

-  TDL internal data / state / logic 
-  NMP internal data / state / logic 
-  Shadow 
-  Review 
-  Internal Decision Layer names / state / logic 
-  Internal Scoring 
-  Theory Lab 
-  Raw COT Intelligence 
-  Internal Contracts 

---

# 7. Public Scroll Narrative

بعد CORE Hero يسير المستخدم في تسلسل:

```
```

```
CORE Official Direction
        ↓
Market Context
        ↓
Why This Direction?
        ↓
Evidence
        ↓
Freshness
        ↓
Governance Trust
        ↓
Methodology / Transparency
```

Public Experience يجب أن يكون أقرب إلى:

**Executive Intelligence Product**

من Dashboard تقليدية.

---

# 8. Public User Workspace

بعد تسجيل الدخول العام:

```
```

```
Overview
→ CORE
→ Market Context
→ Evidence
→ Methodology
→ Account
```

الشاشة الرئيسية تتمحور حول:

**CORE Official Direction Card**

ثم:

-  Market Context Summary 
-  Evidence Summary 
-  Explainability Summary 
-  Freshness 
-  Governance Publication State 
-  Decision Intelligence Access - NAME-ONLY حسب الباقة
-  Current Plan / Entitlement / Upgrade State

يمكن إضافة Asset Selector أو Timeframe Selector فقط إذا سمح Public Contract بذلك.

---

# 9. Public Guardrails

يحظر في Public / Customer surfaces كشف:

- Shadow وReview وأي Experimental internals.
- Decision Intelligence internals.
- أسماء أو ترتيب Decision Layers 01–16 الداخلية.
- Internal Scoring.
- Theory Lab.
- Raw COT Analytics.
- Capability Matrix.
- Internal Evidence غير المصرح بها.
- Internal Logs / Contracts / Database Access.
- TDL/NMP/Golden/Devil's Advocate logic, formulas, weights, inputs, internal state, raw values, layer-level outputs/results, producers, sources, contracts, dependencies, and internal relationships.

## 9.1 NAME-ONLY Exposure Exception

يسمح للعميل برؤية **خمسة أسماء فقط** وفق Entitlement:

1. **TDL - Temporal Decision Logic**
2. **NMP - Nawaf Meet Point**
3. **Nawaf Golden Signal - إشارة نواف الذهبية**
4. **Enhanced Nawaf Golden Signal - إشارة نواف الذهبية المعززة**
5. **Devil's Advocate - محامي الشيطان**

هذا السماح هو **NAME-ONLY**. لا يعني السماح بنتيجة الطبقة أو تفسير منطقها أو كشف سرها.

أسماء الـ11 المتبقية لا تظهر للمستخدم إطلاقًا، ولا في DOM أو API أو hidden routes أو metadata أو logs أو accessibility labels.

**Server-side entitlement is mandatory. CSS-only locking is forbidden.** لا يجوز إرسال السر إلى المتصفح ثم إخفاؤه بصريًا.

---

# 10. Admin / Review Experience

Admin/Review هو:

**Mission Control for Decision Intelligence**

ويكون:

-  Desktop-first 
-  Analytical 
-  Information-dense 
-  Evidence-driven 
-  Governance-aware 
-  Keyboard-friendly 
-  Role-aware 

مع فصل واضح عن Public.

---

# 11. Admin Navigation

```
```

```
Command Center
→ Data Intelligence
→ Market Intelligence
→ Institutional Intelligence
→ Theory Lab
→ TDL
→ Scenarios
→ NMP Review
→ Golden
→ CORE Review
→ Decision Intelligence
→ Scoring
→ Governance
→ Shadow / Review
→ Capability Matrix
→ Explainability
→ Operations & Security
```

هذا Navigation Reference وليس processing pipeline.

---

# 12. Admin Command Center

يعمل كـMission Control.

الصف العلوي يعرض:

-  Platform Health 
-  Governance State 
-  Data Freshness 
-  Provider Health 
-  Engine Health 
-  Blockers 
-  Alerts 

ثم المجالات الرئيسية:

-  CORE 
-  Governance 
-  Scoring 
-  Market Intelligence 
-  Institutional Intelligence 
-  TDL 
-  Scenarios 
-  Golden 
-  Decision Intelligence 

لا تتحول الصفحة إلى عشرات البطاقات المتساوية بصريًا.

الأولوية:

```
```

```
Primary Decision State
→ Governance
→ Supporting Intelligence
→ Evidence
→ Operational Context
```

---

# 13. Data Intelligence

تعرض:

-  External Providers 
-  Ingestion 
-  Canonicalization 
-  Freshness 
-  Quality 
-  Lineage 
-  Provider Health 
-  Evidence 

ويظهر:

**ONE Canonical COT Dataset**

كمصدر canonical موحد.

---

# 14. Market Intelligence

تستخدم مناطق تحليلية مرتبة:

```
```

```
Market State
Price Structure
Trend
Momentum
Volatility
Correction
Regime
Liquidity
Macro / USD Pressure
Evidence
History
```

ويكون drill-down:

**RESULT → WHY → EVIDENCE → SOURCE**

---

# 15. Institutional Intelligence

تتمحور حول:

-  CFTC 
-  COT 
-  TFF 
-  Current Report 
-  Previous Report 
-  Weekly History 
-  Asset Managers 
-  Leveraged Funds 
-  Evidence 
-  History 

مع إظهار أن upstream هو:

**ONE Canonical COT Dataset**

---

# 16. Theory Lab

يعرض المحركات المثبتة فقط.

مثل:

-  Correction 
-  Momentum 
-  Macro 
-  Other Verified Theories 

النمط الموحد:

```
```

```
Inputs
→ Current State
→ Output
→ Evidence
→ Health
→ Explainability
```

لا يعني ظهور Theory أنها microservice مستقلة.

---

# 17. TDL

TDL:

**Admin / Review Only**

يحتوي على:

```
```

```
Investment Mode | Speculation Mode
```

لكن behavior/formulas/contracts تبقى:

`TBD — requires technical freeze evidence`

ويمكن عرض:

-  Temporal State 
-  Alignment 
-  Timeframe Integrity 
-  Conflict 
-  Confirmation 
-  Evidence 
-  History 

---

# 18. Scenario Intelligence

تعرض السيناريوهات ككيانات مقارنة:

-  Positive Scenario 
-  Negative Scenario 
-  Preferred Scenario 

مع:

-  Conflict 
-  Strength 
-  Levels 
-  Drivers 
-  Evidence 
-  Invalidation 
-  Evolution 

ويفضل:

**Scenario Comparison + Evolution Timeline**

---

# 19. NMP Review

يظهر دائمًا:

**NMP — FROZEN / NO NEW DEVELOPMENT**

و:

**Experimental / Review**

وهو Admin/Review only.

يمكن عرض الموجود فقط:

-  State 
-  Value 
-  Level 
-  Timeframe 
-  Source 
-  Status 
-  Evidence 
-  History 

ولا يوجد CTA لتطوير NMP جديد.

---

# 20. Golden Alignment

الترتيب البصري:

```
```

```
Alignment Summary
        ↓
Signal / Status
        ↓
Evidence Chain
        ↓
Reason / Missing Inputs
        ↓
Historical Changes
```

---

# 21. CORE Review

CORE Official Direction هو أحد أقوى العناصر البصرية في Admin.

يعرض:

-  Current Official Direction 
-  Current State 
-  Governance Relationship 
-  Evidence Chain 
-  History 
-  Publication Relationship 

لكن Authority Metadata غير المثبتة تبقى:

```
```

```
Producer: TBD
Source: TBD
Contract: TBD

TBD — requires technical freeze evidence
```

---

# 22. Decision Intelligence

تعرض:

**Decision Layers 01–16**

بدون اختراع أسماء.

أفضل visual representation:

**Decision Layer Rail / Decision Stack**

ويبرز:

-  Active State 
-  Conflict 
-  Alignment 
-  Evidence 
-  History 

ولا يوحي بوجود 16 microservices.

---

# 23. Scoring

الترتيب:

```
```

```
Score Inputs
↓
Raw Score
↓
Commercial Score
↓
Band
↓
Calculation Status
↓
Missing Components
↓
Blocking Gates
↓
Eligibility
↓
History
```

ويجب فصل:

**Score Result**

عن:

**Governance Approval**

بصريًا ووظيفيًا.

---

# 24. Governance Center

هذه من أقوى صفحات النظام.

تبدأ بـ:

**Publication Decision / Eligibility State**

ثم:

-  Governing Inputs 
-  Freshness 
-  Completeness 
-  Gates 
-  Policies 
-  Blockers 
-  Evidence 
-  Launch Readiness 
-  Audit 

وتنتهي بـ:

**Authorized Public Output**

وهو الحد الوحيد الذي يسمح بالعبور إلى Public Projection.

---

# 25. Shadow / Review

Workspace داخلي مستقل.

**Admin / Review Only**

أي logic غير مثبت:

`TBD — requires technical freeze evidence`

ولا يدخل Public Contract.

---

# 26. Capability Matrix

تعرض:

**Capabilities 01–28**

كـlogical capabilities.

يمكن عرض:

-  Registry Status 
-  Runtime State 
-  Dependencies 
-  Health 
-  Exposure 
-  Evidence 

ولا يتم اختراع الأسماء أو افتراض microservice لكل Capability.

---

# 27. Explainability & Evidence Explorer

المبدأ المركزي:

```
```

```
RESULT
 ↓
WHY
 ↓
EVIDENCE
 ↓
SOURCE
 ↓
LINEAGE
```

ويستخدم progressive disclosure بدل إظهار كل التفاصيل دفعة واحدة.

---

# 28. Operations & Security

مساحة مستقلة لـ:

-  Authentication 
-  Authorization 
-  RBAC 
-  Audit 
-  Observability 
-  Provider Health 
-  Service Health 
-  Logs 
-  Diagnostics 
-  Alerts 
-  Platform State 

ولا تخلط مع financial intelligence.

---

# 29. Visual Design System

## Admin / Review

الخلفيات:

-  Near-black 
-  Charcoal 
-  Deep neutral surfaces 

مع:

-  Soft gray borders 
-  High contrast primary text 
-  Low contrast metadata 
-  Minimal elevation 
-  Controlled accent colors 

## Public

يمكن استخدام:

-  Light neutral canvas 

أو:

-  Deep neutral canvas 

لكن مع:

-  generous whitespace 
-  CORE-dominant hierarchy 
-  minimal navigation 
-  evidence summary 
-  governance trust signals 

---

# 30. Semantic Color System

الألوان ليست decorative.

```
```

```
Healthy / Authorized / Positive → Green
Warning / Review               → Amber
Blocked / Critical             → Red
Intelligence / Analysis        → Controlled Sky Blue
Experimental / Review          → Controlled Purple
Neutral                         → Gray / Charcoal
Brand Authority / CORE Emphasis → Warm Refined Metallic Gold
Primary Text                    → White / Off-White
```

لا يستخدم اللون وحده لنقل المعنى.

كل حالة مهمة تستخدم:

**Color + Label + Icon/Shape عند الحاجة**

---


## 30B. Official NDSP Brand & Logo Direction

**Logo complexity: 3/10.**

الشعار يجب أن يكون Minimal، Clean، Highly Recognizable، Premium، Institutional، Intelligent، Timeless، وقابلاً للتوسع من favicon حتى التقارير والعروض المؤسسية.

**Brand Category:** Governed Institutional Decision Intelligence Platform.

### Official palette

| Role | Approved direction |
|---|---|
| Primary foundation | Deep Charcoal / Near Black |
| Brand authority / CORE emphasis | Warm Refined Metallic Gold |
| Analytical secondary | Controlled Sky Blue / Light Cyan-Blue |
| Primary typography | White / Off-White |
| Positive / Authorized | Green |
| Warning / Review | Amber |
| Blocked / Critical | Red |
| Experimental / Review | Controlled Purple |

### Logo construction

- Sophistication through geometry, proportion, negative space, typography, precision.
- Gold must be warm, executive, restrained; never bright yellow or casino-like.
- Sky Blue must remain technical and secondary; it must not dominate the charcoal/gold identity.
- The brand philosophy is: **Intelligence converges into an authorized decision.**
- Avoid candlestick logos, trading arrows, bulls/bears, crypto coins, dollar signs, generic brain/AI sparkle, neon cyberpunk, casino gold, gaming typography, and complex 3D emblems.

# 31. System States

يجب توحيد:

-  Fresh 
-  Stale 
-  Partial 
-  Loading 
-  Error 
-  Blocked 
-  Unauthorized 
-  Experimental 
-  Review 
-  Frozen 
-  Missing Inputs 
-  No Data 

في كامل المنظومة.

---

# 32. Typography

الخط الأساسي:

**Modern Neutral Sans**

الهرمية:

1.  Display Titles 
2.  Page Headings 
3.  Section Headings 
4.  Body 
5.  Labels 
6.  Numeric Emphasis 
7.  Metadata 

Monospace يستخدم فقط لـ:

-  IDs 
-  timestamps 
-  code 
-  contracts 
-  technical metadata 

ولا يستخدم كنمط عام.

---

# 33. Grid

Admin Desktop:

**12-column analytical grid**

Tablet:

**8 columns**

Mobile:

**4 columns**

Spacing يعتمد:

**4px base unit**

لكن Public يستخدم generous spacing أكبر من Admin.

---

# 34. Layout Principle

لا تبنى الصفحة كشبكة من عشرات البطاقات.

الترتيب الأفضل:

```
```

```
PRIMARY INSIGHT
      ↓
SUPPORTING INTELLIGENCE
      ↓
EVIDENCE
      ↓
OPERATIONAL CONTEXT
```

---

# 35. Signature Components

يجب تطوير Design System حول مكونات NDSP المميزة:

-  CORE Direction Card 
-  Governance Badge 
-  Freshness Indicator 
-  Evidence Strength 
-  Domain Header 
-  Decision Layer Rail 
-  Capability Matrix 
-  Scenario Comparison 
-  Data Lineage Trace 
-  Alert Rail 
-  Explainability Drawer 
-  KPI Tile 
-  Status Pill 
-  Evidence Panel 
-  Analytical Card 
-  Timeline 
-  Filter Bar 

---

# 36. CORE Visual Dominance

CORE يجب أن يكون أعلى عنصر بصري من حيث hierarchy في المواضع التي يكون فيها القرار الرسمي هو السياق الرئيسي.

لا يعني ذلك استخدام حجم مبالغ فيه.

بل:

-  Position 
-  Typography 
-  Contrast 
-  Whitespace 
-  Context 
-  Governance relationship 

هي التي تعطيه السلطة البصرية.

---

# 37. Motion

الحركة subtle ومقصودة.

مسموح:

-  Fast page transition 
-  Gentle fade 
-  Small translate 
-  Panel reveal 
-  Drawer transition 
-  Status transition 
-  Single update pulse 

غير مرغوب:

-  Continuous glow 
-  Particle effects 
-  Decorative loops 
-  Excessive glass effects 
-  Large animated backgrounds 
-  Gaming-style effects 

---

# 38. Update Animation

عند تغير Status أو Score:

لا تستخدم animation استعراضية.

يستخدم:

```
```

```
Old State
→ smooth transition
→ New State
→ optional single subtle pulse
```

فقط عند وجود update حقيقي.

---

# 39. Explainability Motion

يفضل progressive reveal:

```
```

```
RESULT
   ↓
WHY
   ↓
EVIDENCE
   ↓
SOURCE
```

بدل فتح عدد كبير من modals.

---

# 40. Ambient Intelligence

يمكن استخدام ambient intelligence بشكل محدود.

أمثلة:

-  subtle tonal background لـMarket Regime 
-  freshness halo صغير 
-  evidence strength bar 
-  restrained confidence indicator 
-  active Decision Layer highlighting 

لكن هذه العناصر لا تستبدل labels النصية.

---

# 41. Charts

Charts تتبع لغة موحدة.

يمكن أن تشمل:

-  Price / Context 
-  Institutional History 
-  Scenario Comparison 
-  Decision Layer State 
-  Score History 
-  Freshness / Health 
-  Evidence Relationships 

ولا يعتمد chart على اللون وحده.

---

# 42. Chart Density

لا تستخدم visualization ضخمة عندما يكون:

-  table 
-  compact chart 
-  timeline 
-  status rail 

أكثر وضوحًا.

الرسوم تخدم القرار ولا تتحول إلى decoration.

---

# 43. KPI Discipline

لا تعرض أكثر من:

**3–5 KPIs رئيسية**

في viewport واحد إلا إذا كانت طبيعة workspace تتطلب غير ذلك.

يجب التمييز بين:

-  Primary KPIs 
-  Secondary Metrics 
-  Metadata 

---

# 44. Admin Mission Control Layout

التكوين المرجعي:

```
```

```
GLOBAL CONTEXT HEADER
────────────────────────

SYSTEM / GOVERNANCE STATUS RAIL
────────────────────────

CORE / GOVERNANCE / SCORING
────────────────────────

SUPPORTING INTELLIGENCE
────────────────────────

EVIDENCE / HISTORY / OPERATIONS
```

مع Sidebar أو role-aware navigation.

---

# 45. Global Context

عندما تسمح العقود:

-  Asset 
-  Symbol 
-  Market 
-  Timeframe 

تظهر كـpersistent global context في Admin.

تغييرها يجب أن ينتقل عبر العقود المعتمدة ولا تقوم الواجهة باختراع propagation logic.

---

# 46. Public Cinematic Direction

"Cinematic" هنا لا يعني animations ضخمة.

بل يعني:

-  Strong visual focus 
-  Large section separation 
-  Controlled typography 
-  Calm gradients 
-  Smooth narrative flow 
-  Minimal navigation 
-  High-quality transitions 

Public لا يجب أن يبدو كمنتج Crypto/Gaming.

---

# 47. Glass Effects

يمكن استخدام glass-like surfaces بحذر شديد في Public.

في Admin:

يفضل:

**Solid / Deep Analytical Surfaces**

على excessive glass.

الوضوح أهم من المؤثر البصري.

---

# 48. Accessibility

إلزامي:

-  Keyboard Navigation 
-  Visible Focus 
-  WCAG-aware Contrast 
-  Screen Reader Labels 
-  Semantic HTML 
-  Reduced Motion 
-  Status Not Color Only 
-  Accessible Charts 
-  Accessible Tables 
-  Accessible Dialogs 
-  RTL/LTR 

---

# 49. Responsive Behavior

Public:

**Mobile priority**

Admin:

**Desktop analytical priority**

Tablet:

**Review mode**

Admin Mobile:

**Limited complexity**

لا يتم إجبار analytical workspace كثيفة على هاتف إذا أضر ذلك بسلامة المراجعة.

---

# 50. RTL / LTR

Arabic:

`lang="ar" dir="rtl"`

English:

`lang="en" dir="ltr"`

Code / JSON / technical contracts:

LTR.

ويجب أن تكون directionality جزءًا من component system.

---

# 51. Security by Design

الحماية لا تعتمد على:

`display:none`

ولا conditional rendering وحده.

بل على:

```
```

```
Feature Registry
+ Route Boundary
+ API Boundary
+ Authentication
+ Authorization
+ RBAC
+ Exposure Registry
+ Governance
+ Tests
```

---

# 52. Public vs Admin/Review Exposure

```
```

```
PUBLIC
────────────────────────────
CORE Public Projection
Market Context
Public Evidence
Public Explainability
Methodology
Account
────────────────────────────
AUTHORIZATION / GOVERNANCE
BOUNDARY
────────────────────────────
ADMIN / REVIEW
Data Intelligence
Market Intelligence
Institutional Intelligence
Theory Lab
TDL
Scenarios
NMP
Golden
CORE Review
Decision Intelligence
Scoring
Governance
Shadow / Review
Capability Matrix
Explainability Explorer
Operations & Security
────────────────────────────
```

---

# 53. الصور المرجعية المعتمدة

يتم إدراج الصور الثلاث المرفقة في التقرير كما يلي:

## Figure UI-01 — NDSP Visual Design System Mindmap

**الصورة:**
 `888888888888888888888888888888888888888888888888888888888888.png`

توضع بعد قسم:

**Visual Design System**

وتمثل:

-  Color System 
-  Typography 
-  Grid 
-  Spacing 
-  Motion 
-  Public Experience 
-  Admin Review Experience 
-  Guardrails 
-  Components 
-  Accessibility 
-  Responsive Behavior 
-  System States 

ويجب التعامل معها كـ:

**Visual Design Reference**

وليس backend architecture.

---

## Figure UI-02 — NDSP UI/UX Information Architecture Mindmap

**الصورة:**
 `111111111111111111111111111111111111111111111111111111111111111111111111111111.png`

توضع بعد قسم:

**UI/UX Information Architecture**

وتمثل:

-  Public Experience 
-  Public User Workspace 
-  Public Detail Pages 
-  Public Guardrails 
-  Admin Review Experience 
-  Domain Workspaces 
-  Governance Center 
-  Decision Intelligence 
-  Scoring 
-  TDL 
-  NMP 
-  Golden 
-  Capability Matrix 
-  Explainability 
-  Operations & Security 

وتعد:

**Information Architecture Reference**

---

## Figure UI-03 — NDSP Public vs Admin/Review Exposure Architecture

**الصورة:**
 `22222222222222222222222222222222222222222222222222222222.png`

توضع بعد قسم:

**Security / Exposure Architecture**

وتمثل الحد الحاكم:

```
```

```
Internal Intelligence Stores
        │
        ├── Admin / Review Path
        │
        └── Governance-controlled Public Path
                     ↓
             CORE Public Projection
                     ↓
                 Public API
                     ↓
              Public Frontend
```

وتعد:

**Exposure Boundary Reference**

ولا تستخدم لإثبات producer أو contract غير مثبت.

---

# 54. ترتيب الصور في التقرير

الترتيب المعتمد:

```
```

```
UI/UX Information Architecture
        ↓
Figure UI-02
        ↓
Visual Design System
        ↓
Figure UI-01
        ↓
Security / Exposure Architecture
        ↓
Figure UI-03
```

---

# 55. Design Governance Rule

أي صفحة جديدة يجب أن تجيب قبل تنفيذها:

1.  هل هي Public أم Admin/Review؟ 
2.  ما Exposure Classification؟ 
3.  ما API Contract؟ 
4.  هل البيانات Governance-authorized؟ 
5.  ما Primary Insight؟ 
6.  ما Evidence Path؟ 
7.  ما Freshness State؟ 
8.  ما Error/Blocked State؟ 
9.  هل تدعم RTL/LTR؟ 
10.  هل تدعم Accessibility؟ 
11.  هل تحتوي معلومات داخلية غير مسموحة؟ 
12.  هل اخترع التصميم business logic غير مثبت؟ 

إذا كانت الإجابة على السؤال الأخير نعم:

**STOP — TECHNICAL FREEZE REQUIRED**

---

# 56. قاعدة عدم الاختراع

التصميم لا يحدد من تلقاء نفسه:

-  Producer 
-  Authority 
-  Formula 
-  Contract 
-  Capability Name 
-  Decision Layer Name 
-  TDL Mode Behavior 
-  Shadow Logic 
-  Review Logic 
-  Scoring Formula 
-  Governance Rule 

غير المثبت.

يستخدم:

`TBD — requires technical freeze evidence`

---

# 57. NMP Freeze

```
```

```
NMP_STATUS=FROZEN
NMP_NEW_DEVELOPMENT=NO
NMP_CLASSIFICATION=EXPERIMENTAL_REVIEW_INTERNAL
NMP_INTERNAL_DATA_EXPOSURE=ADMIN_REVIEW_ONLY
NMP_CUSTOMER_SAFE_NAME_ONLY_EXPOSURE=ENTITLEMENT_AUTHORIZED
NMP_LOGIC_FORMULA_STATE_OUTPUT_EXPOSURE=FORBIDDEN
```

---

# 58. Public Projection Rule

```
```

```
INTERNAL_EXISTENCE
≠
PUBLIC_AUTHORIZATION
```

ولا يصبح شيء Public إلا عبر:

```
```

```
Governance
→ Authorized Public Output
→ CORE Public Projection
→ Public API
→ Public Experience
```

---

# 59. Visual Design Approval State

```
```

```
NDSP_VISUAL_IDENTITY=INSTITUTIONAL_DECISION_INTELLIGENCE
LOGO_COMPLEXITY=3_OF_10
BRAND_FOUNDATION=DEEP_CHARCOAL_NEAR_BLACK
BRAND_AUTHORITY_ACCENT=WARM_REFINED_METALLIC_GOLD
ANALYTICAL_SECONDARY_ACCENT=CONTROLLED_SKY_BLUE
PRIMARY_TEXT=WHITE_OFF_WHITE
INDIGO_VIOLET_AS_PRIMARY_BRAND=SUPERSEDED
PURPLE_USAGE=REVIEW_EXPERIMENTAL_SEMANTIC_ONLY
PUBLIC_STYLE=CALM_EXECUTIVE_INTELLIGENCE
ADMIN_STYLE=DEEP_ANALYTICAL_MISSION_CONTROL
CORE_VISUAL_PRIORITY=HIGHEST
SEMANTIC_COLOR_SYSTEM=REQUIRED
SYSTEM_STATE_LANGUAGE=REQUIRED
MOTION=SUBTLE_ONLY
REDUCED_MOTION=REQUIRED
ADMIN_GRID=12_COLUMN_DESKTOP
TABLET_GRID=8_COLUMN
MOBILE_GRID=4_COLUMN
SPACING_BASE=4PX
PUBLIC_WHITESPACE=GENEROUS
ADMIN_INFORMATION_DENSITY=CONTROLLED_HIGH
RESULT_WHY_EVIDENCE_SOURCE=PRIMARY_EXPLAINABILITY_PATTERN
ACCESSIBILITY=REQUIRED
RTL_LTR=REQUIRED
```

---

# 60. UI/UX Architecture Approval State

```
```

```
PUBLIC_ADMIN_BOUNDARY=REQUIRED
PUBLIC_PROJECTION_ONLY=REQUIRED
PUBLIC_DIRECT_INTERNAL_DB_ACCESS=FORBIDDEN
ADMIN_DIRECT_INTERNAL_DB_ACCESS=FORBIDDEN
ADMIN_REVIEW_AUTHORIZATION=REQUIRED
RBAC=REQUIRED
PUBLIC_DISPLAY_REGISTRY=REQUIRED
SUBSCRIPTION_ENTITLEMENT_SERVER_SIDE=REQUIRED
CSS_ONLY_LOCKING=FORBIDDEN
UNAUTHORIZED_DATA_TO_BROWSER=FORBIDDEN
CUSTOMER_VISIBLE_LAYER_NAMES=5
VISIBLE_NAME_01=TDL
VISIBLE_NAME_02=NMP
VISIBLE_NAME_03=NAWAF_GOLDEN_SIGNAL
VISIBLE_NAME_04=ENHANCED_NAWAF_GOLDEN_SIGNAL
VISIBLE_NAME_05=DEVILS_ADVOCATE
TDL_INTERNAL_EXPOSURE=FORBIDDEN
TDL_NAME_ONLY_EXPOSURE=ENTITLEMENT_AUTHORIZED
NMP_INTERNAL_EXPOSURE=FORBIDDEN
NMP_NAME_ONLY_EXPOSURE=ENTITLEMENT_AUTHORIZED
HIDDEN_11_INTERNAL_LAYER_NAMES_EXPOSURE=FORBIDDEN
LAYER_LOGIC_FORMULAS_WEIGHTS_INPUTS_SOURCES_CONTRACTS=FORBIDDEN
SHADOW_PUBLIC_EXPOSURE=FORBIDDEN
REVIEW_PUBLIC_EXPOSURE=FORBIDDEN
CAPABILITY_MATRIX_PUBLIC_EXPOSURE=FORBIDDEN
ONE_CANONICAL_COT_DATASET=PRESERVED
DECISION_LAYERS=01_TO_16_LOGICAL
CAPABILITIES=01_TO_28_LOGICAL
CORE_AUTHORITY_METADATA=TECHNICAL_FREEZE_REQUIRED
```

---


# 61. حوكمة المصطلحات الحساسة وحماية الأسرار

NDSP يحتوي على ملكية فكرية ومنطق تحليلي داخلي. القاعدة الحاكمة:

**Internal existence ≠ Public authorization.**

- لا تُشتق Public labels من internal identifiers تلقائيًا.
- لا تُعرض internal engine names أو formulas أو weights أو contract names أو producer/source mappings.
- لا تظهر الأسرار عبر HTML IDs، CSS classes، routes، URLs، query parameters، ARIA، alt text، analytics events، browser logs، source maps أو error messages.
- لا يجوز إرسال البيانات السرية إلى المتصفح ثم إخفاؤها.
- يجب أن يسبق العرض: Governance → Exposure Classification → Subscription Entitlement → Approved Public Display Mapping → API Projection → Customer Interface.

# 62. الأسماء الخمسة الوحيدة المسموح للعميل برؤيتها

1. **TDL - Temporal Decision Logic**
2. **NMP - Nawaf Meet Point**
3. **Nawaf Golden Signal - إشارة نواف الذهبية**
4. **Enhanced Nawaf Golden Signal - إشارة نواف الذهبية المعززة**
5. **Devil's Advocate - محامي الشيطان**

هذه الأسماء هي **Customer Display Abstraction**. لا تُستخدم لتسمية Decision Layers 01-16 داخليًا ولا لإثبات تطابق 1:1 مع ترقيمها.

الـ11 المتبقية تبقى **Protected Intelligence** بلا أسماء أو ترتيب أو وصف يكشف البنية.

# 63. حدود NAME-ONLY Exposure

| مسموح للعميل | ممنوع كشفه |
|---|---|
| اسم الطبقة المصرح به حسب الباقة | المنطق، الخوارزمية، المعادلات، الأوزان |
| حالة Entitlement: متاح / غير متاح | Inputs الداخلية، raw values، layer-level outputs/results |
| وصف تجاري عام للقيمة | Producer، Source، Contract، dependencies |
| زر ترقية / مقارنة باقة | أسماء الـ11 المحمية أو ترتيبها |
| اسم الباقة وحالة الاشتراك | DB paths، service names، internal IDs، debug metadata |

أي نتيجة خاصة بطبقة منفردة غير الاسم تحتاج **Public Contract مستقل + Governance approval**. هذا التقرير لا يمنح هذا الإذن.

# 64. الباقات الأربع المعتمدة في تجربة العميل

التصميم الجديد يوحّد Customer-Facing Plans على:

1. **Free**
2. **Pro**
3. **Elite**
4. **Institutional**

المسميات القديمة مثل Insight / NMP Pro / Elite 16 / NDSP SaaS تعامل كـLegacy traceability ولا تستخدم في الواجهة الجديدة.

## Entitlement matrix

| السياق / الباقة | أسماء الطبقات الظاهرة | قاعدة الحماية |
|---|---|---|
| **16-Day Trial** | TDL + NMP + Nawaf Golden Signal + Enhanced Nawaf Golden Signal + Devil's Advocate | الأسماء فقط طوال التجربة؛ لا منطق ولا أسرار ولا raw layer outputs |
| **Free** | TDL | Name-only baseline بعد انتهاء التجربة إذا لم توجد ترقية معتمدة |
| **Pro** | TDL + NMP | Name-only؛ enforced server-side |
| **Elite** | الخمس جميعًا | Name-only؛ الوصول التجاري الأعلى لا يساوي كشف الملكية الفكرية |
| **Institutional** | الخمس جميعًا | Name-only + مزايا مؤسسية متعاقد عليها؛ لا كشف للمنطق الداخلي |

الأسعار، حدود الأصول، API allowances، user limits، retention، SLA وأي حدود تجارية أخرى يجب أن تأتي من Billing/Subscription Contract أو Configuration، لا من hard-coded UI.

# 65. تجربة الترقية والباقات

- Pricing/Plans تعرض أربع بطاقات واضحة: Free / Pro / Elite / Institutional.
- Feature Matrix تستخدم مفاهيم تجارية آمنة مثل Analytical Depth وEvidence Context وDecision Intelligence.
- Locked state لا يحتوي الاسم السري خلف blur أو asterisks؛ السر لا يصل أصلًا إلى Frontend.
- عند نهاية تجربة 16 يومًا يتبع العرض Entitlement الباقة المختارة، أو Free baseline إذا لم توجد ترقية مدفوعة معتمدة.
- Admin/Owner RBAC منفصل تمامًا عن Subscription Entitlement.

# 66. Decision Intelligence Access Component

مكوّن موحد يعرض:

- Visible approved name.
- Entitlement badge.
- Protected Intelligence summary without hidden names.
- Current Plan.
- Upgrade CTA عند الحاجة.

لا يعرض 01-16 كقائمة أسماء للعميل، ولا يكشف أسماء الطبقات المحمية في DOM/API/metadata.

# 67. الصفحة العامة مقابل مساحة العميل

Landing/Public غير المسجل يبقى CORE-first ولا يتحول إلى مخطط تقني. صفحة Pricing يمكنها وصف الباقات وطبقاتها المسماة المعتمدة، بشرط عدم تجاوز الأسماء الخمسة. Customer Workspace بعد المصادقة هو المكان الأساسي لتطبيق Entitlement الأسماء.

# 68. Final UI/UX + Confidentiality Approval State

```text
OWNER_REVISION=2026-08-08
VISUAL_IDENTITY=CHARCOAL_GOLD_SKYBLUE
LOGO_COMPLEXITY=3_OF_10
CUSTOMER_VISIBLE_NAMES=5_NAME_ONLY
HIDDEN_INTERNAL_NAMES=11_PLUS_ALL_UNAPPROVED_TERMS
TRIAL_DAYS=16
CUSTOMER_PLANS=FREE_PRO_ELITE_INSTITUTIONAL
ENTITLEMENT_ENFORCEMENT=SERVER_SIDE
SECRETS_SENT_TO_BROWSER=FORBIDDEN
UNIQUE_CONTENT_PRESERVED=YES
TRUE_DUPLICATES_CONSOLIDATED=YES
```

# 69. القاعدة النهائية

NDSP يجب أن يبيّن **عمق الذكاء** الذي يقدمه دون أن يمنح المستخدم أو المنافس **خريطة مجانية لأسرار هذا الذكاء**.



NDSP لا يُصمم كـTrading Dashboard.

NDSP يُصمم كـ:

**Governed Institutional Decision Intelligence Platform**

Public يرى:

**النتيجة الرسمية المصرح بها + السياق + الأدلة العامة + الشفافية.**

Admin/Review يرى:

**الذكاء + الأدلة + العلاقات + القرار + Scoring + Governance + التشغيل**

وفق الصلاحيات.

والقاعدة النهائية:

> Public sees only what Governance explicitly authorizes for public projection.

> Admin/Review receives internal analytical exposure only through authenticated and authorized boundaries.

> Visual design must reinforce architecture, never bypass it.

---


# 70. Owner Visual Freeze — SOVEREIGN OBSIDIAN (CONTROLLING DESIGN-ONLY REFERENCE)

هذه المراجعة هي **التجميد البصري الحاكم** لتصميم NDSP. تطبق قاعدة **MERGE, NOT REWRITE**: جميع متطلبات Architecture وBusiness Logic وContracts وDatabase Ownership وRuntime وExposure وConfidentiality وSubscription Entitlement تبقى كما هي. هذه المراجعة تستبدل فقط أي لغة تصميمية أقدم تتعارض بصريًا مع المرجع المرفق.

## 70.1 Visual precedence

عند وجود تعارض بصري بين نص أقدم وبين هذه المراجعة، تكون الأولوية بالترتيب:

1. **Figure UI-04 — Sovereign Obsidian Master Theme Board**.
2. الرموز والقيم الرقمية في هذا القسم.
3. **Figure UI-05 — Public Hero / Evidence-to-CORE Composition Reference**.
4. بقية النصوص التصميمية السابقة، ما لم تكن متطلبات Architecture / Exposure / Accessibility / Security.

اسم الثيم الحاكم:

**SOVEREIGN OBSIDIAN — NDSP Decision Intelligence Visual System**

الوضع الافتراضي للمنتج:

**Dark Institutional / Sovereign Obsidian**

أي Light mode مستقبلي يجب أن يكون Variant محكومًا من نفس النظام، ولا يغير الثيم الافتراضي أو معنى الألوان الدلالية.

## 70.2 Exact brand color system

| Role | Token | Exact value |
|---|---|---|
| Page Canvas / Deep Charcoal | `--ndsp-canvas` | `#080D10` |
| Refined Gold / Authority | `--ndsp-gold` | `#D4AF37` |
| Sky Blue / Intelligence | `--ndsp-sky` | `#29B6F6` |
| Off-White / Primary Text | `--ndsp-off-white` | `#F5F6F7` |
| Authorized Green | `--ndsp-authorized` | `#2FB67C` |
| Warning Amber | `--ndsp-warning` | `#D89C3A` |
| Critical Red | `--ndsp-critical` | `#D95C5C` |
| Review Purple | `--ndsp-review` | `#8B6BD9` |

الاستخدام الحاكم:

- Gold = Brand Authority / CORE / primary governed CTA / selected authority emphasis.
- Sky Blue = Evidence / Intelligence / data paths / focus / analytical accent.
- Green = Authorized / Healthy only.
- Amber = Warning only.
- Red = Critical / Blocked only.
- Purple = Review / Experimental only.
- Off-White = primary text.
- لا يستخدم Gold كبديل للألوان الدلالية.

## 70.3 Exact surfaces and borders

| Role | Exact value |
|---|---|
| Page Canvas | `#080D10` |
| Surface | `#111518` |
| Surface Elevated | `#161C24` |
| Surface Disabled | `#0F1319` |
| Border | `1px #262C36` |
| Border Subtle | `1px #1D232C` |

الحواف والسطوح يجب أن تكون Solid / Deep Analytical، مع elevation محدود. Glass غير مسموح كطبقة رئيسية.

## 70.4 Typography freeze

**Font pairing: IBM Plex Sans Arabic (AR) + Inter (EN).**

Monospace يبقى للاستخدام التقني المحدود فقط.

| Level | Use | Size / Line height | Weight |
|---|---|---:|---|
| H1 | Large Title / عنوان كبير | `48 / 56` | Bold |
| H2 | Section Title / عنوان متوسط | `32 / 40` | SemiBold |
| H3 | Sub Title / عنوان صغير | `24 / 32` | SemiBold |
| Body 1 | Body / Paragraph | `16 / 24` | Regular |
| Body 2 | Secondary Text | `14 / 20` | Regular |
| Caption | Caption / Label | `12 / 16` | Regular |
| Micro | Micro Text | `11 / 16` | Regular |

العربية RTL والإنجليزية LTR جزء من Component System وليستا معالجة لاحقة.

## 70.5 Spacing, radius, borders and shadows

Spacing system in pixels:

`4, 8, 12, 16, 24, 32, 48, 64`

Radius system:

`4px, 8px, 12px`

Border system:

`1px #262C36`

Shadow system — subtle and restrained:

- Small: `0 1px 2px rgba(0,0,0,.25)`
- Medium: `0 4px 12px rgba(0,0,0,.30)`
- Large: `0 12px 32px rgba(0,0,0,.35)`

## 70.6 Logo and brand lockup

الـPublic Header يستخدم **NDSP full lockup** كما في Figure UI-04/UI-05:

- رمز NDSP الهندسي Gold مع Sky Blue tip.
- حروف NDSP بالـOff-White.
- العبارة العربية: **منصة نواف لدعم القرار**.
- لا يستخدم placeholder بحرف `N`.
- لا يستخدم شعار Trading أو Candlestick أو Crypto أو AI sparkle.
- Logo complexity يبقى `3/10`.

## 70.7 CORE Authority Card — exact visual language

CORE ليس Card عام. هو Signature Authority Component ويستخدم:

- خلفية Deep Surface.
- إطار Gold رفيع.
- Gold convergence highlight موضعي ومحدود.
- تقسيمات رأسية رفيعة.
- أيقونات line-based بالذهبي.
- النصوص العامة المصرح بها فقط.

Public-safe authority labels المعتمدة بصريًا:

**CORE | الاتجاه الرسمي | معتمد حوكميًا | أدلة قابلة للتحقق**

هذه العبارات لا تمنح إذنًا لكشف producer/source/logic/formula/state/internal relationships.

## 70.8 Public Hero composition — controlling composition

الـLanding Hero يجب أن يطابق Figure UI-05 في التكوين البصري:

### Header
- Logo أعلى اليمين.
- Navigation محدود: **المنهجية / الحوكمة**.
- **تسجيل الدخول** أعلى اليسار بإطار Gold.
- لا تتحول الـPublic navigation إلى قائمة Admin.

### Hero copy — right side
العنوان:

**منصة نواف لدعم القرار**

السطر الحاكم:

**كل الأدلة. اتجاه رسمي واحد.**

الوصف:

**ذكاء مؤسسي محكوم يحوّل السياق المعقد إلى قرار واضح يمكن تفسيره.**

Primary CTA:

**ابدأ تجربتك لمدة 16 يومًا**

Secondary CTA:

**اعرف لماذا**

### Evidence convergence — left side
تظهر خمسة مسارات عامة آمنة بصريًا:

- بيانات مؤسسية
- تقارير وتحليلات
- سياق تشغيلي
- معلومات خارجية
- معايير وسياسات

تتقارب المسارات بـSky Blue نحو نقطة convergence ذهبية ثم تدخل إلى CORE Authority Card.

هذه labels هي **Public Narrative Categories** وليست mappings إلى internal engines أو Decision Layers أو Providers بعينها. أي بيانات فعلية تحتها يجب أن تأتي من Public Contract وGovernance-authorized projection.

### Journey strip
أسفل الـHero:

**01 السياق → 02 الأدلة → 03 الاتجاه الرسمي**

ويستخدم Gold للسلطة وSky Blue للأدلة/السياق، مع فصل بصري رفيع.

## 70.9 Controlled glow and evidence motion

التصميم المرفق يسمح استثناءً محسوبًا بـ:

- Localized Gold convergence glow عند نقطة التقاء الأدلة وداخل CORE edge.
- Thin evidence-flow lines.
- Sparse Sky Blue evidence points.
- One-time line reveal عند دخول الـHero.
- Gentle Fade.
- Small Translate.
- Single Update Pulse عند تغير حالة حقيقية.

لا يسمح بـ:

- Full-screen continuous glow.
- Decorative particle fields.
- Gaming / cyberpunk neon.
- Large animated backgrounds.
- Continuous ornamental loops.

بذلك يكون الـGlow **authority/evidence cue** وليس effect layer.

## 70.10 Component system

المظهر الحاكم للمكونات:

- Primary Button: Gold filled, dark text, restrained highlight.
- Secondary Button: Deep surface + subtle neutral border.
- Text Link: Sky Blue.
- Inputs/Selectors: Deep surface, `1px #262C36`, Sky Blue focus.
- Governance Badge: icon + label، Gold/semantic according to meaning.
- Freshness Indicator: icon/dot + label، لا يعتمد على اللون وحده.
- Evidence Strength: segmented Sky Blue bars + label.
- Status Pills: icon + label + semantic color.
- Cards: Surface/Elevated tokens، borders رفيعة، shadows restrained.
- Tables/Admin surfaces: Dense, analytical, dark, legible، بنفس token system.

## 70.11 Admin / Review visual language

Admin/Review يستخدم نفس Sovereign Obsidian system مع كثافة أعلى:

- Sidebar role-aware.
- Deep analytical panels.
- Compact tables.
- Filters and selectors.
- Governance/status rails.
- No cinematic empty space equivalent to Public hero.
- Gold يبقى Authority emphasis؛ Sky Blue يبقى analytical.
- Review Purple لا يظهر إلا لحالة Review/Experimental الفعلية.

لا يغير هذا أي RBAC أو Exposure Boundary.

## 70.12 Accessibility and responsive freeze

إلزامي:

- AA Contrast.
- RTL/LTR.
- Visible focus ring باستخدام Sky Blue.
- Reduced Motion.
- Keyboard navigation.
- Status = icon + label + color.
- Desktop preserves the Figure UI-05 composition.
- Tablet/Mobile يعيدان ترتيب العناصر دون تحويل CORE أو الأدلة إلى مخطط داخلي كاشف.

## 70.13 Design-only approval state

```text
OWNER_VISUAL_REVISION=2026-08-08_SOVEREIGN_OBSIDIAN
CONTROLLING_THEME=SOVEREIGN_OBSIDIAN
DEFAULT_MODE=DARK_INSTITUTIONAL
PAGE_CANVAS=#080D10
SURFACE=#111518
SURFACE_ELEVATED=#161C24
SURFACE_DISABLED=#0F1319
BORDER=#262C36
BORDER_SUBTLE=#1D232C
AUTHORITY_GOLD=#D4AF37
INTELLIGENCE_SKY_BLUE=#29B6F6
PRIMARY_TEXT=#F5F6F7
AUTHORIZED_GREEN=#2FB67C
WARNING_AMBER=#D89C3A
CRITICAL_RED=#D95C5C
REVIEW_PURPLE=#8B6BD9
FONT_AR=IBM_PLEX_SANS_ARABIC
FONT_EN=INTER
SPACING=4_8_12_16_24_32_48_64
RADIUS=4_8_12
BORDER_WIDTH=1PX
MOTION=GENTLE_FADE_SMALL_TRANSLATE_SINGLE_UPDATE_PULSE
PUBLIC_HERO=EVIDENCE_CONVERGENCE_TO_CORE
CORE_AUTHORITY_CARD=REQUIRED_SIGNATURE_COMPONENT
PUBLIC_INTERNAL_MAPPING_EXPOSURE=FORBIDDEN
ACCESSIBILITY=AA_RTL_LTR_REDUCED_MOTION
```

**Figure UI-04 — Sovereign Obsidian Master Theme Board:** المرجع البصري الشامل الحاكم للألوان، Typography، surfaces، states، CORE Authority Card، components، spacing، radius، borders، shadows، motion، accessibility، Public Hero وAdmin analytical surface.

**Figure UI-05 — Public Hero / Evidence-to-CORE Composition Reference:** المرجع الحاكم لتكوين الـLanding Hero: الأدلة العامة تتقارب بصريًا نحو CORE ثم تظهر رحلة السياق → الأدلة → الاتجاه الرسمي.



**END OF NDSP UI/UX + VISUAL DESIGN GOVERNANCE**

## Design-only black/gold resolution

- **Sovereign Obsidian** is the controlling default institutional theme: Page Canvas `#080D10`, Surface `#111518`, Elevated `#161C24`.
- Refined Gold `#D4AF37` is Brand / CORE authority; Sky Blue `#29B6F6` is Evidence / Intelligence.
- Green/Amber/Red/Purple remain semantic status colors with the exact values frozen in Section 70.
- Localized CORE/convergence glow and sparse evidence-flow points are allowed exactly as in the controlling theme board; continuous ambient glow, decorative particle fields, and gaming effects remain forbidden.

# Appendix A — المحتوى الاستراتيجي الأصلي: الفريد محفوظ والتصميم القديم مستبدل بالهوية الجديدة

> preserved verbatim in DOCX appendix for traceability. Design conflicts are governed by the precedence matrix above.

# التقرير الاستراتيجي المحدث لبناء واجهات المنصة

يتضمن هذا الإصدار التقرير السابق مع إضافة فصل مرجعي للتوجهات البصرية والتقنية المقترحة. هذه المرجعيات تُستخدم كمصادر إلهام تصميمية وهندسية، وليست نسخًا حرفيًا لهوية أي منتج.

## اعتماد المرجعيات

تم اعتماد Stripe وLinear وVercel وFigma وNotion كمرجعيات تصميم وهندسة للاستفادة من مبادئها وتجارب الاستخدام، دون نسخ الهوية البصرية أو المكونات أو العلامات التجارية حرفيًا.

## التقنيات المعتمدة

يبقى المشروع متعدد التقنيات: Node.js وExpress للخدمات الأساسية، Python مع Uvicorn لبعض خدمات البيانات، React مع Vite للواجهات، واستخدام TypeScript في الواجهات الجديدة قدر الإمكان.

## واجهة المستخدم العامة (مرجعية Stripe)

واجهة تسويقية بسيطة تتضمن Hero واضحًا، ورسومًا مبسطة لمسار البيانات، وCTA، وبطاقات مزايا، مع عرض نتائج CORE الرسمية فقط وعدم إظهار EXPANDED.

## لوحة الإدارة (مرجعية Linear)

Sidebar ثابت، جداول سريعة، مرشحات متقدمة، اختصارات لوحة مفاتيح، تحديثات دون إعادة تحميل، وإظهار حالات CORE/EXPANDED والإدارة الداخلية فقط.

## الإعدادات (مرجعية Vercel)

عرض الخدمات كمكونات مستقلة مع الحالة والإصدار وآخر تشغيل وآخر تقرير وسلامة التشغيل والبيئة وسجل الحوكمة، وتقسيم الإعدادات إلى General وPerspectives وDay Control وUTC وShadow Testing وPermissions وAudit وAPI Contracts.

## الحوارات (مرجعية Figma)

كل عملية حساسة تستخدم Dialog يوضح ما الذي سيتغير وما الذي لن يتغير وتأثيره والإصدار الحالي والجديد وسبب التعديل والمعتمد وتوقيت التنفيذ UTC، مع أزرار صريحة مثل Save as Draft وPromote to CORE.

## التوثيق (مرجعية Notion)

مركز توثيق داخلي هرمي يشمل Governance Overview وTerminology وAPI Contracts وDecision Records وChangelog مع دعم العربية RTL والإنجليزية LTR.

## الهوية البصرية

الهوية البصرية الجديدة: Deep Charcoal / Near Black كأساس، Warm Refined Metallic Gold كـPrimary Brand Authority Accent، Controlled Sky Blue كـSecondary Analytical Accent، وWhite / Off-White للنصوص. تبقى Green/Amber/Red/Controlled Purple ألوانًا دلالية للحالات، ولا يعتمد أي معنى على اللون وحده.

## دعم اللغات

دعم RTL وLTR على مستوى المكونات، مع بقاء JSON والأكواد LTR، وعدم خلط العربية والإنجليزية في نفس الكتلة.

## هيكل الصفحات

المستخدم النهائي: Home وMethodology وCurrent Analysis وDocumentation وSign In. الإدارة: /admin/cot وتتضمن Overview وReports وDaily Control وExperiments وComparisons وGovernance وAudit Logs وContracts وSettings.

## فصل CORE وEXPANDED

يبقى CORE هو المصدر الوحيد للنتائج العامة عبر Public API، بينما يعمل EXPANDED في SHADOW MODE عبر واجهات الإدارة فقط، ولا يوجد مسار مباشر من EXPANDED إلى Public API. أي ترقية تمر عبر Governance Promotion Request واختبارات واعتماد.

## الخلاصة

المنتج العام يبقى بسيطًا وموجّهًا للمستخدم، بينما تبقى أدوات الاختبار والحوكمة والمراقبة داخل لوحة الإدارة وفق أفضل الممارسات المؤسسية.

## المرجعيات البصرية والتقنية المعتمدة لهندسة الواجهات

تم اعتماد هذا التوجه كمرجع تصميم وهندسة، مع الاستفادة من مبادئ تلك المنتجات من دون نسخ هويتها البصرية أو مكوّناتها حرفيًا.

المشروع سيبقى متعدد التقنيات كما كشف التقرير: Node.js وExpress للخدمات الأساسية، Python وUvicorn لبعض خدمات البيانات، وReact وVite للواجهات، مع استخدام TypeScript في الواجهات الجديدة قدر الإمكان.

### توزيع المرجعيات على أجزاء المنظومة

### واجهة المستخدم العامة — مستوحاة من Stripe

ستعرض للمستخدم النتيجة الرسمية CORE فقط:

- Hero واضح يشرح قيمة المنظومة.

- حركة خفيفة وهادئة، وليست مؤثرات ثقيلة.

- تدرجات لونية محسوبة.

- رسم مبسط يوضح مسار البيانات من تقرير COT إلى النتيجة.

- CTA واضح.

- بطاقات مزايا قصيرة.

- عدم إظهار أي معلومة عن اختبار EXPANDED.

الصفحة العامة يجب أن تكون تسويقية وواضحة، وليست لوحة مراقبة تقنية.

### لوحة الإدارة والاختبار — مستوحاة من Linear

هذه هي الواجهة الأهم في مشروع الحوكمة:

- Sidebar ثابت ومنظم.

- جداول سريعة لنتائج CORE وEXPANDED.

- مرشحات حسب التقرير.

- مرشحات حسب الأسبوع الفعّال.

- مرشحات حسب نمط التحليل.

- مرشحات حسب منظور الفئات.

- مرشحات حسب منظور أيام السيطرة.

- مرشحات حسب حالة الاتفاق أو الاختلاف.

- اختصارات لوحة مفاتيح.

- تحديثات سريعة دون إعادة تحميل الصفحة.

- حالات تحميل بسيطة.

- عدم استخدام رسوم ضخمة عندما يكفي جدول واضح.

داخل لوحة الإدارة فقط سيظهر:

| العنصر | الحالة |
| --- | --- |
| CORE | OFFICIAL |
| EXPANDED | SHADOW |
| Experiment Status | RUNNING |
| Public Exposure | DISABLED |

### الإعدادات والمشروعات — مستوحاة من Vercel

يُعرض كل مكوّن ككيان واضح:

- COT Governance Engine

- Raw COT Gateway

- CORE Perspective

- EXPANDED Experiment

- UTC Calendar Policy

- Report Activation Policy

كل بطاقة تعرض:

- الحالة.

- الإصدار.

- آخر تشغيل.

- آخر تقرير COT مستخدم.

- الصحة التشغيلية.

- البيئة.

- رابط السجلات الداخلية.

- آخر تعديل حوكمي.

صفحات الإعدادات ستكون مقسمة إلى:

- General

- Perspectives

- Day Control

- UTC Calendar

- Shadow Testing

- Permissions

- Audit Log

- API Contracts

### النماذج والنوافذ — مستوحاة من Figma

سنستخدم هذا الأسلوب في:

- إنشاء تجربة جديدة.

- تعديل منظور أيام السيطرة.

- ترقية نموذج تجريبي.

- إيقاف اختبار.

- مقارنة نسختين.

- اعتماد قرار حوكمة.

كل عملية حساسة ستستخدم Dialog واضحًا يعرض:

- ما الذي سيتغير؟

- ما الذي لن يتغير؟

- هل يؤثر على المستخدم؟

- النسخة الحالية والجديدة.

- سبب التعديل.

- اسم المعتمد.

- توقيت التنفيذ بصيغة UTC.

لن توجد أزرار غامضة مثل «حفظ» فقط في العمليات الحساسة؛ بل تسميات صريحة مثل:

- Save as Draft

- Start Shadow Test

- Approve Governance Version

- Promote to CORE

- Cancel Without Changes

### التوثيق والتنظيم — مستوحى من Notion

سيكون هناك مركز توثيق داخلي منظم:

- Governance Overview

- Terminology

- Dominance Delta

- Investment Mode

- Speculation Mode

- Day-Control Perspectives

- UTC Policy

- CORE vs EXPANDED

- API Contracts

- Test Cases

- Decision Records

- Changelog

- Incident Notes

ويشمل:

- تنقل جانبي هرمي.

- روابط داخلية بين القواعد.

- Empty states واضحة.

- تاريخ تعديل لكل وثيقة.

- رقم إصدار الحوكمة.

- دعم العربية RTL والإنجليزية LTR.

### الهوية البصرية المقترحة

لن نستخدم واجهة ملوّنة بكثرة. النظام يحتاج مظهرًا مؤسسيًا وتحليليًا.

| الاستخدام | اللون المقترح |
| --- | --- |
| Background | Deep Charcoal / Near Black؛ ويمكن Off-White في Public Light canvas |
| Primary brand accent | Warm Refined Metallic Gold |
| Secondary analytical accent | Controlled Sky Blue / Light Cyan-Blue |
| Success | Green |
| Bearish | Red |
| Warning | Amber |
| Shadow experiment | Purple |
| Official CORE | Warm restrained Gold emphasis + explicit status label |

لكن اللون لن يكون الوسيلة الوحيدة لفهم الحالة؛ سنستخدم النص والأيقونات أيضًا.

- صاعد غير صريح — ذو أفق ضيق.

- هابط صريح — ذو أفق ممتد.

### دعم العربية والإنجليزية

سيُبنى اتجاه الصفحة على مستوى المكوّن، وليس بتغيير CSS عشوائي.

<html lang="ar" dir="rtl">

وللإنجليزية:

<html lang="en" dir="ltr">

الجداول والأرقام ستراعي ما يلي:

- النص العربي RTL.

- الأرقام والمعادلات LTR داخل السطر عند الحاجة.

- الأكواد وJSON دائمًا LTR.

- لا تُخلط الفقرات العربية والإنجليزية في نفس الكتلة.

- التقرير الثنائي اللغة يقسم كل لغة إلى قسم مستقل.

### توزيع التقنية

| الجزء | التقنيات | ملاحظات |
| --- | --- | --- |
| الواجهات | React / Vite / TypeScript | كل واجهة حوكمة جديدة تُكتب بـTypeScript قدر الإمكان. |
| محرك الحوكمة | Node.js / Express / CommonJS / JSON Schema | الموقع الأنسب: backend/services/decision_governance_core/ |
| بيانات COT الخام | Python / Uvicorn | الخدمة الحالية: apps/ndsp-raw-cot-gateway |

أي واجهة جديدة تخص الحوكمة سنكتبها بـTypeScript، حتى لو كانت بعض الواجهات الحالية JavaScript، لأن العقود والأنواع مهمة جدًا في هذا المشروع.

ولا يوضع قرار الاتجاه النهائي داخل خدمة بيانات COT الخام؛ وظيفتها توفير البيانات الخام والتحقق منها فقط.

### نموذج الصفحات

المستخدم النهائي

/
├── Home
├── Methodology
├── Current Analysis
├── Documentation
└── Sign In

وفي صفحة التحليل:

- Official Direction

- Analysis Mode

- Effective Week

- Report Date

- Direction Label

- Dominance Delta

- Last Updated UTC

لا يوجد EXPANDED أو حالة تجربة.

لوحة الإدارة

/admin/cot
├── Overview
├── Reports
├── Daily Control
├── Experiments
├── Comparisons
├── Governance
├── Audit Logs
├── Contracts
└── Settings

### حماية المنطق الأساسي

واجهة الإدارة لن تتصل مباشرة بمخرجات المستخدم. سيكون المساران منفصلين:

CORE Engine
    ↓
Official Result Store
    ↓
Public API
    ↓
User Interface

EXPANDED Shadow Engine
    ↓
Experimental Result Store
    ↓
Internal Admin API
    ↓
Admin Dashboard

ولا يوجد مسار من EXPANDED إلى Public API.

حتى زر الترقية في لوحة الإدارة لا يغيّر النتيجة مباشرة؛ بل ينشئ Governance Promotion Request، ويحتاج اعتمادًا وتحديث إصدار واختبارات قبول.

### الاعتماد المؤقت

CORE

- النمط الاستثماري: مدراء الأصول فقط.

- النمط المضاربي عند سيطرة طويلي الأمد: مدراء الأصول فقط.

- النمط المضاربي عند سيطرة قصيري الأمد: الرافعات المالية فقط.

EXPANDED

- مدراء الأصول + الآخرون.

- الرافعات المالية + المتاجرين.

- يعمل في SHADOW_MODE.

- مخفي عن المستخدم.

- ظاهر للإدارة فقط.

وهذا هو الأسلوب الأقرب إلى ما تفعله المنصات الكبيرة: المنتج العام بسيط، بينما التعقيد والاختبارات والمراقبة تبقى داخل أدوات الإدارة.

## معايير اعتماد مكتبات ومكونات الواجهة

يعتمد المشروع مبدأ «الأداة المناسبة للمهمة المناسبة» (Best Tool for the Job)، بحيث لا تُستخدم أكثر من مكتبة لأداء الوظيفة نفسها دون مبرر هندسي موثق. ويهدف ذلك إلى الحفاظ على اتساق الواجهات، وتسهيل الصيانة، وتقليل حجم الحزم البرمجية، وتجنب الازدواجية التقنية.

يجب أن تدعم جميع المكونات المختارة React وTypeScript، وأن تكون نشطة التطوير، وموثقة رسميًا، وقابلة للتوسع، مع مراعاة الأداء، وإمكانية الوصول، ودعم العربية RTL والإنجليزية LTR.

### مكتبات الواجهة المعتمدة

| المجال | الأداة المعتمدة | الاستخدام |
| --- | --- | --- |
| Design System | shadcn/ui + Radix UI | المكونات الأساسية، النوافذ، القوائم، الحوارات، التبويبات، عناصر الإدخال. |
| Icons | Lucide React | جميع أيقونات النظام ضمن لغة بصرية موحدة. |
| Forms | React Hook Form + Zod | إدارة النماذج والتحقق من البيانات وربطها بعقود API. |
| Server State | TanStack Query | Cache، Retry، Background Refresh، Loading، Error، Optimistic Updates. |
| Routing | React Router أو TanStack Router | إدارة التنقل والمسارات وفق بنية التطبيق الحالية. |
| Large Tables | AG Grid | الجداول الكبيرة، الفرز، التصفية، التجميع، تثبيت الأعمدة، والتصدير. |
| Simple Charts | Recharts | الرسوم البسيطة، KPIs، واللوحات الخفيفة. |
| Advanced Analytics | Apache ECharts | Heatmaps، Sankey، Graph، الرسوم المالية والزمنية والبيانات الكثيفة. |
| Workflow & Graphs | React Flow | مخططات العلاقات والاعتماديات وسير العمل. |
| Standard Maps | Leaflet | الخرائط الخفيفة، النقاط الجغرافية، وطبقات GeoJSON. |
| Advanced Maps | Mapbox GL أو MapLibre GL | الخرائط المتجهية، الطبقات المتعددة، والتحريك والتخصيص المتقدم. |
| Rich Text Editor | TipTap | التوثيق، Decision Records، Incident Notes، والمحتوى التحريري. |
| Code & JSON Editor | Monaco Editor | تحرير JSON، العقود، الإعدادات، المقارنة، ومراجعة الأكواد. |
| Calendar | FullCalendar | التقاويم والجداول الزمنية والتجارب والتقارير الفعالة. |
| Drag & Drop | dnd-kit | إعادة ترتيب العناصر، Kanban، Workflow Builders، وإدارة الأولويات. |
| 3D Visualization | React Three Fiber | المحاكاة أو العروض ثلاثية الأبعاد عند وجود حاجة فعلية فقط. |
| Testing | Vitest + Testing Library | اختبارات الوحدات والمكونات. |
| End-to-End Testing | Playwright | اختبارات المسارات الكاملة وتجارب المستخدم الحرجة. |
| Component Documentation | Storybook | توثيق Design System والمكونات المعزولة. |
| API Mocking for Tests | MSW | محاكاة العقود في التطوير والاختبارات فقط، وليس بديلًا عن البيانات الحقيقية. |
| Dates and UTC | date-fns | معالجة التواريخ وUTC بصورة موحدة. |
| Localization | i18next أو react-intl | إدارة العربية والإنجليزية ورسائل الواجهة. |

### قواعد اختيار مكتبات الرسوم البيانية

Recharts

يُستخدم في:

- مؤشرات الأداء KPIs.

- الرسوم الخطية والأعمدة والمساحات والدوائر.

- اللوحات البسيطة والمتوسطة.

- صفحات المستخدم النهائي.

- مجموعات البيانات الصغيرة والمتوسطة.

Apache ECharts

يُستخدم في:

- التحليلات المتقدمة.

- Heatmaps.

- Sankey.

- Graph Networks.

- الرسوم المالية.

- السلاسل الزمنية الكبيرة.

- صفحات الإدارة والتحليلات المعقدة.

القاعدة: لا تُستخدم Recharts وECharts في الشاشة نفسها إلا عند وجود مبرر تقني واضح. Recharts هو الخيار الافتراضي للرسوم البسيطة، وECharts للرسوم المتقدمة والبيانات الكثيفة.

### قواعد اختيار مكتبات الخرائط

Leaflet

يُستخدم عندما تكون الخريطة بسيطة وتشمل:

- نقاطًا جغرافية.

- طبقات GeoJSON.

- خرائط خفيفة.

- حالات لا تتطلب Vector Tiles أو تحريكًا معقدًا.

Mapbox GL أو MapLibre GL

يُستخدم عندما تتطلب المنظومة:

- خرائط متجهية.

- بيانات جغرافية كبيرة.

- طبقات متعددة.

- Animations.

- تخصيصًا بصريًا متقدمًا.

- أداءً أعلى مع البيانات الجغرافية الكثيفة.

يُفضّل MapLibre GL عند الحاجة إلى خيار مفتوح المصدر، بينما يعتمد Mapbox GL عند الحاجة إلى خدمات Mapbox المدارة وميزاتها المتقدمة.

### معيار الجداول

يعتمد النظام AG Grid كحل موحد للجداول الكبيرة والمعقدة داخل لوحة الإدارة، لما يوفره من فرز، وبحث، وتصفية، وتجميع، وتثبيت للأعمدة، وتصدير، وأداء مناسب مع البيانات الضخمة.

أما الجداول الصغيرة داخل بطاقات العرض أو صفحات المستخدم النهائي، فيُفضّل تنفيذها بمكونات shadcn/ui القياسية لتقليل التعقيد وحجم الحزمة.

يجب مراجعة تراخيص ميزات AG Grid Enterprise قبل استخدام Pivot، Server-Side Row Model، Master/Detail، أو خصائص التصدير المتقدمة.

### معيار النماذج والتحقق

يعتمد المشروع React Hook Form مع Zod للأسباب التالية:

- أنواع TypeScript قوية.

- التحقق من صحة البيانات قبل الإرسال.

- سهولة ربط النماذج بعقود API.

- أداء مرتفع وتقليل عمليات إعادة الرسم.

- إعادة استخدام Schemas بين الواجهة والاختبارات.

- إظهار رسائل خطأ متسقة بالعربية والإنجليزية.

### معيار إدارة بيانات الخادم

تعتمد جميع استدعاءات API على TanStack Query لإدارة:

- Cache.

- Retry.

- Background Refresh.

- Loading State.

- Error State.

- Invalidation.

- Optimistic Updates عند الحاجة.

لا تُستخدم استدعاءات fetch المباشرة داخل مكونات العرض إلا في حالات استثنائية موثقة. ويجب فصل API Client وQuery Hooks عن Presentation Components.

### معيار المحررات

TipTap

يُعتمد للمحتوى الذي يحرره المستخدم، مثل:

- Documentation.

- Governance Notes.

- Incident Reports.

- Decision Records.

- Changelog Notes.

Monaco Editor

يُعتمد لكل ما يتعلق بـ:

- JSON.

- API Contracts.

- Configuration Files.

- مقارنة العقود.

- مراجعة الأكواد والملفات البرمجية.

يُحمّل Monaco Editor باستخدام Lazy Loading بسبب حجمه، ولا يُضمَّن في الحزمة الأولية للصفحات التي لا تحتاجه.

### معيار السحب والإفلات

يعتمد dnd-kit في:

- إعادة ترتيب العناصر.

- لوحات Kanban.

- Workflow Builders.

- إدارة الأولويات.

- تخصيص ترتيب البطاقات أو الأعمدة.

يجب دعم لوحة المفاتيح وقارئات الشاشة في جميع وظائف السحب والإفلات، وألا تكون الإيماءات الوسيلة الوحيدة لتنفيذ العملية.

### معيار العروض ثلاثية الأبعاد

لن تُضمّن Three.js أو React Three Fiber ضمن الحزمة الأساسية للواجهة. ولا تُستخدم إلا إذا وُجدت حاجة فعلية إلى محاكاة ثلاثية الأبعاد أو Visualization تفاعلي، وذلك لتقليل حجم التطبيق والحفاظ على الأداء.

### معايير الاختبار والتوثيق

- Vitest لاختبارات المنطق والوحدات.

- Testing Library لاختبارات سلوك المكونات من منظور المستخدم.

- Playwright لاختبارات End-to-End والمسارات الحساسة.

- Storybook لتوثيق Design System والحالات المختلفة لكل مكوّن.

- MSW لمحاكاة API في التطوير والاختبارات فقط.

### معايير اعتماد أي مكتبة جديدة

- توافق كامل مع React وTypeScript.

- وثائق رسمية جيدة ومحدثة.

- مجتمع نشط وصيانة مستمرة.

- دعم إمكانية الوصول Accessibility.

- دعم الوضعين الفاتح والداكن.

- عدم التعارض مع Design System المعتمد.

- إمكانية Lazy Loading عند الحاجة.

- عدم تكرار وظيفة تؤديها مكتبة أخرى معتمدة.

- مراجعة الترخيص والتكلفة قبل الاعتماد.

- قياس أثر المكتبة على حجم الحزمة والأداء.

- توثيق سبب الاعتماد في Architecture Decision Record.

### التراخيص والتكلفة

يجب مراجعة التراخيص قبل الاعتماد النهائي، خصوصًا للمكتبات أو الميزات التي قد تتطلب اشتراكًا أو ترخيصًا تجاريًا.

- AG Grid Enterprise للخصائص المتقدمة.

- FullCalendar Premium للـTimeline وResource Scheduling.

- Mapbox للخدمات المدارة وحدود الاستخدام.

- بعض ميزات TipTap المتقدمة أو التعاونية.

### المبادئ العامة الملزمة

- shadcn/ui + Radix UI هما الأساس لجميع المكونات العامة.

- Lucide React هو المصدر الموحد للأيقونات.

- React Hook Form + Zod هما المعيار للنماذج.

- TanStack Query هو المعيار لإدارة Server State.

- Recharts للرسوم البسيطة وECharts للرسوم المتقدمة.

- AG Grid للجداول الكبيرة، وshadcn/ui للجداول الصغيرة.

- Leaflet هو الخيار الافتراضي للخرائط البسيطة.

- Mapbox GL أو MapLibre GL للحالات الجغرافية المتقدمة.

- لا تُستخدم أكثر من مكتبة لنفس الغرض دون مبرر هندسي موثق.

- تُفضّل المكونات القابلة لإعادة الاستخدام.

- يُراعى الأداء وتقليل حجم الحزم.

- تُبنى جميع الواجهات الجديدة باستخدام React + Vite + TypeScript.

- يجب أن تدعم جميع المكونات العربية RTL والإنجليزية LTR.

- تُفصل Presentation Layer عن Business Logic وعن Data Access Layer.

- لا تُستخدم بيانات Mock في المنتج النهائي بدل البيانات الحقيقية.

- كل مكتبة جديدة تحتاج قرارًا معماريًا موثقًا ومراجعة للترخيص.

### التركيب المرجعي المقترح

| الطبقة | الاختيار المعتمد |
| --- | --- |
| Base UI | shadcn/ui + Radix UI + Lucide React |
| Forms | React Hook Form + Zod |
| Server State | TanStack Query |
| Routing | React Router أو TanStack Router |
| Simple Charts | Recharts |
| Advanced Charts | Apache ECharts |
| Large Tables | AG Grid |
| Flows | React Flow |
| Documentation | TipTap |
| Code and Contracts | Monaco Editor |
| Calendar | FullCalendar |
| Maps | Leaflet افتراضيًا، وMapbox GL أو MapLibre GL للحالات المتقدمة |
| Drag & Drop | dnd-kit |
| Testing | Vitest + Testing Library + Playwright |
| Component Documentation | Storybook |
| API Mocking | MSW للاختبارات والتطوير فقط |
| 3D | React Three Fiber عند وجود حاجة فعلية |

### الخلاصة التنفيذية لمعايير المكونات

بهذا الاعتماد تصبح مكتبات الواجهة جزءًا من وثيقة هندسية مرجعية، وليست مجرد قائمة أسماء. ويضمن هذا النهج اختيار كل أداة وفق طبيعة المهمة، مع الحفاظ على الاتساق والأداء وقابلية الاختبار والصيانة والتوسع.
