/*
  NDSP — Mobile Auth iOS Layout Fix
  Runtime guard for login/register/auth pages.
*/
(function () {
  "use strict";

  var FIX_ATTR = "data-ndsp-auth-mobile-ios-fix";
  var AUTH_RE = /(login|register|signup|sign-up|auth|forgot-password|reset-password)/i;

  function isAuthRoute() {
    var path = String(window.location.pathname || "");
    var hash = String(window.location.hash || "");
    var search = String(window.location.search || "");
    if (AUTH_RE.test(path) || AUTH_RE.test(hash) || AUTH_RE.test(search)) return true;

    var title = String(document.title || "");
    if (AUTH_RE.test(title)) return true;

    var bodyText = "";
    try {
      bodyText = String(document.body ? document.body.innerText : "").slice(0, 1400);
    } catch (_) {}

    return /تسجيل الدخول|إنشاء الحساب|انشئ حساب|أنشئ حساب|البريد الإلكتروني|كلمة المرور|الوصول الآمن/i.test(bodyText);
  }

  function setVh() {
    var h = window.innerHeight || document.documentElement.clientHeight || 0;
    if (h > 0) {
      document.documentElement.style.setProperty("--ndsp-auth-vh", (h * 0.01) + "px");
    }
  }

  function markAuthPage() {
    if (!isAuthRoute()) return false;

    document.documentElement.setAttribute(FIX_ATTR, "1");
    if (document.body) {
      document.body.setAttribute(FIX_ATTR, "1");
      document.body.classList.add("ndsp-auth-mobile-top-lock");
    }

    var root = document.querySelector("#root") || document.querySelector("#app");
    if (root) root.classList.add("ndsp-auth-mobile-top-lock");

    var main = document.querySelector("main");
    if (main) main.classList.add("ndsp-auth-page", "ndsp-auth-mobile-top-lock");

    Array.prototype.forEach.call(document.querySelectorAll("input[autofocus], textarea[autofocus], select[autofocus]"), function (el) {
      try { el.removeAttribute("autofocus"); } catch (_) {}
    });

    Array.prototype.forEach.call(document.querySelectorAll("input, textarea, select"), function (el) {
      try {
        el.style.fontSize = "16px";
      } catch (_) {}
    });

    return true;
  }

  function forceTop(reason) {
    if (!markAuthPage()) return;
    if (window.location.hash && !AUTH_RE.test(window.location.hash)) return;

    try {
      if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    } catch (_) {}

    var run = function () {
      try {
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        window.scrollTo(0, 0);
      } catch (_) {}
    };

    run();
    setTimeout(run, 40);
    setTimeout(run, 120);
    setTimeout(run, 300);
    setTimeout(run, 650);
  }

  function boot() {
    setVh();
    forceTop("boot");
  }

  window.addEventListener("resize", setVh, { passive: true });
  window.addEventListener("orientationchange", function () {
    setTimeout(setVh, 80);
    setTimeout(function () { forceTop("orientationchange"); }, 180);
  }, { passive: true });

  window.addEventListener("pageshow", function () {
    setVh();
    forceTop("pageshow");
  }, { passive: true });

  window.addEventListener("load", function () {
    setVh();
    forceTop("load");
  }, { passive: true });

  document.addEventListener("DOMContentLoaded", boot);

  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
    if (!a) return;
    var href = String(a.getAttribute("href") || "");
    if (AUTH_RE.test(href)) {
      try { sessionStorage.setItem("ndsp_auth_force_top", "1"); } catch (_) {}
      setTimeout(function () { forceTop("auth-link-click"); }, 80);
    }
  }, true);

  var originalPushState = history.pushState;
  var originalReplaceState = history.replaceState;

  history.pushState = function () {
    var out = originalPushState.apply(this, arguments);
    setTimeout(function () {
      setVh();
      forceTop("pushState");
    }, 50);
    return out;
  };

  history.replaceState = function () {
    var out = originalReplaceState.apply(this, arguments);
    setTimeout(function () {
      setVh();
      forceTop("replaceState");
    }, 50);
    return out;
  };

  window.addEventListener("popstate", function () {
    setTimeout(function () {
      setVh();
      forceTop("popstate");
    }, 50);
  }, { passive: true });

  var mo = new MutationObserver(function () {
    if (isAuthRoute()) {
      markAuthPage();
    }
  });

  function startObserver() {
    if (document.body) {
      mo.observe(document.body, { childList: true, subtree: true });
      boot();
    } else {
      setTimeout(startObserver, 50);
    }
  }

  startObserver();
})();
