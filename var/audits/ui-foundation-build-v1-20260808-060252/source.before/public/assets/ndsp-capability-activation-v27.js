(function(){
  "use strict";
  var VERSION="27";
  var API="/__ndsp/governance-44-v26";
  var timer=null;
  var inFlight=false;
  function esc(value){return String(value==null?"":value).replace(/[&<>"']/g,function(ch){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch];});}
  function language(){return String(document.documentElement.getAttribute("lang")||"").toLowerCase().indexOf("en")===0?"en":"ar";}
  function labels(){return language()==="en"?{
    live:"Live verified",partial:"Partially live",ready:"Ready verified",probes:"Functional probes",
    binding:"Runtime binding",probe:"Functional probe",blockers:"Remaining blockers",checked:"Evidence checked",
    private:"Governed privacy",privateText:"This layer participates in the governed core. Equations and raw evidence remain private."
  }:{
    live:"تشغيل حي موثق",partial:"تشغيل جزئي",ready:"جاهزة وظيفيًا",probes:"اختبارات وظيفية",
    binding:"الربط التشغيلي",probe:"الاختبار الوظيفي",blockers:"العوائق المتبقية",checked:"وقت فحص الدليل",
    private:"خصوصية حوكمية",privateText:"هذه الطبقة مشاركة في القلب الحاكم، بينما تبقى المعادلات والأدلة الخام خاصة."
  };}
  function query(){var params=new URLSearchParams(location.search);return API+"?symbol="+encodeURIComponent(params.get("symbol")||"ETHUSDT")+"&timeframe="+encodeURIComponent(params.get("timeframe")||"weekly")+"&_ndsp_v27="+Date.now();}
  function insertSummary(root,summary){
    var old=root.querySelector("[data-ndsp-v27-runtime-summary]"); if(old) old.remove();
    var t=labels(); var box=document.createElement("section"); box.className="ndsp27-runtime-summary"; box.setAttribute("data-ndsp-v27-runtime-summary","1");
    box.innerHTML="<div><strong>"+esc(summary.capability_live_verified||0)+"</strong><span>"+esc(t.live)+"</span></div>"+
      "<div><strong>"+esc(summary.capability_partial_live||0)+"</strong><span>"+esc(t.partial)+"</span></div>"+
      "<div><strong>"+esc(summary.capability_ready_verified||0)+"</strong><span>"+esc(t.ready)+"</span></div>"+
      "<div><strong>"+esc(summary.capability_probe_verified||0)+"/28</strong><span>"+esc(t.probes)+"</span></div>";
    var anchor=root.querySelector(".ndsp44-summary"); if(anchor&&anchor.parentNode) anchor.parentNode.insertBefore(box,anchor.nextSibling); else root.insertBefore(box,root.firstChild);
  }
  function decorateCapabilities(root,data){
    var t=labels(); var map={}; (data.platform_capabilities||[]).forEach(function(item){map[item.id]=item;});
    root.querySelectorAll("[data-ndsp-capability-card]").forEach(function(card){
      var item=map[card.getAttribute("data-ndsp-capability-card")]; if(!item) return;
      var existing=card.querySelector(".ndsp27-evidence"); if(existing) existing.remove();
      card.classList.add("ndsp27-state-"+String(item.runtime_state||"").toLowerCase());
      card.setAttribute("data-ndsp-v27-evidence","1"); card.setAttribute("data-ndsp-v27-state",item.runtime_state||"");
      var blockers=(item.activation_blockers||[]).join(language()==="en"?"; ":"؛ ")||"—";
      var div=document.createElement("div"); div.className="ndsp27-evidence";
      div.innerHTML="<div><b>"+esc(t.binding)+":</b> "+esc(item.runtime_binding||"—")+"</div>"+
        "<div><b>"+esc(t.probe)+":</b> "+esc(item.functional_probe_status||"—")+" — "+esc(item.functional_probe_detail||"")+"</div>"+
        "<div><b>"+esc(t.blockers)+":</b> "+esc(blockers)+"</div>"+
        "<div><b>"+esc(t.checked)+":</b> "+esc(item.evidence_checked_at||"—")+"</div>";
      card.appendChild(div);
    });
  }
  function decorateLayers(root,data){
    var t=labels(); var map={}; (data.decision_layers||[]).forEach(function(item){map[item.id]=item;});
    root.querySelectorAll("[data-ndsp-layer-card]").forEach(function(card){
      var item=map[card.getAttribute("data-ndsp-layer-card")]; if(!item) return;
      var existing=card.querySelector(".ndsp27-redacted"); if(existing) existing.remove();
      card.removeAttribute("data-ndsp-v27-redacted");
      if(item.state!=="GOVERNED_REDACTED") return;
      card.setAttribute("data-ndsp-v27-redacted","1");
      var div=document.createElement("div"); div.className="ndsp27-redacted";
      div.innerHTML="<b>"+esc(t.private)+":</b> "+esc(t.privateText)+"<br><span>"+esc(item.evidence||"")+"</span>";
      card.appendChild(div);
    });
  }
  async function render(){
    var route=location.pathname; if(route!=="/decisions"&&route!=="/governance") return;
    var root=document.getElementById("ndsp-governance-44-v26"); if(!root||inFlight) return;
    inFlight=true;
    try{
      var response=await fetch(query(),{cache:"no-store",credentials:"same-origin"}); if(!response.ok) throw new Error("HTTP_"+response.status);
      var data=await response.json();
      var signature=[route,language(),data.governance_projection_version||"",(data.governance_summary||{}).evidence_checked_at||""].join("|");
      var expectedReady=route==="/governance"?root.querySelectorAll('[data-ndsp-v27-evidence="1"]').length===28:root.querySelectorAll('[data-ndsp-v27-redacted="1"]').length===(data.governance_summary||{}).layer_governed_redacted;
      if(root.getAttribute("data-ndsp-v27-signature")===signature&&expectedReady)return;
      insertSummary(root,data.governance_summary||{});
      if(route==="/governance") decorateCapabilities(root,data); else decorateLayers(root,data);
      root.setAttribute("data-ndsp-v27","active"); root.setAttribute("data-ndsp-v27-contract",data.governance_projection_version||""); root.setAttribute("data-ndsp-v27-signature",signature);
    }catch(error){console.error("NDSP_V27_DECORATION_ERROR",error);}finally{inFlight=false;}
  }
  function schedule(){clearTimeout(timer);timer=setTimeout(render,120);}
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",schedule,{once:true}); else schedule();
  window.addEventListener("pageshow",schedule); window.addEventListener("popstate",schedule);
  new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:["lang","dir"]});
  window.NDSP_CAPABILITY_ACTIVATION_V27={version:VERSION,render:render};
})();
