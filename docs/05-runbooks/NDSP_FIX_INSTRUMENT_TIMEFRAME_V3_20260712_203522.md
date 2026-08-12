============================================================
NDSP — Fix instrument.timeframe V3
DATE=2026-07-12T20:35:22+02:00
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
SERVICE=ndsp-live-decision-quality.service
URL=http://127.0.0.1:9057/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V3_20260712_203522.md
============================================================

== 1) فحص الخدمة وعقد API قبل التعديل ==
PRE_HTTP=200
PRE_OK=true
PRE_INSTRUMENT_TIMEFRAME=UNSPECIFIED
PRE_SELECTED_TIMEFRAME=weekly
PRE_SCENARIO_STATE=UNDER_MONITORING

== 2) تحليل النطاقات البرمجية قبل التعديل ==
INSTRUMENT_TARGET_COUNT=2
TARGET_1_LINE=480 SCOPES=build_error(symbol,reason)
TARGET_2_LINE=589 SCOPES=build_response(symbol)

== 3) عرض موضعي instrument.timeframe ==
473-        "ok": True,
474-        "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
475-        "project": "NDSP — منصة نواف لدعم القرار",
476-        "package": "free",
477-        "instrument": {
478-            "symbol": s,
479-            "market": market_type(s).upper(),
480:            "timeframe": "UNSPECIFIED",
481-            "live_price": 0,
482-        },
483-        "scenario": {
484-            "scenario_state": "DATA_SOURCE_UNAVAILABLE",
485-            "scenario_directional_context": "غير معلن",
486-            "scenario_activation_level": None,
487-            "scenario_arrival_level": None,
--
582-            "ok": True,
583-            "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
584-            "project": "NDSP — منصة نواف لدعم القرار",
585-            "package": "free",
586-            "instrument": {
587-                "symbol": s,
588-                "market": market_type(s).upper(),
589:                "timeframe": "UNSPECIFIED",
590-                "live_price": live_price,
591-            },
592-            "scenario": {
593-                "scenario_state": "UNDER_MONITORING",
594-                "scenario_directional_context": market_state,
595-                "scenario_activation_level": fmt_price(activation),
596-                "scenario_arrival_level": fmt_price(arrival),

== 4) إنشاء النسخة الاحتياطية ==
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v3_20260712_203522

== 5) تطبيق التصحيح مع دعم النطاق الأبوي ==
تعذر العثور على متغير فريم في النطاق المحلي أو الأبوي عند السطر 480. scopes=build_error

============================================================
[ROLLBACK] فشل تحليل أو تعديل ملف Python
============================================================
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v3_20260712_203522
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V3_20260712_203522.md
FINAL_STATUS=ROLLED_BACK
