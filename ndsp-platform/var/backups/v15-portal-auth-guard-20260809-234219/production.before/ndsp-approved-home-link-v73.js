(function () {
  "use strict";

  var TARGET = "https://www.ndsp.app/";
  var LINK_ID = "ndsp-approved-home-link-v73";
  var DATA_KEY = "ndspApprovedHomeLinkV73";
  var running = false;

  function normalize(value) {
    return String(value || "")
      .replace(/\u00a0/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function matchesApprovedBackText(value) {
    var text = normalize(value);
    return (
      text.indexOf("العودة إلى غرفة القرار") !== -1 ||
      text.indexOf("العودة لغرفة القرار") !== -1 ||
      text.indexOf("العودة الى غرفة القرار") !== -1 ||
      text.indexOf("back to decision room") !== -1 ||
      text.indexOf("return to decision room") !== -1
    );
  }

  function goHome(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
      if (typeof event.stopImmediatePropagation === "function") {
        event.stopImmediatePropagation();
      }
    }
    window.location.assign(TARGET);
  }

  function bindExisting(element) {
    if (!element || !matchesApprovedBackText(element.textContent)) {
      return false;
    }

    if (element.tagName === "A") {
      element.setAttribute("href", TARGET);
      element.setAttribute("rel", "noopener");
    } else {
      element.setAttribute("role", "link");
      element.setAttribute("tabindex", "0");
    }

    element.setAttribute("data-" + DATA_KEY.replace(/[A-Z]/g, function (m) {
      return "-" + m.toLowerCase();
    }), "1");

    if (element.dataset && element.dataset.ndspV73Bound === "1") {
      return true;
    }

    if (element.dataset) {
      element.dataset.ndspV73Bound = "1";
    }

    element.style.cursor = "pointer";

    element.addEventListener("click", goHome, true);
    element.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        goHome(event);
      }
    }, true);

    return true;
  }

  function findBestHost() {
    var forms = document.querySelectorAll("form");

    if (forms.length > 0) {
      var form = forms[forms.length - 1];
      var node = form;

      for (var depth = 0; depth < 5 && node && node.parentElement; depth += 1) {
        if (node.parentElement.children.length <= 12) {
          node = node.parentElement;
        } else {
          break;
        }
      }

      return node || form;
    }

    return (
      document.querySelector("main") ||
      document.querySelector("[role='main']") ||
      document.querySelector("body")
    );
  }

  function createApprovedLink() {
    var link = document.getElementById(LINK_ID);

    if (link) {
      bindExisting(link);
      return link;
    }

    link = document.createElement("a");
    link.id = LINK_ID;
    link.href = TARGET;
    link.rel = "noopener";
    link.textContent = document.documentElement.dir === "ltr"
      ? "Back to Decision Room"
      : "العودة إلى غرفة القرار";

    link.setAttribute("data-ndsp-approved-home-link-v73", "1");
    link.setAttribute("aria-label", link.textContent);

    link.style.display = "block";
    link.style.width = "fit-content";
    link.style.maxWidth = "calc(100% - 32px)";
    link.style.margin = "22px auto 4px";
    link.style.padding = "10px 14px";
    link.style.textAlign = "center";
    link.style.fontFamily = "inherit";
    link.style.fontSize = "clamp(15px, 4vw, 18px)";
    link.style.fontWeight = "500";
    link.style.lineHeight = "1.5";
    link.style.color = "#d8b85a";
    link.style.textDecoration = "none";
    link.style.borderRadius = "10px";
    link.style.cursor = "pointer";
    link.style.position = "relative";
    link.style.zIndex = "20";

    link.addEventListener("click", goHome, true);

    var host = findBestHost();

    if (host && host.parentNode && host.tagName === "FORM") {
      host.insertAdjacentElement("afterend", link);
    } else if (host) {
      host.appendChild(link);
    } else {
      document.body.appendChild(link);
    }

    return link;
  }

  function apply() {
    if (running) {
      return;
    }

    running = true;

    try {
      var all = document.querySelectorAll(
        "a, button, [role='button'], [role='link'], div, span, p"
      );
      var found = false;

      for (var i = 0; i < all.length; i += 1) {
        if (matchesApprovedBackText(all[i].textContent)) {
          found = bindExisting(all[i]) || found;
        }
      }

      if (!found) {
        createApprovedLink();
      }
    } finally {
      running = false;
    }
  }

  document.addEventListener("click", function (event) {
    var node = event.target;

    while (node && node !== document.documentElement) {
      if (
        node.id === LINK_ID ||
        matchesApprovedBackText(node.textContent)
      ) {
        goHome(event);
        return;
      }
      node = node.parentElement;
    }
  }, true);

  function start() {
    apply();

    if (document.documentElement) {
      var observer = new MutationObserver(function () {
        window.clearTimeout(window.__ndspV73Timer);
        window.__ndspV73Timer = window.setTimeout(apply, 80);
      });

      observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        characterData: true
      });
    }

    window.setInterval(apply, 1200);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }

  window.addEventListener("pageshow", apply);
})();
