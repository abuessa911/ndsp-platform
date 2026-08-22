# NDSP V1.2 Final Acceptance Audit
DATE=2026-07-08T00:42:02+02:00
MODE=READ_ONLY_FINAL_ACCEPTANCE
MODIFICATIONS=None

## 1) Reality Lock Markers
2249:## V1.2 Scenario Levels Contract Patch Lock — 20260708_003202
2253:- V12_PATCH_SCENARIO_LEVELS_CONTRACT_STATUS=OK
2279:## V1.2 Frontend Display Verification Read-only Lock — 2026-07-08
2283:- V12_FRONTEND_DISPLAY_VERIFICATION_STATUS=DONE

## 2) Public API Contract
ETHUSDT: SCENARIO_LEVELS=OK | V1_FLAT_FIELDS=OK
BTCUSDT: SCENARIO_LEVELS=OK | V1_FLAT_FIELDS=OK
XAUUSD: SCENARIO_LEVELS=OK | V1_FLAT_FIELDS=OK
USOIL: SCENARIO_LEVELS=OK | V1_FLAT_FIELDS=OK
PUBLIC_API_CONTRACT_STATUS=OK

## 3) Public Pages
/index.html HTTP_CODE=200
/decision-support.html HTTP_CODE=200
/NDSP_Asset_View.html HTTP_CODE=200
/NDSP_Command_Center.html HTTP_CODE=200
/NDSP_Daily_Brief.html HTTP_CODE=200
/NDSP_Settings_Alerts.html HTTP_CODE=200
/disclaimer.html HTTP_CODE=200

## 4) Services
ndsp-quality-live-nmp-wrapper=active
{"ok":true,"service":"ndsp-quality-live-nmp-wrapper","port":9082,"upstream":"http://127.0.0.1:9067","updated_at":"2026-07-07T22:42:08+00:00"}

## 5) PM2
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9%[39m | [1mram usage[22m: [32m9.9%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.174mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.152mb/s[39m [90m/[39m [1m[33m81.98%[39m[22m |

## 6) Final Evaluation
FINAL_STATUS=V12_FINAL_ACCEPTANCE_AUDIT_DONE
REPORT=docs/05-runbooks/NDSP_V12_FINAL_ACCEPTANCE_AUDIT_20260708_004202.md
