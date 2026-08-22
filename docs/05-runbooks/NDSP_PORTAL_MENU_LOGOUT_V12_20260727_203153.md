
============================================================
NDSP — ADD LOGOUT BUTTON INSIDE USER PORTAL MENU V12
============================================================
DATE=2026-07-27T20:31:53+02:00
HOST=vmi2934783.contaboserver.net
CORE=/home/nawaf511/empire-core-new
LIVE_PORTAL=/var/www/ndsp-my/portal
PUBLIC_BASE=https://my.ndsp.app
BACKUP=/home/nawaf511/empire-core-new/backups/portal-menu-logout-v12/20260727_203153
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_MENU_LOGOUT_V12_20260727_203153.md
MODE=SOURCE_ONLY_BUILD_ATOMIC_DEPLOY

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) DISCOVER CANONICAL PORTAL SOURCE
============================================================
FAIL=SOURCE_NODE_MODULES_MISSING:/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1/node_modules

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
FINAL_STATUS=NDSP_PORTAL_MENU_LOGOUT_V12_FAILED_AND_ROLLED_BACK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_MENU_LOGOUT_V12_20260727_203153.md
