============================================================
NDSP — Timeframe Flow Inspection — READ ONLY
DATE=2026-07-12T20:38:06+02:00
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_INSPECT_TIMEFRAME_FLOW_READONLY_20260712_203806.md
============================================================

== 1) بصمة الملف وحالته ==
  File: /home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
  Size: 36053     	Blocks: 72         IO Block: 4096   regular file
Device: 8,1	Inode: 8651062     Links: 1
Access: (0775/-rwxrwxr-x)  Uid: ( 1000/nawaf511)   Gid: ( 1000/nawaf511)
Access: 2026-07-12 20:33:31.822077971 +0200
Modify: 2026-07-12 20:14:12.871726405 +0200
Change: 2026-07-12 20:33:31.701078462 +0200
 Birth: 2026-07-12 20:14:12.871726405 +0200
e613fa035da4f8088f2afaf90c12659bec9bf9ddeda7da4027ab2ce81782180a  /home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py

== 2) فحص سلامة Python ==
[OK] PYTHON_COMPILE=true

== 3) تعريفات الدوال والمسارات والاستدعاءات ==
### الدوال المهمة
FUNCTION=build_error LINE=470 END_LINE=508 ARGS=(symbol, reason)
SOURCE=def build_error(symbol, reason):
FUNCTION=build_response LINE=510 END_LINE=636 ARGS=(symbol)
SOURCE=def build_response(symbol):
FUNCTION=build_response LINE=984 END_LINE=1045 ARGS=(symbol)
SOURCE=def build_response(symbol):

### مسارات FastAPI التي لها علاقة بالقرار أو الفريم
ROUTE_FUNCTION=build_error LINE=470 END_LINE=508 ARGS=(symbol, reason)
SOURCE=def build_error(symbol, reason):
---
ROUTE_FUNCTION=_ndsp_tf_analyze LINE=716 END_LINE=758 ARGS=(symbol, timeframe)
SOURCE=def _ndsp_tf_analyze(symbol, timeframe):
---
ROUTE_FUNCTION=_ndsp_tf_state_text LINE=817 END_LINE=832 ARGS=(a, timeframe)
SOURCE=def _ndsp_tf_state_text(a, timeframe):
---
ROUTE_FUNCTION=_ndsp_apply_timeframe_response LINE=834 END_LINE=917 ARGS=(base, symbol, timeframe)
SOURCE=def _ndsp_apply_timeframe_response(base, symbol, timeframe):
---
ROUTE_FUNCTION=quality_live LINE=920 END_LINE=923 ARGS=(symbol: str=Query('ETHUSDT'), timeframe: str=Query('weekly'))
DECORATOR=app.get('/api/decision/quality-live')
SOURCE=def quality_live(symbol: str = Query("ETHUSDT"), timeframe: str = Query("weekly")):
---
ROUTE_FUNCTION=health LINE=926 END_LINE=934 ARGS=()
DECORATOR=app.get('/api/decision/quality-live/health')
SOURCE=def health():
---

### جميع استدعاءات build_error وbuild_response
CALL=build_response LINE=921 CALLER=quality_live CALLER_ARGS=(symbol: str=Query('ETHUSDT'), timeframe: str=Query('weekly'))
EXPRESSION=build_response(symbol)
SOURCE=base = build_response(symbol)
---
CALL=build_error LINE=636 CALLER=build_response CALLER_ARGS=(symbol)
EXPRESSION=build_error(s, e)
SOURCE=return build_error(s, e)
---
TOTAL_RELEVANT_CALLS=2

