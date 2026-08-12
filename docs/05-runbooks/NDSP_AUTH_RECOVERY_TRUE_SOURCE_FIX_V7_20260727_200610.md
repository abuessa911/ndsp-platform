
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
NGINX_SOURCE_STAGE_GATE=PASS

============================================================
10) INSTALL BACKEND AND NGINX SOURCES
============================================================
NGINX_SOURCE_INSTALLED=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
BACKEND_SOURCE_INSTALL_GATE=PASS
NGINX_SOURCE_INSTALL_GATE=PASS

============================================================
11) ATOMIC AUTH CUTOVER AND RELOAD
============================================================
AUTH_ACTIVE_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_200610-auth-recovery-true-source-fix-v7
AUTH_SERVICE_RESTARTED=YES
RESET_SERVICE_RESTARTED=YES
NGINX_RELOADED=YES

============================================================
12) VERIFY PUBLIC LOGIN TRUE BUILD
============================================================
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
