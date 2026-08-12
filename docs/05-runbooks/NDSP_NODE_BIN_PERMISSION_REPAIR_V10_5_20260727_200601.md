
============================================================
NDSP — NODE BIN PERMISSION REPAIR AND RECOVERY DEPLOYMENT V10.5
============================================================
DATE=2026-07-27T20:06:01+02:00
HOST=vmi2934783.contaboserver.net
USER=nawaf511
PROJECT=/home/nawaf511/empire-core-new
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
AUTH_SERVICE=ndsp-auth-core-clean.service
V7_2=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_2.sh
V10_3=/home/nawaf511/ndsp_prepare_reset_contract_then_run_v7_v10_3.sh
BACKUP=/home/nawaf511/empire-core-new/backups/node-bin-permission-repair-v10-5/20260727_200601
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_NODE_BIN_PERMISSION_REPAIR_V10_5_20260727_200601.md
DIRECT_SOURCE_CONTENT_EDIT_BY_WRAPPER=NO
DIRECT_UI_DIST_EDIT_BY_WRAPPER=NO

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) PRECONDITIONS AND SCRIPT BINDINGS
============================================================
ACTIVE_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1
NODE_MODULES_LINK=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1/node_modules
NODE_MODULES_REAL=/opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules
V7_2_SHA256=3a3d69f86ac5248feeeeaee9fc7075b7e6add0c3823bca29647cd51e7ef44d5d
V10_3_SHA256=94e99b2ec69a03262c53d358a1c94c5389e872565dd9b51cc82bcb883fc03d89
PRECONDITION_GATE=PASS

============================================================
2) DISCOVER PACKAGE BIN TARGETS
============================================================
BIN_TARGET_COUNT=17
RESTORE_SCRIPT=/home/nawaf511/empire-core-new/backups/node-bin-permission-repair-v10-5/20260727_200601/restore-original-bin-modes.sh
BIN_TARGET_DISCOVERY_GATE=PASS

============================================================
3) RESTORE EXECUTABLE BITS ON PACKAGE BIN TARGETS
============================================================
BIN_TARGET_CONTENT_HASH_UNCHANGED=YES
EXECUTABLE_PERMISSION_REPAIR_GATE=PASS

============================================================
4) VERIFY BUILD TOOLS DIRECTLY
============================================================
TOOL=tsc EXIT=0 OUTPUT=Version 5.9.3 
TOOL=vite EXIT=0 OUTPUT=vite/5.4.21 linux-x64 node-v22.23.1 
TOOL=esbuild EXIT=0 OUTPUT=0.21.5 
TOOL=rollup EXIT=0 OUTPUT=rollup v4.62.2 
NODE_BIN_PERMISSION_REPAIR_COMMITTED=YES
SHARED_NODE_MODULES_CONTENT_CHANGED=NO
SHARED_NODE_MODULES_OWNERSHIP_CHANGED=NO
SHARED_NODE_MODULES_EXECUTABLE_BITS_RESTORED=YES
BUILD_TOOL_GATE=PASS

============================================================
5) RUN GOVERNED RECOVERY DEPLOYMENT V10.3
============================================================

============================================================
NDSP — PREPARE RESET CONTRACT THEN RUN V7 — V10
============================================================
DATE=2026-07-27T20:06:08+02:00
PROJECT=/home/nawaf511/empire-core-new
FORGOT_HTML=/var/www/ndsp-my/forgot-password.html
RECOVERED_RESET=/var/www/html/reset-password.html
RESET_HTML=/var/www/ndsp-my/reset-password.html
CANONICAL_DIR=/home/nawaf511/empire-core-new/frontend/auth-recovery
V7_SCRIPT=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_2.sh
BACKUP=/home/nawaf511/empire-core-new/backups/prepare-reset-contract-v10/20260727_200608
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_200608.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) VERIFY INPUT SOURCES
============================================================
RECOVERED_RESET_SHA256=a4c7e7ecb8dd0e3cca396f042657f8ec51b90fac0a45d6f6b5f85ff28034b90a
V7_SHA256=3a3d69f86ac5248feeeeaee9fc7075b7e6add0c3823bca29647cd51e7ef44d5d
FORGOT_PAGE_CANONICAL_API_GATE=PASS
INPUT_SOURCE_GATE=PASS

============================================================
2) PATCH RECOVERED RESET PAGE IN STAGE
============================================================
RESET_ENDPOINT_REPLACEMENT_COUNT=1
RESET_API=/api/auth/reset-password
PATCHED_RESET_SOURCE_GATE=PASS
PATCHED_RESET_JAVASCRIPT_GATE=PASS

============================================================
3) BACKUP CURRENT PRE-SEED STATE
============================================================
CANONICAL_EXISTED=0
RESET_LIVE_EXISTED=0
BACKUP_GATE=PASS

============================================================
4) INSTALL CANONICAL RECOVERY SOURCE
============================================================
CANONICAL_SOURCE_INSTALLED=YES
CANONICAL_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery

