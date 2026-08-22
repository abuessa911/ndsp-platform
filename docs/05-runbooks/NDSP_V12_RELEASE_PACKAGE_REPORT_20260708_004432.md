# NDSP V1.2 Release Package Report
DATE=2026-07-08T00:44:32+02:00
MODE=RELEASE_PACKAGE_CREATE
MODIFICATIONS=Package files only; no runtime changes
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz

## 1) Required Reports
[OK] docs/05-runbooks/NDSP_V12_PATCH_SCENARIO_LEVELS_CONTRACT_REMOTE_ONLY_20260708_003202.md
[OK] docs/05-runbooks/NDSP_V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_20260708_003607.md
[OK] docs/05-runbooks/NDSP_V12_FINAL_ACCEPTANCE_AUDIT_20260708_004202.md
[OK] docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md

## 2) Create Manifest
[OK] Manifest created: /tmp/NDSP_V12_RELEASE_MANIFEST_20260708_004432.txt

## 3) Create Package
[OK] Package created

## 4) SHA256
bb84349c8fa0c5c43c7345aa1608a1167cb48aeddb0abbd14fef5535b43e5eb3  /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz

## 5) Package Listing
tmp/NDSP_V12_RELEASE_MANIFEST_20260708_004432.txt
docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md
docs/05-runbooks/NDSP_V12_PATCH_SCENARIO_LEVELS_CONTRACT_REMOTE_ONLY_20260708_003202.md
docs/05-runbooks/NDSP_V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_20260708_003607.md
docs/05-runbooks/NDSP_V12_FINAL_ACCEPTANCE_AUDIT_20260708_004202.md
backend/app/runtime/ndsp_quality_live_nmp_wrapper.py

## 6) Runtime Safety
ndsp-quality-live-nmp-wrapper=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.4%[39m | [1mram usage[22m: [32m9.7%[39m | [1mlo[22m: ⇓ [32m0.001mb/s[39m ⇑ [32m0.001mb/s[39m | [1meth0[22m: ⇓ [32m0.078mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.224mb/s[39m [90m/[39m [1m[33m81.98%[39m[22m |

PACKAGE_PATH=/home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz
SHA256_PATH=/home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz.sha256
FINAL_STATUS=V12_RELEASE_PACKAGE_CREATED
REPORT=docs/05-runbooks/NDSP_V12_RELEASE_PACKAGE_REPORT_20260708_004432.md
