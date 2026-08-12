
============================================================
NDSP — FORGOT PASSWORD SOURCE ROUTE FIX V1
============================================================
DATE=2026-07-27T12:45:27+02:00
DOMAIN=my.ndsp.app
AUTH_BASE=/opt/ndsp-auth-core-clean
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
AUTH_SERVICE=ndsp-auth-core-clean.service
WEB_ROOT=/var/www/ndsp-my
LIVE_LOGIN=/var/www/ndsp-my/login/index.html
MODE=SOURCE_BUILD_ATOMIC_RELEASE_AND_STATIC_SOURCE_DEPLOY
DATABASE_CHANGE=NO
NGINX_CHANGE=NO
DECISION_BACKEND_CHANGE=NO
BACKUP=/home/nawaf511/empire-core-new/backups/forgot-password-source-route-fix-v1/20260727_124527
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FORGOT_PASSWORD_SOURCE_ROUTE_FIX_V1_20260727_124527.md

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGES
============================================================
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

============================================================
1) REQUIRED COMMANDS AND PATHS
============================================================
ACTIVE_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_103119-legacy-email-delete-source-fix-v1-1
NEW_AUTH_RELEASE=/opt/ndsp-auth-core-clean/releases/20260727_124527-forgot-password-source-route-fix-v1
PRECONDITION_GATE=PASS

============================================================
2) VERIFY CURRENT ROOT CAUSE
============================================================
WRONG_SOURCE_FILE_COUNT=1
WRONG_LIVE_LINK_COUNT=0
ROOT_CAUSE_GATE=PASS
ROOT_CAUSE=FORGOT_PASSWORD_LINK_POINTS_TO_RESET_PASSWORD

============================================================
3) PUBLIC ROUTE PREFLIGHT
============================================================
ROOT_HTTP=302
FORGOT_PASSWORD_HTTP=200
ROOT_PAGE_SHA256=da5060c1890506c6a1b9b1b261867b4de19bcd3a96f08ccc01b3e09ea1a88211
FORGOT_PAGE_SHA256=8d318982941d7249b35994c3456adb44f5a1e2f975ffdabaf81f0608ea5f34e2
FAIL=FORGOT_PASSWORD_ROUTE_CONTAINS_PORTAL_SHELL

ROLLBACK_REQUIRED=YES
ROLLBACK_TRIGGER_EXIT=1
FINAL_STATUS=NDSP_FORGOT_PASSWORD_SOURCE_ROUTE_FIX_V1_FAILED
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FORGOT_PASSWORD_SOURCE_ROUTE_FIX_V1_20260727_124527.md
