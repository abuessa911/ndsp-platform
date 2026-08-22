(function(){
 "use strict";

 const API = "https://api.ndsp.app";
 const DEFAULT_SYMBOL = "BTCUSDT";

 function symbol(){
 return localStorage.getItem("ndsp_symbol") ||
 localStorage.getItem("NDSP_SYMBOL") ||
 DEFAULT_SYMBOL;
 }

 function fmt(v){
 if(v === null || v === undefined || v === "") return "—";
 if(typeof v === "number"){
 return Math.abs(v) >= 1000
 ? v.toLocaleString("en-US", {maximumFractionDigits:2})
 : v.toLocaleString("en-US", {maximumFractionDigits:2});
 }
 return String(v);
 }

 async function get(path){
 const sep = path.includes("?") ? "&" : "?";
 const r = await fetch(API + path + sep + "_=" + Date.now(), {cache:"no-store"});
 return await r.json();
 }

 function allTextNodes(){
 const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
 const out = [];
 let n;
 while(n = walker.nextNode()){
 if(n.nodeValue && n.nodeValue.trim()) out.push(n);
 }
 return out;
 }

 function setNear(labelRegex, value){
 const nodes = allTextNodes();
 for(const n of nodes){
 const t = n.nodeValue.trim();
 if(!labelRegex.test(t)) continue;

 let box = n.parentElement;
 for(let i=0;i<5 && box;i++,box=box.parentElement){
 const candidates = Array.from(box.querySelectorAll("span,div,p,strong,b"));
 const useful = candidates.filter(x => {
 const s = (x.textContent || "").trim();
 return s && s.length < 80 && !labelRegex.test(s);
 });
 if(useful.length){
 useful[useful.length - 1].textContent = fmt(value);
 return true;
 }
 }
 }
 return false;
 }

 function markLive(){
 document.documentElement.setAttribute("data-ndsp-live-binding","active");
 let badge = document.getElementById("ndsp-live-binding-badge");
 if(!badge){
 badge = document.createElement("div");
 badge.id = "ndsp-live-binding-badge";
 badge.style.cssText = "position:fixed;left:14px;bottom:14px;z-index:99999;padding:7px 10px;border:1px solid rgba(212,175,55,.35);background:rgba(10,10,12,.88);color:#D4AF37;border-radius:999px;font:12px/1.2 system-ui,Tahoma;backdrop-filter:blur(8px);pointer-events:none";
 document.body.appendChild(badge);
 }
 badge.textContent = "Live Backend · " + symbol();
 }

 async function bind(){
 try{
 markLive();

 const s = encodeURIComponent(symbol());
 const overview = await get("/api/dashboard/overview?symbol=" + s);
 const asset = await get("/api/market/assets?symbol=" + s);
 const layers = await get("/api/layers?symbol=" + s);
 const structure = await get("/api/market-structure?symbol=" + s);
 const technical = await get("/api/technical-confirmation?symbol=" + s);
 const macro = await get("/api/macro-analysis?symbol=" + s);
 const risk = await get("/api/risk-layer?symbol=" + s);
 const signal = await get("/api/nawaf-signal?symbol=" + s);

 if(!overview.ok) return;

 setNear(/السعر|Live Price|price/i, overview.live_price);
 setNear(/جودة القرار|Decision Quality/i, overview.decision_quality);
 setNear(/الاتجاه|السياق|Directional|Bias/i, overview.directional_bias);
 setNear(/حالة السوق|Market State/i, overview.market_state);
 setNear(/الأفق|Horizon/i, overview.reading_horizon);
 setNear(/قوة الأفق|Horizon Strength/i, overview.horizon_strength);
 setNear(/السيناريو|Scenario/i, overview.scenario_state);
 setNear(/إشارة نواف|الذهبية|Golden/i, overview.golden_label || overview.golden_status);
 setNear(/المزود|Provider/i, overview.provider);

 if(asset.ok && asset.live){
 setNear(/RSI|القوة النسبية/i, asset.live.rsi_4h);
 setNear(/ATR|التذبذب/i, asset.live.atr_4h);
 setNear(/24h|٢٤|24 ساعة/i, asset.live.price_change_24h_pct + "%");
 setNear(/H1|ساعة/i, asset.live.h1_direction);
 setNear(/H4|٤ ساعات/i, asset.live.h4_direction);
 setNear(/D1|يومي/i, asset.live.d1_direction);
 setNear(/الإطار|Timeframe/i, asset.live.selected_timeframe_label);
 }

 if(structure.ok){
 setNear(/هيكل السوق|Market Structure/i, structure.market_state);
 setNear(/سعر المراجعة|Review Price/i, structure.technical_review_price);
 }

 if(technical.ok){
 setNear(/التأكيد الفني|Technical Confirmation/i, technical.confirmation_state);
 }

 if(macro.ok){
 setNear(/العوامل الكلية|Macro/i, macro.macro_state);
 }

 if(risk.ok){
 setNear(/التحفظ|المخاطر|Risk|Caution/i, risk.caution_reason || risk.scenario_risk_note);
 setNear(/منطقة المراجعة|Review Zone/i, risk.scenario_review_zone);
 setNear(/الإبطال|Invalidation/i, risk.scenario_invalidation_level);
 }

 if(signal.ok){
 setNear(/إشارة نواف|Golden Signal/i, signal.golden_status);
 }

 window.NDSP_LIVE_BACKEND = {
 ok:true,
 symbol:symbol(),
 overview,
 asset,
 layers,
 structure,
 technical,
 macro,
 risk,
 signal,
 updated_at:new Date().toISOString()
 };

 }catch(e){
 console.warn("NDSP live binding failed", e);
 }
 }

 window.NDSP_RELOAD_LIVE_BINDING = bind;

 if(document.readyState === "loading"){
 document.addEventListener("DOMContentLoaded", bind);
 }else{
 bind();
 }

 setInterval(bind, 30000);
})();
