# NDSP Patch — Make NOWPayments Optional During V1
DATE=2026-07-07T09:22:49+02:00
PATCH_BACKUP=/home/nawaf511/ndsp_backups/NDSP_NOWPAYMENTS_OPTIONAL_V1_20260707_092249

## 1) Backup server.js

## 2) Show current risky lines
    40	const app = express();
    41	
    42	/* NDSP_TRIAL_INFO_START */
    43	try {
    44	  const { installTrialInfo } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs');
    45	  installTrialInfo(app);
    46	} catch (e) {
    47	  console.error('⚠️ NDSP trial info skipped:', e.message);
    48	}
    49	/* NDSP_TRIAL_INFO_END */
    50	
    51	
    52	/* NDSP_NOWPAYMENTS_START */
    53	try {
    54	  const { installNowPayments } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs');
    55	  installNowPayments(app);
    56	} catch (e) {
    57	  console.error('❌ NDSP NOWPayments failed:', e);
    58	  throw e;
    59	}
    60	/* NDSP_NOWPAYMENTS_END */
    61	
    62	
    63	
    64	
    65	
    66	
    67	/* NDSP_DEVICE_GUARD_START */
    68	try {
    69	  const { installDeviceRegistrationGuard } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs');
    70	  installDeviceRegistrationGuard(app);

## 3) Patch fatal NOWPayments require
[WARN] Exact block not found. Trying safer generic replacement.
[OK] Patched generic NOWPayments fatal throw.

## 4) Verify patched lines
    40	const app = express();
    41	
    42	/* NDSP_TRIAL_INFO_START */
    43	try {
    44	  const { installTrialInfo } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs');
    45	  installTrialInfo(app);
    46	} catch (e) {
    47	  console.error('⚠️ NDSP trial info skipped:', e.message);
    48	}
    49	/* NDSP_TRIAL_INFO_END */
    50	
    51	
    52	/* NDSP_NOWPAYMENTS_START */
    53	try {
    54	  const { installNowPayments } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs');
    55	  installNowPayments(app);
    56	} catch (e) {
    57	  console.warn('⚠ NDSP NOWPayments skipped during V1:', e.message);
    58	}
    59	/* NDSP_NOWPAYMENTS_END */
    60	
    61	
    62	
    63	
    64	
    65	
    66	/* NDSP_DEVICE_GUARD_START */
    67	try {
    68	  const { installDeviceRegistrationGuard } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs');
    69	  installDeviceRegistrationGuard(app);
    70	} catch (e) {
    71	  console.error('❌ NDSP device guard failed:', e);
    72	  throw e;
    73	}
    74	/* NDSP_DEVICE_GUARD_END */
    75	

## 5) Syntax check

## 6) Restart only PM2 ndsp-backend
[PM2] Applying action restartProcessId on app [ndsp-backend](ids: [ 1 ])
[PM2] [ndsp-backend](1) ✓
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2700108  │ 0s     │ 372… │ online    │ 0%       │ 30.4mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 10.1% | ram usage: 9.2% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.167mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.269mb/s / 81.33% |

## 7) Wait and inspect PM2 stability
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2700520  │ 0s     │ 372… │ online    │ 0%       │ 81.2mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 10.7% | ram usage: 9.5% | lo: ⇓ 0.003mb/s ⇑ 0.003mb/s | eth0: ⇓ 0.009mb/s ⇑ 0.005mb/s | disk: ⇓ 0.04mb/s ⇑ 0.226mb/s / 81.33% |
 Describing process with id 1 - name ndsp-backend 
┌───────────────────┬─────────────────────────────────────────────────┐
│ status            │ online                                          │
│ name              │ ndsp-backend                                    │
│ namespace         │ default                                         │
│ version           │ N/A                                             │
│ restarts          │ 372629                                          │
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
│ unstable restarts │ 13                                              │
│ created at        │ 2026-07-07T07:22:50.149Z                        │
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

## 8) Logs after patch
[TAILING] Tailing last 100 lines for [ndsp-backend] process (change the value with --lines option)
/home/nawaf511/.pm2/logs/ndsp-backend-error.log last 100 lines:
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:68:46)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | ⚠️ NDSP trial info skipped: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ⚠ NDSP NOWPayments skipped during V1: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ❌ NDSP device guard failed: Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs'
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
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:68:46)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | /home/nawaf511/empire-core-new/backend/server.js:72
1|ndsp-bac |   throw e;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs'
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
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:68:46)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | ⚠️ NDSP trial info skipped: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ⚠ NDSP NOWPayments skipped during V1: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac | ❌ NDSP device guard failed: Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs'
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
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:68:46)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | /home/nawaf511/empire-core-new/backend/server.js:72
1|ndsp-bac |   throw e;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs'
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
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:68:46)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2

/home/nawaf511/.pm2/logs/ndsp-backend-out.log last 100 lines:
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


## 9) Public API smoke tests
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Tue, 07 Jul 2026 07:22:59 GMT
content-type: application/json; charset=utf-8
content-length: 183
cache-control: no-store
x-ndsp-gateway: platform-9001

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1779.11},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,678.69","scenario_arrival_level":"1,532.63","scenario_review_zone":"1,960.54","scenario_invalidation_level":"1,952.56","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-07T07:22:59Z","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_output

FINAL_STATUS=NOWPAYMENTS_OPTIONAL_PATCH_DONE
REPORT=docs/05-runbooks/NDSP_PATCH_NOWPAYMENTS_OPTIONAL_V1_20260707_092249.md
