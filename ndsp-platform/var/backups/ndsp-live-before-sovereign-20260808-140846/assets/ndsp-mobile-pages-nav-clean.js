(function(){
 'use strict';

 const BUTTON_ID = 'ndsp-mobile-pages-button';
 const DRAWER_ID = 'ndsp-mobile-pages-drawer';
 const BACKDROP_ID = 'ndsp-mobile-pages-backdrop';
 const SLOT_ID = 'ndsp-mobile-pages-inline-slot';

 const portalPages = [
 ['/', 'النظرة التنفيذية', 'Executive Overview'],
 ['/markets', 'مراقبة الأسواق', 'Markets Monitor'],
 ['/phase', 'محرك المراحل', 'Phase Engine'],
 ['/intelligence', 'محرك الذكاء', 'Intelligence Engine'],
 ['/decisions', 'محرك القرار', 'Decision Engine'],
 ['/governance', 'الحوكمة والمخاطر', 'Governance & Risk'],
 ['/data-infra', 'بنية البيانات', 'Data Infrastructure'],
 ['/strategy-lab', 'مختبر الاستراتيجية', 'Strategy Lab'],
 ['/architecture', 'المعمارية', 'Architecture']
 ];

 const authPages = [
 ['https://my.ndsp.app/', 'الصفحة الرئيسية', 'Home'],
 ['https://ndsp.app/login/', 'تسجيل الدخول', 'Login'],
 ['https://ndsp.app/register.html', 'تسجيل مستخدم جديد', 'Create new user'],
 ['https://ndsp.app/admin/', 'مدير النظام', 'System admin'],
 ['https://ndsp.app/owner/', 'مالك النظام', 'System owner']
 ];

 const routeAliases = {
 '/data': '/data-infra',
 '/data-infrastructure': '/data-infra'
 };

 function currentLang(){
 const htmlLang = document.documentElement.getAttribute('lang');
 const stored = localStorage.getItem('ndsp_lang_final') || localStorage.getItem('ndsp_final_lang') || localStorage.getItem('ndsp_lang');
 if (stored === 'en' || htmlLang === 'en') return 'en';
 return 'ar';
 }

 function text(ar, en){
 return currentLang() === 'en' ? en : ar;
 }

 function normalizePath(path){
 try {
 const u = new URL(path, location.origin);
 let p = u.pathname.replace(/\/+$/, '') || '/';
 return routeAliases[p] || p;
 } catch(e) {
 return '/';
 }
 }

 function isSameRoute(a,b){
 try {
 const ua = new URL(a, location.origin);
 const ub = new URL(b, location.origin);
 return normalizePath(ua.pathname) === normalizePath(ub.pathname) && ua.hostname === ub.hostname;
 } catch(e) {
 return normalizePath(a) === normalizePath(b);
 }
 }

 function isAuthStaticPage(){
 const p = normalizePath(location.pathname);
 return (
 location.hostname === 'ndsp.app' &&
 (
 p === '/login' ||
 p === '/register.html' ||
 p === '/register' ||
 p === '/admin' ||
 p === '/owner'
 )
 );
 }

 function fallbackPages(){
 return isAuthStaticPage() ? authPages : portalPages;
 }

 function collectPages(){
 const found = [];
 const seen = new Set();

 document.querySelectorAll('aside a[href], nav a[href]').forEach((a) => {
 if (a.closest('#' + DRAWER_ID)) return;

 const href = a.getAttribute('href');
 if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

 const route = normalizePath(href);
 if (seen.has(route)) return;

 const label = (a.innerText || a.textContent || '').replace(/\s+/g,' ').trim();
 if (!label) return;

 seen.add(route);
 found.push([route, label, label]);
 });

 if (!isAuthStaticPage() && found.length >= 4) return found;
 return fallbackPages();
 }

 function closeDrawer(){
 document.documentElement.classList.remove('ndsp-mobile-pages-open');
 }

 function openDrawer(){
 document.documentElement.classList.add('ndsp-mobile-pages-open');
 }

 function clickOriginalRoute(route){
 const wanted = normalizePath(route);
 const links = Array.from(document.querySelectorAll('aside a[href], nav a[href]'));

 const match = links.find((a) => {
 if (a.closest('#' + DRAWER_ID)) return false;
 return normalizePath(a.getAttribute('href')) === wanted;
 });

 if (match) {
 match.click();
 return true;
 }

 return false;
 }

 function navigateInsideApp(route){
 const cleanRoute = normalizePath(route);

 closeDrawer();

 if (isAuthStaticPage()) {
 window.location.href = route;
 return;
 }

 if (clickOriginalRoute(cleanRoute)) return;

 if (location.pathname !== cleanRoute) {
 history.pushState({}, '', cleanRoute);
 window.dispatchEvent(new PopStateEvent('popstate', { state: history.state }));
 window.dispatchEvent(new Event('ndsp:navigation'));
 }

 window.scrollTo({ top: 0, behavior: 'smooth' });
 }

 function makeButton(){
 document.getElementById(BUTTON_ID)?.remove();

 const button = document.createElement('button');
 button.id = BUTTON_ID;
 button.type = 'button';
 button.innerHTML = '<span class="ndsp-mobile-pages-icon">☰</span><span>' + text('الصفحات','Pages') + '</span>';
 button.addEventListener('click', openDrawer);
 return button;
 }

 function ensureDrawer(){
 document.getElementById(DRAWER_ID)?.remove();
 document.getElementById(BACKDROP_ID)?.remove();

 const backdrop = document.createElement('div');
 backdrop.id = BACKDROP_ID;
 backdrop.addEventListener('click', closeDrawer);

 const drawer = document.createElement('aside');
 drawer.id = DRAWER_ID;
 drawer.setAttribute('aria-label', text('قائمة الصفحات','Pages menu'));

 const pages = collectPages();
 const currentUrl = location.href;

 const links = pages.map((p, i) => {
 const href = p[0];
 const label = currentLang() === 'en' ? p[2] : p[1];
 const active = isSameRoute(href, currentUrl) ? ' is-active' : '';
 const num = String(i + 1).padStart(2, '0');

 return '<a class="ndsp-mobile-pages-link' + active + '" href="' + href + '" data-ndsp-route="' + href + '">' +
 '<span>' + label + '</span>' +
 '<span class="ndsp-mobile-pages-index">' + num + '</span>' +
 '</a>';
 }).join('');

 drawer.innerHTML =
 '<div class="ndsp-mobile-pages-head">' +
 '<div class="ndsp-mobile-pages-title">' +
 '<strong>NDSP</strong>' +
 '<span>' + text('قائمة التنقل بين الصفحات','Page navigation') + '</span>' +
 '</div>' +
 '<button type="button" class="ndsp-mobile-pages-close" aria-label="' + text('إغلاق','Close') + '">×</button>' +
 '</div>' +
 '<div class="ndsp-mobile-pages-list">' + links + '</div>';

 drawer.querySelector('.ndsp-mobile-pages-close')?.addEventListener('click', closeDrawer);

 drawer.querySelectorAll('a[data-ndsp-route]').forEach((a) => {
 a.addEventListener('click', function(e){
 e.preventDefault();
 e.stopPropagation();
 navigateInsideApp(this.getAttribute('data-ndsp-route'));
 });
 });

 document.body.appendChild(backdrop);
 document.body.appendChild(drawer);
 }

 function findLanguageSwitcher(){
 return (
 document.getElementById('ndsp-language-content-switcher') ||
 document.getElementById('ndsp-integrated-lang-switcher') ||
 document.getElementById('ndsp-my-root-lang-switcher') ||
 document.querySelector('[id*="lang"][id*="switcher"]')
 );
 }

 function placeButtonBesideLanguage(){
 document.getElementById(SLOT_ID)?.remove();

 const button = makeButton();
 const slot = document.createElement('div');
 slot.id = SLOT_ID;
 slot.className = 'ndsp-mobile-pages-inline-slot';
 slot.appendChild(button);

 const lang = findLanguageSwitcher();

 if (lang && lang.parentElement) {
 lang.insertAdjacentElement('afterend', slot);
 return;
 }

 const topArea =
 document.querySelector('.topbar, header, [class*="Topbar"], [class*="topbar"]') ||
 document.querySelector('main') ||
 document.body;

 if (topArea === document.body) {
 document.body.insertBefore(slot, document.body.firstChild);
 } else {
 topArea.insertBefore(slot, topArea.firstChild);
 }
 }

 function build(){
 ensureDrawer();
 placeButtonBesideLanguage();

 document.addEventListener('keydown', (e) => {
 if (e.key === 'Escape') closeDrawer();
 }, { once:false });
 }

 function boot(){
 build();

 let t = null;
 const obs = new MutationObserver(() => {
 clearTimeout(t);
 t = setTimeout(() => {
 if (!document.getElementById(BUTTON_ID)) placeButtonBesideLanguage();
 }, 250);
 });

 obs.observe(document.documentElement, {
 childList:true,
 subtree:true
 });
 }

 if (document.readyState === 'loading'){
 document.addEventListener('DOMContentLoaded', boot);
 } else {
 boot();
 }
})();
