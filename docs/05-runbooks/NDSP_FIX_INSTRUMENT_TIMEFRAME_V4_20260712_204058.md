============================================================
NDSP — Fix instrument.timeframe V4
DATE=2026-07-12T20:40:58+02:00
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
SERVICE=ndsp-live-decision-quality.service
PORT=9057
SYMBOL=ETHUSDT
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V4_20260712_204058.md
============================================================

== 1) فحص الخدمة والملف قبل التعديل ==
PRE_SHA256=e613fa035da4f8088f2afaf90c12659bec9bf9ddeda7da4027ab2ce81782180a
[OK] SERVICE_ACTIVE=true
[OK] PRE_PYTHON_COMPILE=true

== 2) فحص عقد API قبل التعديل ==
PRE_HTTP=200
PRE_OK=true
PRE_INSTRUMENT_TIMEFRAME=UNSPECIFIED
PRE_SELECTED_TIMEFRAME=weekly
PRE_SCENARIO_STATE=UNDER_MONITORING

== 3) التحقق من نقطة التصحيح الصحيحة ==
FUNCTION_COUNT=1
FUNCTION_LINE=834
FUNCTION_END_LINE=917
FUNCTION_ARGUMENTS=base,symbol,timeframe
NORMALIZATION_LINES=836

== 4) عرض الدالة قبل التعديل ==
   831	
   832	    return f"قراءة {tf_label} · توازن", f"مراقبة {tf_label}", "السعر داخل نطاق توازن؛ لا توجد قراءة اتجاهية كافية."
   833	
   834	def _ndsp_apply_timeframe_response(base, symbol, timeframe):
   835	    try:
   836	        tf = _ndsp_tf_norm(timeframe)
   837	        a = _ndsp_tf_analyze(symbol, tf)
   838	
   839	        instrument = base.setdefault("instrument", {})
   840	        live_price = _ndsp_tf_float(instrument.get("live_price"))
   841	        if live_price is None or live_price <= 0:
   842	            live_price = _ndsp_tf_float(a.get("close")) or 0
   843	
   844	        atr_v = _ndsp_tf_float(a.get("atr")) or (live_price * 0.01)
   845	        if atr_v <= 0:
   846	            atr_v = live_price * 0.01
   847	
   848	        direction = a.get("direction") or "neutral"
   849	        rsi_v = float(a.get("rsi") or 50)
   850	
   851	        # المستويات مبنية على السعر الحي لكن بسعة ATR للإطار المختار.
   852	        if direction == "bullish":
   853	            activation = live_price + (atr_v * 0.55)
   854	            arrival = live_price + (atr_v * 1.35)
   855	            review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.30)
   856	            invalidation = live_price - (atr_v * 0.95)
   857	        elif direction == "bearish":
   858	            activation = live_price - (atr_v * 0.55)
   859	            arrival = live_price - (atr_v * 1.35)
   860	            review = _ndsp_tf_float(a.get("ema20")) or (live_price + atr_v * 0.30)
   861	            invalidation = live_price + (atr_v * 0.95)
   862	        else:
   863	            if rsi_v >= 50:
   864	                activation = live_price + (atr_v * 0.55)
   865	                arrival = live_price + (atr_v * 1.25)
   866	                review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.25)
   867	                invalidation = live_price - (atr_v * 0.85)
   868	            else:
   869	                activation = live_price - (atr_v * 0.55)

== 5) إنشاء النسخة الاحتياطية ==
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v4_20260712_204058

== 6) تطبيق التصحيح النهائي في طبقة الفريم ==
PATCH_STATE=INSERTED
PATCH_AFTER_LINE=836
PATCH_MARKER=NDSP_INSTRUMENT_TIMEFRAME_CONTRACT_V4

== 7) التحقق الساكن من التصحيح ==
MARKER_COUNT=1
ASSIGNMENT_COUNT=1
POST_PATCH_SHA256=abcf5c95d5eccc7924b030b42023fc2aba238ee329fd34a1d262ce505859b960
[OK] PYTHON_COMPILE=true

