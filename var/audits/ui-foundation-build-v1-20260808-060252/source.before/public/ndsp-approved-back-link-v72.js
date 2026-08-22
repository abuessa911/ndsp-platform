(function () {
  "use strict";

  var TARGET = "https://www.ndsp.app/";
  var MARKER = "ndspApprovedBackLinkV72";

  function normalize(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function isApprovedBackControl(element) {
    var text = normalize(element && element.textContent);
    return (
      text.indexOf("العودة إلى غرفة القرار") !== -1 ||
      text.indexOf("العودة لغرفة القرار") !== -1 ||
      text.indexOf("back to decision room") !== -1 ||
      text.indexOf("return to decision room") !== -1
    );
  }

  function bind(element) {
    if (!element || !isApprovedBackControl(element)) {
      return;
    }

    if (element.tagName === "A") {
      element.setAttribute("href", TARGET);
      element.setAttribute("rel", "noopener");
    }

    if (element.dataset && element.dataset[MARKER] === "1") {
      return;
    }

    if (element.dataset) {
      element.dataset[MARKER] = "1";
    }

    element.addEventListener(
      "click",
      function (event) {
        event.preventDefault();
        event.stopPropagation();
        if (typeof event.stopImmediatePropagation === "function") {
          event.stopImmediatePropagation();
        }
        window.location.assign(TARGET);
      },
      true
    );
  }

  function scan() {
    var controls = document.querySelectorAll(
      "a, button, [role='button'], [data-href], [onclick]"
    );

    for (var i = 0; i < controls.length; i += 1) {
      bind(controls[i]);
    }
  }

  function start() {
    scan();

    if (document.documentElement) {
      var observer = new MutationObserver(scan);
      observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        characterData: true
      });
    }

    window.setInterval(scan, 1200);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }

  window.addEventListener("pageshow", scan);
})();