============================================================
5) SEED MISSING LIVE RESET FILE
============================================================
LIVE_RESET_SEED=PASS

============================================================
6) RUN GOVERNED TRUE-SOURCE V7
============================================================

============================================================
NDSP — AUTH RECOVERY TRUE SOURCE FIX V7
============================================================
DATE=2026-07-27T20:06:10+02:00
HOST=vmi2934783.contaboserver.net
DOMAIN=my.ndsp.app
PROJECT=/home/nawaf511/empire-core-new
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
AUTH_SERVICE=ndsp-auth-core-clean.service
RESET_SERVER=/home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js
RESET_SERVICE=ndsp-password-reset.service
RESET_PORT=9027
FORGOT_HTML=/var/www/ndsp-my/forgot-password.html
RESET_HTML=/var/www/ndsp-my/reset-password.html
CANONICAL_RECOVERY=/home/nawaf511/empire-core-new/frontend/auth-recovery
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-true-source-fix-v7/20260727_200610
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_200610.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) REQUIRED COMMANDS AND TRUE SOURCE BINDINGS
============================================================
OLD_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1
PUBLIC_LOGIN_EQUALS_ACTIVE_UI_DIST=YES
TRUE_LOGIN_SOURCE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1/ui/src/main.tsx
TRUE_LOGIN_BUILD=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1/ui-dist/index.html
TRUE_SOURCE_BINDING_GATE=PASS

============================================================
2) VERIFY EXISTING RECOVERY PAGE CONTRACT
============================================================
EXISTING_RECOVERY_PAGE_CONTENT_GATE=PASS

============================================================
3) BACKUP CURRENT SOURCES
============================================================
CANONICAL_RECOVERY_EXISTED=1
NGINX_BACKUP_FILE_COUNT=1
BACKUP_GATE=PASS

============================================================
4) CREATE NEW AUTH RELEASE
============================================================
NODE_MODULES_REUSED=node_modules
NEW_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
NEW_AUTH_RELEASE_COPY_GATE=PASS

============================================================
5) FIX LOGIN LINK IN TRUE SOURCE
============================================================
TRUE_SOURCE_REPLACEMENT_COUNT=1
TRUE_AUTH_SOURCE_LOGIN_LINK_GATE=PASS

============================================================
6) BUILD NEW AUTH UI
============================================================

> ndsp-clean-auth-core@2.4.0 build
> npm run build:server && npm run build:ui


> ndsp-clean-auth-core@2.4.0 build:server
> tsc -p server/tsconfig.json


> ndsp-clean-auth-core@2.4.0 build:ui
> vite build --config ui/vite.config.ts

