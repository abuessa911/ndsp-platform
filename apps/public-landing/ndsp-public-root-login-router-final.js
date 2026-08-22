(function(){
  function goLogin(e){
    var el=e.target&&e.target.closest?e.target.closest("a,button"):null;
    if(!el)return;
    var txt=(el.innerText||el.textContent||"").trim();
    var href=el.getAttribute?(el.getAttribute("href")||""):"";
    if(txt.indexOf("الدخول إلى المنصة")!==-1||txt.indexOf("تسجيل الدخول")!==-1||href==="/"||href==="/index.html"||href==="https://my.ndsp.app"||href==="https://my.ndsp.app/"){
      e.preventDefault();
      window.location.href="https://my.ndsp.app/login/";
    }
  }
  document.addEventListener("click",goLogin,true);
})();
