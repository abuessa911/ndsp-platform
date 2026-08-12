import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  ar: {
    translation: {
      platform: "منصة دعم القرار",
      foundation: "الأساس التشغيلي للواجهة",
      ready: "جاهز",
      language: "English"
    }
  },
  en: {
    translation: {
      platform: "Decision Support Platform",
      foundation: "Interface foundation",
      ready: "Ready",
      language: "العربية"
    }
  }
};

void i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "ar",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  });

export function applyDocumentLanguage(language: string) {
  const lang = language === "en" ? "en" : "ar";

  document.documentElement.lang = lang;
  document.documentElement.dir =
    lang === "ar" ? "rtl" : "ltr";
}

applyDocumentLanguage(i18n.language);

i18n.on("languageChanged", applyDocumentLanguage);

export default i18n;
