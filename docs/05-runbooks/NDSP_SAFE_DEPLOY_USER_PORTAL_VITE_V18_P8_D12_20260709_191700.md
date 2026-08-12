# NDSP Safe Deploy User Portal Vite v18 P8 D12
DATE=2026-07-09T19:17:00+02:00
PROJECT_DIR=/home/nawaf511/empire-core-new
APP_DIR=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE_DIR=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

== 1) BASIC PATH CHECK ==
OK: /home/nawaf511/empire-core-new/frontend/user-portal-vite
OK: /home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx
OK: /home/nawaf511/empire-core-new/frontend/user-portal-vite/src/styles.css
OK: /var/www/ndsp-my

== 2) GIT STATUS SNAPSHOT ==
 M README.md
 M backend/auth_api/ndsp_platform_gateway_9001.cjs
 M backend/data/raw_cot/current_disaggregated_futures_only_f_disagg.txt
 M backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt
 M backend/data/raw_cot/raw_cot_manifest.json
 M backend/server.js
 M frontend/user-portal-vite/src/main.jsx
 M frontend/user-portal-vite/src/styles.css
?? NDSP_CODEX_V18_P8_D12_ARABIC_MOBILE_DECISION_ROOM_FIX_PROMPT.txt
?? backend/auth_api/ndsp_register_compat_gateway.cjs
?? backend/data/raw_cot/disaggregated_futures_only_f_disagg_20260703_222221.txt
?? backend/data/raw_cot/tff_futures_only_FinFutWk_20260703_222221.txt
?? backend/password_reset_gateway/run_password_reset_gateway.sh
?? backups/
?? docs/00-build-catalog/
?? docs/01-build-control-pack/
?? docs/02-execution-ready-pack/
?? docs/03-final-transition/
?? docs/04-legal/
?? docs/05-runbooks/
?? docs/06-decision-room-contracts/
?? docs/README.md
?? docs/README_NDSP_GOVERNANCE_ENTRYPOINT.md
?? scripts/

