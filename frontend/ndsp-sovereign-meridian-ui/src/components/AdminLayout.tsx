import {
  ArrowsLeftRight,
  Bell,
  BracketsCurly,
  CalendarBlank,
  ChartLineUp,
  Command,
  FileText,
  Flask,
  GearSix,
  House,
  List,
  MagnifyingGlass,
  Scroll,
  ShieldCheck,
  SignOut,
  X,
} from "@phosphor-icons/react";
import type { Icon } from "@phosphor-icons/react";
import { useEffect, useRef, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { adminNavigation } from "../data";
import { Brand } from "./Brand";
import { StatusChip } from "./StatusChip";

const iconMap: Record<string, Icon> = {
  overview: House,
  reports: FileText,
  calendar: CalendarBlank,
  experiments: Flask,
  compare: ArrowsLeftRight,
  governance: ShieldCheck,
  audit: Scroll,
  contracts: BracketsCurly,
  settings: GearSix,
};

const pageMeta: Record<string, { eyebrow: string; title: string; description: string }> = {
  overview: { eyebrow: "COT GOVERNANCE", title: "الملخص التنفيذي", description: "نظرة عامة على الاتجاه الرسمي والأدلة المتاحة" },
  reports: { eyebrow: "REPORTS", title: "تقارير COT", description: "تقارير CORE ونتائج SHADOW للمراجعة الداخلية" },
  "daily-control": { eyebrow: "DAY CONTROL", title: "التحكم اليومي", description: "إدارة الأسبوع الفعّال وسياسة توقيت التوقيت العالمي" },
  experiments: { eyebrow: "SHADOW MODE", title: "التجارب", description: "اختبارات EXPANDED المعزولة عن المسار العام" },
  comparisons: { eyebrow: "COMPARISONS", title: "المقارنات", description: "مقارنة النسخ وقياس مواضع الاتفاق والاختلاف" },
  governance: { eyebrow: "GOVERNANCE", title: "طلبات الحوكمة", description: "سجل الترقيات والاعتمادات وحدود الأثر" },
  "audit-logs": { eyebrow: "AUDIT", title: "سجل التدقيق", description: "أثر غير قابل للالتباس لكل تعديل وتشغيل" },
  contracts: { eyebrow: "API CONTRACTS", title: "العقود", description: "حدود Public API والعقود الداخلية" },
  settings: { eyebrow: "SYSTEM", title: "الإعدادات", description: "الخدمات والسياسات والصلاحيات التشغيلية" },
};

export function AdminLayout() {
  const auth = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [signOutBusy, setSignOutBusy] = useState(false);
  const [signOutError, setSignOutError] = useState<string | null>(null);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const location = useLocation();
  const key = location.pathname.split("/").filter(Boolean).at(-1) ?? "overview";
  const meta = pageMeta[key] ?? pageMeta.overview;
  const userIdentity = auth.user?.name ?? auth.user?.email ?? "Admin";
  const avatarText = userIdentity.replace(/[^\p{L}\p{N}]/gu, "").slice(0, 2).toUpperCase() || "AD";

  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!sidebarOpen) return undefined;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.setTimeout(() => closeButtonRef.current?.focus(), 0);

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSidebarOpen(false);
        menuButtonRef.current?.focus();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [sidebarOpen]);

  const closeSidebar = () => {
    setSidebarOpen(false);
    window.setTimeout(() => menuButtonRef.current?.focus(), 0);
  };

  const handleSignOut = async () => {
    setSignOutBusy(true);
    setSignOutError(null);
    try {
      await auth.signOut();
      navigate("/login", { replace: true });
    } catch {
      setSignOutError("تعذر إنهاء الجلسة. حاول مرة أخرى.");
    } finally {
      setSignOutBusy(false);
    }
  };

  return (
    <div className="admin-shell" dir="rtl">
      {sidebarOpen && (
        <button
          className="admin-sidebar-backdrop"
          type="button"
          aria-label="إغلاق القائمة"
          onClick={closeSidebar}
        />
      )}
      <aside className={`admin-sidebar ${sidebarOpen ? "admin-sidebar--open" : ""}`}>
        <div className="admin-sidebar__brand">
          <Brand compact />
          <button ref={closeButtonRef} className="icon-button admin-sidebar__close" type="button" onClick={closeSidebar} aria-label="إغلاق القائمة">
            <X size={20} />
          </button>
        </div>

        <nav className="admin-nav" aria-label="تنقل لوحة الإدارة">
          <span className="admin-nav__label">مساحة العمل</span>
          {adminNavigation.map((item) => {
            const IconComponent = iconMap[item.icon] ?? ChartLineUp;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                <IconComponent size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="admin-sidebar__boundary">
          <StatusChip label="CORE · OFFICIAL" tone="success" compact />
          <StatusChip label="EXPANDED · SHADOW" tone="review" compact />
          <p>Public Exposure: Disabled</p>
        </div>
      </aside>

      <div className="admin-workspace">
        <header className="admin-topbar">
          <button ref={menuButtonRef} className="icon-button admin-topbar__menu" type="button" onClick={() => setSidebarOpen(true)} aria-label="فتح القائمة">
            <List size={22} />
          </button>
          <label className="admin-search">
            <MagnifyingGlass size={18} aria-hidden="true" />
            <input aria-label="بحث شامل" placeholder="بحث شامل..." />
            <span dir="ltr"><Command size={13} /> K</span>
          </label>
          <div className="admin-topbar__status">
            <StatusChip label="جلسة موثقة" tone="success" compact />
            <button className="icon-button" type="button" aria-label="الإشعارات">
              <Bell size={19} />
            </button>
            <span className="admin-avatar" aria-label={`المستخدم الحالي: ${userIdentity}`} title={userIdentity}>{avatarText}</span>
            <button
              className="icon-button"
              type="button"
              aria-label="تسجيل الخروج"
              title={signOutError ?? "تسجيل الخروج"}
              disabled={signOutBusy}
              onClick={() => void handleSignOut()}
            >
              <SignOut size={19} />
            </button>
          </div>
        </header>

        <section className="admin-page-heading">
          <div>
            <span className="eyebrow">{meta.eyebrow}</span>
            <h1>{meta.title}</h1>
            <p>{meta.description}</p>
          </div>
          <StatusChip label="آخر تحديث 08:34 التوقيت العالمي" tone="info" />
        </section>

        <main className="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
