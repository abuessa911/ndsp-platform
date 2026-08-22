import {
  BarChart3,
  BriefcaseBusiness,
  CircleUserRound,
  Command,
  FileText,
  History,
  Home,
  Settings
} from "lucide-react";

export type NavigationItem = {
  id: string;
  labelAr: string;
  labelEn: string;
  href: string;
  icon: typeof Home;
};

export const primaryNavigation: NavigationItem[] = [
  {
    id: "home",
    labelAr: "الرئيسية",
    labelEn: "Home",
    href: "/portal/",
    icon: Home
  },
  {
    id: "command",
    labelAr: "مركز القرار",
    labelEn: "Decision Center",
    href: "/portal/command",
    icon: Command
  },
  {
    id: "markets",
    labelAr: "الأسواق",
    labelEn: "Markets",
    href: "/portal/asset",
    icon: BarChart3
  },
  {
    id: "brief",
    labelAr: "الموجز",
    labelEn: "Brief",
    href: "/portal/brief",
    icon: FileText
  },
  {
    id: "completed",
    labelAr: "القرارات المكتملة",
    labelEn: "Completed Decisions",
    href: "/portal/completed",
    icon: History
  }
];

export const secondaryNavigation: NavigationItem[] = [
  {
    id: "portfolio",
    labelAr: "مساحة العمل",
    labelEn: "Workspace",
    href: "/portal/",
    icon: BriefcaseBusiness
  },
  {
    id: "account",
    labelAr: "الحساب",
    labelEn: "Account",
    href: "/portal/settings",
    icon: CircleUserRound
  },
  {
    id: "settings",
    labelAr: "الإعدادات",
    labelEn: "Settings",
    href: "/portal/settings",
    icon: Settings
  }
];

export function isNavigationActive(
  pathname: string,
  href: string
): boolean {
  if (href === "/portal/") {
    return pathname === "/portal" || pathname === "/portal/";
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}