### أسماء متغيرات الفريم الموجودة
LINE=113 NAME=interval CONTEXT=Load
LINE=159 NAME=interval CONTEXT=Load
LINE=162 NAME=interval CONTEXT=Load
LINE=218 NAME=interval CONTEXT=Load
LINE=226 NAME=interval CONTEXT=Load
LINE=227 NAME=interval CONTEXT=Load
LINE=284 NAME=interval CONTEXT=Load
LINE=305 NAME=interval CONTEXT=Load
LINE=644 NAME=tf CONTEXT=Load
LINE=644 NAME=tf CONTEXT=Store
LINE=645 NAME=tf CONTEXT=Load
LINE=647 NAME=tf CONTEXT=Load
LINE=649 NAME=tf CONTEXT=Load
LINE=654 NAME=tf CONTEXT=Load
LINE=654 NAME=tf CONTEXT=Store
LINE=655 NAME=tf CONTEXT=Load
LINE=657 NAME=tf CONTEXT=Load
LINE=662 NAME=tf CONTEXT=Load
LINE=662 NAME=tf CONTEXT=Store
LINE=663 NAME=tf CONTEXT=Load
LINE=665 NAME=tf CONTEXT=Load
LINE=670 NAME=tf CONTEXT=Load
LINE=670 NAME=tf CONTEXT=Store
LINE=671 NAME=tf CONTEXT=Load
LINE=673 NAME=tf CONTEXT=Load
LINE=717 NAME=tf CONTEXT=Store
LINE=717 NAME=timeframe CONTEXT=Load
LINE=718 NAME=tf CONTEXT=Load
LINE=722 NAME=tf CONTEXT=Load
LINE=748 NAME=tf CONTEXT=Load
LINE=818 NAME=timeframe CONTEXT=Load
LINE=836 NAME=tf CONTEXT=Store
LINE=836 NAME=timeframe CONTEXT=Load
LINE=837 NAME=tf CONTEXT=Load
LINE=876 NAME=tf CONTEXT=Load
LINE=896 NAME=tf CONTEXT=Load
LINE=903 NAME=tf CONTEXT=Load
LINE=904 NAME=tf CONTEXT=Load
LINE=912 NAME=tf CONTEXT=Load
LINE=922 NAME=_ndsp_apply_timeframe_response CONTEXT=Load
LINE=922 NAME=timeframe CONTEXT=Load

