(function(){
 'use strict';

 const STORE_KEY = 'ndsp_lang';
 const BUTTON_ID = 'ndsp-unified-i18n-switcher';
 const STYLE_ID = 'ndsp-unified-i18n-style';

 const arToEn = {
 /* Public landing */
 "نواف": "Nawaf",
 "كيف تعمل": "How it works",
 "المنهجية": "Methodology",
 "الرادار": "Radar",
 "الباقات": "Plans",
 "دخول المستخدم": "User login",
 "ابدأ تجربة 16 يوم": "Start 16-day trial",
 "منصة نواف لدعم القرار – NDSP": "Nawaf Decision Support Platform — NDSP",
 "غرفة قرار سيادية للقراءات عالية الانضباط.": "A decision room for highly disciplined readings.",
 "غرفة قرار سيادية للقراءات عالية الانضباط": "A decision room for highly disciplined readings",
 "من البيانات المتفرقة إلى قراءة واحدة قابلة للمراجعة.": "From scattered data to one reviewable reading.",
 "ست طبقات معلنة، وعشر طبقات محمية.": "Six declared layers and ten protected layers.",
 "رادار وظيفي بخمس حالات": "Functional radar with five states",
 "ابدأ تجربة 16 يوم قبل اعتماد الاشتراك.": "Start a 16-day trial before subscribing.",
 "ابدأ تجربة NDSP لمدة 16 يوم": "Start your 16-day NDSP trial",
 "أنشئ حسابك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات ضمن تجربة منظمة قبل الاشتراك.": "Create your account to access the NDSP dashboard and follow readings and alerts during a structured trial before subscribing.",

 /* Shared nav/auth */
 "الصفحة الرئيسية": "Home",
 "تسجيل الدخول": "Login",
 "تسجيل مستخدم جديد": "Create new user",
 "مدير النظام": "System admin",
 "مالك النظام": "System owner",
 "الدخول إلى منصة NDSP": "Access the NDSP platform",
 "سجّل دخولك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات وحالة الأسواق.": "Sign in to access the NDSP dashboard, readings, alerts, and market status.",
 "النظام متاح الآن.": "The system is available now.",
 "التسجيل متاح الآن.": "Registration is available now.",
 "لوحة الإدارة متاحة.": "The admin console is available.",
 "منطقة المالك محمية.": "The owner area is protected.",
 "NDSP منصة دعم قرار، وليست منصة تنفيذ أو أوامر تداول.": "NDSP is a decision-support platform, not an execution platform or trading-order system.",
 "بتسجيلك في NDSP فأنت تستخدم منصة دعم قرار معلوماتية، وليست منصة تنفيذ أو توصيات تداول.": "By registering with NDSP, you are using an informational decision-support platform, not an execution or trading-recommendation platform.",
 "هذه الصفحة مخصصة للمديرين المخوّلين فقط.": "This page is for authorized administrators only.",
 "هذه الصفحة مخصصة لمالك النظام فقط وتتطلب صلاحيات عليا.": "This page is for the system owner only and requires elevated permissions.",
 "البريد الإلكتروني": "Email",
 "كلمة المرور": "Password",
 "تأكيد كلمة المرور": "Confirm password",
 "أعد كتابة كلمة المرور": "Re-enter password",
 "الاسم": "Name",
 "اسم المستخدم": "User name",
 "رقم الجوال": "Mobile number",
 "رمز الوصول": "Access code",
 "رمز تحقق ثانوي": "Secondary verification code",
 "نسيت كلمة المرور؟": "Forgot password?",
 "جلسة آمنة": "Secure session",
 "إنشاء الحساب": "Create account",
 "دخول المدير": "Admin login",
 "دخول المالك": "Owner login",
 "العودة للرئيسية": "Back to home",
 "يوم تجربة": "trial days",
 "طبقة حوكمة": "governance layers",
 "مراقبة حالة": "status monitoring",
 "لوحة مدير النظام": "System admin console",
 "لوحة مالك النظام": "System owner console",
 "إدارة الحسابات، متابعة حالة المستخدمين، ومراقبة التشغيل اليومي للمنصة.": "Manage accounts, monitor user status, and oversee daily platform operations.",
 "إدارة الصلاحيات العليا، مراجعة حالة النظام، ومتابعة الإعدادات الحساسة.": "Manage elevated permissions, review system status, and monitor sensitive settings.",

 /* Portal / Empire app */
 "Executive Overview": "النظرة التنفيذية",
 "Markets Monitor": "مراقبة الأسواق",
 "Phase Engine": "محرك المراحل",
 "Intelligence Engine": "محرك الذكاء",
 "Decision Engine": "محرك القرار",
 "Governance & Risk": "الحوكمة والمخاطر",
 "Data Infrastructure": "بنية البيانات",
 "Strategy Lab": "مختبر الاستراتيجية",
 "Architecture": "المعمارية",
 "Decision Intelligence": "ذكاء القرار",
 "Live cross-asset state, regime mapping, decision confidence and governance posture across all monitored markets.": "حالة مباشرة متعددة الأصول، ربط للأنظمة، ثقة القرار، ووضع الحوكمة عبر جميع الأسواق المراقبة.",
 "MARKET STATE": "حالة السوق",
 "DECISION CONFIDENCE": "ثقة القرار",
 "RISK POSTURE": "وضع المخاطر",
 "GOVERNANCE": "الحوكمة",
 "Composite across 16 assets": "قراءة مركبة عبر 16 أصلًا",
 "3 of 4 classes in expansion": "3 من 4 فئات في توسع",
 "Drawdown": "التراجع",
 "Active positions vs trade limit": "المراكز النشطة مقابل حد التداول",
 "LAST 24H": "آخر 24 ساعة",
 "LIVE": "مباشر",
 "MARKETS LIVE": "الأسواق مباشرة",
 "SECURE ACCESS": "وصول آمن",
 "SESSION": "جلسة",
 "SYSTEM ONLINE": "النظام متاح",
 "Risk Analyst": "محلل مخاطر",
 "COMMAND": "الأوامر",
 "INTELLIGENCE": "الذكاء",
 "OPERATIONS": "العمليات",
 "PASS": "اجتاز",
 "WARN": "تنبيه",
 "ARMED": "مفعّل",
 "Kill-Switch": "إيقاف الطوارئ",
 "TRADE LIMIT": "حد التداول",
 "DRAWDOWN": "التراجع",
 "COMPLIANCE": "الامتثال",
 "Position Sizing within VaR": "حجم المراكز ضمن قيمة المخاطر",
 "Concentration < 35% per class": "التركيز أقل من 35% لكل فئة",
 "Liquidity Coverage > 30D": "تغطية السيولة أكثر من 30 يوم",
 "Correlation Cluster Limit": "حد ترابط المجموعة",
 "RISK-ON": "إقبال على المخاطر",
 "MODERATE": "متوسط",
 "Composite": "مركب",
 "Active positions": "مراكز نشطة",
 "Trade limit": "حد التداول",

 /* Plans / common */
 "تجريبي": "Starter",
 "مخصص": "Controlled",
 "الباقات": "Plans",
 "الاشتراك": "Subscription"
 };

 const enToAr = {};
 Object.keys(arToEn).forEach(ar => {
 enToAr[arToEn[ar]] = ar;
 });

 const dictionaries = {
 ar: enToAr,
 en: arToEn
 };

 function currentLang(){
 const saved = localStorage.getItem(STORE_KEY);
 if (saved === 'ar' || saved === 'en') return saved;

 const docLang = (document.documentElement.getAttribute('lang') || '').toLowerCase();
 if (docLang.startsWith('en')) return 'en';
 if (docLang.startsWith('ar')) return 'ar';

 const host = location.hostname;
 if (host === 'my.ndsp.app') return 'en';
 return 'ar';
 }

 function opposite(lang){
 return lang === 'ar' ? 'en' : 'ar';
 }

 function escapeRegExp(str){
 return String(str).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 }

 function translateString(value, lang){
 if (!value || !String(value).trim()) return value;

 const dict = dictionaries[lang] || {};
 let s = String(value);

 const trimmed = s.trim();
 if (dict[trimmed]) {
 return s.replace(trimmed, dict[trimmed]);
 }

 const keys = Object.keys(dict).sort((a,b) => b.length - a.length);
 for (const key of keys) {
 if (!key || key.length < 2) continue;
 if (s.includes(key)) {
 s = s.replace(new RegExp(escapeRegExp(key), 'g'), dict[key]);
 }
 }

 return s;
 }

 function shouldSkipNode(node){
 const p = node.parentElement;
 if (!p) return true;

 const tag = p.tagName;
 if (['SCRIPT','STYLE','NOSCRIPT','TEXTAREA','CODE','PRE','SVG'].includes(tag)) return true;
 if (p.closest('#' + BUTTON_ID)) return true;
 if (p.closest('script,style,noscript,textarea,code,pre,svg')) return true;

 return false;
 }

 function translateTextNodes(lang){
 const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
 acceptNode(node){
 if (shouldSkipNode(node)) return NodeFilter.FILTER_REJECT;
 if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
 return NodeFilter.FILTER_ACCEPT;
 }
 });

 const nodes = [];
 while (walker.nextNode()) nodes.push(walker.currentNode);

 for (const node of nodes) {
 const oldValue = node.nodeValue;
 const newValue = translateString(oldValue, lang);
 if (newValue !== oldValue) node.nodeValue = newValue;
 }
 }

 function translateAttributes(lang){
 const attrs = ['placeholder','title','aria-label','alt','value'];
 const nodes = document.querySelectorAll('input,button,a,img,[title],[aria-label],[placeholder]');

 nodes.forEach(el => {
 attrs.forEach(attr => {
 if (!el.hasAttribute(attr)) return;
 const oldValue = el.getAttribute(attr);
 const newValue = translateString(oldValue, lang);
 if (newValue !== oldValue) el.setAttribute(attr, newValue);
 });
 });
 }

 function injectStyle(){
 const old = document.getElementById(STYLE_ID);
 if (old) old.remove();

 const style = document.createElement('style');
 style.id = STYLE_ID;
 style.textContent = `
 #${BUTTON_ID}{
 position:fixed;
 top:14px;
 inset-inline-start:18px;
 z-index:2147483000;
 display:flex;
 align-items:center;
 gap:6px;
 padding:6px;
 border:1px solid rgba(212,175,55,.34);
 background:linear-gradient(180deg,rgba(14,12,8,.92),rgba(5,5,5,.94));
 color:#f7f1df;
 border-radius:999px;
 box-shadow:0 14px 40px rgba(0,0,0,.28);
 backdrop-filter:blur(10px);
 -webkit-backdrop-filter:blur(10px);
 font-family:system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif;
 }

 #${BUTTON_ID} button{
 border:0;
 border-radius:999px;
 padding:7px 11px;
 background:transparent;
 color:#b9ad91;
 cursor:pointer;
 font-weight:800;
 font-size:12px;
 letter-spacing:.08em;
 }

 #${BUTTON_ID} button.active{
 background:linear-gradient(135deg,#f4d77d,#d4af37);
 color:#080705;
 }

 #${BUTTON_ID} button:hover{
 color:#f4d77d;
 }

 #${BUTTON_ID} button.active:hover{
 color:#080705;
 }

 html[data-ndsp-lang="en"] body{
 direction:ltr;
 }

 html[data-ndsp-lang="ar"] body{
 direction:rtl;
 }

 @media(max-width:760px){
 #${BUTTON_ID}{
 top:10px;
 inset-inline-start:10px;
 transform:scale(.92);
 transform-origin:top left;
 }
 }
 `;
 document.head.appendChild(style);
 }

 function renderButton(lang){
 const old = document.getElementById(BUTTON_ID);
 if (old) old.remove();

 const box = document.createElement('div');
 box.id = BUTTON_ID;
 box.setAttribute('dir','ltr');
 box.innerHTML = `
 <button type="button" data-lang="ar">AR</button>
 <button type="button" data-lang="en">EN</button>
 `;

 document.body.appendChild(box);

 box.querySelectorAll('button').forEach(btn => {
 const bLang = btn.getAttribute('data-lang');
 if (bLang === lang) btn.classList.add('active');

 btn.addEventListener('click', () => {
 setLang(bLang);
 });
 });
 }

 function applyLang(lang){
 document.documentElement.setAttribute('lang', lang);
 document.documentElement.setAttribute('data-ndsp-lang', lang);
 document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

 document.title = translateString(document.title, lang);

 translateTextNodes(lang);
 translateAttributes(lang);

 renderButton(lang);
 }

 function setLang(lang){
 localStorage.setItem(STORE_KEY, lang);
 location.reload();
 }

 function boot(){
 injectStyle();
 const lang = currentLang();
 applyLang(lang);

 let timer = null;
 const obs = new MutationObserver(() => {
 clearTimeout(timer);
 timer = setTimeout(() => {
 injectStyle();
 translateTextNodes(currentLang());
 translateAttributes(currentLang());
 renderButton(currentLang());
 }, 120);
 });

 obs.observe(document.documentElement, {
 childList:true,
 subtree:true
 });
 }

 if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', boot);
 } else {
 boot();
 }
})();
