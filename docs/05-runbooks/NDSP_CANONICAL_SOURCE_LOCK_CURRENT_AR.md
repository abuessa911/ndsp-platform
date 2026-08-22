# قفل المصدر الفعلي لمنظومة NDSP

**Document ID:** `NDSP-CANONICAL-SOURCE-LOCK-001`  
**Generated:** `2026-07-11T16:42:18.917028+00:00`  
**Host:** `vmi2934783`  
**Project:** `/home/nawaf511/empire-core-new`  
**Status:** `SOURCE_CANDIDATES_DISCOVERED_PENDING_FILE_BY_FILE_APPROVAL`  

هذا التقرير يثبت أدلة المصدر الفعلي دون تعديل الإنتاج. لا يعتبر أي ملف مصدرًا نهائيًا إلا بعد اعتماد المالك لمسار واحد لكل مسؤولية.

## الأمان

- Production changes: `NONE`
- Services restarted: `NONE`
- Databases changed: `NONE`

## Git

- Branch: `feature/ndsp-os`
- HEAD: `4e7c9bf2d96484488a6f19608fadec0d3d016558`
- Dirty worktree: `نعم`
- Changed/untracked entries: `27`

## الواجهة والمسارات الحية

- `/home/nawaf511/empire-core-new/frontend/user-portal-vite`
- `/home/nawaf511/empire-core-new/apps/user-portal`
- `/home/nawaf511/empire-core-new/frontend`
- `/home/nawaf511/empire-core-new/apps`
- `/var/www/ndsp-my`
- `/var/www/html`

## PM2

- `ndsp-portal` status=`online` cwd=`/home/nawaf511/empire-core-new/apps/user-portal` script=`/home/nawaf511/.nvm/versions/node/v24.15.0/bin/npm`

## systemd

