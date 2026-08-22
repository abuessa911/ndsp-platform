
============================================================
NDSP — AUTH RECOVERY CANONICAL SOURCE FIX V3
============================================================
DATE=2026-07-27T13:32:52+02:00
DOMAIN=my.ndsp.app
PROJECT=/home/nawaf511/empire-core-new
RESET_PACKAGE=/home/nawaf511/empire-core-new/backend/password_reset_gateway
RESET_SERVICE=ndsp-password-reset.service
CANONICAL_SOURCE=/home/nawaf511/empire-core-new/frontend/auth-recovery
WEB_ROOT=/var/www/ndsp-my
MODE=CANONICAL_SOURCE_ATOMIC_STATIC_DEPLOY
DATABASE_CHANGE=NO
NGINX_CHANGE=NO
BACKEND_CHANGE=NO
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-source-fix-v3/20260727_133252
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_SOURCE_FIX_V3_20260727_133252.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) COMMANDS AND REAL SERVICE BINDING
============================================================
SERVICE_WORKING_DIRECTORY=/home/nawaf511/empire-core-new/backend/password_reset_gateway
SERVICE_EXEC_START={ path=/usr/bin/node ; argv[]=/usr/bin/node /home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
REAL_PASSWORD_RESET_SERVICE_GATE=PASS
RESET_PASSWORD_FIELD=newPassword

============================================================
2) VERIFY EXISTING PUBLIC BACKEND ROUTES
============================================================
FORGOT_API_HTTP=404
FAIL=FORGOT_PASSWORD_PUBLIC_API_ROUTE_MISSING_HTTP_404

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
-- No entries --
DATABASE_CHANGED=NO
NGINX_CHANGED=NO
PASSWORD_RESET_BACKEND_CHANGED=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_SOURCE_FIX_V3_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_SOURCE_FIX_V3_20260727_133252.md
