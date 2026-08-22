============================================================
NDSP — RETIRE PORTAL V50 V1
MODE=REMOVE_LEGACY_PUBLIC_PORTAL_AND_REDIRECT_TO_CANONICAL
DATE=2026-07-27T00:03:18+02:00
LEGACY=/var/www/ndsp-my/portal-v50
CANONICAL_TARGET=/portal/command-center/
============================================================

== 0) Explicit destructive confirmation ==
EXPLICIT_CONFIRMATION=YES

== 1) Preconditions ==
CANONICAL_HTTP=200
LEGACY_BEFORE_HTTP=200
PRECONDITION_GATE=PASS

== 2) Discover and classify active references ==
REFERENCE_DISCOVERY_GATE=PASS

== 3) Backup legacy portal, Nginx, and active routing files ==
eaa5c3b162f14765360094020611113fa1e7975662c35180dc3cdb7aca67853d  /home/nawaf511/empire-core-new/backups/retire-portal-v50-v1/20260727_000318/portal-v50.tar.gz
BACKUP=/home/nawaf511/empire-core-new/backups/retire-portal-v50-v1/20260727_000318
BACKUP_GATE=PASS

== 4) Migrate login bridge and active navigation ==
REDIRECT_STUB=/var/www/ndsp-my/completed-decisions-review.html TARGET=/portal/completed/
REDIRECT_STUB=/var/www/ndsp-my/asset-selector.html TARGET=/portal/markets/
REDIRECT_STUB=/var/www/ndsp-my/my-watchlist.html TARGET=/portal/portfolio/
REDIRECT_STUB=/var/www/ndsp-my/decision-room.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/data-freshness.html TARGET=/portal/data-health/
REDIRECT_STUB=/var/www/ndsp-my/risk-governance.html TARGET=/portal/risk/
REDIRECT_STUB=/var/www/ndsp-my/portal.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-guide.html TARGET=/portal/guide/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v30-1/index.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/decision-room-v30/index.html TARGET=/portal/decision-room/
REDIRECT_STUB=/var/www/ndsp-my/user-portal/index.html TARGET=/portal/command-center/
REDIRECT_STUB=/var/www/ndsp-my/decision-room/index.html TARGET=/portal/decision-room/
NAVIGATION_PATCHED=/var/www/ndsp-my/telegram-alerts/index.html OCCURRENCES=1
NAVIGATION_PATCHED=/var/www/ndsp-my/admin/index.html OCCURRENCES=3
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/decision-radar.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/nmp.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/market-assets.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/platform.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/command-center.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/data-health.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/ndsp-canonical-user-portal-v86.js OCCURRENCES=1
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/decision-center.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/scenario-levels.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/ndsp-canonical-user-portal-v79.js OCCURRENCES=1
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/markets.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/NDSP_Command_Center.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/governance.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/completed-decisions.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/radar.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/ndsp-canonical-user-portal-v78.js OCCURRENCES=1
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/dashboard.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/decision-support.html OCCURRENCES=6
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/analysis-center.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/access/index.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/decision-room-v31/index.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/owner/index.html OCCURRENCES=3
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/login/index.html OCCURRENCES=1
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/assets/ndsp-login-v1.js OCCURRENCES=1
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/dashboard/index.html OCCURRENCES=2
GENERIC_LEGACY_REFERENCE_CLOSED=/var/www/ndsp-my/decision-room-v31/account/index.html OCCURRENCES=2
REDIRECT_STUB_COUNT=12
NAVIGATION_REFERENCE_COUNT=4
GENERIC_LEGACY_FILE_COUNT=26
GENERIC_LEGACY_REFERENCE_COUNT=52
LOGIN_CACHE_BUST_FILE_COUNT=0
LOGIN_CACHE_BUST_REFERENCE_COUNT=0
ACTIVE_ROUTING_MIGRATION_GATE=PASS

== 5) Retire portal-v50 in Nginx configuration ==
REMOVED_PORTAL_V50_LOCATION_BLOCKS=3
PATCHED_MY_NDSP_APP_SERVER_BLOCKS=2
NGINX_PORTAL_V50_RETIREMENT_GATE=PASS

== 6) Remove legacy portal directory from public webroot ==
LEGACY_PUBLIC_DIRECTORY_REMOVED=YES
LEGACY_ARCHIVE_RETAINED_OUTSIDE_WEBROOT=/home/nawaf511/empire-core-new/backups/retire-portal-v50-v1/20260727_000318/portal-v50.tar.gz

== 7) Validate and reload Nginx ==
NGINX_CONFIG_GATE=PASS
NGINX_RELOADED=YES

== 8) Public retirement verification ==
LEGACY_RAW_HTTP=200
LEGACY_LOCATION=
LEGACY_FINAL_HTTP=200

FAILURE_LINE=774
FAILURE_EXIT_CODE=1
ROLLBACK=STARTED
ROLLBACK_LEGACY_DIRECTORY=RESTORED
ROLLBACK_NGINX_RELOAD=ATTEMPTED
ROLLBACK=RESTORED
FINAL_STATUS=FAILED_AND_ROLLBACK_ATTEMPTED
