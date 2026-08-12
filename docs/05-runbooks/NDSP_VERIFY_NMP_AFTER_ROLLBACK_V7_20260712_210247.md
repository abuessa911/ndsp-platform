============================================================
NDSP — Verify NMP After Rollback V7
DATE=2026-07-12T21:02:47+02:00
PROJECT=/home/nawaf511/empire-core-new
LOCAL_BASE=http://127.0.0.1:9082
PUBLIC_BASE=https://api.ndsp.app
SYMBOL=ETHUSDT
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_VERIFY_NMP_AFTER_ROLLBACK_V7_20260712_210247.md
MODE=READ_ONLY
============================================================

== 1) حالة الخدمات ==
[OK] ndsp-live-decision-quality.service=active
[WARN] ndsp-golden-signal-explainability.service=inactive
[OK] ndsp-quality-live-nmp-wrapper.service=active

== 2) جلب الحالات المحلية ==

--- FETCH ---
ENDPOINT=local
TIMEFRAME=daily
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=daily
HTTP=200
[OK] FETCHED=true

--- FETCH ---
ENDPOINT=local
TIMEFRAME=weekly
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
HTTP=200
[OK] FETCHED=true

--- FETCH ---
ENDPOINT=local
TIMEFRAME=monthly
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=monthly
HTTP=200
[OK] FETCHED=true

== 3) جلب الحالات العامة ==

--- FETCH ---
ENDPOINT=public
TIMEFRAME=daily
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=daily
HTTP=200
[OK] FETCHED=true

--- FETCH ---
ENDPOINT=public
TIMEFRAME=weekly
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
HTTP=200
[OK] FETCHED=true

--- FETCH ---
ENDPOINT=public
TIMEFRAME=monthly
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=monthly
HTTP=200
[OK] FETCHED=true

== 4) تحليل العقود ==

--- LOCAL DAILY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=daily
SELECTED_TIMEFRAME=daily
NMP_STATUS=AVAILABLE
NMP_VALUE=3224.99
NMP_TIMEFRAME=daily
NMP_SOURCE_INTERVAL=1d
TOP_NMP_TIMEFRAME=daily
SCENARIO_NMP_TIMEFRAME=daily
PUBLIC_NMP_TIMEFRAME=None

--- LOCAL WEEKLY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=weekly
SELECTED_TIMEFRAME=weekly
NMP_STATUS=AVAILABLE
NMP_VALUE=1678.12
NMP_TIMEFRAME=weekly
NMP_SOURCE_INTERVAL=1w
TOP_NMP_TIMEFRAME=weekly
SCENARIO_NMP_TIMEFRAME=weekly
PUBLIC_NMP_TIMEFRAME=None

--- LOCAL MONTHLY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=monthly
SELECTED_TIMEFRAME=monthly
NMP_STATUS=AVAILABLE
NMP_VALUE=2007.02
NMP_TIMEFRAME=monthly
NMP_SOURCE_INTERVAL=1M
TOP_NMP_TIMEFRAME=monthly
SCENARIO_NMP_TIMEFRAME=monthly
PUBLIC_NMP_TIMEFRAME=None

--- PUBLIC DAILY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=daily
SELECTED_TIMEFRAME=daily
NMP_STATUS=AVAILABLE
NMP_VALUE=3224.99
NMP_TIMEFRAME=daily
NMP_SOURCE_INTERVAL=1d
TOP_NMP_TIMEFRAME=daily
SCENARIO_NMP_TIMEFRAME=daily
PUBLIC_NMP_TIMEFRAME=None

--- PUBLIC WEEKLY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=weekly
SELECTED_TIMEFRAME=weekly
NMP_STATUS=AVAILABLE
NMP_VALUE=1678.12
NMP_TIMEFRAME=weekly
NMP_SOURCE_INTERVAL=1w
TOP_NMP_TIMEFRAME=weekly
SCENARIO_NMP_TIMEFRAME=weekly
PUBLIC_NMP_TIMEFRAME=None

--- PUBLIC MONTHLY CONTRACT ---
OK=True
INSTRUMENT_TIMEFRAME=monthly
SELECTED_TIMEFRAME=monthly
NMP_STATUS=AVAILABLE
NMP_VALUE=2007.02
NMP_TIMEFRAME=monthly
NMP_SOURCE_INTERVAL=1M
TOP_NMP_TIMEFRAME=monthly
SCENARIO_NMP_TIMEFRAME=monthly
PUBLIC_NMP_TIMEFRAME=None

== CONTRACT ERROR SUMMARY ==
LOCAL_ERRORS=[]
PUBLIC_ERRORS=[]
LOCAL_NMP_CONTRACT_OK=true
PUBLIC_NMP_CONTRACT_OK=true
FINAL_ANALYSIS=NMP_CONTRACT_OK

== 5) ملخص المسارات المتسلسلة ==

PORT=9057 HTTP=200
instrument=weekly
selected=weekly
nmp_tf=MISSING
nmp_interval=MISSING
source_mode=python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27

PORT=9067 HTTP=200
instrument=weekly
selected=weekly
nmp_tf=MISSING
nmp_interval=MISSING
source_mode=python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27

PORT=9082 HTTP=200
instrument=weekly
selected=weekly
nmp_tf=weekly
nmp_interval=1w
source_mode=python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27

============================================================
[OK] NMP يحترم الفريم المطلوب محليًا وعبر المسار العام
DAILY_SOURCE_INTERVAL=1d
WEEKLY_SOURCE_INTERVAL=1w
MONTHLY_SOURCE_INTERVAL=1M
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_VERIFY_NMP_AFTER_ROLLBACK_V7_20260712_210247.md
FINAL_STATUS=NMP_CONTRACT_OK
============================================================
