
============================================================
NDSP — RESET PASSWORD SOURCE SEED V8
============================================================
DATE=2026-07-27T14:34:46+02:00
HOST=vmi2934783.contaboserver.net
PROJECT=/home/nawaf511/empire-core-new
RECOVERED_SOURCE=/var/www/html/reset-password.html
CANONICAL_RECOVERY=/home/nawaf511/empire-core-new/frontend/auth-recovery
LIVE_RESET=/var/www/ndsp-my/reset-password.html
V7_SCRIPT=/home/nawaf511/ndsp_auth_recovery_true_source_fix_v7.sh
BACKUP=/home/nawaf511/empire-core-new/backups/reset-password-source-seed-v8/20260727_143446
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RESET_PASSWORD_SOURCE_SEED_V8_20260727_143446.md

============================================================
0) PRIVILEGES AND REQUIRED COMMANDS
============================================================
SUDO_GATE=PASS
COMMAND_GATE=PASS

============================================================
1) VERIFY RECOVERED RESET SOURCE
============================================================
FAIL=RECOVERED_SOURCE_RESET_API_CONTRACT_MISSING

WRAPPER_ROLLBACK_REQUIRED=YES
WRAPPER_ROLLBACK_TRIGGER_EXIT=1
DATABASE_CHANGED=NO
FINAL_STATUS=NDSP_RESET_PASSWORD_SOURCE_SEED_V8_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_RESET_PASSWORD_SOURCE_SEED_V8_20260727_143446.md
