import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import ar from "./locales/ar";
import en from "./locales/en";
import fr from "./locales/fr";
import es from "./locales/es";
import de from "./locales/de";
import zh from "./locales/zh";
import hi from "./locales/hi";
import pt from "./locales/pt";
import ru from "./locales/ru";
import ja from "./locales/ja";
import ko from "./locales/ko";
import it from "./locales/it";
import nl from "./locales/nl";
import tr from "./locales/tr";
import pl from "./locales/pl";
import sv from "./locales/sv";
import id from "./locales/id";
import ms from "./locales/ms";
import th from "./locales/th";
import vi from "./locales/vi";
import ur from "./locales/ur";
import fa from "./locales/fa";
import bn from "./locales/bn";
import ro from "./locales/ro";
import hu from "./locales/hu";
import cs from "./locales/cs";
import el from "./locales/el";
import uk from "./locales/uk";
import sw from "./locales/sw";

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ar: { translation: ar },
      en: { translation: en },
      fr: { translation: fr },
      es: { translation: es },
      de: { translation: de },
      zh: { translation: zh },
      hi: { translation: hi },
      pt: { translation: pt },
      ru: { translation: ru },
      ja: { translation: ja },
      ko: { translation: ko },
      it: { translation: it },
      nl: { translation: nl },
      tr: { translation: tr },
      pl: { translation: pl },
      sv: { translation: sv },
      id: { translation: id },
      ms: { translation: ms },
      th: { translation: th },
      vi: { translation: vi },
      ur: { translation: ur },
      fa: { translation: fa },
      bn: { translation: bn },
      ro: { translation: ro },
      hu: { translation: hu },
      cs: { translation: cs },
      el: { translation: el },
      uk: { translation: uk },
      sw: { translation: sw },
    },
    fallbackLng: "en",
    defaultNS: "translation",
    detection: {
      order: ["localStorage", "navigator"],
      caches: ["localStorage"],
    },
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;

export const LANGUAGES = [
  { code: "ar", name: "العربية", dir: "rtl", flag: "🇸🇦" },
  { code: "en", name: "English", dir: "ltr", flag: "🇺🇸" },
  { code: "fr", name: "Français", dir: "ltr", flag: "🇫🇷" },
  { code: "es", name: "Español", dir: "ltr", flag: "🇪🇸" },
  { code: "de", name: "Deutsch", dir: "ltr", flag: "🇩🇪" },
  { code: "zh", name: "中文", dir: "ltr", flag: "🇨🇳" },
  { code: "hi", name: "हिन्दी", dir: "ltr", flag: "🇮🇳" },
  { code: "pt", name: "Português", dir: "ltr", flag: "🇵🇹" },
  { code: "ru", name: "Русский", dir: "ltr", flag: "🇷🇺" },
  { code: "ja", name: "日本語", dir: "ltr", flag: "🇯🇵" },
  { code: "ko", name: "한국어", dir: "ltr", flag: "🇰🇷" },
  { code: "it", name: "Italiano", dir: "ltr", flag: "🇮🇹" },
  { code: "nl", name: "Nederlands", dir: "ltr", flag: "🇳🇱" },
  { code: "tr", name: "Türkçe", dir: "ltr", flag: "🇹🇷" },
  { code: "pl", name: "Polski", dir: "ltr", flag: "🇵🇱" },
  { code: "sv", name: "Svenska", dir: "ltr", flag: "🇸🇪" },
  { code: "id", name: "Bahasa Indonesia", dir: "ltr", flag: "🇮🇩" },
  { code: "ms", name: "Bahasa Melayu", dir: "ltr", flag: "🇲🇾" },
  { code: "th", name: "ภาษาไทย", dir: "ltr", flag: "🇹🇭" },
  { code: "vi", name: "Tiếng Việt", dir: "ltr", flag: "🇻🇳" },
  { code: "ur", name: "اردو", dir: "rtl", flag: "🇵🇰" },
  { code: "fa", name: "فارسی", dir: "rtl", flag: "🇮🇷" },
  { code: "bn", name: "বাংলা", dir: "ltr", flag: "🇧🇩" },
  { code: "ro", name: "Română", dir: "ltr", flag: "🇷🇴" },
  { code: "hu", name: "Magyar", dir: "ltr", flag: "🇭🇺" },
  { code: "cs", name: "Čeština", dir: "ltr", flag: "🇨🇿" },
  { code: "el", name: "Ελληνικά", dir: "ltr", flag: "🇬🇷" },
  { code: "uk", name: "Українська", dir: "ltr", flag: "🇺🇦" },
  { code: "sw", name: "Kiswahili", dir: "ltr", flag: "🇰🇪" },
];
