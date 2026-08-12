============================================================
NDSP — Full 16 Layers + 28 Capabilities Exposure and Display V22
DATE=2026-07-12T23:42:08+02:00
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
WRAPPER=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_EXPOSURE_DISPLAY_V22_20260712_234208.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_EXPOSURE_DISPLAY_V22_20260712_234208
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-exposure-display-v22-20260712_234208
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
[OK] pre-change API gate passed
[OK] public governance projection module installed
[OK] 9082 wrapper patched additively
[OK] public API now exposes all 16 layers and 28 capabilities
[OK] frontend source now consumes live 16+28 contract

> ndsp-user-portal-vite@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 27 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   8.02 kB │ gzip:  2.42 kB
dist/assets/index-CB5D1TQG.css    8.81 kB │ gzip:  2.62 kB
dist/assets/index-BX9FubtP.js   169.72 kB │ gzip: 53.47 kB
✓ built in 1.87s
[OK] frontend build passed
[OK] built frontend deployed with safe permissions and compatibility aliases restored
============================================================
[ROLLBACK] browser full-display and preservation gate failed
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/lib/ndspGovernance.ts
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Decisions.tsx
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Governance.tsx
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/index-BX9FubtP.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/index-CB5D1TQG.css
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_EXPOSURE_DISPLAY_V22_20260712_234208.md
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-exposure-display-v22-20260712_234208
FINAL_STATUS=ROLLED_BACK
