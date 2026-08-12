(function () {
  "use strict";

  var VERSION = "25";
  var API_PATH = "/__ndsp/governance-44-v26";
  var ROOT_ID = "ndsp-governance-44-v26";
  var LANGUAGE_KEYS = ["ndsp_lang_final", "ndsp_final_lang", "ndsp_lang"];
  var ACTIVE_PATHS = ["/decisions", "/governance"];
  var currentAbort = null;

  var layerDescriptions = {
    ar: {
      "NDSP-CORE-L01": "اتجاه الالتزام القانوني طويل ومتوسط المدى.",
      "NDSP-CORE-L02": "الاتجاه المضاربي قصير المدى وربطه بالسياق الزمني.",
      "NDSP-CORE-L03": "اتجاه السوق الحاكم المستخرج من قراءة السيناريو.",
      "NDSP-CORE-L04": "بوابة التصحيح والجاهزية قبل اكتمال القراءة.",
      "NDSP-CORE-L05": "فحص التباعد والتعارض بين الأطر الزمنية.",
      "NDSP-CORE-L06": "منطق الزمن واليوم وصلاحية نافذة القراءة.",
      "NDSP-CORE-L07": "مستويات التفعيل والوصول والمراجعة والإلغاء.",
      "NDSP-CORE-L08": "نقطة التقاء نواف وقيمة الالتقاء الحرجة.",
      "NDSP-CORE-L09": "قراءة الزخم وقوة الدفع الحالية.",
      "NDSP-CORE-L10": "السيولة والبنية ومناطق التركز الهيكلي.",
      "NDSP-CORE-L11": "سياق الدولار والعوامل الاقتصادية الكلية.",
      "NDSP-CORE-L12": "الرادار الحاكم للمخاطر وحدود الحذر.",
      "NDSP-CORE-L13": "إشارة نواف الذهبية وحالة اكتمال مدخلاتها.",
      "NDSP-CORE-L14": "إشارة نواف الذهبية المعززة وشروطها الإضافية.",
      "NDSP-CORE-L15": "اختبار محامي الشيطان قبل الخلاصة النهائية.",
      "NDSP-CORE-L16": "الختم النهائي وحالة القرار القانونية."
    },
    en: {
      "NDSP-CORE-L01": "Long and medium-term canonical commitment direction.",
      "NDSP-CORE-L02": "Short-term speculative direction and temporal context.",
      "NDSP-CORE-L03": "Governing market direction derived from the scenario.",
      "NDSP-CORE-L04": "Correction and readiness gate before completion.",
      "NDSP-CORE-L05": "Divergence and cross-timeframe conflict validation.",
      "NDSP-CORE-L06": "Time, day logic and reading-window validity.",
      "NDSP-CORE-L07": "Activation, arrival, review and invalidation levels.",
      "NDSP-CORE-L08": "Nawaf Meet Point and critical confluence value.",
      "NDSP-CORE-L09": "Momentum state and current impulse strength.",
      "NDSP-CORE-L10": "Liquidity, structure and structural concentration.",
      "NDSP-CORE-L11": "USD context and macroeconomic influence.",
      "NDSP-CORE-L12": "Governing risk radar and caution boundaries.",
      "NDSP-CORE-L13": "Nawaf Golden Signal and input completeness.",
      "NDSP-CORE-L14": "Enhanced Nawaf Golden Signal and extra conditions.",
      "NDSP-CORE-L15": "Devil's Advocate validation before final synthesis.",
      "NDSP-CORE-L16": "Final seal and governed decision state."
    }
  };

  var domainNames = {
    data_foundation: "أساس البيانات",
    evidence: "الأدلة والتتبع",
    governance: "الحوكمة",
    simulation: "المحاكاة",
    observability: "المراقبة",
    intelligence: "السياق الذكي",
    orchestration: "التنسيق",
    explainability: "التفسير",
    evaluation: "التقييم",
    personalization: "التخصيص",
    access: "الوصول",
    integrations: "التكاملات",
    commercial: "التجاري",
    security: "الأمن",
    operations: "التشغيل"
  };

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function normalize(value) {
    return String(value || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function language() {
    var rootLanguage = normalize(document.documentElement.getAttribute("lang"));
    if (rootLanguage.indexOf("en") === 0) return "en";
    try {
      if (LANGUAGE_KEYS.some(function (key) {
        return normalize(localStorage.getItem(key)) === "en";
      })) return "en";
    } catch (_) {}
    return "ar";
  }

  function copy() {
    if (language() === "en") {
      return {
        platform: "NDSP — Nawaf Decision Support Platform",
        layersTitle: "The 16 governed decision layers",
        layersSubtitle: "Live exposure of every decision layer from the governed public contract. A visible layer is not automatically a completed layer.",
        capabilitiesTitle: "The 28 platform capabilities",
        capabilitiesSubtitle: "Complete platform-capability exposure with truthful installation and runtime state. These capabilities do not hold decision authority.",
        decisions: "Decision Layers",
        governance: "Platform Capabilities",
        symbol: "Asset symbol",
        timeframe: "Timeframe",
        refresh: "Refresh",
        total: "Total",
        bound: "Bound",
        installed: "Installed",
        live: "Live",
        state: "State",
        family: "Family",
        blocking: "Blocking",
        visibility: "Visibility",
        yes: "Yes",
        no: "No",
        criticality: "Criticality",
        failPolicy: "Fail policy",
        dependencies: "Dependencies",
        authority: "Decision authority",
        loading: "Loading the governed contract…",
        retry: "Retry",
        error: "The governed contract could not be loaded.",
        truth: "Truth boundary: only NDSP-CORE-L01 through L16 may influence the governed decision. Platform capabilities protect, explain, observe or operate the system without becoming decision engines.",
        installedYes: "Installed",
        installedNo: "Not installed",
        runtime: "Runtime",
        disclaimer: "Explanatory decision-support output; not an execution instruction."
      };
    }
    return {
      platform: "NDSP — منصة نواف لدعم القرار",
      layersTitle: "طبقات القرار الحاكمة الـ16",
      layersSubtitle: "عرض حي لكل طبقة من العقد العام المحكوم. ظهور الطبقة لا يعني أنها مكتملة تلقائيًا.",
      capabilitiesTitle: "قدرات المنصة الـ28",
      capabilitiesSubtitle: "عرض كامل لقدرات المنصة مع حالة التثبيت والتشغيل الحقيقية. هذه القدرات لا تملك سلطة القرار.",
      decisions: "طبقات القرار",
      governance: "قدرات المنصة",
      symbol: "رمز الأصل",
      timeframe: "الإطار الزمني",
      refresh: "تحديث",
      total: "الإجمالي",
      bound: "المربوط",
      installed: "المثبت",
      live: "الحي",
      state: "الحالة",
      family: "العائلة",
      blocking: "حاجبة",
      visibility: "الظهور",
      yes: "نعم",
      no: "لا",
      criticality: "الأهمية",
      failPolicy: "سياسة الفشل",
      dependencies: "التبعيات",
      authority: "سلطة القرار",
      loading: "جارٍ تحميل العقد المحكوم…",
      retry: "إعادة المحاولة",
      error: "تعذر تحميل العقد المحكوم.",
      truth: "حد الحقيقة: الطبقات NDSP-CORE-L01 إلى L16 وحدها قد تؤثر في القرار المحكوم. قدرات المنصة تحمي النظام أو تفسره أو تراقبه أو تشغله من دون أن تتحول إلى محركات قرار.",
      installedYes: "مثبتة",
      installedNo: "غير مثبتة",
      runtime: "التشغيل",
      disclaimer: "مخرجات تفسيرية لدعم القرار وليست أمر تنفيذ."
    };
  }

  function tone(state) {
    var value = String(state || "").toUpperCase();
    if (["ACTIVE", "AVAILABLE", "PASSED", "READY", "LIVE"].indexOf(value) >= 0) return "ndsp44-good";
    if (["BLOCKED", "NOT_INSTALLED"].indexOf(value) >= 0) return "ndsp44-bad";
    return "ndsp44-warn";
  }

  function setTheme(root) {
    var background = getComputedStyle(document.body).backgroundColor || "rgb(7,17,31)";
    var numbers = background.match(/[\d.]+/g) || [7, 17, 31];
    var luminance = (Number(numbers[0]) * .2126 + Number(numbers[1]) * .7152 + Number(numbers[2]) * .0722) / 255;
    root.setAttribute("data-theme", luminance > .62 ? "light" : "dark");
  }

  function visible(element) {
    if (!element) return false;
    var style = getComputedStyle(element);
    var rect = element.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || 1) > 0 && rect.width > 0 && rect.height > 0;
  }

  function positionRoot() {
    var root = document.getElementById(ROOT_ID);
    if (!root) return;
    var top = window.innerWidth < 760 ? 56 : 64;
    Array.prototype.slice.call(document.querySelectorAll("header,[role='banner']")).forEach(function (element) {
      if (!visible(element)) return;
      var style = getComputedStyle(element);
      var rect = element.getBoundingClientRect();
      if ((style.position === "fixed" || style.position === "sticky") && rect.top <= 8 && rect.width > window.innerWidth * .5 && rect.bottom < 180) {
        top = Math.max(top, Math.round(rect.bottom));
      }
    });
    root.style.top = top + "px";
    root.style.left = "0px";
    root.style.right = "0px";
    if (window.innerWidth >= 760) {
      var side = Array.prototype.slice.call(document.querySelectorAll("aside,nav,[data-sidebar],.sidebar"))
        .filter(function (element) {
          if (!visible(element)) return false;
          var rect = element.getBoundingClientRect();
          var style = getComputedStyle(element);
          return rect.height > window.innerHeight * .55 && rect.width >= 150 && rect.width <= Math.min(420, window.innerWidth * .42) && (style.position === "fixed" || style.position === "sticky" || rect.top < 100);
        })
        .sort(function (a, b) { return b.getBoundingClientRect().height - a.getBoundingClientRect().height; })[0];
      if (side) {
        var sideRect = side.getBoundingClientRect();
        if (sideRect.left < window.innerWidth / 2) root.style.left = Math.max(0, Math.round(sideRect.right)) + "px";
        else root.style.right = Math.max(0, Math.round(window.innerWidth - sideRect.left)) + "px";
      }
    }
  }

  function ensureRoot() {
    var root = document.getElementById(ROOT_ID);
    if (!root) {
      root = document.createElement("section");
      root.id = ROOT_ID;
      root.setAttribute("aria-live", "polite");
      document.body.appendChild(root);
    }
    document.documentElement.classList.add("ndsp44-active");
    root.setAttribute("dir", language() === "en" ? "ltr" : "rtl");
    root.setAttribute("data-ndsp-lang", language());
    setTheme(root);
    positionRoot();
    return root;
  }

  function removeRoot() {
    var root = document.getElementById(ROOT_ID);
    if (root) root.remove();
    document.documentElement.classList.remove("ndsp44-active");
  }

  function routeTo(path) {
    window.location.assign(path + window.location.search);
  }

  function headerHtml(route, data) {
    var t = copy();
    var summary = data.governance_summary || {};
    var title = route === "/governance" ? t.capabilitiesTitle : t.layersTitle;
    var subtitle = route === "/governance" ? t.capabilitiesSubtitle : t.layersSubtitle;
    var symbol = esc((data.instrument || {}).symbol || "ETHUSDT");
    var timeframe = esc((data.instrument || {}).timeframe || "weekly");
    return '<div class="ndsp44-hero">' +
      '<div class="ndsp44-topline">' +
        '<div><div class="ndsp44-kicker">' + esc(t.platform) + '</div>' +
        '<h1 class="ndsp44-title">' + esc(title) + '</h1>' +
        '<p class="ndsp44-subtitle">' + esc(subtitle) + '</p></div>' +
        '<div class="ndsp44-tabs">' +
          '<button class="ndsp44-tab" data-ndsp44-route="/decisions" aria-current="' + (route === "/decisions" ? "page" : "false") + '">' + esc(t.decisions) + '</button>' +
          '<button class="ndsp44-tab" data-ndsp44-route="/governance" aria-current="' + (route === "/governance" ? "page" : "false") + '">' + esc(t.governance) + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="ndsp44-controls">' +
        '<input class="ndsp44-input" data-ndsp44-symbol aria-label="' + esc(t.symbol) + '" value="' + symbol + '">' +
        '<select class="ndsp44-select" data-ndsp44-timeframe aria-label="' + esc(t.timeframe) + '">' +
          '<option value="daily" ' + (timeframe === "daily" ? "selected" : "") + '>Daily</option>' +
          '<option value="weekly" ' + (timeframe === "weekly" ? "selected" : "") + '>Weekly</option>' +
          '<option value="monthly" ' + (timeframe === "monthly" ? "selected" : "") + '>Monthly</option>' +
        '</select>' +
        '<button class="ndsp44-button" data-ndsp44-refresh>' + esc(t.refresh) + '</button>' +
      '</div>' +
      '<div class="ndsp44-summary">' +
        '<div class="ndsp44-stat"><strong>' + esc(summary.layer_total || 16) + '</strong><span>' + esc(t.total) + ' · ' + esc(t.decisions) + '</span></div>' +
        '<div class="ndsp44-stat"><strong>' + esc(summary.layer_bound || 0) + '</strong><span>' + esc(t.bound) + '</span></div>' +
        '<div class="ndsp44-stat"><strong>' + esc(summary.capability_installed || 0) + '</strong><span>' + esc(t.installed) + '</span></div>' +
        '<div class="ndsp44-stat"><strong>' + esc(summary.capability_live || 0) + '</strong><span>' + esc(t.live) + '</span></div>' +
      '</div>' +
    '</div>';
  }

  function layerHtml(layer) {
    var t = copy();
    var lang = language();
    var name = lang === "en" ? (layer.name_en || layer.canonical_name) : (layer.name_ar || layer.canonical_name);
    var state = lang === "en" ? layer.state : (layer.state_ar || layer.state);
    var description = (layerDescriptions[lang] || {})[layer.id] || layer.evidence || "";
    return '<article class="ndsp44-card" data-ndsp-layer-card="' + esc(layer.id) + '">' +
      '<div class="ndsp44-card-head">' +
        '<div class="ndsp44-id">' + esc(String(layer.id || "").replace("NDSP-CORE-", "")) + '</div>' +
        '<div class="ndsp44-name"><strong>' + esc(name) + '</strong><small>' + esc(layer.canonical_name) + '</small></div>' +
        '<span class="ndsp44-badge ' + tone(layer.state) + '">' + esc(state) + '</span>' +
      '</div>' +
      '<div class="ndsp44-meta">' +
        '<div><span>' + esc(t.family) + '</span><strong>' + esc(layer.family || "—") + '</strong></div>' +
        '<div><span>' + esc(t.blocking) + '</span><strong>' + esc(layer.blocking ? t.yes : t.no) + '</strong></div>' +
        '<div><span>' + esc(t.visibility) + '</span><strong>' + esc(layer.public_visibility || "—") + '</strong></div>' +
        '<div><span>' + esc(t.state) + '</span><strong>' + esc(layer.score == null ? "—" : layer.score + "%") + '</strong></div>' +
      '</div>' +
      '<p class="ndsp44-desc">' + esc(description) + '</p>' +
      '<div class="ndsp44-progress"><i style="width:' + Math.max(0, Math.min(100, Number(layer.score) || 0)) + '%"></i></div>' +
    '</article>';
  }

  function capabilityHtml(capability) {
    var t = copy();
    var lang = language();
    var name = lang === "en" ? String(capability.canonical_name || "").replace(/_/g, " ") : (capability.name_ar || capability.canonical_name);
    var state = lang === "en" ? capability.runtime_state : (capability.runtime_state_ar || capability.runtime_state);
    var domain = lang === "en" ? String(capability.domain || "").replace(/_/g, " ") : (domainNames[capability.domain] || capability.domain || "—");
    return '<article class="ndsp44-card" data-ndsp-capability-card="' + esc(capability.id) + '">' +
      '<div class="ndsp44-card-head">' +
        '<div class="ndsp44-id">' + esc(String(capability.id || "").replace("NDSP-CAP-", "P")) + '</div>' +
        '<div class="ndsp44-name"><strong>' + esc(name) + '</strong><small>' + esc(capability.canonical_name) + '</small></div>' +
        '<span class="ndsp44-badge ' + tone(capability.runtime_state) + '">' + esc(state) + '</span>' +
      '</div>' +
      '<div class="ndsp44-meta">' +
        '<div><span>' + esc(t.installed) + '</span><strong>' + esc(capability.installed ? t.installedYes : t.installedNo) + '</strong></div>' +
        '<div><span>' + esc(t.runtime) + '</span><strong>' + esc(state) + '</strong></div>' +
        '<div><span>' + esc(t.criticality) + '</span><strong>' + esc(capability.criticality || "—") + '</strong></div>' +
        '<div><span>' + esc(t.failPolicy) + '</span><strong>' + esc(capability.fail_policy || "—") + '</strong></div>' +
        '<div><span>' + esc(t.dependencies) + '</span><strong>' + esc((capability.dependencies || []).length) + '</strong></div>' +
        '<div><span>' + esc(t.authority) + '</span><strong>' + esc(t.no) + '</strong></div>' +
      '</div>' +
      '<p class="ndsp44-desc">' + esc(domain) + '</p>' +
    '</article>';
  }

  function contentHtml(route, data) {
    var t = copy();
    var list = route === "/governance" ? (data.platform_capabilities || []) : (data.decision_layers || []);
    var cards = route === "/governance" ? list.map(capabilityHtml).join("") : list.map(layerHtml).join("");
    var total = route === "/governance" ? 28 : 16;
    return headerHtml(route, data) +
      '<div class="ndsp44-section">' +
        '<div class="ndsp44-section-head">' +
          '<h2 class="ndsp44-section-title">' + esc(route === "/governance" ? t.governance : t.decisions) + '</h2>' +
          '<div class="ndsp44-section-note">' + list.length + ' / ' + total + '</div>' +
        '</div>' +
        '<div class="ndsp44-grid">' + cards + '</div>' +
        '<div class="ndsp44-truth">' + esc(t.truth) + '<br>' + esc(t.disclaimer) + '</div>' +
      '</div>';
  }

  function requestParams() {
    var query = new URLSearchParams(location.search);
    return {
      symbol: (query.get("symbol") || "ETHUSDT").toUpperCase(),
      timeframe: (query.get("timeframe") || "weekly").toLowerCase()
    };
  }

  function bindControls(root) {
    root.querySelectorAll("[data-ndsp44-route]").forEach(function (button) {
      button.addEventListener("click", function () {
        routeTo(button.getAttribute("data-ndsp44-route"));
      });
    });
    var refresh = root.querySelector("[data-ndsp44-refresh]");
    if (refresh) {
      refresh.addEventListener("click", function () {
        var symbol = root.querySelector("[data-ndsp44-symbol]").value.trim().toUpperCase() || "ETHUSDT";
        var timeframe = root.querySelector("[data-ndsp44-timeframe]").value;
        var url = new URL(location.href);
        url.searchParams.set("symbol", symbol);
        url.searchParams.set("timeframe", timeframe);
        url.searchParams.set("fresh", String(Date.now()));
        location.assign(url.pathname + url.search);
      });
    }
  }

  async function render() {
    var route = location.pathname.replace(/\/+$/, "") || "/";
    if (ACTIVE_PATHS.indexOf(route) < 0) {
      removeRoot();
      return;
    }
    var root = ensureRoot();
    var t = copy();
    root.innerHTML = '<div class="ndsp44-loading">' + esc(t.loading) + '</div>';
    if (currentAbort) currentAbort.abort();
    currentAbort = new AbortController();
    var params = requestParams();
    var endpoint = API_PATH + "?symbol=" + encodeURIComponent(params.symbol) + "&timeframe=" + encodeURIComponent(params.timeframe) + "&_ndsp_ui=" + Date.now();
    try {
      var response = await fetch(endpoint, {
        cache: "no-store",
        headers: { Accept: "application/json" },
        signal: currentAbort.signal
      });
      if (!response.ok) throw new Error("HTTP_" + response.status);
      var data = await response.json();
      if (!data || !Array.isArray(data.decision_layers) || data.decision_layers.length !== 16 || !Array.isArray(data.platform_capabilities) || data.platform_capabilities.length !== 28) {
        throw new Error("CONTRACT_16_28_MISMATCH");
      }
      root.setAttribute("data-ndsp-contract", data.governance_projection_version || "missing");
      root.innerHTML = '<div class="ndsp44-wrap">' + contentHtml(route, data) + '</div>';
      bindControls(root);
      positionRoot();
    } catch (error) {
      if (error && error.name === "AbortError") return;
      console.error("NDSP44_FETCH_ERROR", error);
      root.innerHTML = '<div class="ndsp44-error" data-ndsp44-error><div><strong>' + esc(t.error) + '</strong><div>' + esc(error && error.message || error) + '</div><button class="ndsp44-button" data-ndsp44-retry style="margin-top:14px">' + esc(t.retry) + '</button></div></div>';
      var retry = root.querySelector("[data-ndsp44-retry]");
      if (retry) retry.addEventListener("click", render);
    }
  }

  function bindExistingMenu() {
    var selectors = "aside a,aside button,nav a,nav button,[data-sidebar] a,[data-sidebar] button,.sidebar a,.sidebar button";
    document.querySelectorAll(selectors).forEach(function (element) {
      if (element.getAttribute("data-ndsp44-bound") === "1") return;
      var value = normalize(element.innerText || element.textContent || element.getAttribute("aria-label"));
      var target = null;
      if (value === "الحوكمة والمخاطر" || value === "الحوكمة" || value === "governance & risk" || value === "governance") target = "/governance";
      if (value === "مركز القرار" || value === "القرارات" || value === "decision center" || value === "decision layers") target = "/decisions";
      if (!target) return;
      element.setAttribute("data-ndsp44-bound", "1");
      element.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        location.assign(target);
      }, true);
    });
  }

  function boot() {
    bindExistingMenu();
    render();
    positionRoot();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot, { once: true });
  else boot();
  window.addEventListener("resize", positionRoot);
  window.addEventListener("pageshow", boot);
  window.addEventListener("popstate", boot);
  new MutationObserver(bindExistingMenu).observe(document.documentElement, { childList: true, subtree: true });
  window.NDSP_GOVERNANCE_44_V26 = { version: VERSION, render: render };
})();