== 8) عرض الدالة بعد التعديل ==
   831	
   832	    return f"قراءة {tf_label} · توازن", f"مراقبة {tf_label}", "السعر داخل نطاق توازن؛ لا توجد قراءة اتجاهية كافية."
   833	
   834	def _ndsp_apply_timeframe_response(base, symbol, timeframe):
   835	    try:
   836	        tf = _ndsp_tf_norm(timeframe)
   837	        # NDSP_INSTRUMENT_TIMEFRAME_CONTRACT_V4
   838	        _ndsp_instrument = base.get("instrument")
   839	        if not isinstance(_ndsp_instrument, dict):
   840	            _ndsp_instrument = {}
   841	            base["instrument"] = _ndsp_instrument
   842	        _ndsp_instrument["timeframe"] = tf
   843	        a = _ndsp_tf_analyze(symbol, tf)
   844	
   845	        instrument = base.setdefault("instrument", {})
   846	        live_price = _ndsp_tf_float(instrument.get("live_price"))
   847	        if live_price is None or live_price <= 0:
   848	            live_price = _ndsp_tf_float(a.get("close")) or 0
   849	
   850	        atr_v = _ndsp_tf_float(a.get("atr")) or (live_price * 0.01)
   851	        if atr_v <= 0:
   852	            atr_v = live_price * 0.01
   853	
   854	        direction = a.get("direction") or "neutral"
   855	        rsi_v = float(a.get("rsi") or 50)
   856	
   857	        # المستويات مبنية على السعر الحي لكن بسعة ATR للإطار المختار.
   858	        if direction == "bullish":
   859	            activation = live_price + (atr_v * 0.55)
   860	            arrival = live_price + (atr_v * 1.35)
   861	            review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.30)
   862	            invalidation = live_price - (atr_v * 0.95)
   863	        elif direction == "bearish":
   864	            activation = live_price - (atr_v * 0.55)
   865	            arrival = live_price - (atr_v * 1.35)
   866	            review = _ndsp_tf_float(a.get("ema20")) or (live_price + atr_v * 0.30)
   867	            invalidation = live_price + (atr_v * 0.95)
   868	        else:
   869	            if rsi_v >= 50:
   870	                activation = live_price + (atr_v * 0.55)
   871	                arrival = live_price + (atr_v * 1.25)
   872	                review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.25)
   873	                invalidation = live_price - (atr_v * 0.85)
   874	            else:
   875	                activation = live_price - (atr_v * 0.55)
   876	                arrival = live_price - (atr_v * 1.25)
   877	                review = _ndsp_tf_float(a.get("ema20")) or (live_price + atr_v * 0.25)

== 9) إعادة تشغيل الخدمة ==
[OK] SERVICE_ACTIVE_AFTER_RESTART=true

== 10) انتظار عودة API ==
[OK] API_RETURNED=true

== 11) اختبار عقد الفريمات ==

--- TIMEFRAME TEST ---
REQUESTED=daily
EXPECTED=daily
HTTP=200
OK=true
INSTRUMENT_TIMEFRAME=daily
SELECTED_TIMEFRAME=daily
SCENARIO_STATE=UNDER_MONITORING
TIMEFRAME_WARNING=NONE
[OK] CONTRACT_TIMEFRAME=daily

--- TIMEFRAME TEST ---
REQUESTED=weekly
EXPECTED=weekly
HTTP=200
OK=true
INSTRUMENT_TIMEFRAME=weekly
SELECTED_TIMEFRAME=weekly
SCENARIO_STATE=UNDER_MONITORING
TIMEFRAME_WARNING=NONE
[OK] CONTRACT_TIMEFRAME=weekly

--- TIMEFRAME TEST ---
REQUESTED=monthly
EXPECTED=monthly
HTTP=200
OK=true
INSTRUMENT_TIMEFRAME=monthly
SELECTED_TIMEFRAME=monthly
SCENARIO_STATE=UNDER_MONITORING
TIMEFRAME_WARNING=NONE
[OK] CONTRACT_TIMEFRAME=monthly

