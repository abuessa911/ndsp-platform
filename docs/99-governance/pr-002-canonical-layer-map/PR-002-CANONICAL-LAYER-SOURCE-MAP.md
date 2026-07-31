# PR-002 — Canonical Layer / Source Map

- Generated: `2026-07-31T08:34:58.022880+00:00`
- Project: `/home/nawaf511/empire-core-new`
- Branch: `governance/pr-002-canonical-layer-map`
- Git HEAD: `5d7f160ccb6c3e2a42a8aaa349d16507a9009cd6`
- Runtime modifications: **NO**
- Service restarts: **NO**
- Deletions: **NO**

## Gate decision

**PASS**

- Confirmed: 16/16
- Review required: 0/16
- No evidence: 0/16

## Canonical map

| Layer | Canonical source | Owner | Runtime owner | Status | Evidence |
|---|---|---|---|---|---|
| L01 | backend/layers/canonical_v1/direction/l01_tdl_medium_long.py | nawaf511 | nawaf511 | CONFIRMED | implementation=8, consumers=5, tests=0, docs=19, total=32 |
| L02 | backend/layers/canonical_v1/direction/l02_tdl_short_speculative.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=0, docs=13, total=23 |
| L03 | backend/layers/canonical_v1/direction/l03_market_direction_context.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=0, docs=13, total=23 |
| L04 | backend/layers/canonical_v1/direction/l04_correction_gate.py | nawaf511 | nawaf511 | CONFIRMED | implementation=6, consumers=5, tests=0, docs=13, total=24 |
| L05 | backend/layers/canonical_v1/quality/l05_divergence_engine.py | nawaf511 | nawaf511 | CONFIRMED | implementation=4, consumers=5, tests=0, docs=13, total=22 |
| L06 | backend/layers/canonical_v1/direction/l06_temporal_day_logic.py | nawaf511 | nawaf511 | CONFIRMED | implementation=4, consumers=5, tests=0, docs=13, total=22 |
| L07 | backend/layers/canonical_v1/structure/l07_scenario_levels.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=1, docs=13, total=24 |
| L08 | backend/layers/canonical_v1/structure/l08_nmp_confirmation.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=0, docs=13, total=23 |
| L09 | backend/layers/canonical_v1/quality/l09_momentum_engine.py | nawaf511 | nawaf511 | CONFIRMED | implementation=4, consumers=5, tests=0, docs=13, total=22 |
| L10 | backend/layers/canonical_v1/quality/l10_liquidity_structure_confirmation.py | nawaf511 | nawaf511 | CONFIRMED | implementation=4, consumers=5, tests=0, docs=13, total=22 |
| L11 | backend/layers/canonical_v1/risk/l11_usd_macro_filter.py | nawaf511 | nawaf511 | CONFIRMED | implementation=4, consumers=5, tests=0, docs=13, total=22 |
| L12 | backend/layers/canonical_v1/risk/l12_risk_engine.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=0, docs=13, total=23 |
| L13 | backend/layers/canonical_v1/quality/l13_nawaf_golden_signal.py | nawaf511 | nawaf511 | CONFIRMED | implementation=5, consumers=5, tests=0, docs=13, total=23 |
| L14 | backend/layers/canonical_v1/quality/l14_nawaf_enhanced_golden_signal.py | nawaf511 | nawaf511 | CONFIRMED | implementation=7, consumers=5, tests=0, docs=13, total=25 |
| L15 | backend/layers/canonical_v1/risk/l15_devils_advocate.py | nawaf511 | nawaf511 | CONFIRMED | implementation=6, consumers=5, tests=0, docs=13, total=24 |
| L16 | backend/layers/canonical_v1/final/l16_decision_readiness_state_machine.py | nawaf511 | nawaf511 | CONFIRMED | implementation=6, consumers=5, tests=0, docs=17, total=28 |

## Approval conditions

1. Every layer L01-L16 has one canonical source.
2. Every layer has a named code owner and runtime owner.
3. Every duplicate implementation has an identified consumer.
4. No deletion, consolidation, or migration occurs in PR-002.
5. Runtime and API behavior remain unchanged.

## Review procedure

Edit `owners.json`, rerun the generator, and require all 16 layers to become `CONFIRMED` before merging.