- `certbot.service` active=`inactive` workdir=`` fragment=`/usr/lib/systemd/system/certbot.service`
- `decisionos-backend.service` active=`inactive` workdir=`/opt/decisionos/backend` fragment=`/etc/systemd/system/decisionos-backend.service`
- `empire-binance-feed.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/empire-binance-feed.service`
- `empire-ndip-api.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/empire-ndip-api.service`
- `empire-webhook.service` active=`inactive` workdir=`/opt/empire/webhooks/universal` fragment=`/etc/systemd/system/empire-webhook.service`
- `marketpulse.service` active=`inactive` workdir=`/home/nawaf511/marketpulse` fragment=`/etc/systemd/system/marketpulse.service`
- `ndip-api-new.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndip-api-new.service`
- `ndip-autonomous-loop.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-autonomous-loop.service`
- `ndip-autopilot.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-autopilot.service`
- `ndip-auto-signal.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-auto-signal.service`
- `ndip-auto-trade.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-auto-trade.service`
- `ndip-backend.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-backend.service`
- `ndip-dashboard.service` active=`inactive` workdir=`/root/empire-core/backend` fragment=`/etc/systemd/system/ndip-dashboard.service`
- `ndip-engine.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-engine.service`
- `ndip-frontend.service` active=`inactive` workdir=`/opt/empire-core/frontend` fragment=`/etc/systemd/system/ndip-frontend.service`
- `ndip-health-monitor.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndip-health-monitor.service`
- `ndip-run-server.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-run-server.service`
- `ndip-security-cleanup.service` active=`inactive` workdir=`/opt/ndip/backend/app` fragment=`/etc/systemd/system/ndip-security-cleanup.service`
- `ndip.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip.service`
- `ndip-signal-engine.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-signal-engine.service`
- `ndip-signal.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-signal.service`
- `ndip-telegram-decision-worker.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndip-telegram-decision-worker.service`
- `ndip-trading-loop.service` active=`inactive` workdir=`/opt/empire-core/backend` fragment=`/etc/systemd/system/ndip-trading-loop.service`
- `ndsp-16-layers.service` active=`active` workdir=`/opt/ndsp16-api` fragment=`/etc/systemd/system/ndsp-16-layers.service`
- `ndsp-access-guard-9024.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-access-guard-9024` fragment=`/etc/systemd/system/ndsp-access-guard-9024.service`
- `ndsp-access-guard-final.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-access-guard-final` fragment=`/etc/systemd/system/ndsp-access-guard-final.service`
- `ndsp-access-guard.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-access-guard` fragment=`/etc/systemd/system/ndsp-access-guard.service`
- `ndsp-admin-actions.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-admin-actions.service`
- `ndsp-admin-console.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/apps/admin-console` fragment=`/etc/systemd/system/ndsp-admin-console.service`
- `ndsp-admin-snapshot-updater.service` active=`activating` workdir=`` fragment=`/etc/systemd/system/ndsp-admin-snapshot-updater.service`
- `ndsp-admin-ui-proxy.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-admin-ui-proxy.service`
- `ndsp-admin-user-ops.service` active=`active` workdir=`/opt/ndsp-admin-user-ops` fragment=`/etc/systemd/system/ndsp-admin-user-ops.service`
- `ndsp-admin-users-official-readonly.service` active=`active` workdir=`` fragment=`/etc/systemd/system/ndsp-admin-users-official-readonly.service`
- `ndsp-admin-users-official.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/admin_users_official_api` fragment=`/etc/systemd/system/ndsp-admin-users-official.service`
- `ndsp-api-compat.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-api-compat.service`
- `ndsp-api.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndsp-api.service`
- `ndsp-app.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/frontend_public` fragment=`/etc/systemd/system/ndsp-app.service`
- `ndsp-auth-api.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-auth-api.service`
- `ndsp-backend.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndsp-backend.service`
- `ndsp-bot-execution.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/services/bot_execution` fragment=`/etc/systemd/system/ndsp-bot-execution.service`
- `ndsp-bot_execution.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/services/bot_execution` fragment=`/etc/systemd/system/ndsp-bot_execution.service`
- `ndsp-change-password-gateway.service` active=`active` workdir=`/opt/ndsp-change-password-gateway` fragment=`/etc/systemd/system/ndsp-change-password-gateway.service`
- `ndsp-checkout-api.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express` fragment=`/etc/systemd/system/ndsp-checkout-api.service`
- `ndsp-command-center-real-data.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-command-center-real-data.service`
- `ndsp-completed-decision.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/services/completed_decision` fragment=`/etc/systemd/system/ndsp-completed-decision.service`
- `ndsp-completed_decision.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/services/completed_decision` fragment=`/etc/systemd/system/ndsp-completed_decision.service`
- `ndsp-ctl-001-workspace-identity.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity` fragment=`/etc/systemd/system/ndsp-ctl-001-workspace-identity.service`
- `ndsp-current-user-display.service` active=`active` workdir=`/opt/ndsp-current-user-display` fragment=`/etc/systemd/system/ndsp-current-user-display.service`
- `ndsp-decision-governance-core.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/services/decision_governance_core` fragment=`/etc/systemd/system/ndsp-decision-governance-core.service`
- `ndsp-decision_governance_core.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/services/decision_governance_core` fragment=`/etc/systemd/system/ndsp-decision_governance_core.service`
- `ndsp-decision-package-v1.service` active=`active` workdir=`/opt/ndsp-decision-package-v1` fragment=`/etc/systemd/system/ndsp-decision-package-v1.service`
- `ndsp-enterprise-api.service` active=`inactive` workdir=`/opt/ndsp-enterprise-api` fragment=`/etc/systemd/system/ndsp-enterprise-api.service`
- `ndsp-governance-bridge.service` active=`active` workdir=`/home/nawaf511/empire-core-new/apps/ndsp-governance-bridge` fragment=`/etc/systemd/system/ndsp-governance-bridge.service`
- `ndsp-investing-calendar.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-investing-calendar.service`
- `ndsp-layers-api.service` active=`active` workdir=`/home/nawaf511/empire-core-new/apps/ndsp-layers-api` fragment=`/etc/systemd/system/ndsp-layers-api.service`
- `ndsp-layers.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend/app/api/routers` fragment=`/etc/systemd/system/ndsp-layers.service`
- `ndsp-live-decision-quality.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality` fragment=`/etc/systemd/system/ndsp-live-decision-quality.service`
- `ndsp-live-economic-calendar.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-live-economic-calendar.service`
- `ndsp-live-market-adapter.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndsp-live-market-adapter.service`
- `ndsp-market-prices-updater.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-market-prices-updater.service`
- `ndsp-mt4-freshness-guard.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndsp-mt4-freshness-guard.service`
- `ndsp-news-ticker.service` active=`active` workdir=`/opt/ndsp-news-ticker` fragment=`/etc/systemd/system/ndsp-news-ticker.service`
- `ndsp-password-reset.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/password_reset_gateway` fragment=`/etc/systemd/system/ndsp-password-reset.service`
- `ndsp-platform-gateway-9002.service` active=`active` workdir=`/opt/ndsp-platform-gateway-9002` fragment=`/etc/systemd/system/ndsp-platform-gateway-9002.service`
- `ndsp-platform-gateway.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-platform-gateway.service`
- `ndsp-portal-real-data-api.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-portal-real-data-api` fragment=`/etc/systemd/system/ndsp-portal-real-data-api.service`
- `ndsp-portal-real-data-ledger.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-portal-real-data-ledger.service`
- `ndsp-public-gateway.service` active=`inactive` workdir=`/var/www/ndsp-public-gateway` fragment=`/etc/systemd/system/ndsp-public-gateway.service`
- `ndsp-public-summary-v548.service` active=`active` workdir=`/opt/ndsp-public-summary-v548` fragment=`/etc/systemd/system/ndsp-public-summary-v548.service`
- `ndsp-quality-live-golden-wrapper.service` active=`active` workdir=`` fragment=`/etc/systemd/system/ndsp-quality-live-golden-wrapper.service`
- `ndsp-quality-live-nmp-wrapper.service` active=`active` workdir=`` fragment=`/etc/systemd/system/ndsp-quality-live-nmp-wrapper.service`
- `ndsp-raw-cot-gateway.service` active=`active` workdir=`/home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway` fragment=`/etc/systemd/system/ndsp-raw-cot-gateway.service`
- `ndsp-real-feeds-sync.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-real-feeds-sync.service`
- `ndsp-refresh-live-data.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-refresh-live-data.service`
- `ndsp-refresh-static-data-contract.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-refresh-static-data-contract.service`
- `ndsp-refresh-static-data-contract-v45.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-refresh-static-data-contract-v45.service`
- `ndsp-refresh-static-data-contract-v46.service` active=`activating` workdir=`` fragment=`/etc/systemd/system/ndsp-refresh-static-data-contract-v46.service`
- `ndsp-refresh-static-data-contract-with-nmp.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-refresh-static-data-contract-with-nmp.service`
- `ndsp-register-compat-gateway.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-register-compat-gateway.service`
- `ndsp-scenario-levels-adapter.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend` fragment=`/etc/systemd/system/ndsp-scenario-levels-adapter.service`
- `ndsp-telegram-alert.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-telegram-alert.service`
- `ndsp-telegram-link-listener.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-telegram-link-listener` fragment=`/etc/systemd/system/ndsp-telegram-link-listener.service`
- `ndsp-tradingview-calendar.service` active=`inactive` workdir=`` fragment=`/etc/systemd/system/ndsp-tradingview-calendar.service`
- `ndsp-trial-fingerprint-guard.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-trial-fingerprint-guard.service`
- `ndsp-trial-register-canonical-wrapper.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-trial-register-canonical-wrapper` fragment=`/etc/systemd/system/ndsp-trial-register-canonical-wrapper.service`
- `ndsp-trial-register.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-trial-register.service`
- `ndsp-trial-seats-api.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-trial-seats-api` fragment=`/etc/systemd/system/ndsp-trial-seats-api.service`
- `ndsp-ui-bridge-api.service` active=`active` workdir=`/opt/ndsp-ui-bridge-api` fragment=`/etc/systemd/system/ndsp-ui-bridge-api.service`
- `ndsp-user-alert-channels.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/ndsp-user-alert-channels` fragment=`/etc/systemd/system/ndsp-user-alert-channels.service`
- `ndsp-user-dashboard.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-user-dashboard.service`
- `ndsp-user-login.service` active=`active` workdir=`/home/nawaf511/empire-core-new/backend/auth_api` fragment=`/etc/systemd/system/ndsp-user-login.service`
- `ndsp-user-portal.service` active=`inactive` workdir=`/home/nawaf511/empire-core-new/apps/user-portal` fragment=`/etc/systemd/system/ndsp-user-portal.service`
- `ndsp-v3-portal-gateway.service` active=`active` workdir=`/opt/ndsp-v3-portal-gateway` fragment=`/etc/systemd/system/ndsp-v3-portal-gateway.service`
- `ndsp-v52-contract.service` active=`active` workdir=`` fragment=`/etc/systemd/system/ndsp-v52-contract.service`
- `ndsp-v53-bridge.service` active=`active` workdir=`` fragment=`/etc/systemd/system/ndsp-v53-bridge.service`
- `twelvedata-poller.service` active=`inactive` workdir=`/opt/empire-core/feeds` fragment=`/etc/systemd/system/twelvedata-poller.service`

