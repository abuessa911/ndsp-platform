(function(){
  'use strict';
  if(window.__NDSP_LOGIN_TO_PORTAL_V90__) return;
  window.__NDSP_LOGIN_TO_PORTAL_V90__=true;

  var API='/api/auth/login';
  var SESSION='/api/auth/session';
  var PORTAL='/portal-v50/?ndsp_source=login-success-v90&ts=';
  var nativeFetch=window.fetch.bind(window);
  var busy=false;

  function q(sel,root){ return (root||document).querySelector(sel); }

  function emailInput(){
    return q('input[type="email"]') ||
           q('input[name="email" i]') ||
           q('input[autocomplete="username"]') ||
           q('input[name*="email" i]') ||
           q('input[name*="user" i]');
  }

  function passwordInput(){
    return q('input[type="password"]') ||
           q('input[name="password" i]') ||
           q('input[name*="pass" i]');
  }

  function isLoginButton(el){
    if(!el) return false;
    var b=el.closest('button,[role="button"],input[type="submit"]');
    if(!b) return false;
    var text=((b.innerText||b.value||'')+' '+(b.getAttribute('aria-label')||'')).trim().toLowerCase();
    return /login|sign in|secure access|دخول|تسجيل الدخول/.test(text);
  }

  function setBusy(on){
    busy=on;
    document.querySelectorAll('button[type="submit"],input[type="submit"]').forEach(function(b){
      try{ b.disabled=on; }catch(e){}
    });
  }

  function messageBox(){
    var box=document.getElementById('ndsp-v90-login-message');
    if(box) return box;
    box=document.createElement('div');
    box.id='ndsp-v90-login-message';
    box.setAttribute('role','alert');
    box.style.cssText='margin:12px 0;padding:10px 12px;border:1px solid rgba(214,68,68,.65);border-radius:10px;background:rgba(90,16,16,.28);color:#ffd7d7;font:600 13px/1.7 system-ui;text-align:center;';
    var p=passwordInput();
    var host=(p&&p.closest('form'))||document.body;
    if(host&&host.appendChild) host.appendChild(box);
    return box;
  }

  function showError(text){
    var box=messageBox();
    box.textContent=text||'Login failed. Please verify the email and password.';
    box.style.display='block';
  }

  function hideError(){
    var box=document.getElementById('ndsp-v90-login-message');
    if(box) box.style.display='none';
  }

  function successPayload(data,status){
    if(status<200||status>=300) return false;
    if(!data) return true;
    if(data.ok===false||data.success===false||data.error) return false;
    return true;
  }

  async function sessionReady(){
    for(var i=0;i<20;i++){
      try{
        var r=await nativeFetch(SESSION+'?v=90&ts='+Date.now(),{
          credentials:'include',
          cache:'no-store',
          headers:{Accept:'application/json'}
        });
        if(r.ok){
          var d=await r.json().catch(function(){return {};});
          if(d&&(d.ok===true||d.authenticated===true||d.user||d.email||d.session)) return true;
        }
      }catch(e){}
      await new Promise(function(resolve){setTimeout(resolve,100);});
    }
    return false;
  }

  function clearOldClientState(){
    try{
      sessionStorage.removeItem('ndsp_redirect_after_login');
      localStorage.removeItem('ndsp_redirect_after_login');
      sessionStorage.setItem('ndsp_v90_login_target','/portal-v50/');
    }catch(e){}
    try{
      if('serviceWorker' in navigator){
        navigator.serviceWorker.getRegistrations().then(function(rs){
          rs.forEach(function(r){try{r.unregister();}catch(e){}});
        }).catch(function(){});
      }
      if(window.caches&&caches.keys){
        caches.keys().then(function(keys){
          keys.forEach(function(k){caches.delete(k).catch(function(){});});
        }).catch(function(){});
      }
    }catch(e){}
  }

  function goPortal(){
    clearOldClientState();
    location.replace(PORTAL+Date.now());
  }

  async function performLogin(event){
    if(event){
      try{event.preventDefault();}catch(e){}
      try{event.stopPropagation();}catch(e){}
      try{event.stopImmediatePropagation();}catch(e){}
    }
    if(busy) return;

    var e=emailInput();
    var p=passwordInput();
    var email=e&&String(e.value||'').trim();
    var password=p&&String(p.value||'');

    if(!email||!password){
      showError('Enter the email and password.');
      return;
    }

    hideError();
    setBusy(true);

    try{
      var r=await nativeFetch(API,{
        method:'POST',
        credentials:'include',
        cache:'no-store',
        headers:{
          'Content-Type':'application/json',
          'Accept':'application/json',
          'X-NDSP-Login-Target':'/portal-v50/'
        },
        body:JSON.stringify({email:email,password:password})
      });

      var data=await r.clone().json().catch(function(){return null;});
      if(!successPayload(data,r.status)){
        var msg=(data&&(data.message||data.detail||data.error))||'Login failed. Please verify the email and password.';
        showError(typeof msg==='string'?msg:'Login failed. Please verify the email and password.');
        setBusy(false);
        return;
      }

      await sessionReady();
      goPortal();
    }catch(err){
      showError('Login request failed. Please try again.');
      setBusy(false);
    }
  }

  function installCapture(){
    document.addEventListener('submit',function(ev){
      var form=ev.target;
      if(!form||!passwordInput()) return;
      performLogin(ev);
    },true);

    document.addEventListener('click',function(ev){
      if(isLoginButton(ev.target)&&emailInput()&&passwordInput()){
        performLogin(ev);
      }
    },true);

    document.addEventListener('keydown',function(ev){
      if(ev.key==='Enter'&&emailInput()&&passwordInput()){
        var active=document.activeElement;
        if(active&&(active===emailInput()||active===passwordInput())){
          performLogin(ev);
        }
      }
    },true);
  }

  async function redirectExistingSession(){
    try{
      var r=await nativeFetch(SESSION+'?v=90&ts='+Date.now(),{
        credentials:'include',
        cache:'no-store',
        headers:{Accept:'application/json'}
      });
      if(!r.ok) return;
      var d=await r.json().catch(function(){return {};});
      if(d&&(d.ok===true||d.authenticated===true||d.user||d.email||d.session)) goPortal();
    }catch(e){}
  }

  clearOldClientState();
  installCapture();
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',redirectExistingSession,{once:true});
  }else{
    redirectExistingSession();
  }
})();
