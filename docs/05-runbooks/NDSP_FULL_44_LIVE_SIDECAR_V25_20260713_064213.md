============================================================
NDSP — Full 16 Layers + 28 Capabilities Runtime-Discovered CORS Live Sidecar V25
DATE=2026-07-13T06:42:13+02:00
MODE=ADDITIVE_NO_FRONTEND_REBUILD_NARROW_CORS
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
WRAPPER=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V25_20260713_064213.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V25_20260713_064213
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v25-20260713_064213
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
[OK] pre-change API gate passed
[OK] public governance projection module installed
============================================================
[ROLLBACK] public API CORS header for my.ndsp.app is missing
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V25_20260713_064213.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V25_20260713_064213
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v25-20260713_064213
FINAL_STATUS=ROLLED_BACK