## API

- `https://api.ndsp.app/api/health` → HTTP `200` `application/json; charset=utf-8`
- `https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT` → HTTP `200` `application/json; charset=utf-8`

## الصفحات

- `https://my.ndsp.app/` → HTTP `200`
- `https://my.ndsp.app/index.html` → HTTP `200`
- `https://my.ndsp.app/decision-support.html` → HTTP `200`
- `https://my.ndsp.app/NDSP_Asset_View.html` → HTTP `200`
- `https://my.ndsp.app/NDSP_Command_Center.html` → HTTP `200`
- `https://my.ndsp.app/NDSP_Daily_Brief.html` → HTTP `200`
- `https://my.ndsp.app/NDSP_Settings_Alerts.html` → HTTP `200`
- `https://my.ndsp.app/login.html` → HTTP `200`
- `https://my.ndsp.app/register.html` → HTTP `200`
- `https://my.ndsp.app/forgot-password.html` → HTTP `200`
- `https://my.ndsp.app/reset-password.html` → HTTP `200`
- `https://my.ndsp.app/admin.html` → HTTP `200`

## سجل الطبقات الـ16

- Exists: `True`
- Valid JSON: `True`
- Layer count: `16`
- SHA-256: `1e82873218176c33ab67176a9ff11494ddf87a72e75ca510abf0d59bcb3d1931`

