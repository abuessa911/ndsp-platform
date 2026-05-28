import { Switch, Route } from "wouter";
import { useTranslation } from "react-i18next";
import { useEffect } from "react";
import { LANGUAGES } from "@/i18n";
import Home from "@/pages/Home";

function NotFound() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-foreground mb-4">404</h1>
        <p className="text-muted-foreground">Page not found</p>
        <a href="/" className="mt-4 inline-block text-primary hover:underline">Go Home</a>
      </div>
    </div>
  );
}

function App() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const lang =
      LANGUAGES.find((l) => l.code === i18n.language) ||
      LANGUAGES.find((l) => i18n.language.startsWith(l.code));
    if (lang) {
      document.documentElement.dir = lang.dir;
      document.documentElement.lang = lang.code;
    }
  }, [i18n.language]);

  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route component={NotFound} />
    </Switch>
  );
}

export default App;
