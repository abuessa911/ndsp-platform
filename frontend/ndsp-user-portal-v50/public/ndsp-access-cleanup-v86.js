(function () {
  'use strict';
  if (window.__NDSP_ACCESS_V86__) return;
  window.__NDSP_ACCESS_V86__=true;
  var HOME='https://www.ndsp.app/';
  var exact=[
    '\u0627\u0644\u0639\u0648\u062f\u0629 \u0625\u0644\u0649 \u063a\u0631\u0641\u0629 \u0627\u0644\u0642\u0631\u0627\u0631',
    '\u0627\u0644\u0639\u0648\u062f\u0629 \u0627\u0644\u0649 \u063a\u0631\u0641\u0629 \u0627\u0644\u0642\u0631\u0627\u0631',
    'Back to Decision Room','Return to Decision Room'
  ];
  var known='#ndsp-home-link-v75,#ndsp-home-hard-fix-v74,#ndsp-approved-home-link-v73,[data-ndsp-home-link-v75],[data-ndsp-home-hard-fix-v74],[data-ndsp-approved-home-link-v73]';
  function norm(x){return String(x||'').replace(/\s+/g,' ').trim();}
  function isText(x){return exact.indexOf(norm(x))!==-1;}
  function visible(el){if(!el||!el.isConnected)return false;var s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)!==0&&r.width>0&&r.height>0;}
  function run(){
    document.querySelectorAll(known).forEach(function(el){el.remove();});
    var candidates=[];
    document.querySelectorAll('a,button,[role="link"],[role="button"],span,p,div').forEach(function(el){if(visible(el)&&isText(el.textContent)&&!Array.from(el.children).some(function(c){return isText(c.textContent);})){candidates.push(el);}});
    var keep=null;
    candidates.forEach(function(el){var s=getComputedStyle(el),r=el.getBoundingClientRect();var floating=s.position==='fixed'||s.position==='sticky'||r.width>Math.min(window.innerWidth*0.78,340)||r.height>64;if(floating){el.remove();return;}if(!keep)keep=el;else el.remove();});
    if(keep){var root=keep.closest('a,button,[role="link"],[role="button"]')||keep;if(root.tagName==='A'){root.setAttribute('href',HOME);root.removeAttribute('target');}else{root.setAttribute('role','link');root.setAttribute('tabindex','0');root.onclick=function(e){e.preventDefault();window.location.assign(HOME);};root.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();window.location.assign(HOME);}};}root.setAttribute('data-ndsp-v86-original-back-link','1');}
    document.documentElement.setAttribute('data-ndsp-v86-access-clean','active');
  }
  var timer=null;function schedule(){clearTimeout(timer);timer=setTimeout(run,40);}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true});setTimeout(run,500);setTimeout(run,1800);
})();
