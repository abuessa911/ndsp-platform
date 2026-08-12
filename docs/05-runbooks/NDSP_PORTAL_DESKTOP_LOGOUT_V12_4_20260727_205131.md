
============================================================
NDSP — ADD LOGOUT TO DESKTOP MORE MENU FROM SOURCE V12.4
============================================================
DATE=2026-07-27T20:51:31+02:00
HOST=vmi2934783.contaboserver.net
SOURCE_DIR=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1
LIVE_PORTAL=/var/www/ndsp-my/portal
PUBLIC_BASE=https://my.ndsp.app
BACKUP=/home/nawaf511/empire-core-new/backups/portal-desktop-logout-v12-4/20260727_205131
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_DESKTOP_LOGOUT_V12_4_20260727_205131.md
MODE=SOURCE_FIRST_BUILD_ATOMIC_DEPLOY

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) PRECONDITIONS AND SOURCE BINDING
============================================================
MAIN_SHA256_BEFORE=0cf384c20ae503c7e39c8d4f3e42274c5a923d04b5d5708d1522c1b780237be5
CSS_SHA256_BEFORE=483712fd3557fbdd3c454a6259e0294725e2333ad31c9ad49a378ede3d6e5740
TRUE_SOURCE_BINDING_GATE=PASS

============================================================
2) DISCOVER COMPATIBLE REUSABLE NODE_MODULES
============================================================
NODE_MODULES=/home/nawaf511/empire-core-new/frontend/user-portal-vite/node_modules
VITE_VERSION=vite/6.4.3 linux-x64 node-v22.23.1
NODE_MODULES_GATE=PASS

============================================================
3) BACKUP SOURCE AND LIVE PORTAL
============================================================
BACKUP_GATE=PASS

============================================================
4) CREATE STAGED SOURCE COPY
============================================================
STAGED_SOURCE=/tmp/ndsp_portal_desktop_logout_v12_3_mNl2Ym/source
STAGED_NODE_MODULES=/home/nawaf511/empire-core-new/frontend/user-portal-vite/node_modules
STAGED_SOURCE_GATE=PASS

============================================================
5) PATCH TRUE REACT AND I18N SOURCE
============================================================
TRUE_SOURCE_PATCH_GATE=PASS

============================================================
6) BUILD FRESH VITE ARTIFACT
============================================================
BUILT_JS_COUNT=1
SOURCE_MAP_COUNT=0
FRESH_BUILD_GATE=PASS

============================================================
7) INSTALL CANONICAL SOURCE
============================================================
MAIN_SHA256_AFTER=a2e515751892f12d4fdb8cd59fb2f175621e7c49759bff4963bf60c9c73a4820
CSS_SHA256_AFTER=0db834542fa417d42e0e142b7da030a68c937e14129d771ff48fa1abaa5e0249
CANONICAL_SOURCE_INSTALL_GATE=PASS

============================================================
8) ATOMIC LIVE PORTAL DEPLOYMENT
============================================================
LIVE_PORTAL_ATOMIC_SWAP=PASS

============================================================
9) VERIFY PUBLIC BUILD AND LOGOUT ROUTE
============================================================
FAIL=PUBLIC_JS_HTTP_404

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
LIVE_PORTAL_ROLLBACK=PASS
CANONICAL_SOURCE_ROLLBACK=PASS
DATABASE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
DIRECT_DIST_PATCH_USED=NO
FINAL_STATUS=NDSP_PORTAL_DESKTOP_LOGOUT_V12_4_FAILED_AND_ROLLED_BACK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_DESKTOP_LOGOUT_V12_4_20260727_205131.md
