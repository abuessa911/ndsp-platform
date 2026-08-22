
============================================================
NDSP — AUTH RECOVERY TRUE SOURCE FIX V7
============================================================
DATE=2026-07-27T14:21:40+02:00
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
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-true-source-fix-v7/20260727_142140
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_142140.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
FAIL=SET_NDSP_CONFIRM_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7=YES

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_142140.md
