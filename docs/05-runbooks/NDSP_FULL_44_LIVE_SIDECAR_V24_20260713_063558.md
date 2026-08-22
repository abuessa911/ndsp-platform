============================================================
NDSP — Full 16 Layers + 28 Capabilities CORS-Safe Live Sidecar V24
DATE=2026-07-13T06:35:58+02:00
MODE=ADDITIVE_NO_FRONTEND_REBUILD_NARROW_CORS
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
WRAPPER=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V24_20260713_063558.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V24_20260713_063558
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v24-20260713_063558
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
[OK] pre-change API gate passed
[OK] public governance projection module installed
FASTAPI_APP_ASSIGNMENT_NOT_FOUND
============================================================
[ROLLBACK] unexpected error line=367 rc=1
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V24_20260713_063558.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V24_20260713_063558
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v24-20260713_063558
FINAL_STATUS=ROLLED_BACK
