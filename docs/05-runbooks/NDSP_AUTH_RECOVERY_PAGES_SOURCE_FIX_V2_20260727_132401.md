
============================================================
NDSP — AUTH RECOVERY PAGES SOURCE FIX V2
============================================================
DATE=2026-07-27T13:24:02+02:00
DOMAIN=my.ndsp.app
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
AUTH_SERVICE=ndsp-auth-core-clean.service
WEB_ROOT=/var/www/ndsp-my
MODE=CANONICAL_STATIC_SOURCE_ATOMIC_RELEASE
DATABASE_CHANGE=NO
NGINX_CHANGE=NO
DECISION_BACKEND_CHANGE=NO
RUNTIME_DOM_PATCH=NO
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-pages-source-fix-v2/20260727_132401
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_PAGES_SOURCE_FIX_V2_20260727_132401.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) REQUIRED COMMANDS AND PRECONDITIONS
============================================================
OLD_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1
NEW_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_132401-auth-recovery-pages-source-fix-v2
PRECONDITION_GATE=PASS

============================================================
2) VERIFY BACKEND RECOVERY CONTRACTS
============================================================
FAIL=FORGOT_PASSWORD_API_NOT_FOUND_IN_AUTH_SOURCE

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_CHANGED=NO
NGINX_CHANGED=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_PAGES_SOURCE_FIX_V2_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_PAGES_SOURCE_FIX_V2_20260727_132401.md
