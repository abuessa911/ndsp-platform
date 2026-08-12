
============================================================
NDSP — ADD LOGOUT TO DESKTOP MORE MENU FROM SOURCE V12.5
============================================================
DATE=2026-07-27T20:54:45+02:00
HOST=vmi2934783.contaboserver.net
SOURCE_DIR=/home/nawaf511/Downloads/NDSP_COMMERCIAL_FRONTEND_LIVE_V1
LIVE_PORTAL=/var/www/ndsp-my/portal
PUBLIC_BASE=https://my.ndsp.app
BACKUP=/home/nawaf511/empire-core-new/backups/portal-desktop-logout-v12-5/20260727_205445
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_DESKTOP_LOGOUT_V12_5_20260727_205445.md
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
STAGED_SOURCE=/tmp/ndsp_portal_desktop_logout_v12_5_NXp2iG/source
STAGED_NODE_MODULES=/home/nawaf511/empire-core-new/frontend/user-portal-vite/node_modules
STAGED_SOURCE_GATE=PASS

============================================================
5) PATCH TRUE REACT AND I18N SOURCE
============================================================
TRUE_SOURCE_PATCH_GATE=PASS

============================================================
6) BUILD FRESH VITE ARTIFACT
============================================================
VITE_BUILD_BASE=/portal/
STAGED_JS_ASSET_PATH=/portal/assets/index-YRhdpSxC.js
STAGED_JS_LOCAL=/tmp/ndsp_portal_desktop_logout_v12_5_NXp2iG/dist/assets/index-YRhdpSxC.js
BUILT_JS_COUNT=1
SOURCE_MAP_COUNT=0
FRESH_BUILD_GATE=PASS

============================================================
7) INSTALL CANONICAL SOURCE
============================================================
MAIN_SHA256_AFTER=61af61873e636f04401cf7f4b4c35cca26500f974eab9cce5d8c830c4cbe85c5
CSS_SHA256_AFTER=5dd3b31a3fda41d58fef21bc2b313cbf5772c88d679fb374115c7ab708c003ec
CANONICAL_SOURCE_INSTALL_GATE=PASS

============================================================
8) ATOMIC LIVE PORTAL DEPLOYMENT
============================================================
PREVIOUS_HASHED_ASSETS_PRESERVED=YES
LIVE_PORTAL_ATOMIC_SWAP=PASS

============================================================
9) VERIFY PUBLIC BUILD AND LOGOUT ROUTE
============================================================
PUBLIC_PORTAL_HTTP=200
PUBLIC_HTML_REFERENCES_NEW_ASSET=YES
PUBLIC_JS_HTTP=200
PUBLIC_JS_URL=https://my.ndsp.app/portal/assets/index-YRhdpSxC.js?v=20260727_205445
PUBLIC_JS_EQUALS_STAGED_BUILD=YES
PUBLIC_LOGOUT_MARKER=VERIFIED
PUBLIC_ARABIC_LABEL=VERIFIED
PUBLIC_ENGLISH_LABEL=VERIFIED
LOGOUT_ENDPOINT_PROBE_HTTP=200
PUBLIC_VERIFICATION_GATE=PASS

============================================================
10) COMMIT AND FINAL RESULT
============================================================
FINAL_STATUS=NDSP_PORTAL_DESKTOP_LOGOUT_V12_5_DEPLOYED_AND_VERIFIED
DESKTOP_MORE_MENU_LOGOUT=VERIFIED
MOBILE_DRAWER_LOGOUT=VERIFIED
CENTRAL_I18N_LOGOUT_KEYS=VERIFIED
LOGOUT_API=/api/auth/logout
SUCCESS_REDIRECT=/login/?logged_out=1
SOURCE_FIRST_DEPLOYMENT=YES
VITE_BUILD_BASE=/portal/
PUBLIC_JS_EQUALS_STAGED_BUILD=YES
DIRECT_DIST_PATCH_USED=NO
RUNTIME_INJECTION_USED=NO
DATABASE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
SERVICE_RESTARTED=NO
BACKUP=/home/nawaf511/empire-core-new/backups/portal-desktop-logout-v12-5/20260727_205445
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PORTAL_DESKTOP_LOGOUT_V12_5_20260727_205445.md