== 4) الأسطر المحيطة بـ build_error ==
   450	            caution = "لا يوجد اصطفاف كاف بين H1 و4H وD1."
   451	    elif rsi4 >= 58:
   452	        state = "تذبذب بيني · زخم علوي"
   453	        horizon = "مراقبة اختراق"
   454	        caution = "الزخم مرتفع نسبيًا لكن الاتجاه لم يتأكد بعد."
   455	    elif rsi4 <= 42:
   456	        state = "تذبذب بيني · ضغط سفلي"
   457	        horizon = "مراقبة كسر"
   458	        caution = "الزخم منخفض نسبيًا لكن الاتجاه لم يتأكد بعد."
   459	    elif float(atr_pct or 0) >= 2.5:
   460	        state = "تذبذب واسع · مخاطرة أعلى"
   461	        horizon = "مراقبة موسعة"
   462	        caution = "التذبذب مرتفع؛ لا توجد قراءة اتجاهية كافية."
   463	    else:
   464	        state = "تذبذب بيني · قرب المتوسط"
   465	        horizon = "مراقبة توازن"
   466	        caution = "السعر قريب من نطاق التوازن ولا يوجد اصطفاف اتجاهي واضح."
   467	
   468	    return state, horizon, caution
   469	
   470	def build_error(symbol, reason):
   471	    s = clean_symbol(symbol)
   472	    return {
   473	        "ok": True,
   474	        "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
   475	        "project": "NDSP — منصة نواف لدعم القرار",
   476	        "package": "free",
   477	        "instrument": {
   478	            "symbol": s,
   479	            "market": market_type(s).upper(),
   480	            "timeframe": "UNSPECIFIED",
   481	            "live_price": 0,
   482	        },
   483	        "scenario": {
   484	            "scenario_state": "DATA_SOURCE_UNAVAILABLE",
   485	            "scenario_directional_context": "غير معلن",
   486	            "scenario_activation_level": None,
   487	            "scenario_arrival_level": None,
   488	            "scenario_review_zone": "",
   489	            "scenario_invalidation_level": None,
   490	            "scenario_confidence_band": "غير معلن",
   491	            "scenario_time_horizon": "أفق مراقبة",
   492	            "scenario_risk_note": "تعذر جلب السعر الحي من مزود السوق.",
   493	            "scenario_last_updated": now_iso(),
   494	        },
   495	        "allowed_public_outputs": {
   496	            "directional_bias": "غير معلن",
   497	            "reading_horizon": "أفق مراقبة",
   498	            "horizon_strength": "تحتاج تأكيد",
   499	            "market_state": "غير معلن",
   500	            "decision_quality": 50,
   501	            "caution_reason": "تعذر جلب السعر الحي من مزود السوق.",
   502	            "sanitized_summary": "قراءة سياقية صادرة من الباك إند؛ مصدر البيانات غير متصل لهذا الأصل.",
   503	        },
   504	        "live_price_bound": False,
   505	        "data_provider": "unavailable",
   506	        "provider_error": str(reason),
   507	        "generated_at": now_iso(),
   508	    }
   509	
   510	def build_response(symbol):
   511	    s = clean_symbol(symbol)
   512	
   513	    try:
   514	        h1 = analyze_interval(s, "1h")
   515	        h4 = analyze_interval(s, "4h")
   516	        d1 = analyze_interval(s, "1d")
   517	
   518	        provider = h4.get("provider") or h1.get("provider") or "unknown"
   519	
   520	        live_price = h1["close"] or h4["close"]
   521	        momentum_price_4h = h4["momentum_price"]
   522	        momentum_close_time_4h = h4["momentum_close_time"]
   523	
   524	        atr4 = h4["atr"] or (live_price * 0.01)
   525	        rsi4 = h4["rsi"]
   526	
   527	        dirs = [h1["direction"], h4["direction"], d1["direction"]]
   528	        bull = dirs.count("bullish")
   529	        bear = dirs.count("bearish")
   530	
   531	        if bull >= 2:
   532	            direction = "bullish"
   533	        elif bear >= 2:
   534	            direction = "bearish"
   535	        else:
   536	            direction = "neutral"
   537	
   538	        if h1.get("prev_24_close"):
   539	            change_24 = ((live_price - h1["prev_24_close"]) / h1["prev_24_close"]) * 100
   540	        else:
   541	            change_24 = 0.0
   542	
   543	        if direction == "bullish":
   544	            activation = live_price + (atr4 * 0.95)
   545	            arrival = live_price + (atr4 * 1.90)
   546	            review = live_price
   547	            invalidation = live_price - (atr4 * 0.95)
   548	            horizon = "أفق قصير/متوسط"
   549	            caution = "انتظار اختراق التفعيل مع مراقبة التذبذب."
   550	        elif direction == "bearish":
   551	            activation = live_price - (atr4 * 0.95)
   552	            arrival = live_price - (atr4 * 1.90)
   553	            review = live_price
   554	            invalidation = live_price + (atr4 * 0.95)
   555	            horizon = "أفق قصير/متوسط"
   556	            caution = "انتظار كسر التفعيل مع مراقبة التذبذب."
   557	        else:
   558	            activation = live_price + (atr4 * 0.95)
   559	            arrival = live_price + (atr4 * 1.90)
   560	            review = live_price
   561	            invalidation = live_price - (atr4 * 0.95)
   562	            horizon = "أفق مراقبة"
   563	            caution = "انتظار اختراق التفعيل."
   564	
   565	        atr_pct = (atr4 / live_price * 100) if live_price else 0
   566	
   567	        quality = dynamic_quality_score(direction, bull, bear, h1, h4, d1, atr_pct)
   568	        confidence, strength = quality_labels(quality)
   569	
   570	        market_state, horizon, caution = dynamic_decision_texts(

== 5) الأسطر المحيطة بـ build_response ==
   490	            "scenario_confidence_band": "غير معلن",
   491	            "scenario_time_horizon": "أفق مراقبة",
   492	            "scenario_risk_note": "تعذر جلب السعر الحي من مزود السوق.",
   493	            "scenario_last_updated": now_iso(),
   494	        },
   495	        "allowed_public_outputs": {
   496	            "directional_bias": "غير معلن",
   497	            "reading_horizon": "أفق مراقبة",
   498	            "horizon_strength": "تحتاج تأكيد",
   499	            "market_state": "غير معلن",
   500	            "decision_quality": 50,
   501	            "caution_reason": "تعذر جلب السعر الحي من مزود السوق.",
   502	            "sanitized_summary": "قراءة سياقية صادرة من الباك إند؛ مصدر البيانات غير متصل لهذا الأصل.",
   503	        },
   504	        "live_price_bound": False,
   505	        "data_provider": "unavailable",
   506	        "provider_error": str(reason),
   507	        "generated_at": now_iso(),
   508	    }
   509	
   510	def build_response(symbol):
   511	    s = clean_symbol(symbol)
   512	
   513	    try:
   514	        h1 = analyze_interval(s, "1h")
   515	        h4 = analyze_interval(s, "4h")
   516	        d1 = analyze_interval(s, "1d")
   517	
   518	        provider = h4.get("provider") or h1.get("provider") or "unknown"
   519	
   520	        live_price = h1["close"] or h4["close"]
   521	        momentum_price_4h = h4["momentum_price"]
   522	        momentum_close_time_4h = h4["momentum_close_time"]
   523	
   524	        atr4 = h4["atr"] or (live_price * 0.01)
   525	        rsi4 = h4["rsi"]
   526	
   527	        dirs = [h1["direction"], h4["direction"], d1["direction"]]
   528	        bull = dirs.count("bullish")
   529	        bear = dirs.count("bearish")
   530	
   531	        if bull >= 2:
   532	            direction = "bullish"
   533	        elif bear >= 2:
   534	            direction = "bearish"
   535	        else:
   536	            direction = "neutral"
   537	
   538	        if h1.get("prev_24_close"):
   539	            change_24 = ((live_price - h1["prev_24_close"]) / h1["prev_24_close"]) * 100
   540	        else:
   541	            change_24 = 0.0
   542	
   543	        if direction == "bullish":
   544	            activation = live_price + (atr4 * 0.95)
   545	            arrival = live_price + (atr4 * 1.90)
   546	            review = live_price
   547	            invalidation = live_price - (atr4 * 0.95)
   548	            horizon = "أفق قصير/متوسط"
   549	            caution = "انتظار اختراق التفعيل مع مراقبة التذبذب."
   550	        elif direction == "bearish":
   551	            activation = live_price - (atr4 * 0.95)
   552	            arrival = live_price - (atr4 * 1.90)
   553	            review = live_price
   554	            invalidation = live_price + (atr4 * 0.95)
   555	            horizon = "أفق قصير/متوسط"
   556	            caution = "انتظار كسر التفعيل مع مراقبة التذبذب."
   557	        else:
   558	            activation = live_price + (atr4 * 0.95)
   559	            arrival = live_price + (atr4 * 1.90)
   560	            review = live_price
   561	            invalidation = live_price - (atr4 * 0.95)
   562	            horizon = "أفق مراقبة"
   563	            caution = "انتظار اختراق التفعيل."
   564	
   565	        atr_pct = (atr4 / live_price * 100) if live_price else 0
   566	
   567	        quality = dynamic_quality_score(direction, bull, bear, h1, h4, d1, atr_pct)
   568	        confidence, strength = quality_labels(quality)
   569	
   570	        market_state, horizon, caution = dynamic_decision_texts(
   571	            direction, bull, bear, h1, h4, d1, atr_pct, quality
   572	        )
   573	
   574	        summary = (
   575	            f"قراءة سعرية حية على {s}: السعر {fmt_price(live_price)}، "
   576	            f"تغير 24 ساعة {change_24:.3f}%. "
   577	            f"زخم 4H عند سعر {fmt_price(momentum_price_4h)}، "
   578	            f"والسياق {market_state}."
   579	        )
   580	
   581	        return {
   582	            "ok": True,
   583	            "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
   584	            "project": "NDSP — منصة نواف لدعم القرار",
   585	            "package": "free",
   586	            "instrument": {
   587	                "symbol": s,
   588	                "market": market_type(s).upper(),
   589	                "timeframe": "UNSPECIFIED",
   590	                "live_price": live_price,
   591	            },
   592	            "scenario": {
   593	                "scenario_state": "UNDER_MONITORING",
   594	                "scenario_directional_context": market_state,
   595	                "scenario_activation_level": fmt_price(activation),
   596	                "scenario_arrival_level": fmt_price(arrival),
   597	                "scenario_review_zone": fmt_price(review),
   598	                "scenario_invalidation_level": fmt_price(invalidation),
   599	                "scenario_confidence_band": confidence,
   600	                "scenario_time_horizon": horizon,
   601	                "scenario_risk_note": caution,
   602	                "scenario_last_updated": now_iso(),
   603	            },
   604	            "allowed_public_outputs": {
   605	                "directional_bias": market_state,
   606	                "reading_horizon": horizon,
   607	                "horizon_strength": strength,
   608	                "market_state": market_state,
   609	                "decision_quality": quality,
   610	                "caution_reason": caution,
   611	                "sanitized_summary": summary,
   612	            },
   613	            "live_market_analysis": {
   614	                "provider": provider,
   615	                "price": live_price,
   616	                "price_change_24h_pct": change_24,
   617	                "atr_4h": atr4,
   618	                "atr_4h_pct": atr_pct,
   619	                "rsi_4h": rsi4,
   620	                "momentum_price_4h": momentum_price_4h,
   621	                "momentum_close_time_4h": momentum_close_time_4h,
   622	                "direction": direction,
   623	                "market_state": market_state,
   624	                "horizon_strength": strength,
   625	                "confidence_band": confidence,
   626	                "h1_direction": h1["direction"],
   627	                "h4_direction": h4["direction"],
   628	                "d1_direction": d1["direction"],
   629	            },
   630	            "live_price_bound": True,
   631	            "data_provider": provider,
   632	            "generated_at": now_iso(),
   633	        }
   634	
   635	    except Exception as e:
   636	        return build_error(s, e)
   637	
   638	
   639	# NDSP_ASSET_TIMEFRAME_READING_V27
   640	# Adds timeframe-specific reading for Asset View.
   641	# Supported: daily / weekly / monthly.
   642	# Keeps the old endpoint compatible when timeframe is omitted.
   643	def _ndsp_tf_norm(tf):
   644	    tf = str(tf or "weekly").strip().lower()
   645	    if tf in ("1d", "d", "day", "daily", "يومي"):
   646	        return "daily"
   647	    if tf in ("1w", "w", "week", "weekly", "اسبوعي", "أسبوعي"):
   648	        return "weekly"
   649	    if tf in ("1m", "m", "month", "monthly", "شهري"):
   650	        return "monthly"
   651	    return "weekly"
   652	
   653	def _ndsp_tf_label(tf):
   654	    tf = _ndsp_tf_norm(tf)
   655	    if tf == "daily":
   656	        return "يومي"
   657	    if tf == "monthly":
   658	        return "شهري"
   659	    return "أسبوعي"
   660	
   661	def _ndsp_tf_horizon(tf):
   662	    tf = _ndsp_tf_norm(tf)
   663	    if tf == "daily":
   664	        return "أفق يومي"
   665	    if tf == "monthly":
   666	        return "أفق شهري"
   667	    return "أفق أسبوعي"
   668	
   669	def _ndsp_tf_group(tf):
   670	    tf = _ndsp_tf_norm(tf)
   671	    if tf == "daily":
   672	        return 1
   673	    if tf == "monthly":
   674	        return 21
   675	    return 5
   676	
   677	def _ndsp_tf_aggregate(k, group):
   678	    if group <= 1:
   679	        return k
   680	
   681	    highs = k.get("highs") or []
   682	    lows = k.get("lows") or []
   683	    closes = k.get("closes") or []
   684	    vols = k.get("vols") or []
   685	    times = k.get("close_times") or []
   686	
   687	    n = len(closes)
   688	    if n < group:
   689	        return k
   690	

