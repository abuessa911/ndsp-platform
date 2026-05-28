# NDSP Current State Summary

Updated: 2026-05-28T09:35:13+02:00

Runtime:
- Public site: https://ndsp.app/
- User portal: https://my.ndsp.app/
- Admin console: https://admin.ndsp.app/
- API namespace: /api
- Backend service: ndsp-api.service
- Backend runtime port: 9001
- PostgreSQL DB: ndsp_auth
- Telegram alerts: enabled

API Namespace:
- API_TOTAL=81
- CANONICAL_COUNT=81
- VERSIONED_TOTAL=0
- NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
- /api/v1 hidden/retired from OpenAPI
- /api/v6 hidden/retired from OpenAPI
- /api/v7 retired and returns 404
- /api/v8 hidden/retired from OpenAPI

Frontend:
- /var/www/ndsp
- /var/www/ndsp-my
- /var/www/ndsp-admin

Security:
- Public secrets: 0
- Legal acknowledgment: active
- Language switch: active

Trial:
- Duration: 16 days
- Seats: 50 total
- Specialist/academic: 10
- Normal beginner: 25
- Premium invite-only: 15

Final readiness:
- FINAL_STATUS=NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_DONE
- Report: /home/nawaf511/ndsp_launch_reports/NDSP_FINAL_READINESS_AFTER_API_UNIFICATION_20260527_171035.md

Latest namespace snapshot:
- /home/nawaf511/ndsp_snapshots/NDSP_AFTER_API_NAMESPACE_UNIFICATION_20260527_170420.tar.gz
- /home/nawaf511/ndsp_snapshots/NDSP_AFTER_API_NAMESPACE_UNIFICATION_20260527_170420.tar.gz.sha256