## مرشحو مصادر الطبقات

### TDL
- `NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002C_frontend_source_intake_20260628_001739/frontend-user-portal-vite/src/main.jsx`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/v1/frontend_contract.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_saas_packages_policy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_user_dashboard_gateway.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/layers/layer_orchestrator.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/shared/tdl_day_logic_v2.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_EXCLUSIONS_AND_ADOPTIONS.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- ... +55 more in JSON

### NMP
- `DSP_NMP_V1_POLICY.md`
- `NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002C_frontend_source_intake_20260628_001739/frontend-user-portal-vite/src/main.jsx`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/v1/frontend_contract.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/layers/layer_orchestrator.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/DSP_NMP_V1_POLICY.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_EXCLUSIONS_AND_ADOPTIONS.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/DSP_NMP_V1_POLICY.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- ... +55 more in JSON

### MARKET_DIRECTION
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/runtime/ndsp_quality_live_golden_wrapper.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-live-decision-quality/server.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-layers-api/app.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/tests/test_ndsp_python_decision_governance_v1.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/tests/test_ndsp_python_tdl_v2_decision_outputs.py`
- `backend/app/ndsp_governance/decision_output_policy.py`
- `backend/app/runtime/ndsp_quality_live_golden_wrapper.py`
- `backend/architecture/ui/artifacts/NDSP_Sovereign_Command_Preview.html`
- `backend/docs/API_CONTRACT.md`
- `backend/docs/BACKEND_GUIDE.md`
- `backend/docs/openapi.yaml`
- `backend/ndsp-live-decision-quality/server.py`
- `backend/runtime/private_governance/final_extra_snapshot/decision_output_policy.py`
- `backend/runtime/private_governance/source_snapshot/decision_output_policy.py`
- `backend/runtime/quarantine/live-before-dev020c-20260629_101120/NDSP_Sovereign_Command_Preview.html`
- `backend/runtime/quarantine/live-html-before-dev018b-20260629_093055/NDSP_Radar_Command.html`
- ... +55 more in JSON

### CORRECTION
- `apps/admin-console/NDSP_Terms_Privacy.html`
- `apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp_latest_16_layers_logic_functions.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Terms_Privacy.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/ndsp_latest_16_layers_logic_functions.py`
- `docs/01-build-control-pack/governance/NDSP_STABILITY_FIRST_TRANSFORMATION_GOVERNANCE_AR.md`
- `docs/01-build-control-pack/governance/NDSP_STABILITY_FIRST_TRANSFORMATION_GOVERNANCE_EN.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_AR.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_EN.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_EN.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_MAP_CURRENT.json`
- `docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md`
- `docs/05-runbooks/NDSP_V13_FINAL_D4_OWNERSHIP_STABILIZATION_AND_REPACKAGE_20260709_075518.md`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_EXPERIENCE_CONTRACT_V1.json`
- `docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `frontend/admin-console/NDSP_Terms_Privacy.html`
- `frontend/public-landing/NDSP_Terms_Privacy.html`

### DIVERGENCE
- `apps/admin-console/data/owner-layer-source-map.json`
- `apps/public-landing/_next/static/chunks/0p431l498zrcc.js`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_tdl_trade_horizon_addons.cjs`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp_latest_16_layers_logic_functions.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/public-landing/_next/static/chunks/0p431l498zrcc.js`
- `backend/auth_api/ndsp_tdl_trade_horizon_addons.cjs`
- `backend/ndsp_latest_16_layers_logic_functions.py`
- `backend/ndsp_tdl_trade_horizon_addons.cjs`
- `backend/runtime/private_governance/config/layers_config.json`
- `backend/runtime/private_governance/final_extra_snapshot/layers_config.json`
- `backend/runtime/private_governance/final_extra_snapshot/layers_engine.py`
- `backend/runtime/private_governance/source_snapshot/layers_engine.py`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_AR.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_EN.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_EN.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_MAP_CURRENT.json`
- `docs/05-runbooks/NDSP_P1_AUTH_FUNCTIONAL_DISCOVERY_READONLY_20260707_232843.md`
- `docs/05-runbooks/NDSP_V18_P8_D6_PUBLIC_TERMS_SANITIZER_20260709_142051.md`