== 3) SOURCE SAFETY GATE ==
OK: no old .html menu hrefs.
OK: no rejected current-clock timestamp formatter.
OK: no rejected fake hard-coded levels.
442:async function fetchScenarioLevels(symbol) {
443:  const endpoint = `/api/scenario/levels?symbol=${encodeURIComponent(symbol)}`;
476:  const [scenarioPayload, setScenarioPayload] = useState(null);
492:    () => getReferenceLevels(scenarioPayload || price, tr.locale, tr.waitingData),
493:    [scenarioPayload, price, tr.locale, tr.waitingData]
523:    fetchScenarioLevels(symbol).then((payload) => {
OK: scenario payload binding exists.
OK: adapter key exists: activation_price
OK: adapter key exists: arrival_price
OK: adapter key exists: review_price
OK: adapter key exists: cancel_price
OK: adapter key exists: invalidation_price
OK: adapter key exists: nmp_price

== 4) API PREFLIGHT - NON-BLOCKING ==
-- API health --
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:01 GMT
content-type: application/json; charset=utf-8
content-length: 183
cache-control: no-store
x-ndsp-gateway: platform-9001

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
-- Decision API --
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:04 GMT
content-type: application/json; charset=utf-8
content-length: 8474
cache-control: no-store, no-cache, max-age=0, must-revalidate
cache-control: no-store, no-cache, must-revalidate, proxy-revalidate

{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1739.25},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,638.55","scenario_arrival_level":"1,492.08","scenario_review_zone":"1,956.26","scenario_invalidation_level":"1,913.18","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-09T17:17:03Z","scenario_levels":{"activation":{"price":1638.55,"label_ar":"مستوى التفعيل","label_en":"Activation level","source":"computed","raw_value":"1,638.55"},"arrival":{"price":1492.08,"label_ar":"مستوى الوصول","label_en":"Arrival level","source":"computed","raw_value":"1,492.08"},"review":{"price":1956.26,"label_ar":"مستوى المراجعة","label_en":"Review level","source":"computed","raw_value":"1,956.26"},"invalidation":{"price":1913.18,"label_ar":"مستوى الإلغاء","label_en":"Invalidation level","source":"computed","raw_value":"1,913.18"}},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_outputs":{"directional_bias":"قراءة أسبوعي · ضغط هابط","reading_horizon":"متابعة كسر أسبوعي","horizon_strength":"عالية جدًا","market_state":"قراءة أسبوعي · ضغط هابط","decision_quality":87,"caution_reason":"انتظار ثبات السعر دون منطقة المراجعة.","sanitized_summary":"قراءة أسبوعي على ETHUSDT: السعر 1,739.25، جودة القراءة 87، الحالة قراءة أسبوعي · ضغط هابط.","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة."},"live_market_analysis":{"provider":"binance","price":1739.25,"price_change_24h_pct":0.1652864004422932,"atr_4h":28.26928571428571,"atr_4h_pct":1.6253721842337623,"rsi_4h":41.20419138437655,"momentum_price_4h":1739.51,"momentum_close_time_4h":1783612799999,"direction":"neutral","market_state":"تذبذب بيني · ضغط سفلي","horizon_strength":"ضعيفة/متوسطة","confidence_band":"منخفض","h1_direction":"neutral","h4_direction":"neutral","d1_direction":"neutral","technical_review_price":1752.9430844782282,"scenario_levels_model":"timeframe_atr_ema_v27","selected_timeframe":"weekly","selected_timeframe_label":"أسبوعي","selected_timeframe_close":1743.54,"selected_timeframe_rsi":27.46673272933181,"selected_timeframe_atr":183.08571428571426,"selected_timeframe_direction":"bearish","timeframe_model":"asset_view_timeframe_v27"},"live_price_bound":true,"data_provider":"binance","generated_at":"2026-07-09T17:17:03Z","golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_alignment":{"golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_label_public":"جزئية / تحت المراقبة","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_name_public":"إشارة نواف الذهبية","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_effect_public":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","not_recommendation":true,"no_buy_sell":true,"protected_layers_masked":true,"source_mode":"quality_live_governed_output_runtime_alignment","wrapper_version":"1.0.0-ndsp-golden-explainability"},"golden_spotlight":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","summary":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","quality_effect":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","evidence":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}]},"explainability":{"golden_signal_exposed":true,"golden_signal":false,"golden_status":"partial","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence_trace":true,"reason_codes":true,"engine_coverage":"masked_public_trace","protected_layers_masked":true,"no_internal_formula_exposure":true,"not_recommendation":true},"public_explainability":{"golden_alignment":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","reason":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"notice":"هذه قراءة سياقية داعمة لجودة القرار فقط، وليست توصية مالية."}},"_ndsp_golden_explainability_injected_at_ms":1783617423880,"nmp":{"status":"AVAILABLE","value":1583.4,"level":1583.4,"source":"quality-live-nmp-wrapper","provider":"binance_klines","method":"RSI_EXTREME_MOMENTUM_CANDLE_OPEN","rule":"NMP = opening price of the momentum candle","symbol":"ETHUSDT","timeframe":"1D","source_interval":"1d","direction":"BEARISH","rsi":12.7647,"momentum_candle":{"open_time_ms":1780704000000,"open":1583.4,"high":1601.22,"low":1505.68,"close":1569.69},"note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة.","updated_at":"2026-07-09T17:17:04+00:00"},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_value":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D","scenario_levels":{"activation":{"price":1638.55,"label_ar":"مستوى التفعيل","label_en":"Activation level","source":"computed","raw_value":"1,638.55"},"arrival":{"price":1492.08,"label_ar":"مستوى الوصول","label_en":"Arrival level","source":"computed","raw_value":"1,492.08"},"review":{"price":1956.26,"label_ar":"مستوى المراجعة","label_en":"Review level","source":"computed","raw_value":"1,956.26"},"invalidation":{"price":1913.18,"label_ar":"مستوى الإلغاء","label_en":"Invalidation level","source":"computed","raw_value":"1,913.18"}},"_ndsp_v12_scenario_levels_contract":{"status":"injected","source":"quality-live-nmp-wrapper","rule":"derived_from_existing_scenario_flat_fields_without_inventing_numbers"},"_ndsp_nmp_injected_at":"2026-07-09T17:17:04+00:00","_ndsp_nmp_contract":"quality-live-nmp-wrapper-v1"}
-- Scenario levels via frontend same-origin proxy --
HTTP/2 404 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:04 GMT
content-type: application/json; charset=utf-8
cache-control: no-store
access-control-allow-origin: *
access-control-allow-methods: GET,OPTIONS
access-control-allow-headers: Content-Type,Authorization
x-ndsp-gateway: platform-9001
x-ndsp-portal: approved-design-only-d10-d4
x-content-type-options: nosniff

{"ok": false, "error": "NOT_FOUND", "path": "/api/scenario/levels", "service": "ndsp-platform-gateway-9002"}
-- Scenario levels via api domain --
HTTP/2 404 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:05 GMT
content-type: application/json; charset=utf-8
cache-control: no-store
access-control-allow-origin: *
access-control-allow-methods: GET,OPTIONS
access-control-allow-headers: Content-Type,Authorization
x-ndsp-gateway: platform-9001

{"ok": false, "error": "NOT_FOUND", "path": "/api/scenario/levels", "service": "ndsp-platform-gateway-9002"}
NOTE: scenario levels check is non-blocking. If endpoint is missing, UI must show fallback, not fake levels.

== 5) BACKUP LIVE + SOURCE FILES ==
OK: live backup created: /home/nawaf511/ndsp_deploy_backups/ndsp-my-before-vite-v18-p8-d12-20260709_191700.tar.gz
OK: source backup created: /home/nawaf511/ndsp_deploy_backups/source-vite-v18-p8-d12-20260709_191700

