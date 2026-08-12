# NDSP Command Center / Radar Preflight
DATE=2026-07-07T09:52:05+02:00
FRONTEND=/var/www/ndsp-my

## 1) Target files
--- /var/www/ndsp-my/NDSP_Command_Center.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 3.3K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Command_Center.html

--- /var/www/ndsp-my/decision-radar.html ---
-rw-rw-r-- 1 nawaf511 nawaf511 3.2K يوليو   7 09:48 /var/www/ndsp-my/decision-radar.html

--- /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js ---
-rw-rw-r-- 1 nawaf511 nawaf511 3.6K يوليو   5 18:54 /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js

--- /var/www/ndsp-my/assets/premium.js ---
-rw-rw-r-- 1 nawaf511 nawaf511 40K يوليو   5 18:01 /var/www/ndsp-my/assets/premium.js

--- /var/www/ndsp-my/assets/ndsp-global-menu.js ---
-rw-rw-r-- 1 nawaf511 nawaf511 11K يوليو   7 09:48 /var/www/ndsp-my/assets/ndsp-global-menu.js

--- /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js ---
-rw-rw-r-- 1 nawaf511 nawaf511 500 يوليو   7 09:42 /var/www/ndsp-my/assets/ndsp-disclaimer-gate.js

## 2) Command Center markers
1:<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#040405"><title>NDSP — مركز القيادة</title><link rel="stylesheet" href="/assets/premium.css?v=22-restore-radar">  <link rel="stylesheet" href="/assets/ndsp-radar-safe-clean.css?v=23">
2:  <link rel="stylesheet" href="/assets/ndsp-global-menu.css?v=24-page-match">
4:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
5:  <!-- NDSP_CANONICAL_PAGE_ALIAS_V1 source=decision-radar.html -->
6:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>مركز القيادة</h1><p>رادار فخم يتلون حسب حالة الأصل.</p></section><section class="radar-layout"><div class="radar-box"><div class="radar"><div class="core"><span data-live-state>Loading</span></div><div class="node n1">TDL</div><div class="node n2">NMP</div><div class="node n3">USD Macro</div><div class="node n4">Risk</div><div class="node n5">Devil Gate</div><div class="node n6">Hidden Consensus</div></div><div class="notice">الأصل: <b data-selected-symbol>ETHUSDT</b> — السعر: <b data-live-price>تحميل</b></div></div><div class="brief-box"><h2>Premium Decision Radar</h2><div class="brief-grid"><article class="card"><h3>Decision Core</h3><span data-live-state>تحميل</span></article><article class="card"><h3>Decision Quality</h3><span>مؤشر جودة القرار.</span></article><article class="card"><h3>Devil’s Advocate</h3><span>الطبقة الوحيدة التي يسمح لها بالمنع.</span></article><article class="card"><h3>Scenario Levels</h3><span>Activation / Arrival / Review / Invalidation</span></article></div><div class="notice">قراءة JSON الحية:</div><pre data-live-json>تحميل...</pre></div></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>  <script src="/assets/ndsp-radar-safe-clean.js?v=23"></script>
7:  <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>

## 3) Radar JS markers
7:    return location.pathname.indexOf("decision-radar") !== -1;
24:      text.indexOf('"scenario_state"') !== -1 ||
25:      text.indexOf('"scenario_activation_level"') !== -1 ||
56:    card.className = "ndsp-radar-safe-json-card-v23";
97:        panel.classList.add("ndsp-radar-json-panel-cleaned-v23");
103:    document.documentElement.setAttribute("data-ndsp-radar-json-clean", "v23");

