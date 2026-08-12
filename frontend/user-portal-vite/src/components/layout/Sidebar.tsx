import { X } from "lucide-react";
import { useTranslation } from "react-i18next";

import {
  isNavigationActive,
  primaryNavigation,
  secondaryNavigation
} from "../../config/navigation";

import { Brand } from "./Brand";

type Props = {
  pathname: string;
  mobileOpen: boolean;
  onMobileClose: () => void;
};

export function Sidebar({
  pathname,
  mobileOpen,
  onMobileClose
}: Props) {
  const { i18n } = useTranslation();
  const isArabic = i18n.language !== "en";

  const renderItems = (
    items: typeof primaryNavigation
  ) =>
    items.map((item) => {
      const Icon = item.icon;
      const active = isNavigationActive(
        pathname,
        item.href
      );

      return (
        <a
          key={item.id}
          href={item.href}
          className={
            active
              ? "ndsp-nav-item ndsp-nav-item--active"
              : "ndsp-nav-item"
          }
          aria-current={active ? "page" : undefined}
          onClick={onMobileClose}
        >
          <Icon size={18} strokeWidth={1.8} />
          <span>
            {isArabic ? item.labelAr : item.labelEn}
          </span>
        </a>
      );
    });

  return (
    <>
      <aside
        className={
          mobileOpen
            ? "ndsp-sidebar ndsp-sidebar--open"
            : "ndsp-sidebar"
        }
      >
        <div className="ndsp-sidebar__header">
          <Brand />

          <button
            type="button"
            className="ndsp-icon-button ndsp-sidebar__close"
            onClick={onMobileClose}
            aria-label={isArabic ? "إغلاق" : "Close"}
          >
            <X size={20} />
          </button>
        </div>

        <nav
          className="ndsp-sidebar__nav"
          aria-label={
            isArabic
              ? "التنقل الرئيسي"
              : "Primary navigation"
          }
        >
          <div className="ndsp-nav-group">
            {renderItems(primaryNavigation)}
          </div>

          <div className="ndsp-sidebar__separator" />

          <div className="ndsp-nav-group ndsp-nav-group--secondary">
            {renderItems(secondaryNavigation)}
          </div>
        </nav>

        <div className="ndsp-sidebar__footer">
          <span className="ndsp-status-dot" />
          <div>
            <strong>
              {isArabic ? "النظام متصل" : "System online"}
            </strong>
            <span>
              {isArabic
                ? "بيانات القرار متاحة"
                : "Decision data available"}
            </span>
          </div>
        </div>
      </aside>

      {mobileOpen && (
        <button
          type="button"
          className="ndsp-sidebar-backdrop"
          onClick={onMobileClose}
          aria-label={isArabic ? "إغلاق القائمة" : "Close menu"}
        />
      )}
    </>
  );
}