== 12) عرض الاستجابة الأسبوعية النهائية ==
{
  "ok": true,
  "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27",
  "project": "NDSP — منصة نواف لدعم القرار",
  "package": "free",
  "instrument": {
    "symbol": "ETHUSDT",
    "market": "CRYPTO",
    "timeframe": "weekly",
    "live_price": 1818.5
  },
  "scenario": {
    "scenario_state": null,
    "scenario_directional_context": null,
    "scenario_activation_level": null,
    "scenario_arrival_level": null,
    "scenario_review_zone": null,
    "scenario_invalidation_level": null,
    "scenario_confidence_band": null,
    "scenario_time_horizon": null,
    "scenario_risk_note": null
  },
  "timeframe_check": {
    "instrument_timeframe": "weekly",
    "selected_timeframe": "weekly",
    "selected_timeframe_label": "أسبوعي",
    "selected_timeframe_direction": "bearish"
  },
  "live_price_bound": true,
  "data_provider": "binance",
  "generated_at": "2026-07-12T18:41:15Z"
}

== 13) تشغيل فحص الحوكمة السابق ==
============================================================
NDSP — Weekly Quality Live Contract Check
URL: http://127.0.0.1:9057/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
DATE: 2026-07-12T20:41:16+02:00
============================================================

HTTP_CODE=200

== Contract Summary ==
{
  "ok": true,
  "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27",
  "project": "NDSP — منصة نواف لدعم القرار",
  "package": "free",
  "instrument": {
    "symbol": "ETHUSDT",
    "market": "CRYPTO",
    "timeframe": "weekly",
    "live_price": 1818.5
  },
  "scenario": {
    "scenario_state": "UNDER_MONITORING",
    "scenario_directional_context": "قراءة أسبوعي · ضغط هابط",
    "scenario_activation_level": "1,718.48",
    "scenario_arrival_level": "1,572.99",
    "scenario_review_zone": "1,944.29",
    "scenario_invalidation_level": "1,991.27",
    "scenario_confidence_band": "عالية جدًا",
    "scenario_time_horizon": "متابعة كسر أسبوعي",
    "scenario_risk_note": "انتظار ثبات السعر دون منطقة المراجعة.",
    "scenario_last_updated": "2026-07-12T18:41:17Z"
  },
  "allowed_public_outputs": {
    "directional_bias": "قراءة أسبوعي · ضغط هابط",
    "reading_horizon": "متابعة كسر أسبوعي",
    "horizon_strength": "عالية جدًا",
    "market_state": "قراءة أسبوعي · ضغط هابط",
    "decision_quality": 86,
    "caution_reason": "انتظار ثبات السعر دون منطقة المراجعة.",
    "sanitized_summary": "قراءة أسبوعي على ETHUSDT: السعر 1,818.50، جودة القراءة 86، الحالة قراءة أسبوعي · ضغط هابط."
  },
  "timeframe_check": {
    "requested_timeframe": "weekly",
    "instrument_timeframe": "weekly",
    "selected_timeframe": "weekly",
    "selected_timeframe_label": "أسبوعي",
    "selected_timeframe_direction": "bearish"
  },
  "market_alignment": {
    "h1_direction": "bullish",
    "h4_direction": "bullish",
    "d1_direction": "neutral",
    "weekly_direction": "bearish"
  },
  "generated_at": "2026-07-12T18:41:17Z",
  "data_provider": "binance",
  "live_price_bound": true
}

== Governance Checks ==
[OK] API response reports ok=true
[OK] Calculation timeframe is weekly
[OK] instrument.timeframe is weekly
[OK] Live price is bound to the decision
[OK] Data provider is Binance
[INFO] scenario_state=UNDER_MONITORING
[INFO] live_price=1818.5
[INFO] activation_level=1,718.48
[INFO] decision_quality=86

FINAL_STATUS=OK

============================================================
[OK] تم إصلاح عقد instrument.timeframe من طبقة الفريم
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v4_20260712_204058
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V4_20260712_204058.md
FINAL_STATUS=FIXED
============================================================
