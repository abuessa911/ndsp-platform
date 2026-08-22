import {
  ArrowLeft,
  CheckCircle,
  EnvelopeSimple,
  LockKey,
  ShieldCheck,
} from "@phosphor-icons/react";
import { useState } from "react";
import type { FormEvent, ReactNode } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  authErrorMessage,
  requestPasswordReset,
  resetPassword,
} from "../api/auth";
import { Brand } from "../components/Brand";

function RecoveryShell({ children }: { children: ReactNode }) {
  return (
    <section className="sign-in-page">
      <div className="sign-in-panel">
        <Brand />
        <div className="sign-in-panel__message">
          <span className="eyebrow">ACCOUNT RECOVERY</span>
          <h1>استعادة آمنة للحساب</h1>
          <p>تتم العملية عبر خدمة الاستعادة الفعلية، دون كشف وجود الحساب أو تفاصيله.</p>
        </div>
        <div className="sign-in-panel__proof">
          <ShieldCheck size={22} />
          <span>الرمز مؤقت ويُتحقق منه في الخادم</span>
        </div>
      </div>
      <div className="sign-in-form-wrap">{children}</div>
    </section>
  );
}

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [complete, setComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await requestPasswordReset(email.trim());
      setComplete(true);
    } catch (requestError) {
      setError(authErrorMessage(requestError));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <RecoveryShell>
      <form className="sign-in-form" onSubmit={submit}>
        <span className="eyebrow">FORGOT PASSWORD</span>
        <h2>استعادة كلمة المرور</h2>
        <p>أدخل بريد الحساب، وسنرسل تعليمات الاستعادة إذا كان الحساب مؤهلًا.</p>
        {complete ? (
          <div className="auth-message auth-message--success" role="status">
            <CheckCircle size={18} weight="fill" />
            إذا كان البريد مسجلًا فستصلك تعليمات الاستعادة.
          </div>
        ) : (
          <label>
            <span>البريد الإلكتروني</span>
            <div className="input-with-icon">
              <EnvelopeSimple size={18} />
              <input
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="name@example.com"
                dir="ltr"
              />
            </div>
          </label>
        )}
        {error ? <div className="auth-message auth-message--error" role="alert">{error}</div> : null}
        {!complete ? (
          <button className="button button--primary button--wide" type="submit" disabled={submitting}>
            {submitting ? "جارٍ الإرسال..." : <>إرسال تعليمات الاستعادة <ArrowLeft size={18} /></>}
          </button>
        ) : null}
        <small><Link to="/login">العودة إلى تسجيل الدخول</Link></small>
      </form>
    </RecoveryShell>
  );
}

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token")?.trim() ?? "";
  const email = searchParams.get("email")?.trim() || null;
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [complete, setComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    if (!token) {
      setError("رابط الاستعادة لا يحتوي رمزًا صالحًا.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("كلمتا المرور غير متطابقتين.");
      return;
    }

    setSubmitting(true);
    try {
      await resetPassword({ email, newPassword, token });
      setComplete(true);
    } catch (requestError) {
      setError(authErrorMessage(requestError));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <RecoveryShell>
      <form className="sign-in-form" onSubmit={submit}>
        <span className="eyebrow">RESET PASSWORD</span>
        <h2>تعيين كلمة مرور جديدة</h2>
        <p>اختر كلمة مرور قوية ومختلفة عن كلمات المرور السابقة.</p>
        {complete ? (
          <div className="auth-message auth-message--success" role="status">
            <CheckCircle size={18} weight="fill" /> تم تحديث كلمة المرور بنجاح.
          </div>
        ) : (
          <>
            <label>
              <span>كلمة المرور الجديدة</span>
              <div className="input-with-icon">
                <LockKey size={18} />
                <input
                  type="password"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  value={newPassword}
                  onChange={(event) => setNewPassword(event.target.value)}
                  dir="ltr"
                />
              </div>
            </label>
            <label>
              <span>تأكيد كلمة المرور</span>
              <div className="input-with-icon">
                <LockKey size={18} />
                <input
                  type="password"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  dir="ltr"
                />
              </div>
            </label>
          </>
        )}
        {error ? <div className="auth-message auth-message--error" role="alert">{error}</div> : null}
        {!complete ? (
          <button className="button button--primary button--wide" type="submit" disabled={submitting || !token}>
            {submitting ? "جارٍ التحديث..." : <>تحديث كلمة المرور <ArrowLeft size={18} /></>}
          </button>
        ) : null}
        <small><Link to="/login">العودة إلى تسجيل الدخول</Link></small>
      </form>
    </RecoveryShell>
  );
}