## 4) Premium JS markers
7:function radarState(v){v=String(v||"").toUpperCase();if(v.includes("ALLOWED"))return"allowed";if(v.includes("CAUTION"))return"caution";if(v.includes("BLOCK"))return"blocked";return"watch"}
8:function nav(){let n=[["asset-selector.html","الأسواق والأصول"],["decision-radar.html?symbol="+selectedSymbol,"الرادار"],["decision-center.html?symbol="+selectedSymbol,"مركز القرار"],["completed-decisions.html","سجل القرار"],["decision-guide.html","الدليل"],["user-guide.html","أنماط المستخدم"],["settings.html","الإعدادات"]].map(x=>`<a href="/${x[0]}"><span>${x[1]}</span><small>›</small></a>`).join("");document.querySelectorAll("[data-nav]").forEach(e=>e.innerHTML=n)}
9:async function assets(){return await(await fetch("/assets/ndsp-assets.json",{cache:"no-store"})).json()}
10:function paintRadar(raw){let r=document.querySelector(".radar");if(!r)return;let st=radarState(raw||document.querySelector("[data-live-state]")?.textContent||decisionFor(selectedSymbol));r.classList.remove("state-allowed","state-caution","state-blocked","state-watch");r.classList.add("state-"+st);document.documentElement.setAttribute("data-ndsp-radar-state",st)}
12:let tb=document.querySelector("[data-assets-body]");if(tb){tb.innerHTML=a.map(x=>{let q=scoreFor(x.symbol),d=decisionFor(x.symbol),dev=scoreFor(x.symbol+"devil")>82?"BLOCK":"PASS";return`<tr data-market="${x.market}" data-search="${x.symbol} ${x.name} ${x.market}"><td><b>${x.symbol}</b><br><span style="color:rgba(244,239,228,.55)">${x.name}</span></td><td>${marketNames[x.market]||x.market}</td><td>Live</td><td><span class="badge ${cls(d)}">${d}</span></td><td>${["Activation","Arrival","Review","Invalidation","Monitoring"][scoreFor(x.symbol+"s")%5]}</td><td><b>${q}%</b></td><td>${scoreFor(x.symbol+"n")>70?"قريب":"مراقبة"}</td><td>${scoreFor(x.symbol+"u")>70?"ضغط":"محايد"}</td><td><span class="badge ${dev==="BLOCK"?"block":"ok"}">${dev}</span></td><td>Hidden ${Math.min(96,q+3)}%</td><td><a class="btn" href="/decision-radar.html?symbol=${x.symbol}">فتح الرادار</a></td></tr>`}).join("");document.querySelector("[data-count-assets]")&&(document.querySelector("[data-count-assets]").textContent=a.length);document.querySelector("[data-hidden-avg]")&&(document.querySelector("[data-hidden-avg]").textContent=Math.round(a.reduce((s,x)=>s+scoreFor(x.symbol+"h"),0)/a.length)+"%")}}
13:document.addEventListener("click",e=>{let p=e.target.closest("[data-market]");if(p){document.querySelectorAll("[data-market]").forEach(x=>x.classList.remove("active"));p.classList.add("active");let active=p.dataset.market;document.querySelectorAll("tbody tr").forEach(tr=>tr.classList.toggle("hidden",!(active==="ALL"||tr.dataset.market===active)))}})
14:async function live(){document.querySelectorAll("[data-selected-symbol]").forEach(e=>e.textContent=selectedSymbol);let d=decisionFor(selectedSymbol);document.querySelectorAll("[data-live-state]").forEach(e=>e.textContent=d);paintRadar(d);let box=document.querySelector("[data-live-json]");try{let r=await fetch("/api/decision/quality-live?symbol="+encodeURIComponent(selectedSymbol),{cache:"no-store"});if(r.ok){let j=await r.json();box&&(box.textContent=JSON.stringify(j,null,2));let state=j?.scenario?.scenario_state||j?.scenario_state||d;document.querySelectorAll("[data-live-state]").forEach(e=>e.textContent=state);document.querySelectorAll("[data-live-price]").forEach(e=>e.textContent=j?.instrument?.live_price||j?.live_price||"متصل");paintRadar(state);return}}catch(e){}box&&(box.textContent="الواجهة تعمل. لم تصل قراءة JSON حية لهذا الأصل الآن.")}
33:    var radar = document.querySelector(".radar");
34:    if(!radar) return;
40:    radar.classList.remove("state-allowed","state-caution","state-blocked","state-watch","devil-block");
41:    radar.classList.add("state-" + state);
45:      radar.classList.add("devil-block");
48:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
118:    var radar = document.querySelector(".radar");
119:    if(!radar) return;
121:    var stateEl = document.querySelector("[data-live-state]") || radar.querySelector(".core");
126:    radar.classList.remove("state-allowed","state-caution","state-blocked","state-watch","devil-block");
127:    radar.classList.add("state-" + state);
131:      radar.classList.add("devil-block");
134:    var core = radar.querySelector(".core");
143:    var existingLegend = document.querySelector(".ndsp-radar-legend");
146:      legend.className = "ndsp-radar-legend";
152:      radar.insertAdjacentElement("afterend", legend);
155:    var existingMeta = document.querySelector(".ndsp-radar-meta");
158:      meta.className = "ndsp-radar-meta";
161:      var anchor = document.querySelector(".ndsp-radar-legend") || radar;
165:    document.documentElement.setAttribute("data-ndsp-luxury-gold-radar", "v5");
166:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
214:    var radar = document.querySelector(".radar");
215:    if(!radar) return;
217:    document.querySelectorAll(".ndsp-radar-legend,.ndsp-radar-meta").forEach(function(x){ x.remove(); });
219:    var stateEl = document.querySelector("[data-live-state]") || radar.querySelector(".core");
224:    radar.classList.remove("state-allowed","state-caution","state-blocked","state-watch","state-unknown","devil-block");
225:    radar.classList.add("state-" + state);
229:      radar.classList.add("devil-block");
232:    var core = radar.querySelector(".core");
243:    legend.className = "ndsp-radar-legend";
249:    radar.insertAdjacentElement("afterend", legend);
252:    meta.className = "ndsp-radar-meta";
257:    document.documentElement.setAttribute("data-ndsp-luxury-gold-radar", "v6");
258:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
307:    var box = document.querySelector(".radar-box");
312:    var old = box.querySelector(".ndsp-pro-radar-wrap");
322:    wrap.className = "ndsp-pro-radar-wrap";
324:      '<div class="ndsp-pro-radar" data-state="'+state+'">' +
334:        '<div class="ndsp-pro-node node-hidden">Hidden<br>Consensus<span class="mini"></span><span class="ico">●●</span></div>' +
336:        '<div class="ndsp-pro-node node-nmp">NMP<span class="mini"></span><span class="ico">⌁</span></div>' +
350:    document.documentElement.setAttribute("data-ndsp-radar-pro-exact", "v7");
351:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
397:<svg viewBox="0 0 460 460" aria-hidden="true">
447:    var box = document.querySelector(".radar-box");
463:      <div class="ndsp-svg-v8-radar" data-state="${state}">
473:        <div class="ndsp-svg-v8-node hidden">Hidden<br>Consensus<span class="bar"></span><span class="ico">●●</span></div>
475:        <div class="ndsp-svg-v8-node nmp">NMP<span class="bar"></span><span class="ico">⌁</span></div>
489:    document.documentElement.setAttribute("data-ndsp-radar-svg-pro", "v8");
490:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
535:<svg viewBox="0 0 460 460" aria-hidden="true">
588:    var box = document.querySelector(".radar-box");
607:      <div class="ndsp-svg-v9-radar" data-state="${state}">
617:        <div class="ndsp-svg-v9-node hidden">Hidden<br>Consensus<span class="bar"></span><span class="ico">●●</span></div>
619:        <div class="ndsp-svg-v9-node nmp">NMP<span class="bar"></span><span class="ico">⌁</span></div>
633:    document.documentElement.setAttribute("data-ndsp-radar-svg-art", "v9");
634:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
657:  var BASE = "/assets/radar-art/radar-base-gold.svg";
659:    allowed: "/assets/radar-art/radar-overlay-allowed.svg",
660:    caution: "/assets/radar-art/radar-overlay-caution.svg",
661:    blocked: "/assets/radar-art/radar-overlay-blocked.svg",
662:    monitoring: "/assets/radar-art/radar-overlay-monitoring.svg",
663:    unknown: "/assets/radar-art/radar-overlay-caution.svg"
689:    var box = document.querySelector(".radar-box");
704:      '<div class="ndsp-art-radar" data-state="'+state+'">' +
724:    document.documentElement.setAttribute("data-ndsp-image-backed-radar", VERSION);
725:    document.documentElement.setAttribute("data-ndsp-radar-state", state);
747:  var ASSET = "/assets/radar-art/ndsp-radar-reference-exact.webp";
760:    var box = document.querySelector(".radar-box");
780:    document.documentElement.setAttribute("data-ndsp-exact-reference-radar", "v11");
781:    document.documentElement.setAttribute("data-ndsp-radar-state", state);

