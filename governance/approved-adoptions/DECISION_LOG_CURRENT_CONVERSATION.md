# NDSP Decision Log — Current Conversation

Approved decisions:
1. /api is the only approved API namespace.
2. /api/v7 is retired and must return 404.
3. PostgreSQL runtime database is ndsp_auth only.
4. Env files are centralized in /etc/ndsp.
5. Telegram auto alert timer is enabled.
6. Published frontend paths are /var/www/ndsp, /var/www/ndsp-my, and /var/www/ndsp-admin.
7. Old /var/www paths are quarantined instead of deleted.
8. Legal/trial acknowledgment appears before entry.
9. Arabic/English switch is approved inside the acknowledgment modal.
10. Current gold snapshot is NDSP_FIX_OLD_DB_SCRIPTS_ENV_CANONICAL_20260526_210427.

## API Namespace Finalization — 20260527_171503

Approved:
- /api is the only public OpenAPI namespace.
- /api/v1, /api/v6, /api/v7, and /api/v8 must not appear in public OpenAPI.
- Versioned runtime routes, if any remain, are compatibility-only and hidden.
- Frontend legacy API references count is zero.
- Final readiness passed after API unification.

Evidence:
- API final report: /home/nawaf511/ndsp_launch_reports/NDSP_FINALIZE_API_NAMESPACE_UNIFICATION_20260527_170355.md
- Readiness report: /home/nawaf511/ndsp_launch_reports/NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_20260527_171035.md
- Snapshot report: /home/nawaf511/ndsp_launch_reports/NDSP_SNAPSHOT_AFTER_API_NAMESPACE_UNIFICATION_20260527_170420.md

Assertions:
- API_TOTAL=81
- CANONICAL_COUNT=81
- VERSIONED_TOTAL=0
- NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
- PUBLIC_SECRET_HITS=0
- FINAL_STATUS=NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_DONE

## API Namespace Finalization — 20260528_093513

Approved:
- /api is the only public OpenAPI namespace.
- /api/v1, /api/v6, /api/v7, and /api/v8 must not appear in public OpenAPI.
- Versioned runtime routes, if any remain, are compatibility-only and hidden.
- Frontend legacy API references count is zero.
- Final readiness passed after API unification.

Evidence:
- API final report: /home/nawaf511/ndsp_launch_reports/NDSP_FINALIZE_API_NAMESPACE_UNIFICATION_20260527_170355.md
- Readiness report: /home/nawaf511/ndsp_launch_reports/NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_20260527_171035.md
- Snapshot report: /home/nawaf511/ndsp_launch_reports/NDSP_SNAPSHOT_AFTER_API_NAMESPACE_UNIFICATION_20260527_170420.md

Assertions:
- API_TOTAL=81
- CANONICAL_COUNT=81
- VERSIONED_TOTAL=0
- NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
- PUBLIC_SECRET_HITS=0
- FINAL_STATUS=NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_DONE