### DAY_LOGIC
- `apps/admin-console/api/research/tdl-day-logic-v2.json`
- `apps/admin-console/config/tdl_day_logic_v2.json`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/shared/tdl_day_logic_v2.js`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/shared/tdl_day_logic_v2.json`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/shared/tdl_day_logic_v2.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/api/research/tdl-day-logic-v2.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/config/tdl_day_logic_v2.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/shared/tdl_day_logic_v2.js`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/shared/tdl_day_logic_v2.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/shared/tdl_day_logic_v2.py`
- `backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/research/tdl_lab/results/latest.json`
- `backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/backend/research/tdl_lab/tdl_lab_engine.py`
- `backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/admin-console-published-pages/tdl-lab-latest.json`
- `backend/architecture/reports/DEV-002H-APPS-SHARED-TESTS-INTAKE-20260628_004224.md`
- `backend/research/tdl_lab/results/latest.json`
- `backend/research/tdl_lab/tdl_lab_engine.py`
- `backend/shared/tdl_day_logic_v2.js`
- `backend/shared/tdl_day_logic_v2.json`
- `backend/shared/tdl_day_logic_v2.py`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_AR.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_EN.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- ... +10 more in JSON

### SCENARIO_LEVELS
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002F_deployment_tools_intake_20260628_003143/backend/ndsp_scenario_levels_adapter.cjs`
- `backend/_backups/DEV002F_deployment_tools_intake_20260628_003143/backend/portal_snapshot_generator.cjs`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-live-decision-quality/server.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Help_Center.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Terms_Privacy.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/app/ndsp_governance/decision_output_policy.py`
- `backend/app/runtime/ndsp_quality_live_nmp_wrapper.py`
- `backend/architecture/reports/DEV-002B-SOURCE-CLASSIFICATION-20260628_001339.md`
- `backend/architecture/reports/DEV-002F-DEPLOYMENT-TOOLS-INTAKE-20260628_003240.md`
- `backend/architecture/reports/DEV-012E-LOCAL-HEALTH-PROCESS-OWNERSHIP-CHECK-20260628_152910.md`
- `backend/architecture/reports/DEV-012Z-RECOVER-AND-CLOSE-SYSTEMD-LOCAL-20260628_172726.md`
- `backend/ndsp-live-decision-quality/server.py`
- `backend/ndsp_scenario_levels_adapter.cjs`
- `backend/portal_snapshot_generator.cjs`
- `backend/runtime/private_governance/final_extra_snapshot/decision_output_policy.py`
- `backend/runtime/private_governance/source_snapshot/decision_output_policy.py`
- `docs/00-build-catalog/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_v1.md`
- ... +55 more in JSON

