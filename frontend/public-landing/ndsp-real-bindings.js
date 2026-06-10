(function(){
  "use strict";

  var API_BASES = ["/api", "https://api.ndsp.app/api"];

  function $(id){ return document.getElementById(id); }

  function setText(el, text){
    if(!el) return;
    el.textContent = text;
  }

  async function postFirst(paths, payload){
    var lastErr = null;
    for(var i=0;i<API_BASES.length;i++){
      for(var j=0;j<paths.length;j++){
        var url = API_BASES[i] + paths[j];
        try{
          var r = await fetch(url, {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(payload),
            credentials:"same-origin"
          });
          var txt = await r.text();
          var data = {};
          try{ data = JSON.parse(txt); }catch(e){ data = {raw:txt}; }
          if(r.ok) return {ok:true, status:r.status, url:url, data:data};
          lastErr = {ok:false, status:r.status, url:url, data:data};
        }catch(e){
          lastErr = {ok:false, status:0, url:url, error:String(e && e.message ? e.message : e)};
        }
      }
    }
    return lastErr || {ok:false,error:"NO_API_ATTEMPT"};
  }

  function detectRegisterPath(type, invite){
    var t = String(type || "").toLowerCase();
    if(invite && String(invite).trim()) return ["/trial/register/private-invite"];
    if(t.indexOf("professional") >= 0 || t.indexOf("specialist") >= 0 || t.indexOf("academic") >= 0 || t.indexOf("متخصص") >= 0 || t.indexOf("أكاديمي") >= 0) {
      return ["/trial/register/professional"];
    }
    if(t.indexOf("private") >= 0 || t.indexOf("premium") >= 0 || t.indexOf("خاص") >= 0 || t.indexOf("مميز") >= 0) {
      return ["/trial/register/private-invite"];
    }
    return ["/trial/register/ordinary"];
  }

  function statusBox(){
    var box = document.getElementById("ndspRegisterStatus");
    if(!box){
      box = document.createElement("div");
      box.id = "ndspRegisterStatus";
      box.style.cssText = "margin-top:12px;padding:12px;border:1px solid rgba(247,212,106,.28);border-radius:14px;color:#f8fafc;background:rgba(2,6,23,.45);font-size:13px;line-height:1.7";
      var anchor = $("f_ack") || $("discAgree") || $("f_email");
      if(anchor && anchor.closest){
        var parent = anchor.closest("form") || anchor.parentElement;
        if(parent) parent.appendChild(box);
      } else {
        document.body.appendChild(box);
      }
    }
    return box;
  }

  function bindRegistration(){
    var name = $("f_name");
    var phone = $("f_phone");
    var email = $("f_email");
    var type = $("f_type");
    var invite = $("f_invite");
    var ack = $("f_ack");
    var disc = $("discAgree");

    if(!email || !phone) return;

    var form = email.closest("form") || phone.closest("form");
    var buttons = Array.prototype.slice.call(document.querySelectorAll("button,input[type='submit']"));

    async function submit(ev){
      if(ev) ev.preventDefault();

      var box = statusBox();
      var payload = {
        name: name ? name.value.trim() : "",
        full_name: name ? name.value.trim() : "",
        phone: phone ? phone.value.trim() : "",
        email: email ? email.value.trim() : "",
        segment: type ? type.value : "ordinary",
        type: type ? type.value : "ordinary",
        invite_code: invite ? invite.value.trim() : "",
        source: "ndsp.app",
        accepted_terms: !!(ack && ack.checked),
        accepted_disclaimer: !!(disc && disc.checked)
      };

      if(!payload.name || !payload.phone || !payload.email){
        setText(box, "يرجى تعبئة الاسم والجوال والبريد الإلكتروني.");
        return;
      }

      if(ack && !ack.checked){
        setText(box, "يجب الموافقة على الإقرار قبل إرسال الطلب.");
        return;
      }

      if(disc && !disc.checked){
        setText(box, "يجب الموافقة على إخلاء المسؤولية قبل إرسال الطلب.");
        return;
      }

      setText(box, "جاري إرسال الطلب عبر واجهة التسجيل الحقيقية...");
      var paths = detectRegisterPath(payload.type, payload.invite_code);
      var res = await postFirst(paths, payload);

      window.NDSP_REAL_REGISTER_LAST_RESULT = res;

      if(res && res.ok){
        setText(box, "تم استلام طلبك بنجاح. سيتم إشعارك حسب آلية القبول والتجربة.");
      }else{
        var msg = "تعذر إرسال الطلب. تحقق من البيانات أو حاول لاحقًا.";
        if(res && res.data && (res.data.message || res.data.error || res.data.detail)){
          msg += " — " + (res.data.message || res.data.error || res.data.detail);
        }
        setText(box, msg);
      }
    }

    if(form){
      form.addEventListener("submit", submit);
    }

    buttons.forEach(function(btn){
      var txt = (btn.textContent || btn.value || "").trim();
      if(/احجز|إرسال|ارسل|تسجيل|انضم|Submit|Register|Book/i.test(txt)){
        btn.addEventListener("click", submit);
      }
    });

    window.NDSP_REAL_BINDINGS = window.NDSP_REAL_BINDINGS || {};
    window.NDSP_REAL_BINDINGS.registration = true;
  }

  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", bindRegistration);
  } else {
    bindRegistration();
  }
})();