== 6) كل الأسطر المتعلقة بالمسار والفريم ==
470:def build_error(symbol, reason):
480:            "timeframe": "UNSPECIFIED",
510:def build_response(symbol):
589:                "timeframe": "UNSPECIFIED",
636:        return build_error(s, e)
640:# Adds timeframe-specific reading for Asset View.
642:# Keeps the old endpoint compatible when timeframe is omitted.
716:def _ndsp_tf_analyze(symbol, timeframe):
717:    tf = _ndsp_tf_norm(timeframe)
817:def _ndsp_tf_state_text(a, timeframe):
818:    tf_label = _ndsp_tf_label(timeframe)
834:def _ndsp_apply_timeframe_response(base, symbol, timeframe):
836:        tf = _ndsp_tf_norm(timeframe)
903:        la["selected_timeframe"] = tf
904:        la["selected_timeframe_label"] = _ndsp_tf_label(tf)
905:        la["selected_timeframe_close"] = a.get("close")
906:        la["selected_timeframe_rsi"] = a.get("rsi")
907:        la["selected_timeframe_atr"] = a.get("atr")
908:        la["selected_timeframe_direction"] = direction
909:        la["timeframe_model"] = "asset_view_timeframe_v27"
910:        la["scenario_levels_model"] = "timeframe_atr_ema_v27"
912:        base["source_mode"] = str(base.get("source_mode", "")) + f" + asset_timeframe_{tf}_v27"
915:        base["timeframe_warning"] = str(e)
919:@app.get("/api/decision/quality-live")
920:def quality_live(symbol: str = Query("ETHUSDT"), timeframe: str = Query("weekly")):
921:    base = build_response(symbol)
922:    base = _ndsp_apply_timeframe_response(base, symbol, timeframe)
925:@app.get("/api/decision/quality-live/health")
939:if "_ndsp_original_build_response_backend_levels_safe" not in globals():
940:    _ndsp_original_build_response_backend_levels_safe = build_response
984:    def build_response(symbol):
985:        base = _ndsp_original_build_response_backend_levels_safe(symbol)

============================================================
[OK] انتهى الفحص دون تعديل أي ملف
TARGET=/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_INSPECT_TIMEFRAME_FLOW_READONLY_20260712_203806.md
FINAL_STATUS=READ_ONLY_INSPECTION_OK
============================================================
