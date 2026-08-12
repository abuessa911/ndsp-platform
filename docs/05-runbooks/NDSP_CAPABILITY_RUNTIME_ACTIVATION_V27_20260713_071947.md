============================================================
NDSP — Capability Runtime Activation and Governed Layer Exposure V27
DATE=2026-07-13T07:19:58+02:00
MODE=TRUTHFUL_RUNTIME_EVIDENCE_NO_FRONTEND_REBUILD
PROJECT=/home/nawaf511/empire-core-new
LIVE=/var/www/ndsp-my
EVIDENCE=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_071947.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_071947
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-20260713_071947
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
PRE_SAME_ORIGIN_HTTP=200
[OK] V26 baseline and public contract verified
[OK] missing personalized-experience capability module installed safely
[OK] capability runtime controller installed
Created symlink /etc/systemd/system/timers.target.wants/ndsp-capability-runtime-controller.timer → /etc/systemd/system/ndsp-capability-runtime-controller.timer.
[OK] all 28 capabilities are installed and functionally verified; live states are evidence-based
curl: (7) Failed to connect to 127.0.0.1 port 9082 after 0 ms: Couldn't connect to server
LOCAL_9082_HTTP=000
============================================================
[ROLLBACK] local 9082 HTTP=000
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.js
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.timer
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.service
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/platform/runtime/capability_runtime_controller_v1.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/personalization.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/__init__.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_071947.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_071947
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-20260713_071947
FINAL_STATUS=ROLLED_BACK
