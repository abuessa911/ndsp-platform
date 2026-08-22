const NDSP_PUBLIC_FOUR_LAYERS_V140 = "NDSP_PUBLIC_FOUR_LAYERS_V140";
const NDSP_PUBLIC_IP_EXPOSURE_LOCK_V1_1 = "NDSP_PUBLIC_IP_EXPOSURE_LOCK_V1_1";
const OPTIONAL_API_LOADING_V56 = "NDSP_OPTIONAL_API_LOADING_V56";
const BINDING_FIX_V52="NDSP_BIND_VERIFY_ALL_PAGES_V52";
const CONTEXT_FIX_V51="NDSP_CONTEXT_LOCK_GATE_FIX_V51";
const VERSION = "v50";
const BASE = `/portal-${VERSION}`;
const STORAGE_KEY = "ndsp_analysis_context_v1";
const LANG_KEY = "ndsp_portal_lang_v1";

const ROUTES = {
  selector: { path: "/analysis-center.html", ar: "اختيار التحليل", en: "Analysis Setup", shortAr: "الاختيار", shortEn: "Setup" },
  home: { path: "/portal.html", ar: "لوحة المستخدم", en: "User Home", shortAr: "الرئيسية", shortEn: "Home" },
  markets: { path: "/market-assets.html", ar: "الأسواق والأصول", en: "Markets & Assets", shortAr: "الأسواق", shortEn: "Markets" },
  decision: { path: "/decision-support.html", ar: "غرفة القرار", en: "Decision Room", shortAr: "القرار", shortEn: "Decision" },
  layers: { path: "/decision-layers.html", ar: "الطبقات والمحركات", en: "Layers & Engines", shortAr: "الطبقات", shortEn: "Layers" },
  capabilities: { path: "/platform-capabilities.html", ar: "قدرات المنصة", en: "Platform Capabilities", shortAr: "القدرات", shortEn: "Capabilities" },
  scenarios: { path: "/scenario-levels.html", ar: "السيناريوهات والمستويات", en: "Scenarios & Levels", shortAr: "السيناريو", shortEn: "Scenario" },
  risk: { path: "/risk-governance.html", ar: "المخاطر والاعتراض", en: "Risk & Challenge", shortAr: "المخاطر", shortEn: "Risk" },
  completed: { path: "/completed-decisions.html", ar: "القرارات المكتملة", en: "Completed Decisions", shortAr: "السجل", shortEn: "History" },
  data: { path: "/data-health.html", ar: "صحة البيانات", en: "Data Health", shortAr: "البيانات", shortEn: "Data" },
  guide: { path: "/decision-guide.html", ar: "دليل القرار", en: "Decision Guide", shortAr: "الدليل", shortEn: "Guide" },
  telegram: { path: "/telegram-alerts/", ar: "تنبيهات Telegram", en: "Telegram Alerts", shortAr: "تيليجرام", shortEn: "Telegram" }
};

const PATH_TO_PAGE = {
  "/analysis-center.html": "selector", "/asset-selector.html": "selector",
  "/portal.html": "home", "/dashboard.html": "home", "/platform.html": "home", "/command-center.html": "home", "/NDSP_Command_Center.html": "home",
  "/market-assets.html": "markets", "/markets.html": "markets", "/my-watchlist.html": "markets",
  "/decision-support.html": "decision", "/decision-center.html": "decision", "/decision-room.html": "decision",
  "/decision-layers.html": "layers", "/decision-radar.html": "layers", "/radar.html": "layers",
  "/platform-capabilities.html": "capabilities",
  "/scenario-levels.html": "scenarios", "/nmp.html": "scenarios",
  "/risk-governance.html": "risk", "/governance.html": "risk",
  "/completed-decisions.html": "completed", "/completed-decisions-review.html": "completed",
  "/data-health.html": "data", "/data-freshness.html": "data",
  "/decision-guide.html": "guide", "/guide.html": "guide"
};

const T = {
  ar: {
    product: "NDSP — منصة دعم القرار", contextLocked: "السياق مقفل", changeContext: "تغيير الاختيار",
    market: "السوق", asset: "الأصل", timeframe: "الفريم", analysisMode: "نوع القراءة", viewMode: "مستوى العرض", session: "جلسة القرار",
    dataState: "حالة البيانات", liveGoverned: "حية ومحكومة", waiting: "بانتظار البيانات", unavailable: "غير متاح", unknown: "غير محدد",
    investment: "استثمارية", speculative: "مضاربية", beginner: "بسيط", professional: "محترف",
    start: "ابدأ التحليل", refresh: "تحديث", loading: "جاري تحميل السياق والبيانات المحكومة...", noFabrication: "لا تُعرض قيم افتراضية أو مصطنعة عند غياب البيانات.",
    selectorTitle: "ابدأ من السياق الصحيح", selectorDesc: "اختر السوق والأصل والفريم ونوع القراءة أولًا. بعد ذلك تُقفل الجلسة وتصبح كل صفحة وكل طلب API مرتبطًا بنفس الأصل والسياق.",
    selectMarket: "1. اختر السوق", selectAsset: "2. اختر الأصل", selectTimeframe: "3. اختر الفريم", selectReading: "4. اختر نوع القراءة", selectView: "5. اختر مستوى العرض",
    searchAsset: "ابحث بالرمز أو الاسم", selectedContext: "السياق المختار", incompleteSelection: "أكمل السوق والأصل والفريم ونوع القراءة قبل بدء التحليل.",
    decisionTitle: "غرفة القرار", decisionDesc: "ملخص واحد واضح أولًا، ثم التفسير والمستويات والمخاطر والأدلة حسب السياق المقفل.",
    currentDecision: "القرار الحالي", readingState: "حالة القراءة", direction: "السياق الاتجاهي", strength: "قوة القراءة", readiness: "جاهزية القرار", whyIncomplete: "لماذا لم يكتمل القرار؟",
    activation: "التفعيل", arrival: "الوصول", review: "المراجعة", invalidation: "الإلغاء", nmp: "NMP",
    simpleExplain: "التفسير المبسط", proExplain: "التفسير المحترف", governingScenario: "السيناريو الحاكم", alternatives: "السيناريوهات البديلة",
    risk: "المخاطر", macro: "الدولار والسياق الكلي", devil: "محامي الشيطان", evidence: "الأدلة التحليلية", layerCompletion: "اكتمال وحدات القرار",
    mismatchTitle: "تم حجب الاستجابة بسبب اختلاف السياق", mismatchText: "أعادت الخدمة بيانات لا تطابق الأصل أو الفريم المختار. لم تُعرض النتيجة لمنع اعتماد تحليل أصل آخر.",
    layersTitle: "الطبقات الست عشرة", layersDesc: "كل طبقة تعرض حالتها ومساهمتها وأثرها دون خلطها بقدرات المنصة.",
    capabilitiesTitle: "قدرات المنصة الثماني والعشرون", capabilitiesDesc: "قدرات تشغيل وتجربة وبيانات وتكامل؛ لا تُعد طبقات قرار ولا تملك سلطة علمية مستقلة.",
    scenariosTitle: "السيناريوهات والمستويات", scenariosDesc: "التفعيل والوصول والمراجعة والإلغاء وNMP لنفس الأصل والفريم المختارين.",
    riskTitle: "المخاطر والاعتراض", riskDesc: "السياق الكلي ثم المخاطر ثم محامي الشيطان قبل رفع الجاهزية.",
    completedTitle: "القرارات المكتملة والسجل", completedDesc: "قرارات موثقة منفصلة عن القراءة الجارية، مع بصمة وسياق واضحين.",
    dataTitle: "صحة البيانات والمصادر", dataDesc: "حالة نقاط النهاية وزمن الاستجابة وصحة تطابق السياق دون تحويلها إلى سلطة قرار.",
    marketsTitle: "كل الأسواق والأصول", marketsDesc: "سجل العرض المتاح. اختيار أي أصل ينشئ سياقًا جديدًا ولا يعيد استخدام بيانات الأصل السابق.",
    guideTitle: "دليل قراءة القرار", guideDesc: "اقرأ الملخص أولًا، ثم السبب والمستويات والمخاطر، وبعدها الأدلة والتفاصيل المتقدمة.",
    noData: "لم تصل بيانات محكومة لهذه الخانة حتى الآن.", raw: "البيانات الخام للمحترف", blocking: "مانعة", notBlocking: "غير مانعة", status: "الحالة", confidence: "الثقة", family: "العائلة",
    source: "المصدر", latency: "زمن الاستجابة", http: "HTTP", contextMatch: "تطابق السياق", yes: "نعم", no: "لا", retry: "إعادة المحاولة",
    officialLanding: "صفحة الهبوط", login: "الدخول", register: "مستخدم جديد", menu: "القائمة", close: "إغلاق",
    homeTitle: "لوحة المستخدم", homeDesc: "بوابة مختصرة تقودك من السياق المقفل إلى القرار ثم الأدلة دون إغراقك في شاشة واحدة.",
    nextStep: "الخطوة التالية", openDecision: "فتح غرفة القرار", openLayers: "عرض الطبقات المعلنة", openScenarios: "عرض السيناريوهات", openRisk: "عرض المخاطر",
    coverage: "التغطية", records: "السجلات", integrity: "سلامة السلسلة", current: "الحالية", history: "التاريخ", noRecords: "لا توجد سجلات متاحة من الخدمة الحالية.",
    platformOnly: "قدرة منصة — بلا سلطة قرار", underMonitoring: "تحت المتابعة", completed: "مكتملة", blocked: "محجوبة", active: "نشطة", partial: "جزئية", notEvaluated: "لم تُقيّم"
  },
  en: {
    product: "NDSP — Decision Support Platform", contextLocked: "Context locked", changeContext: "Change selection",
    market: "Market", asset: "Asset", timeframe: "Timeframe", analysisMode: "Reading type", viewMode: "View level", session: "Decision session",
    dataState: "Data state", liveGoverned: "Live and governed", waiting: "Waiting for data", unavailable: "Unavailable", unknown: "Unknown",
    investment: "Investment", speculative: "Speculative", beginner: "Beginner", professional: "Professional",
    start: "Start analysis", refresh: "Refresh", loading: "Loading governed context and data...", noFabrication: "Missing values are never replaced with fabricated defaults.",
    selectorTitle: "Start with the correct context", selectorDesc: "Select market, asset, timeframe and reading type first. The session is then locked and every page and API request uses the same context.",
    selectMarket: "1. Select market", selectAsset: "2. Select asset", selectTimeframe: "3. Select timeframe", selectReading: "4. Select reading type", selectView: "5. Select view level",
    searchAsset: "Search by symbol or name", selectedContext: "Selected context", incompleteSelection: "Complete market, asset, timeframe and reading type before starting.",
    decisionTitle: "Decision Room", decisionDesc: "One clear summary first, followed by interpretation, levels, risk and evidence for the locked context.",
    currentDecision: "Current decision", readingState: "Reading state", direction: "Directional context", strength: "Reading strength", readiness: "Decision readiness", whyIncomplete: "Why is the decision incomplete?",
    activation: "Activation", arrival: "Arrival", review: "Review", invalidation: "Invalidation", nmp: "NMP — NMP",
    simpleExplain: "Beginner explanation", proExplain: "Professional explanation", governingScenario: "Governing scenario", alternatives: "Alternative scenarios",
    risk: "Risk", macro: "USD and macro", devil: "Devil's Advocate", evidence: "Analytical evidence", layerCompletion: "Decision unit completion",
    mismatchTitle: "Response blocked due to context mismatch", mismatchText: "The service returned a different asset or timeframe. The result was not rendered to prevent cross-asset analysis contamination.",
    layersTitle: "The Sixteen Layers", layersDesc: "Each layer shows its state, contribution and effect, separate from platform capabilities.",
    capabilitiesTitle: "The Twenty-Eight Platform Capabilities", capabilitiesDesc: "Operational, experience, data and integration capabilities; they are not decision layers and have no independent scientific authority.",
    scenariosTitle: "Scenarios and Levels", scenariosDesc: "Activation, arrival, review, invalidation and NMP for the same selected asset and timeframe.",
    riskTitle: "Risk and Challenge", riskDesc: "Macro first, then risk, then Devil's Advocate before readiness is raised.",
    completedTitle: "Completed Decisions and History", completedDesc: "Documented decisions separated from the live reading, with explicit context and fingerprint.",
    dataTitle: "Data and Source Health", dataDesc: "Endpoint health, latency and context matching without turning infrastructure into decision authority.",
    marketsTitle: "All Markets and Assets", marketsDesc: "Display registry. Selecting another asset creates a new context and never reuses the previous asset's decision.",
    guideTitle: "Decision Reading Guide", guideDesc: "Read summary first, then reasons, levels and risk, followed by evidence and advanced details.",
    noData: "No governed value has been received for this field.", raw: "Raw data for professional view", blocking: "Blocking", notBlocking: "Non-blocking", status: "State", confidence: "Confidence", family: "Family",
    source: "Source", latency: "Latency", http: "HTTP", contextMatch: "Context match", yes: "Yes", no: "No", retry: "Retry",
    officialLanding: "Landing", login: "Login", register: "Register", menu: "Menu", close: "Close",
    homeTitle: "User Home", homeDesc: "A concise gateway from locked context to decision and evidence without forcing everything into one page.",
    nextStep: "Next step", openDecision: "Open decision room", openLayers: "View public layers", openScenarios: "View scenarios", openRisk: "View risk",
    coverage: "Coverage", records: "Records", integrity: "Chain integrity", current: "Current", history: "History", noRecords: "No records are available from the current service.",
    platformOnly: "Platform capability — no decision authority", underMonitoring: "Under monitoring", completed: "Completed", blocked: "Blocked", active: "Active", partial: "Partial", notEvaluated: "Not evaluated"
  }
};

const app = document.getElementById("app");
let lang = localStorage.getItem(LANG_KEY) === "en" ? "en" : "ar";
let assetsRegistry = { markets: [] };
let layerRegistry = { layers: [] };
let capabilityRegistry = { capabilities: [] };
let lastBundle = null;
let endpointTelemetry = [];

