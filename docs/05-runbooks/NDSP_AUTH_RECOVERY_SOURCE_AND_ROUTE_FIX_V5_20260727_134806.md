
============================================================
NDSP — AUTH RECOVERY SOURCE AND ROUTE FIX V5
============================================================
DATE=2026-07-27T13:48:06+02:00
HOST=vmi2934783.contaboserver.net
DOMAIN=my.ndsp.app
PROJECT=/home/nawaf511/empire-core-new
RESET_SERVER=/home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js
RESET_SERVICE=ndsp-password-reset.service
RESET_PORT=9027
CANONICAL_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery
WEB_ROOT=/var/www/ndsp-my
MODE=SOURCE_FIRST_BACKEND_NGINX_AND_STATIC_DEPLOY
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-source-and-route-fix-v5/20260727_134806
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_SOURCE_AND_ROUTE_FIX_V5_20260727_134806.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) REQUIRED COMMANDS AND PRECONDITIONS
============================================================
SERVICE_WORKING_DIRECTORY=/home/nawaf511/empire-core-new/backend/password_reset_gateway
SERVICE_EXEC_START={ path=/usr/bin/node ; argv[]=/usr/bin/node /home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
PASSWORD_RESET_PORT=9027
PRECONDITION_GATE=PASS

============================================================
2) VERIFY CURRENT ROOT CAUSE
============================================================
LOCAL_FORGOT_BACKEND_HTTP=200
LOCAL_RESET_INVALID_TOKEN_HTTP=400
PUBLIC_MY_FORGOT_BEFORE_HTTP=404
ROOT_CAUSE_GATE=PASS
ROOT_CAUSE_1=MY_NDSP_APP_AUTH_PROXY_POINTS_TO_WRONG_BACKEND
ROOT_CAUSE_2=RECOVERY_STATIC_DIRECTORIES_NOT_GOVERNED
ROOT_CAUSE_3=EMAIL_LINK_USES_RESET_PASSWORD_HTML

============================================================
3) DISCOVER ACTIVE NGINX SOURCE FILES
============================================================
ACTIVE_NGINX_SOURCE=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf

============================================================
4) SECURE BACKUP
============================================================
CANONICAL_SOURCE_EXISTED=0
FORGOT_DIRECTORY_EXISTED=0
RESET_DIRECTORY_EXISTED=0
NGINX_BACKUP_FILE_COUNT=1
BACKUP_GATE=PASS

============================================================
5) PREPARE LOGIN CANONICAL SOURCE
============================================================
LOGIN_CANONICAL_SOURCE_GATE=PASS

============================================================
6) CREATE RECOVERY PAGE SOURCE
============================================================
RECOVERY_PAGE_SOURCE_CREATED=YES
RECOVERY_JAVASCRIPT_SYNTAX_GATE=PASS

============================================================
7) PATCH PASSWORD-RESET BACKEND SOURCE
============================================================
PASSWORD_RESET_BACKEND_SOURCE_GATE=PASS

============================================================
8) CREATE CANONICAL SOURCE MANIFEST
============================================================
CANONICAL_SOURCE_MANIFEST_CREATED=YES

============================================================
9) PREPARE NGINX SOURCE CHANGES
============================================================
NGINX_SOURCE_STAGE_GATE=PASS

============================================================
10) INSTALL CANONICAL FRONTEND SOURCE
============================================================
CANONICAL_SOURCE_INSTALLED=YES
CANONICAL_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery

============================================================
11) INSTALL BACKEND AND NGINX SOURCE
============================================================
NGINX_SOURCE_INSTALLED=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
BACKEND_SOURCE_INSTALL=PASS
NGINX_SOURCE_INSTALL=PASS
NGINX_CONFIGURATION_TEST=PASS

============================================================
12) DEPLOY LIVE PAGES FROM CANONICAL SOURCE
============================================================
LIVE_PAGE_DEPLOYMENT=PASS

============================================================
13) RESTART SERVICE AND RELOAD NGINX
============================================================
PASSWORD_RESET_SERVICE_RESTARTED=YES
NGINX_RELOADED=YES

============================================================
14) LOCAL BACKEND POST-DEPLOY VERIFICATION
============================================================
LOCAL_FORGOT_AFTER_HTTP=200
LOCAL_RESET_AFTER_HTTP=400
LOCAL_BACKEND_GATE=PASS

============================================================
15) PUBLIC PAGE VERIFICATION
============================================================
FAIL=PUBLIC_LOGIN_FORGOT_LINK_MISSING

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
NGINX_FILE_RESTORED=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
NGINX_ROLLBACK=COMPLETE
PASSWORD_RESET_BACKEND_ROLLBACK=COMPLETE
LIVE_RECOVERY_PAGES_ROLLBACK=COMPLETE
CANONICAL_SOURCE_ROLLBACK=COMPLETE
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DATA_CHANGED_BY_SCRIPT=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_SOURCE_AND_ROUTE_FIX_V5_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_SOURCE_AND_ROUTE_FIX_V5_20260727_134806.md
