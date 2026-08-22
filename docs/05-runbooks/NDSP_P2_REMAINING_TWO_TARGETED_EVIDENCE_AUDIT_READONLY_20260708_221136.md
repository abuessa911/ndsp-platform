# NDSP P2 Remaining Two Targeted Evidence Audit — Read-only
DATE=2026-07-08T22:11:36+02:00
MODE=READ_ONLY_TARGETED_EVIDENCE_AUDIT
TARGETS=ndip-api-new.service,testapp.service
MODIFICATIONS=None
NO_STOP=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_RESTART=1
NO_REBOOT=1
ARTIFACT_DIR=/tmp/NDSP_P2_REMAINING_TWO_EVIDENCE_20260708_221136

## 1) Runtime baseline
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m14%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.115mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.252mb/s[39m [90m/[39m [1m[33m82.08%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Current failed units
  UNIT                 LOAD   ACTIVE SUB    DESCRIPTION
● ndip-api-new.service loaded failed failed NDIP API - New Backend
● testapp.service      loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

2 loaded units listed.
