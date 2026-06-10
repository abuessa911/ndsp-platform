(function () {
  "use strict";

  const CHOICE_KEY = "ndsp_2fa_user_selected";
  const REQUEST_KEY = "ndsp_2fa_requested_for_login";
  const DASHBOARD_PATH = "/DSP_Command_Center.html";

  function lowerText(el) {
    return ((el && (el.innerText || el.textContent || el.value)) || "").trim().toLowerCase();
  }

  function bodyText() {
    return (document.body && document.body.innerText ? document.body.innerText : "").toLowerCase();
  }

  function isLoginPage() {
    return /login|ndsp_login/i.test(location.pathname);
  }

  function isLoginButton(el) {
    if (!el) return false;
    const t = lowerText(el);
    return (
      t.includes("login") ||
      t.includes("sign in") ||
      t.includes("تسجيل الدخول") ||
      t === "دخول"
    );
  }

  function wants2FA() {
    const cb = document.getElementById("ndsp-login-2fa-choice");
    if (cb) return !!cb.checked;
    return localStorage.getItem(CHOICE_KEY) === "1";
  }

  function saveChoice(value) {
    localStorage.setItem(CHOICE_KEY, value ? "1" : "0");
    localStorage.setItem(REQUEST_KEY, value ? "1" : "0");
  }

  function looksLikeOtpView() {
    const txt = bodyText();
    const codeInputs = Array.from(document.querySelectorAll("input")).filter(function (i) {
      const ml = String(i.getAttribute("maxlength") || i.maxLength || "");
      const type = String(i.getAttribute("type") || "").toLowerCase();
      const im = String(i.getAttribute("inputmode") || "").toLowerCase();
      return (
        ml === "1" ||
        im === "numeric" ||
        type === "tel" ||
        type === "number"
      );
    });

    return (
      codeInputs.length >= 4 ||
      txt.includes("التحقق بخطوتين") ||
      txt.includes("أدخل الرمز") ||
      txt.includes("ادخل الرمز") ||
      txt.includes("verification code") ||
      txt.includes("two-step") ||
      txt.includes("two factor") ||
      txt.includes("2fa")
    );
  }

  function goDashboard() {
    if (!wants2FA()) {
      localStorage.setItem(REQUEST_KEY, "0");
      window.location.href = DASHBOARD_PATH;
    }
  }

  function addChoiceBox() {
    if (!isLoginPage()) return;
    if (document.getElementById("ndsp-2fa-choice-box")) return;
    if (looksLikeOtpView()) return;

    const loginBtn = Array.from(document.querySelectorAll("button,a,input,[role='button']")).find(isLoginButton);
    const passwordInput = document.querySelector("input[type='password']");
    const anchor = loginBtn || passwordInput || document.querySelector("form") || document.body;
    if (!anchor || !anchor.parentNode) return;

    const box = document.createElement("div");
    box.id = "ndsp-2fa-choice-box";
    box.setAttribute("dir", "rtl");
    box.style.cssText = [
      "margin:14px 0",
      "padding:12px 14px",
      "border:1px solid rgba(214,176,73,.35)",
      "border-radius:14px",
      "background:rgba(214,176,73,.08)",
      "color:#e8edf5",
      "font-size:13px",
      "line-height:1.8"
    ].join(";");

    box.innerHTML =
      '<label style="display:flex;align-items:center;gap:10px;cursor:pointer;justify-content:flex-start">' +
        '<input id="ndsp-login-2fa-choice" type="checkbox" style="width:18px;height:18px;accent-color:#d6b049">' +
        '<span><b>اختياري:</b> تفعيل التحقق بخطوتين لهذا الدخول فقط</span>' +
      '</label>' +
      '<div style="opacity:.78;margin-top:6px">إذا لم تحدد الخيار، سيتم الدخول العادي بدون نقلك إلى صفحة كود التحقق.</div>' +
      '<div style="opacity:.68;margin-top:3px;direction:ltr;text-align:left">Optional: enable two-step verification for this login only.</div>';

    anchor.parentNode.insertBefore(box, anchor);

    const cb = document.getElementById("ndsp-login-2fa-choice");
    cb.checked = localStorage.getItem(CHOICE_KEY) === "1";
    cb.addEventListener("change", function () {
      saveChoice(cb.checked);
    });
    saveChoice(cb.checked);
  }

  function addOtpSkipBox() {
    if (!looksLikeOtpView()) return;
    if (wants2FA()) return;
    if (document.getElementById("ndsp-otp-skip-box")) return;

    const host = document.querySelector("form") || document.body.firstElementChild || document.body;
    const box = document.createElement("div");
    box.id = "ndsp-otp-skip-box";
    box.setAttribute("dir", "rtl");
    box.style.cssText = [
      "margin:14px auto",
      "max-width:520px",
      "padding:14px",
      "border:1px solid rgba(55,214,201,.4)",
      "border-radius:16px",
      "background:rgba(55,214,201,.08)",
      "color:#e8edf5",
      "font-size:14px",
      "line-height:1.8",
      "text-align:center"
    ].join(";");

    box.innerHTML =
      '<b>التحقق بخطوتين اختياري الآن.</b><br>' +
      '<span style="opacity:.8">لم يتم اختيار 2FA قبل الدخول، لذلك يمكنك المتابعة بدون كود.</span><br>' +
      '<button id="ndsp-skip-otp-now" type="button" style="margin-top:10px;padding:11px 18px;border-radius:12px;border:1px solid rgba(214,176,73,.55);background:#d6b049;color:#080b10;font-parameter:800;cursor:pointer">متابعة بدون كود</button>';

    if (host && host.parentNode) {
      host.parentNode.insertBefore(box, host);
    } else {
      document.body.prepend(box);
    }

    const btn = document.getElementById("ndsp-skip-otp-now");
    if (btn) btn.addEventListener("click", goDashboard);

    setTimeout(function () {
      if (!wants2FA() && looksLikeOtpView()) goDashboard();
    }, 450);
  }

  function monitorLoginAttempt() {
    saveChoice(wants2FA());

    if (wants2FA()) return;

    let rounds = 0;
    const timer = setInterval(function () {
      rounds += 1;
      if (looksLikeOtpView()) {
        clearInterval(timer);
        goDashboard();
      }
      if (rounds > 40) clearInterval(timer);
    }, 150);
  }

  function patchFetch() {
    if (window.__ndsp2faOptionalFetchPatched) return;
    window.__ndsp2faOptionalFetchPatched = true;

    const originalFetch = window.fetch;
    if (typeof originalFetch !== "function") return;

    window.fetch = async function (input, init) {
      init = init || {};
      const selected = wants2FA();

      try {
        const headers = new Headers(init.headers || {});
        headers.set("X-DSP-2FA-Requested", selected ? "1" : "0");
        headers.set("X-DSP-2FA-Optional", selected ? "0" : "1");
        init.headers = headers;
      } catch (_) {}

      const response = await originalFetch(input, init);

      try {
        const url = typeof input === "string" ? input : (input && input.url ? input.url : "");
        const contentType = response.headers.get("content-type") || "";

        if (!selected && /login|auth|signin|session/i.test(url) && contentType.includes("application/json")) {
          const data = await response.clone().json();
          let changed = false;

          function clean(obj) {
            if (!obj || typeof obj !== "object") return;
            Object.keys(obj).forEach(function (k) {
              const key = k.toLowerCase();
              if (
                key === "requires2fa" ||
                key === "requires_2fa" ||
                key === "require2fa" ||
                key === "require_2fa" ||
                key === "mfarequired" ||
                key === "mfa_required" ||
                key === "otprequired" ||
                key === "otp_required" ||
                key === "twofactorrequired" ||
                key === "two_factor_required"
              ) {
                obj[k] = false;
                changed = true;
              }

              if (
                key === "nextstep" ||
                key === "next_step" ||
                key === "step" ||
                key === "screen"
              ) {
                const v = String(obj[k] || "").toLowerCase();
                if (v.includes("2fa") || v.includes("otp") || v.includes("verify")) {
                  obj[k] = "dashboard";
                  changed = true;
                }
              }

              if (obj[k] && typeof obj[k] === "object") clean(obj[k]);
            });
          }

          clean(data);

          if (changed) {
            const newHeaders = new Headers(response.headers);
            newHeaders.set("content-type", "application/json; charset=utf-8");
            return new Response(JSON.stringify(data), {
              status: response.status,
              statusText: response.statusText,
              headers: newHeaders
            });
          }
        }
      } catch (_) {}

      return response;
    };
  }

  function boot() {
    patchFetch();
    addChoiceBox();
    addOtpSkipBox();

    document.addEventListener("click", function (e) {
      const btn = e.target && e.target.closest ? e.target.closest("button,a,input,[role='button']") : null;
      if (isLoginButton(btn)) monitorLoginAttempt();
    }, true);

    document.addEventListener("submit", function () {
      monitorLoginAttempt();
    }, true);

    const observer = new MutationObserver(function () {
      addChoiceBox();
      addOtpSkipBox();
    });

    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
