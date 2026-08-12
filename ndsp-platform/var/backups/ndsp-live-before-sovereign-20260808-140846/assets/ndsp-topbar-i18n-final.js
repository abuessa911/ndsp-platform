(function(){
 'use strict';

 const STORE_KEY = 'ndsp_lang';
 const BUTTON_ID = 'ndsp-topbar-lang-switcher';
 const STYLE_ID = 'ndsp-topbar-lang-style';

 const arToEn = {
 "الصفحة الرئيسية": "Home",
 "تسجيل الدخول": "Login",
 "تسجيل مستخدم جديد": "Create new user",
 "مدير النظام": "System admin",
 "مالك النظام": "System owner",

 "الدخول إلى منصة NDSP": "Access the NDSP platform",
 "ابدأ تجربة NDSP لمدة 16 يوم": "Start your 16-day NDSP trial",
 "لوحة مدير النظام": "System admin console",
 "لوحة مالك النظام": "System owner console",

 "سجّل دخولك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات وحالة الأسواق.": "Sign in to access the NDSP dashboard, readings, alerts, and market status.",
 "أنشئ حسابك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات ضمن تجربة منظمة قبل الاشتراك.": "Create your account to access the NDSP dashboard and follow readings and alerts during a structured trial before subscribing.",
 "إدارة الحسابات، متابعة حالة المستخدمين، ومراقبة التشغيل اليومي للمنصة.": "Manage accounts, monitor user status, and oversee daily platform operations.",
 "إدارة الصلاحيات العليا، مراجعة حالة النظام، ومتابعة الإعدادات الحساسة.": "Manage elevated permissions, review system status, and monitor sensitive settings.",

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
 "دخول المستخدم": "User login",
 "إنشاء الحساب": "Create account",
 "دخول المدير": "Admin login",
 "دخول المالك": "Owner login",
 "العودة للرئيسية": "Back to home",

 "يوم تجربة": "trial days",
 "طبقة حوكمة": "governance layers",
 "مراقبة حالة": "status monitoring",

 "النظام متاح الآن.": "The system is available now.",
 "التسجيل متاح الآن.": "Registration is available now.",
 "لوحة الإدارة متاحة.": "The admin console is available.",
 "منطقة المالك محمية.": "The owner area is protected.",

 "NDSP منصة دعم قرار، وليست منصة تنفيذ أو أوامر تداول.": "NDSP is a decision-support platform, not an execution platform or trading-order system.",
 "بتسجيلك في NDSP فأنت تستخدم منصة دعم قرار معلوماتية، وليست منصة تنفيذ أو توصيات تداول.": "By registering with NDSP, you are using an informational decision-support platform, not an execution or trading-recommendation platform.",
 "هذه الصفحة مخصصة للمديرين المخوّلين فقط.": "This page is for authorized administrators only.",
 "هذه الصفحة مخصصة لمالك النظام فقط وتتطلب صلاحيات عليا.": "This page is for the system owner only and requires elevated permissions.",

 "نواف": "Nawaf",
 "كيف تعمل": "How it works",
 "المنهجية": "Methodology",
 "الرادار": "Radar",
 "الباقات": "Plans",
 "منصة نواف لدعم القرار – NDSP": "Nawaf Decision Support Platform — NDSP",
 "غرفة قرار سيادية للقراءات عالية الانضباط.": "A decision room for highly disciplined readings.",
 "من البيانات المتفرقة إلى قراءة واحدة قابلة للمراجعة.": "From scattered data to one reviewable reading.",
 "ست طبقات معلنة، وعشر طبقات محمية.": "Six declared layers and ten protected layers.",
 "ابدأ تجربة 16 يوم": "Start 16-day trial",

 "Executive Overview": "النظرة التنفيذية",
 "Markets Monitor": "مراقبة الأسواق",
 "Phase Engine": "محرك المراحل",
 "Intelligence Engine": "محرك الذكاء",
 "Decision Engine": "محرك القرار",
 "Governance & Risk": "الحوكمة والمخاطر",
 "Data Infrastructure": "بنية البيانات",
 "Decision Intelligence": "ذكاء القرار",
 "Live cross-asset state, regime mapping, decision confidence and governance posture across all monitored markets.": "حالة مباشرة متعددة الأصول، ربط للأنظمة، ثقة القرار، ووضع الحوكمة عبر جميع الأسواق المراقبة.",
 "MARKET STATE": "حالة السوق",
 "DECISION CONFIDENCE": "ثقة القرار",
 "RISK POSTURE": "وضع المخاطر",
 "GOVERNANCE": "الحوكمة",
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
 "RISK-ON": "إقبال على المخاطر",
 "MODERATE": "متوسط",
 "LIVE": "مباشر",
 "LAST 24H": "آخر 24 ساعة"
 };

 const enToAr = {};
 Object.keys(arToEn).forEach(ar => {
 enToAr[arToEn[ar]] = ar;
 });

 function hasArabicText(){
 return /[\u0600-\u06FF]/.test(document.body ? document.body.innerText : '');
 }

 function sourceLang(){
 return hasArabicText() ? 'ar' : 'en';
 }

 function desiredLang(){
 const saved = localStorage.getItem(STORE_KEY);
 if (saved === 'ar' || saved === 'en') return saved;

 const htmlLang = (document.documentElement.getAttribute('lang') || '').toLowerCase();
 if (htmlLang.startsWith('ar')) return 'ar';
 if (htmlLang.startsWith('en')) return 'en';

 return sourceLang();
 }

 function dictFor(from, to){
 if (from === to) return {};
 if (from === 'ar' && to === 'en') return arToEn;
 if (from === 'en' && to === 'ar') return enToAr;
 return {};
 }

 function escapeRegExp(str){
 return String(str).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 }

 function translateString(value, dict){
 if (!value || !String(value).trim()) return value;

 let s = String(value);
 const trimmed = s.trim();

 if (dict[trimmed]) return s.replace(trimmed, dict[trimmed]);

 Object.keys(dict).sort((a,b) => b.length - a.length).forEach(key => {
 if (key && s.includes(key)) {
 s = s.replace(new RegExp(escapeRegExp(key), 'g'), dict[key]);
 }
 });

 return s;
 }

 function skipTextNode(node){
 const p = node.parentElement;
 if (!p) return true;
 if (p.closest('script,style,noscript,textarea,code,pre,svg')) return true;
 if (p.closest('#' + BUTTON_ID)) return true;
 return false;
 }

 function translatePage(from, to){
 const dict = dictFor(from, to);

 if (Object.keys(dict).length) {
 const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
 acceptNode(node){
 if (skipTextNode(node)) return NodeFilter.FILTER_REJECT;
 if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
 return NodeFilter.FILTER_ACCEPT;
 }
 });

 const nodes = [];
 while (walker.nextNode()) nodes.push(walker.currentNode);

 nodes.forEach(node => {
 const oldValue = node.nodeValue;
 const newValue = translateString(oldValue, dict);
 if (newValue !== oldValue) node.nodeValue = newValue;
 });

 const attrs = ['placeholder','title','aria-label','alt','value'];
 document.querySelectorAll('input,button,a,img,[placeholder],[title],[aria-label]').forEach(el => {
 attrs.forEach(attr => {
 if (!el.hasAttribute(attr)) return;
 const oldValue = el.getAttribute(attr);
 const newValue = translateString(oldValue, dict);
 if (newValue !== oldValue) el.setAttribute(attr, newValue);
 });
 });

 document.title = translateString(document.title, dict);
 }

 document.documentElement.setAttribute('lang', to);
 document.documentElement.setAttribute('dir', to === 'ar' ? 'rtl' : 'ltr');
 document.documentElement.setAttribute('data-ndsp-lang', to);
 }

 function injectStyle(){
 document.getElementById(STYLE_ID)?.remove();

 const style = document.createElement('style');
 style.id = STYLE_ID;
 style.textContent = `
 #${BUTTON_ID}{
 display:inline-flex;
 align-items:center;
 gap:6px;
 padding:6px;
 border:1px solid rgba(212,175,55,.34);
 background:linear-gradient(180deg,rgba(14,12,8,.92),rgba(5,5,5,.94));
 color:#f7f1df;
 border-radius:999px;
 box-shadow:0 12px 30px rgba(0,0,0,.20);
 font-family:system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif;
 flex:0 0 auto;
 }

 #${BUTTON_ID} button{
 border:0;
 border-radius:999px;
 padding:7px 12px;
 background:transparent;
 color:#b9ad91;
 cursor:pointer;
 font-weight:900;
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

.ndsp-lang-topbar-slot{
 display:flex;
 align-items:center;
 justify-content:flex-end;
 gap:10px;
 flex:0 0 auto;
 }

 @media(max-width:760px){
 #${BUTTON_ID}{
 transform:scale(.92);
 transform-origin:center;
 }
 }
 `;
 document.head.appendChild(style);
 }

 function buildButton(lang){
 const box = document.createElement('div');
 box.id = BUTTON_ID;
 box.setAttribute('dir','ltr');

 box.innerHTML = `
 <button type="button" data-lang="ar">AR</button>
 <button type="button" data-lang="en">EN</button>
 `;

 box.querySelectorAll('button').forEach(btn => {
 const bLang = btn.getAttribute('data-lang');
 if (bLang === lang) btn.classList.add('active');

 btn.addEventListener('click', function(){
 localStorage.setItem(STORE_KEY, bLang);
 location.reload();
 });
 });

 return box;
 }

 function placeButton(lang){
 document.getElementById(BUTTON_ID)?.remove();
 document.querySelectorAll('.ndsp-lang-topbar-slot').forEach(x => x.remove());

 const slot = document.createElement('div');
 slot.className = 'ndsp-lang-topbar-slot';
 slot.appendChild(buildButton(lang));

 const topbar = document.querySelector('.topbar');
 if (topbar) {
 topbar.appendChild(slot);
 return;
 }

 const header = document.querySelector('header');
 if (header) {
 header.appendChild(slot);
 return;
 }

 const nav = document.querySelector('nav');
 if (nav) {
 nav.parentElement.insertBefore(slot, nav);
 return;
 }

 document.body.insertBefore(slot, document.body.firstChild);
 }

 function boot(){
 injectStyle();

 const from = sourceLang();
 const to = desiredLang();

 translatePage(from, to);
 placeButton(to);
 }

 if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', boot);
 } else {
 boot();
 }
})();
