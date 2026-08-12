# NDSP Fix Reference Levels Payload V2
DATE=2026-07-09T19:09:30+02:00
PROJECT_DIR=/home/nawaf511/empire-core-new
APP_DIR=/home/nawaf511/empire-core-new/frontend/user-portal-vite
MAIN=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_FIX_REFERENCE_LEVELS_PAYLOAD_V2_20260709_190927

## Fixed
- P1: Reference levels now prefer scenario payload from /api/scenario/levels.
- P2: Adapter keys supported: activation_price, arrival_price, review_price, cancel_price, invalidation_price, nmp_price.
- Preserved previous fixes: no .html menu hrefs, no current-clock Last Update.

## No Production Actions
- No deploy.
- No PM2 restart.
- No Nginx change.
- No backend/API modification.

FINAL_STATUS=REFERENCE_LEVELS_PAYLOAD_V2_LOCAL_OK_READY_FOR_CODEX_REVIEW
