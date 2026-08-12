# NDSP P2 Hold-Review Decision Matrix — Read-only
DATE=2026-07-08T21:52:12+02:00
MODE=READ_ONLY_DECISION_MATRIX
MODIFICATIONS=None
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_RESTART=1
NO_REBOOT=1

LATEST_DEEP_AUDIT_FOUND=1
LATEST_DEEP_AUDIT=docs/05-runbooks/NDSP_P2_HOLD_REVIEW_SERVICES_DEEP_AUDIT_READONLY_20260708_065452.md

## 1) Critical runtime baseline
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.8%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.003mb/s[39m | [1meth0[22m: ⇓ [32m0.001mb/s[39m ⇑ 0mb/s | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.211mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Latest deep-audit summary excerpt
44:---- SERVICE=ndip-api-new.service ----
203:PATHS_MISSING_COUNT=0
208:PROJECT_REFS_COUNT=2
211:NGINX_REFS_COUNT=0
267:PRELIMINARY_DECISION=REVIEW_IMPORT_PATH_OR_LEGACY_BACKEND
269:---- SERVICE=signal-engine.service ----
341:PATHS_MISSING_COUNT=3
344:PROJECT_REFS_COUNT=0
347:NGINX_REFS_COUNT=0
403:PRELIMINARY_DECISION=LIKELY_LEGACY_EXEC_PATH_MISSING_REVIEW_BEFORE_DISABLE
405:---- SERVICE=subscription-watcher.service ----
477:PATHS_MISSING_COUNT=1
480:PROJECT_REFS_COUNT=0
483:NGINX_REFS_COUNT=0
540:PRELIMINARY_DECISION=LIKELY_LEGACY_MISSING_FILE_REVIEW_BEFORE_DISABLE
542:---- SERVICE=testapp.service ----
614:PATHS_MISSING_COUNT=2
645:PROJECT_REFS_COUNT=28
648:NGINX_REFS_COUNT=0
704:PRELIMINARY_DECISION=HAS_PROJECT_REFS_DEEP_REVIEW_REQUIRED
728:FINAL_STATUS=P2_HOLD_REVIEW_SERVICES_DEEP_AUDIT_READONLY_DONE

## 3) Decision matrix
service                       enabled   active  failed  project_refs  nginx_refs  path_missing_hint  journal_hint  recommendation
ndip-api-new.service          disabled  failed  failed  UNKNOWN       UNKNOWN     UNKNOWN            NONE          KEEP_REVIEW
signal-engine.service         enabled   failed  failed  0             0           3                  NONE          KEEP_REVIEW
subscription-watcher.service  enabled   failed  failed  0             0           1                  NONE          KEEP_REVIEW
testapp.service               enabled   failed  failed  28            0           2                  NONE          DO_NOT_DISABLE_UNTIL_PROJECT_REFS_REVIEWED

## 4) Recommended next action
NEXT_ACTION=Send this report output before any patch.
RULE=No disable/fix for hold-review services until this matrix is reviewed.
PATCH_MODE_REQUIRED=YES

## 5) Runtime safety after matrix
nginx=active
pm2-nawaf511=active
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

FINAL_STATUS=P2_HOLD_REVIEW_DECISION_MATRIX_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_HOLD_REVIEW_DECISION_MATRIX_READONLY_20260708_215212.md
