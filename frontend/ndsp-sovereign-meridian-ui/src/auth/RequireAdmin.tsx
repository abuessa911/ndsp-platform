import { ShieldWarning } from "@phosphor-icons/react";
import { Link, Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";

export function RequireAdmin() {
  const auth = useAuth();
  const location = useLocation();

  if (auth.status === "loading") {
    return (
      <section className="auth-state-page" dir="rtl" aria-live="polite">
        <span className="auth-spinner" aria-hidden="true" />
        <h1>جارٍ التحقق من الجلسة</h1>
        <p>يتم التحقق من صلاحية الحساب قبل فتح مساحة الإدارة.</p>
      </section>
    );
  }

  if (auth.status === "unavailable") {
    return (
      <section className="auth-state-page" dir="rtl" role="alert">
        <ShieldWarning size={38} />
        <h1>تعذر التحقق من الجلسة</h1>
        <p>{auth.error ?? "خدمة المصادقة غير متاحة مؤقتًا."}</p>
        <button className="button button--primary" type="button" onClick={() => void auth.refresh().catch(() => undefined)}>
          إعادة المحاولة
        </button>
      </section>
    );
  }

  if (auth.status === "anonymous") {
    const returnTo = `${location.pathname}${location.search}${location.hash}`;
    return <Navigate to={`/login?returnTo=${encodeURIComponent(returnTo)}`} replace />;
  }

  if (!auth.isAdmin) {
    return (
      <section className="auth-state-page" dir="rtl">
        <ShieldWarning size={38} />
        <h1>الصلاحية غير كافية</h1>
        <p>الحساب مسجّل، لكنه لا يملك صلاحية دخول لوحة الإدارة.</p>
        <Link className="button button--outline" to="/analysis">العودة إلى التحليل العام</Link>
      </section>
    );
  }

  return <Outlet />;
}