### MOMENTUM
- `DSP_NMP_V1_POLICY.md`
- `apps/admin-console/NMP_Research_Lab.html`
- `apps/admin-console/data/owner-layer-source-map.json`
- `apps/ndsp-governance-bridge/policies/governance_runtime.py`
- `apps/ndsp-governance-bridge/policies/tdl_v2_policy.py`
- `backend/.backup_execution_bridge_20260529_225823/app_core_governed_pipeline.py`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/__init__.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/cot/cftc_auto_provider.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/cot/cot_asset_mapper.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/cot/manual_cot_provider.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/cot/test_cot_v6_1_storage.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/DSP_NMP_V1_POLICY.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/DSP_NMP_V1_POLICY.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/docs/NDSP_GOVERNANCE_DOCUMENTATION.md`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-live-decision-quality/server.py`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp_latest_16_layers_logic_functions.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NMP_Research_Lab.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/policies/governance_runtime.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/policies/tdl_v2_policy.py`
- `backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/NMP_RESEARCH_LAB_POLICY.md`
- `backend/_backups/DEV002J_research_data_reference_intake_20260628_004658/research/nmp-lab/scripts/nmp_lab_engine.py`
- `backend/app/runtime/ndsp_quality_live_nmp_wrapper.py`
- ... +37 more in JSON

### LIQUIDITY_STRUCTURE
- `apps/admin-console/NDSP_Admin_Console.html`
- `apps/admin-console/data/owner-layer-source-map.json`
- `apps/admin-console/index.html`
- `apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.json`
- `apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.md`
- `apps/ndsp-governance-bridge/policies/tdl_v2_policy.py`
- `apps/public-landing/_next/static/chunks/0dz19whtn4g5a.js`
- `apps/public-landing/_next/static/chunks/0u2g92xsd07bs.js`
- `backend/.backup_execution_bridge_20260529_225823/app_core_governed_pipeline.py`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/v1/frontend_contract.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/__init__.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/black_layer_engine.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Admin_Console.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/index.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.md`
- ... +37 more in JSON

