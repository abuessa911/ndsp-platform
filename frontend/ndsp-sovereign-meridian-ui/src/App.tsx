import { ArrowRight } from "@phosphor-icons/react";
import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { RequireAdmin } from "./auth/RequireAdmin";
import { AdminLayout } from "./components/AdminLayout";
import { PublicLayout } from "./components/PublicLayout";
import { AnalysisPage } from "./pages/AnalysisPage";
import { DocumentationPage } from "./pages/DocumentationPage";
import { HomePage } from "./pages/HomePage";
import { MethodologyPage } from "./pages/MethodologyPage";
import { ForgotPasswordPage, ResetPasswordPage } from "./pages/AccountRecoveryPage";
import { SignInPage } from "./pages/SignInPage";
import { RegisterPage } from "./pages/RegisterPage";
import {
  AdminExperimentsPage,
  AdminGenericPage,
  AdminGovernancePage,
  AdminOverviewPage,
  AdminReportsPage,
  AdminSettingsPage,
} from "./pages/admin/AdminPages";

function NotFoundPage() {
  return (
    <section className="not-found-page" dir="rtl">
      <span className="eyebrow">404</span>
      <h1>هذه الصفحة غير موجودة</h1>
      <p>قد يكون الرابط تغير أو لم يعد متاحًا.</p>
      <Link className="button button--primary" to="/">العودة للرئيسية <ArrowRight size={17} /></Link>
    </section>
  );
}

function DomainRootPage() {
  const hostname = window.location.hostname.toLowerCase();
  if (hostname === "my.ndsp.app") return <Navigate to="/login" replace />;
  if (hostname === "admin.ndsp.app") return <Navigate to="/admin/cot/overview" replace />;
  return <HomePage />;
}

function LegacySignInRedirect() {
  const location = useLocation();
  return <Navigate to={`/login${location.search}${location.hash}`} replace />;
}

export function App() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route index element={<DomainRootPage />} />
        <Route path="methodology" element={<MethodologyPage />} />
        <Route path="analysis" element={<AnalysisPage />} />
        <Route path="documentation" element={<DocumentationPage />} />
      </Route>

      <Route path="register" element={<RegisterPage />} />
      <Route path="login" element={<SignInPage />} />
      <Route path="sign-in" element={<LegacySignInRedirect />} />
      <Route path="forgot-password" element={<ForgotPasswordPage />} />
      <Route path="reset-password" element={<ResetPasswordPage />} />

      <Route element={<RequireAdmin />}>
        <Route path="admin/cot" element={<AdminLayout />}>
          <Route index element={<Navigate to="overview" replace />} />
          <Route path="overview" element={<AdminOverviewPage />} />
          <Route path="reports" element={<AdminReportsPage />} />
          <Route path="daily-control" element={<AdminGenericPage />} />
          <Route path="experiments" element={<AdminExperimentsPage />} />
          <Route path="comparisons" element={<AdminGenericPage />} />
          <Route path="governance" element={<AdminGovernancePage />} />
          <Route path="audit-logs" element={<AdminGenericPage />} />
          <Route path="contracts" element={<AdminGenericPage />} />
          <Route path="settings" element={<AdminSettingsPage />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
