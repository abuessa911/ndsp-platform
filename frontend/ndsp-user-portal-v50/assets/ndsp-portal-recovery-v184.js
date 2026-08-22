(function(){
  "use strict";

  var retryKey="ndsp_portal_v184_retry";

  function appEmpty(){
    var app=document.getElementById("app");
    return !app || (!app.children.length && !String(app.textContent||"").trim());
  }

  function showRecovery(){
    var app=document.getElementById("app");
    if(!app){ return; }

    app.innerHTML=
      '<main style="min-height:100vh;display:grid;place-items:center;padding:24px;background:#070705;color:#f5f0e5;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Tahoma,Arial,sans-serif">'+
        '<section style="width:min(620px,100%);padding:26px;border:1px solid #5d481c;border-radius:22px;background:#11100b;text-align:center">'+
          '<strong style="display:block;color:#e4bd54;margin-bottom:12px">NDSP</strong>'+
          '<h1 style="font-size:28px;margin:0 0 12px">تعذر بدء بوابة المستخدم</h1>'+
          '<p style="color:#aaa39a;line-height:1.8">تم منع الشاشة السوداء. اضغط إعادة المحاولة.</p>'+
          '<button id="ndspPortalRetryV184" style="min-height:46px;padding:10px 18px;border:0;border-radius:12px;background:#e4bd54;color:#080704;font-weight:900">إعادة المحاولة</button>'+
        '</section>'+
      '</main>';

    document.getElementById("ndspPortalRetryV184").onclick=function(){
      sessionStorage.removeItem(retryKey);
      location.replace(location.pathname+"?refresh=184&ts="+Date.now());
    };
  }

  window.setTimeout(function(){
    if(!appEmpty()){
      sessionStorage.removeItem(retryKey);
      return;
    }

    if(sessionStorage.getItem(retryKey)!=="1"){
      sessionStorage.setItem(retryKey,"1");
      var separator=location.search ? "&" : "?";
      location.replace(location.pathname+location.search+separator+"ndsp_recovery=183&ts="+Date.now());
      return;
    }

    showRecovery();
  },6500);
})();
