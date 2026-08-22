/*
  NDSP — Auth Mobile iOS Fix V75
*/
(function () {
  "use strict";

  var ATTR = "data-ndsp-auth-mobile-ios-v75";
  var ROUTE_RE = /(login|register|signup|sign-up|auth|forgot-password|reset-password)/i;
  var TEXT_RE = /تسجيل الدخول|إنشاء الحساب|إنشاء حساب|انشئ حساب|أنشئ حساب|البريد الإلكتروني|كلمة المرور|الوصول الآمن/i;

  function isAuthRoute() {
    var path = String(window.location.pathname || "");
    var hash = String(window.location.hash || "");
    var search = String(window.location.search || "");

    if (ROUTE_RE.test(path) || ROUTE_RE.test(hash) || ROUTE_RE.test(search)) return true;

    var title = String(document.title || "");
    if (ROUTE_RE.test(title)) return true;

    var bodyText = "";
    try {
      bodyText = String(document.body ? document.body.innerText : "").slice(0, 2000);
    } catch (_) {}

    return TEXT_RE.test(bodyText);
  }

  function setVh() {
    var h = window.innerHeight || document.documentElement.clientHeight || 0;
    if (h > 0) {
      document.documentElement.style.setProperty("--ndsp-auth-vh", (h * 0.01) + "px");
    }
  }

  function normalize() {
    Array.prototype.forEach.call(
      document.querySelectorAll("input[autofocus], textarea[autofocus], select[autofocus]"),
      function (el) {
        try { el.removeAttribute("autofocus"); } catch (_) {}
      }
    );

    Array.prototype.forEach.call(
      document.querySelectorAll("input, textarea, select"),
      function (el) {
        try { el.style.fontSize = "16px"; } catch (_) {}
      }
    );
  }

  function markPage() {
    if (!isAuthRoute()) return false;

    document.documentElement.setAttribute(ATTR, "1");

    if (document.body) {
      document.body.setAttribute(ATTR, "1");
      document.body.classList.add("ndsp-auth-mobile-top-lock-v75");
    }

    var root = document.querySelector("#root") || document.querySelector("#app");
    if (root) root.classList.add("ndsp-auth-mobile-top-lock-v75");

    var main = document.querySelector("main");
    if (main) main.classList.add("ndsp-auth-page", "ndsp-auth-mobile-top-lock-v75");

    normalize();
    return true;
  }

  function forceTop() {
    if (!markPage()) return;

    try {
      if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    } catch (_) {}

    function run() {
      try {
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        window.scrollTo(0, 0);
      } catch (_) {}
    }

    run();
    requestAnimationFrame(run);
    setTimeout(run, 40);
    setTimeout(run, 120);
    setTimeout(run, 300);
    setTimeout(run, 700);
    setTimeout(run, 1200);
  }

  function boot() {
    setVh();
    forceTop();
  }

  window.addEventListener("resize", setVh, { passive: true });

  window.addEventListener("orientationchange", function () {
    setTimeout(setVh, 80);
    setTimeout(forceTop, 180);
  }, { passive: true });

  window.addEventListener("pageshow", function () {
    setVh();
    forceTop();
  }, { passive: true });

  window.addEventListener("load", function () {
    setVh();
    forceTop();
  }, { passive: true });

  document.addEventListener("DOMContentLoaded", boot);

  var oldPush = history.pushState;
  var oldReplace = history.replaceState;

  history.pushState = function () {
    var out = oldPush.apply(this, arguments);
    setTimeout(boot, 50);
    return out;
  };

  history.replaceState = function () {
    var out = oldReplace.apply(this, arguments);
    setTimeout(boot, 50);
    return out;
  };

  window.addEventListener("popstate", function () {
    setTimeout(boot, 50);
  }, { passive: true });

  function startObserver() {
    if (!document.body) {
      setTimeout(startObserver, 50);
      return;
    }

    var mo = new MutationObserver(function () {
      if (isAuthRoute()) markPage();
    });

    mo.observe(document.body, { childList: true, subtree: true });
    boot();
  }

  startObserver();
})();
