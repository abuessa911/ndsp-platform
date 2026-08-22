import {
  createContext,
  type PropsWithChildren,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react"

export type NdspLanguage = "ar" | "en"

type LanguageContextValue = {
  language: NdspLanguage
  isArabic: boolean
  setLanguage: (language: NdspLanguage) => void
  toggleLanguage: () => void
}

const STORAGE_KEY = "ndsp-public-language"

const LanguageContext =
  createContext<LanguageContextValue | null>(null)

function getInitialLanguage(): NdspLanguage {
  if (typeof window === "undefined") {
    return "ar"
  }

  const stored = window.localStorage.getItem(STORAGE_KEY)

  if (stored === "ar" || stored === "en") {
    return stored
  }

  return "ar"
}

export function LanguageProvider({
  children,
}: PropsWithChildren) {
  const [language, setLanguage] =
    useState<NdspLanguage>(getInitialLanguage)

  useEffect(() => {
    const root = document.documentElement

    root.lang = language
    root.dir = language === "ar" ? "rtl" : "ltr"

    window.localStorage.setItem(STORAGE_KEY, language)
  }, [language])

  const value = useMemo<LanguageContextValue>(
    () => ({
      language,
      isArabic: language === "ar",
      setLanguage,
      toggleLanguage: () =>
        setLanguage((current) =>
          current === "ar" ? "en" : "ar",
        ),
    }),
    [language],
  )

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useNdspLanguage() {
  const context = useContext(LanguageContext)

  if (!context) {
    throw new Error(
      "useNdspLanguage must be used within LanguageProvider.",
    )
  }

  return context
}
