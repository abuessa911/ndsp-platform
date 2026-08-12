
============================================================
NDSP — ADD LOGOUT BUTTON INSIDE USER PORTAL MENU V12.1
============================================================
DATE=2026-07-27T20:38:29+02:00
HOST=vmi2934783.contaboserver.net
CORE=/home/nawaf511/empire-core-new
LIVE_PORTAL=/var/www/ndsp-my/portal
PUBLIC_BASE=https://my.ndsp.app
BACKUP=/home/nawaf511/empire-core-new/backups/portal-menu-logout-v12-1/20260727_203829
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_MENU_LOGOUT_V12_1_20260727_203829.md
MODE=SOURCE_ONLY_BUILD_ATOMIC_DEPLOY

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) DISCOVER CANONICAL PORTAL SOURCE
============================================================
SOURCE_DIR=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1
SOURCE_MAIN=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/src/main.jsx
SOURCE_CSS=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/src/styles.css

============================================================
1.1) DISCOVER COMPATIBLE REUSABLE NODE_MODULES
============================================================
NODE_MODULES=/home/nawaf511/empire-core-new/frontend/user-portal-vite/node_modules
NODE_MODULES_VITE=vite/6.4.3 linux-x64 node-v22.23.1
SOURCE_AND_BUILD_DEPENDENCY_DISCOVERY_GATE=PASS

============================================================
2) BACKUP SOURCE AND LIVE PORTAL
============================================================
SOURCE_MAIN_SHA256_BEFORE=0cf384c20ae503c7e39c8d4f3e42274c5a923d04b5d5708d1522c1b780237be5
SOURCE_CSS_SHA256_BEFORE=483712fd3557fbdd3c454a6259e0294725e2333ad31c9ad49a378ede3d6e5740
BACKUP_GATE=PASS

============================================================
3) CREATE STAGED SOURCE COPY
============================================================
STAGED_SOURCE_GATE=PASS

============================================================
4) MODIFY THE ACTUAL REACT MENU SOURCE
============================================================

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
FINAL_STATUS=NDSP_PORTAL_MENU_LOGOUT_V12_1_FAILED_AND_ROLLED_BACK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_MENU_LOGOUT_V12_1_20260727_203829.md
