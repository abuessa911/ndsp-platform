============================================================
NDSP — Fix instrument.timeframe V2
DATE=2026-07-12T20:33:29+02:00
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
SERVICE=ndsp-live-decision-quality.service
URL=http://127.0.0.1:9057/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V2_20260712_203329.md
============================================================

== 1) فحص الخدمة قبل التعديل ==
PRE_HTTP=200
PRE_INSTRUMENT_TIMEFRAME=UNSPECIFIED
PRE_SELECTED_TIMEFRAME=weekly

== 2) عرض المواضع الحالية ==
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
--
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

== 3) إنشاء النسخة الاحتياطية ==
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v2_20260712_203329

== 4) تعديل جميع المواضع الصحيحة ==
تعذر تحديد متغير الفريم بأمان داخل build_error عند السطر 480

[ROLLBACK] فشل تعديل ملف Python.
[ROLLBACK] تمت استعادة الملف الأصلي.
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_v2_20260712_203329
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_V2_20260712_203329.md
FINAL_STATUS=ROLLED_BACK
