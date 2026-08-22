
============================================================
NDSP — AUTH RECOVERY TRUE SOURCE FIX V7
============================================================
DATE=2026-07-27T19:50:13+02:00
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
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-true-source-fix-v7/20260727_195013
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_195013.md

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
NEW_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_195013-auth-recovery-true-source-fix-v7
NEW_AUTH_RELEASE_COPY_GATE=PASS

============================================================
5) FIX LOGIN LINK IN TRUE SOURCE
============================================================

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_195013.md
