============================================================
NDSP — PORTAL V50 HARD RETIRE V2
MODE=DELETE_LEGACY_APP_KEEP_REDIRECT_STUB_NO_NGINX_CHANGE
DATE=2026-07-27T00:08:36+02:00
LEGACY=/var/www/ndsp-my/portal-v50
CANONICAL_TARGET=/portal/command-center/
============================================================

== 0) Explicit destructive confirmation ==
EXPLICIT_CONFIRMATION=YES

== 1) Preconditions and canonical health ==
CANONICAL_HTTP=200
LEGACY_BEFORE_HTTP=200
PRECONDITION_GATE=PASS

== 2) Discover active legacy references ==
ACTIVE_REFERENCE_FILE_COUNT=41
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/NDSP_Command_Center.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/access/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/admin/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/analysis-center.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/asset-selector.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/assets/ndsp-login-v1.js
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/command-center.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/completed-decisions-review.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/completed-decisions.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/dashboard.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/dashboard/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/data-freshness.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/data-health.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-center.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-guide.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-radar.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room-v30-1/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room-v30/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room-v31/account/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room-v31/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-room/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/decision-support.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/governance.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/login/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/market-assets.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/markets.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/my-watchlist.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/ndsp-canonical-user-portal-v78.js
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/ndsp-canonical-user-portal-v79.js
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/ndsp-canonical-user-portal-v86.js
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/ndsp-login-to-portal-v90.js
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/nmp.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/owner/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/platform.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/portal.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/radar.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/risk-governance.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/scenario-levels.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/telegram-alerts/index.html
ACTIVE_REFERENCE_FILE=/var/www/ndsp-my/user-portal/index.html
REFERENCE_DISCOVERY_GATE=PASS

== 3) Backup old app and exact active files ==
eaa5c3b162f14765360094020611113fa1e7975662c35180dc3cdb7aca67853d  /home/nawaf511/empire-core-new/backups/portal-v50-hard-retire-v2/20260727_000836/portal-v50.tar.gz
BACKUP=/home/nawaf511/empire-core-new/backups/portal-v50-hard-retire-v2/20260727_000836
BACKUP_GATE=PASS

== 4) Replace all active legacy targets with canonical routes ==
REDIRECT_STUB=/var/www/ndsp-my/completed-decisions-review.html TARGET=/portal/completed/
REDIRECT_STUB=/var/www/ndsp-my/asset-selector.html TARGET=/portal/markets/
REFERENCE_PATCHED=/var/www/ndsp-my/ndsp-login-to-portal-v90.js OCCURRENCES=3
REDIRECT_STUB=/var/www/ndsp-my/my-watchlist.html TARGET=/portal/portfolio/
REDIRECT_STUB=/var/www/ndsp-my/decision-room.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/data-freshness.html TARGET=/portal/data-health/
REDIRECT_STUB=/var/www/ndsp-my/risk-governance.html TARGET=/portal/risk/
REDIRECT_STUB=/var/www/ndsp-my/portal.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-guide.html TARGET=/portal/guide/
REDIRECT_STUB=/var/www/ndsp-my/decision-radar.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/nmp.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/market-assets.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/platform.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/command-center.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/data-health.html TARGET=/portal/command-center/
REFERENCE_PATCHED=/var/www/ndsp-my/ndsp-canonical-user-portal-v86.js OCCURRENCES=1
REDIRECT_STUB=/var/www/ndsp-my/decision-center.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/scenario-levels.html TARGET=/portal/command-center/
REFERENCE_PATCHED=/var/www/ndsp-my/ndsp-canonical-user-portal-v79.js OCCURRENCES=1
REDIRECT_STUB=/var/www/ndsp-my/markets.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/NDSP_Command_Center.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/governance.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/completed-decisions.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/radar.html TARGET=/portal/command-center/
REFERENCE_PATCHED=/var/www/ndsp-my/ndsp-canonical-user-portal-v78.js OCCURRENCES=1
REDIRECT_STUB=/var/www/ndsp-my/dashboard.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-support.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/analysis-center.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v30-1/index.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v30/index.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/user-portal/index.html TARGET=/portal/command-center/
REFERENCE_PATCHED=/var/www/ndsp-my/telegram-alerts/index.html OCCURRENCES=1
REFERENCE_PATCHED=/var/www/ndsp-my/admin/index.html OCCURRENCES=3
REDIRECT_STUB=/var/www/ndsp-my/decision-room/index.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/access/index.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v31/index.html TARGET=/portal/command-center/
REFERENCE_PATCHED=/var/www/ndsp-my/owner/index.html OCCURRENCES=3
REFERENCE_PATCHED=/var/www/ndsp-my/login/index.html OCCURRENCES=1
REFERENCE_PATCHED=/var/www/ndsp-my/assets/ndsp-login-v1.js OCCURRENCES=1
REDIRECT_STUB=/var/www/ndsp-my/dashboard/index.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v31/account/index.html TARGET=/portal/command-center/
PATCHED_ACTIVE_FILE_COUNT=41
PATCHED_LEGACY_REFERENCE_COUNT=85
REDIRECT_STUB_COUNT=32
LOGIN_CACHE_BUST_REFERENCE_COUNT=0
ACTIVE_ROUTING_PATCH_GATE=PASS

== 5) Delete the old app and leave only a redirect shell ==
LEGACY_REMAINING_FILE_COUNT=1
LEGACY_REMAINING_SUBDIRECTORY_COUNT=0
LEGACY_APPLICATION_FILES_DELETED=YES
REDIRECT_SHELL_ONLY=YES

== 6) Static closure gate ==
ACTIVE_LEGACY_REFERENCE_COUNT=0
STATIC_REFERENCE_CLOSURE_GATE=PASS

== 7) Public legacy retirement verification ==
PUBLIC_LEGACY_HTTP=200
OLD_PATH_HTTP=200 PATH=markets/

FAILURE_LINE=743
FAILURE_EXIT_CODE=1
ROLLBACK=STARTED
ROLLBACK_LEGACY_APP=RESTORED
ROLLBACK_ROUTING_FILES=RESTORED
ROLLBACK=COMPLETE
FINAL_STATUS=FAILED_AND_ROLLED_BACK
