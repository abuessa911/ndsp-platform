============================================================
NDSP — NMP Requested Timeframe Fix V6
DATE=2026-07-12T20:58:24+02:00
PROJECT=/home/nawaf511/empire-core-new
TARGET=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
SERVICE=ndsp-quality-live-nmp-wrapper.service
LOCAL_BASE=http://127.0.0.1:9082
PUBLIC_BASE=https://api.ndsp.app
SYMBOL=ETHUSDT
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_NMP_REQUESTED_TIMEFRAME_V6_20260712_205824.md
============================================================

== 1) فحص الحالة الحالية ==
OWNER=root
GROUP=root
MODE=755
PRE_SHA256=d3f066f0f5b3c0d74dd4d29057e92b97dc539a4b4a3aa802711fb4ef478dfd68
PRE_HTTP=200
PRE_INSTRUMENT_TIMEFRAME=weekly
PRE_SELECTED_TIMEFRAME=weekly
PRE_NMP_TIMEFRAME=weekly
PRE_NMP_SOURCE_INTERVAL=1w

== 2) إنشاء النسخة الاحتياطية ==
BACKUP=/home/nawaf511/ndsp_backend_backups/nmp-requested-timeframe-v6-20260712_205824/ndsp_quality_live_nmp_wrapper.py.before_v6
BACKUP_SHA256=d3f066f0f5b3c0d74dd4d29057e92b97dc539a4b4a3aa802711fb4ef478dfd68

== 3) تحليل وتعديل NMP wrapper ==
PATCH_STATE=INSERTED
COMPUTE_FUNCTION_LINE=90
INJECTION_FUNCTION=enrich_with_nmp
METADATA_REPLACEMENTS=7
FETCH_REPLACEMENTS=2
REQUESTED_TIMEFRAME_BOUND=YES
ACTUAL_CANDLE_INTERVAL_BOUND=YES

== 4) فحص الملف المؤقت ==
[OK] PATCHED_PYTHON_COMPILE=true
PATCHED_SHA256=bc74d12705dc6d991b9ce5c9a131d1fc173499f89b2a1fc2e46f22b569918907

== 5) عرض مواضع التصحيح ==
82-
83-def binance_symbol_ok(symbol):
84-    s = str(symbol or "").upper().strip()
85-    if not s.endswith("USDT"):
86-        return False
87-    base = s.replace("USDT", "")
88-    return bool(base) and base.isalnum()
89-
90:# NDSP_NMP_REQUESTED_TIMEFRAME_V6
91-def _ndsp_nmp_timeframe_contract_v6(value):
92-    token = str(value or "").strip()
93-    lowered = token.lower()
94-
95-    if lowered in (
96-        "daily",
97-        "day",
98-        "d",
99-        "1d",
100-        "يومي",
101-    ):
102-        return {
103-            "public": "daily",
104-            "canonical": "1D",
105:            "source_interval": "1d",
106-        }
107-
108-    if lowered in (
109-        "monthly",
110-        "month",
111-        "m",
112-        "1m",
113-        "شهري",
114-    ):
115-        return {
116-            "public": "monthly",
117-            "canonical": "1M",
118:            "source_interval": "1M",
119-        }
120-
121-    return {
122-        "public": "weekly",
123-        "canonical": "1W",
124:        "source_interval": "1w",
125-    }
126-
127-
128:def _ndsp_nmp_requested_timeframe_v6(data):
129-    if not isinstance(data, dict):
130-        return "weekly"
131-
132-    instrument = data.get("instrument")
133-    if not isinstance(instrument, dict):
134-        instrument = {}
135-
136-    analysis = data.get("live_market_analysis")
--
141-        instrument.get("timeframe")
142-        or analysis.get("selected_timeframe")
143-        or "weekly"
144-    )
145-
146-    return _ndsp_nmp_timeframe_contract_v6(candidate)["public"]
147-
148-def compute_nmp(symbol, timeframe, data):
149:    _ndsp_tf_contract_v6 = _ndsp_nmp_timeframe_contract_v6(timeframe)
150:    timeframe = _ndsp_tf_contract_v6["canonical"]
151:    source_interval = _ndsp_tf_contract_v6["source_interval"]
152-    symbol = str(symbol or "").upper().strip()
153-    tf = str(timeframe or "1D").strip()
154:    interval = source_interval
155-
156-    if not binance_symbol_ok(symbol):
157-        return {
158-            "status": "UNAVAILABLE",
159-            "value": None,
160-            "level": None,
161-            "source": "quality-live-nmp-wrapper",
162-            "timeframe": timeframe,
163-            "note": "NMP غير متاح لهذا الأصل عبر Binance klines."
164-        }
165-
166-    url = "https://api.binance.com/api/v3/klines?" + urllib.parse.urlencode({
167-        "symbol": symbol,
168:        "interval": source_interval,
169-        "limit": 220
170-    })
171-
172-    try:
173-        rows = http_json(url, timeout=8)
174-    except Exception as e:
175-        return {
176-            "status": "UNAVAILABLE",
--
242-        "value": level,
243-        "level": level,
244-        "source": "quality-live-nmp-wrapper",
245-        "provider": "binance_klines",
246-        "method": "RSI_EXTREME_MOMENTUM_CANDLE_OPEN",
247-        "rule": "NMP = opening price of the momentum candle",
248-        "symbol": symbol,
249-        "timeframe": timeframe,
250:        "source_interval": source_interval,
251-        "direction": direction,
252-        "rsi": round(float(rsi), 4),
253-        "momentum_candle": {
254-            "open_time_ms": candle_time_ms,
255-            "open": opens[idx],
256-            "high": highs[idx],
257-            "low": lows[idx],
258-            "close": closes[idx]
--
264-def enrich_with_nmp(data, symbol, timeframe):
265-    if not isinstance(data, dict):
266-        return data
267-
268-    existing = data.get("nmp")
269-    if isinstance(existing, dict) and existing.get("status") == "AVAILABLE" and existing.get("value") is not None:
270-        return data
271-
272:    nmp = compute_nmp(symbol, _ndsp_nmp_requested_timeframe_v6(data), data)
273-
274-    data["nmp"] = nmp
275-    data["nmp_status"] = nmp.get("status")
276-    data["nmp_level"] = nmp.get("value")
277-    data["nmp_value"] = nmp.get("value")
278-    data["nmp_source"] = nmp.get("source")
279-    data["nmp_timeframe"] = timeframe
280-    # NDSP_V12_SCENARIO_LEVELS_CONTRACT_CALL

== 6) تثبيت الملف المعدل ==
POST_INSTALL_SHA256=bc74d12705dc6d991b9ce5c9a131d1fc173499f89b2a1fc2e46f22b569918907
[OK] TARGET_PYTHON_COMPILE=true

== 7) إعادة تشغيل NMP wrapper ==
[OK] SERVICE_ACTIVE=true
[WAIT] api attempt=1/30 HTTP=000
[OK] API_READY=http://127.0.0.1:9082/health
{
  "ok": true,
  "service": "ndsp-quality-live-nmp-wrapper",
  "port": 9082,
  "upstream": "http://127.0.0.1:9067",
  "updated_at": "2026-07-12T18:58:32+00:00"
}

