(function(){
 var AUTH_COOKIE = "ndsp_portal_auth_final";
 var MAX_AGE = 60 * 60 * 24 * 7;

 function setAuthCookie(){
 document.cookie = AUTH_COOKIE + "=1; Path=/; Max-Age=" + MAX_AGE + "; Secure; SameSite=Lax";
 }

 function clearCookie(name){
 document.cookie = name + "=; Path=/; Max-Age=0; Secure; SameSite=Lax";
 }

 function isLoginPage(){
 return /^\/login\/?$/.test(window.location.pathname || "");
 }

 function nextUrl(){
 try { return new URLSearchParams(window.location.search).get("next") || "/"; }
 catch(e) { return "/"; }
 }

 function looksLikeSuccess(text){
 if(!text) return false;
 try {
 var data = JSON.parse(text);
 if(data && (data.ok === true || data.success === true || data.authenticated === true)) return true;
 if(data && (data.token || data.access_token || data.accessToken || data.session || data.jwt)) return true;
 if(data && data.user && (data.user.email || data.user.id || data.user.name)) return true;
 } catch(e) {}
 return /access_token|accessToken|jwt|session_token|auth_token|"ok"\s*:\s*true|"success"\s*:\s*true|"authenticated"\s*:\s*true/i.test(text);
 }

 if(isLoginPage() && window.fetch && !window.__ndspAuthFetchWrappedFinal){
 window.__ndspAuthFetchWrappedFinal = true;
 var originalFetch = window.fetch;

 window.fetch = async function(input, init){
 var method = "GET";
 var url = "";
 try {
 method = (init && init.method) || (input && input.method) || "GET";
 url = typeof input === "string" ? input : ((input && input.url) || "");
 } catch(e) {}

 var response = await originalFetch.apply(this, arguments);

 try {
 if(response && response.ok && /POST|PUT|PATCH/i.test(method) && /login|auth|session|trial|api/i.test(url)){
 response.clone().text().then(function(text){
 if(looksLikeSuccess(text)){
 setAuthCookie();
 setTimeout(function(){
 if(isLoginPage()) window.location.replace(nextUrl());
 }, 250);
 }
 }).catch(function(){});
 }
 } catch(e) {}

 return response;
 };
 }

 document.addEventListener("click", function(e){
 var el = e.target && e.target.closest ? e.target.closest("a,button") : null;
 if(!el) return;

 var txt = (el.innerText || el.textContent || "").trim();
 var href = el.getAttribute ? (el.getAttribute("href") || "") : "";

 if(txt.indexOf("تسجيل الخروج") !== -1 || txt.toLowerCase().indexOf("logout") !== -1 || href.indexOf("/logout") !== -1){
 clearCookie(AUTH_COOKIE);
 try { window.localStorage.clear(); } catch(e) {}
 try { window.sessionStorage.clear(); } catch(e) {}
 setTimeout(function(){ window.location.href = "/login/"; }, 100);
 }
 }, true);

 window.NDSPSetPortalAuthCookieFinal = setAuthCookie;
 window.NDSPClearPortalAuthCookieFinal = function(){ clearCookie(AUTH_COOKIE); };
})();