== 6) BUILD VITE APP ==

> ndsp-user-portal-vite@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 27 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.44 kB │ gzip:  0.33 kB
dist/assets/index-CB5D1TQG.css    8.81 kB │ gzip:  2.62 kB
dist/assets/index-BX9FubtP.js   169.72 kB │ gzip: 53.47 kB
✓ built in 3.24s
OK: build completed.

== 7) STAGE DIST ==
OK: staged dist at /home/nawaf511/ndsp_deploy_stage/vite-v18-p8-d12-20260709_191700

== 8) WRITE ROLLBACK SCRIPT ==
OK: rollback script created: /home/nawaf511/ndsp_deploy_backups/rollback_ndsp_my_vite_v18_p8_d12_20260709_191700.sh

== 9) DEPLOY DIST TO LIVE - NO DELETE ==
Important: using rsync without --delete to avoid deleting existing legacy/static pages.
OK: dist copied to live.

== 10) LIVE FILE CHECK ==
OK: live index exists.
OK: live assets exist.

== 11) HTTP SMOKE TEST ==
HOME_HTTP=200
INDEX_HTTP=200
OK: frontend HTTP 200.

== 12) LIVE ASSET HTTP CHECK FROM INDEX ==
ASSET_HTTP 200 /assets/index-BX9FubtP.js
ASSET_HTTP 200 /assets/index-CB5D1TQG.css

== 13) POST DEPLOY API SMOKE - NON-BLOCKING ==
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:17 GMT
content-type: application/json; charset=utf-8
content-length: 183
cache-control: no-store
x-ndsp-gateway: platform-9001

