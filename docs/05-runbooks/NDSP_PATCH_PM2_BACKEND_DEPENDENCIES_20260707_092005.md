# NDSP Patch — PM2 Backend Dependencies Fix
DATE=2026-07-07T09:20:05+02:00
PATCH_BACKUP=/home/nawaf511/ndsp_backups/NDSP_PM2_BACKEND_DEPS_FIX_20260707_092005

## 1) Pre-check
Current directory: /home/nawaf511/empire-core-new

## 2) Backup package files
[INFO] Backing up backend/node_modules listing

## 3) Node/npm versions
v22.22.2
10.9.8

## 4) Dependency state before
ndsp-auth-api@1.0.0 /home/nawaf511/empire-core-new/backend
└── (empty)


## 5) Install backend dependencies safely

added 43 packages, removed 17 packages, and changed 7 packages in 3s

## 6) Dependency state after
ndsp-auth-api@1.0.0 /home/nawaf511/empire-core-new/backend
└── otplib@13.4.1


## 7) Restart only PM2 ndsp-backend
[PM2] Applying action restartProcessId on app [ndsp-backend](ids: [ 1 ])
[PM2] [ndsp-backend](1) ✓
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2688760  │ 0s     │ 372… │ online    │ 0%       │ 26.4mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 23.4% | ram usage: 9.4% | lo: ⇓ 0.002mb/s ⇑ 0.002mb/s | eth0: ⇓ 0.006mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.203mb/s / 81.33% |

## 8) PM2 status after restart
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2690002  │ 0s     │ 372… │ online    │ 0%       │ 42.9mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 23.4% | ram usage: 9.4% | lo: ⇓ 0.002mb/s ⇑ 0.002mb/s | eth0: ⇓ 0.006mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.203mb/s / 81.33% |
 Describing process with id 1 - name ndsp-backend 
┌───────────────────┬─────────────────────────────────────────────────┐
│ status            │ online                                          │
│ name              │ ndsp-backend                                    │
│ namespace         │ default                                         │
│ version           │ N/A                                             │
│ restarts          │ 372610                                          │
│ uptime            │ 0s                                              │
│ script path       │ /usr/bin/npm                                    │
│ script args       │ run start                                       │
│ error log path    │ /home/nawaf511/.pm2/logs/ndsp-backend-error.log │
│ out log path      │ /home/nawaf511/.pm2/logs/ndsp-backend-out.log   │
│ pid path          │ /home/nawaf511/.pm2/pids/ndsp-backend-1.pid     │
│ interpreter       │ /usr/bin/node                                   │
│ interpreter args  │ N/A                                             │
│ script id         │ 1                                               │
│ exec cwd          │ /home/nawaf511/empire-core-new/backend          │
│ exec mode         │ fork_mode                                       │
│ node.js version   │ 22.22.2                                         │
│ node env          │ N/A                                             │
│ watch & reload    │ ✘                                               │
│ unstable restarts │ 9                                               │
│ created at        │ 2026-07-07T07:20:11.218Z                        │
└───────────────────┴─────────────────────────────────────────────────┘
 Actions available 
┌────────────────────────┐
│ km:heapdump            │
│ km:cpu:profiling:start │
│ km:cpu:profiling:stop  │
│ km:heap:sampling:start │
│ km:heap:sampling:stop  │
└────────────────────────┘
 Trigger via: pm2 trigger ndsp-backend <action_name>

 Divergent env variables from local env 


 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs ndsp-backend [--lines 1000]` to display logs
 Use `pm2 env 1` to display environment variables
 Use `pm2 monit` to monitor CPU and Memory usage ndsp-backend

## 9) PM2 backend logs after patch
[TAILING] Tailing last 80 lines for [ndsp-backend] process (change the value with --lines option)
/home/nawaf511/.pm2/logs/ndsp-backend-out.log last 80 lines:
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 

/home/nawaf511/.pm2/logs/ndsp-backend-error.log last 80 lines:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ❌ NDSP NOWPayments failed: Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:54:34)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | /home/nawaf511/empire-core-new/backend/server.js:58
1|ndsp-bac |   throw e;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:54:34)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | ⚠️ NDSP trial info skipped: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ❌ NDSP NOWPayments failed: Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:54:34)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | /home/nawaf511/empire-core-new/backend/server.js:58
1|ndsp-bac |   throw e;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:54:34)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2


## 10) Public API smoke test
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Tue, 07 Jul 2026 07:20:17 GMT
content-type: application/json; charset=utf-8
content-length: 183
cache-control: no-store
x-ndsp-gateway: platform-9001

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1779.11},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,678.69","scenario_arrival_level":"1,532.63","scenario_review_zone":"1,960.54","scenario_invalidation_level":"1,952.56","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون من�

FINAL_STATUS=PM2_BACKEND_DEPENDENCY_PATCH_DONE
REPORT=docs/05-runbooks/NDSP_PATCH_PM2_BACKEND_DEPENDENCIES_20260707_092005.md
