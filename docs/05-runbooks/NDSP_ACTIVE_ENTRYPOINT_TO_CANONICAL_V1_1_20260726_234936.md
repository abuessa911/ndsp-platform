============================================================
NDSP — ACTIVE ENTRYPOINT TO CANONICAL V1.1
MODE=TARGETED_ROUTING_LAYER_MIGRATION_WITH_ROLLBACK
DATE=2026-07-26T23:49:37+02:00
WEBROOT=/var/www/ndsp-my
CANONICAL_TARGET=/portal/command-center/
============================================================

== 0) Explicit confirmation ==
EXPLICIT_CONFIRMATION=YES

== 1) Preconditions and canonical health ==
CANONICAL_HTTP=200
CANONICAL_HEALTH_GATE=PASS

== 2) Discover active login-page references ==

FAILURE_LINE=147
FAILURE_EXIT_CODE=1
FINAL_STATUS=FAILED_AND_ROLLED_BACK
