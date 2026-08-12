/* NDSP_LANDING_V34_1 — public content only; no decision formulas or private evidence. */
(() => {
  const marker = "ndspLandingV34";
  const content = {
    ar: {
      eyebrow: "غرفة دعم القرار", title: "قرار واحد واضح، وقراءة تتعمّق عند الحاجة.",
      intro: "NDSP ليست شاشة سوق ولا منصة توصيات. هي غرفة قرار متكاملة تجمع الحالة الحاكمة، مستويات السيناريو، والأدلة العامة في ترتيب مفهوم للمستخدم العادي والمحترف.",
      seal: "بيانات حية ومحكومة", providers: "تغطية مصادر محكومة", cta: "استكشف غرفة القرار", account: "إنشاء حساب مستخدم",
      notice: "<strong>تأثير محكوم وخصوصية:</strong> تؤثر الطبقات المربوطة في القرار من الخلفية وفق حالتها الحاكمة. يختلف فقط مستوى الإفصاح في الواجهة؛ فتظهر التفاصيل العامة للمراجعة، بينما تبقى المعادلات والأدلة الداخلية محمية.",
      cards: [
        ["01", "56 أصلًا عبر أربعة أسواق", "الأصول الرقمية والعملات والسلع والمؤشرات تأتي من سجل أصول موحّد؛ ولا تُعرض قائمة ثابتة بديلة عند تعذّر البيانات."],
        ["02", "قوة القراءة غير جاهزية القرار", "شريطان منفصلان يوضحان قوة القراءة وجاهزية القرار، حتى لا تُفهم الإشارة الداعمة على أنها قرار مكتمل."],
        ["03", "أنماط القراءة: بسيط ومحترف", "الوضع البسيط يركز على الملخص والحالة والمستويات؛ والوضع المحترف يفتح TDL وNMP والزخم والتباعد والمخاطر."],
        ["04", "خمسة مستويات للسيناريو", "المراقبة والتفعيل والوصول والمراجعة والإلغاء تظهر كبطاقات واضحة بدل رسوم تجريدية أو لغة تنفيذية."],
        ["05", "16 طبقة حوكمة، رؤية آمنة", "يكشف رادار واحد اكتمال وحدات القراءة فقط. أما التفاصيل المحمية فتظهر حالتها دون كشف أسرار المحرك أو المعادلات."],
        ["06", "مصدر أساسي وبديل محكوم", "لا يُعلن المصدر فعليًا إلا بعد نجاحه. وتبقى بيانات نهاية اليوم موصوفة بوضوح ولا تُقدَّم كأنها لحظية."]
      ]
    },
    en: {
      eyebrow: "Decision support room", title: "One clear decision, with depth when it is needed.",
      intro: "NDSP is neither a market screen nor a recommendation platform. It is an advanced Decision Room that brings governing state, scenario levels, and public evidence into an understandable order for both new and professional users.",
      seal: "Live & governed data", providers: "Governed source coverage", cta: "Explore the Decision Room", account: "Create a user account",
      notice: "<strong>Governed impact and privacy:</strong> Bound layers influence the decision in the backend according to their governing state. Only the disclosure level differs in the interface: public details support review while equations and internal evidence remain protected.",
      cards: [
        ["01", "56 assets across four markets", "Digital assets, currencies, commodities, and indices come from one governed asset registry. No static fallback list is shown when data is unavailable."],
        ["02", "Reading strength is not decision readiness", "Separate bars show reading strength and decision readiness, so supportive context is never presented as a completed decision."],
        ["03", "Reading modes: Beginner and Professional", "Beginner mode focuses on the summary, state, and levels; Professional mode opens TDL, NMP, momentum, divergence, and risk."],
        ["04", "Five scenario levels", "Monitoring, activation, arrival, review, and invalidation appear as clear cards rather than abstract plots or execution language."],
        ["05", "16 governed layers, safe visibility", "One radar shows decision-unit completion only. Protected details show their status without exposing engine secrets or equations."],
        ["06", "Primary and governed fallback sources", "A provider is shown as active only after a successful request. End-of-day data remains clearly labelled and is never presented as intraday."]
      ]
    }
  };

  const getLanguage = () => {
    try {
      const saved = localStorage.getItem("ndsp_lang_final") || localStorage.getItem("ndsp_final_lang") || localStorage.getItem("ndsp_lang");
      if (/^(en|english)$/i.test(saved || "")) return "en";
      if (/^(ar|arabic|العربية|عربي)$/i.test(saved || "")) return "ar";
    } catch (_) { /* Storage is optional. */ }
    const root = document.documentElement;
    if ((root.lang || "").toLowerCase().startsWith("en") && root.dir !== "rtl") return "en";
    return /[\u0600-\u06FF]/.test(document.body.innerText || "") ? "ar" : "en";
  };

  const escape = value => String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));

  const render = () => {
    const lang = getLanguage();
    const t = content[lang];
    const old = document.getElementById(marker);
    if (old && old.dataset.lang === lang) return;
    if (old) old.remove();
    const section = document.createElement("section");
    section.id = marker;
    section.className = marker;
    section.dataset.lang = lang;
    section.dir = lang === "ar" ? "rtl" : "ltr";
    section.innerHTML = `<div class="${marker}__frame"><div class="${marker}__top"><div><p class="${marker}__eyebrow">${escape(t.eyebrow)}</p><h2>${escape(t.title)}</h2><p class="${marker}__intro">${escape(t.intro)}</p></div><span class="${marker}__seal">${escape(t.seal)}</span></div><div class="${marker}__grid">${t.cards.map(card => `<article class="${marker}__card"><span class="${marker}__number">${card[0]}</span><h3>${escape(card[1])}</h3><p>${escape(card[2])}</p></article>`).join("")}</div><div class="${marker}__providers"><b>${escape(t.providers)}</b><span class="${marker}__provider">Binance · Digital assets</span><span class="${marker}__provider">Yahoo Finance · Multi-market</span><span class="${marker}__provider">Stooq · End-of-day fallback</span></div><div class="${marker}__bottom"><p class="${marker}__notice">${t.notice}</p><div class="${marker}__actions"><a class="${marker}__action ${marker}__action--primary" href="https://my.ndsp.app/decision-room-v31/">${escape(t.cta)}</a><a class="${marker}__action" href="https://my.ndsp.app/decision-room-v31/account/?mode=register">${escape(t.account)}</a></div></div></div>`;
    const footer = document.querySelector("footer");
    if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer);
    else document.body.appendChild(section);
  };

  const start = () => {
    render();
    new MutationObserver(() => window.setTimeout(render, 0)).observe(document.documentElement, { attributes: true, attributeFilter: ["lang", "dir"] });
    document.addEventListener("click", () => window.setTimeout(render, 80), { passive: true });
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
})();
