import { List, SignIn, X } from "@phosphor-icons/react";
import { useEffect, useRef, useState } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { publicNavigation } from "../data";
import { Brand } from "./Brand";

export function PublicLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const location = useLocation();
  const auth = useAuth();
  const accountPath = auth.isAdmin ? "/admin/cot/overview" : auth.status === "authenticated" ? "/analysis" : "/login";
  const accountLabel = auth.isAdmin ? "لوحة الإدارة" : auth.status === "authenticated" ? "الحساب" : "تسجيل الدخول";

  useEffect(() => {
    setMenuOpen(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [location.pathname]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 18);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (!menuOpen) return undefined;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.setTimeout(() => closeButtonRef.current?.focus(), 0);

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
        menuButtonRef.current?.focus();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [menuOpen]);

  const closeMenu = () => {
    setMenuOpen(false);
    window.setTimeout(() => menuButtonRef.current?.focus(), 0);
  };

  return (
    <div className="public-shell" dir="rtl">
      <header className={`public-header ${scrolled ? "public-header--scrolled" : ""}`}>
        <div className="container public-header__inner">
          <NavLink to="/" aria-label="العودة إلى الرئيسية" className="public-header__brand">
            <Brand compact />
          </NavLink>

          <nav className="public-nav public-nav--desktop" aria-label="التنقل العام">
            {publicNavigation.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="public-header__actions">
            <NavLink className="button button--outline button--small public-header__signin" to={accountPath}>
              <SignIn size={18} aria-hidden="true" />
              {accountLabel}
            </NavLink>
            <button
              ref={menuButtonRef}
              className="icon-button public-header__menu"
              type="button"
              aria-label="فتح القائمة"
              aria-expanded={menuOpen}
              aria-controls="public-mobile-menu"
              onClick={() => setMenuOpen(true)}
            >
              <List size={24} />
            </button>
          </div>
        </div>
      </header>

      {menuOpen && (
        <div className="mobile-menu-layer" role="presentation">
          <button
            className="mobile-menu-backdrop"
            type="button"
            aria-label="إغلاق القائمة"
            onClick={closeMenu}
          />
          <aside
            id="public-mobile-menu"
            className="mobile-menu"
            role="dialog"
            aria-modal="true"
            aria-label="قائمة التنقل"
          >
            <div className="mobile-menu__header">
              <Brand compact />
              <button
                ref={closeButtonRef}
                className="icon-button mobile-menu__close"
                type="button"
                onClick={closeMenu}
                aria-label="إغلاق القائمة"
              >
                <X size={24} />
              </button>
            </div>

            <div className="mobile-menu__notice">
              <strong>NDSP</strong>
              <span>منصة دعم القرار — تجربة مؤسسية محكومة وقابلة للتفسير.</span>
            </div>

            <nav className="mobile-menu__nav" aria-label="تنقل الجوال">
              <span className="mobile-menu__section-label">التنقل</span>
              {publicNavigation.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) => (isActive ? "active" : undefined)}
                  onClick={closeMenu}
                >
                  {item.label}
                </NavLink>
              ))}

              <span className="mobile-menu__section-label">الحساب</span>
              <NavLink to={accountPath} onClick={closeMenu}>
                {accountLabel}
              </NavLink>
            </nav>

            <div className="mobile-menu__footer">
              <NavLink className="button button--primary button--wide" to="/register" onClick={closeMenu}>
                ابدأ تجربة Elite لمدة 16 يومًا
              </NavLink>
              <small>دون بطاقة دفع · دون خصم تلقائي</small>
            </div>
          </aside>
        </div>
      )}

      <main id="main-content">
        <Outlet />
      </main>

      <footer className="public-footer">
        <div className="container public-footer__inner">
          <Brand compact />
          <div className="public-footer__copy">
            <p>NDSP منصة دعم قرار تفسيرية. لا تنفذ صفقات ولا تقدم أوامر تداول.</p>
            <span>النتائج العامة تقتصر على CORE الرسمي المصرح به.</span>
          </div>
          <span dir="ltr">© 2026 NDSP</span>
        </div>
      </footer>
    </div>
  );
}