== 8) اختبار NMP حسب الفريم المطلوب ==

--- TEST DAILY ---
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=daily
HTTP=200
OK=True
INSTRUMENT_TIMEFRAME=daily
SELECTED_TIMEFRAME=daily
NMP_STATUS=AVAILABLE
NMP_TIMEFRAME=1D
NMP_SOURCE_INTERVAL=1d
TOP_NMP_TIMEFRAME=daily
SCENARIO_NMP_TIMEFRAME=daily
NMP_VALUE=3224.99
MOMENTUM_CANDLE=PRESENT
TIMEFRAME_WARNING=None

--- TEST WEEKLY ---
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
HTTP=200
OK=True
INSTRUMENT_TIMEFRAME=weekly
SELECTED_TIMEFRAME=weekly
NMP_STATUS=AVAILABLE
NMP_TIMEFRAME=1W
NMP_SOURCE_INTERVAL=1w
TOP_NMP_TIMEFRAME=weekly
SCENARIO_NMP_TIMEFRAME=weekly
NMP_VALUE=1678.12
MOMENTUM_CANDLE=PRESENT
TIMEFRAME_WARNING=None

--- TEST MONTHLY ---
URL=http://127.0.0.1:9082/api/decision/quality-live?symbol=ETHUSDT&timeframe=monthly
HTTP=200
OK=True
INSTRUMENT_TIMEFRAME=monthly
SELECTED_TIMEFRAME=monthly
NMP_STATUS=AVAILABLE
NMP_TIMEFRAME=1M
NMP_SOURCE_INTERVAL=1M
TOP_NMP_TIMEFRAME=monthly
SCENARIO_NMP_TIMEFRAME=monthly
NMP_VALUE=2007.02
MOMENTUM_CANDLE=PRESENT
TIMEFRAME_WARNING=None

NMP_TIMEFRAME_ERRORS=["daily:TOP_NMP_TIMEFRAME:daily", "daily:SCENARIO_NMP_TIMEFRAME:daily", "weekly:TOP_NMP_TIMEFRAME:weekly", "weekly:SCENARIO_NMP_TIMEFRAME:weekly", "monthly:TOP_NMP_TIMEFRAME:monthly", "monthly:SCENARIO_NMP_TIMEFRAME:monthly"]

============================================================
[ROLLBACK] فشل السكربت عند السطر 954، exit=1
============================================================
[OK] SERVICE_ACTIVE=true
[ROLLBACK] تمت استعادة NMP wrapper.
TARGET=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
BACKUP=/home/nawaf511/ndsp_backend_backups/nmp-requested-timeframe-v6-20260712_205824/ndsp_quality_live_nmp_wrapper.py.before_v6
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_NMP_REQUESTED_TIMEFRAME_V6_20260712_205824.md
FINAL_STATUS=ROLLED_BACK