function tx(key){ return T[lang][key] ?? T.ar[key] ?? key; }
function esc(value){ return String(value ?? "").replace(/[&<>"']/g, m => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m])); }
function num(value){ const n = Number(value); return Number.isFinite(n) ? n : null; }
function fmt(value, digits=2){ const n=num(value); return n===null ? tx("unavailable") : n.toLocaleString(lang==="ar"?"ar-SA":"en-US",{maximumFractionDigits:digits}); }
function pick(...values){ return values.find(v => v !== undefined && v !== null && String(v).trim() !== ""); }
function arr(value){ return Array.isArray(value) ? value : []; }
function obj(value){ return value && typeof value === "object" && !Array.isArray(value) ? value : {}; }
function normalizeSymbol(v){ return String(v||"").replace(/[^A-Za-z0-9]/g,"").toUpperCase(); }
function normalizeTimeframe(v){
  const x=String(v||"").toLowerCase().replace(/\s+/g,"");
  const map={"1w":"weekly","week":"weekly","weekly":"weekly","w":"weekly","1d":"daily","day":"daily","daily":"daily","d":"daily","4hour":"4h","4hours":"4h","4h":"4h","h4":"4h","1hour":"1h","1h":"1h","h1":"1h"};
  return map[x]||x;
}
/* NDSP_V104_NATIVE_TIMEFRAME_LABELS */
function timeframeLabel(value){
  const id=normalizeTimeframe(value);
  const ar={
    "15m":"15 دقيقة",
    "1h":"ساعة",
    "4h":"4 ساعات",
    "daily":"يومي",
    "weekly":"أسبوعي",
    "monthly":"شهري"
  };
  const en={
    "15m":"15 min",
    "1h":"1 hour",
    "4h":"4 hours",
    "daily":"Daily",
    "weekly":"Weekly",
    "monthly":"Monthly"
  };
  return (lang==="ar"?ar:en)[id]||String(value||"").toUpperCase();
}

function statusTone(value){
  const s=String(value||"").toUpperCase();
  if(/GOVERNED_REDACTED|INPUTS_INCOMPLETE|INCOMPLETE|NOT_EVALUATED|UNAVAILABLE|PENDING|UNDER_REVIEW/.test(s))return"warn";
  if(/BLOCK|FAIL|ERROR|INVALID|MISMATCH/.test(s))return"bad";
  if(/COMPLETE|READY|ACTIVE|AVAILABLE|PASS|OK|ALIGNED|CONFIRMED/.test(s))return"ok";
  if(/MONITOR|PARTIAL|WARN|REVIEW|WAIT/.test(s))return"warn";
  return"";
}
function statusLabel(value){
  const s=String(value||"").toUpperCase();
  const ar={UNDER_MONITORING:"تحت المتابعة",MONITORING_ONLY:"متابعة فقط",UNDER_REVIEW:"تحت المراجعة",COMPLETED:"مكتملة",COMPLETE:"مكتملة",READY:"جاهزة",BLOCKED:"محجوبة",DATA_BLOCKED:"محجوبة بسبب البيانات",GOVERNED_REDACTED:"محجوبة حسب صلاحية العرض",ACTIVE:"نشطة",ENABLED:"مفعلة",AVAILABLE:"متاحة",UNAVAILABLE:"غير متاحة",PARTIAL_AVAILABLE:"متاحة جزئيًا",INPUTS_INCOMPLETE:"مدخلات غير مكتملة",INCOMPLETE:"غير مكتملة",NOT_EVALUATED:"لم تُقيّم",PENDING:"قيد المتابعة",CONFIRMED:"مؤكدة",ALIGNED:"متوافقة",NEUTRAL:"محايدة",BULLISH:"ميل صاعد",BEARISH:"ميل هابط",PASS:"ناجح",WARN:"تحذير",FAIL:"فشل"};
  const en={UNDER_MONITORING:"Under monitoring",MONITORING_ONLY:"Monitoring only",UNDER_REVIEW:"Under review",COMPLETED:"Completed",COMPLETE:"Complete",READY:"Ready",BLOCKED:"Blocked",DATA_BLOCKED:"Data blocked",GOVERNED_REDACTED:"Redacted by view policy",ACTIVE:"Active",ENABLED:"Enabled",AVAILABLE:"Available",UNAVAILABLE:"Unavailable",PARTIAL_AVAILABLE:"Partially available",INPUTS_INCOMPLETE:"Inputs incomplete",INCOMPLETE:"Incomplete",NOT_EVALUATED:"Not evaluated",PENDING:"Pending",CONFIRMED:"Confirmed",ALIGNED:"Aligned",NEUTRAL:"Neutral",BULLISH:"Bullish",BEARISH:"Bearish",PASS:"Pass",WARN:"Warning",FAIL:"Fail"};
  return (lang==="ar"?ar:en)[s] || value || tx("unknown");
}

function deepGet(root, paths){
  for(const path of paths){ let cur=root; let ok=true; for(const key of path.split(".")){ if(cur && Object.prototype.hasOwnProperty.call(cur,key)){cur=cur[key]}else{ok=false;break} } if(ok && cur!==undefined && cur!==null && cur!=="") return cur; }
  return null;
}
function hashText(text){ let h=2166136261; for(let i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,16777619)} return (h>>>0).toString(16).padStart(8,"0"); }
function newSession(ctx){ const core=[ctx.market,ctx.symbol,ctx.timeframe,ctx.analysis_mode].join("|"); return `NDSP-${hashText(core).toUpperCase()}-${Date.now().toString(36).toUpperCase()}`; }
function getContext(){
  const q=new URLSearchParams(location.search); let stored={}; try{stored=JSON.parse(sessionStorage.getItem(STORAGE_KEY)||localStorage.getItem(STORAGE_KEY)||"{}")}catch{}
  const ctx={
    market:q.get("market")||stored.market||"", symbol:normalizeSymbol(q.get("symbol")||stored.symbol||""), timeframe:normalizeTimeframe(q.get("timeframe")||stored.timeframe||""),
    analysis_mode:(q.get("mode")||stored.analysis_mode||"").toLowerCase(), view_mode:(q.get("view")||stored.view_mode||"beginner").toLowerCase(), session_id:q.get("session")||stored.session_id||""
  };
  if(ctx.market&&ctx.symbol&&ctx.timeframe&&ctx.analysis_mode&&!ctx.session_id)ctx.session_id=newSession(ctx);
  return ctx;
}
function contextComplete(ctx){ return !!(ctx.market&&ctx.symbol&&ctx.timeframe&&["investment","speculative"].includes(ctx.analysis_mode)&&["beginner","professional"].includes(ctx.view_mode)); }
function saveContext(ctx){ if(!ctx.session_id)ctx.session_id=newSession(ctx); const raw=JSON.stringify(ctx); sessionStorage.setItem(STORAGE_KEY,raw); localStorage.setItem(STORAGE_KEY,raw); return ctx; }
function contextQuery(ctx){ const q=new URLSearchParams({market:ctx.market,symbol:ctx.symbol,timeframe:ctx.timeframe,mode:ctx.analysis_mode,view:ctx.view_mode,session:ctx.session_id}); return q.toString(); }
function routeHref(page,ctx=getContext()){ const r=ROUTES[page]||ROUTES.selector; return contextComplete(ctx)&&page!=="selector" ? `${r.path}?${contextQuery(ctx)}` : r.path; }
function currentPage(){ const q=new URLSearchParams(location.search); if(q.get("page")&&ROUTES[q.get("page")])return q.get("page"); const path=location.pathname.replace(/\/$/,"")||"/"; if(path.startsWith(`${BASE}/`)){const part=path.split("/").filter(Boolean).pop(); if(ROUTES[part])return part; return "selector"} return PATH_TO_PAGE[path]||"selector"; }
function assetSymbol(asset){ return normalizeSymbol(typeof asset==="string"?asset:pick(asset?.symbol,asset?.asset_symbol,asset?.ticker,asset?.code,asset?.asset_id,asset?.instrument,asset?.id,asset?.pair)); }
function marketRecord(id){ return arr(assetsRegistry.markets).find(m=>String(m.id).toUpperCase()===String(id).toUpperCase()); }
function marketForSymbol(symbol){ const target=normalizeSymbol(symbol); return arr(assetsRegistry.markets).find(m=>arr(m.assets).some(a=>assetSymbol(a)===target)); }
function allAssets(){ return arr(assetsRegistry.markets).flatMap(m=>arr(m.assets).map(a=>({symbol:assetSymbol(a),market:m.id,name_ar:typeof a==="object"?(a.name_ar||a.arabic_name||a.label_ar||""):"",name_en:typeof a==="object"?(a.name_en||a.english_name||a.label_en||a.name||""):""}))).filter(x=>x.symbol); }

async function loadJSON(url){ const res=await fetch(url,{credentials:"same-origin",cache:"no-store",headers:{Accept:"application/json"}}); if(!res.ok)throw new Error(`${url} HTTP ${res.status}`); return res.json(); }
async function loadRegistries(){
  const result=await Promise.allSettled([
    loadJSON(`${BASE}/config/assets.json?v=${Date.now()}`)
  ]);
  const assets=result[0];
  if(assets.status==="fulfilled")assetsRegistry=assets.value;
  layerRegistry={layers:[]};
  capabilityRegistry={capabilities:[]};
  if(!arr(assetsRegistry.markets).length&&arr(assetsRegistry.assets).length){
    const groups={};
    for(const x of assetsRegistry.assets){
      const m=x.market||x.asset_class||"OTHER";
      (groups[m]??=[]).push(x);
    }
    assetsRegistry.markets=Object.entries(groups).map(([id,assets])=>({
      id,name_ar:id,name_en:id,assets
    }));
  }
}

function navItems(){ /* NDSP_PUBLIC_FOUR_LAYERS_V140 */ return ["home","markets","decision","layers","scenarios","risk","completed","data","guide","telegram"]; }
function shell(content,page,ctx){
  document.documentElement.lang=lang; document.documentElement.dir=lang==="ar"?"rtl":"ltr"; document.body.dataset.ndspPage=page; document.body.dataset.ndspContextKey=contextComplete(ctx)?[ctx.market,ctx.symbol,ctx.timeframe,ctx.analysis_mode,ctx.view_mode,ctx.session_id].join("|"):"UNLOCKED";
  const complete=contextComplete(ctx);
  const nav=navItems().map(k=>`<a class="${page===k?"active":""}" href="${routeHref(k,ctx)}">${esc(lang==="ar"?ROUTES[k].ar:ROUTES[k].en)}</a>`).join("");
  const mobile=["home","markets","decision","layers","guide"].map(k=>`<a class="${page===k?"active":""}" href="${routeHref(k,ctx)}"><span>${esc(lang==="ar"?ROUTES[k].shortAr:ROUTES[k].shortEn)}</span></a>`).join("");
  const context=complete?`<div class="contextBar" data-context-locked="true"><div class="contextGrid">
    ${ctxItem(tx("market"),marketRecord(ctx.market)?.[lang==="ar"?"name_ar":"name_en"]||ctx.market)}
    ${ctxItem(tx("asset"),ctx.symbol)}${ctxItem(tx("timeframe"),ctx.timeframe.toUpperCase())}
    ${ctxItem(tx("analysisMode"),tx(ctx.analysis_mode))}${ctxItem(tx("viewMode"),tx(ctx.view_mode))}
    <div class="ctxItem ctxSession"><small>${tx("session")}</small><strong>${esc(ctx.session_id)}</strong></div></div></div>`:"";
  app.innerHTML=`<div class="appShell" data-ndsp-page="${esc(page)}" data-ndsp-context-key="${esc(complete?[ctx.market,ctx.symbol,ctx.timeframe,ctx.analysis_mode,ctx.view_mode,ctx.session_id].join("|"):"UNLOCKED")}"><header class="topbar"><a class="brand" href="${routeHref(complete?"home":"selector",ctx)}"><span class="brandMark">N</span><span class="brandText"><strong>NDSP</strong><small>${esc(tx("product"))}</small></span></a><nav class="nav">${nav}</nav><div class="topActions"><button class="btn langBtn" id="langToggle">${lang==="ar"?"EN":"AR"}</button>${complete?`<a class="btn" href="${ROUTES.selector.path}">${tx("changeContext")}</a>`:""}<button class="iconBtn mobileMenuBtn" id="menuOpen">${tx("menu")}</button></div></header>${context}<main class="main">${content}</main><nav class="bottomNav">${mobile}</nav><div class="drawer" id="drawer"><button class="drawerBackdrop" id="drawerClose" aria-label="${tx("close")}"></button><aside class="drawerPanel"><div class="cardHead"><div><b>NDSP</b><p>${tx("product")}</p></div><button class="iconBtn" id="drawerClose2">×</button></div><div class="drawerLinks">${nav}<a href="https://www.ndsp.app/">${tx("officialLanding")}</a><a href="/login/">${tx("login")}</a><a href="/register/">${tx("register")}</a></div></aside></div></div>`;
  document.getElementById("langToggle")?.addEventListener("click",()=>{lang=lang==="ar"?"en":"ar";localStorage.setItem(LANG_KEY,lang);render()});
  document.getElementById("menuOpen")?.addEventListener("click",()=>document.getElementById("drawer")?.classList.add("open"));
  ["drawerClose","drawerClose2"].forEach(id=>document.getElementById(id)?.addEventListener("click",()=>document.getElementById("drawer")?.classList.remove("open")));
}
function ctxItem(label,value,cls=""){ return `<div class="ctxItem ${cls}"><small>${esc(label)}</small><strong>${esc(value||tx("unavailable"))}</strong></div>`; }
function pageHero(title,desc,actions=""){ return `<section class="pageHero"><div><div class="eyebrow">NDSP · ${esc(tx("contextLocked"))}</div><h1>${esc(title)}</h1><p>${esc(desc)}</p></div><div class="heroActions">${actions}</div></section>`; }
function badge(value,label){ return `<span class="badge ${statusTone(value)}">${esc(label||statusLabel(value))}</span>`; }
function meter(label,value,type=""){ const n=num(value); return `<div class="kpi"><small>${esc(label)}</small><strong>${n===null?esc(tx("unavailable")):`${fmt(n,0)}%`}</strong><div class="meter ${type}" style="--value:${n===null?0:Math.max(0,Math.min(100,n))}%"><span></span></div></div>`; }
function noData(text=tx("noData")){ return `<div class="empty">${esc(text)}</div>`; }
function rawDetails(data){return "";}
function toast(message){ let el=document.querySelector(".toast"); if(!el){el=document.createElement("div");el.className="toast";document.body.append(el)}el.textContent=message;el.classList.remove("hidden");setTimeout(()=>el.classList.add("hidden"),2800); }

function selectorPage(){
  let ctx=getContext(); const validMarket=marketRecord(ctx.market); if(!validMarket){ctx.market=arr(assetsRegistry.markets)[0]?.id||""} if(ctx.symbol && !marketForSymbol(ctx.symbol))ctx.symbol="";
  let search="";
  const draw=()=>{
    const market=marketRecord(ctx.market); const assets=arr(market?.assets).map(a=>typeof a==="string"?{symbol:assetSymbol(a),name_ar:"",name_en:""}:{symbol:assetSymbol(a),name_ar:a.name_ar||a.arabic_name||a.label_ar||"",name_en:a.name_en||a.english_name||a.label_en||a.name||""}).filter(a=>a.symbol).filter(a=>`${a.symbol} ${a.name_ar||""} ${a.name_en||""}`.toLowerCase().includes(search.toLowerCase()));
    const steps=[ctx.market,ctx.symbol,ctx.timeframe,ctx.analysis_mode,ctx.view_mode];
    const marketHtml=arr(assetsRegistry.markets).map(m=>`<button class="marketBtn ${ctx.market===m.id?"selected":""}" data-market="${esc(m.id)}"><b>${esc(lang==="ar"?(m.name_ar||m.id):(m.name_en||m.id))}</b><small>${arr(m.assets).length} ${lang==="ar"?"أصل":"assets"}</small></button>`).join("");
    const assetHtml=assets.map(a=>`<button class="assetBtn ${normalizeSymbol(ctx.symbol)===normalizeSymbol(a.symbol)?"selected":""}" data-asset="${esc(a.symbol)}"><b>${esc(a.symbol)}</b><small>${esc(lang==="ar"?(a.name_ar||market?.name_ar||""):(a.name_en||market?.name_en||""))}</small></button>`).join("")||noData();
    const content=`${pageHero(tx("selectorTitle"),tx("selectorDesc"),`<a class="btn" href="https://www.ndsp.app/">${tx("officialLanding")}</a><a class="btn" href="/login/">${tx("login")}</a>`)}
      <div class="stepper">${steps.map((v,i)=>`<div class="step ${v?"done":""} ${!v&&steps.slice(0,i).every(Boolean)?"active":""}"><b>0${i+1}</b>${esc([tx("market"),tx("asset"),tx("timeframe"),tx("analysisMode"),tx("viewMode")][i])}</div>`).join("")}</div>
      <div class="grid grid2"><section class="card span2"><div class="cardHead"><div><h2>${tx("selectMarket")}</h2><p>${lang==="ar"?"السوق يحدد سجل الأصول ومصادر البيانات والقواعد المتاحة.":"The market controls the asset registry, sources and available rules."}</p></div></div><div class="marketGrid">${marketHtml}</div></section>
      <section class="card span2"><div class="cardHead"><div><h2>${tx("selectAsset")}</h2><p>${lang==="ar"?"اختيار أصل جديد ينشئ جلسة جديدة ويلغي أي بيانات قرار محفوظة للأصل السابق.":"Selecting a new asset creates a new session and discards previous decision data."}</p></div></div><div class="assetTools"><input class="input" id="assetSearch" placeholder="${tx("searchAsset")}" value="${esc(search)}"></div><div class="assetList">${assetHtml}</div></section>
      <section class="card"><div class="cardHead"><div><h2>${tx("selectTimeframe")}</h2></div></div><div class="segmented timeframeSegmented" data-ndsp-native-timeframe-grid="true">${["15m","1h","4h","daily","weekly","monthly"].map(x=>`<button class="segBtn ${ctx.timeframe===x?"selected":""}" data-timeframe="${x}" aria-pressed="${ctx.timeframe===x?"true":"false"}">${timeframeLabel(x)}</button>`).join("")}</div></section>
      <section class="card"><div class="cardHead"><div><h2>${tx("selectReading")}</h2></div></div><div class="segmented">${["investment","speculative"].map(x=>`<button class="segBtn ${ctx.analysis_mode===x?"selected":""}" data-mode="${x}">${tx(x)}</button>`).join("")}</div></section>
      <section class="card span2"><div class="cardHead"><div><h2>${tx("selectView")}</h2><p>${lang==="ar"?"العرض يغيّر كمية التفاصيل فقط ولا يغيّر قيمة القرار.":"View level changes detail only and never changes scientific values."}</p></div></div><div class="segmented">${["beginner","professional"].map(x=>`<button class="segBtn ${ctx.view_mode===x?"selected":""}" data-view="${x}">${tx(x)}</button>`).join("")}</div></section></div>
      <div class="selectionSummary"><div><b>${tx("selectedContext")}</b><div class="summaryTokens"><span class="token">${esc(ctx.market||"—")}</span><span class="token">${esc(ctx.symbol||"—")}</span><span class="token">${esc(ctx.timeframe||"—")}</span><span class="token">${esc(ctx.analysis_mode?tx(ctx.analysis_mode):"—")}</span><span class="token">${esc(ctx.view_mode?tx(ctx.view_mode):"—")}</span></div></div><button class="btn btnGold" id="startAnalysis">${tx("start")}</button></div>`;
    shell(content,"selector",ctx);
    document.querySelectorAll("[data-market]").forEach(b=>b.onclick=()=>{ctx.market=b.dataset.market;ctx.symbol="";ctx.session_id="";draw()});
    document.querySelectorAll("[data-asset]").forEach(b=>b.onclick=()=>{ctx.symbol=normalizeSymbol(b.dataset.asset);ctx.session_id="";draw()});
    document.querySelectorAll("[data-timeframe]").forEach(b=>b.onclick=()=>{ctx.timeframe=b.dataset.timeframe;ctx.session_id="";draw()});
    document.querySelectorAll("[data-mode]").forEach(b=>b.onclick=()=>{ctx.analysis_mode=b.dataset.mode;ctx.session_id="";draw()});
    document.querySelectorAll("[data-view]").forEach(b=>b.onclick=()=>{ctx.view_mode=b.dataset.view;draw()});
    document.getElementById("assetSearch")?.addEventListener("input",e=>{search=e.target.value;draw()});
    document.getElementById("startAnalysis")?.addEventListener("click",()=>{if(!contextComplete(ctx)){toast(tx("incompleteSelection"));return}ctx.session_id=newSession(ctx);saveContext(ctx);location.href=routeHref("home",ctx)});
  }; draw();
}

function assertContextOrRedirect(page){ const ctx=getContext(); if(page!=="selector"&&!contextComplete(ctx)){ location.replace(`${ROUTES.selector.path}?return=${encodeURIComponent(location.pathname)}`); return null } saveContext(ctx); return ctx; }

function humanizeText(value){
  if(value===null||value===undefined)return "";
  let s=String(value).trim();
  if(!s)return "";
  const key=s.toUpperCase().replace(/[\s-]+/g,"_");
  const arMap={
    MISSING_CANONICAL_COT_DIRECTIONS:"بيانات اتجاهات التموضع المؤسسي المطلوبة غير مكتملة.",
    NMP_NOT_CONFIRMED:"لم تتأكد NMP بعد.",
    NMP_PENDING:"NMP ما زالت قيد التحقق.",
    CORRECTION_NOT_CONFIRMED:"بوابة التصحيح لم تتأكد بعد.",
    DATA_INCOMPLETE:"البيانات المطلوبة غير مكتملة.",
    INPUTS_INCOMPLETE:"مدخلات القراءة غير مكتملة.",
    NOT_EVALUATED:"لم تكتمل عملية التقييم.",
    UNDER_MONITORING:"تحت المتابعة.",
    MONITORING_ONLY:"متابعة فقط.",
    GOVERNED_COMPLETED_CONTEXT:"سياق مكتمل ومحكوم.",
    GOVERNED_BULLISH_CONTEXT_UNDER_MONITORING:"سياق صاعد محكوم تحت المتابعة.",
    GOVERNED_BEARISH_CONTEXT_UNDER_MONITORING:"سياق هابط محكوم تحت المتابعة."
  };
  if(lang==="ar"&&arMap[key])return arMap[key];
  if(lang==="ar"){
    s=s.replace(/Governed bullish context under monitoring/gi,"سياق صاعد محكوم تحت المتابعة")
       .replace(/Governed bearish context under monitoring/gi,"سياق هابط محكوم تحت المتابعة")
       .replace(/Governed completed context/gi,"سياق مكتمل ومحكوم")
       .replace(/under monitoring/gi,"تحت المتابعة")
       .replace(/bullish/gi,"صاعد")
       .replace(/bearish/gi,"هابط")
       .replace(/monitoring only/gi,"متابعة فقط");
    if(/^[A-Z0-9_:-]{6,}$/.test(s))return "شرط تحقق داخلي لم يكتمل بعد.";
  }else if(/^[A-Z0-9_:-]{6,}$/.test(s)){
    return s.replace(/_/g," ").toLowerCase().replace(/\b\w/g,c=>c.toUpperCase());
  }
  return s;
}
function humanizeValue(value){
  if(Array.isArray(value))return value.map(humanizeValue).filter(Boolean).join(" · ");
  if(value&&typeof value==="object")return humanizeText(value.message||value.reason||value.description||value.code||value.state||"");
  return humanizeText(value);
}
function responseContext(data){
  const symbol=normalizeSymbol(pick(deepGet(data,["instrument.symbol","asset.symbol","symbol","asset_id","data.instrument.symbol","data.symbol","data.asset_id","decision.symbol","decision.asset_id","record.symbol","record.asset_id"]),""));
  const timeframe=normalizeTimeframe(pick(deepGet(data,["instrument.timeframe","asset.timeframe","timeframe","data.instrument.timeframe","data.timeframe","decision.timeframe","record.timeframe"]),""));
  const analysisMode=String(pick(deepGet(data,["analysis_mode","mode","data.analysis_mode","decision.analysis_mode","request_meta.analysis_mode"]),"")||"").toLowerCase();
  return {symbol,timeframe,analysisMode};
}
function validateResponse(data,ctx,options={}){
  const got=responseContext(data);
  const requireSymbol=options.requireSymbol===true;
  const requireTimeframe=options.requireTimeframe===true;
  const symbolDeclared=!!got.symbol;
  const timeframeDeclared=!!got.timeframe&&got.timeframe!=="unspecified";
  const modeDeclared=!!got.analysisMode;
  const symbolOk=(!requireSymbol&&!symbolDeclared)||(symbolDeclared&&got.symbol===normalizeSymbol(ctx.symbol));
  const timeframeOk=(!requireTimeframe&&!timeframeDeclared)||(timeframeDeclared&&got.timeframe===normalizeTimeframe(ctx.timeframe));
  const modeOk=!modeDeclared||got.analysisMode===String(ctx.analysis_mode||"").toLowerCase();
  return {ok:symbolOk&&timeframeOk&&modeOk,got,expected:{symbol:ctx.symbol,timeframe:ctx.timeframe,analysisMode:ctx.analysis_mode},symbolOk,timeframeOk,modeOk,symbolDeclared,timeframeDeclared,modeDeclared};
}
function recordContext(record){
  const d=record?.decision||record||{};
  return responseContext(d);
}
function recordMatchesContext(record,ctx){
  const got=recordContext(record);
  if(!got.symbol||got.symbol!==normalizeSymbol(ctx.symbol))return false;
  if(got.timeframe&&got.timeframe!=="unspecified"&&got.timeframe!==normalizeTimeframe(ctx.timeframe))return false;
  if(got.analysisMode&&got.analysisMode!==String(ctx.analysis_mode||"").toLowerCase())return false;
  return true;
}

async function fetchTimed(name,url){
  const start=performance.now(); let status=0,data=null,error=""; const ctx=getContext();
  try{
    const res=await fetch(url,{cache:"no-store",headers:{
      Accept:"application/json",
      "X-NDSP-Context-Session":ctx.session_id||"",
      "X-NDSP-Market":ctx.market||"",
      "X-NDSP-Symbol":ctx.symbol||"",
      "X-NDSP-Timeframe":ctx.timeframe||"",
      "X-NDSP-Analysis-Mode":ctx.analysis_mode||"",
      "X-NDSP-View-Mode":ctx.view_mode||""
    }});
    status=res.status; const body=await res.text();
    try{data=JSON.parse(body)}catch{data={raw:body.slice(0,1500)}}
    if(!res.ok)error=`HTTP ${status}`;
  }catch(e){error=e.message}
  const latency=Math.round(performance.now()-start); const row={name,url,status,latency,error,data}; endpointTelemetry.push(row); return row;
}
async function fetchDecisionBundle(ctx,force=false){
  const contextKey=[ctx.market,ctx.symbol,ctx.timeframe,ctx.analysis_mode,ctx.view_mode,ctx.session_id].join("|");
  if(lastBundle&&!force&&lastBundle.contextKey===contextKey)return lastBundle;
  endpointTelemetry=[];
  const q=new URLSearchParams({market:ctx.market,symbol:ctx.symbol,timeframe:ctx.timeframe,analysis_mode:ctx.analysis_mode,mode:ctx.analysis_mode,view_mode:ctx.view_mode,session_id:ctx.session_id,_:Date.now()});
  const rows=await Promise.all([
    fetchTimed("quality-live",`/api/decision/quality-live?${q}`),
    fetchTimed("api-health","/api/health")
  ]);
  const quality=rows[0].data||{},health=rows[1].data||{};
  const primary=quality?.data||quality;
  const validation=validateResponse(primary,ctx,{requireSymbol:true,requireTimeframe:true});
  lastBundle={
    contextKey,
    ctx,
    quality:primary,
    levels:{},
    current:{},
    history:{},
    health,
    validation,
    telemetry:rows,
    loadedAt:new Date().toISOString()
  };
  return lastBundle;
}

async function fetchCompletedRecords(ctx){
  const q=new URLSearchParams({
    market:ctx.market,
    symbol:ctx.symbol,
    timeframe:ctx.timeframe,
    analysis_mode:ctx.analysis_mode,
    mode:ctx.analysis_mode,
    view_mode:ctx.view_mode,
    session_id:ctx.session_id,
    _:Date.now()
  });
  const collectionRow=await fetchTimed(
    "completed-collection",
    `/api/completed-decisions?${q}`
  );
  const collection=collectionRow.data||{};
  return {
    current:{},
    history:collection,
    rows:[collectionRow],
    unauthorized:
      collectionRow.status===401||
      collectionRow.status===403,
    failed:
      collectionRow.status>=400&&
      collectionRow.status!==401&&
      collectionRow.status!==403
  };
}

/* NDSP_CONTRACT_CONSUMER_V125_BEGIN */
window.__NDSP_CONTRACT_CONSUMER_V125__={version:"124.0.0",build:"20260717_223240",mode:"native-core-contract-consumer",noCrossTimeframeFallback:true,noResponseFabrication:true};
function timeframeLabelV125(value){
  const tf=normalizeTimeframe(value);
  const ar={"15m":"15 دقيقة","1h":"ساعة","4h":"4 ساعات",daily:"يومي",weekly:"أسبوعي",monthly:"شهري"};
  const en={"15m":"15 min","1h":"1 hour","4h":"4 hours",daily:"Daily",weekly:"Weekly",monthly:"Monthly"};
  return (lang==="ar"?ar:en)[tf]||tf||tx("unknown");
}
function publicTextV125LegacyV129(value){
  let out=String(value??"").replace(/\u200f|\u200e/g,"").trim();
  const replacements=[
    [/GOVERNED_REDACTED/gi,lang==="ar"?"محجوبة حسب صلاحية العرض":"Redacted by view policy"],
    [/INPUTS_INCOMPLETE/gi,lang==="ar"?"مدخلات غير مكتملة":"Inputs incomplete"],
    [/UNDER_MONITORING/gi,lang==="ar"?"تحت المتابعة":"Under monitoring"],
    [/MONITORING_ONLY/gi,lang==="ar"?"متابعة فقط":"Monitoring only"],
    [/UNDER_REVIEW/gi,lang==="ar"?"تحت المراجعة":"Under review"],
    [/PARTIAL_AVAILABLE/gi,lang==="ar"?"متاحة جزئيًا":"Partially available"],
    [/NOT_EVALUATED/gi,lang==="ar"?"لم تُقيّم":"Not evaluated"],
    [/DATA_BLOCKED/gi,lang==="ar"?"محجوبة بسبب البيانات":"Data blocked"]
  ];
  replacements.forEach(([pattern,label])=>{out=out.replace(pattern,label)});
  return out.replace(/\s+/g," ").trim();
}
function layerIdentifierV125(layer){
  return String(pick(layer?.layer_id,layer?.id,layer?.canonical_id,layer?.code,layer?.layer_code,"")||"").toUpperCase();
}
function layerByCodeV125(layers,code){
  const target=String(code||"").toUpperCase();
  return arr(layers).find(layer=>{
    const id=layerIdentifierV125(layer);
    return id===target||id.endsWith(target)||String(layer?.canonical_name||"").toUpperCase()===target;
  })||{};
}
function layerRawStateV125(layer){
  return pick(layer?.state,layer?.status,layer?.layer_state,layer?.runtime_state,layer?.availability,layer?.decision_state,layer?.result_state,"");
}
function layerStateV125(layer){
  return statusLabel(layerRawStateV125(layer)||"NOT_EVALUATED");
}
function layerScoreV125(layer){
  const rawState=String(layerRawStateV125(layer)||"").toUpperCase();
  if(rawState.includes("REDACTED"))return null;
  const candidates=[layer?.confidence,layer?.confidence_score,layer?.completion,layer?.completion_score,layer?.score,layer?.readiness,layer?.readiness_score,layer?.strength,layer?.strength_score,layer?.quality,layer?.quality_score];
  for(const value of candidates){
    const n=Number(value);
    if(Number.isFinite(n))return Math.max(0,Math.min(100,n));
  }
  if(typeof layer?.value==="number"&&Number.isFinite(layer.value))return Math.max(0,Math.min(100,layer.value));
  if(typeof layer?.value==="string"&&/^\s*\d+(?:\.\d+)?\s*%?\s*$/.test(layer.value)){
    const n=Number(layer.value.replace("%",""));
    if(Number.isFinite(n))return Math.max(0,Math.min(100,n));
  }
  return null;
}
function layerReasonsV125(layer){
  const values=[];
  const arrays=[layer?.reasons,layer?.reason_codes,layer?.messages,layer?.blockers,layer?.evidence];
  arrays.forEach(items=>arr(items).forEach(item=>{
    const value=typeof item==="string"?item:pick(item?.message_ar,item?.message,item?.reason_ar,item?.reason,item?.summary_ar,item?.summary,item?.code,"");
    if(value)values.push(publicTextV125(value));
  }));
  [layer?.reason_ar,layer?.reason,layer?.summary_ar,layer?.summary,layer?.explanation_ar,layer?.explanation,layer?.message,layer?.unavailable_reason].forEach(value=>{if(value)values.push(publicTextV125(value))});
  return [...new Set(values.filter(Boolean))];
}
function layerReceivedV125(layer){return Boolean(layer&&typeof layer==="object"&&Object.keys(layer).length)}
function layerNarrativeV125(layer,frame){
  if(!layerReceivedV125(layer))return lang==="ar"?`عقد الطبقة غير مستلم لفريم ${timeframeLabelV125(frame)}.`:`Layer contract was not received for ${timeframeLabelV125(frame)}.`;
  const raw=String(layerRawStateV125(layer)||"").toUpperCase();
  const state=layerStateV125(layer);
  const score=layerScoreV125(layer);
  const reasons=layerReasonsV125(layer);
  if(raw.includes("GOVERNED_REDACTED"))return lang==="ar"?"الطبقة مرتبطة بالفريم، لكن تفاصيلها محجوبة وفق سياسة العرض الحالية.":"The layer is bound to the timeframe, but details are redacted by the current view policy.";
  if(raw.includes("INPUTS_INCOMPLETE")){
    const detail=reasons[0]|| (lang==="ar"?"مدخلات الطبقة لم تكتمل بعد لهذا الفريم.":"The layer inputs are not complete for this timeframe yet.");
    return score===null?`${state} · ${detail}`:`${state} · ${Math.round(score)}% · ${detail}`;
  }
  if(reasons.length)return reasons.slice(0,2).join(" · ");
  if(score!==null)return `${state} · ${Math.round(score)}%`;
  return state|| (lang==="ar"?"العقد مستلم لهذا الفريم.":"The contract was received for this timeframe.");
}
function cleanBlockersV125(values,state,readiness,l16){
  const source=Array.isArray(values)?values:(values===undefined||values===null||values===""?[]:[values]);
  let list=source.map(item=>publicTextV125(typeof item==="string"?item:pick(item?.message_ar,item?.message,item?.reason_ar,item?.reason,item?.code,JSON.stringify(item)))).filter(Boolean);
  if(readiness!==null&&readiness>0){
    list=list.filter(value=>{
      const normalized=String(value||"").replace(/[٠-٩]/g,d=>String("٠١٢٣٤٥٦٧٨٩".indexOf(d))).replace(/٫/g,".");
      const mentionsReadiness=/جاهزية|readiness/i.test(normalized);
      const mentionsZero=/(^|[^0-9])0(?:\.0+)?\s*[%٪]/.test(normalized);
      return !(mentionsReadiness&&mentionsZero);
    });
  }
  if(!list.length)list=layerReasonsV125(l16);
  if(!list.length&&String(state||"").toUpperCase().includes("MONITOR")&&readiness!==null){
    list=[lang==="ar"?`القراءة تحت المتابعة؛ الجاهزية الحالية ${Math.round(readiness)}% ولم تستوفِ جميع شروط الاكتمال.`:`The reading is under monitoring; current readiness is ${Math.round(readiness)}% and not all completion conditions are satisfied.`];
  }
  return list;
}
function completionReasonV125(x){
  const strength=num(x?.quality);
  const readiness=num(x?.readiness);
  const blockers=arr(x?.blockers).map(value=>publicTextV125(value)).filter(Boolean);
  const blocker=blockers[0]||"";
  if(lang==="ar"){
    if(strength!==null&&readiness!==null)return `القراءة لم تكتمل بعد؛ قوة الأدلة الحالية ${Math.round(strength)}%، بينما جاهزية القرار ${Math.round(readiness)}%. ${blocker?`السبب الحاكم: ${blocker}`:"ما زالت بعض شروط الاكتمال قيد المتابعة في السياق الحالي."}`;
    if(readiness!==null)return `القراءة لم تكتمل بعد؛ جاهزية القرار الحالية ${Math.round(readiness)}%. ${blocker?`السبب الحاكم: ${blocker}`:"ما زالت بعض شروط الاكتمال قيد المتابعة في السياق الحالي."}`;
    if(strength!==null)return `القراءة لم تكتمل بعد؛ قوة الأدلة الحالية ${Math.round(strength)}%. ${blocker?`السبب الحاكم: ${blocker}`:"ما زالت بعض شروط الاكتمال قيد المتابعة في السياق الحالي."}`;
    return blocker||"القراءة لم تكتمل بعد لأن بعض شروط الاكتمال ما زالت قيد المتابعة في السياق الحالي.";
  }
  if(strength!==null&&readiness!==null)return `The reading is not complete yet; current evidence strength is ${Math.round(strength)}%, while decision readiness is ${Math.round(readiness)}%. ${blocker?`Governing reason: ${blocker}`:"Some completion conditions remain under monitoring."}`;
  if(readiness!==null)return `The reading is not complete yet; current decision readiness is ${Math.round(readiness)}%. ${blocker?`Governing reason: ${blocker}`:"Some completion conditions remain under monitoring."}`;
  if(strength!==null)return `The reading is not complete yet; current evidence strength is ${Math.round(strength)}%. ${blocker?`Governing reason: ${blocker}`:"Some completion conditions remain under monitoring."}`;
  return blocker||"The reading is not complete yet because some completion conditions remain under monitoring.";
}
/* NDSP_CONTRACT_CONSUMER_V125_END */

/* NDSP_STRENGTH_REFERENCE_LEVELS_V127_BEGIN */
window.__NDSP_STRENGTH_REFERENCE_LEVELS_V127__={version:"127.0.0",build:"20260718_110552",exactTimeframeOnly:true,noCrossTimeframeFallback:true,noResponseFabrication:true};
function valueAtPathV127(root,path){
  let cur=root;
  for(const key of String(path||"").split(".")){
    if(!cur||typeof cur!=="object"||!Object.prototype.hasOwnProperty.call(cur,key))return null;
    cur=cur[key];
  }
  return cur;
}
function normalizeNumericTextV127(value){
  return String(value??"")
    .replace(/[٠-٩]/g,d=>String("٠١٢٣٤٥٦٧٨٩".indexOf(d)))
    .replace(/٪/g,"%")
    .replace(/٬/g,",")
    .replace(/٫/g,".")
    .trim();
}
function numericValueV127(value,keys=["value","score","percent","percentage","strength","strength_score","reading_strength","quality","quality_score","decision_quality"]){
  if(value===null||value===undefined||typeof value==="boolean")return null;
  if(typeof value==="number")return Number.isFinite(value)?value:null;
  if(value&&typeof value==="object"&&!Array.isArray(value)){
    for(const key of keys){
      if(Object.prototype.hasOwnProperty.call(value,key)){
        const n=numericValueV127(value[key],keys);
        if(n!==null)return n;
      }
    }
    return null;
  }
  const raw=normalizeNumericTextV127(value).replace(/[%٪]/g,"").replace(/,/g,"");
  if(/^[-+]?\d+(?:\.\d+)?$/.test(raw)){
    const n=Number(raw);
    return Number.isFinite(n)?n:null;
  }
  return null;
}
function layerScoreCandidateV127(layer){
  if(!layer||typeof layer!=="object")return null;
  for(const key of ["confidence","confidence_score","completion","completion_score","score","value","percent","percentage","quality","quality_score","strength","strength_score","readiness","readiness_score"]){
    if(Object.prototype.hasOwnProperty.call(layer,key)){
      const n=numericValueV127(layer[key]);
      if(n!==null&&n>=0&&n<=100)return n;
    }
  }
  const output=layer.output;
  if(output&&typeof output==="object"&&!Array.isArray(output)){
    for(const key of ["score","value","percent","percentage","confidence","quality","quality_score","strength","strength_score"]){
      if(Object.prototype.hasOwnProperty.call(output,key)){
        const n=numericValueV127(output[key]);
        if(n!==null&&n>=0&&n<=100)return n;
      }
    }
  }
  return null;
}
function layerWeightV127(layer){
  for(const key of ["weight","layer_weight","contribution_weight","importance_weight","governance_weight"]){
    const n=numericValueV127(layer?.[key]);
    if(n!==null&&n>0)return n;
  }
  return 1;
}
function layerEligibleForStrengthV127(layer){
  const state=String(pick(layer?.state,layer?.status,layer?.layer_state,layer?.governed_state,layer?.public_state,"")).toUpperCase();
  const visibility=String(pick(layer?.visibility,layer?.public_visibility,"")).toUpperCase();
  return !["GOVERNED_REDACTED","REDACTED","HIDDEN","NOT_EVALUATED","UNAVAILABLE","NO_DATA"].some(token=>state.includes(token)||visibility.includes(token));
}
function strengthContractV127(d,summary,l16,layers){
  const candidates=[
    ["system_power_profile.overall_strength",valueAtPathV127(d,"system_power_profile.overall_strength")],
    ["system_power_profile.strength_score",valueAtPathV127(d,"system_power_profile.strength_score")],
    ["system_power_profile.strength",valueAtPathV127(d,"system_power_profile.strength")],
    ["system_power_profile.overall_score",valueAtPathV127(d,"system_power_profile.overall_score")],
    ["governance_summary.overall_strength",valueAtPathV127(d,"governance_summary.overall_strength")],
    ["governance_summary.strength_score",valueAtPathV127(d,"governance_summary.strength_score")],
    ["governance_summary.strength",valueAtPathV127(d,"governance_summary.strength")],
    ["governance_summary.reading_strength",valueAtPathV127(d,"governance_summary.reading_strength")],
    ["governance_summary.system_power_profile.overall_strength",valueAtPathV127(d,"governance_summary.system_power_profile.overall_strength")],
    ["governance_summary.system_power_profile.strength_score",valueAtPathV127(d,"governance_summary.system_power_profile.strength_score")],
    ["governance_summary.system_power_profile.strength",valueAtPathV127(d,"governance_summary.system_power_profile.strength")],
    ["governance_summary.system_power_profile.overall_score",valueAtPathV127(d,"governance_summary.system_power_profile.overall_score")],
    ["reading_maturity.overall_strength",valueAtPathV127(d,"reading_maturity.overall_strength")],
    ["reading_maturity.strength_score",valueAtPathV127(d,"reading_maturity.strength_score")],
    ["reading_maturity.strength",valueAtPathV127(d,"reading_maturity.strength")],
    ["final_summary.reading_strength",summary?.reading_strength],
    ["final_summary.strength_score",summary?.strength_score],
    ["final_summary.strength",summary?.strength],
    ["final_summary.decision_quality",summary?.decision_quality],
    ["decision_layers.L16.strength",l16?.strength],
    ["decision_layers.L16.strength_score",l16?.strength_score],
    ["decision_layers.L16.reading_strength",l16?.reading_strength],
    ["decision_layers.L16.evidence_strength",l16?.evidence_strength],
    ["decision_layers.L16.overall_strength",l16?.overall_strength],
    ["reading_strength",d?.reading_strength],
    ["strength_score",d?.strength_score],
    ["quality_score",d?.quality_score],
    ["decision_quality",d?.decision_quality]
  ].map(([source,raw])=>({source,value:numericValueV127(raw),eligibleCount:0,method:"explicit"})).filter(item=>item.value!==null&&item.value>=0&&item.value<=100);
  const positive=candidates.find(item=>item.value>0);
  if(positive)return positive;
  const eligible=arr(layers).filter(layer=>layerEligibleForStrengthV127(layer)).map(layer=>({score:layerScoreCandidateV127(layer),weight:layerWeightV127(layer)})).filter(item=>item.score!==null);
  if(eligible.length>=3){
    const totalWeight=eligible.reduce((sum,item)=>sum+item.weight,0);
    if(totalWeight>0){
      const value=eligible.reduce((sum,item)=>sum+(item.score*item.weight),0)/totalWeight;
      return{source:"decision_layers.weighted_non_redacted_mean",value,eligibleCount:eligible.length,method:"weighted_mean_non_redacted"};
    }
  }
  return candidates[0]||{source:"",value:null,eligibleCount:eligible.length,method:"unavailable"};
}
const LEVEL_PATHS_V127={
  activation:["scenario_levels.activation.value","scenario_levels.activation.level","scenario_levels.activation.price","scenario_levels.activation","reference_levels.activation.value","reference_levels.activation.level","reference_levels.activation.price","reference_levels.activation","scenario.scenario_activation_level","scenario.activation_level","scenario.activation","levels.activation","scenario_activation_level","activation_level"],
  arrival:["scenario_levels.arrival.value","scenario_levels.arrival.level","scenario_levels.arrival.price","scenario_levels.arrival","reference_levels.arrival.value","reference_levels.arrival.level","reference_levels.arrival.price","reference_levels.arrival","scenario.scenario_arrival_level","scenario.arrival_level","scenario.arrival","levels.arrival","scenario_arrival_level","arrival_level"],
  review:["scenario_levels.review.value","scenario_levels.review.level","scenario_levels.review.price","scenario_levels.review","scenario_levels.review_zone.value","scenario_levels.review_zone.level","scenario_levels.review_zone","reference_levels.review.value","reference_levels.review.level","reference_levels.review","scenario.scenario_review_level","scenario.scenario_review_zone","scenario.review_level","scenario.review_zone","scenario.review","levels.review","scenario_review_level","scenario_review_zone","review_level","review_zone"],
  invalidation:["scenario_levels.invalidation.value","scenario_levels.invalidation.level","scenario_levels.invalidation.price","scenario_levels.invalidation","scenario_levels.cancel.value","scenario_levels.cancel.level","scenario_levels.cancel.price","scenario_levels.cancel","reference_levels.invalidation.value","reference_levels.invalidation.level","reference_levels.invalidation","reference_levels.cancel.value","reference_levels.cancel.level","reference_levels.cancel","scenario.scenario_invalidation_level","scenario.invalidation_level","scenario.cancel_level","scenario.invalidation","levels.invalidation","scenario_invalidation_level","invalidation_level","cancel_level"]
};
function scenarioLevelContractV127(kind,d){
  for(const path of LEVEL_PATHS_V127[kind]||[]){
    const raw=valueAtPathV127(d,path);
    const value=numericValueV127(raw,["value","level","price","display_value","numeric_value"]);
    if(value!==null)return{value,source:path};
  }
  const levels=d?.scenario_levels;
  if(Array.isArray(levels)){
    const aliases={activation:["activation","trigger","التفعيل"],arrival:["arrival","الوصول"],review:["review","review_zone","المراجعة"],invalidation:["invalidation","cancel","cancellation","الإلغاء","الالغاء"]}[kind]||[];
    for(let index=0;index<levels.length;index+=1){
      const item=levels[index];
      if(!item||typeof item!=="object")continue;
      const identity=[item.type,item.kind,item.key,item.id,item.name,item.name_ar,item.name_en,item.label].filter(Boolean).join(" ").toLowerCase();
      if(aliases.some(alias=>identity.includes(String(alias).toLowerCase()))){
        const value=numericValueV127(item,["value","level","price","display_value","numeric_value"]);
        if(value!==null)return{value,source:`scenario_levels[${index}]`};
      }
    }
  }
  return{value:null,source:""};
}
function displayLevelV127(value){
  const n=numericValueV127(value,["value","level","price","display_value","numeric_value"]);
  return n===null?tx("unavailable"):fmt(n,2);
}
/* NDSP_STRENGTH_REFERENCE_LEVELS_V127_END */

/* NDSP_PROFESSIONAL_EXPLANATION_V128_BEGIN */
window.__NDSP_PROFESSIONAL_EXPLANATION_V128__={version:"128.0.0",build:"20260718_113003",exactTimeframeOnly:true,publicExplainabilityFirst:true,noCrossTimeframeFallback:true,noResponseFabrication:true};
function cleanProfessionalScalarV128(value){
  if(value===null||value===undefined||typeof value==="boolean"||typeof value==="number")return "";
  let text=publicTextV125(String(value).replace(/\u200f|\u200e/g,"").trim());
  const replacements=[
    [/BULLISH/gi,lang==="ar"?"ميل صاعد":"Bullish bias"],
    [/BEARISH/gi,lang==="ar"?"ميل هابط":"Bearish bias"],
    [/NEUTRAL/gi,lang==="ar"?"محايد":"Neutral"],
    [/ALLOWED/gi,lang==="ar"?"مسموح":"Allowed"],
    [/ARMED/gi,lang==="ar"?"مهيأ":"Armed"],
    [/BLOCKED/gi,lang==="ar"?"محجوب":"Blocked"],
    [/INCOMPLETE/gi,lang==="ar"?"غير مكتمل":"Incomplete"],
    [/COMPLETE/gi,lang==="ar"?"مكتمل":"Complete"]
  ];
  replacements.forEach(([pattern,label])=>{text=text.replace(pattern,label)});
  text=text.replace(/\s+/g," ").replace(/^[\s·|\-]+|[\s·|\-]+$/g,"").trim();
  if(!text||text==="[object Object]")return "";
  const numeric=text.replace(/[٠-٩]/g,d=>String("٠١٢٣٤٥٦٧٨٩".indexOf(d))).replace(/٪/g,"%").replace(/٬/g,",").replace(/٫/g,".");
  if(/^[-+]?\d+(?:[.,]\d+)?%?$/.test(numeric))return "";
  return text;
}
const PROFESSIONAL_KEYS_V128=[
  "professional_explanation_ar","professional_ar","decision_explanation_ar","public_summary_ar","summary_ar","narrative_ar","reasoning_ar","rationale_ar","explanation_ar","decision_rationale_ar","governing_rationale_ar","interpretation_ar","analysis_ar","public_text_ar","text_ar","message_ar","description_ar","reason_ar","reasons_ar","evidence_ar","key_evidence_ar",
  "professional_explanation","professional","decision_explanation","public_summary","summary","narrative","reasoning","rationale","explanation","decision_rationale","governing_rationale","interpretation","analysis","public_text","text","message","description","reason","reasons","evidence","key_evidence","what_it_means","why","context","direction","state","status","output","result"
];
const PROFESSIONAL_SKIP_KEYS_V128=new Set(["generated_at","updated_at","timestamp","timeframe","symbol","market","source","source_mode","version","id","code","key","weight","score","confidence","percentage","percent","active","enabled","ok"]);
function collectProfessionalFragmentsV128(value,depth=0,output=[],seen=new Set()){
  if(value===null||value===undefined||depth>5||output.length>=12)return output;
  if(typeof value==="string"||typeof value==="number"||typeof value==="boolean"){
    const text=cleanProfessionalScalarV128(value);
    const key=text.replace(/\s+/g," ").toLowerCase();
    if(text&&!seen.has(key)){
      seen.add(key);
      output.push(text.slice(0,500));
    }
    return output;
  }
  if(Array.isArray(value)){
    value.slice(0,16).forEach(item=>collectProfessionalFragmentsV128(item,depth+1,output,seen));
    return output;
  }
  if(typeof value==="object"){
    const processed=new Set();
    PROFESSIONAL_KEYS_V128.forEach(key=>{
      if(output.length>=12)return;
      if(Object.prototype.hasOwnProperty.call(value,key)){
        processed.add(key);
        collectProfessionalFragmentsV128(value[key],depth+1,output,seen);
      }
    });
    if(!output.length||depth>0){
      Object.entries(value).slice(0,32).forEach(([key,item])=>{
        if(output.length>=12||processed.has(key)||key.startsWith("_")||PROFESSIONAL_SKIP_KEYS_V128.has(String(key).toLowerCase()))return;
        collectProfessionalFragmentsV128(item,depth+1,output,seen);
      });
    }
  }
  return output;
}
function professionalExplanationContractV128(d,summary,layers,frame){
  const candidates=[
    ["public_explainability.professional_explanation_ar",valueAtPathV127(d,"public_explainability.professional_explanation_ar")],
    ["public_explainability.professional_explanation",valueAtPathV127(d,"public_explainability.professional_explanation")],
    ["public_explainability.professional_ar",valueAtPathV127(d,"public_explainability.professional_ar")],
    ["public_explainability.professional",valueAtPathV127(d,"public_explainability.professional")],
    ["public_explainability.decision_explanation_ar",valueAtPathV127(d,"public_explainability.decision_explanation_ar")],
    ["public_explainability.decision_explanation",valueAtPathV127(d,"public_explainability.decision_explanation")],
    ["public_explainability.summary_ar",valueAtPathV127(d,"public_explainability.summary_ar")],
    ["public_explainability.summary",valueAtPathV127(d,"public_explainability.summary")],
    ["public_explainability.narrative_ar",valueAtPathV127(d,"public_explainability.narrative_ar")],
    ["public_explainability.narrative",valueAtPathV127(d,"public_explainability.narrative")],
    ["public_explainability.reasoning_ar",valueAtPathV127(d,"public_explainability.reasoning_ar")],
    ["public_explainability.reasoning",valueAtPathV127(d,"public_explainability.reasoning")],
    ["public_explainability.explanation_ar",valueAtPathV127(d,"public_explainability.explanation_ar")],
    ["public_explainability.explanation",valueAtPathV127(d,"public_explainability.explanation")],
    ["public_explainability.rationale_ar",valueAtPathV127(d,"public_explainability.rationale_ar")],
    ["public_explainability.rationale",valueAtPathV127(d,"public_explainability.rationale")],
    ["public_explainability",d?.public_explainability],
    ["explainability.professional_explanation_ar",valueAtPathV127(d,"explainability.professional_explanation_ar")],
    ["explainability.professional_explanation",valueAtPathV127(d,"explainability.professional_explanation")],
    ["explainability.professional_ar",valueAtPathV127(d,"explainability.professional_ar")],
    ["explainability.professional",valueAtPathV127(d,"explainability.professional")],
    ["explainability.summary_ar",valueAtPathV127(d,"explainability.summary_ar")],
    ["explainability.summary",valueAtPathV127(d,"explainability.summary")],
    ["explainability.narrative_ar",valueAtPathV127(d,"explainability.narrative_ar")],
    ["explainability.narrative",valueAtPathV127(d,"explainability.narrative")],
    ["explainability.reasoning_ar",valueAtPathV127(d,"explainability.reasoning_ar")],
    ["explainability.reasoning",valueAtPathV127(d,"explainability.reasoning")],
    ["explainability.explanation_ar",valueAtPathV127(d,"explainability.explanation_ar")],
    ["explainability.explanation",valueAtPathV127(d,"explainability.explanation")],
    ["explainability.rationale_ar",valueAtPathV127(d,"explainability.rationale_ar")],
    ["explainability.rationale",valueAtPathV127(d,"explainability.rationale")],
    ["explainability",d?.explainability],
    ["professional_explanation",d?.professional_explanation],
    ["final_summary.professional_explanation",summary?.professional_explanation],
    ["public_explanation",d?.public_explanation],
    ["rationale",d?.rationale],
    ["golden_reason_public",d?.golden_reason_public],
    ["golden_evidence_public",d?.golden_evidence_public],
    ["decision_layers.L16.reasons",layerReasonsV125(layerByCodeV125(layers,"L16"))]
  ];
  for(const [source,value] of candidates){
    const fragments=collectProfessionalFragmentsV128(value);
    const text=fragments.join(" · ").trim().slice(0,3000);
    if(text.length>=12){
      let raw="";
      try{raw=JSON.stringify(value)||""}catch(_){raw=String(value??"")}
      return{source,text,sectionCount:fragments.length,redacted:/GOVERNED_REDACTED/i.test(raw)||/محجوبة حسب صلاحية العرض|Redacted by view policy/i.test(text),frame};
    }
  }
  return{source:"",text:"",sectionCount:0,redacted:false,frame};
}
function professionalExplanationHtmlV128(x){
  const available=typeof x?.professional==="string"&&x.professional.trim().length>=12;
  const frameLabel=timeframeLabelV125(x?.frame);
  const text=available?x.professional:tx("noData");
  const note=available?(lang==="ar"?`مرتبط بعقد التفسير المحكوم لفريم ${frameLabel}`:`Bound to the governed ${frameLabel} explanation contract`):"";
  return `<div class="ndsp-v128-pro-body"><p class="decisionNarrative ndsp-v128-pro-narrative">${esc(text)}</p>${note?`<small class="ndsp-v128-pro-contract-note">${esc(note)}</small>`:""}</div>`;
}
/* NDSP_PROFESSIONAL_EXPLANATION_V128_END */

/* NDSP_PUBLIC_EXPLANATION_MODE_GUARD_V129_BEGIN */
window.__NDSP_PUBLIC_EXPLANATION_MODE_GUARD_V129__={version:"129.0.0",build:"20260718_120631",exactTimeframeOnly:true,exclusiveSelectedMode:true,publicVocabularyOnly:true,rawContractHidden:true,noCrossTimeframeFallback:true,noResponseFabrication:true};
const NDSP_V129_FORBIDDEN_PUBLIC_TERMS=/\bCOT\b|RAW[_\s-]*COT|COMMITMENTS?\s+OF\s+TRADERS?|ASSET\s+MANAGERS?|LEVERAGED\s+FUNDS?|NON[-\s]?COMMERCIALS?|DEALER\s+INTERMEDIAR(?:Y|IES)|SWAP\s+DEALERS?|TDL[-_\s]*(?:M\s*&\s*L|S)\b|PUBLIC_EXPLAINABILITY|SOURCE_MODE|GOVERNANCE_PROJECTION_VERSION|CAPABILITY_RUNTIME_EVIDENCE_VERSION|DECISION_LAYERS?\s*\[\s*\d+\s*\]|GOVERNED_REDACTED|INPUTS_INCOMPLETE|UNDER_MONITORING|MONITORING_ONLY|UNDER_REVIEW|PARTIAL_AVAILABLE|NOT_EVALUATED|DATA_BLOCKED/gi;
function sanitizePublicNarrativeV129(value){
  let text=String(value??"").replace(/\u200f|\u200e/g,"").trim();
  const ar=lang==="ar";
  const rules=[
    [/RAW[_\s-]*COT/gi,ar?"البيانات الحاكمة":"governing data"],
    [/\bCOT\b/gi,ar?"البيانات الحاكمة":"governing data"],
    [/COMMITMENTS?\s+OF\s+TRADERS?/gi,ar?"بيانات السوق الحاكمة":"governing market data"],
    [/ASSET\s+MANAGERS?/gi,ar?"الفئة المؤسسية طويلة الأجل":"long-horizon institutional category"],
    [/LEVERAGED\s+FUNDS?/gi,ar?"الفئة المضاربية":"speculative category"],
    [/NON[-\s]?COMMERCIALS?/gi,ar?"الفئة غير التجارية":"non-commercial category"],
    [/DEALER\s+INTERMEDIAR(?:Y|IES)/gi,ar?"فئة الوساطة المؤسسية":"institutional intermediary category"],
    [/SWAP\s+DEALERS?/gi,ar?"فئة التحوط المؤسسي":"institutional hedging category"],
    [/TDL[-_\s]*(?:M\s*&\s*L|S)\b/gi,ar?"منطق القرار الزمني":"temporal decision logic"],
    [/GOVERNED_REDACTED/gi,ar?"محجوبة وفق صلاحية العرض":"redacted by view policy"],
    [/INPUTS_INCOMPLETE/gi,ar?"مدخلات غير مكتملة":"inputs incomplete"],
    [/UNDER_MONITORING|MONITORING_ONLY/gi,ar?"تحت المتابعة":"under monitoring"],
    [/UNDER_REVIEW/gi,ar?"تحت المراجعة":"under review"],
    [/PARTIAL_AVAILABLE/gi,ar?"متاحة جزئيًا":"partially available"],
    [/NOT_EVALUATED/gi,ar?"لم تُقيّم":"not evaluated"],
    [/DATA_BLOCKED/gi,ar?"محجوبة بسبب نقص البيانات":"blocked by missing data"],
    [/PUBLIC_EXPLAINABILITY|SOURCE_MODE|GOVERNANCE_PROJECTION_VERSION|CAPABILITY_RUNTIME_EVIDENCE_VERSION/gi,""],
    [/DECISION_LAYERS?\s*\[\s*\d+\s*\]/gi,""],
    [/NDSP-CORE-L\d+/gi,""],
    [/\b(?:BULLISH)\b/gi,ar?"ميل صاعد":"bullish bias"],
    [/\b(?:BEARISH)\b/gi,ar?"ميل هابط":"bearish bias"],
    [/\b(?:NEUTRAL)\b/gi,ar?"توازن":"balanced"],
    [/\b(?:BLOCKED)\b/gi,ar?"محجوبة":"blocked"],
    [/\b(?:INCOMPLETE)\b/gi,ar?"غير مكتملة":"incomplete"],
    [/\b(?:COMPLETE)\b/gi,ar?"مكتملة":"complete"]
  ];
  rules.forEach(([pattern,replacement])=>{text=text.replace(pattern,replacement)});
  text=text.replace(/\b[A-Z][A-Z0-9_]{3,}\b/g,match=>match.includes("_")?"":match);
  text=text.replace(/\s*·\s*·+/g," · ").replace(/\s*[|]+\s*/g," · ").replace(/\s+/g," ").replace(/^[\s·|\-:]+|[\s·|\-:]+$/g,"").trim();
  return text;
}
function publicTextV125(value){return sanitizePublicNarrativeV129(publicTextV125LegacyV129(value));}
function sanitizeRenderedPublicTextV129(root){
  if(!root||typeof document==="undefined")return;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
  const nodes=[];let node;
  while((node=walker.nextNode())){const parent=node.parentElement;const tag=parent?.tagName||"";if(tag!=="SCRIPT"&&tag!=="STYLE")nodes.push(node);}
  nodes.forEach(textNode=>{const before=textNode.nodeValue||"";const after=sanitizePublicNarrativeV129(before);if(after!==before)textNode.nodeValue=after;});
}
if(typeof MutationObserver!=="undefined"&&typeof app!=="undefined"&&app){
  let busy=false;
  const observer=new MutationObserver(()=>{if(busy)return;busy=true;try{sanitizeRenderedPublicTextV129(app)}finally{busy=false}});
  observer.observe(app,{childList:true,subtree:true,characterData:true});
}
function strictPublicValueV129(value,depth=0){
  if(value===null||value===undefined||depth>3)return "";
  if(typeof value==="string"||typeof value==="number")return sanitizePublicNarrativeV129(value);
  if(Array.isArray(value))return value.map(item=>strictPublicValueV129(item,depth+1)).filter(Boolean).slice(0,2).join(" · ");
  if(typeof value==="object"){
    const keys=lang==="ar"?["summary_ar","message_ar","reason_ar","narrative_ar","description_ar","explanation_ar","public_text_ar","summary","message","reason","narrative","description","explanation","public_text"]:["summary","message","reason","narrative","description","explanation","public_text","summary_ar","message_ar","reason_ar"];
    for(const key of keys){if(Object.prototype.hasOwnProperty.call(value,key)){const text=strictPublicValueV129(value[key],depth+1);if(text)return text;}}
  }
  return "";
}
function percentTextV129(value){const n=num(value);return n===null?"":`${Math.round(n)}%`;}
function levelTextV129(value){const n=numericValueV127(value,["value","level","price","display_value","numeric_value"]);return n===null?"":fmt(n,2);}
function completedStateV129(state){return /(?:^|_)(?:COMPLETE|COMPLETED|EXECUTED|GOLDEN_ALIGNMENT)(?:$|_)/i.test(String(state||""));}
function explanationDifferenceV129(strength,readiness){
  if(strength===null||readiness===null)return lang==="ar"?"لا تتوفر قيمة مكتملة للمقارنة بين قوة القراءة وجاهزية القرار.":"A complete comparison between reading strength and decision readiness is not available.";
  const gap=Math.round(strength-readiness);
  if(gap>=5)return lang==="ar"?"قوة الأدلة أعلى من جاهزية القرار؛ توجد قراءة قابلة للفهم، لكن شروط الاكتمال ما زالت غير مكتملة.":"Evidence strength is higher than decision readiness; the reading is interpretable, but completion conditions remain unmet.";
  if(gap<=-5)return lang==="ar"?"جاهزية القرار أعلى من تماسك الأدلة؛ لذلك لا تكفي الجاهزية وحدها لاعتماد الحالة كمكتملة.":"Decision readiness is higher than evidence coherence; readiness alone is not enough to mark the state complete.";
  return lang==="ar"?"قوة القراءة وجاهزية القرار متقاربتان، وما زالت الشروط الحاكمة الأخرى تحدد اكتمال الحالة.":"Reading strength and decision readiness are close, while other governing conditions still determine completion.";
}
function decisionExplanationContractV129(x,ctx){
  const frame=x?.frame||ctx?.timeframe||"";
  const frameLabel=timeframeLabelV125(frame);
  const state=sanitizePublicNarrativeV129(statusLabel(x?.state)||tx("unknown"));
  const direction=sanitizePublicNarrativeV129(x?.direction||tx("unknown"));
  const strength=num(x?.quality);
  const readiness=num(x?.readiness);
  const strengthText=percentTextV129(strength);
  const readinessText=percentTextV129(readiness);
  const complete=completedStateV129(x?.state);
  const blocker=arr(x?.blockers).map(value=>strictPublicValueV129(value)).find(Boolean)||"";
  const activation=levelTextV129(x?.levels?.activation);
  const arrival=levelTextV129(x?.levels?.arrival);
  const review=levelTextV129(x?.levels?.review);
  const invalidation=levelTextV129(x?.levels?.invalidation);
  const nmp=levelTextV129(x?.nmp);
  const macro=strictPublicValueV129(x?.macro);
  const risk=strictPublicValueV129(x?.risk);
  const devil=strictPublicValueV129(x?.devil);
  const statusSentence=complete?(lang==="ar"?"الحالة مكتملة وفق العقد الحالي.":"The state is complete under the current contract."):(lang==="ar"?`الحالة ${state} وما زالت قيد المتابعة حتى تستوفي جميع شروط الاكتمال.`:`The state is ${state} and remains under monitoring until all completion conditions are satisfied.`);
  const simpleParts=[
    lang==="ar"?`فريم ${frameLabel}: السياق الاتجاهي ${direction}.`:`${frameLabel}: directional context is ${direction}.`,
    strengthText&&readinessText?(lang==="ar"?`قوة القراءة ${strengthText}، وجاهزية القرار ${readinessText}.`:`Reading strength is ${strengthText}, and decision readiness is ${readinessText}.`):strengthText?(lang==="ar"?`قوة القراءة ${strengthText}.`:`Reading strength is ${strengthText}.`):readinessText?(lang==="ar"?`جاهزية القرار ${readinessText}.`:`Decision readiness is ${readinessText}.`):"",
    statusSentence
  ].filter(Boolean);
  const simple=sanitizePublicNarrativeV129(simpleParts.join(" "));
  const levelParts=[];
  if(activation)levelParts.push(lang==="ar"?`التفعيل ${activation}`:`activation ${activation}`);
  if(arrival)levelParts.push(lang==="ar"?`الوصول ${arrival}`:`arrival ${arrival}`);
  if(review)levelParts.push(lang==="ar"?`المراجعة ${review}`:`review ${review}`);
  if(invalidation)levelParts.push(lang==="ar"?`الإلغاء ${invalidation}`:`invalidation ${invalidation}`);
  const sections=[
    {key:"judgement",title:lang==="ar"?"الحكم العام":"Overall judgement",text:lang==="ar"?`القراءة على فريم ${frameLabel} تعرض ${direction}، وحالتها الحالية ${state}.`:`The ${frameLabel} reading shows ${direction}, with the current state ${state}.`},
    {key:"strength",title:lang==="ar"?"قوة القراءة مقابل الجاهزية":"Reading strength versus readiness",text:[strengthText&&readinessText?(lang==="ar"?`قوة الأدلة ${strengthText} مقابل جاهزية قرار ${readinessText}.`:`Evidence strength is ${strengthText} versus decision readiness of ${readinessText}.`):"",explanationDifferenceV129(strength,readiness)].filter(Boolean).join(" ")},
    {key:"reason",title:lang==="ar"?"سبب الحالة الحالية":"Reason for the current state",text:blocker||statusSentence},
    {key:"levels",title:lang==="ar"?"المستويات المرجعية":"Reference levels",text:levelParts.length?(lang==="ar"?`${levelParts.join("، ")}. هذه مستويات لمتابعة السيناريو على الفريم نفسه وليست أوامر تنفيذ.`:`${levelParts.join(", ")}. These are scenario-monitoring references for the same timeframe, not execution instructions.`):(lang==="ar"?"لم يعرض العقد الحالي مستويات مرجعية مكتملة لهذا الفريم.":"The current contract did not provide a complete reference-level set for this timeframe.")},
    {key:"nmp",title:lang==="ar"?"نقطة الالتقاء":"Confluence point",text:nmp?(lang==="ar"?`نقطة الالتقاء المرجعية لهذا الفريم عند ${nmp}، وتُقرأ ضمن السياق الكامل لا بصورة منفردة.`:`The reference confluence point for this timeframe is ${nmp}, and it must be read within the full context.`):(lang==="ar"?"لم يعرض العقد نقطة التقاء مكتملة لهذا الفريم.":"The contract did not provide a complete confluence point for this timeframe.")},
    {key:"risk",title:lang==="ar"?"المخاطر والاعتراض":"Risk and challenge",text:[risk,devil,macro].filter(value=>value&&value.length>=8).slice(0,3).join(" · ")||(lang==="ar"?"لم يتضمن العرض العام تفاصيل إضافية للمخاطر أو الاعتراض، لذلك تبقى الحالة محكومة بالقيم الظاهرة أعلاه.":"The public view contains no additional risk or challenge detail, so the state remains governed by the values shown above.")}
  ].map(section=>Object.assign({},section,{text:sanitizePublicNarrativeV129(section.text)})).filter(section=>section.text);
  return{mode:ctx?.view_mode==="professional"?"professional":"beginner",frame,simple,sections,forbidden:false};
}
function selectedExplanationHtmlV129(x,ctx,contract){
  const c=contract||decisionExplanationContractV129(x,ctx);
  if(c.mode==="professional"){
    return `<section class="card ndsp-v129-explanation-card ndsp-v129-professional-card" data-ndsp-v129-explanation-card="yes" data-ndsp-v129-explanation-mode="professional" data-ndsp-v129-explanation-frame="${esc(c.frame||"")}" data-ndsp-v129-explanation-section-count="${c.sections.length}"><div class="cardHead"><div><h2>${tx("proExplain")}</h2><p>${lang==="ar"?"تفسير مترابط من الحالة والقوة والجاهزية والمستويات والمخاطر المتاحة في عقد الفريم نفسه.":"A coherent interpretation from the state, strength, readiness, levels, and available risk outputs in the same timeframe contract."}</p></div></div><div class="ndsp-v129-professional-sections">${c.sections.map(section=>`<div class="ndsp-v129-professional-section" data-ndsp-v129-section="${esc(section.key)}"><b>${esc(section.title)}</b><p>${esc(section.text)}</p></div>`).join("")}</div><small class="ndsp-v129-contract-note">${lang==="ar"?`مرتبط بالمخرجات المحكومة لفريم ${timeframeLabelV125(c.frame)}`:`Bound to the governed ${timeframeLabelV125(c.frame)} outputs`}</small></section>`;
  }
  return `<section class="card ndsp-v129-explanation-card ndsp-v129-simple-card" data-ndsp-v129-explanation-card="yes" data-ndsp-v129-explanation-mode="beginner" data-ndsp-v129-explanation-frame="${esc(c.frame||"")}" data-ndsp-v129-explanation-section-count="1"><div class="cardHead"><div><h2>${tx("simpleExplain")}</h2></div></div><p class="decisionNarrative ndsp-v129-simple-narrative">${esc(c.simple)}</p></section>`;
}
/* NDSP_PUBLIC_EXPLANATION_MODE_GUARD_V129_END */


function extractDecision(bundle){
  const d=bundle.quality||{}; const s=obj(d.scenario); const execution=obj(d.execution); const summary=obj(d.final_summary); const levelsSource=bundle.levels||{};
  const layers=arr(pick(d.decision_layers,d.layers,d.layer_results,execution.layers));
  const l16=layerByCodeV125(layers,"L16");
  const frame=normalizeTimeframe(pick(d?.instrument?.timeframe,d?.live_market_analysis?.selected_timeframe,d?.nmp_timeframe,""));
  const state=pick(execution.governed_single_truth_state,d.single_truth_state,d.scenario_state,d.decision_status,s.scenario_state,summary.state,layerRawStateV125(l16));
  const direction=pick(d.scenario_directional_context,s.scenario_directional_context,d.directional_context,summary.directional_context,d.trend_context,d?.live_market_analysis?.selected_timeframe_direction);
  const strengthContract=strengthContractV127(d,summary,l16,layers);
  const quality=strengthContract.value;
  const legacyReadiness=num(pick(d.readiness_score,d.decision_readiness,execution.readiness_score,summary.readiness_score));
  const l16Readiness=layerScoreV125(l16);
  const readiness=l16Readiness!==null?l16Readiness:legacyReadiness;
  const confidence=num(pick(d.confidence_score,d.confidence,summary.confidence));
  const blockerSource=pick(execution.blockers,d.blockers,d.why_not_completed,d.incompletion_reasons,summary.blockers,[]);
  const blockers=cleanBlockersV125(blockerSource,state,readiness,l16);
  const activation=scenarioLevelContractV127("activation",d);
  const arrival=scenarioLevelContractV127("arrival",d);
  const review=scenarioLevelContractV127("review",d);
  const invalidation=scenarioLevelContractV127("invalidation",d);
  const lv=obj(pick(d.scenario_levels,d.reference_levels,d.levels,s.scenario_levels,levelsSource.scenario_levels,levelsSource.reference_levels,levelsSource.levels,levelsSource));
  const nmp=pick(d.nmp_level,d.nmp_price,obj(d.nmp).level,obj(d.nmp).price,s.nmp,s.nmp_level,lv.nmp,lv.nmp_level);
  const macro=pick(deepGet(d,["macro.summary","usd_macro.summary","usd_macro_text"]),layerReasonsV125(layerByCodeV125(layers,"L11")).join(" · "));
  const risk=pick(deepGet(d,["risk.summary","risk_text","risk_context"]),layerReasonsV125(layerByCodeV125(layers,"L12")).join(" · "));
  const devil=pick(deepGet(d,["devils_advocate.summary","devils_advocate_text","challenge.summary"]),layerReasonsV125(layerByCodeV125(layers,"L15")).join(" · "));
  const simple=pick(d.beginner_explanation,summary.beginner_explanation,d.explanation_simple,d.explanation);
  const professionalContract=professionalExplanationContractV128(d,summary,layers,frame);
  const professional=professionalContract.text;
  const updated=pick(d.updated_at,d.generated_at,d.timestamp,obj(d.request_meta).generated_at,bundle.loadedAt);
  return {state,direction,quality,readiness,confidence,blockers,levels:{activation:activation.value,arrival:arrival.value,review:review.value,invalidation:invalidation.value},levelSources:{activation:activation.source,arrival:arrival.source,review:review.source,invalidation:invalidation.source},strengthSource:strengthContract.source,strengthEligibleCount:strengthContract.eligibleCount||0,strengthMethod:strengthContract.method||"",nmp,layers,macro,risk,devil,simple,professional,professionalSource:professionalContract.source,professionalSectionCount:professionalContract.sectionCount||0,professionalRedacted:Boolean(professionalContract.redacted),updated,frame,raw:d};
}

function loadingShell(page,ctx,title,desc){ shell(`${pageHero(title,desc)}<div class="loading"><div><div class="spinner"></div>${tx("loading")}</div></div>`,page,ctx); }
function mismatchCard(validation){return `<section class="warningBox"><h3>${tx("mismatchTitle")}</h3><p>${tx("mismatchText")}</p><code>${esc(JSON.stringify(validation))}</code></section>`;}
function decisionSummaryCardsLegacyV125(x){return `<div class="grid grid4"><section class="card"><div class="kpi"><small>${tx("readingState")}</small><strong style="font-size:24px">${esc(statusLabel(x.state))}</strong>${badge(x.state)}</div></section><section class="card"><div class="kpi"><small>${tx("direction")}</small><strong style="font-size:22px">${esc(x.direction||tx("unavailable"))}</strong></div></section><section class="card">${meter(tx("strength"),x.quality)}</section><section class="card">${meter(tx("readiness"),x.readiness,"readiness")}</section></div>`;}

function decisionSummaryCards(x){
  const strengthAvailable=num(x.quality)!==null;
  const derived=x.strengthMethod==="weighted_mean_non_redacted";
  const strengthNote=lang==="ar"?(strengthAvailable?(derived?`محسوبة من ${x.strengthEligibleCount||0} طبقات مستلمة وغير محجوبة لنفس الفريم`:"القوة من حقل صريح في العقد الحاكم للفريم"):"تعذر تكوين قوة قراءة محكومة"):(strengthAvailable?(derived?`Calculated from ${x.strengthEligibleCount||0} received non-redacted layers for the same timeframe`:"Strength from an explicit governing contract field"):"A governed reading strength could not be formed");
  return `<div class="grid grid4"><section class="card"><div class="kpi"><small>${tx("readingState")}</small><strong style="font-size:24px">${esc(statusLabel(x.state))}</strong>${badge(x.state)}</div></section><section class="card"><div class="kpi"><small>${tx("direction")}</small><strong style="font-size:22px">${esc(x.direction||tx("unavailable"))}</strong></div></section><section class="card" data-ndsp-v127-strength-card="yes" data-ndsp-v127-strength-value="${strengthAvailable?esc(String(x.quality)):""}" data-ndsp-v127-strength-source="${esc(x.strengthSource||"")}" data-ndsp-v127-strength-method="${esc(x.strengthMethod||"")}" data-ndsp-v127-strength-layer-count="${esc(String(x.strengthEligibleCount||0))}">${meter(tx("strength"),x.quality)}<small class="sub ndsp-v127-contract-note">${esc(strengthNote)}</small></section><section class="card" data-ndsp-v127-readiness-card="yes">${meter(tx("readiness"),x.readiness,"readiness")}</section></div>`;
}
function levelsHtml(x){
  const levels=[["activation",x.levels.activation,""],["arrival",x.levels.arrival,"arrival"],["review",x.levels.review,"review"],["invalidation",x.levels.invalidation,"invalidation"]];
  const frameLabel=timeframeLabelV125(x.frame);
  return `<div class="levelGrid" data-ndsp-v127-level-grid="yes" data-ndsp-v127-level-timeframe="${esc(x.frame||"")}">${levels.map(([k,v,c])=>{const present=numericValueV127(v,["value","level","price","display_value","numeric_value"])!==null;return `<div class="level ${c}" data-ndsp-v127-level-kind="${k}" data-ndsp-v127-level-present="${present?"yes":"no"}" data-ndsp-v127-level-value="${present?esc(String(numericValueV127(v,["value","level","price","display_value","numeric_value"]))):""}" data-ndsp-v127-level-source="${esc(x.levelSources?.[k]||"")}"><small>${tx(k)}</small><strong>${esc(displayLevelV127(v))}</strong><span class="ndsp-v127-level-contract">${present?(lang==="ar"?`عقد ${frameLabel} مرتبط`:`${frameLabel} contract bound`):tx("unavailable")}</span></div>`}).join("")}</div>`;
}
function blockersHtml(x){ if(!x.blockers.length)return noData(lang==="ar"?"لا توجد موانع مسجلة في العقد المستلم.":"No blockers were recorded in the received contract."); return `<div class="reasonList">${x.blockers.map((r,i)=>`<div class="reason"><i>${i+1}</i><span>${esc(r)}</span></div>`).join("")}</div>`; }
function layerValues(x){ const map=new Map(x.layers.map(l=>[l.id||l.layer_id||l.canonical_id,l])); return arr(layerRegistry.layers).map((reg,i)=>{const live=map.get(reg.id)||x.layers[i]||{};return {reg,live,value:layerScoreV125(live)||0};}); }

function radarCanvasHtml(){return `<canvas id="radarCanvas" class="radarCanvas" width="700" height="700" aria-label="${tx("layerCompletion")}"></canvas>`;}
function drawRadar(values){ const canvas=document.getElementById("radarCanvas");if(!canvas)return;const dpr=Math.max(1,devicePixelRatio||1),css=canvas.getBoundingClientRect().width||500;canvas.width=css*dpr;canvas.height=css*dpr;const c=canvas.getContext("2d");c.scale(dpr,dpr);const w=css,h=css,cx=w/2,cy=h/2,r=w*.37,n=Math.max(3,values.length||16);c.clearRect(0,0,w,h);c.strokeStyle="rgba(215,174,67,.22)";c.lineWidth=1;for(let ring=1;ring<=4;ring++){c.beginPath();for(let i=0;i<n;i++){const a=-Math.PI/2+i*Math.PI*2/n,rr=r*ring/4,x=cx+Math.cos(a)*rr,y=cy+Math.sin(a)*rr;i?c.lineTo(x,y):c.moveTo(x,y)}c.closePath();c.stroke()}for(let i=0;i<n;i++){const a=-Math.PI/2+i*Math.PI*2/n;c.beginPath();c.moveTo(cx,cy);c.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r);c.stroke()}c.beginPath();values.forEach((v,i)=>{const a=-Math.PI/2+i*Math.PI*2/n,rr=r*Math.max(0,Math.min(100,v))/100,x=cx+Math.cos(a)*rr,y=cy+Math.sin(a)*rr;i?c.lineTo(x,y):c.moveTo(x,y)});c.closePath();c.fillStyle="rgba(215,174,67,.22)";c.strokeStyle="#ffe48b";c.lineWidth=2;c.fill();c.stroke();c.fillStyle="#d7ae43";c.font="11px monospace";c.textAlign="center";for(let i=0;i<n;i++){const a=-Math.PI/2+i*Math.PI*2/n,x=cx+Math.cos(a)*(r+22),y=cy+Math.sin(a)*(r+22)+4;c.fillText(`L${String(i+1).padStart(2,"0")}`,x,y)}}

async function homePage(ctx){ loadingShell("home",ctx,tx("homeTitle"),tx("homeDesc")); const b=await fetchDecisionBundle(ctx); const x=extractDecision(b); const content=`${pageHero(tx("homeTitle"),tx("homeDesc"),`<a class="btn btnGold" href="${routeHref("decision",ctx)}">${tx("openDecision")}</a>`)}${!b.validation.ok?mismatchCard(b.validation):decisionSummaryCards(x)}<div class="grid grid3" style="margin-top:16px"><section class="card"><div class="cardHead"><div><h2>${tx("whyIncomplete")}</h2></div></div>${blockersHtml(x)}</section><section class="card span2"><div class="cardHead"><div><h2>${tx("nextStep")}</h2><p>${lang==="ar"?"تنقل بين الصفحات مع بقاء سياق الأصل والفريم مقفلًا.":"Move between pages while the asset and timeframe remain locked."}</p></div></div><div class="sectionLinks"><a class="sectionLink" href="${routeHref("decision",ctx)}"><b>${tx("openDecision")}</b><small>${tx("decisionDesc")}</small></a><a class="sectionLink" href="${routeHref("layers",ctx)}"><b>${tx("openLayers")}</b><small>${tx("layersDesc")}</small></a><a class="sectionLink" href="${routeHref("scenarios",ctx)}"><b>${tx("openScenarios")}</b><small>${tx("scenariosDesc")}</small></a><a class="sectionLink" href="${routeHref("risk",ctx)}"><b>${tx("openRisk")}</b><small>${tx("riskDesc")}</small></a></div></section></div>${rawDetails(b.quality)}`; shell(content,"home",ctx); }

/* NDSP_EMBEDDED_LAYER_SUMMARY_V134_BEGIN */
window.__NDSP_EMBEDDED_LAYER_SUMMARY_V134__={version:"134.0.0",exactTimeframeOnly:true,noCrossTimeframeFallback:true,noResponseFabrication:true,reusesV133PublicSemantics:true};
function embeddedDecisionLayerSummaryV134(x,ctx){
  const rows=exactLayerRowsV133(x).slice(0,8);
  const frame=normalizeTimeframe(ctx?.timeframe||x?.frame||"");
  const frameLabel=timeframeLabelV125(frame);
  if(!rows.length)return noData(lang==="ar"?"لم تصل عقود وحدات القرار لهذا السياق.":"Decision-unit contracts were not received for this context.");
  return rows.map(({live,reg},index)=>{
    const received=layerReceivedV125(live);
    const publicState=layerPublicStateV133(live);
    const publicMetric=layerPublicMetricV133(live);
    const id=String(reg?.id||layerIdentifierV125(live)||`NDSP-CORE-L${String(index+1).padStart(2,"0")}`);
    const number=String(id.match(/L(\d{1,2})$/i)?.[1]||String(index+1).padStart(2,"0")).padStart(2,"0");
    const name=lang==="ar"?pick(reg?.name_ar,reg?.public_name_ar,`الوحدة ${number}`):pick(reg?.name_en,reg?.public_name_en,`Unit ${number}`);
    const contractText=received?(lang==="ar"?`عقد ${frameLabel} مرتبط`:`${frameLabel} contract bound`):(lang==="ar"?`عقد ${frameLabel} غير مستلم`:`${frameLabel} contract not received`);
    return `<div class="reason ndsp-v134-summary-layer" data-ndsp-v134-summary-layer="yes" data-ndsp-contract-layer="${esc(id)}" data-ndsp-contract-timeframe="${esc(frame)}" data-ndsp-contract-received="${received?"yes":"no"}" data-ndsp-v134-public-state="${esc(publicState)}"><i>${esc(number)}</i><span><b>${esc(name)}</b><br><small class="ndsp-v134-summary-status"><strong class="ndsp-v134-summary-state">${esc(publicState)}</strong><span class="ndsp-v134-summary-metric">${esc(publicMetric)}</span></small><em class="ndsp-v134-summary-contract">${esc(contractText)}</em></span></div>`;
  }).join("");
}
/* NDSP_EMBEDDED_LAYER_SUMMARY_V134_END */


/* NDSP_PUBLIC_FOUR_LAYERS_V140_BEGIN */
function publicLayerStateV140(kind,x){
  if(kind==="tdl"){
    return {state:x.direction||statusLabel(x.state),tone:statusTone(x.state)};
  }
  if(kind==="nmp"){
    const available=!(x.nmp===null||x.nmp===undefined||x.nmp==="");
    return {
      state:available
        ?(lang==="ar"?"متاحة":"Available")
        :(lang==="ar"?"قيد المتابعة":"Pending"),
      tone:available?"ok":"warn"
    };
  }
  if(kind==="gold"){
    const state=String(x.state||"").toUpperCase();
    const ready=/COMPLETE|COMPLETED|READY|PUBLISHABLE/.test(state);
    return {
      state:ready
        ?(lang==="ar"?"توافق مكتمل":"Alignment complete")
        :(lang==="ar"?"تحت المراقبة":"Under monitoring"),
      tone:ready?"ok":"warn"
    };
  }
  const blocked=arr(x.blockers).length>0;
  return {
    state:blocked
      ?(lang==="ar"?"اعتراض قائم":"Challenge active")
      :(lang==="ar"?"لا اعتراض مانع":"No blocking challenge"),
    tone:blocked?"warn":"ok"
  };
}

function publicFourLayersHtmlV140(x){
  const definitions=[
    {
      key:"tdl",
      ar:"منطق الاتجاه الزمني TDL",
      en:"Timed Direction Logic (TDL)",
      arText:"يعرض السياق الاتجاهي والزمني بصياغة عامة دون كشف مكونات الحساب.",
      enText:"Shows governed directional and temporal context without exposing calculation components."
    },
    {
      key:"nmp",
      ar:"NMP",
      en:"NMP",
      arText:"يعرض حالة نقطة الالتقاء وقيمتها المسموح بها لهذا الأصل والفريم.",
      enText:"Shows the permitted meeting-point state and value for this asset and timeframe."
    },
    {
      key:"gold",
      ar:"الإشارة الذهبية",
      en:"Golden Signal",
      arText:"يلخص درجة اكتمال التوافق العام دون عرض الطبقات الداعمة أو ترتيبها.",
      enText:"Summarizes overall alignment without listing supporting layers or their order."
    },
    {
      key:"devil",
      ar:"محامي الشيطان",
      en:"Devil's Advocate",
      arText:"يعرض وجود اعتراض حاكم أو عدم وجود اعتراض مانع دون كشف قواعده الداخلية.",
      enText:"Shows whether a governing challenge exists without exposing its internal rules."
    }
  ];

  const cards=definitions.map(item=>{
    const state=publicLayerStateV140(item.key,x);
    const extra=item.key==="nmp" && !(x.nmp===null||x.nmp===undefined||x.nmp==="")
      ?`<strong class="publicLayerValueV140">${esc(fmt(x.nmp))}</strong>`
      :"";
    return `<article class="publicLayerCardV140">
      <div class="publicLayerTopV140">
        <h3>${esc(lang==="ar"?item.ar:item.en)}</h3>
        <span class="badge ${esc(state.tone)}">${esc(state.state)}</span>
      </div>
      <p>${esc(lang==="ar"?item.arText:item.enText)}</p>
      ${extra}
    </article>`;
  }).join("");

  const note=lang==="ar"
    ?"تعمل 12 طبقة إضافية داخل محرك NDSP دون عرض أسمائها أو ترتيبها أو صيغها."
    :"Twelve additional layers remain active inside NDSP without exposing their names, order, or formulas.";

  return `<section class="card publicLayersSectionV140">
    <div class="cardHead">
      <div>
        <h2>${lang==="ar"?"الطبقات الأربع المعلنة":"Four Public Layers"}</h2>
        <p>${esc(note)}</p>
      </div>
      <span class="publicLayerCountV140">4 / 16</span>
    </div>
    <div class="publicLayerGridV140">${cards}</div>
  </section>`;
}
/* NDSP_PUBLIC_FOUR_LAYERS_V140_END */

async function decisionPage(ctx){ loadingShell("decision",ctx,tx("decisionTitle"),tx("decisionDesc")); const b=await fetchDecisionBundle(ctx); const x=extractDecision(b); if(!b.validation.ok){shell(`${pageHero(tx("decisionTitle"),tx("decisionDesc"))}${mismatchCard(b.validation)}`,"decision",ctx);return}
  const explanationV129=decisionExplanationContractV129(x,ctx); const summaryNarrative=explanationV129.simple;
  const content=`${pageHero(tx("decisionTitle"),tx("decisionDesc"),`<button class="btn" id="refreshDecision">${tx("refresh")}</button>`)}${decisionSummaryCards(x)}
  <div class="grid grid3" style="margin-top:16px"><section class="card"><div class="cardHead"><div><h2>${tx("whyIncomplete")}</h2></div></div>${blockersHtml(x)}</section><section class="card span2"><div class="cardHead"><div><h2>${tx("currentDecision")}</h2><p>${esc(x.updated||"")}</p></div>${badge(x.state)}</div><h2 class="decisionTitle">${esc(x.direction||statusLabel(x.state))}</h2><p class="decisionNarrative">${esc(summaryNarrative)}</p></section></div>
  <section class="card" style="margin-top:16px"><div class="cardHead"><div><h2>${lang==="ar"?"مستويات السيناريو المحكومة":"Governed Scenario Levels"}</h2><p>${lang==="ar"?"كل مستوى يخص الأصل والفريم الظاهرين في شريط السياق فقط.":"Every level belongs only to the asset and timeframe in the context bar."}</p></div></div>${levelsHtml(x)}</section>
  <div class="grid grid2 ndsp-v129-selected-explanation-row" data-ndsp-v129-selected-view="${esc(explanationV129.mode)}" style="margin-top:16px"><section class="card"><div class="cardHead"><div><h2>${tx("nmp")}</h2></div></div><div class="nmpBox"><small>${tx("nmp")}</small><strong>${esc(x.nmp===null||x.nmp===undefined?tx("unavailable"):fmt(x.nmp))}</strong>${badge(x.nmp?"AVAILABLE":"PENDING")}</div></section>${selectedExplanationHtmlV129(x,ctx,explanationV129)}</div>
  <div style="margin-top:16px">${publicFourLayersHtmlV140(x)}</div>
  <section class="card" style="margin-top:16px"><div class="cardHead"><div><h2>${lang==="ar"?"انتقل إلى التفاصيل المترابطة":"Open Linked Details"}</h2></div></div><div class="sectionLinks"><a class="sectionLink" href="${routeHref("scenarios",ctx)}"><b>${tx("alternatives")}</b><small>${tx("scenariosDesc")}</small></a><a class="sectionLink" href="${routeHref("risk",ctx)}"><b>${tx("risk")}</b><small>${tx("riskDesc")}</small></a><a class="sectionLink" href="${routeHref("completed",ctx)}"><b>${tx("completedTitle")}</b><small>${tx("completedDesc")}</small></a><a class="sectionLink" href="${routeHref("data",ctx)}"><b>${tx("dataTitle")}</b><small>${tx("dataDesc")}</small></a></div></section>`;
  shell(content,"decision",ctx);document.getElementById("refreshDecision")?.addEventListener("click",async()=>{lastBundle=null;await decisionPage(ctx)});
}

async function layersPage(ctx){
  loadingShell(
    "layers",
    ctx,
    lang==="ar"?"الطبقات المعلنة":"Public Layers",
    lang==="ar"
      ?"أربعة أسماء عامة فقط؛ بقية الطبقات تعمل داخليًا دون كشفها."
      :"Only four public names are shown; the remaining layers operate internally."
  );
  const b=await fetchDecisionBundle(ctx);
  const x=extractDecision(b);
  if(!b.validation.ok){
    shell(
      `${pageHero(
        lang==="ar"?"الطبقات المعلنة":"Public Layers",
        lang==="ar"
          ?"أربعة أسماء عامة فقط؛ بقية الطبقات تعمل داخليًا دون كشفها."
          :"Only four public names are shown; the remaining layers operate internally."
      )}${mismatchCard(b.validation)}`,
      "layers",
      ctx
    );
    return;
  }
  shell(
    `${pageHero(
      lang==="ar"?"الطبقات المعلنة":"Public Layers",
      lang==="ar"
        ?"تظهر أربعة أسماء فقط، وتبقى 12 طبقة محجوبة نصيًا وبصريًا."
        :"Four names are shown; twelve layers remain textually and visually hidden."
    )}${publicFourLayersHtmlV140(x)}`,
    "layers",
    ctx
  );
}

function capabilitiesPage(ctx){
  location.replace(routeHref("decision",ctx));
}
function scenarioArrayV136(value){
  if(Array.isArray(value))return value;
  if(value&&typeof value==="object"){
    for(const key of ["items","scenarios","alternatives","paths","options"]){if(Array.isArray(value[key]))return value[key]}
  }
  return [];
}
function explicitAlternativeScenariosV136(raw){
  const paths=["alternative_scenarios","scenarios.alternatives","scenario.alternatives","alternative_paths","scenarios.alternative_paths","scenario.alternative_paths","decision.alternative_scenarios","public_scenarios.alternatives","scenario_contract.alternatives","governance_summary.alternative_scenarios"];
  for(const path of paths){
    const values=scenarioArrayV136(valueAtPathV127(raw,path));
    if(values.length)return{source:path,items:values};
  }
  return{source:"",items:[]};
}
function normalizedExplicitScenarioV136(item,index){
  const raw=item&&typeof item==="object"?item:{description:item};
  const title=scenarioSanitizeV136(pick(raw.public_name_ar,raw.name_ar,raw.public_title,raw.title,raw.name,raw.label,raw.scenario,lang==="ar"?`المسار البديل ${index+1}`:`Alternative path ${index+1}`));
  const condition=scenarioSanitizeV136(pick(raw.public_explanation_ar,raw.public_description,raw.condition,raw.trigger,raw.description,raw.reason,raw.narrative,raw.summary,raw.explanation));
  const status=scenarioSanitizeV136(pick(raw.public_state,raw.state_label,raw.status_label,raw.state,raw.status));
  return{title,condition:condition||status|| (lang==="ar"?"مسار بديل وارد من عقد السيناريو للفريم نفسه.":"An alternative path supplied by the same-timeframe scenario contract."),status};
}
function derivedScenarioPathsV136(x,ctx){
  const activation=scenarioLevelContractV127("activation",x.raw).value;
  const arrival=scenarioLevelContractV127("arrival",x.raw).value;
  const review=scenarioLevelContractV127("review",x.raw).value;
  const invalidation=scenarioLevelContractV127("invalidation",x.raw).value;
  const frame=timeframeLabelV125(ctx?.timeframe||x?.frame||"");
  const activationText=displayLevelV127(activation);
  const arrivalText=displayLevelV127(arrival);
  const reviewText=displayLevelV127(review);
  const invalidationText=displayLevelV127(invalidation);
  if([activation,arrival,review,invalidation].some(value=>numericValueV127(value)===null))return[];
  if(lang==="ar")return[
    {title:"مسار التفعيل والمتابعة",condition:`يبقى السيناريو الحاكم تحت المتابعة على فريم ${frame} إلى أن يتأكد مستوى التفعيل ${activationText}. بعد التفعيل يُراقب مستوى الوصول ${arrivalText} ضمن السياق نفسه، من دون اعتباره أمر تنفيذ.`,status:"مشروط بالتفعيل",levelKind:"activation"},
    {title:"مسار إعادة التقييم",condition:`وصول السعر إلى مستوى المراجعة ${reviewText} يفتح إعادة تقييم لقوة القراءة وجاهزية القرار على فريم ${frame}. هذا المسار لا يعني انقلاب الاتجاه تلقائيًا.`,status:"إعادة تقييم",levelKind:"review"},
    {title:"مسار إلغاء السيناريو",condition:`تحقق مستوى الإلغاء ${invalidationText} يبطل السيناريو الحالي لهذا الفريم، ويوقف الاعتماد على مسار التفعيل والوصول إلى أن تصدر قراءة محكومة جديدة.`,status:"إلغاء مشروط",levelKind:"invalidation"}
  ];
  return[
    {title:"Activation and monitoring path",condition:`The governing scenario remains under monitoring on ${frame} until activation at ${activationText} is confirmed. After activation, arrival at ${arrivalText} is monitored within the same context and is not an execution instruction.`,status:"Conditional activation",levelKind:"activation"},
    {title:"Reassessment path",condition:`Reaching the review level at ${reviewText} triggers a reassessment of reading strength and decision readiness on ${frame}. It does not automatically reverse the directional context.`,status:"Reassessment",levelKind:"review"},
    {title:"Scenario invalidation path",condition:`Reaching the invalidation level at ${invalidationText} cancels the current scenario for this timeframe until a new governed reading is issued.`,status:"Conditional invalidation",levelKind:"invalidation"}
  ];
}
function alternativeScenarioContractV136(x,ctx){
  const explicit=explicitAlternativeScenariosV136(x.raw);
  if(explicit.items.length){
    return{source:"explicit",sourcePath:explicit.source,frame:normalizeTimeframe(ctx?.timeframe||x?.frame||""),items:explicit.items.map(normalizedExplicitScenarioV136)};
  }
  return{source:"level_derived",sourcePath:"scenario_levels",frame:normalizeTimeframe(ctx?.timeframe||x?.frame||""),items:derivedScenarioPathsV136(x,ctx)};
}
function alternativeScenarioHtmlV136(contract){
  const c=contract||{source:"",frame:"",items:[]};
  if(!c.items.length)return noData(lang==="ar"?"تعذر تكوين مسارات بديلة لأن عقد هذا الفريم لا يحتوي مجموعة مستويات سيناريو مكتملة.":"Alternative paths could not be formed because this timeframe contract does not contain a complete scenario-level set.");
  return c.items.map((item,index)=>`<article class="reason ndsp-v136-alt-card" data-ndsp-v136-alt-card="yes" data-ndsp-v136-alt-source="${esc(c.source)}" data-ndsp-v136-alt-timeframe="${esc(c.frame)}" data-ndsp-v136-alt-kind="${esc(item.levelKind||"explicit")}"><i>${index+1}</i><span><b>${esc(item.title)}</b>${item.status?`<small class="ndsp-v136-alt-status">${esc(item.status)}</small>`:""}<p>${esc(item.condition)}</p></span></article>`).join("");
}
/* NDSP_GOVERNED_ALTERNATIVE_SCENARIOS_V136_END */

async function scenariosPage(ctx){
  loadingShell("scenarios",ctx,tx("scenariosTitle"),tx("scenariosDesc"));
  const b=await fetchDecisionBundle(ctx); const x=extractDecision(b);
  if(!b.validation.ok){shell(`${pageHero(tx("scenariosTitle"),tx("scenariosDesc"))}${mismatchCard(b.validation)}`,"scenarios",ctx);return}
  const alternatives=alternativeScenarioContractV136(x,ctx);
  const sourceText=alternatives.source==="explicit"
    ?(lang==="ar"?`سيناريوهات بديلة واردة من عقد الفريم ${timeframeLabelV125(alternatives.frame)}.`:`Alternative scenarios supplied by the ${timeframeLabelV125(alternatives.frame)} contract.`)
    :(lang==="ar"?`لا يحتوي العقد على قائمة بدائل مستقلة؛ لذلك تُعرض مسارات شرطية مستخرجة مباشرة من مستويات السيناريو المحكومة لفريم ${timeframeLabelV125(alternatives.frame)}، وليست توقعات أو أوامر تنفيذ.`:`The contract contains no standalone alternative list, so conditional paths are derived directly from the governed ${timeframeLabelV125(alternatives.frame)} scenario levels. They are not forecasts or execution instructions.`);
  const content=`${pageHero(tx("scenariosTitle"),tx("scenariosDesc"))}
  <section class="card"><div class="cardHead"><div><h2>${tx("governingScenario")}</h2><p>${esc(x.direction||statusLabel(x.state))}</p></div>${badge(x.state)}</div>${levelsHtml(x)}</section>
  <div class="grid grid2 ndsp-v136-scenario-grid" style="margin-top:16px">
    <section class="card"><div class="cardHead"><div><h2>${tx("nmp")}</h2></div></div><div class="nmpBox"><strong>${esc(x.nmp?fmt(x.nmp):tx("unavailable"))}</strong></div></section>
    <section class="card ndsp-v136-alternatives" data-ndsp-v136-alternatives="yes" data-ndsp-v136-source="${esc(alternatives.source)}" data-ndsp-v136-timeframe="${esc(alternatives.frame)}"><div class="cardHead"><div><h2>${tx("alternatives")}</h2><p class="ndsp-v136-source-note">${esc(sourceText)}</p></div></div><div class="reasonList ndsp-v136-alt-list">${alternativeScenarioHtmlV136(alternatives)}</div></section>
  </div>`;
  shell(content,"scenarios",ctx);
}
async function riskPage(ctx){
  loadingShell("risk",ctx,tx("riskTitle"),tx("riskDesc"));
  const b=await fetchDecisionBundle(ctx);
  const x=extractDecision(b);

  if(!b.validation.ok){
    shell(
      `${pageHero(tx("riskTitle"),tx("riskDesc"))}${mismatchCard(b.validation)}`,
      "risk",
      ctx
    );
    return;
  }

  const cards=[
    {
      title:lang==="ar"?"السياق الكلي":"Macro Context",
      text:x.macro||(
        lang==="ar"
          ?"لا توجد قراءة كلية مسموحة للعرض حاليًا."
          :"No governed macro reading is currently available."
      )
    },
    {
      title:lang==="ar"?"المخاطر":"Risk",
      text:x.risk||(
        lang==="ar"
          ?"لا توجد قراءة مخاطر مسموحة للعرض حاليًا."
          :"No governed risk reading is currently available."
      )
    },
    {
      title:lang==="ar"?"محامي الشيطان":"Devil's Advocate",
      text:x.devil||(
        lang==="ar"
          ?"لا يوجد اعتراض مسموح للعرض حاليًا."
          :"No governed challenge is currently available."
      )
    }
  ].map(item=>`<section class="card publicRiskCardV140">
    <div class="cardHead"><div><h2>${esc(item.title)}</h2></div></div>
    <p class="decisionNarrative">${esc(item.text)}</p>
  </section>`).join("");

  shell(
    `${pageHero(tx("riskTitle"),tx("riskDesc"))}
     <div class="grid grid3 publicRiskGridV140">${cards}</div>
     <section class="card compactBlockersV140">
       <div class="cardHead"><div><h2>${tx("whyIncomplete")}</h2></div></div>
       ${blockersHtml(x)}
     </section>`,
    "risk",
    ctx
  );
}

function extractRecords(payload){
  const p=payload?.data||payload||{};
  return arr(p.decisions).length?arr(p.decisions):arr(p.records).length?arr(p.records):arr(p.items).length?arr(p.items):Array.isArray(p)?p:[];
}
function filteredRecords(payload,ctx){return extractRecords(payload).filter(r=>recordMatchesContext(r,ctx));}
function completedRecordsHtml(payload,ctx){
  const current=filteredRecords(payload.current,ctx),history=filteredRecords(payload.history,ctx);
  const records=[...current,...history].filter((r,i,a)=>a.indexOf(r)===i);
  const rows=records.map((r,i)=>{
    const d=r.decision||r,rc=recordContext(r);
    return `<tr><td>${i+1}</td><td>${esc(rc.symbol)}</td><td>${esc(statusLabel(d.decision_status||d.state||d.scenario_state))}</td><td>${esc(rc.analysisMode||ctx.analysis_mode)}</td><td>${esc(rc.timeframe||ctx.timeframe)}</td><td>${esc(d.completed_at||d.updated_at||d.timestamp||"—")}</td><td><code>${esc(d.semantic_fingerprint||d.record_hash||d.decision_id||"—")}</code></td></tr>`;
  }).join("");
  return `<div class="grid grid4"><section class="card"><div class="kpi"><small>${tx("current")}</small><strong>${current.length}</strong></div></section><section class="card"><div class="kpi"><small>${tx("history")}</small><strong>${history.length}</strong></div></section><section class="card"><div class="kpi"><small>${tx("records")}</small><strong>${records.length}</strong></div></section><section class="card"><div class="kpi"><small>${tx("integrity")}</small><strong style="font-size:20px">${esc(statusLabel(deepGet(payload.history,["integrity.status","chain_verified"])||"NOT_EVALUATED"))}</strong></div></section></div><section class="card" style="margin-top:16px"><div class="cardHead"><div><h2>${tx("completedTitle")}</h2></div></div>${rows?`<div class="tableWrap"><table><thead><tr><th>#</th><th>${tx("asset")}</th><th>${tx("status")}</th><th>${tx("analysisMode")}</th><th>${tx("timeframe")}</th><th>${lang==="ar"?"الوقت":"Time"}</th><th>${lang==="ar"?"البصمة":"Fingerprint"}</th></tr></thead><tbody>${rows}</tbody></table></div>`:noData(tx("noRecords"))}</section>${rawDetails({current,history})}`;
}
async function completedPage(ctx){
  loadingShell("completed",ctx,tx("completedTitle"),tx("completedDesc"));
  const bundle=await fetchDecisionBundle(ctx);
  if(!bundle.validation.ok){shell(`${pageHero(tx("completedTitle"),tx("completedDesc"))}${mismatchCard(bundle.validation)}`,"completed",ctx);return}
  const protectedText=lang==="ar"?"سجل القرارات محمي. اضغط لتحميل السجل باستخدام جلسة الدخول الحالية، ولن تُرسل هذه الطلبات في بقية صفحات المنصة.":"Decision history is protected. Load it using the current authenticated session; these requests are not sent from other portal pages.";
  const content=`${pageHero(tx("completedTitle"),tx("completedDesc"))}<div class="infoBox" style="margin-bottom:16px">${protectedText}</div><section class="card"><div class="cardHead"><div><h2>${tx("completedTitle")}</h2><p>${lang==="ar"?"يعرض السجل القرارات المطابقة للسوق والأصل والفريم ونوع القراءة فقط.":"Only records matching the locked market, asset, timeframe and reading type are shown."}</p></div><button class="btn btnGold" id="loadProtectedHistory">${lang==="ar"?"تحميل السجل المحمي":"Load protected history"}</button></div><div id="completedRecordsState">${noData(lang==="ar"?"لم يتم طلب بيانات السجل المحمي بعد.":"Protected history has not been requested yet.")}</div></section>`;
  shell(content,"completed",ctx);
  document.getElementById("loadProtectedHistory")?.addEventListener("click",async event=>{
    const button=event.currentTarget,state=document.getElementById("completedRecordsState");
    button.disabled=true;
    button.textContent=lang==="ar"?"جارِ التحميل…":"Loading…";
    if(state)state.innerHTML=`<div class="loading"><div><div class="spinner"></div>${tx("loading")}</div></div>`;
    const payload=await fetchCompletedRecords(ctx);
    if(payload.unauthorized){
      const returnUrl=encodeURIComponent(location.pathname+location.search);
      if(state)state.innerHTML=`<div class="warningBox"><h3>${lang==="ar"?"يتطلب تسجيل الدخول":"Authentication required"}</h3><p>${lang==="ar"?"لم تتجاوز الواجهة الحماية ولم تجعل السجل عامًا. سجّل الدخول ثم عد لتحميل القرارات الخاصة بحسابك.":"The portal did not bypass protection or expose private history. Sign in, then return to load your account records."}</p><a class="btn btnGold" href="/login/?return=${returnUrl}">${tx("login")}</a></div>`;
    }else if(payload.failed){
      if(state)state.innerHTML=`<div class="warningBox"><h3>${lang==="ar"?"تعذر تحميل السجل":"History unavailable"}</h3><p>${lang==="ar"?"أعادت خدمة السجل استجابة غير ناجحة. لم تُعرض بيانات بديلة أو مصطنعة.":"The history service returned an unsuccessful response. No substitute or fabricated records were shown."}</p></div>`;
    }else if(state){
      state.innerHTML=completedRecordsHtml(payload,ctx);
    }
    button.disabled=false;
    button.textContent=lang==="ar"?"إعادة تحميل السجل":"Reload protected history";
  });
}
async function dataPage(ctx){
  loadingShell("data",ctx,tx("dataTitle"),tx("dataDesc"));
  const b=await fetchDecisionBundle(ctx,true);
function endpointContextStatus(r,ctx){
  const data=(r&&r.data)||{};
  const pick=(obj,keys)=>{for(const k of keys){const parts=k.split('.');let v=obj;for(const p of parts){if(v==null){v=undefined;break}v=v[p]}if(v!=null&&String(v).trim()!=="")return String(v).trim()}return ""};
  const expected={
    symbol:String((ctx&&ctx.symbol)||"").trim().toUpperCase(),
    timeframe:String((ctx&&ctx.timeframe)||"").trim().toLowerCase(),
    analysisMode:String((ctx&&(ctx.analysisMode||ctx.mode))||"").trim().toLowerCase()
  };
  const got={
    symbol:pick(data,["symbol","instrument.symbol","asset.symbol","request_meta.symbol","meta.symbol"]).toUpperCase(),
    timeframe:pick(data,["timeframe","instrument.timeframe","request_meta.timeframe","meta.timeframe"]).toLowerCase(),
    analysisMode:pick(data,["analysisMode","analysis_mode","mode","request_meta.analysisMode","request_meta.analysis_mode","meta.analysisMode"]).toLowerCase()
  };
  const declared=Boolean(got.symbol||got.timeframe||got.analysisMode);
  const fieldOk=(e,g)=>!e||!g||e===g;
  const ok=fieldOk(expected.symbol,got.symbol)&&fieldOk(expected.timeframe,got.timeframe)&&fieldOk(expected.analysisMode,got.analysisMode);
  const ar=(document.documentElement.dir||"").toLowerCase()==="rtl";
  return {ok,label:declared?(ok?(ar?"مطابق":"Match"):(ar?"غير مطابق":"Mismatch")):(ar?"غير معلن":"Not declared"),got,expected};
}
  const cards=b.telemetry.map(r=>{const cv=endpointContextStatus(r,ctx);return `<article class="provider"><div class="cardHead"><div><strong>${esc(r.name)}</strong><small>${esc(r.url.split("?")[0])}</small></div>${badge(r.error?"FAIL":r.status===200&&cv.ok?"PASS":"WARN")}</div><dl><dt>${tx("http")}</dt><dd>${r.status||"—"}</dd><dt>${tx("latency")}</dt><dd>${r.latency} ms</dd><dt>${tx("contextMatch")}</dt><dd>${esc(cv.label)}</dd><dt>${tx("status")}</dt><dd>${esc(r.error||statusLabel(r.data?.ok===false?"WARN":r.status===200?"PASS":"WARN"))}</dd></dl></article>`}).join("");
  shell(`${pageHero(tx("dataTitle"),tx("dataDesc"),`<button class="btn" id="retryData">${tx("retry")}</button>`)}<div class="infoBox" style="margin-bottom:16px">${tx("noFabrication")}</div><section class="providerGrid">${cards}</section>${rawDetails({telemetry:b.telemetry,health:b.health})}`,"data",ctx);
  document.getElementById("retryData")?.addEventListener("click",()=>dataPage(ctx));
}
function marketsPage(ctx){
  const cards=arr(assetsRegistry.markets).map(m=>`<section class="card"><div class="cardHead"><div><h2>${esc(lang==="ar"?(m.name_ar||m.id):(m.name_en||m.id))}</h2><p>${arr(m.assets).length} ${lang==="ar"?"أصل":"assets"}</p></div><span class="badge gold">${esc(m.id)}</span></div><div class="assetList" style="max-height:none">${arr(m.assets).map(a=>{const symbol=assetSymbol(a);const next={...ctx,market:m.id,symbol,session_id:""};next.session_id=newSession(next);return `<a class="assetBtn" href="${routeHref("home",next)}" data-new-context="true"><b>${esc(symbol)}</b><small>${lang==="ar"?"إنشاء جلسة قرار جديدة":"Create a new decision session"}</small></a>`}).join("")}</div></section>`).join("");
  shell(`${pageHero(tx("marketsTitle"),tx("marketsDesc"),`<a class="btn btnGold" href="${ROUTES.selector.path}">${tx("changeContext")}</a>`)}<div class="grid grid2">${cards}</div>`,"markets",ctx);
  document.querySelectorAll("[data-new-context]").forEach(a=>a.addEventListener("click",()=>{const u=new URL(a.href);const q=u.searchParams;saveContext({market:q.get("market"),symbol:q.get("symbol"),timeframe:q.get("timeframe"),analysis_mode:q.get("mode"),view_mode:q.get("view"),session_id:q.get("session")})}));
}
function guidePage(ctx){ const items=lang==="ar"?[
  ["01","اختر السياق","السوق ثم الأصل ثم الفريم ثم نوع القراءة ثم مستوى العرض."],
  ["02","اقرأ ملخص القرار","الحالة الحاكمة والاتجاه والقوة والجاهزية."],
  ["03","افهم سبب عدم الاكتمال","الموانع تشرح لماذا لا تتحول القراءة القوية تلقائيًا إلى قرار جاهز."],
  ["04","راجع المستويات وNMP","التفعيل والوصول والمراجعة والإلغاء مرتبطة بالسياق المقفل."],
  ["05","اقرأ المخاطر والاعتراض","الدولار والسياق الكلي ثم المخاطر ثم محامي الشيطان."],
  ["06","راجع التفسير المسموح","اعتمد على ملخص القرار والمخاطر والأدلة التي تسمح الحوكمة بعرضها."],
  ["07","راجع السجل وصحة البيانات","القرارات المكتملة والتاريخ وصحة نقاط النهاية في صفحات مستقلة."]
]:[
  ["01","Select context","Market, asset, timeframe, reading type, then view level."],
  ["02","Read the decision summary","Governing state, direction, strength and readiness."],
  ["03","Understand incompletion","Blockers explain why strong evidence does not automatically mean a ready decision."],
  ["04","Review levels and NMP","Activation, arrival, review and invalidation belong to the locked context."],
  ["05","Read risk and challenge","USD and macro, then risk, then Devil's Advocate."],
  ["06","Review governed explanation","Use the decision summary, risk view, and evidence approved for user display."],
  ["07","Review history and data health","Completed decisions, history and endpoint health have dedicated pages."]
]; shell(`${pageHero(tx("guideTitle"),tx("guideDesc"))}<div class="grid grid2">${items.map(([n,t,d])=>`<section class="card"><div class="eyebrow">${n}</div><h2>${esc(t)}</h2><p class="decisionNarrative">${esc(d)}</p></section>`).join("")}</div><div class="infoBox" style="margin-top:16px">${lang==="ar"?"NDSP غرفة دعم قرار تفسيرية وليست منصة تنفيذ أو أوامر شراء وبيع.":"NDSP is an explanatory decision-support room, not an execution or buy/sell order system."}</div>`,"guide",ctx); }

async function render(){
  const page=currentPage(); if(page==="selector"){selectorPage();return} const ctx=assertContextOrRedirect(page); if(!ctx)return; if(page==="layers"||page==="capabilities"){location.replace(routeHref("decision",ctx));return;}
  try{
    if(page==="home")return await homePage(ctx); if(page==="markets")return marketsPage(ctx); if(page==="decision")return await decisionPage(ctx); if(page==="layers")return await layersPage(ctx); if(page==="capabilities")return capabilitiesPage(ctx); if(page==="scenarios")return await scenariosPage(ctx); if(page==="risk")return await riskPage(ctx); if(page==="completed")return await completedPage(ctx); if(page==="data")return await dataPage(ctx); if(page==="guide")return guidePage(ctx);
  }catch(e){shell(`${pageHero(lang==="ar"?"تعذر تحميل الصفحة":"Page load failed",e.message)}<div class="warningBox"><b>${esc(e.message)}</b><br>${tx("noFabrication")}</div>`,page,ctx);}
}

/* NDSP_LAYER_PUBLIC_SEMANTICS_V133_BEGIN */
window.__NDSP_LAYER_PUBLIC_SEMANTICS_V133__={version:"133.0.0",build:"20260718_133000",exactTimeframeOnly:true,noCrossTimeframeFallback:true,noResponseFabrication:true,publicStateVocabulary:true,receivedContractNeverShownAsGenericUnavailable:true,apiRowsArePrimary:true};
function layerSanitizeV133(value){
  const raw=String(value??"");
  if(typeof sanitizePublicNarrativeV129==="function")return sanitizePublicNarrativeV129(raw);
  if(typeof publicTextV125==="function")return publicTextV125(raw);
  return raw.replace(/\bPASSED\b/gi,lang==="ar"?"اجتازت التحقق":"Validation passed").replace(/\bINPUTS_INCOMPLETE\b/gi,lang==="ar"?"مدخلات غير مكتملة":"Inputs incomplete").replace(/\bGOVERNED_REDACTED\b/gi,lang==="ar"?"محجوبة حسب صلاحية العرض":"Redacted by view policy").replace(/\bNOT_EVALUATED\b/gi,lang==="ar"?"لم تُقيّم بعد":"Not evaluated yet").replace(/\bUNDER_MONITORING\b/gi,lang==="ar"?"تحت المتابعة":"Under monitoring").replace(/\s+/g," ").trim();
}
function layerPublicStateV133(layer){
  const raw=String(layerRawStateV125(layer)||"").toUpperCase().trim();
  const ar=lang==="ar";
  if(/GOVERNED_REDACTED/.test(raw))return ar?"محجوبة حسب صلاحية العرض":"Redacted by view policy";
  if(/DATA_BLOCKED|BLOCKED/.test(raw))return ar?"محجوبة بسبب البيانات":"Blocked by data";
  if(/INPUTS_INCOMPLETE|INCOMPLETE/.test(raw))return ar?"مدخلاتها غير مكتملة":"Inputs incomplete";
  if(/NOT_EVALUATED/.test(raw))return ar?"لم تُقيّم بعد":"Not evaluated yet";
  if(/UNDER_MONITORING|PENDING/.test(raw))return ar?"تحت المتابعة":"Under monitoring";
  if(/MONITORING_ONLY/.test(raw))return ar?"متابعة فقط":"Monitoring only";
  if(/UNDER_REVIEW/.test(raw))return ar?"تحت المراجعة":"Under review";
  if(/PARTIAL_AVAILABLE/.test(raw))return ar?"متاحة جزئيًا":"Partially available";
  if(/UNAVAILABLE/.test(raw))return ar?"غير متاحة لهذا السياق":"Unavailable for this context";
  if(/PASSED|\bPASS\b|\bOK\b/.test(raw))return ar?"اجتازت التحقق":"Validation passed";
  if(/COMPLETED|COMPLETE|READY/.test(raw))return ar?"مكتملة":"Complete";
  if(/CONFIRMED/.test(raw))return ar?"مؤكدة":"Confirmed";
  if(/ALIGNED/.test(raw))return ar?"متوافقة":"Aligned";
  if(/ACTIVE|ENABLED/.test(raw))return ar?"نشطة":"Active";
  if(/AVAILABLE/.test(raw))return ar?"متاحة":"Available";
  if(/NEUTRAL/.test(raw))return ar?"محايدة":"Neutral";
  if(/BULLISH/.test(raw))return ar?"ميل صاعد":"Bullish bias";
  if(/BEARISH/.test(raw))return ar?"ميل هابط":"Bearish bias";
  return layerSanitizeV133(statusLabel(raw||"NOT_EVALUATED"));
}
function genericUnavailableV133(value){
  const normalized=String(value||"").replace(/[ـ\s.،,:؛-]+/g,"").toUpperCase();
  return ["UNAVAILABLE","NOTAVAILABLE","غيرمتاح","غيرمتاحة","لاتوجدبيانات","غيرمنشور"].includes(normalized);
}
function layerPublicReasonsV133(layer){
  const raw=String(layerRawStateV125(layer)||"").toUpperCase();
  const received=layerReceivedV125(layer);
  return layerReasonsV125(layer)
    .map(layerSanitizeV133)
    .map(v=>String(v||"").trim())
    .filter(Boolean)
    .filter(value=>{
      if(received&&!/UNAVAILABLE/.test(raw)&&genericUnavailableV133(value))return false;
      if(/\bPASSED\b|\bPASS\b|\bACTIVE\b|\bAVAILABLE\b|\bUNAVAILABLE\b|INPUTS_INCOMPLETE|GOVERNED_REDACTED|NOT_EVALUATED/i.test(value))return false;
      return value.length>=5;
    });
}
function layerPublicNarrativeV133(layer,frame){
  const frameLabel=timeframeLabelV125(frame);
  if(!layerReceivedV125(layer))return lang==="ar"?`لم يصل عقد هذه الوحدة لفريم ${frameLabel}.`:`This unit contract was not received for ${frameLabel}.`;
  const raw=String(layerRawStateV125(layer)||"").toUpperCase();
  const state=layerPublicStateV133(layer);
  const score=layerScoreV125(layer);
  const reasons=layerPublicReasonsV133(layer);
  const scoreText=score===null?"":(lang==="ar"?` ودرجتها ${fmt(score,0)}%`:` with a score of ${fmt(score,0)}%`);
  if(/GOVERNED_REDACTED/.test(raw))return lang==="ar"?`الوحدة مرتبطة بفريم ${frameLabel}، لكن تفاصيلها محجوبة وفق صلاحية العرض الحالية.`:`The unit is bound to ${frameLabel}, but its details are redacted by the current view policy.`;
  if(/DATA_BLOCKED|BLOCKED/.test(raw))return reasons[0]||(lang==="ar"?`الوحدة مرتبطة بالفريم، لكن تقييمها محجوب إلى أن تكتمل البيانات المرجعية المطلوبة.`:`The unit is bound to the timeframe, but evaluation is blocked until the required reference data is complete.`);
  if(/INPUTS_INCOMPLETE|INCOMPLETE/.test(raw))return reasons[0]||(lang==="ar"?`مدخلات هذه الوحدة لم تكتمل بعد لفريم ${frameLabel}.`:`This unit's inputs are not complete yet for ${frameLabel}.`);
  if(/NOT_EVALUATED/.test(raw))return lang==="ar"?`العقد مستلم لفريم ${frameLabel}، لكن الوحدة لم تُقيّم بعد.`:`The contract is received for ${frameLabel}, but the unit has not been evaluated yet.`;
  if(/PASSED|\bPASS\b|\bOK\b/.test(raw))return reasons[0]||(lang==="ar"?`اجتازت الوحدة شرط التحقق الخاص بها على فريم ${frameLabel}${scoreText}.`:`The unit passed its validation condition on ${frameLabel}${scoreText}.`);
  if(/COMPLETED|COMPLETE|READY/.test(raw))return reasons[0]||(lang==="ar"?`اكتملت مخرجات الوحدة على فريم ${frameLabel}${scoreText}.`:`The unit output is complete on ${frameLabel}${scoreText}.`);
  if(/ACTIVE|ENABLED/.test(raw))return reasons[0]||(lang==="ar"?`الوحدة نشطة ومتصلة بعقد فريم ${frameLabel}${scoreText}.`:`The unit is active and bound to the ${frameLabel} contract${scoreText}.`);
  if(/PARTIAL_AVAILABLE/.test(raw))return reasons[0]||(lang==="ar"?`مخرجات الوحدة متاحة جزئيًا على فريم ${frameLabel}${scoreText}.`:`The unit output is partially available on ${frameLabel}${scoreText}.`);
  if(/UNAVAILABLE/.test(raw))return reasons[0]||(lang==="ar"?`الوحدة غير متاحة لهذا السياق على فريم ${frameLabel}.`:`The unit is unavailable for this context on ${frameLabel}.`);
  if(/AVAILABLE/.test(raw))return reasons[0]||(lang==="ar"?`مخرجات الوحدة متاحة ومربوطة بفريم ${frameLabel}${scoreText}.`:`The unit output is available and bound to ${frameLabel}${scoreText}.`);
  if(/UNDER_MONITORING|MONITORING_ONLY|UNDER_REVIEW|PENDING/.test(raw))return reasons[0]||(lang==="ar"?`الوحدة ${state} على فريم ${frameLabel}${scoreText}.`:`The unit is ${state} on ${frameLabel}${scoreText}.`);
  if(reasons.length)return reasons.slice(0,2).join(" · ");
  return score===null?(lang==="ar"?`عقد الوحدة مستلم ومربوط بفريم ${frameLabel}.`:`The unit contract is received and bound to ${frameLabel}.`):(lang==="ar"?`${state} بدرجة ${fmt(score,0)}% على فريم ${frameLabel}.`:`${state} with a score of ${fmt(score,0)}% on ${frameLabel}.`);
}
function layerPublicMetricV133(layer){
  const received=layerReceivedV125(layer);
  const raw=String(layerRawStateV125(layer)||"").toUpperCase();
  const score=layerScoreV125(layer);
  if(!received)return lang==="ar"?"العقد: غير مستلم":"Contract: not received";
  if(score!==null)return lang==="ar"?`درجة الوحدة: ${fmt(score,0)}%`:`Unit score: ${fmt(score,0)}%`;
  if(/GOVERNED_REDACTED/.test(raw))return lang==="ar"?"الدرجة: محجوبة حسب صلاحية العرض":"Score: redacted by view policy";
  return lang==="ar"?"العقد: مستلم، ولا توجد درجة عامة منشورة":"Contract: received; no public numeric score";
}
function layerRegistryMetaV133(layer,index){
  const id=layerIdentifierV125(layer)||`NDSP-CORE-L${String(index+1).padStart(2,"0")}`;
  const registry=arr(layerRegistry?.layers);
  const reg=registry.find(item=>String(item?.id||item?.layer_id||item?.canonical_id||item?.code||"").toUpperCase()===String(id).toUpperCase())||registry[index]||{};
  const source=layer&&typeof layer==="object"?layer:{};
  return {
    id,
    name_ar:pick(reg.name_ar,reg.public_name_ar,source.name_ar,source.public_name_ar,source.name,`الوحدة ${String(index+1).padStart(2,"0")}`),
    name_en:pick(reg.name_en,reg.public_name_en,source.name_en,source.public_name_en,source.name,`Unit ${String(index+1).padStart(2,"0")}`),
    role_ar:pick(reg.role_ar,reg.description_ar,source.role_ar,source.description_ar,"وحدة تحليلية مرتبطة بعقد الفريم المختار."),
    role_en:pick(reg.role_en,reg.description_en,source.role_en,source.description_en,"Analytical unit bound to the selected timeframe contract."),
    blocking:Boolean(reg.blocking??source.blocking??false)
  };
}
function exactLayerRowsV133(x){
  return arr(x?.layers).map((live,index)=>({live,reg:layerRegistryMetaV133(live,index),index})).sort((a,b)=>{
    const ai=Number(String(a.reg.id).match(/L(\d{1,2})$/i)?.[1]||a.index+1);
    const bi=Number(String(b.reg.id).match(/L(\d{1,2})$/i)?.[1]||b.index+1);
    return ai-bi;
  });
}
const layersPageLegacyV133=layersPage;
const riskPageLegacyV133=riskPage;
layersPage=async function layersPageV133(ctx){
  loadingShell("layers",ctx,tx("layersTitle"),tx("layersDesc"));
  const b=await fetchDecisionBundle(ctx); const x=extractDecision(b);
  if(!b.validation.ok){shell(`${pageHero(tx("layersTitle"),tx("layersDesc"))}${mismatchCard(b.validation)}`,"layers",ctx);return}
  const rows=exactLayerRowsV133(x);
  if(rows.length!==16){
    shell(`${pageHero(tx("layersTitle"),tx("layersDesc"))}<div class="warningBox" data-ndsp-v133-error="layer-count">${lang==="ar"?`وصل ${rows.length} عقدًا فقط بدل 16 لهذا الفريم، لذلك حُجب العرض.`:`Only ${rows.length} of 16 layer contracts were received for this timeframe, so the view was blocked.`}</div>`,"layers",ctx);
    return;
  }
  const cards=rows.map(({reg,live})=>{
    const received=layerReceivedV125(live);
    const rawState=layerRawStateV125(live)||"NOT_EVALUATED";
    const publicState=layerPublicStateV133(live);
    const narrative=layerPublicNarrativeV133(live,ctx.timeframe);
    const metric=layerPublicMetricV133(live);
    return `<article class="layerCard ${reg.blocking?"blocking":""} ndsp-v133-layer-card" data-ndsp-v133-layer="yes" data-ndsp-contract-layer="${esc(reg.id)}" data-ndsp-contract-timeframe="${esc(ctx.timeframe)}" data-ndsp-contract-received="${received?"yes":"no"}" data-ndsp-v133-public-state="${esc(publicState)}"><div class="layerTop"><span class="layerId">${esc(reg.id)}</span>${badge(rawState,publicState)}</div><h3>${esc(lang==="ar"?reg.name_ar:reg.name_en)}</h3><p>${esc(lang==="ar"?reg.role_ar:reg.role_en)}</p><div class="layerMeta"><span>${esc(metric)}</span><span>${reg.blocking?tx("blocking"):tx("notBlocking")}</span></div><div class="layerOutput ndsp-v133-layer-contract"><small>${esc(narrative)}</small><strong>${lang==="ar"?`عقد ${timeframeLabelV125(ctx.timeframe)} مرتبط`:`${timeframeLabelV125(ctx.timeframe)} contract bound`}</strong></div></article>`;
  }).join("");
  shell(`${pageHero(tx("layersTitle"),tx("layersDesc"),`<a class="btn" href="${routeHref("capabilities",ctx)}">${tx("capabilitiesTitle")}</a>`)}<div class="infoBox" style="margin-bottom:16px">${lang==="ar"?"كل بطاقة تقرأ عقد الوحدة الحقيقي لنفس الأصل والفريم. لا تُعرض الرموز الداخلية، ولا يعني غياب الدرجة العامة أن العقد غير موجود.":"Each card consumes the real unit contract for the same asset and timeframe. Internal tokens are hidden, and a missing public score does not mean the contract is missing."}</div><section class="layerGrid">${cards}</section>${rawDetails(x.layers)}`,"layers",ctx);
};
riskPage=async function riskPageV133(ctx){
  loadingShell("risk",ctx,tx("riskTitle"),tx("riskDesc"));
  const b=await fetchDecisionBundle(ctx); const x=extractDecision(b);
  if(!b.validation.ok){shell(`${pageHero(tx("riskTitle"),tx("riskDesc"))}${mismatchCard(b.validation)}`,"risk",ctx);return}
  const specs=[[tx("macro"),"L11"],[tx("risk"),"L12"],[tx("devil"),"L15"]];
  const cards=specs.map(([title,code])=>{
    const live=layerByCodeV125(x.layers,code);
    const rawState=layerRawStateV125(live)||"NOT_EVALUATED";
    const publicState=layerPublicStateV133(live);
    const narrative=layerPublicNarrativeV133(live,ctx.timeframe);
    const metric=layerPublicMetricV133(live);
    return `<section class="card ndsp-v133-risk-card" data-ndsp-v133-risk-card="yes" data-ndsp-contract-layer="NDSP-CORE-${code}" data-ndsp-contract-timeframe="${esc(ctx.timeframe)}" data-ndsp-contract-received="${layerReceivedV125(live)?"yes":"no"}" data-ndsp-v133-public-state="${esc(publicState)}"><div class="cardHead"><div><div class="eyebrow">${code}</div><h2>${esc(title)}</h2></div>${badge(rawState,publicState)}</div><p class="decisionNarrative">${esc(narrative)}</p><div class="ndsp-v133-risk-contract"><strong>${lang==="ar"?`عقد ${timeframeLabelV125(ctx.timeframe)} مرتبط`:`${timeframeLabelV125(ctx.timeframe)} contract bound`}</strong><span>${esc(metric)}</span></div></section>`;
  }).join("");
  shell(`${pageHero(tx("riskTitle"),tx("riskDesc"))}<div class="grid grid3">${cards}</div><section class="card" style="margin-top:16px"><div class="cardHead"><div><h2>${tx("whyIncomplete")}</h2></div></div>${blockersHtml(x)}</section>${rawDetails(x.raw)}`,"risk",ctx);
};
/* NDSP_LAYER_PUBLIC_SEMANTICS_V133_END */

await loadRegistries();
await render();
