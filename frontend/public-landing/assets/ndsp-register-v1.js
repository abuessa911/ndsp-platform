/* NDSP_REGISTER_CLEAN_V1 */
(() => {
  "use strict";

  const form = document.getElementById("ndsp-register-form");
  if (!form) return;

  const message = document.getElementById("auth-message");
  const submit = form.querySelector('button[type="submit"]');

  const show = (text, type = "error") => {
    message.textContent = text;
    message.className = `auth-message show ${type}`;
  };

  const clear = () => {
    message.textContent = "";
    message.className = "auth-message";
  };

  const parseBody = async (response) => {
    const type = response.headers.get("content-type") || "";
    if (type.includes("application/json")) {
      try { return await response.json(); } catch {}
    }
    try { return { message: await response.text() }; } catch {}
    return {};
  };

  const friendly = (status, payload) => {
    const code = String(payload?.error || payload?.code || "").toUpperCase();
    if (status === 409 || code.includes("EXISTS") || code.includes("DUPLICATE")) {
      return "يوجد حساب مسجل بهذا البريد أو رقم الجوال.";
    }
    if (code.includes("SEAT") || code.includes("CAPACITY")) {
      return "اكتمل العدد المتاح حاليًا. حاول لاحقًا.";
    }
    if (status === 400 || status === 422) {
      return payload?.message || "تحقق من البيانات المدخلة ثم أعد المحاولة.";
    }
    return payload?.message || "تعذر إنشاء الحساب الآن. أعد المحاولة بعد قليل.";
  };

  const send = async (endpoint, payload) => {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      credentials: "same-origin",
      cache: "no-store",
      body: JSON.stringify(payload)
    });
    return { response, body: await parseBody(response) };
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clear();

    const data = new FormData(form);
    const name = String(data.get("name") || "").trim();
    const email = String(data.get("email") || "").trim().toLowerCase();
    const phone = String(data.get("phone") || "").trim();
    const password = String(data.get("password") || "");
    const confirmPassword = String(data.get("confirm_password") || "");
    const accepted = data.get("accept_terms") === "on";

    if (name.length < 2) return show("اكتب الاسم بشكل صحيح.");
    if (!email.includes("@")) return show("اكتب بريدًا إلكترونيًا صحيحًا.");
    if (phone.length < 8) return show("اكتب رقم جوال صحيحًا.");
    if (password.length < 8) return show("كلمة المرور يجب ألا تقل عن 8 أحرف.");
    if (password !== confirmPassword) return show("كلمة المرور وتأكيدها غير متطابقين.");
    if (!accepted) return show("يجب الموافقة على إخلاء المسؤولية وشروط التجربة.");

    const payload = {
      name,
      email,
      phone,
      password,
      confirm_password: confirmPassword,
      confirmPassword,
      acceptedTerms: true,
      acceptedDisclaimer: true,
      trialDays: 16
    };

    submit.disabled = true;
    submit.textContent = "جارٍ إنشاء الحساب";

    try {
      let result = await send("/api/trial/register/ordinary", payload);
      if ([404, 405].includes(result.response.status)) {
        result = await send("/api/register", payload);
      }

      if (!result.response.ok) {
        throw Object.assign(new Error("REGISTER_FAILED"), result);
      }

      show("تم إنشاء الحساب. سيتم نقلك إلى تسجيل الدخول.", "success");
      window.setTimeout(() => {
        window.location.assign(`/login/?registered=1&email=${encodeURIComponent(email)}`);
      }, 900);
    } catch (error) {
      const status = error?.response?.status || 0;
      show(friendly(status, error?.body || {}));
    } finally {
      submit.disabled = false;
      submit.textContent = "إنشاء الحساب وبدء التجربة";
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
