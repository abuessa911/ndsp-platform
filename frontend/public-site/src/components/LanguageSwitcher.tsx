import { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { LANGUAGES } from "@/i18n";
import { Globe, Search, Check, ChevronDown } from "lucide-react";

export function LanguageSwitcher() {
  const { i18n, t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  const currentLang =
    LANGUAGES.find((l) => l.code === i18n.language) ||
    LANGUAGES.find((l) => i18n.language.startsWith(l.code)) ||
    LANGUAGES[1];

  const filtered = LANGUAGES.filter(
    (l) =>
      l.name.toLowerCase().includes(search.toLowerCase()) ||
      l.code.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpen(false);
        setSearch("");
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  useEffect(() => {
    if (open && searchRef.current) {
      setTimeout(() => searchRef.current?.focus(), 50);
    }
  }, [open]);

  function changeLang(code: string) {
    i18n.changeLanguage(code);
    const lang = LANGUAGES.find((l) => l.code === code);
    document.documentElement.dir = lang?.dir || "ltr";
    document.documentElement.lang = code;
    setOpen(false);
    setSearch("");
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border bg-card hover:bg-accent transition-colors text-sm font-medium"
      >
        <Globe className="w-4 h-4 text-primary" />
        <span className="hidden sm:inline text-muted-foreground">{currentLang?.flag}</span>
        <span className="text-foreground">{currentLang?.name}</span>
        <ChevronDown
          className={`w-3 h-3 text-muted-foreground transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <div className="absolute top-full mt-2 right-0 w-72 bg-card border border-border rounded-xl shadow-xl z-50 overflow-hidden">
          <div className="p-2 border-b border-border">
            <div className="flex items-center gap-2 px-3 py-2 bg-muted/50 rounded-lg">
              <Search className="w-4 h-4 text-muted-foreground flex-shrink-0" />
              <input
                ref={searchRef}
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t("languageSwitcher.search")}
                className="bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground w-full"
              />
            </div>
          </div>
          <div className="max-h-64 overflow-y-auto">
            {filtered.length === 0 ? (
              <div className="px-4 py-3 text-sm text-muted-foreground text-center">
                {t("languageSwitcher.noResults")}
              </div>
            ) : (
              filtered.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => changeLang(lang.code)}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-accent transition-colors text-sm"
                >
                  <span className="text-base w-6">{lang.flag}</span>
                  <span className="flex-1 text-left text-foreground">{lang.name}</span>
                  <span className="text-xs text-muted-foreground uppercase">{lang.code}</span>
                  {i18n.language === lang.code && (
                    <Check className="w-4 h-4 text-primary flex-shrink-0" />
                  )}
                </button>
              ))
            )}
          </div>
          <div className="border-t border-border px-4 py-2">
            <p className="text-xs text-muted-foreground text-center">
              {LANGUAGES.length} {t("languageSwitcher.label")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
