# NDSP Patch — Quarantine Unused PM2 ndsp-backend
DATE=2026-07-07T09:26:29+02:00
BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_QUARANTINE_UNUSED_PM2_BACKEND_20260707_092629

## 1) Pre-state
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 0        │ 0      │ 372… │ errored   │ 0%       │ 0b       │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11% | ram usage: 9.3% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.169mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.3mb/s / 81.33% |

 Describing process with id 1 - name ndsp-backend 
┌───────────────────┬─────────────────────────────────────────────────┐
│ status            │ errored                                         │
│ name              │ ndsp-backend                                    │
│ namespace         │ default                                         │
│ version           │ N/A                                             │
│ restarts          │ 372631                                          │
│ uptime            │ 0                                               │
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
│ unstable restarts │ 0                                               │
│ created at        │ N/A                                             │
└───────────────────┴─────────────────────────────────────────────────┘
 Divergent env variables from local env 


 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs ndsp-backend [--lines 1000]` to display logs
 Use `pm2 env 1` to display environment variables
 Use `pm2 monit` to monitor CPU and Memory usage ndsp-backend

 Describing process with id 0 - name ndsp-portal 
┌───────────────────┬─────────────────────────────────────────────────────┐
│ status            │ online                                              │
│ name              │ ndsp-portal                                         │
│ namespace         │ default                                             │
│ version           │ 0.39.7                                              │
│ restarts          │ 0                                                   │
│ uptime            │ 42h                                                 │
│ script path       │ /home/nawaf511/.nvm/versions/node/v24.15.0/bin/npm  │
│ script args       │ run start                                           │
│ error log path    │ /home/nawaf511/.pm2/logs/ndsp-portal-error.log      │
│ out log path      │ /home/nawaf511/.pm2/logs/ndsp-portal-out.log        │
│ pid path          │ /home/nawaf511/.pm2/pids/ndsp-portal-0.pid          │
│ interpreter       │ /home/nawaf511/.nvm/versions/node/v24.15.0/bin/node │
│ interpreter args  │ N/A                                                 │
│ script id         │ 0                                                   │
│ exec cwd          │ /home/nawaf511/empire-core-new/apps/user-portal     │
│ exec mode         │ fork_mode                                           │
│ node.js version   │ 24.15.0                                             │
│ node env          │ N/A                                                 │
│ watch & reload    │ ✘                                                   │
│ unstable restarts │ 0                                                   │
│ created at        │ 2026-05-22T19:23:44.960Z                            │
└───────────────────┴─────────────────────────────────────────────────────┘
 Actions available 
┌────────────────────────┐
│ km:heapdump            │
│ km:cpu:profiling:start │
│ km:cpu:profiling:stop  │
│ km:heap:sampling:start │
│ km:heap:sampling:stop  │
└────────────────────────┘
 Trigger via: pm2 trigger ndsp-portal <action_name>

 Code metrics value 
┌────────────────────────┬───────────┐
│ Heap Size              │ 14.19 MiB │
│ Heap Usage             │ 81.38 %   │
│ Used Heap Size         │ 11.55 MiB │
│ Active requests        │ 0         │
│ Active handles         │ 5         │
│ Event Loop Latency     │ 0.61 ms   │
│ Event Loop Latency p95 │ 1.81 ms   │
└────────────────────────┴───────────┘
 Divergent env variables from local env 
┌────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PWD                │ /home/nawaf511/empire-core-new/apps/user-portal                                                                                                                                                                                                  │
│ TELEGRAM_BOT_TOKEN │ 8570826779:AAF7wVKT57HAcMVN-MsfxCgkdurLDWr-nxo                                                                                                                                                                                                   │
│ SSH_CONNECTION     │ 109.83.85.169 37703 161.97.144.189 22                                                                                                                                                                                                            │
│ XDG_SESSION_ID     │ 2609                                                                                                                                                                                                                                             │
│ SSH_CLIENT         │ 109.83.85.169 37703 22                                                                                                                                                                                                                           │
│ PATH               │ /home/nawaf511/.nvm/versions/node/v24.15.0/bin:/home/nawaf511/empire-core-new/apps/user-portal/node_modules/.bin:/home/nawaf511/empire-core-new/apps/node_modules/.bin:/home/nawaf511/empire-core-new/node_modules/.bin:/home/nawaf511/node_modu │
│ SSH_TTY            │ /dev/pts/4                                                                                                                                                                                                                                       │
│ _                  │ /home/nawaf511/.nvm/versions/node/v24.15.0/bin/npx                                                                                                                                                                                               │
└────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs ndsp-portal [--lines 1000]` to display logs
 Use `pm2 env 0` to display environment variables
 Use `pm2 monit` to monitor CPU and Memory usage ndsp-portal

## 2) Backup PM2 state and logs

## 3) Confirm live owners before quarantine
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2661,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=1349,fd=3))                                                                                                                                                                                                                               
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1347,fd=32))                                                                                                                                                                                                                                 
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=1357,fd=3))                                                                                                                                                                                                                               

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 183
Cache-Control: no-store
X-NDSP-Gateway: platform-9001
Date: Tue, 07 Jul 2026 07:26:47 GMT
Connection: keep-alive
Keep-Alive: timeout=5

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
HTTP/1.0 200 OK
Server: NDSPQualityLiveNMPWrapper/1.0 Python/3.12.3
Date: Tue, 07 Jul 2026 07:26:49 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 7145
Cache-Control: no-store, no-cache, max-age=0, must-revalidate