## 5) API sample
{
    "ok": true,
    "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality + backend_only_dynamic_levels_safe + asset_timeframe_weekly_v27",
    "project": "NDSP \u2014 \u0645\u0646\u0635\u0629 \u0646\u0648\u0627\u0641 \u0644\u062f\u0639\u0645 \u0627\u0644\u0642\u0631\u0627\u0631",
    "package": "free",
    "instrument": {
        "symbol": "ETHUSDT",
        "market": "CRYPTO",
        "timeframe": "UNSPECIFIED",
        "live_price": 1779.11
    },
    "scenario": {
        "scenario_state": "UNDER_MONITORING",
        "scenario_directional_context": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637",
        "scenario_activation_level": "1,678.69",
        "scenario_arrival_level": "1,532.63",
        "scenario_review_zone": "1,960.54",
        "scenario_invalidation_level": "1,952.56",
        "scenario_confidence_band": "\u0639\u0627\u0644\u064a\u0629 \u062c\u062f\u064b\u0627",
        "scenario_time_horizon": "\u0645\u062a\u0627\u0628\u0639\u0629 \u0643\u0633\u0631 \u0623\u0633\u0628\u0648\u0639\u064a",
        "scenario_risk_note": "\u0627\u0646\u062a\u0638\u0627\u0631 \u062b\u0628\u0627\u062a \u0627\u0644\u0633\u0639\u0631 \u062f\u0648\u0646 \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629.",
        "scenario_last_updated": "2026-07-07T07:52:06Z",
        "nmp_status": "AVAILABLE",
        "nmp_level": 1583.4,
        "nmp_source": "quality-live-nmp-wrapper",
        "nmp_timeframe": "1D"
    },
    "allowed_public_outputs": {
        "directional_bias": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637",
        "reading_horizon": "\u0645\u062a\u0627\u0628\u0639\u0629 \u0643\u0633\u0631 \u0623\u0633\u0628\u0648\u0639\u064a",
        "horizon_strength": "\u0639\u0627\u0644\u064a\u0629 \u062c\u062f\u064b\u0627",
        "market_state": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637",
        "decision_quality": 86,
        "caution_reason": "\u0627\u0646\u062a\u0638\u0627\u0631 \u062b\u0628\u0627\u062a \u0627\u0644\u0633\u0639\u0631 \u062f\u0648\u0646 \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629.",
        "sanitized_summary": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u0639\u0644\u0649 ETHUSDT: \u0627\u0644\u0633\u0639\u0631 1,779.11\u060c \u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0621\u0629 86\u060c \u0627\u0644\u062d\u0627\u0644\u0629 \u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637.",
        "nmp_status": "AVAILABLE",
        "nmp_level": 1583.4,
        "nmp_note": "NMP \u0645\u062d\u0633\u0648\u0628 \u0641\u064a \u0627\u0644\u0628\u0627\u0643 \u0625\u0646\u062f \u0645\u0646 \u0634\u0645\u0639\u0629 \u0627\u0644\u0632\u062e\u0645\u060c \u0648\u0644\u064a\u0633 \u0645\u0646 \u0627\u0644\u0648\u0627\u062c\u0647\u0629."
    },
    "live_market_analysis": {
        "provider": "binance",
        "price": 1779.11,
        "price_change_24h_pct": 0.5357052039126705,
        "atr_4h": 28.891428571428587,
        "atr_4h_pct": 1.6239259276508249,
        "rsi_4h": 43.717138299757785,
        "momentum_price_4h": 1771.56,
        "momentum_close_time_4h": 1783396799999,
        "direction": "neutral",
        "market_state": "\u062a\u0630\u0628\u0630\u0628 \u0628\u064a\u0646\u064a \u00b7 \u0642\u0631\u0628 \u0627\u0644\u0645\u062a\u0648\u0633\u0637",
        "horizon_strength": "\u0636\u0639\u064a\u0641\u0629/\u0645\u062a\u0648\u0633\u0637\u0629",
        "confidence_band": "\u0645\u0646\u062e\u0641\u0636",
        "h1_direction": "neutral",
        "h4_direction": "neutral",
        "d1_direction": "neutral",
        "technical_review_price": 1763.2827588574876,
        "scenario_levels_model": "timeframe_atr_ema_v27",
        "selected_timeframe": "weekly",
        "selected_timeframe_label": "\u0623\u0633\u0628\u0648\u0639\u064a",
        "selected_timeframe_close": 1799.56,
        "selected_timeframe_rsi": 32.23801503801785,
        "selected_timeframe_atr": 182.57500000000002,
        "selected_timeframe_direction": "bearish",
        "timeframe_model": "asset_view_timeframe_v27"
    },
    "live_price_bound": true,
    "data_provider": "binance",
    "generated_at": "2026-07-07T07:52:06Z",
    "golden_signal": false,
    "golden_alignment_active": false,
    "golden_status": "partial",
    "golden_name": "NDSP_GOLDEN_ALIGNMENT",
    "golden_reason_public": "\u0628\u0639\u0636 \u0634\u0631\u0648\u0637 \u0627\u0644\u0645\u062d\u0627\u0630\u0627\u0629 \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629 \u0645\u062a\u0648\u0641\u0631\u0629\u060c \u0644\u0643\u0646 \u0627\u0644\u0625\u0634\u0627\u0631\u0629 \u0644\u0645 \u062a\u0643\u062a\u0645\u0644 \u0628\u0627\u0644\u0643\u0627\u0645\u0644 \u0644\u0647\u0630\u0627 \u0627\u0644\u0623\u0635\u0644.",
    "golden_evidence_public": [
        {
            "label": "\u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0631",
            "value": "86 / 100"
        },
        {
            "label": "\u062d\u0627\u0644\u0629 \u0627\u0644\u0633\u064a\u0646\u0627\u0631\u064a\u0648",
            "value": "UNDER_MONITORING"
        },
        {
            "label": "\u0633\u064a\u0627\u0642 \u0627\u0644\u0627\u062a\u062c\u0627\u0647",
            "value": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637"
        },
        {
            "label": "\u0633\u0628\u0628 \u0627\u0644\u062a\u062d\u0641\u0638",
            "value": "\u0627\u0646\u062a\u0638\u0627\u0631 \u062b\u0628\u0627\u062a \u0627\u0644\u0633\u0639\u0631 \u062f\u0648\u0646 \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629."
        }
    ],
    "golden_alignment": {
        "golden_signal": false,
        "golden_alignment_active": false,
        "golden_status": "partial",
        "golden_label_public": "\u062c\u0632\u0626\u064a\u0629 / \u062a\u062d\u062a \u0627\u0644\u0645\u0631\u0627\u0642\u0628\u0629",
        "golden_name": "NDSP_GOLDEN_ALIGNMENT",
        "golden_name_public": "\u0625\u0634\u0627\u0631\u0629 \u0646\u0648\u0627\u0641 \u0627\u0644\u0630\u0647\u0628\u064a\u0629",
        "golden_reason_public": "\u0628\u0639\u0636 \u0634\u0631\u0648\u0637 \u0627\u0644\u0645\u062d\u0627\u0630\u0627\u0629 \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629 \u0645\u062a\u0648\u0641\u0631\u0629\u060c \u0644\u0643\u0646 \u0627\u0644\u0625\u0634\u0627\u0631\u0629 \u0644\u0645 \u062a\u0643\u062a\u0645\u0644 \u0628\u0627\u0644\u0643\u0627\u0645\u0644 \u0644\u0647\u0630\u0627 \u0627\u0644\u0623\u0635\u0644.",
        "golden_evidence_public": [
            {
                "label": "\u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0631",
                "value": "86 / 100"
            },
            {
                "label": "\u062d\u0627\u0644\u0629 \u0627\u0644\u0633\u064a\u0646\u0627\u0631\u064a\u0648",
                "value": "UNDER_MONITORING"
            },
            {
                "label": "\u0633\u064a\u0627\u0642 \u0627\u0644\u0627\u062a\u062c\u0627\u0647",
                "value": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637"
            },
            {
                "label": "\u0633\u0628\u0628 \u0627\u0644\u062a\u062d\u0641\u0638",
                "value": "\u0627\u0646\u062a\u0638\u0627\u0631 \u062b\u0628\u0627\u062a \u0627\u0644\u0633\u0639\u0631 \u062f\u0648\u0646 \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629."
            }
        ],
        "golden_effect_public": "\u0645\u0639\u0632\u0651\u0632 \u0644\u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0631 \u0641\u0642\u0637\u060c \u0648\u0644\u064a\u0633 \u062a\u0648\u0635\u064a\u0629 \u0645\u0627\u0644\u064a\u0629 \u0648\u0644\u0627 \u0623\u0645\u0631 \u062a\u0646\u0641\u064a\u0630.",
        "not_recommendation": true,
        "no_buy_sell": true,
        "protected_layers_masked": true,
        "source_mode": "quality_live_governed_output_runtime_alignment",
        "wrapper_version": "1.0.0-ndsp-golden-explainability"
    },
    "golden_spotlight": {
        "title": "\u0625\u0634\u0627\u0631\u0629 \u0646\u0648\u0627\u0641 \u0627\u0644\u0630\u0647\u0628\u064a\u0629",
        "status": "partial",
        "label": "\u062c\u0632\u0626\u064a\u0629 / \u062a\u062d\u062a \u0627\u0644\u0645\u0631\u0627\u0642\u0628\u0629",
        "summary": "\u0628\u0639\u0636 \u0634\u0631\u0648\u0637 \u0627\u0644\u0645\u062d\u0627\u0630\u0627\u0629 \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629 \u0645\u062a\u0648\u0641\u0631\u0629\u060c \u0644\u0643\u0646 \u0627\u0644\u0625\u0634\u0627\u0631\u0629 \u0644\u0645 \u062a\u0643\u062a\u0645\u0644 \u0628\u0627\u0644\u0643\u0627\u0645\u0644 \u0644\u0647\u0630\u0627 \u0627\u0644\u0623\u0635\u0644.",
        "quality_effect": "\u0645\u0639\u0632\u0651\u0632 \u0644\u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0631 \u0641\u0642\u0637\u060c \u0648\u0644\u064a\u0633 \u062a\u0648\u0635\u064a\u0629 \u0645\u0627\u0644\u064a\u0629 \u0648\u0644\u0627 \u0623\u0645\u0631 \u062a\u0646\u0641\u064a\u0630.",
        "evidence": [
            {
                "label": "\u062c\u0648\u062f\u0629 \u0627\u0644\u0642\u0631\u0627\u0631",
                "value": "86 / 100"
            },
            {
                "label": "\u062d\u0627\u0644\u0629 \u0627\u0644\u0633\u064a\u0646\u0627\u0631\u064a\u0648",
                "value": "UNDER_MONITORING"
            },
            {
                "label": "\u0633\u064a\u0627\u0642 \u0627\u0644\u0627\u062a\u062c\u0627\u0647",
                "value": "\u0642\u0631\u0627\u0621\u0629 \u0623\u0633\u0628\u0648\u0639\u064a \u00b7 \u0636\u063a\u0637 \u0647\u0627\u0628\u0637"
            },
            {
                "label": "\u0633\u0628\u0628 \u0627\u0644\u062a\u062d\u0641\u0638",
                "value": "\u0627\u0646\u062a\u0638\u0627\u0631 \u062b\u0628\u0627\u062a \u0627\u0644\u0633\u0639\u0631 \u062f\u0648\u0646 \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629."
            }
        ]
    },
    "explainability": {
        "golden_signal_exposed": true,
        "golden_signal": false,
        "golden_status": "partial",
        "golden_reason_public": "\u0628\u0639\u0636 \u0634\u0631\u0648\u0637 \u0627\u0644\u0645\u062d\u0627\u0630\u0627\u0629 \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629 \u0645\u062a\u0648\u0641\u0631\u0629\u060c \u0644\u0643\u0646 \u0627\u0644\u0625\u0634\u0627\u0631\u0629 \u0644\u0645 \u062a\u0643\u062a\u0645\u0644 \u0628\u0627\u0644\u0643\u0627\u0645\u0644 \u0644\u0647\u0630\u0627 \u0627\u0644\u0623\u0635\u0644.",
        "evidence_trace": true,
        "reason_codes": true,
        "engine_coverage": "masked_public_trace",
        "protected_layers_masked": true,
        "no_internal_formula_exposure": true,
        "not_recommendation": true

## 6) Public HTTP size checks
[200] size=3297 https://my.ndsp.app/NDSP_Command_Center.html
[200] size=3229 https://my.ndsp.app/decision-radar.html
[200] size=2544 https://my.ndsp.app/decision-support.html
[200] size=2789 https://my.ndsp.app/NDSP_Asset_View.html

## 7) Script duplication check
/var/www/ndsp-my/NDSP_Command_Center.html:4:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/NDSP_Command_Center.html:6:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>مركز القيادة</h1><p>رادار فخم يتلون حسب حالة الأصل.</p></section><section class="radar-layout"><div class="radar-box"><div class="radar"><div class="core"><span data-live-state>Loading</span></div><div class="node n1">TDL</div><div class="node n2">NMP</div><div class="node n3">USD Macro</div><div class="node n4">Risk</div><div class="node n5">Devil Gate</div><div class="node n6">Hidden Consensus</div></div><div class="notice">الأصل: <b data-selected-symbol>ETHUSDT</b> — السعر: <b data-live-price>تحميل</b></div></div><div class="brief-box"><h2>Premium Decision Radar</h2><div class="brief-grid"><article class="card"><h3>Decision Core</h3><span data-live-state>تحميل</span></article><article class="card"><h3>Decision Quality</h3><span>مؤشر جودة القرار.</span></article><article class="card"><h3>Devil’s Advocate</h3><span>الطبقة الوحيدة التي يسمح لها بالمنع.</span></article><article class="card"><h3>Scenario Levels</h3><span>Activation / Arrival / Review / Invalidation</span></article></div><div class="notice">قراءة JSON الحية:</div><pre data-live-json>تحميل...</pre></div></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>  <script src="/assets/ndsp-radar-safe-clean.js?v=23"></script>
/var/www/ndsp-my/NDSP_Command_Center.html:7:  <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>
/var/www/ndsp-my/decision-radar.html:4:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/decision-radar.html:5:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Premium Decision Radar</h1><p>رادار فخم يتلون حسب حالة الأصل.</p></section><section class="radar-layout"><div class="radar-box"><div class="radar"><div class="core"><span data-live-state>Loading</span></div><div class="node n1">TDL</div><div class="node n2">NMP</div><div class="node n3">USD Macro</div><div class="node n4">Risk</div><div class="node n5">Devil Gate</div><div class="node n6">Hidden Consensus</div></div><div class="notice">الأصل: <b data-selected-symbol>ETHUSDT</b> — السعر: <b data-live-price>تحميل</b></div></div><div class="brief-box"><h2>Premium Decision Radar</h2><div class="brief-grid"><article class="card"><h3>Decision Core</h3><span data-live-state>تحميل</span></article><article class="card"><h3>Decision Quality</h3><span>مؤشر جودة القرار.</span></article><article class="card"><h3>Devil’s Advocate</h3><span>الطبقة الوحيدة التي يسمح لها بالمنع.</span></article><article class="card"><h3>Scenario Levels</h3><span>Activation / Arrival / Review / Invalidation</span></article></div><div class="notice">قراءة JSON الحية:</div><pre data-live-json>تحميل...</pre></div></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>  <script src="/assets/ndsp-radar-safe-clean.js?v=23"></script>
/var/www/ndsp-my/decision-radar.html:6:  <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>

FINAL_STATUS=COMMAND_CENTER_RADAR_PREFLIGHT_DONE
REPORT=docs/05-runbooks/NDSP_COMMAND_CENTER_RADAR_PREFLIGHT_20260707_095205.md
