import React, { FormEvent, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const ADMIN_EMAIL = "ndsp.app@gmail.com";

type User = {
  email: string;
  name: string | null;
  role: string;
  accountType: string;
  isAdmin: boolean;
};

type LoginResponse = {
  ok: boolean;
  error?: string;
  redirect?: string;
  user?: User;
};

function App() {
  const query = new URLSearchParams(location.search);
  const initialAdmin = query.get("admin") === "1";
  const [email, setEmail] = useState(initialAdmin ? ADMIN_EMAIL : "");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState(
    query.get("logged_out") === "1" ? "تم تسجيل الخروج بأمان." : ""
  );
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/auth/session", { credentials: "include", cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) return;
        const payload = await response.json();
        const user = payload?.user as User | undefined;
        if (user?.isAdmin) location.replace("/owner/");
        else if (user) location.replace("/portal/command-center/");
      })
      .catch(() => undefined);
  }, []);

  async function authenticate(adminIntent: boolean) {
    setError("");
    setMessage("");

    const normalizedEmail = adminIntent ? ADMIN_EMAIL : email.trim().toLowerCase();
    if (adminIntent && email !== ADMIN_EMAIL) setEmail(ADMIN_EMAIL);
    if (!normalizedEmail || !password) {
      setError("أدخل البريد الإلكتروني وكلمة المرور.");
      return;
    }

    setBusy(true);
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        credentials: "include",
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: normalizedEmail,
          password,
          remember,
          adminIntent
        })
      });
      const payload = (await response.json().catch(() => ({}))) as LoginResponse;

      if (!response.ok || !payload.ok) {
        if (payload.error === "ADMIN_ACCESS_REQUIRED") {
          setError("هذا الحساب لا يحمل صلاحية الإدارة.");
        } else {
          setError("البريد أو كلمة المرور غير صحيحة.");
        }
        return;
      }

      const destination = adminIntent ? "/owner/" : payload.redirect || "/portal/command-center/";
      setMessage("تم قبول الحساب. جارٍ فتح الصفحة…");
      location.replace(destination);
    } catch {
      setError("تعذر الاتصال بخدمة الدخول. أعد المحاولة.");
    } finally {
      setBusy(false);
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    void authenticate(initialAdmin);
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <a className="brand-mark" href="/" aria-label="NDSP">N</a>
        <div className="brand">NDSP</div>
        <div className="top-actions">
          <a href="/" className="nav-button">الرئيسية</a>
          <button type="button" className="nav-button">EN</button>
        </div>
      </header>

      <main className="content">
        <section className="auth-card" aria-labelledby="login-title">
          <div className="eyebrow">الوصول الآمن</div>
          <h1 id="login-title">تسجيل الدخول</h1>
          <p className="lead">ادخل إلى حسابك للوصول إلى بوابة المستخدم وغرفة القرار.</p>

          <form onSubmit={submit} noValidate>
            <label htmlFor="email">البريد الإلكتروني</label>
            <input
              id="email"
              type="email"
              autoComplete="username"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="name@example.com"
              dir="ltr"
              disabled={busy}
            />

            <label htmlFor="password">كلمة المرور</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="أدخل كلمة المرور"
              disabled={busy}
            />

            <div className="form-row">
              <label className="remember">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(event) => setRemember(event.target.checked)}
                />
                <span>تذكرني</span>
              </label>
              <a href="/forgot-password/">نسيت كلمة المرور؟</a>
            </div>

            {error && <div className="notice error" role="alert">{error}</div>}
            {message && <div className="notice success" role="status">{message}</div>}

            <div className="login-actions" data-ndsp-owner-actions-v2="integrated-form-actions">
              <button type="submit" className="primary" disabled={busy}>
              {busy ? "جارٍ التحقق…" : "دخول آمن"}
            </button>

              <button
              type="button"
              className="owner-button"
              disabled={busy}
              onClick={() => void authenticate(true)}
            
              data-ndsp-owner-login-source-v1="1"
            >
              <span className="owner-icon">N</span>
              دخول لوحة المالك
            </button>
            </div>
          </form>

          <div className="new-account">
            <span>ليس لديك حساب؟</span>
            <a href="/register/">ابدأ التجربة</a>
          </div>
        </section>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode><App /></React.StrictMode>
);
