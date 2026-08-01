# PR-062 — COT Direction and Time Backend Audit

## Scope

This audit scans backend and integration source trees in read-only mode. It identifies current COT direction, category, timing, CORE/EXPANDED, and result-integration logic. It does not change runtime or product code.

## Approved baseline used for comparison

- Dominance delta: `Long - Short` within the same dataset.
- `Long > Short`: bullish.
- `Short > Long`: bearish.
- `Long == Short`: neutral only.
- Investment: Asset Manager Positions determine official direction.
- Investment: Asset Manager Changes determine weekly support only.
- Investment: Day Control, TDL-M&L, and TDL-S are disabled.
- Speculation: Changes only; Day Control and approved TDL logic may run.
- Time: UTC only.
- Tuesday report: effective next Monday at `00:00:00Z`.
- Effective interval: `[effectiveFrom, effectiveUntil)`.
- Public result: CORE only.
- EXPANDED: internal `SHADOW_MODE` only.

## Audit totals

- Candidate files scanned: **40**
- Logic candidate files: **24**
- Direction candidates: **12**
- Time candidates: **12**
- CORE/EXPANDED candidates: **13**
- Critical risk: **0**
- High risk: **7**
- Medium risk: **7**
- Low risk: **10**

## Automated risk indicators

- Positions/Changes co-location: **0**
- Investment with TDL/Day Control co-location: **0**
- Potential local-time usage: **3**
- Public/EXPANDED co-location: **0**
- Legacy path references: **2**

These indicators are audit candidates, not automatic proof of defects. Each requires human review before PR-063/PR-064 changes.

## Highest-priority impact map

| Risk | Action | Kind | Path | Flags |
|---|---|---|---|---|
| HIGH | REPLACE_OR_WRAP | RUNTIME_IMPLEMENTATION | `apps/ndsp-governance-bridge/app/core/tdl_v2_policy.py` | NONE |
| HIGH | ALIGN_CONTRACT | CONTRACT | `backend/app/api/v1/frontend_contract.py` | NONE |
| HIGH | REPLACE_OR_WRAP | RUNTIME_IMPLEMENTATION | `backend/middleware/trialGuard.js` | LOCAL_TIME_USAGE |
| HIGH | REPLACE_OR_WRAP | INTEGRATION | `backend/ndsp_api_compat_gateway.cjs` | NONE |
| HIGH | REPLACE_OR_WRAP | RUNTIME_IMPLEMENTATION | `backend/ndsp_tdl_trade_horizon_addons.cjs` | LOCAL_TIME_USAGE |
| HIGH | REPLACE_OR_WRAP | INTEGRATION | `backend/ndsp_trial_register_gateway.cjs` | LOCAL_TIME_USAGE |
| HIGH | REPLACE_OR_WRAP | INTEGRATION | `backend/ndsp_user_dashboard_gateway.cjs` | NONE |
| MEDIUM | WRAP_OR_REPLACE | RUNTIME_IMPLEMENTATION | `backend/app/support_layers/quality/decision_quality_stack.py` | NONE |
| MEDIUM | WRAP_OR_REPLACE | RUNTIME_IMPLEMENTATION | `backend/app/support_layers/scenario/scenario_engine.py` | NONE |
| MEDIUM | WRAP_OR_REPLACE | INTEGRATION | `backend/ndsp_admin_actions_gateway.cjs` | LEGACY_PATH_REFERENCE |
| MEDIUM | WRAP_OR_REPLACE | RUNTIME_IMPLEMENTATION | `backend/ndsp_device_guard.cjs` | NONE |
| MEDIUM | WRAP_OR_REPLACE | RUNTIME_IMPLEMENTATION | `backend/ndsp_layer_name_masking_policy.cjs` | NONE |
| MEDIUM | REVIEW_CONFIGURATION | CONFIG | `backend/package-lock.json` | NONE |
| MEDIUM | ADD_REGRESSION_TESTS | TEST | `backend/tests/pr024-critical-contracts.test.cjs` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `apps/ndsp-governance-bridge/app/core/__init__.py` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `apps/ndsp-governance-bridge/policies/admin_snapshot/tdl_v2_policy_admin.py` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `backend/ndsp_admin_extension.cjs` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `backend/ndsp_admin_migrate.cjs` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `backend/ndsp_admin_ui_proxy.cjs` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `backend/ndsp_admin_users_official_readonly.cjs` | NONE |
| LOW | REVIEW | RUNTIME_IMPLEMENTATION | `backend/ndsp_one_device_one_account.sh` | LEGACY_PATH_REFERENCE |
| LOW | REVIEW | INTEGRATION | `backend/ndsp_platform_gateway_9001.cjs` | NONE |
| LOW | REVIEW | INTEGRATION | `backend/ndsp_user_login_gateway.cjs` | NONE |
| LOW | REVIEW | INTEGRATION | `backend/server.js` | NONE |

## Required next steps

1. Human-review all CRITICAL and HIGH records.
2. Confirm current writers/readers of official and experimental results.
3. Resolve TDL-M&L and TDL-S semantics before implementation.
4. Freeze versioned direction/time contracts in PR-063.
5. Add regression fixtures before replacing any runtime path.
6. Correct direction and time layers only after contract approval.

## Safety

- Product code changes: **0**
- Traceability rows modified: **0**
- Production services restarted: **0**
- Mutating requests executed: **0**
- Runtime changes: **none**

## Artifacts

- `PR062_LOGIC_INVENTORY.csv`
- `PR062_LOGIC_INVENTORY.json`
- `PR062_CODE_IMPACT_MAP.csv`
- `PR062_CODE_IMPACT_MAP.json`
- `PR062_UNRESOLVED_ITEMS.csv`
- `PR062_SUMMARY.json`
- `PR062_SHA256SUMS.txt`
