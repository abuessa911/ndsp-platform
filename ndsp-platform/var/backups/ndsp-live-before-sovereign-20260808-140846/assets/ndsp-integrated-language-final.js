(function(){
 'use strict';

 const STORE_KEY = 'ndsp_final_lang';
 const BUTTON_ID = 'ndsp-integrated-lang-switcher';
 const STYLE_ID = 'ndsp-integrated-lang-style';

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
 "دخول المستخدم": "User login",
 "ابدأ تجربة 16 يوم": "Start 16-day trial",
 "منصة نواف لدعم القرار – NDSP": "Nawaf Decision Support Platform — NDSP",
 "غرفة قرار سيادية للقراءات عالية الانضباط.": "A decision room for highly disciplined readings.",
 "من البيانات المتفرقة إلى قراءة واحدة قابلة للمراجعة.": "From scattered data to one reviewable reading.",
 "ست طبقات معلنة، وعشر طبقات محمية.": "Six declared layers and ten protected layers.",

 "النظرة التنفيذية": "Executive Overview",
 "مراقبة الأسواق": "Markets Monitor",
 "محرك المراحل": "Phase Engine",
 "محرك الذكاء": "Intelligence Engine",
 "محرك القرار": "Decision Engine",
 "الحوكمة والمخاطر": "Governance & Risk",
 "بنية البيانات": "Data Infrastructure",
 "مختبر الاستراتيجية": "Strategy Lab",
 "المعمارية": "Architecture",
 "ذكاء القرار": "Decision Intelligence",
 "حالة مباشرة متعددة الأصول، ربط للأنظمة، ثقة القرار، ووضع الحوكمة عبر جميع الأسواق المراقبة.": "Live cross-asset state, regime mapping, decision confidence and governance posture across all monitored markets.",
 "حالة السوق": "Market state",
 "ثقة القرار": "Decision confidence",
 "وضع المخاطر": "Risk posture",
 "الحوكمة": "Governance",
 "قراءة مركبة عبر 16 أصلًا": "Composite across 16 assets",
 "3 من 4 فئات في توسع": "3 of 4 classes in expansion",
 "جلسة": "Session",
 "الأسواق مباشرة": "Markets live",
 "وصول آمن": "Secure access",
 "النظام متاح": "System online",
 "محلل مخاطر": "Risk Analyst",
 "الأوامر": "Command",
 "الذكاء": "Intelligence",
 "العمليات": "Operations",
 "اجتاز": "Pass",
 "تنبيه": "Warn",
 "مفعّل": "Armed",
 "إيقاف الطوارئ": "Kill-Switch",
 "حد التداول": "Trade limit",
 "التراجع": "Drawdown",
 "الامتثال": "Compliance",
 "إقبال على المخاطر": "Risk-on",
 "متوسط": "Moderate",
 "مباشر": "Live",
 "آخر 24 ساعة": "Last 24H"
 };

 const enToAr = {
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
 "Market state": "حالة السوق",
 "DECISION CONFIDENCE": "ثقة القرار",
 "Decision confidence": "ثقة القرار",
 "RISK POSTURE": "وضع المخاطر",
 "Risk posture": "وضع المخاطر",
 "GOVERNANCE": "الحوكمة",
 "Governance": "الحوكمة",
 "Composite across 16 assets": "قراءة مركبة عبر 16 أصلًا",
 "3 of 4 classes in expansion": "3 من 4 فئات في توسع",
 "SESSION": "جلسة",
 "Session": "جلسة",
 "MARKETS LIVE": "الأسواق مباشرة",
 "Markets live": "الأسواق مباشرة",
 "SECURE ACCESS": "وصول آمن",
 "Secure access": "وصول آمن",
 "SYSTEM ONLINE": "النظام متاح",
 "System online": "النظام متاح",
 "Risk Analyst": "محلل مخاطر",
 "COMMAND": "الأوامر",
 "Command": "الأوامر",
 "INTELLIGENCE": "الذكاء",
 "Intelligence": "الذكاء",
 "OPERATIONS": "العمليات",
 "Operations": "العمليات",
 "PASS": "اجتاز",
 "WARN": "تنبيه",
 "ARMED": "مفعّل",
 "Kill-Switch": "إيقاف الطوارئ",
 "TRADE LIMIT": "حد التداول",
 "Trade limit": "حد التداول",
 "DRAWDOWN": "التراجع",
 "Drawdown": "التراجع",
 "COMPLIANCE": "الامتثال",
 "Compliance": "الامتثال",
 "RISK-ON": "إقبال على المخاطر",
 "Risk-on": "إقبال على المخاطر",
 "MODERATE": "متوسط",
 "Moderate": "متوسط",
 "LIVE": "مباشر",
 "Live": "مباشر",
 "LAST 24H": "آخر 24 ساعة",
 "Last 24H": "آخر 24 ساعة",

 "Home": "الصفحة الرئيسية",
 "Login": "تسجيل الدخول",
 "Create new user": "تسجيل مستخدم جديد",
 "System admin": "مدير النظام",
 "System owner": "مالك النظام",
 "Access the NDSP platform": "الدخول إلى منصة NDSP",
 "Start your 16-day NDSP trial": "ابدأ تجربة NDSP لمدة 16 يوم",
 "System admin console": "لوحة مدير النظام",
 "System owner console": "لوحة مالك النظام",
 "Sign in to access the NDSP dashboard, readings, alerts, and market status.": "سجّل دخولك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات وحالة الأسواق.",
 "Create your account to access the NDSP dashboard and follow readings and alerts during a structured trial before subscribing.": "أنشئ حسابك للوصول إلى لوحة NDSP ومتابعة القراءات والتنبيهات ضمن تجربة منظمة قبل الاشتراك.",
 "Email": "البريد الإلكتروني",
 "Password": "كلمة المرور",
 "Confirm password": "تأكيد كلمة المرور",
 "Re-enter password": "أعد كتابة كلمة المرور",
 "Name": "الاسم",
 "User name": "اسم المستخدم",
 "Mobile number": "رقم الجوال",
 "Access code": "رمز الوصول",
 "Secondary verification code": "رمز تحقق ثانوي",
 "Forgot password?": "نسيت كلمة المرور؟",
 "Secure session": "جلسة آمنة",
 "User login": "دخول المستخدم",
 "Create account": "إنشاء الحساب",
 "Admin login": "دخول المدير",
 "Owner login": "دخول المالك",
 "Back to home": "العودة للرئيسية",
 "trial days": "يوم تجربة",
 "governance layers": "طبقة حوكمة",
 "status monitoring": "مراقبة حالة",
 "The system is available now.": "النظام متاح الآن.",
 "Registration is available now.": "التسجيل متاح الآن.",
 "The admin console is available.": "لوحة الإدارة متاحة.",
 "The owner area is protected.": "منطقة المالك محمية."
 };

 function selectedLang(){
 const saved = localStorage.getItem(STORE_KEY);
 if (saved === 'ar' || saved === 'en') return saved;
 return 'ar';
 }

 function escapeRegExp(str){
 return String(str).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 }

 function translateString(value, lang){
 if (!value || !String(value).trim()) return value;

 const dict = lang === 'ar' ? enToAr : arToEn;
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

 function skipNode(node){
 const p = node.parentElement;
 if (!p) return true;
 if (p.closest('script,style,noscript,textarea,code,pre,svg')) return true;
 if (p.closest('#' + BUTTON_ID)) return true;
 return false;
 }

 function applyText(lang){
 if (!document.body) return;

 const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
 acceptNode(node){
 if (skipNode(node)) return NodeFilter.FILTER_REJECT;
 if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
 return NodeFilter.FILTER_ACCEPT;
 }
 });

 const nodes = [];
 while (walker.nextNode()) nodes.push(walker.currentNode);

 nodes.forEach(node => {
 const oldValue = node.nodeValue;
 const newValue = translateString(oldValue, lang);
 if (newValue !== oldValue) node.nodeValue = newValue;
 });

 const attrs = ['placeholder','title','aria-label','alt','value'];
 document.querySelectorAll('input,button,a,img,[placeholder],[title],[aria-label]').forEach(el => {
 attrs.forEach(attr => {
 if (!el.hasAttribute(attr)) return;
 const oldValue = el.getAttribute(attr);
 const newValue = translateString(oldValue, lang);
 if (newValue !== oldValue) el.setAttribute(attr, newValue);
 });
 });

 document.title = translateString(document.title, lang);
 document.documentElement.setAttribute('lang', lang);
 document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
 document.documentElement.setAttribute('data-ndsp-lang', lang);
 }

 function injectStyle(){
 document.getElementById(STYLE_ID)?.remove();

 const style = document.createElement('style');
 style.id = STYLE_ID;
 style.textContent = `
 :root{
 --ndsp-gold:#d4af37 !important;
 --ndsp-gold-hi:#f4d77d !important;
 --ndsp-line:rgba(212,175,55,.28) !important;
 --ndsp-green:#34d399 !important;
 --primary:45 65% 52% !important;
 --accent:45 82% 60% !important;
 --ring:45 82% 60% !important;
 }

 [class*="text-cyan"],
 [class*="text-sky"],
 [class*="text-blue"],
.text-primary,
.text-accent{
 color:var(--ndsp-gold-hi) !important;
 }

 [class*="border-cyan"],
 [class*="border-sky"],
 [class*="border-blue"],
.border-primary,
.border-accent{
 border-color:rgba(212,175,55,.46) !important;
 }

 [class*="bg-cyan"],
 [class*="bg-sky"],
 [class*="bg-blue"],
.bg-primary,
.bg-accent{
 background:linear-gradient(135deg,var(--ndsp-gold-hi),var(--ndsp-gold)) !important;
 background-color:var(--ndsp-gold) !important;
 color:#080705 !important;
 }

 [class*="text-green"],
 [class*="text-emerald"]{
 color:var(--ndsp-green) !important;
 }

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

.ndsp-lang-integrated-slot{
 display:flex;
 align-items:center;
 justify-content:flex-start;
 gap:10px;
 margin:0;
 padding:0;
 flex:0 0 auto;
 }

.topbar.ndsp-lang-integrated-slot{
 margin-inline-start:10px;
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
 const target = btn.getAttribute('data-lang');
 if (target === lang) btn.classList.add('active');

 btn.addEventListener('click', () => {
 localStorage.setItem(STORE_KEY, target);
 location.reload();
 });
 });

 return box;
 }

 function findTopArea(){
 const direct = document.querySelector('.topbar, header, [class*="Topbar"], [class*="topbar"]');
 if (direct) return direct;

 const candidates = Array.from(document.querySelectorAll('div,section,header'));
 let best = null;
 let bestArea = Infinity;

 for (const el of candidates) {
 const txt = (el.innerText || '').replace(/\s+/g,' ').trim();
 if (!txt) continue;

 const hasSession = txt.includes('SESSION') || txt.includes('جلسة');
 const hasMarket = txt.includes('MARKETS') || txt.includes('الأسواق');
 if (!hasSession && !hasMarket) continue;

 const r = el.getBoundingClientRect();
 if (!r.width || !r.height) continue;

 const area = r.width * r.height;
 if (area < bestArea) {
 best = el;
 bestArea = area;
 }
 }

 return best;
 }

 function placeButton(lang){
 document.getElementById(BUTTON_ID)?.remove();
 document.querySelectorAll('.ndsp-lang-integrated-slot').forEach(x => x.remove());

 const slot = document.createElement('div');
 slot.className = 'ndsp-lang-integrated-slot';
 slot.appendChild(buildButton(lang));

 const topArea = findTopArea();
 if (topArea) {
 topArea.appendChild(slot);
 return;
 }

 const main = document.querySelector('main');
 if (main) {
 main.insertBefore(slot, main.firstChild);
 return;
 }

 document.body.insertBefore(slot, document.body.firstChild);
 }

 function boot(){
 const lang = selectedLang();

 injectStyle();
 applyText(lang);
 placeButton(lang);

 let timer = null;
 const obs = new MutationObserver(() => {
 clearTimeout(timer);
 timer = setTimeout(() => {
 injectStyle();
 applyText(selectedLang());
 placeButton(selectedLang());
 }, 200);
 });

 obs.observe(document.documentElement, {
 childList:true,
 subtree:true
 });

 setTimeout(() => {
 applyText(selectedLang());
 placeButton(selectedLang());
 }, 600);
 }

 if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', boot);
 } else {
 boot();
 }
})();
