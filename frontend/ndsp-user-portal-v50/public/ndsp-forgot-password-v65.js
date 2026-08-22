(function () {
  "use strict";

  var LINK_ID = "ndsp-forgot-password-link";
  var STYLE_ID = "ndsp-forgot-password-style-v65";
  var TARGET = "/forgot-password.html";
  var LABEL = "\u0646\u0633\u064a\u062a \u0643\u0644\u0645\u0629 \u0627\u0644\u0645\u0631\u0648\u0631\u061f";

  function isLoginContext() {
    var path = String(window.location.pathname || "").toLowerCase();
    return /(^|\/)login(?:\/|\.html|$)/.test(path) ||
      Boolean(document.querySelector('form input[type="password"]'));
  }

  function ensureStyle() {
    if (document.getElementById(STYLE_ID)) {
      return;
    }

    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      ".ndsp-forgot-password-wrap-v65{display:flex;justify-content:center;align-items:center;width:100%;margin:14px 0 8px;direction:rtl}",
      ".ndsp-forgot-password-link-v65{display:inline-flex;justify-content:center;align-items:center;min-height:46px;padding:10px 24px;border:1px solid rgba(214,177,61,.58);border-radius:14px;background:rgba(214,177,61,.08);color:#e7c75e!important;font-weight:700;font-size:15px;line-height:1.4;text-decoration:none!important;box-sizing:border-box;transition:background .18s ease,border-color .18s ease,transform .18s ease}",
      ".ndsp-forgot-password-link-v65:hover,.ndsp-forgot-password-link-v65:focus-visible{background:rgba(214,177,61,.16);border-color:rgba(231,199,94,.9);outline:none;transform:translateY(-1px)}",
      ".ndsp-forgot-password-link-v65:active{transform:translateY(0)}",
      "@media(max-width:640px){.ndsp-forgot-password-link-v65{width:100%;min-height:48px}}"
    ].join("");
    document.head.appendChild(style);
  }

  function findPasswordInput() {
    return document.querySelector(
      'form input[type="password"], input[name="password"], input[autocomplete="current-password"]'
    );
  }

  function injectButton() {
    if (!isLoginContext()) {
      return false;
    }

    if (document.getElementById(LINK_ID)) {
      return true;
    }

    var password = findPasswordInput();
    if (!password) {
      return false;
    }

    var form = password.closest("form") || password.parentElement;
    if (!form) {
      return false;
    }

    ensureStyle();

    var wrap = document.createElement("div");
    wrap.className = "ndsp-forgot-password-wrap-v65";
    wrap.setAttribute("dir", "rtl");
    wrap.setAttribute("data-ndsp-v65", "forgot-password");

    var link = document.createElement("a");
    link.id = LINK_ID;
    link.className = "ndsp-forgot-password-link-v65";
    link.href = TARGET;
    link.textContent = LABEL;
    link.setAttribute("aria-label", "Forgot password");
    link.setAttribute("data-target", TARGET);

    wrap.appendChild(link);

    var submit = form.querySelector(
      'button[type="submit"], input[type="submit"], [data-action="login"]'
    );

    if (submit && submit.parentNode) {
      submit.parentNode.insertBefore(wrap, submit);
    } else {
      var field = password.closest(
        ".field, .form-field, .form-group, .input-group, label, div"
      ) || password;

      if (field.parentNode) {
        field.parentNode.insertBefore(wrap, field.nextSibling);
      } else {
        form.appendChild(wrap);
      }
    }

    return true;
  }

  function boot() {
    if (injectButton()) {
      return;
    }

    var observer = new MutationObserver(function () {
      if (injectButton()) {
        observer.disconnect();
      }
    });

    observer.observe(document.documentElement, {
      childList: true,
      subtree: true
    });

    window.setTimeout(function () {
      observer.disconnect();
      injectButton();
    }, 30000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
}());
