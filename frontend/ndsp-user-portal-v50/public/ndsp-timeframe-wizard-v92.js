(function(){
  'use strict';
  if(window.__NDSP_TIMEFRAME_WIZARD_V92__) return;
  window.__NDSP_TIMEFRAME_WIZARD_V92__=true;

  var FRAMES=[
    ['15m','15 دقيقة','15m'],
    ['1h','ساعة','1H'],
    ['4h','4 ساعات','4H'],
    ['daily','يومي','Daily'],
    ['weekly','أسبوعي','Weekly'],
    ['monthly','شهري','Monthly']
  ];

  var KEY='ndsp_user_context_v1';
  var timer=0;
  var applying=false;

  function txt(el){
    return String((el&&el.textContent)||'').replace(/\s+/g,' ').trim();
  }

  function normalize(v){
    v=String(v||'').trim().toLowerCase();
    var m={
      '15m':'15m','15min':'15m',
      '1h':'1h','60m':'1h','hourly':'1h',
      '4h':'4h','240m':'4h',
      '1d':'daily','daily':'daily','day':'daily',
      '1w':'weekly','weekly':'weekly','week':'weekly',
      '1mo':'monthly','monthly':'monthly','month':'monthly'
    };
    return m[v]||'';
  }

  function arabic(){
    return document.documentElement.dir==='rtl' ||
      String(document.documentElement.lang||'').toLowerCase().indexOf('ar')===0 ||
      /اختر الفريم|اختيار الفريم/.test(document.body?document.body.innerText:'');
  }

  function selected(){
    try{
      var q=normalize(new URL(location.href).searchParams.get('timeframe'));
      if(q) return q;
    }catch(e){}
    try{
      var raw=localStorage.getItem(KEY);
      var obj=raw?JSON.parse(raw):{};
      var s=normalize(obj.timeframe||obj.frame);
      if(s) return s;
    }catch(e){}
    return normalize(document.documentElement.getAttribute('data-ndsp-v86-selected-frame'))||'15m';
  }

  function persist(id){
    id=normalize(id)||'15m';
    try{
      var raw=localStorage.getItem(KEY);
      var obj=raw?JSON.parse(raw):{};
      obj.timeframe=id;
      if(!obj.analysis_mode&&!obj.analysisMode&&!obj.mode) obj.analysis_mode='speculative';
      localStorage.setItem(KEY,JSON.stringify(obj));
      sessionStorage.setItem(KEY,JSON.stringify(obj));
    }catch(e){}
    try{
      var u=new URL(location.href);
      u.searchParams.set('timeframe',id);
      history.replaceState(history.state,'',u.pathname+u.search+u.hash);
    }catch(e){}
    document.documentElement.setAttribute('data-ndsp-v86-selected-frame',id);
    document.documentElement.setAttribute('data-ndsp-v92-selected-frame',id);
    document.dispatchEvent(new CustomEvent('ndsp:timeframe-change',{detail:{timeframe:id}}));
    return id;
  }

  function removeTop(){
    document.querySelectorAll(
      '#ndsp-v86-timeframe-control,#ndsp-v86-timeframe-status,[data-ndsp-v86-timeframe-control]'
    ).forEach(function(el){
      try{el.remove();}catch(e){}
    });
  }

  function removeOldWizard(){
    document.querySelectorAll(
      '#ndsp-v91-timeframe-wizard,[data-ndsp-v91-timeframe-wizard="true"],[data-ndsp-v91-timeframe-grid]'
    ).forEach(function(el){
      var root=el.closest('#ndsp-v91-timeframe-wizard,[data-ndsp-v91-timeframe-wizard="true"]');
      try{(root||el).remove();}catch(e){}
    });

    var all=[].slice.call(document.querySelectorAll('#ndsp-v92-timeframe-wizard'));
    all.slice(1).forEach(function(el){try{el.remove();}catch(e){}});
  }

  function heading(){
    var nodes=document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role="heading"],div,span');
    for(var i=0;i<nodes.length;i++){
      var t=txt(nodes[i]).toLowerCase();
      var ok=t.indexOf('اختر الفريم')>=0 ||
        t.indexOf('اختيار الفريم')>=0 ||
        /choose\s+(the\s+)?timeframe/.test(t) ||
        /select\s+(the\s+)?timeframe/.test(t);
      if(ok){
        var r=nodes[i].getBoundingClientRect();
        if(r.width>80&&r.height>10) return nodes[i];
      }
    }
    return null;
  }

  function card(h){
    var n=h;
    for(var i=0;i<8&&n&&n!==document.body;i++,n=n.parentElement){
      var t=txt(n).toUpperCase();
      var has=(t.indexOf('1H')>=0&&t.indexOf('4H')>=0) ||
        (t.indexOf('DAILY')>=0&&t.indexOf('WEEKLY')>=0);
      var r=n.getBoundingClientRect();
      if(has&&r.width>180&&r.height>100) return n;
    }
    return h.parentElement||h;
  }

  function oldGroup(c,h){
    var best=null;
    var area=Infinity;
    c.querySelectorAll('div,section,nav,[role="group"]').forEach(function(n){
      if(n.contains(h)||n.id==='ndsp-v92-timeframe-wizard') return;
      var t=txt(n).toUpperCase();
      var score=['1H','4H','DAILY','WEEKLY'].filter(function(x){return t.indexOf(x)>=0;}).length;
      var r=n.getBoundingClientRect();
      var a=r.width*r.height;
      if(score>=3&&r.width>120&&r.height>30&&a<area){
        best=n;
        area=a;
      }
    });
    return best;
  }

  function update(id){
    document.querySelectorAll('[data-ndsp-v92-timeframe-button]').forEach(function(b){
      b.setAttribute('aria-pressed',b.getAttribute('data-frame')===id?'true':'false');
    });
  }

  function apply(id,old){
    if(applying) return;
    applying=true;
    id=persist(id);
    try{
      if(window.__NDSP_MULTI_TIMEFRAME_V86__&&
         typeof window.__NDSP_MULTI_TIMEFRAME_V86__.setFrame==='function'){
        window.__NDSP_MULTI_TIMEFRAME_V86__.setFrame(id,false);
      }
    }catch(e){}
    update(id);
    setTimeout(function(){applying=false;},100);
  }

  function build(c,old){
    var w=document.createElement('div');
    w.id='ndsp-v92-timeframe-wizard';
    w.setAttribute('data-ndsp-timeframe-wizard-ui','true');

    var g=document.createElement('div');
    g.id='ndsp-v92-timeframe-grid';
    g.setAttribute('role','group');
    g.setAttribute('aria-label',arabic()?'اختر الفريم':'Choose timeframe');

    FRAMES.forEach(function(f){
      var b=document.createElement('button');
      b.type='button';
      b.setAttribute('data-ndsp-v92-timeframe-button','true');
      b.setAttribute('data-frame',f[0]);
      b.setAttribute('aria-pressed','false');
      b.textContent=arabic()?f[1]:f[2];
      b.addEventListener('click',function(){apply(f[0],old);});
      g.appendChild(b);
    });

    w.appendChild(g);
    if(old&&old.parentElement){
      old.parentElement.insertBefore(w,old.nextSibling);
    }else{
      c.appendChild(w);
    }
    return w;
  }

  function render(){
    removeTop();
    removeOldWizard();

    var h=heading();
    if(!h) return false;

    var c=card(h);
    var old=oldGroup(c,h);
    if(old) old.setAttribute('data-ndsp-v92-old-frame-group','true');

    var w=document.getElementById('ndsp-v92-timeframe-wizard');
    if(!w) w=build(c,old);

    var id=selected();
    update(id);
    document.documentElement.setAttribute('data-ndsp-v92-selected-frame',id);
    return true;
  }

  function schedule(){
    clearTimeout(timer);
    timer=setTimeout(render,60);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',render,{once:true});
  }else{
    render();
  }

  new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true});
  document.addEventListener('ndsp:timeframe-change',schedule);
  window.addEventListener('popstate',schedule);

  setTimeout(render,250);
  setTimeout(render,900);
  setTimeout(render,1800);
})();
