# NDSP — Final Commercial Launch Precision Gate V1.1

- Date: 2026-07-26T22:26:37+02:00
- Mode: READ_ONLY_FALSE_POSITIVE_CORRECTION
- Scope: Reclassify the 25 findings from V1 by content semantics.

## 1. Canonical route redirects
CRITICAL | 1. Canonical route redirects | command-center redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | markets redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | prices-chart redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | opportunities redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | decision-room redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | portfolio redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | scenarios redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | layers redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | risk redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | completed redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | data-health redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | alerts redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | guide redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | support redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | account redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | plans redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | settings redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | context redirect invalid raw=301 location=https final=200
CRITICAL | 1. Canonical route redirects | trial-expired redirect invalid raw=301 location=https final=200

## 2. Sensitive-path response classification
INFO | 2. Sensitive-path response classification | {"actual_sensitive_content": false, "bytes": 27973, "html": true, "path": "/portal-commercial-preview/.env", "reason": "env_assignments=0 secret=False", "spa_fallback": true}
PASS | 2. Sensitive-path response classification | HTTP 200 is SPA fallback, not sensitive exposure: /portal-commercial-preview/.env
INFO | 2. Sensitive-path response classification | {"actual_sensitive_content": false, "bytes": 27973, "html": true, "path": "/portal-commercial-preview/src/main.jsx", "reason": "jsx_hits=[]", "spa_fallback": true}
PASS | 2. Sensitive-path response classification | HTTP 200 is SPA fallback, not sensitive exposure: /portal-commercial-preview/src/main.jsx
INFO | 2. Sensitive-path response classification | {"actual_sensitive_content": false, "bytes": 27973, "html": true, "path": "/.git/config", "reason": "git_hits=[]", "spa_fallback": true}
PASS | 2. Sensitive-path response classification | HTTP 200 is SPA fallback, not sensitive exposure: /.git/config
INFO | 2. Sensitive-path response classification | {"actual_sensitive_content": false, "bytes": 27973, "html": true, "path": "/backups/", "reason": "listing_hits=[]", "spa_fallback": true}
PASS | 2. Sensitive-path response classification | HTTP 200 is SPA fallback, not sensitive exposure: /backups/

## 3. Source-map content classification
PASS | 3. Source-map content classification | Current JS asset: /portal-commercial-preview/assets/index-BbNOtHX6.js
INFO | 3. Source-map content classification | {"actual_source_map": true, "bytes": 687526, "has_sources_content": true, "is_html": false, "source_count": 10, "valid_json": true}
CRITICAL | 3. Source-map content classification | Real production source map is publicly accessible

## 4. Browser-rendered runtime classification
FAIL | 4. Browser-rendered runtime classification | Chromium execution failed rc=124

## 5. Corrected launch decision
PASS_COUNT=5
WARN_COUNT=0
FAIL_COUNT=21
CRITICAL_FAIL_COUNT=20
COMMERCIAL_LAUNCH_READY=NO
FINAL_STATUS=BLOCKED_BY_CONFIRMED_CRITICAL_FAILURES
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_COMMERCIAL_LAUNCH_PRECISION_GATE_V1_1_20260726_222637.md
JSON_REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_COMMERCIAL_LAUNCH_PRECISION_GATE_V1_1_20260726_222637.json
SOURCE_CHANGED=NO
BACKEND_CHANGED=NO
NGINX_CHANGED=NO
SERVICE_RESTARTED=NO
