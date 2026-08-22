import { useState } from "react"
import {
  Menu,
  UserRound,
  X,
} from "lucide-react"
import {
  NavLink,
} from "react-router-dom"

import { NdspLogo } from "@/components/ndsp/ndsp-logo"
import { useNdspLanguage } from "@/lib/language-context"

const navigationItems = [
  { ar: "الرئيسية", en: "Home", href: "/" },
  { ar: "نظرة عامة", en: "Overview", href: "/overview" },
  { ar: "CORE", en: "CORE", href: "/core" },
  { ar: "السياق", en: "Context", href: "/market-context" },
  { ar: "الأدلة", en: "Evidence", href: "/evidence" },
  { ar: "المنهجية", en: "Methodology", href: "/methodology" },
]

export function PublicHeader() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const { isArabic, toggleLanguage } = useNdspLanguage()

  const languageLabel = isArabic ? "EN" : "AR"
  const languageAriaLabel = isArabic
    ? "Switch to English"
    : "التبديل إلى العربية"
  const loginLabel = isArabic ? "تسجيل الدخول" : "Sign in"
  const navigationLabel = isArabic
    ? "التنقل الرئيسي"
    : "Primary navigation"
  const menuLabel = isArabic ? "فتح القائمة" : "Open menu"

  return (
    <>
      <header className="sovereign-header">
        <div className="sovereign-header__inner">
          <NdspLogo />

          <nav
            className="sovereign-header__nav"
            aria-label={navigationLabel}
          >
            {navigationItems.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                end={item.href === "/"}
                className={({ isActive }) =>
                  isActive ? "is-active" : undefined
                }
              >
                {isArabic ? item.ar : item.en}
              </NavLink>
            ))}
          </nav>

          <div className="sovereign-header__actions">
            <button
              className="sovereign-language"
              type="button"
              aria-label={languageAriaLabel}
              onClick={toggleLanguage}
            >
              {languageLabel}
            </button>

            <NavLink
              className="sovereign-login"
              to="/account"
            >
              <UserRound size={17} strokeWidth={1.5} />
              <span>{loginLabel}</span>
            </NavLink>
          </div>

          <button
            className="sovereign-mobile-trigger"
            type="button"
            aria-label={menuLabel}
            aria-expanded={mobileOpen}
            onClick={() =>
              setMobileOpen((current) => !current)
            }
          >
            {mobileOpen ? (
              <X size={23} />
            ) : (
              <Menu size={23} />
            )}
          </button>
        </div>
      </header>

      {mobileOpen && (
        <div className="sovereign-mobile-panel">
          {navigationItems.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              onClick={() => setMobileOpen(false)}
            >
              {isArabic ? item.ar : item.en}
            </NavLink>
          ))}

          <button
            className="sovereign-mobile-panel__language"
            type="button"
            aria-label={languageAriaLabel}
            onClick={toggleLanguage}
          >
            <span>{isArabic ? "English" : "العربية"}</span>
            <strong>{languageLabel}</strong>
          </button>

          <NavLink
            className="sovereign-mobile-panel__login"
            to="/account"
            onClick={() => setMobileOpen(false)}
          >
            {loginLabel}
          </NavLink>
        </div>
      )}
    </>
  )
}
