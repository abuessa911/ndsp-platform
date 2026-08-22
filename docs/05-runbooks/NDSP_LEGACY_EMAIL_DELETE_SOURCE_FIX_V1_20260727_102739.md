============================================================
NDSP — LEGACY MALFORMED EMAIL DELETE SOURCE FIX V1
DATE=2026-07-27T10:27:39+02:00
MODE=SOURCE_ONLY_SERVER_BUILD_ATOMIC_AUTH_RELEASE
AUTH_CURRENT=/opt/ndsp-auth-core-clean/current
AUTH_SERVICE=ndsp-auth-core-clean
============================================================

== 0) Explicit confirmation and privileges ==
EXPLICIT_CONFIRMATION=YES
SUDO_GATE=PASS

== 1) Preconditions ==
PRECONDITION_GATE=PASS
AUTH_OLD_TARGET=/opt/ndsp-auth-core-clean/releases/20260727_100613-integrated-auth-controls-v2
AUTH_NODE_MODULES=/opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules

== 2) Read-only database verification ==
ERROR_EXIT=1
ERROR_LINE=113

ROLLBACK_BEGIN=YES
ROLLBACK_COMPLETE=YES
FINAL_STATUS=FAILED_AND_ROLLED_BACK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_LEGACY_EMAIL_DELETE_SOURCE_FIX_V1_20260727_102739.md
ERROR_EXIT=1
ERROR_LINE=113

ROLLBACK_BEGIN=YES
ROLLBACK_COMPLETE=YES
FINAL_STATUS=FAILED_AND_ROLLED_BACK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_LEGACY_EMAIL_DELETE_SOURCE_FIX_V1_20260727_102739.md
