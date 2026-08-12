
==> بيانات العملية
DATE=2026-07-12T20:28:42+02:00
PROJECT_DIR=/home/nawaf511/empire-core-new
PORT=9057
URL=http://127.0.0.1:9057/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_INSTRUMENT_TIMEFRAME_20260712_202842.md

==> فحص الاستجابة الحالية
PRE_HTTP=200
PRE_OK=true
PRE_INSTRUMENT_TIMEFRAME=UNSPECIFIED
PRE_SELECTED_TIMEFRAME=weekly
PRE_SCENARIO_STATE=UNDER_MONITORING

==> اكتشاف عملية خدمة المنفذ 9057
RUNTIME_PID=2612388
RUNTIME_CWD=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality
RUNTIME_CMD=/usr/bin/python3 /home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py 
SYSTEMD_UNIT=ndsp-live-decision-quality.service

==> البحث عن ملف المصدر الذي يبني instrument.timeframe
CANDIDATES:
score=500 matches=2 path=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
score=470 matches=2 path=/home/nawaf511/empire-core-new/backend/_backups/DEV002G_legacy_backend_modules_intake_20260628_003623/backend/ndsp-live-decision-quality/server.py
score=470 matches=2 path=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py

==> عرض المواضع الحالية قبل التعديل
472-    return {
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
488-            "scenario_review_zone": "",
--
581-        return {
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
597-                "scenario_review_zone": fmt_price(review),

==> إنشاء النسخة الاحتياطية
BACKUP=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py.bak.instrument_timeframe_20260712_202842

==> تطبيق تعديل محدود على instrument.timeframe
يوجد أكثر من موضع UNSPECIFIED ولم يمكن تحديد موضع instrument بأمان
