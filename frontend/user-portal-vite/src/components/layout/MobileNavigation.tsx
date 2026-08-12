import { useTranslation } from "react-i18next";

import {
  isNavigationActive,
  primaryNavigation
} from "../../config/navigation";

type Props = {
  pathname: string;
};

export function MobileNavigation({
  pathname
}: Props) {
  const { i18n } = useTranslation();
  const isArabic = i18n.language !== "en";

  const items = primaryNavigation.slice(0, 5);

  return (
    <nav
      className="ndsp-mobile-nav"
      aria-label={
        isArabic ? "التنقل السريع" : "Quick navigation"
      }
    >
      {items.map((item) => {
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
                ? "ndsp-mobile-nav__item ndsp-mobile-nav__item--active"
                : "ndsp-mobile-nav__item"
            }
          >
            <Icon size={19} strokeWidth={1.8} />
            <span>
              {isArabic ? item.labelAr : item.labelEn}
            </span>
          </a>
        );
      })}
    </nav>
  );
}
