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

const navigationItems = [
  { label: "الرئيسية", href: "/" },
  { label: "نظرة عامة", href: "/overview" },
  { label: "CORE", href: "/core" },
  { label: "السياق", href: "/market-context" },
  { label: "الأدلة", href: "/evidence" },
  { label: "المنهجية", href: "/methodology" },
]

export function PublicHeader() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <>
      <header className="sovereign-header">
        <div className="sovereign-header__inner">
          <NdspLogo />

          <nav
            className="sovereign-header__nav"
            aria-label="التنقل الرئيسي"
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
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="sovereign-header__actions">
            <button
              className="sovereign-language"
              type="button"
              aria-label="Switch to English"
            >
              EN
            </button>

            <NavLink
              className="sovereign-login"
              to="/account"
            >
              <UserRound size={17} strokeWidth={1.5} />
              <span>تسجيل الدخول</span>
            </NavLink>
          </div>

          <button
            className="sovereign-mobile-trigger"
            type="button"
            aria-label="فتح القائمة"
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
              {item.label}
            </NavLink>
          ))}

          <NavLink
            className="sovereign-mobile-panel__login"
            to="/account"
            onClick={() => setMobileOpen(false)}
          >
            تسجيل الدخول
          </NavLink>
        </div>
      )}
    </>
  )
}