### USD_MACRO
- `apps/admin-console/data/owner-layer-source-map.json`
- `apps/public-landing/_next/static/chunks/0dz19whtn4g5a.js`
- `apps/public-landing/_next/static/chunks/0u2g92xsd07bs.js`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/public-landing/_next/static/chunks/0dz19whtn4g5a.js`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/public-landing/_next/static/chunks/0u2g92xsd07bs.js`
- `docs/01-build-control-pack/governance/NDSP_STABILITY_FIRST_TRANSFORMATION_GOVERNANCE_AR.md`
- `docs/01-build-control-pack/governance/NDSP_STABILITY_FIRST_TRANSFORMATION_GOVERNANCE_EN.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_EN.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_MAP_CURRENT.json`
- `docs/05-runbooks/NDSP_COMMAND_CENTER_RADAR_PREFLIGHT_20260707_095205.md`
- `docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md`
- `docs/05-runbooks/NDSP_DAILY_BRIEF_PREFLIGHT_20260707_101610.md`
- `docs/05-runbooks/NDSP_DECISION_SUPPORT_PREFLIGHT_20260707_100303.md`
- `docs/05-runbooks/NDSP_DISCLAIMER_GATE_PREFLIGHT_20260707_094108.md`
- `docs/05-runbooks/NDSP_MENU_PAGE_MATCH_PREFLIGHT_20260707_094603.md`
- `docs/05-runbooks/NDSP_PAGE_PRIORITY_MATRIX_20260707_210713.md`
- `docs/05-runbooks/NDSP_PATCH_DISCLAIMER_GATE_V1_20260707_094240.md`
- `docs/05-runbooks/NDSP_PATCH_MENU_CANONICAL_PAGE_MATCH_V1_20260707_094821.md`
- `docs/05-runbooks/NDSP_PATCH_MOBILE_MENU_CSS_ONLY_V2_20260707_180918.md`
- `docs/05-runbooks/NDSP_PATCH_MOBILE_MENU_LINK_LAYOUT_V4_20260707_194553.md`
- `docs/05-runbooks/NDSP_PATCH_MOBILE_MENU_TEXT_READABILITY_V3_20260707_181813.md`
- `docs/05-runbooks/NDSP_ROUTES_INVENTORY_AUDIT_20260707_210030.md`
- ... +10 more in JSON

### RISK
- `NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt`
- `apps/admin-console/NDSP_Admin_Console.html`
- `apps/admin-console/data/owner-layer-source-map.json`
- `apps/admin-console/index.html`
- `apps/ndsp-governance-bridge/policies/governance_runtime.py`
- `apps/ndsp-governance-bridge/policies/ndsp_alert_audit.py`
- `apps/ndsp-layers-api/app.py`
- `apps/public-landing/_next/static/chunks/0dz19whtn4g5a.js`
- `apps/public-landing/_next/static/chunks/0t31ucwgip53p.js`
- `backend/.backup_execution_bridge_20260529_225823/app_core_governed_pipeline.py`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/frontend_fields_api.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/services/execution_webhook_bridge.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/backtest/backtest_engine.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/__init__.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/black_layer_engine.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/black_layer/test_black_layer.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/quality/decision_quality_stack.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/quality/test_integration_dqs.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/scenario/scenario_engine.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- ... +51 more in JSON

