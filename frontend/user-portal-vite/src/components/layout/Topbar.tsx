import {
  Bell,
  Languages,
  Menu,
  Search
} from "lucide-react";

import { useTranslation } from "react-i18next";

type Props = {
  onMenuOpen: () => void;
};

export function Topbar({ onMenuOpen }: Props) {
  const { i18n } = useTranslation();
  const isArabic = i18n.language !== "en";

  const toggleLanguage = async () => {
    await i18n.changeLanguage(
      isArabic ? "en" : "ar"
    );
  };

  return (
    <header className="ndsp-topbar">
      <div className="ndsp-topbar__start">
        <button
          type="button"
          className="ndsp-icon-button ndsp-mobile-menu"
          onClick={onMenuOpen}
          aria-label={
            isArabic ? "فتح القائمة" : "Open menu"
          }
        >
          <Menu size={21} />
        </button>

        <div className="ndsp-topbar__context">
          <span className="ndsp-topbar__eyebrow">
            {isArabic
              ? "منصة دعم القرار"
              : "Decision Support Platform"}
          </span>
          <strong>
            {isArabic
              ? "مساحة القرار"
              : "Decision Workspace"}
          </strong>
        </div>
      </div>

      <div className="ndsp-topbar__actions">
        <button
          type="button"
          className="ndsp-icon-button"
          aria-label={isArabic ? "بحث" : "Search"}
          title={isArabic ? "بحث" : "Search"}
        >
          <Search size={19} />
        </button>

        <button
          type="button"
          className="ndsp-icon-button"
          aria-label={
            isArabic ? "الإشعارات" : "Notifications"
          }
          title={
            isArabic ? "الإشعارات" : "Notifications"
          }
        >
          <Bell size={19} />
        </button>

        <button
          type="button"
          className="ndsp-language-button"
          onClick={toggleLanguage}
        >
          <Languages size={18} />
          <span>{isArabic ? "EN" : "AR"}</span>
        </button>

        <div
          className="ndsp-user-avatar"
          aria-label={isArabic ? "الحساب" : "Account"}
        >
          N
        </div>
      </div>
    </header>
  );
}