[36mvite v5.4.21 [32mbuilding for production...[36m[39m
transforming...
[32m✓[39m 30 modules transformed.
rendering chunks...
computing gzip size...
[2m../ui-dist/[22m[32mindex.html                 [39m[1m[2m  0.55 kB[22m[1m[22m[2m │ gzip:  0.36 kB[22m
[2m../ui-dist/[22m[2massets/[22m[35mindex-BndmgE4p.css  [39m[1m[2m  4.65 kB[22m[1m[22m[2m │ gzip:  1.67 kB[22m
[2m../ui-dist/[22m[2massets/[22m[36mindex-D4g0JUF9.js   [39m[1m[2m146.13 kB[22m[1m[22m[2m │ gzip: 47.56 kB[22m
[32m✓ built in 3.79s[39m
TRUE_SOURCE_BUILD_GATE=PASS
AUTH_UI_BUILD_DIR=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
TRUE_SOURCE_BUILD_GATE=PASS

============================================================
7) FIX RESET EMAIL LINK IN BACKEND SOURCE
============================================================
PASSWORD_RESET_EMAIL_LINK_SOURCE_GATE=PASS

============================================================
8) CREATE CANONICAL RECOVERY SOURCE SNAPSHOT
============================================================
CANONICAL_RECOVERY_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery
CANONICAL_RECOVERY_SOURCE_GATE=PASS

============================================================
9) PREPARE NGINX SOURCE ROUTES
============================================================
NGINX_PATCHED_FILE_COUNT=1
NGINX_PATCHED_HTTPS_SERVER_COUNT=1
NGINX_SOURCE_STAGE_GATE=PASS

============================================================
10) INSTALL BACKEND AND NGINX SOURCES
============================================================
NGINX_SOURCE_INSTALLED=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
BACKEND_SOURCE_INSTALL_GATE=PASS
NGINX_SOURCE_INSTALL_GATE=PASS

============================================================
11) ATOMIC AUTH CUTOVER AND RELOAD
============================================================
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
AUTH_ACTIVE_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
AUTH_SERVICE_RESTARTED=YES
RESET_SERVICE_RESTARTED=YES
NGINX_RELOADED=YES

============================================================
12) VERIFY PUBLIC LOGIN TRUE BUILD
============================================================
PUBLIC_LOGIN_TRUE_BUILD_GATE=PASS
PUBLIC_LOGIN_HTTP=200
PUBLIC_LOGIN_EQUALS_NEW_UI_DIST=YES
PUBLIC_LOGIN_FORGOT_LINK=/forgot-password/
PUBLIC_LOGIN_TRUE_BUILD_GATE=PASS

============================================================
13) VERIFY PUBLIC RECOVERY PAGES
============================================================
PUBLIC_FORGOT_PAGE_HTTP=200
PUBLIC_RESET_PAGE_HTTP=200
PORTAL_SHELL_ON_RECOVERY_ROUTES=NO
PUBLIC_RECOVERY_PAGE_GATE=PASS

============================================================
14) VERIFY SAME-ORIGIN API ROUTES
============================================================
PUBLIC_FORGOT_API_HTTP=200
PUBLIC_RESET_INVALID_TOKEN_HTTP=400
FORGOT_REQUEST_REACHED_PASSWORD_RESET_BACKEND=PASS
RESET_REQUEST_REACHED_PASSWORD_RESET_BACKEND=PASS
REQUEST_REMAINED_FRONTEND_ONLY=NO

============================================================
15) SOURCE AND DEPLOYMENT AUDIT
============================================================
AUTH_LOGIN_CHANGED_IN_TRUE_SOURCE=YES
AUTH_UI_REBUILT_FROM_TRUE_SOURCE=YES
DIRECT_UI_DIST_EDIT_USED=NO
AUTH_RELEASE_ATOMIC_CUTOVER=YES
PASSWORD_RESET_BACKEND_SOURCE_CHANGED=YES
NGINX_SOURCE_CHANGED=YES
RUNTIME_PATCH_USED=NO
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
SOURCE_AND_DEPLOYMENT_AUDIT=PASS

============================================================
16) FINAL RESULT
============================================================
FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_DEPLOYED_AND_VERIFIED
ROOT_CAUSE=PUBLIC_LOGIN_WAS_SERVED_FROM_AUTH_CORE_UI_DIST
TRUE_LOGIN_SOURCE=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7/ui/src/main.tsx
TRUE_LOGIN_BUILD=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7/ui-dist
AUTH_ACTIVE_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
LOGIN_FORGOT_LINK=/forgot-password/
FORGOT_PASSWORD_PAGE=VERIFIED
RESET_PASSWORD_PAGE=VERIFIED
FORGOT_PASSWORD_API_ON_MY_NDSP_APP=VERIFIED
RESET_PASSWORD_API_ON_MY_NDSP_APP=VERIFIED
EMAIL_RESET_LINK=https://my.ndsp.app/reset-password/
REQUESTS_REACHED_BACKEND=YES
PORTAL_SHELL_ON_RECOVERY_ROUTES=NO
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-true-source-fix-v7/20260727_200610
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_200610.md

============================================================
تم إصلاح رحلة استعادة كلمة المرور من المصدر الحقيقي.
افتح من الجوال:
https://my.ndsp.app/forgot-password/?v=20260727_200610

التقرير:
/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_200610.md

الإصدار النشط:
/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
============================================================

============================================================
7) FINAL RESULT
============================================================
FINAL_STATUS=NDSP_PREPARE_RESET_CONTRACT_V10_AND_V7_COMPLETED
V7_FINAL_STATUS=DEPLOYED_AND_VERIFIED
FORGOT_API=/api/auth/forgot-password
RESET_API=/api/auth/reset-password
LEGACY_RESET_ENDPOINT=/ndsp-rp/reset REMOVED
CANONICAL_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
RUNTIME_PATCH_USED=NO
BACKUP=/home/nawaf511/empire-core-new/backups/prepare-reset-contract-v10/20260727_200608
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_200608.md

============================================================
تم تصحيح عقد صفحة إعادة كلمة المرور وتشغيل V7.
افتح:
https://my.ndsp.app/forgot-password/
التقرير:
/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_200608.md
============================================================

============================================================
6) FINAL RESULT
============================================================
FINAL_STATUS=NDSP_NODE_BIN_PERMISSION_REPAIR_V10_5_AND_DEPLOYMENT_COMPLETED
NODE_BIN_TARGET_COUNT=17
NODE_BIN_CONTENT_HASH_UNCHANGED=YES
NODE_BIN_EXECUTABLE_BITS_RESTORED=YES
AUTH_RECOVERY_DEPLOYMENT=DEPLOYED_AND_VERIFIED
DATABASE_SCHEMA_CHANGED_BY_WRAPPER=NO
DATABASE_DIRECT_EDIT_BY_WRAPPER=NO
DIRECT_UI_DIST_EDIT_BY_WRAPPER=NO
BACKUP=/home/nawaf511/empire-core-new/backups/node-bin-permission-repair-v10-5/20260727_200601
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_NODE_BIN_PERMISSION_REPAIR_V10_5_20260727_200601.md
