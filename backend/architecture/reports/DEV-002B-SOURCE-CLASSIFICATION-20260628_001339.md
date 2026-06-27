# DEV-002B — Repository Source Classification

Generated: 20260628_001339
Root: /home/nawaf511/empire-core-new
Branch: feature/ndsp-os
Head: bb8f1ce chore(DEV-002): add repository hygiene policy

## Purpose

Classify untracked and modified repository files after DEV-002 hygiene.

This report does not delete files and does not stage files.

## Current Git Status Summary

```text
 M frontend/user-portal-vite/package-lock.json
 M frontend/user-portal-vite/package.json
 M frontend/user-portal-vite/src/main.jsx
 M frontend/user-portal-vite/src/styles.css
?? .env.delivery.example
?? .env.example
?? DSP_FINAL_TRIAL_POLICY.md
?? DSP_NMP_V1_POLICY.md
?? apps/
?? backend/.env.example
?? backend/.env.telegram.example
?? backend/__init__.py
?? backend/_archive_safe_cleanup_20260627_214310/
?? backend/admin_users_official_api/
?? backend/alembic.ini
?? backend/app/
?? backend/architecture/reports/
?? backend/auth_api/
?? backend/config/
?? backend/data/
?? backend/db/
?? backend/docs/
?? backend/layers/
?? backend/migrations/
?? backend/ndsp-access-guard-9024/
?? backend/ndsp-access-guard-final/
?? backend/ndsp-access-guard/
?? backend/ndsp-live-decision-quality/
?? backend/ndsp-portal-real-data-api/
?? backend/ndsp-telegram-link-listener/
?? backend/ndsp-trial-register-canonical-wrapper/
?? backend/ndsp-trial-seats-api/
?? backend/ndsp-user-alert-channels/
?? backend/ndsp_checkout_plans_package/
?? backend/ndsp_latest_16_layers_logic_functions.py
?? backend/ndsp_live_market_adapter.cjs
?? backend/ndsp_scenario_levels_adapter.cjs
?? backend/package_reference/
?? backend/password_reset_gateway/
?? backend/portal_snapshot_generator.cjs
?? backend/research/
?? backend/runtime/
?? backend/scripts/
?? backend/shared/
?? bin/
?? deploy_frontend_from_apps.sh
?? docs/
?? fix_portal.sh
?? frontend/user-portal-vite/src/config/
?? frontend/user-portal-vite/src/core/
?? frontend/user-portal-vite/src/hooks/
?? frontend/user-portal-vite/src/pages/
?? frontend/user-portal-vite/vite.config.js
?? governance/
?? ndsp_checkout_plans_package/
?? ndsp_governance/
?? research/
?? run_local_ndsp.py
?? runtime/
?? shared/
?? tests/
```

## Classification Table

