/* NDSP_LOGIN_CLEAN_V1 */
(() => {
  "use strict";

  const form = document.getElementById("ndsp-login-form");
  if (!form) return;

  const message = document.getElementById("auth-message");
  const submit = form.querySelector('button[type="submit"]');
  const params = new URLSearchParams(window.location.search);
  const emailInput = form.querySelector('input[name="email"]');

  const show = (text, type = "error") => {
    message.textContent = text;
    message.className = `auth-message show ${type}`;
  };

  if (params.get("registered") === "1") {
    show("تم إنشاء الحساب. سجّل الدخول للمتابعة.", "success");
  } else if (params.get("logged_out") === "1") {
    show("تم تسجيل الخروج بنجاح.", "success");
  } else if (params.get("error") === "forbidden") {
    show("هذا الحساب لا يملك صلاحية دخول لوحة الإدارة.");
  }

  if (params.get("email") && emailInput) {
    emailInput.value = params.get("email");
  }

  const safeNext = (authenticatedUser = null) => {
    const next = params.get("next");

    if (next && next.startsWith("/") && !next.startsWith("//")) {
      return next;
    }

    const role = String(
      authenticatedUser?.role ||
      authenticatedUser?.accountType ||
      authenticatedUser?.account_type ||
      ""
    ).trim().toUpperCase();

    if (["ADMIN", "OWNER"].includes(role)) {
      return "/owner/";
    }

    return params.get("admin") === "1"
      ? "/owner/"
      : "/portal-v50/";
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const email = String(data.get("email") || "").trim().toLowerCase();
    const password = String(data.get("password") || "");
    const remember = data.get("remember") === "on";
    const requestedNext = params.get("next") || "";
    const adminIntent =
      params.get("admin") === "1" ||
      requestedNext.startsWith("/owner") ||
      requestedNext.startsWith("/admin");

    if (!email.includes("@")) return show("اكتب بريدًا إلكترونيًا صحيحًا.");
    if (!password) return show("اكتب كلمة المرور.");

    submit.disabled = true;
    submit.textContent = "جارٍ التحقق";

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        credentials: "same-origin",
        cache: "no-store",
        body: JSON.stringify({ email, password, remember, adminIntent })
      });

      let payload = {};
      try { payload = await response.json(); } catch {}

      if (!response.ok) {
        const code = String(payload?.error || "").toUpperCase();
        if (code.includes("INVALID") || response.status === 401) {
          throw new Error("البريد أو كلمة المرور غير صحيحة.");
        }
        if (code.includes("SUSPEND") || code.includes("INACTIVE")) {
          throw new Error("الحساب غير نشط. تواصل مع الإدارة.");
        }
        throw new Error(payload?.message || "تعذر تسجيل الدخول الآن.");
      }

      show("تم التحقق. جارٍ فتح البوابة.", "success");
      window.setTimeout(
        () => window.location.assign(safeNext(payload?.user || payload?.account)),
        350
      );
    } catch (error) {
      show(error?.message || "تعذر تسجيل الدخول الآن.");
    } finally {
      submit.disabled = false;
      submit.textContent = "دخول آمن";
    }
  });

  document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.passwordToggle);
      if (!input) return;
      const visible = input.type === "text";
      input.type = visible ? "password" : "text";
      button.textContent = visible ? "إظهار" : "إخفاء";
    });
  });
})();
