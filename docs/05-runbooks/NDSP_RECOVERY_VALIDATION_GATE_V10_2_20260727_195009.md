
============================================================
NDSP — CORRECT RECOVERY VALIDATION GATES AND RUN V10.2
============================================================
DATE=2026-07-27T19:50:10+02:00
V7_ORIGINAL=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7.sh
V10_ORIGINAL=/home/nawaf511/ndsp_prepare_reset_contract_then_run_v7_v10.sh
V7_FIXED=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_1.sh
V10_FIXED=/home/nawaf511/ndsp_prepare_reset_contract_then_run_v7_v10_2.sh
BACKUP=/home/nawaf511/empire-core-new/backups/recovery-validation-gate-v10-2/20260727_195009
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RECOVERY_VALIDATION_GATE_V10_2_20260727_195009.md
PRODUCTION_CHANGE_BY_WRAPPER=NO

============================================================
0) EXPLICIT CONFIRMATION
============================================================
EXPLICIT_CONFIRMATION=YES

============================================================
1) VERIFY ORIGINAL SCRIPT FILES
============================================================
V7_ORIGINAL_SHA256=c68b09d0570d64ea039144094154e12ab24976805e9fffa4117251cf5c7df82d
V10_ORIGINAL_SHA256=ce9287bf91130e679d9f8c147a99e76fa719d23d99f5e6b52f1827b76af3abcd
ORIGINAL_SCRIPT_GATE=PASS

============================================================
2) BUILD CORRECTED V7.1 AND V10.2
============================================================
V7_FIXED_SHA256=6d6bdee37f502068fad53e093712c290e1232cc5630b7548b3a4861953953bdd
V10_FIXED_SHA256=e8672476e63cca7a4ce8731b5c5675dc57fd7fb07d16c05b067439db8cae7206
CORRECTED_SCRIPT_BUILD_GATE=PASS

============================================================
3) RUN CORRECTED V10.2
============================================================

============================================================
NDSP — PREPARE RESET CONTRACT THEN RUN V7 — V10
============================================================
DATE=2026-07-27T19:50:11+02:00
PROJECT=/home/nawaf511/empire-core-new
FORGOT_HTML=/var/www/ndsp-my/forgot-password.html
RECOVERED_RESET=/var/www/html/reset-password.html
RESET_HTML=/var/www/ndsp-my/reset-password.html
CANONICAL_DIR=/home/nawaf511/empire-core-new/frontend/auth-recovery
V7_SCRIPT=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_1.sh
BACKUP=/home/nawaf511/empire-core-new/backups/prepare-reset-contract-v10/20260727_195010
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_195010.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) VERIFY INPUT SOURCES
============================================================
RECOVERED_RESET_SHA256=a4c7e7ecb8dd0e3cca396f042657f8ec51b90fac0a45d6f6b5f85ff28034b90a
V7_SHA256=6d6bdee37f502068fad53e093712c290e1232cc5630b7548b3a4861953953bdd
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
Traceback (most recent call last):
  File "<stdin>", line 46, in <module>
  File "/usr/lib/python3.12/pathlib.py", line 1049, in write_text
    with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/pathlib.py", line 1015, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: '/opt/ndsp-auth-core-clean/releases/20260727_195013-auth-recovery-true-source-fix-v7/ui/src/main.tsx'

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_195013.md

WRAPPER_ROLLBACK_REQUIRED=YES
WRAPPER_ROLLBACK_TRIGGER_EXIT=1
SEEDED_RESET_PAGE_REMOVED=YES
SEEDED_CANONICAL_SOURCE_REMOVED=YES
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_PREPARE_RESET_CONTRACT_V10_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_195010.md
FAIL=V10_2_EXECUTION_FAILED_EXIT_1
