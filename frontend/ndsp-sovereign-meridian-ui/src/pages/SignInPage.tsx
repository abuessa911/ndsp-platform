import {
  ArrowLeft,
  ArrowRight,
  CheckCircle,
  EnvelopeSimple,
  Key,
  LockKey,
  ShieldCheck,
} from "@phosphor-icons/react";
import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import {
  authErrorMessage,
  internalClientPath,
  login,
  verifyTwoFactor,
} from "../api/auth";
import type { AuthUser, LoginResult } from "../api/auth";
import { useAuth } from "../auth/AuthContext";
import { Brand } from "../components/Brand";

type SignInStage = "credentials" | "two-factor";

function destinationForUser(
  user: AuthUser | null,
  requestedReturn: string | null,
  backendRedirect: string | null,
): string {
  const safeBackendRedirect = internalClientPath(backendRedirect);
  if (user?.isAdmin) {
    if (requestedReturn?.startsWith("/admin/cot")) return requestedReturn;
    if (safeBackendRedirect?.startsWith("/admin/cot")) return safeBackendRedirect;
    return "/admin/cot/overview";
  }

  if (
    safeBackendRedirect &&
    /^\/(analysis|methodology|documentation)(?:[/?#]|$)/.test(safeBackendRedirect)
  ) {
    return safeBackendRedirect;
  }
  return "/analysis";
}

export function SignInPage() {
  const auth = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const requestedReturn = internalClientPath(searchParams.get("returnTo"));
  const trialIntent = searchParams.get("intent") === "elite-trial";
  const [stage, setStage] = useState<SignInStage>("credentials");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [challengeToken, setChallengeToken] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [complete, setComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    if (auth.status !== "authenticated") return;
    navigate(destinationForUser(auth.user, requestedReturn, null), { replace: true });
  }, [auth.status, auth.user, navigate, requestedReturn]);

  const finishAuthentication = async (result: LoginResult) => {
    if (result.setupRequired && !result.authenticated) {
      setNotice(
        result.message ??
          "يلزم إكمال إعداد التحقق بخطوتين من مسار الحساب المعتمد قبل فتح لوحة الإدارة.",
      );
      return;
    }

    const session = await auth.refresh();
    if (!session.authenticated) {
      throw new Error("SESSION_NOT_ESTABLISHED");
    }

    setComplete(true);
    navigate(destinationForUser(session.user, requestedReturn, result.redirect), { replace: true });
  };

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setNotice(null);

    try {
      const result =
        stage === "credentials"
          ? await login(email.trim(), password)
          : await verifyTwoFactor({
              email: email.trim(),
              code: code.trim(),
              challengeToken,
            });

      if (result.twoFactorRequired && !result.authenticated) {
        setChallengeToken(result.challengeToken);
        setStage("two-factor");
        setNotice(result.message ?? "أدخل رمز التحقق لإكمال تسجيل الدخول.");
        return;
      }

      await finishAuthentication(result);
    } catch (requestError) {
      const message =
        requestError instanceof Error && requestError.message === "SESSION_NOT_ESTABLISHED"
          ? "تم قبول الطلب، لكن لم تُنشأ جلسة صالحة. تحقق من إعدادات Cookie وNginx."
          : authErrorMessage(requestError);
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  const returnToCredentials = () => {
    setStage("credentials");
    setCode("");
    setChallengeToken(null);
    setError(null);
    setNotice(null);
  };

  return (
    <section className="sign-in-page">
      <div className="sign-in-panel">
        <Brand />
        <div className="sign-in-panel__message">
          <span className="eyebrow">SECURE ACCOUNT ACCESS</span>
          <h1>مساحة قرار محكومة</h1>
          <p>الدخول متصل بخدمة المصادقة الفعلية، والجلسة تُتحقق قبل فتح أي مسار إداري.</p>
        </div>
        <div className="sign-in-panel__proof">
          <ShieldCheck size={22} />
          <span>الجلسة عبر Cookie آمنة ولا تُحفظ كلمة المرور داخل الواجهة</span>
        </div>
      </div>

      <div className="sign-in-form-wrap">
        <form className="sign-in-form" onSubmit={submit}>
          <span className="eyebrow">
            {stage === "two-factor" ? "TWO-FACTOR VERIFICATION" : "WELCOME BACK"}
          </span>
          <h2>{stage === "two-factor" ? "رمز التحقق" : "تسجيل الدخول"}</h2>
          <p>
            {stage === "two-factor"
              ? "أدخل الرمز الصادر من وسيلة التحقق المرتبطة بحسابك."
              : trialIntent
                ? "سجّل الدخول إلى حساب التجربة المعتمد."
                : "استخدم بريد الحساب وكلمة المرور للوصول الآمن."}
          </p>

          {stage === "credentials" ? (
            <>
              <label>
                <span>البريد الإلكتروني</span>
                <div className="input-with-icon">
                  <EnvelopeSimple size={18} />
                  <input
                    type="email"
                    required
                    autoComplete="username"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="name@example.com"
                    dir="ltr"
                  />
                </div>
              </label>
              <label>
                <span>كلمة المرور</span>
                <div className="input-with-icon">
                  <LockKey size={18} />
                  <input
                    type="password"
                    required
                    minLength={6}
                    autoComplete="current-password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="••••••••••••"
                    dir="ltr"
                  />
                </div>
              </label>
            </>
          ) : (
            <label>
              <span>رمز التحقق</span>
              <div className="input-with-icon">
                <Key size={18} />
                <input
                  type="text"
                  required
                  minLength={6}
                  maxLength={10}
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  value={code}
                  onChange={(event) => setCode(event.target.value.replace(/\D/g, ""))}
                  placeholder="000000"
                  dir="ltr"
                />
              </div>
            </label>
          )}

          {error ? <div className="auth-message auth-message--error" role="alert">{error}</div> : null}
          {notice ? <div className="auth-message auth-message--notice" role="status">{notice}</div> : null}

          <div className="sign-in-options">
            {stage === "two-factor" ? (
              <button type="button" onClick={returnToCredentials}>
                <ArrowRight size={14} /> العودة إلى بيانات الدخول
              </button>
            ) : (
              <Link to="/forgot-password">نسيت كلمة المرور؟</Link>
            )}
            <Link to="/">العودة للرئيسية</Link>
          </div>

          <button className="button button--primary button--wide" type="submit" disabled={submitting || complete}>
            {complete ? (
              <><CheckCircle size={18} weight="fill" /> تم التحقق</>
            ) : submitting ? (
              "جارٍ التحقق..."
            ) : stage === "two-factor" ? (
              <>تأكيد الرمز <ArrowLeft size={18} /></>
            ) : (
              <>تسجيل الدخول <ArrowLeft size={18} /></>
            )}
          </button>
          <small>لا تتضمن هذه الحزمة مفاتيح API أو كلمات مرور أو أسرار خادم.</small>
        </form>
      </div>
    </section>
  );
}
