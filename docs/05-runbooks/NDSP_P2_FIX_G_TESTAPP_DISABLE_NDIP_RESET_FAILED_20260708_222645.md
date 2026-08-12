# NDSP P2 Fix G — testapp Disable + ndip reset-failed
DATE=2026-07-08T22:26:45+02:00
MODE=CONTROLLED_TESTAPP_DISABLE_NDIP_RESET_FAILED
MODIFICATION=Disable testapp.service and reset failed state for ndip-api-new.service
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
NO_DELETE=1
NO_MASK=1
NO_REBOOT=1
NO_SERVICE_START=1
NO_RESTART=1
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645

LATEST_D3_AUDIT=docs/05-runbooks/NDSP_P2_REMAINING_TWO_D3_STRICT_SEPARATION_AUDIT_READONLY_20260708_222216.md

## 1) Runtime safety before change
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m15.4%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.115mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.163mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 2) Pre-check services

---- SERVICE=ndip-api-new.service ----
ENABLED_BEFORE=disabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
FRAGMENT=/etc/systemd/system/ndip-api-new.service
RESULT=exit-code
EXEC_MAIN_STATUS=1
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645/ndip-api-new.service.unit.before

---- SERVICE=testapp.service ----
ENABLED_BEFORE=enabled
ACTIVE_BEFORE=failed
FAILED_BEFORE=failed
FRAGMENT=/etc/systemd/system/testapp.service
RESULT=exit-code
EXEC_MAIN_STATUS=203
BACKUP_UNIT=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645/testapp.service.unit.before

## 3) Validate D3 evidence
D3_TESTAPP_DISABLE_EVIDENCE=OK
D3_NDIP_RESET_FAILED_ONLY_EVIDENCE=OK

## 4) Apply controlled changes
ACTION=testapp.service disable + reset-failed
Removed "/etc/systemd/system/multi-user.target.wants/testapp.service".
ACTION=ndip-api-new.service reset-failed only

## 5) Post-check services
ndip-api-new.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive
testapp.service ENABLED_AFTER=disabled ACTIVE_AFTER=inactive FAILED_AFTER=inactive

## 6) Failed units after Fix G
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_AFTER=0

## 7) Runtime safety after change
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 3D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m15.4%[39m | [1mram usage[22m: [32m10.3%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.115mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.163mb/s[39m [90m/[39m [1m[33m82.06%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200

## 8) Final Evaluation
TESTAPP_ENABLED_FINAL=disabled
TESTAPP_FAILED_FINAL=inactive
NDIP_ENABLED_FINAL=disabled
NDIP_FAILED_FINAL=inactive
NGINX_ACTIVE_FINAL=active
PM2_ACTIVE_FINAL=active
API_HTTP_FINAL=200
QUALITY_LIVE_HTTP_FINAL=200
MY_NDSP_HTTP_FINAL=200
P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_STATUS=OK
FINAL_STATUS=P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_OK
REALITY_LOCK_STATUS=UPDATED
REPORT=docs/05-runbooks/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645.md
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645