| Status | Classification | Path |
|---|---|---|
| ` M` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/package-lock.json` |
| ` M` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/package.json` |
| ` M` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/main.jsx` |
| ` M` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/styles.css` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `.env.delivery.example` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `.env.example` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `DSP_FINAL_TRIAL_POLICY.md` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `DSP_NMP_V1_POLICY.md` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `apps/` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `backend/.env.example` |
| `??` | `DOC_OR_EXAMPLE_REVIEW` | `backend/.env.telegram.example` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/__init__.py` |
| `??` | `LOCAL_RUNTIME_IGNORE` | `backend/_archive_safe_cleanup_20260627_214310/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/admin_users_official_api/` |
| `??` | `UNKNOWN_REVIEW` | `backend/alembic.ini` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/app/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/auth_api/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/config/` |
| `??` | `UNKNOWN_REVIEW` | `backend/data/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/db/` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/docs/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/layers/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/migrations/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-access-guard-9024/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-access-guard-final/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-access-guard/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-live-decision-quality/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-portal-real-data-api/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-telegram-link-listener/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-trial-register-canonical-wrapper/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-trial-seats-api/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/ndsp-user-alert-channels/` |
| `??` | `UNKNOWN_REVIEW` | `backend/ndsp_checkout_plans_package/` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/ndsp_latest_16_layers_logic_functions.py` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/ndsp_live_market_adapter.cjs` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/ndsp_scenario_levels_adapter.cjs` |
| `??` | `UNKNOWN_REVIEW` | `backend/package_reference/` |
| `??` | `LEGACY_BACKEND_MODULE_REVIEW` | `backend/password_reset_gateway/` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/portal_snapshot_generator.cjs` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/research/` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/runtime/` |
| `??` | `BACKEND_TOOLING_REVIEW` | `backend/scripts/` |
| `??` | `BACKEND_SOURCE_REVIEW` | `backend/shared/` |
| `??` | `DEPLOYMENT_TOOL_REVIEW` | `bin/` |
| `??` | `DEPLOYMENT_TOOL_REVIEW` | `deploy_frontend_from_apps.sh` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `docs/` |
| `??` | `DEPLOYMENT_TOOL_REVIEW` | `fix_portal.sh` |
| `??` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/config/` |
| `??` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/core/` |
| `??` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/hooks/` |
| `??` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/src/pages/` |
| `??` | `FRONTEND_SOURCE_REVIEW` | `frontend/user-portal-vite/vite.config.js` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `governance/` |
| `??` | `UNKNOWN_REVIEW` | `ndsp_checkout_plans_package/` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `ndsp_governance/` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `research/` |
| `??` | `DEPLOYMENT_TOOL_REVIEW` | `run_local_ndsp.py` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `runtime/` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `shared/` |
| `??` | `TOP_LEVEL_SOURCE_REVIEW` | `tests/` |

## Counts By Classification

```text
     11 LEGACY_BACKEND_MODULE_REVIEW
      9 FRONTEND_SOURCE_REVIEW
      9 BACKEND_TOOLING_REVIEW
      8 TOP_LEVEL_SOURCE_REVIEW
      7 BACKEND_SOURCE_REVIEW
      6 DOC_OR_EXAMPLE_REVIEW
      5 UNKNOWN_REVIEW
      4 DEPLOYMENT_TOOL_REVIEW
      1 LOCAL_RUNTIME_IGNORE
```

## Recommended Next Actions

1. Do not use `git add .`.
2. Commit only intentional source groups.
3. Keep runtime, backup, cache, env, and dependency folders local.
4. Review frontend modified files separately from backend platform files.
5. Decide whether legacy backend modules should be archived, migrated, or registered.

## Suggested Buckets

### Likely source candidates

```text
 M frontend/user-portal-vite/src/main.jsx
 M frontend/user-portal-vite/src/styles.css
?? apps/
?? backend/app/
?? backend/auth_api/
?? backend/config/
?? backend/db/
?? backend/layers/
?? backend/migrations/
?? backend/shared/
?? docs/
?? frontend/user-portal-vite/src/config/
?? frontend/user-portal-vite/src/core/
?? frontend/user-portal-vite/src/hooks/
?? frontend/user-portal-vite/src/pages/
?? frontend/user-portal-vite/vite.config.js
?? governance/
?? shared/
?? tests/
```

### Local/runtime/ignore candidates

```text
?? backend/_archive_safe_cleanup_20260627_214310/
```

### Docs/policy candidates

```text
?? .env.delivery.example
?? .env.example
?? DSP_FINAL_TRIAL_POLICY.md
?? DSP_NMP_V1_POLICY.md
?? backend/.env.example
?? backend/.env.telegram.example
```

### Deployment/tool candidates

```text
?? backend/ndsp_live_market_adapter.cjs
?? backend/ndsp_scenario_levels_adapter.cjs
?? backend/portal_snapshot_generator.cjs
?? backend/scripts/
?? bin/
?? deploy_frontend_from_apps.sh
?? fix_portal.sh
?? run_local_ndsp.py
```
