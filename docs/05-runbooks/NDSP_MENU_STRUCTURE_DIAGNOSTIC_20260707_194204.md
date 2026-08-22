# NDSP Menu Structure Diagnostic
DATE=2026-07-07T19:42:04+02:00
MODE=READ_ONLY
MODIFICATIONS=None
LIVE=/var/www/ndsp-my

## 1) Menu files
-rw-rw-r-- 1 nawaf511 nawaf511 13K يوليو   7 18:18 /var/www/ndsp-my/assets/ndsp-global-menu.css
-rw-rw-r-- 1 nawaf511 nawaf511 11K يوليو   7 09:48 /var/www/ndsp-my/assets/ndsp-global-menu.js

## 2) HTML CSS reference versions
--- asset-selector.html ---
ndsp-global-menu.css?v=mobile-menu-text-v3-20260707_181813
--- NDSP_Asset_View.html ---
ndsp-global-menu.css?v=mobile-menu-text-v3-20260707_181813
--- decision-modes-guide.html ---
ndsp-global-menu.css?v=mobile-menu-text-v3-20260707_181813
--- index.html ---
ndsp-global-menu.css?v=mobile-menu-text-v3-20260707_181813

## 3) CSS menu selectors around panel/link/item
12:.ndsp-menu-button{
16:  inset-inline-start:12px;
24:  color:var(--ndsp-menu-gold2);
34:  -webkit-tap-highlight-color:transparent;
37:.ndsp-menu-button .bars{
43:.ndsp-menu-button .bars::before,
44:.ndsp-menu-button .bars::after,
45:.ndsp-menu-button .bars span{
48:  inset-inline:0;
54:.ndsp-menu-button .bars::before{top:0}
55:.ndsp-menu-button .bars span{top:5.5px}
56:.ndsp-menu-button .bars::after{bottom:0}
58:.ndsp-menu-backdrop{
64:  opacity:0;
66:  transition:opacity .22s ease;
69:.ndsp-menu-panel{
73:  inset-inline-start:10px;
80:  color:var(--ndsp-menu-text);
82:  transform:translateX(calc(-100% - 22px));
83:  transition:transform .24s ease;
91:html[dir="rtl"] .ndsp-menu-panel{
92:  inset-inline-start:auto;
93:  inset-inline-end:10px;
94:  transform:translateX(calc(100% + 22px));
97:body.ndsp-global-menu-open .ndsp-menu-backdrop{
98:  opacity:1;
101:body.ndsp-global-menu-open .ndsp-menu-panel{
102:  transform:translateX(0);
126:  color:#050506;
132:  color:var(--ndsp-menu-gold);
149:  color:var(--ndsp-menu-text);
160:  color:var(--ndsp-menu-muted);
166:.ndsp-menu-links{
171:.ndsp-menu-link{
181:  color:var(--ndsp-menu-text);
185:.ndsp-menu-link.primary{
186:  border-color:rgba(244,210,96,.58);
190:  color:var(--ndsp-menu-gold2);
193:.ndsp-menu-link b{
197:.ndsp-menu-link small{
200:  color:var(--ndsp-menu-muted);
205:.ndsp-menu-link .arrow{
206:  color:var(--ndsp-menu-gold2);
208:  opacity:.85;
216:  color:var(--ndsp-menu-muted);
223:  .ndsp-menu-button{
230:  .ndsp-menu-panel{
239:.ndsp-menu-link.active{
240:  border-color:rgba(244,210,96,.72) !important;
247:.ndsp-menu-link.active b{
248:  color:#ffe18a !important;
262:.ndsp-menu-panel{
268:  scrollbar-color:rgba(212,175,55,.62) rgba(8,8,10,.38) !important;
273:.ndsp-menu-panel::-webkit-scrollbar{
278:.ndsp-menu-panel::-webkit-scrollbar-track{
283:.ndsp-menu-panel::-webkit-scrollbar-thumb{
289:.ndsp-menu-panel::-webkit-scrollbar-button{
295:.ndsp-menu-panel *{
300:.ndsp-menu-backdrop{
307:  .ndsp-menu-panel{
309:    inset-inline:8px !important;
316:  .ndsp-menu-panel a,
317:  .ndsp-menu-panel button,
318:  .ndsp-menu-panel [role="button"]{
324:  .ndsp-menu-panel{
326:    inset-inline:6px !important;
332:  .ndsp-menu-panel::-webkit-scrollbar{
348:.ndsp-menu-panel{
349:  right:14px !important;
350:  left:auto !important;
357:  color:#f7efe0 !important;
358:  opacity:1 !important;
366:.ndsp-menu-panel,
367:.ndsp-menu-panel *{
371:.ndsp-menu-panel a,
372:.ndsp-menu-panel button,
373:.ndsp-menu-panel [role="button"],
374:.ndsp-menu-panel .ndsp-menu-link,
375:.ndsp-menu-panel .ndsp-menu-item{
376:  color:#f5efe3 !important;
377:  opacity:1 !important;
380:.ndsp-menu-panel a *,
381:.ndsp-menu-panel button *,
382:.ndsp-menu-panel [role="button"] *,
383:.ndsp-menu-panel .ndsp-menu-link *,
384:.ndsp-menu-panel .ndsp-menu-item *{
385:  color:inherit !important;
386:  opacity:1 !important;
389:.ndsp-menu-panel a,
390:.ndsp-menu-panel .ndsp-menu-link,
391:.ndsp-menu-panel .ndsp-menu-item{
393:  border-color:rgba(212,175,55,.26) !important;
396:.ndsp-menu-panel a:hover,
397:.ndsp-menu-panel button:hover,
398:.ndsp-menu-panel [role="button"]:hover,
399:.ndsp-menu-panel .ndsp-menu-link:hover,
400:.ndsp-menu-panel .ndsp-menu-item:hover{
402:  border-color:rgba(244,210,96,.58) !important;
405:.ndsp-menu-panel [aria-current="page"],
406:.ndsp-menu-panel .active,
407:.ndsp-menu-panel .is-active{
409:  border-color:rgba(244,210,96,.78) !important;
410:  color:#ffe18a !important;
413:.ndsp-menu-panel small,
414:.ndsp-menu-panel p,
415:.ndsp-menu-panel span{
416:  opacity:1 !important;
419:.ndsp-menu-backdrop{
426:  .ndsp-menu-panel{
427:    left:8px !important;
428:    right:8px !important;
436:  .ndsp-menu-panel{
437:    left:6px !important;
438:    right:6px !important;
451:.ndsp-menu-panel{
456:  opacity:1 !important;
461:.ndsp-menu-panel::before,
462:.ndsp-menu-panel::after{
463:  opacity:.18 !important;
467:.ndsp-menu-panel,
468:.ndsp-menu-panel *{
470:  opacity:1 !important;
476:.ndsp-menu-panel :is(a,button,div,span,p,small,strong,b,h1,h2,h3,h4,label){
477:  color:#f8f0df !important;
478:  -webkit-text-fill-color:#f8f0df !important;
481:.ndsp-menu-panel :is(a,button,[role="button"],.ndsp-menu-link,.ndsp-menu-item){
484:  color:#f8f0df !important;
485:  -webkit-text-fill-color:#f8f0df !important;
488:.ndsp-menu-panel :is(a,button,[role="button"],.ndsp-menu-link,.ndsp-menu-item) :is(span,p,small,strong,b,div){
489:  color:#f8f0df !important;
490:  -webkit-text-fill-color:#f8f0df !important;
491:  opacity:1 !important;
494:.ndsp-menu-panel :is(a,button,[role="button"],.ndsp-menu-link,.ndsp-menu-item):hover{
496:  border-color:rgba(244,210,96,.72) !important;
499:.ndsp-menu-panel :is([aria-current="page"],.active,.is-active){
501:  border-color:rgba(244,210,96,.86) !important;
502:  color:#ffe18a !important;
503:  -webkit-text-fill-color:#ffe18a !important;
506:.ndsp-menu-panel :is([aria-current="page"],.active,.is-active) *{
507:  color:#ffe18a !important;
508:  -webkit-text-fill-color:#ffe18a !important;
511:.ndsp-menu-backdrop{

## 4) JS generated class names and labels
4:  - Match menu labels with official canonical NDSP page routes.
13:  function lang(){
15:    try { saved = localStorage.getItem("ndsp_lang") || ""; } catch(e){}
16:    var htmlLang = document.documentElement.lang || "";
22:      return new URL(location.href).searchParams.get("symbol") || "BTCUSDT";
151:  function label(item){
152:    return lang() === "ar" ? item.ar : item.en;
156:    return lang() === "ar" ? item.subAr : item.subEn;
160:    var ar = lang() === "ar";
162:      menu: ar ? "القائمة" : "Menu",
174:        : "Menu labels match official routes. NDSP is a decision-support platform, not financial advice or execution instruction."
178:  function href(path){
192:    return '<a class="ndsp-menu-link '+(primary?'primary':'')+active+'" href="'+href(path)+'">' +
193:      '<span><b>'+label(item)+'</b><small>'+sub(item)+'</small></span>' +
201:      document.title = "NDSP — " + label(item);
202:      document.documentElement.setAttribute("data-ndsp-page-name", label(item));
209:    document.querySelectorAll(".ndsp-menu-button,.ndsp-menu-backdrop,.ndsp-menu-panel").forEach(function(el){
215:    var btn = document.createElement("button");
216:    btn.className = "ndsp-menu-button";
218:    btn.setAttribute("aria-label", t.menu);
219:    btn.innerHTML = '<span class="bars"><span></span></span><span>'+t.menu+'</span>';
221:    var backdrop = document.createElement("div");
222:    backdrop.className = "ndsp-menu-backdrop";
224:    var panel = document.createElement("nav");
225:    panel.className = "ndsp-menu-panel";
226:    panel.setAttribute("aria-label", t.menu);
228:    panel.innerHTML =
229:      '<div class="ndsp-menu-head">' +
230:        '<div class="ndsp-menu-brand">' +
231:          '<div class="ndsp-menu-mark">ND</div>' +
234:        '<button class="ndsp-menu-close" type="button" aria-label="'+t.close+'">×</button>' +
237:      '<div class="ndsp-menu-group">' +
238:        '<p class="ndsp-menu-group-title">'+t.main+'</p>' +
239:        '<div class="ndsp-menu-links">' +
244:      '<div class="ndsp-menu-group">' +
245:        '<p class="ndsp-menu-group-title">'+t.decision+'</p>' +
246:        '<div class="ndsp-menu-links">' +
253:      '<div class="ndsp-menu-group">' +
254:        '<p class="ndsp-menu-group-title">'+t.macro+'</p>' +
255:        '<div class="ndsp-menu-links">' +
263:      '<div class="ndsp-menu-group">' +
264:        '<p class="ndsp-menu-group-title">'+t.follow+'</p>' +
265:        '<div class="ndsp-menu-links">' +
272:      '<div class="ndsp-menu-group">' +
273:        '<p class="ndsp-menu-group-title">'+t.guides+'</p>' +
274:        '<div class="ndsp-menu-links">' +
283:      '<div class="ndsp-menu-group">' +
284:        '<p class="ndsp-menu-group-title">'+t.legal+'</p>' +
285:        '<div class="ndsp-menu-links">' +
290:      '<div class="ndsp-menu-note">'+t.note+'</div>';
297:      document.documentElement.classList.add("ndsp-menu-open");
301:      document.documentElement.classList.remove("ndsp-menu-open");
307:    var closeBtn = panel.querySelector(".ndsp-menu-close");

## 5) Patch markers
252:/* NDSP_MOBILE_MENU_CSS_ONLY_V1_START */
336:/* NDSP_MOBILE_MENU_CSS_ONLY_V1_END */
338:/* NDSP_MOBILE_MENU_CSS_ONLY_V2_START */
443:/* NDSP_MOBILE_MENU_CSS_ONLY_V2_END */
445:/* NDSP_MOBILE_MENU_TEXT_READABILITY_V3_START */
516:/* NDSP_MOBILE_MENU_TEXT_READABILITY_V3_END */

FINAL_STATUS=MENU_STRUCTURE_DIAGNOSTIC_DONE
REPORT=docs/05-runbooks/NDSP_MENU_STRUCTURE_DIAGNOSTIC_20260707_194204.md
