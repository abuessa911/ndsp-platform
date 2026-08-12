# NDSP V1.2 Scenario Levels Strict Validator
DATE=2026-07-08T00:07:02+02:00
MODE=READ_ONLY_CONTRACT_VALIDATION
MODIFICATIONS=None
API_BASE=https://api.ndsp.app


## SYMBOL=ETHUSDT
HTTP_CODE=200
[FAIL] scenario_levels/reference_levels object missing
TOP_LEVEL_KEYS=_ndsp_golden_explainability_injected_at_ms,_ndsp_nmp_contract,_ndsp_nmp_injected_at,allowed_public_outputs,data_provider,explainability,generated_at,golden_alignment,golden_alignment_active,golden_evidence_public,golden_name,golden_reason_public,golden_signal,golden_spotlight,golden_status,instrument,live_market_analysis,live_price_bound,nmp,nmp_level,nmp_source,nmp_status,nmp_timeframe,nmp_value,ok,package,project,public_explainability,scenario,source_mode
STRICT_RESULT=ETHUSDT:FAIL

## SYMBOL=BTCUSDT
HTTP_CODE=200
[FAIL] scenario_levels/reference_levels object missing
TOP_LEVEL_KEYS=_ndsp_golden_explainability_injected_at_ms,_ndsp_nmp_contract,_ndsp_nmp_injected_at,allowed_public_outputs,data_provider,explainability,generated_at,golden_alignment,golden_alignment_active,golden_evidence_public,golden_name,golden_reason_public,golden_signal,golden_spotlight,golden_status,instrument,live_market_analysis,live_price_bound,nmp,nmp_level,nmp_source,nmp_status,nmp_timeframe,nmp_value,ok,package,project,public_explainability,scenario,source_mode
STRICT_RESULT=BTCUSDT:FAIL

## SYMBOL=XAUUSD
HTTP_CODE=200
[FAIL] scenario_levels/reference_levels object missing
TOP_LEVEL_KEYS=_ndsp_golden_explainability_injected_at_ms,_ndsp_nmp_contract,_ndsp_nmp_injected_at,allowed_public_outputs,data_provider,explainability,generated_at,golden_alignment,golden_alignment_active,golden_evidence_public,golden_name,golden_reason_public,golden_signal,golden_spotlight,golden_status,instrument,live_market_analysis,live_price_bound,nmp,nmp_level,nmp_source,nmp_status,nmp_timeframe,nmp_value,ok,package,project,public_explainability,scenario,source_mode
STRICT_RESULT=XAUUSD:FAIL

## SYMBOL=USOIL
HTTP_CODE=200
[FAIL] scenario_levels/reference_levels object missing
TOP_LEVEL_KEYS=_ndsp_golden_explainability_injected_at_ms,_ndsp_nmp_contract,_ndsp_nmp_injected_at,allowed_public_outputs,data_provider,explainability,generated_at,golden_alignment,golden_alignment_active,golden_evidence_public,golden_name,golden_reason_public,golden_signal,golden_spotlight,golden_status,instrument,live_market_analysis,live_price_bound,nmp,nmp_level,nmp_source,nmp_status,nmp_timeframe,nmp_value,ok,package,project,public_explainability,scenario,source_mode
STRICT_RESULT=USOIL:FAIL

## Runtime Safety
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11% | ram usage: 9.6% | lo: ⇓ 0.013mb/s ⇑ 0.013mb/s | eth0: ⇓ 0.171mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.104mb/s / 81.97% |

## Final Evaluation
VALID_ALL=0
SCENARIO_LEVELS_STRICT_STATUS=CHECK_ALERTS
FINAL_STATUS=V12_SCENARIO_LEVELS_STRICT_VALIDATOR_WITH_ALERTS
REPORT=docs/05-runbooks/NDSP_V12_SCENARIO_LEVELS_STRICT_VALIDATOR_20260708_000702.md