### GOLDEN_SIGNAL
- `backend/.backup_execution_bridge_20260529_225823/app_core_governed_pipeline.py`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/runtime/ndsp_quality_live_golden_wrapper.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Admin_Console.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Help_Center.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Terms_Privacy.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/data/owner-layer-source-map.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/index.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/NDSP_LAYER_VISIBILITY_OWNER_INTERNAL_POLICY.md`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.json`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/ndsp-governance-bridge/layers/NDSP_OWNER_INTERNAL_16_LAYER_REGISTRY.md`
- `backend/app/ndsp_governance/decision_output_policy.py`
- `backend/app/runtime/ndsp_quality_live_golden_wrapper.py`
- `backend/architecture/ui/artifacts/NDSP_Sovereign_Command_Preview.html`
- `backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/ndsp_layer_name_masking_policy.cjs`
- `backend/runtime/private_governance/final_extra_snapshot/decision_output_policy.py`
- ... +55 more in JSON

### ENHANCED_GOLDEN_SIGNAL
- `backend/architecture/ui/artifacts/NDSP_Sovereign_Command_Preview.html`
- `backend/runtime/quarantine/live-before-dev020c-20260629_101120/NDSP_Sovereign_Command_Preview.html`
- `docs/00-build-catalog/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_v1.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_AR.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_EN.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_MAP_CURRENT.json`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_EXPERIENCE_CONTRACT_V1.json`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_AR_v1.md`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_EN_v1.md`

### DEVILS_ADVOCATE
- `backend/_backups/DEV002C_frontend_source_intake_20260628_001739/frontend-user-portal-vite/src/main.jsx`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/v1/frontend_contract.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_admin_ui_proxy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_layer_name_masking_policy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_saas_packages_policy.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_user_dashboard_gateway.cjs`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_EXCLUSIONS_AND_ADOPTIONS.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.json`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/ndsp_governance/NDSP_SAAS_PACKAGES_POLICY.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/BACKEND_GUIDE.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/NDSP_BACKEND_PACKAGE_README.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_EXCLUSIONS_AND_ADOPTIONS.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/ndsp_governance/NDSP_CURRENT_ADOPTIONS_MASTER.md`
- ... +55 more in JSON

### READINESS_STATE
- `backend/architecture/GOVERNANCE_RULES.md`
- `docs/02-architecture/core/NDSP_16_LAYER_CORE_AND_FUTURE_INTEGRATION_BLUEPRINT_EN.md`
- `docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_AR.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_LOCK_CURRENT_EN.md`
- `docs/05-runbooks/NDSP_CANONICAL_SOURCE_MAP_CURRENT.json`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_AR_v1.md`
- `docs/06-decision-room-contracts/NDSP_DECISION_ROOM_MASTER_CONTRACTS_EN_v1.md`

### DECISION_QUALITY
- `NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt`
- `backend/.backup_execution_bridge_20260529_225823/app_core_governed_pipeline.py`
- `backend/.backup_execution_bridge_20260529_225823/governed_pipeline.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/decision_quality_public.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/ndsp_public_quality_unique.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/api/v1/frontend_contract.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/decision_output_policy.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/ndsp_governance/frontend_fields_api.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/runtime/ndsp_quality_live_golden_wrapper.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/backtest/backtest_engine.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/macro/__init__.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/quality/decision_quality_stack.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/app/support_layers/quality/test_integration_dqs.py`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/auth_api/ndsp_trial_register_gateway.cjs`
- `backend/_backups/DEV002D_backend_core_source_intake_20260628_002228/backend/layers/layer_orchestrator.py`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_docs_policy_intake_20260628_002836/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/API_CONTRACT.md`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/backend/docs/openapi.yaml`
- `backend/_backups/DEV002E_hotfix_placeholder_scan_20260628_002936/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.md`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-live-decision-quality/server.py`
- `backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp_latest_16_layers_logic_functions.py`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Admin_Console.html`
- `backend/_backups/DEV002H_apps_shared_tests_intake_20260628_004041/apps/admin-console/NDSP_Help_Center.html`
- ... +55 more in JSON

## القرار

تم جمع الأدلة ومرشحي المصدر. لا يبدأ الدمج أو الحذف أو إعادة البناء حتى اعتماد مسار واحد لكل طبقة ومسؤولية تشغيلية.

`FINAL_STATUS=NDSP_CANONICAL_SOURCE_LOCK_EVIDENCE_CAPTURED_OK`