{"ok":true,"service":"ndsp-platform-gateway","platform_backend_port":9001,"bot_backend_port":9002,"public_api_namespace":"/api","legacy_services_behind_gateway":[9017,9019,9020,9021]}
HTTP/2 200 
server: nginx/1.24.0 (Ubuntu)
date: Thu, 09 Jul 2026 17:17:19 GMT
content-type: application/json; charset=utf-8
content-length: 8474
cache-control: no-store, no-cache, max-age=0, must-revalidate
cache-control: no-store, no-cache, must-revalidate, proxy-revalidate

{"ok":true,"source_mode":"python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27","project":"NDSP — منصة نواف لدعم القرار","package":"free","instrument":{"symbol":"ETHUSDT","market":"CRYPTO","timeframe":"UNSPECIFIED","live_price":1739.25},"scenario":{"scenario_state":"UNDER_MONITORING","scenario_directional_context":"قراءة أسبوعي · ضغط هابط","scenario_activation_level":"1,638.55","scenario_arrival_level":"1,492.08","scenario_review_zone":"1,956.26","scenario_invalidation_level":"1,913.18","scenario_confidence_band":"عالية جدًا","scenario_time_horizon":"متابعة كسر أسبوعي","scenario_risk_note":"انتظار ثبات السعر دون منطقة المراجعة.","scenario_last_updated":"2026-07-09T17:17:18Z","scenario_levels":{"activation":{"price":1638.55,"label_ar":"مستوى التفعيل","label_en":"Activation level","source":"computed","raw_value":"1,638.55"},"arrival":{"price":1492.08,"label_ar":"مستوى الوصول","label_en":"Arrival level","source":"computed","raw_value":"1,492.08"},"review":{"price":1956.26,"label_ar":"مستوى المراجعة","label_en":"Review level","source":"computed","raw_value":"1,956.26"},"invalidation":{"price":1913.18,"label_ar":"مستوى الإلغاء","label_en":"Invalidation level","source":"computed","raw_value":"1,913.18"}},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D"},"allowed_public_outputs":{"directional_bias":"قراءة أسبوعي · ضغط هابط","reading_horizon":"متابعة كسر أسبوعي","horizon_strength":"عالية جدًا","market_state":"قراءة أسبوعي · ضغط هابط","decision_quality":87,"caution_reason":"انتظار ثبات السعر دون منطقة المراجعة.","sanitized_summary":"قراءة أسبوعي على ETHUSDT: السعر 1,739.25، جودة القراءة 87، الحالة قراءة أسبوعي · ضغط هابط.","nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة."},"live_market_analysis":{"provider":"binance","price":1739.25,"price_change_24h_pct":0.1652864004422932,"atr_4h":28.26928571428571,"atr_4h_pct":1.6253721842337623,"rsi_4h":41.20419138437655,"momentum_price_4h":1739.51,"momentum_close_time_4h":1783612799999,"direction":"neutral","market_state":"تذبذب بيني · ضغط سفلي","horizon_strength":"ضعيفة/متوسطة","confidence_band":"منخفض","h1_direction":"neutral","h4_direction":"neutral","d1_direction":"neutral","technical_review_price":1752.9430844782282,"scenario_levels_model":"timeframe_atr_ema_v27","selected_timeframe":"weekly","selected_timeframe_label":"أسبوعي","selected_timeframe_close":1743.54,"selected_timeframe_rsi":27.46673272933181,"selected_timeframe_atr":183.08571428571426,"selected_timeframe_direction":"bearish","timeframe_model":"asset_view_timeframe_v27"},"live_price_bound":true,"data_provider":"binance","generated_at":"2026-07-09T17:17:18Z","golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_alignment":{"golden_signal":false,"golden_alignment_active":false,"golden_status":"partial","golden_label_public":"جزئية / تحت المراقبة","golden_name":"NDSP_GOLDEN_ALIGNMENT","golden_name_public":"إشارة نواف الذهبية","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","golden_evidence_public":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"golden_effect_public":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","not_recommendation":true,"no_buy_sell":true,"protected_layers_masked":true,"source_mode":"quality_live_governed_output_runtime_alignment","wrapper_version":"1.0.0-ndsp-golden-explainability"},"golden_spotlight":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","summary":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","quality_effect":"معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.","evidence":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}]},"explainability":{"golden_signal_exposed":true,"golden_signal":false,"golden_status":"partial","golden_reason_public":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence_trace":true,"reason_codes":true,"engine_coverage":"masked_public_trace","protected_layers_masked":true,"no_internal_formula_exposure":true,"not_recommendation":true},"public_explainability":{"golden_alignment":{"title":"إشارة نواف الذهبية","status":"partial","label":"جزئية / تحت المراقبة","reason":"بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل.","evidence":[{"label":"جودة القرار","value":"87 / 100"},{"label":"حالة السيناريو","value":"UNDER_MONITORING"},{"label":"سياق الاتجاه","value":"قراءة أسبوعي · ضغط هابط"},{"label":"سبب التحفظ","value":"انتظار ثبات السعر دون منطقة المراجعة."}],"notice":"هذه قراءة سياقية داعمة لجودة القرار فقط، وليست توصية مالية."}},"_ndsp_golden_explainability_injected_at_ms":1783617439456,"nmp":{"status":"AVAILABLE","value":1583.4,"level":1583.4,"source":"quality-live-nmp-wrapper","provider":"binance_klines","method":"RSI_EXTREME_MOMENTUM_CANDLE_OPEN","rule":"NMP = opening price of the momentum candle","symbol":"ETHUSDT","timeframe":"1D","source_interval":"1d","direction":"BEARISH","rsi":12.7647,"momentum_candle":{"open_time_ms":1780704000000,"open":1583.4,"high":1601.22,"low":1505.68,"close":1569.69},"note":"NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة.","updated_at":"2026-07-09T17:17:19+00:00"},"nmp_status":"AVAILABLE","nmp_level":1583.4,"nmp_value":1583.4,"nmp_source":"quality-live-nmp-wrapper","nmp_timeframe":"1D","scenario_levels":{"activation":{"price":1638.55,"label_ar":"مستوى التفعيل","label_en":"Activation level","source":"computed","raw_value":"1,638.55"},"arrival":{"price":1492.08,"label_ar":"مستوى الوصول","label_en":"Arrival level","source":"computed","raw_value":"1,492.08"},"review":{"price":1956.26,"label_ar":"مستوى المراجعة","label_en":"Review level","source":"computed","raw_value":"1,956.26"},"invalidation":{"price":1913.18,"label_ar":"مستوى الإلغاء","label_en":"Invalidation level","source":"computed","raw_value":"1,913.18"}},"_ndsp_v12_scenario_levels_contract":{"status":"injected","source":"quality-live-nmp-wrapper","rule":"derived_from_existing_scenario_flat_fields_without_inventing_numbers"},"_ndsp_nmp_injected_at":"2026-07-09T17:17:19+00:00","_ndsp_nmp_contract":"quality-live-nmp-wrapper-v1"}
== 14) SUMMARY ==
BACKUP_TAR=/home/nawaf511/ndsp_deploy_backups/ndsp-my-before-vite-v18-p8-d12-20260709_191700.tar.gz
SOURCE_BACKUP_DIR=/home/nawaf511/ndsp_deploy_backups/source-vite-v18-p8-d12-20260709_191700
STAGE_DIR=/home/nawaf511/ndsp_deploy_stage/vite-v18-p8-d12-20260709_191700
ROLLBACK_SCRIPT=/home/nawaf511/ndsp_deploy_backups/rollback_ndsp_my_vite_v18_p8_d12_20260709_191700.sh
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_SAFE_DEPLOY_USER_PORTAL_VITE_V18_P8_D12_20260709_191700.md
FINAL_STATUS=SAFE_DEPLOY_OK_FRONTEND_VITE_ONLY
