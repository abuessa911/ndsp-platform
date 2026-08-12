(function(){
  "use strict";

  if(window.__NDSP_REGISTRATION_SUBMIT_BRIDGE_V152__){
    return;
  }

  window.__NDSP_REGISTRATION_SUBMIT_BRIDGE_V152__=true;

  var endpoint='/api/register';
  var schema='canonical';

  function normalize(value){
    return String(value||"").toLowerCase().replace(/\s+/g," ").trim();
  }

  function descriptor(element){
    return normalize([
      element.tagName,
      element.type,
      element.name,
      element.id,
      element.placeholder,
      element.getAttribute("aria-label"),
      element.autocomplete
    ].join(" "));
  }

  function visible(element){
    var style=window.getComputedStyle(element);

    return style.display!=="none"&&
      style.visibility!=="hidden"&&
      !element.disabled;
  }

  function scoreForm(form){
    var score=0;
    var text=normalize(form.innerText||"");

    Array.prototype.forEach.call(
      form.querySelectorAll("input,select,textarea"),
      function(element){
        if(!visible(element)){
          return;
        }

        var value=descriptor(element);

        if(/\bemail\b|البريد/.test(value)){
          score+=5;
        }

        if(/password|كلمة المرور/.test(value)){
          score+=4;
        }

        if(/phone|mobile|tel|جوال|هاتف/.test(value)){
          score+=4;
        }

        if(/full.?name|\bname\b|الاسم/.test(value)&&
           !/username|user.?name/.test(value)){
          score+=3;
        }

        if(String(element.type||"").toLowerCase()==="checkbox"){
          score+=1;
        }
      }
    );

    if(/register|sign up|create account|تسجيل مستخدم جديد|إنشاء حساب|تأكيد كلمة المرور/.test(text)){
      score+=10;
    }

    if(/login|sign in|تسجيل الدخول|نسيت كلمة المرور/.test(text)){
      score-=4;
    }

    return score;
  }

  function findRegistrationForm(){
    var forms=Array.prototype.filter.call(
      document.querySelectorAll("form"),
      visible
    );

    forms.sort(function(left,right){
      return scoreForm(right)-scoreForm(left);
    });

    return forms.length&&scoreForm(forms[0])>=12?forms[0]:null;
  }

  function findValue(form,pattern,type){
    var controls=form.querySelectorAll("input,select,textarea");

    for(var index=0;index<controls.length;index+=1){
      var element=controls[index];

      if(!visible(element)){
        continue;
      }

      if(type&&normalize(element.type)!==type){
        continue;
      }

      if(pattern.test(descriptor(element))){
        return String(element.value||"").trim();
      }
    }

    return "";
  }

  function checkedConsent(form){
    var boxes=form.querySelectorAll('input[type="checkbox"]');

    for(var index=0;index<boxes.length;index+=1){
      if(visible(boxes[index])&&!boxes[index].checked){
        return false;
      }
    }

    return true;
  }

  function messageNode(form){
    var existing=form.querySelector("[data-ndsp-register-message-v152]");

    if(existing){
      return existing;
    }

    var node=document.createElement("div");
    node.setAttribute("data-ndsp-register-message-v152","");
    node.setAttribute("role","status");
    node.setAttribute("aria-live","polite");
    node.style.marginTop="14px";
    node.style.padding="12px 14px";
    node.style.borderRadius="12px";
    node.style.border="1px solid rgba(212,175,55,.35)";
    node.style.background="rgba(212,175,55,.08)";
    node.style.lineHeight="1.8";
    node.style.display="none";
    form.appendChild(node);
    return node;
  }

  function setMessage(form,text,kind){
    var node=messageNode(form);
    node.textContent=text;
    node.style.display="block";

    if(kind==="success"){
      node.style.borderColor="rgba(41,180,110,.55)";
      node.style.background="rgba(41,180,110,.10)";
    }else if(kind==="error"){
      node.style.borderColor="rgba(220,75,75,.55)";
      node.style.background="rgba(220,75,75,.10)";
    }
  }

  function setBusy(form,busy){
    Array.prototype.forEach.call(
      form.querySelectorAll('button[type="submit"],input[type="submit"]'),
      function(button){
        button.disabled=busy;
        button.setAttribute("aria-busy",busy?"true":"false");
      }
    );
  }

  function buildPayload(form){
    var email=findValue(form,/\bemail\b|البريد/,"email")||
      findValue(form,/\bemail\b|البريد/);

    var phone=findValue(form,/phone|mobile|tel|جوال|هاتف/);

    var name=findValue(
      form,
      /full.?name|\bname\b|الاسم/
    );

    var passwordFields=Array.prototype.filter.call(
      form.querySelectorAll('input[type="password"]'),
      visible
    );

    var password=passwordFields.length?
      String(passwordFields[0].value||""):"";

    var confirmPassword=passwordFields.length>1?
      String(passwordFields[1].value||""):password;

    var accepted=checkedConsent(form);

    if(schema==="minimal"){
      return {
        email:email,
        phone:phone,
        name:name,
        password:password,
        confirm_password:confirmPassword
      };
    }

    if(schema==="auth"){
      return {
        email:email,
        username:email,
        name:name,
        display_name:name,
        phone:phone,
        password:password,
        confirm_password:confirmPassword,
        password_confirmation:confirmPassword,
        terms_accepted:accepted,
        disclaimer_accepted:accepted,
        consent:accepted
      };
    }

    return {
      name:name,
      full_name:name,
      email:email,
      phone:phone,
      mobile:phone,
      password:password,
      confirm_password:confirmPassword,
      password_confirmation:confirmPassword,
      segment:"ordinary",
      requested_segment:"ordinary",
      user_type:"ordinary",
      type:"ordinary",
      terms_accepted:accepted,
      disclaimer_accepted:accepted,
      consent:accepted,
      source:"ndsp_public_register_v152",
      page:"register",
      invite_code:""
    };
  }

  function extractMessage(data,fallback){
    if(!data||typeof data!=="object"){
      return fallback;
    }

    return data.message||
      data.detail||
      data.error||
      data.reason||
      fallback;
  }

  async function submitRegistration(event){
    event.preventDefault();
    event.stopPropagation();

    if(event.stopImmediatePropagation){
      event.stopImmediatePropagation();
    }

    var form=event.target&&event.target.tagName==="FORM"?
      event.target:event.currentTarget;

    if(!form.checkValidity()){
      form.reportValidity();
      return;
    }

    var payload=buildPayload(form);

    if(!payload.email||!payload.password){
      setMessage(
        form,
        document.documentElement.lang==="en"?
          "Complete the required registration fields.":
          "أكمل حقول التسجيل المطلوبة.",
        "error"
      );
      return;
    }

    if(payload.confirm_password&&
       payload.password!==payload.confirm_password){
      setMessage(
        form,
        document.documentElement.lang==="en"?
          "The password confirmation does not match.":
          "تأكيد كلمة المرور غير مطابق.",
        "error"
      );
      return;
    }

    setBusy(form,true);
    setMessage(
      form,
      document.documentElement.lang==="en"?
        "Submitting your registration request.":
        "جارٍ إرسال طلب التسجيل.",
      "pending"
    );

    try{
      var response=await fetch(endpoint,{
        method:"POST",
        credentials:"same-origin",
        headers:{
          "Content-Type":"application/json",
          "Accept":"application/json"
        },
        body:JSON.stringify(payload)
      });

      var raw=await response.text();
      var data={};

      try{
        data=raw?JSON.parse(raw):{};
      }catch(ignore){
        data={message:raw};
      }

      if(response.ok){
        setMessage(
          form,
          document.documentElement.lang==="en"?
            "Registration received. Check your email or wait for account approval. The 16-day trial starts only when the account is activated.":
            "تم استلام التسجيل. تحقق من بريدك أو انتظر اعتماد الحساب. تبدأ تجربة 16 يوم فقط عند تفعيل الحساب.",
          "success"
        );

        form.setAttribute("data-ndsp-registration-complete-v152","true");
        return;
      }

      if(response.status===409){
        setMessage(
          form,
          document.documentElement.lang==="en"?
            "This email or phone is already registered. Use sign in or password recovery.":
            "البريد أو رقم الجوال مسجل مسبقًا. استخدم تسجيل الدخول أو استعادة كلمة المرور.",
          "error"
        );
        return;
      }

      setMessage(
        form,
        String(
          extractMessage(
            data,
            document.documentElement.lang==="en"?
              "Registration could not be completed.":
              "تعذر إكمال التسجيل."
          )
        ),
        "error"
      );
    }catch(error){
      setMessage(
        form,
        document.documentElement.lang==="en"?
          "The registration service is temporarily unavailable.":
          "خدمة التسجيل غير متاحة مؤقتًا.",
        "error"
      );
    }finally{
      setBusy(form,false);
    }
  }

  function bind(){
    var form=findRegistrationForm();

    if(!form||form.dataset.ndspRegisterBoundV152==="true"){
      return;
    }

    form.dataset.ndspRegisterBoundV152="true";
    form.onsubmit=null;
    form.method="post";
    form.action=endpoint;
    form.noValidate=false;
    form.addEventListener("submit",submitRegistration,true);

    form.addEventListener("click",function(event){
      var target=event.target&&event.target.closest?
        event.target.closest('button[type="submit"],input[type="submit"]'):null;

      if(!target||target.form!==form){
        return;
      }

      event.preventDefault();
      event.stopPropagation();

      if(event.stopImmediatePropagation){
        event.stopImmediatePropagation();
      }

      if(typeof form.requestSubmit==="function"){
        form.requestSubmit();
      }else{
        form.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}));
      }
    },true);
  }

  if(document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded",bind,{once:true});
  }else{
    bind();
  }

  var observer=new MutationObserver(bind);
  observer.observe(document.documentElement,{
    childList:true,
    subtree:true,
    attributes:true,
    attributeFilter:["class","style","hidden"]
  });
})();
