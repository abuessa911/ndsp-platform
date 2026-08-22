(function(){
  if (location.hostname !== "ndsp.app") return;

  function removeDevil(){
    var selectors = [
      "#ndsp-devil-advocate-visible-card",
      "#ndsp-devil-advocate-integrated-card",
      "[data-ndsp-layer='devil-advocate']"
    ];

    selectors.forEach(function(sel){
      document.querySelectorAll(sel).forEach(function(el){
        if (el && el.parentNode) el.parentNode.removeChild(el);
      });
    });

    var nodes = Array.prototype.slice.call(document.querySelectorAll("aside, section, div"));
    nodes.forEach(function(el){
      var txt = (el.innerText || el.textContent || "").trim();
      if (!txt) return;

      if (txt.indexOf("محامي الشيطان") !== -1 || txt.indexOf("اختبار الاعتراض المعاكس") !== -1) {
        if (el === document.body || el === document.documentElement) return;
        if (txt.length > 1600) return;
        try { el.remove(); } catch(e) {}
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", removeDevil);
  } else {
    removeDevil();
  }

  setTimeout(removeDevil, 250);
  setTimeout(removeDevil, 900);
  setTimeout(removeDevil, 1800);
})();