{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1779.11},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,678.69","scenario_arrival_level":"1,532.63","scenario_review_zone":"1,960.54","scenario_invalidation_level":"1,952.56","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-07T07:26:48Z","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_outputs":{"directional_bias":"قراءة أسبوعي · ضغط هابط","reading_horizon":"متابعة كسر أسبوعي","horizon_strength":"عالية جدًا","market_state":"قراءة أسبوعي · ضغط هابط","decision_quality":86,"caution_reason":"انتظار ثبات السعر دون منطقة المراجعة.","sanitized_summary":"قراءة أسبوعي على ETHUSDT: السعر 1,779.11، جودة القراءة 86، الحالة قراءة أسبوعي · ضغط هابط.","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة."},"live_market_analysis":{"provider":"binance","price":1779.11,"price_change_24h_pct":0.5357052039126705,"atr_4h":28.891428571428587,"atr_4h_pct":1.6239259276508249,"rsi_4h":43.717138299757785,"momentum_price_4h":1771.56,"momentum_close_time_4h":1783396799999,"direction":"neutral","market_state":"تذبذب بيني · قرب المتوسط","horizon_strength":"ضعيفة/متوسطة","confidence_band":"منخفض","h1_direction":"neutral","h4_direction":"neutral","d1_direction":"neutral","technical_review_price":1763.2827588574876,"scenario_levels_model":"timeframe_atr_ema_v27","selected_timeframe":"weekly","selected_timeframe_label":"أسبوعي","selected_timeframe_close":1799.56,"selected_timeframe_rsi":32.23801503801785,"selected_timeframe_atr":182.57500000000002,"selected_timeframe_direction":"bearish","timeframe_model":"asset_view_timeframe_v27"},"live_price_bound":true,"data_provider":"binance","generated_at":"2026-07-07T07:26:48Z","golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"86 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_alignment":{"golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_label_public":"جزئية / تحت المراقبة","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_name_public":"إشارة نواف الذهبية","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"86 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_effect_public":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","not_recommendation":true,"no_buy_sell":true,"protected_layers_masked":true,"source_mode":"quality_live_governed_output_runtime_alignment","wrapper_version":"1.0.0-ndsp-golden-explainability"},"golden_spotlight":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","summary":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","quality_effect":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","evidence":[{"label":"جودة القرار","value":"86 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}]},"explainability":{"golden_signal_exposed":true,"golden_signal":false,"golden_status":"partial","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence_trace":true,"reason_codes":true,"engine_coverage":"masked_public_trace","protected_layers_masked":true,"no_internal_formula_exposure":true,"not_recommendation":true},"public_explainability":{"golden_alignment":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","reason":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence":[{"label":"جودة القرار","value":"86 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"notice":"هذه قراءة سياقية داعمة لجودة القرار فقط، وليست توصية مالية."}},"_ndsp_golden_explainability_injected_at_ms":1783409208912,"nmp":{"status":"AVAILABLE","value":1583.4,"level":1583.4,"source":"quality-live-nmp-wrapper","provider":"binance_klines","method":"RSI_EXTREME_MOMENTUM_CANDLE_OPEN","rule":"NMP = opening price of the momentum candle","symbol":"ETHUSDT","timeframe":"1D","source_interval":"1d","direction":"BEARISH","rsi":12.7647,"momentum_candle":{"open_time_ms":1780704000000,"open":1583.4,"high":1601.22,"low":1505.68,"close":1569.69},"note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة.","updated_at":"2026-07-07T07:26:49+00:00"},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_value":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D","_ndsp_nmp_injected_at":"2026-07-07T07:26:49+00:00","_ndsp_nmp_contract":"quality-live-nmp-wrapper-v1"}
## 4) Quarantine broken PM2 process
[PM2] Applying action deleteProcessId on app [ndsp-backend](ids: [ 1 ])
[PM2] [ndsp-backend](1) ✓
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11% | ram usage: 9.3% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.169mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.3mb/s / 81.33% |
[PM2] Saving current process list...
[PM2] Successfully saved in /home/nawaf511/.pm2/dump.pm2

## 5) Post-state
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 11% | ram usage: 9.3% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.169mb/s ⇑ 0.006mb/s | disk: ⇓ 0mb/s ⇑ 0.3mb/s / 81.33% |

## 6) Public smoke tests after quarantine
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Tue, 07 Jul 2026 07:26:50 GMT
content-type: application/json; charset=utf-8
content-length: 183
cache-control: no-store
x-ndsp-gateway: platform-9001

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1779.11},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,678.69","scenario_arrival_level":"1,532.63","scenario_review_zone":"1,960.54","scenario_invalidation_level":"1,952.56","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-07T07:26:50Z","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_output
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Tue, 07 Jul 2026 07:26:51 GMT
content-type: text/html; charset=utf-8
content-length: 812
last-modified: Sun, 05 Jul 2026 17:03:19 GMT
etag: "6a4a8e57-32c"
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains
content-security-policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://my.ndsp.app https://api.ndsp.app; object-src 'none'; base-uri 'self'; frame-ancestors 'none';
permissions-policy: camera=(), microphone=(), geolocation=()
accept-ranges: bytes


HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Tue, 07 Jul 2026 07:26:51 GMT
content-type: text/html; charset=utf-8
content-length: 812
last-modified: Sun, 05 Jul 2026 17:03:19 GMT
etag: "6a4a8e57-32c"
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains
content-security-policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://my.ndsp.app https://api.ndsp.app; object-src 'none'; base-uri 'self'; frame-ancestors 'none';
permissions-policy: camera=(), microphone=(), geolocation=()
accept-ranges: bytes


## 7) Rollback command if ever needed
cd /home/nawaf511/empire-core-new/backend
pm2 start npm --name ndsp-backend -- run start
pm2 save --force

FINAL_STATUS=UNUSED_PM2_BACKEND_QUARANTINED
REPORT=docs/05-runbooks/NDSP_PATCH_QUARANTINE_UNUSED_PM2_BACKEND_20260707_092629.md
