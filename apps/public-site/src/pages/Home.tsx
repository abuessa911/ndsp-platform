import { useState } from "react";
import { useTranslation } from "react-i18next";
import { LanguageSwitcher } from "@/components/LanguageSwitcher";
import { NewsTicker } from "@/components/NewsTicker";
import {
  Shield,
  AlertTriangle,
  Users,
  CheckCircle,
  XCircle,
  Lock,
  Star,
  Building2,
  Zap,
  ChevronRight,
  X,
  Activity,
  Mail,
  ExternalLink,
} from "lucide-react";

export default function Home() {
  const { t, i18n } = useTranslation();
  const [showTrial, setShowTrial] = useState(false);
  const isRtl = ["ar", "ur", "fa"].includes(i18n.language);

  const plans = [
    {
      key: "insight",
      icon: Zap,
      color: "text-blue-400",
      borderColor: "border-blue-500/20",
      glowColor: "hover:shadow-blue-500/10",
      popular: false,
      locked: true,
    },
    {
      key: "nmpPro",
      icon: Star,
      color: "text-primary",
      borderColor: "border-primary/30",
      glowColor: "hover:shadow-primary/15",
      popular: false,
      locked: true,
    },
    {
      key: "elite16",
      icon: Shield,
      color: "text-cyan-400",
      borderColor: "border-cyan-500/30",
      glowColor: "hover:shadow-cyan-500/15",
      popular: true,
      locked: false,
    },
    {
      key: "saas",
      icon: Building2,
      color: "text-purple-400",
      borderColor: "border-purple-500/20",
      glowColor: "hover:shadow-purple-500/10",
      popular: false,
      locked: true,
    },
  ];

  return (
    <div className={`min-h-screen bg-background ${isRtl ? "rtl" : "ltr"}`}>
      {/* Warning Banner */}
      <div className="bg-amber-950/80 border-b border-amber-700/40 px-4 py-2.5">
        <div className="max-w-7xl mx-auto flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-amber-200/80 leading-relaxed">{t("warning.text")}</p>
        </div>
      </div>

      {/* News Ticker */}
      <NewsTicker />

      {/* Navbar */}
      <header className="sticky top-0 z-40 border-b border-border/50 bg-background/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center">
              <Shield className="w-4 h-4 text-primary" />
            </div>
            <span className="font-bold text-foreground tracking-tight">NDSP</span>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <a href="#plans" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              {t("nav.plans")}
            </a>
            <a href="#trial" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              {t("nav.trial")}
            </a>
            <a href="#about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              {t("nav.faq")}
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <LanguageSwitcher />
            <a
              href="https://ndsp.app/#/register"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-semibold hover:opacity-90 transition-opacity"
            >
              {t("nav.register")}
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </header>

      <main>
        {/* Hero */}
        <section className="relative py-20 px-4 hero-grid overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent pointer-events-none" />
          <div className="max-w-4xl mx-auto text-center relative">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 mb-8 animate-fade-in-up">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              <span className="text-sm text-primary font-medium">{t("hero.badge")}</span>
            </div>

            <h1
              className="text-4xl sm:text-5xl md:text-6xl font-bold text-foreground leading-tight mb-6 animate-fade-in-up"
              style={{ animationDelay: "0.1s" }}
            >
              {t("hero.title")}
            </h1>

            <p
              className="text-xl text-primary font-medium mb-4 animate-fade-in-up"
              style={{ animationDelay: "0.15s" }}
            >
              {t("hero.subtitle")}
            </p>

            <div
              className="flex items-center justify-center gap-2 mb-6 animate-fade-in-up"
              style={{ animationDelay: "0.2s" }}
            >
              <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
              <p className="text-sm text-amber-300/80">{t("hero.disclaimer")}</p>
            </div>

            <p
              className="text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-in-up"
              style={{ animationDelay: "0.25s" }}
            >
              {t("hero.description")}
            </p>

            <div
              className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up"
              style={{ animationDelay: "0.3s" }}
            >
              <button
                onClick={() => setShowTrial(true)}
                className="flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-primary text-primary-foreground font-bold text-base hover:opacity-90 transition-opacity glow-gold"
              >
                {t("hero.startTrial")}
                <ChevronRight className="w-5 h-5" />
              </button>
              <a
                href="https://ndsp.app/#/trial"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl border border-border text-foreground font-medium text-base hover:bg-accent transition-colors"
              >
                {t("hero.viewJourney")}
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        </section>

        {/* Status Cards */}
        <section className="py-12 px-4 border-y border-border/50 bg-card/30">
          <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-start gap-4 p-5 rounded-xl bg-card border border-border">
              <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center flex-shrink-0">
                <Users className="w-5 h-5 text-muted-foreground" />
              </div>
              <div>
                <div className="text-xs text-muted-foreground mb-1">{t("status.visitor")}</div>
                <div className="text-sm text-foreground font-medium">{t("status.visitorDesc")}</div>
              </div>
            </div>
            <div className="flex items-start gap-4 p-5 rounded-xl bg-card border border-border">
              <div className="w-10 h-10 rounded-lg bg-green-900/30 border border-green-500/20 flex items-center justify-center flex-shrink-0">
                <Activity className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <div className="text-xs text-muted-foreground mb-1">{t("status.backend")}</div>
                <div className="text-sm text-foreground font-medium">{t("status.backendDesc")}</div>
              </div>
            </div>
            <div className="flex items-start gap-4 p-5 rounded-xl bg-card border border-border">
              <div className="w-10 h-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center flex-shrink-0">
                <Mail className="w-5 h-5 text-primary" />
              </div>
              <div>
                <div className="text-xs text-muted-foreground mb-1">{t("status.contact")}</div>
                <div className="text-sm text-foreground font-medium">{t("status.contactDesc")}</div>
              </div>
            </div>
          </div>
        </section>

        {/* Welcome */}
        <section className="py-16 px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-2xl font-bold text-foreground mb-6">{t("welcome.title")}</h2>
            <p className="text-muted-foreground leading-relaxed mb-8">{t("welcome.text")}</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={() => setShowTrial(true)}
                className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-opacity"
              >
                {t("welcome.startTrial")}
              </button>
              <a
                href="https://ndsp.app/#/trial"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-border text-foreground hover:bg-accent transition-colors"
              >
                {t("welcome.viewJourney")}
              </a>
            </div>
          </div>
        </section>

        {/* Seats */}
        <section className="py-16 px-4 bg-card/20">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-2xl font-bold text-foreground text-center mb-3">{t("seats.title")}</h2>
            <p className="text-muted-foreground text-center mb-10 max-w-2xl mx-auto">{t("seats.subtitle")}</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { key: "specialist", count: 10, icon: Shield, color: "text-blue-400", bg: "bg-blue-900/20 border-blue-500/20" },
                { key: "regular", count: 25, icon: Users, color: "text-green-400", bg: "bg-green-900/20 border-green-500/20" },
                { key: "special", count: 15, icon: Star, color: "text-primary", bg: "bg-primary/10 border-primary/20" },
              ].map((seat) => (
                <div key={seat.key} className={`p-6 rounded-xl border ${seat.bg}`}>
                  <div className="flex items-center gap-3 mb-4">
                    <seat.icon className={`w-5 h-5 ${seat.color}`} />
                    <span className="font-semibold text-foreground">{t(`seats.${seat.key}`)}</span>
                  </div>
                  <div className={`text-4xl font-black ${seat.color} mb-3`}>{seat.count}</div>
                  <p className="text-sm text-muted-foreground">{t(`seats.${seat.key}Desc`)}</p>
                </div>
              ))}
            </div>
            <p className="text-center text-sm text-muted-foreground mt-6 font-medium">{t("seats.total")}</p>
          </div>
        </section>

        {/* Plans */}
        <section id="plans" className="py-20 px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-foreground text-center mb-4">{t("plans.title")}</h2>
            <div className="h-1 w-16 bg-primary mx-auto mb-12 rounded-full" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
              {plans.map((plan) => {
                const PlanIcon = plan.icon;
                const features = t(`plans.${plan.key}.features`, { returnObjects: true }) as string[];
                const hidden = t(`plans.${plan.key}.hidden`, { returnObjects: true }) as string[];
                return (
                  <div
                    key={plan.key}
                    className={`relative plan-card p-5 rounded-2xl border ${plan.borderColor} bg-card shadow-sm hover:shadow-lg ${plan.glowColor} transition-all duration-300`}
                  >
                    {plan.popular && (
                      <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                        <span className="badge-trial text-xs px-3 py-1 rounded-full">Elite</span>
                      </div>
                    )}
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-9 h-9 rounded-lg bg-current/10 flex items-center justify-center">
                        <PlanIcon className={`w-5 h-5 ${plan.color}`} />
                      </div>
                      <div>
                        <div className="font-bold text-foreground text-sm">{t(`plans.${plan.key}.name`)}</div>
                        <div className={`text-lg font-black ${plan.color}`}>{t(`plans.${plan.key}.price`)}</div>
                      </div>
                    </div>

                    <p className="text-xs text-muted-foreground mb-5 leading-relaxed">{t(`plans.${plan.key}.desc`)}</p>

                    <div className="mb-4">
                      <div className="text-xs font-semibold text-foreground/60 uppercase tracking-wider mb-2">
                        {t("plans.features")}
                      </div>
                      <ul className="space-y-1.5">
                        {features.map((f, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-foreground/80">
                            <CheckCircle className="w-3.5 h-3.5 text-green-400 flex-shrink-0 mt-0.5" />
                            {f}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="mb-5">
                      <div className="text-xs font-semibold text-foreground/40 uppercase tracking-wider mb-2">
                        {t("plans.hidden")}
                      </div>
                      <ul className="space-y-1">
                        {hidden.slice(0, 3).map((h, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-muted-foreground/50">
                            <XCircle className="w-3.5 h-3.5 text-muted-foreground/30 flex-shrink-0 mt-0.5" />
                            {h}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {plan.locked ? (
                      <div className="mt-auto">
                        <div className="flex items-center gap-2 text-xs text-muted-foreground/50 mb-2">
                          <Lock className="w-3.5 h-3.5" />
                          <span>{t("plans.locked")}</span>
                        </div>
                        <button
                          disabled
                          className="w-full py-2.5 rounded-lg bg-muted/30 text-muted-foreground/40 text-sm font-medium cursor-not-allowed"
                        >
                          {t("plans.selectPlan")}
                        </button>
                      </div>
                    ) : (
                      <a
                        href="https://ndsp.app/#/register"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-semibold hover:opacity-90 transition-opacity"
                      >
                        {t("plans.selectPlan")}
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* About / FAQ */}
        <section id="about" className="py-16 px-4 bg-card/20">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-foreground text-center mb-3">{t("about.title")}</h2>
            <p className="text-muted-foreground text-center mb-10">{t("about.subtitle")}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-6 rounded-2xl bg-card border border-border">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-9 h-9 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center">
                    <CheckCircle className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="font-semibold text-foreground">{t("about.whatIs")}</h3>
                </div>
                <ul className="space-y-3">
                  {(t("about.whatIsItems", { returnObjects: true }) as string[]).map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                      <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="p-6 rounded-2xl bg-card border border-border">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-9 h-9 rounded-lg bg-destructive/10 border border-destructive/20 flex items-center justify-center">
                    <XCircle className="w-5 h-5 text-destructive" />
                  </div>
                  <h3 className="font-semibold text-foreground">{t("about.whatNot")}</h3>
                </div>
                <ul className="space-y-3">
                  {(t("about.whatNotItems", { returnObjects: true }) as string[]).map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                      <XCircle className="w-4 h-4 text-destructive/60 flex-shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-primary" />
              <span className="font-bold text-foreground">NDSP</span>
            </div>
            <p className="text-xs text-muted-foreground text-center max-w-xl">{t("footer.disclaimer")}</p>
            <p className="text-xs text-muted-foreground">© 2025 NDSP. {t("footer.rights")}.</p>
          </div>
        </div>
      </footer>

      {/* Trial Modal */}
      {showTrial && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="bg-card border border-border rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-primary/30 bg-primary/10">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                  <span className="text-xs text-primary font-medium">{t("trial.badge")}</span>
                </div>
                <button
                  onClick={() => setShowTrial(false)}
                  className="w-8 h-8 rounded-lg bg-muted hover:bg-accent transition-colors flex items-center justify-center"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <h2 className="text-xl font-bold text-foreground mb-2">{t("trial.title")}</h2>
              <p className="text-sm text-muted-foreground mb-6">{t("trial.subtitle")}</p>

              <div className="grid grid-cols-2 gap-3 mb-6">
                {[
                  { label: "trial.duration", value: "trial.durationVal" },
                  { label: "trial.currentPlan", value: "trial.currentPlanVal" },
                  { label: "trial.benefits", value: "trial.benefitsVal" },
                  { label: "trial.survey", value: "trial.surveyVal" },
                  { label: "trial.limitedSeats", value: "trial.limitedSeatsVal" },
                  { label: "trial.payment", value: "trial.paymentVal" },
                ].map((item, i) => (
                  <div key={i} className="p-4 rounded-xl bg-muted/30 border border-border">
                    <div className="text-xs font-semibold text-foreground/60 mb-1">{t(item.label)}</div>
                    <div className="text-sm text-foreground/80 leading-snug">{t(item.value)}</div>
                  </div>
                ))}
              </div>

              <div className="flex gap-3">
                <a
                  href="https://ndsp.app/#/register"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-opacity"
                >
                  {t("trial.start")}
                  <ExternalLink className="w-4 h-4" />
                </a>
                <button
                  onClick={() => setShowTrial(false)}
                  className="px-5 py-3 rounded-xl border border-border text-foreground hover:bg-accent transition-colors"
                >
                  {t("trial.close")}
                </button>
              </div>

              <p className="text-xs text-muted-foreground text-center mt-4">{t("footer.disclaimer")}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
