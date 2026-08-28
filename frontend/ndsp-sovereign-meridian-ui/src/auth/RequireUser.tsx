import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";

export function RequireUser() {
  const auth = useAuth();
  const location = useLocation();

  if (auth.status === "loading") {
    return <section className="route-state" dir="rtl">جارٍ التحقق من الجلسة…</section>;
  }

  if (auth.status === "unavailable") {
    return <section className="route-state route-state--danger" dir="rtl">تعذر التحقق من الجلسة الآمنة. لا يمكن فتح مسار التحليل.</section>;
  }

  if (auth.status !== "authenticated") {
    const returnTo = `${location.pathname}${location.search}${location.hash}`;
    return <Navigate to={`/login?returnTo=${encodeURIComponent(returnTo)}`} replace />;
  }

  return <Outlet />;
}
