(function () {
  'use strict';
  if (window.__NDSP_ROUTE_V86__) return;
  window.__NDSP_ROUTE_V86__ = true;
  var CANONICAL='/portal-v50/';
  var LOGIN='/login/';
  var LEGACY=['/decision-room-v30/','/decision-room-v30-1/','/decision-room-v31/','/decision-room-v31/account/'];
  function path(){var p=window.location.pathname||'/';if(p.indexOf('.')===-1&&!p.endsWith('/'))p+='/';return p;}
  function isLegacy(){var p=path();return LEGACY.some(function(x){return p.indexOf(x)===0;});}
  function go(target,source){var j=target.indexOf('?')===-1?'?':'&';window.location.replace(target+j+'ndsp_source='+encodeURIComponent(source)+'&ts='+Date.now());}
  async function session(){try{var r=await fetch('/api/auth/session',{credentials:'include',cache:'no-store',headers:{Accept:'application/json'}});if(!r.ok)return false;var d=await r.json().catch(function(){return {};});return !!(d&&(d.ok===true||d.authenticated===true||d.user||d.email||d.session));}catch(_){return false;}}
  async function enforce(){var p=path();if(p===CANONICAL)return;var ok=await session();if(p===LOGIN){if(ok)go(CANONICAL,'authenticated-login');return;}if(isLegacy()){if(ok)go(CANONICAL,'authenticated-legacy-route');else go(LOGIN+'?next='+encodeURIComponent(CANONICAL),'unauthenticated-legacy-route');}}
  function start(){enforce();var n=0;var t=setInterval(function(){n+=1;enforce();if(n>=120||path()===CANONICAL)clearInterval(t);},500);window.addEventListener('focus',enforce);document.addEventListener('visibilitychange',function(){if(!document.hidden)enforce();});}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
