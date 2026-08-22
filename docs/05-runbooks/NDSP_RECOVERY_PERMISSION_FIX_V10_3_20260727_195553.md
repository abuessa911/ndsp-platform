
============================================================
NDSP — RECOVERY RELEASE PERMISSION FIX V10.3
============================================================
DATE=2026-07-27T19:55:53+02:00
PROJECT=/home/nawaf511/empire-core-new
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
V7_1=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_1.sh
V10_2=/home/nawaf511/ndsp_prepare_reset_contract_then_run_v7_v10_2.sh
V7_2=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_2.sh
V10_3=/home/nawaf511/ndsp_prepare_reset_contract_then_run_v7_v10_3.sh
BACKUP=/home/nawaf511/empire-core-new/backups/recovery-permission-fix-v10-3/20260727_195553
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RECOVERY_PERMISSION_FIX_V10_3_20260727_195553.md
DIRECT_DATABASE_EDIT=NO
DIRECT_UI_DIST_EDIT=NO

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) VERIFY GENERATED V7.1 AND V10.2
============================================================
V7_1_SHA256=6d6bdee37f502068fad53e093712c290e1232cc5630b7548b3a4861953953bdd
V10_2_SHA256=e8672476e63cca7a4ce8731b5c5675dc57fd7fb07d16c05b067439db8cae7206
GENERATED_SCRIPT_INPUT_GATE=PASS

============================================================
2) BUILD V7.2 WITH ROOT-OWNED RELEASE WRITE FIX
============================================================
V7_2_SHA256=3a3d69f86ac5248feeeeaee9fc7075b7e6add0c3823bca29647cd51e7ef44d5d
ROOT_OWNED_RELEASE_WRITE_FIX=PASS
INCOMPLETE_RELEASE_ROLLBACK_FIX=PASS

============================================================
3) BUILD V10.3 BOUND TO V7.2
============================================================
V10_3_SHA256=94e99b2ec69a03262c53d358a1c94c5389e872565dd9b51cc82bcb883fc03d89
V10_3_TO_V7_2_BINDING=PASS
CORRECTED_SCRIPT_BUILD_GATE=PASS

============================================================
4) CLEAN ONLY THE KNOWN INCOMPLETE RELEASE FROM LAST FAILURE
============================================================
ACTIVE_RELEASE_BEFORE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1
KNOWN_INCOMPLETE_RELEASE_REMOVED=/opt/ndsp-auth-core-clean/releases/20260727_195013-auth-recovery-true-source-fix-v7
INCOMPLETE_RELEASE_CLEANUP_GATE=PASS

============================================================
5) RUN V10.3
============================================================

============================================================
NDSP — PREPARE RESET CONTRACT THEN RUN V7 — V10
============================================================
DATE=2026-07-27T19:55:56+02:00
PROJECT=/home/nawaf511/empire-core-new
FORGOT_HTML=/var/www/ndsp-my/forgot-password.html
RECOVERED_RESET=/var/www/html/reset-password.html
RESET_HTML=/var/www/ndsp-my/reset-password.html
CANONICAL_DIR=/home/nawaf511/empire-core-new/frontend/auth-recovery
V7_SCRIPT=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7_2.sh
BACKUP=/home/nawaf511/empire-core-new/backups/prepare-reset-contract-v10/20260727_195556
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_195556.md

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
DATE=2026-07-27T19:55:58+02:00
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
BACKUP=/home/nawaf511/empire-core-new/backups/auth-recovery-true-source-fix-v7/20260727_195558
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_195558.md

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
NEW_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_195558-auth-recovery-true-source-fix-v7
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

sh: 1: tsc: Permission denied

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=127
INCOMPLETE_AUTH_RELEASE_REMOVED=/opt/ndsp-auth-core-clean/releases/20260727_195558-auth-recovery-true-source-fix-v7
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_20260727_195558.md

WRAPPER_ROLLBACK_REQUIRED=YES
WRAPPER_ROLLBACK_TRIGGER_EXIT=127
SEEDED_RESET_PAGE_REMOVED=YES
SEEDED_CANONICAL_SOURCE_REMOVED=YES
DATABASE_SCHEMA_CHANGED=NO
DATABASE_DIRECT_EDIT=NO
FINAL_STATUS=NDSP_PREPARE_RESET_CONTRACT_V10_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_20260727_195556.md
FAIL=V10_3_EXECUTION_FAILED_EXIT_127
