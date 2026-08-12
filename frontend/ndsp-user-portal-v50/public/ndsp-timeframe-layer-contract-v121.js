(function () {
  "use strict";

  if (window.__NDSP_TIMEFRAME_LAYER_CONTRACT_V121__) {
    return;
  }

  var VERSION = "121.0.0";
  var CONTRACT_VERSION = "ndsp.timeframe-layer-contract.v2";
  var API_PATH = "/api/decision/quality-live";
  var STYLE_ID = "ndsp-timeframe-layer-contract-v121-style";
  var CONTEXT_KEY = "ndsp_analysis_context_v1";
  var GENERIC_MISSING_AR = "لم تصل بيانات محكومة لهذه الخانة حتى الآن.";

  var REGISTRY = [
    ["NDSP-CORE-L01", "L01", "tdl_medium_long", "منطق القرار الزمني — المتوسط والطويل", ["منطق القرار الزمني - المتوسط والطويل"]],
    ["NDSP-CORE-L02", "L02", "tdl_short_speculative", "منطق القرار الزمني — القصير والمضاربي", ["منطق القرار الزمني - القصير والمضاربي"]],
    ["NDSP-CORE-L03", "L03", "market_direction_context", "اتجاه السوق الحاكم", []],
    ["NDSP-CORE-L04", "L04", "correction_gate", "بوابة التصحيح", []],
    ["NDSP-CORE-L05", "L05", "divergence_engine", "محرك الانحراف", []],
    ["NDSP-CORE-L06", "L06", "temporal_day_logic", "منطق الزمن والأيام", []],
    ["NDSP-CORE-L07", "L07", "scenario_levels", "مستويات السيناريو", ["مستويات السيناريو المحكومة"]],
    ["NDSP-CORE-L08", "L08", "nmp_confirmation", "نقطة الالتقاء NMP", ["NMP", "NMP"]],
    ["NDSP-CORE-L09", "L09", "momentum_engine", "محرك الزخم", []],
    ["NDSP-CORE-L10", "L10", "liquidity_structure_confirmation", "تأكيد البنية والسيولة", []],
    ["NDSP-CORE-L11", "L11", "usd_macro_filter", "فلتر الدولار والسياق الكلي", ["الدولار والسياق الكلي"]],
    ["NDSP-CORE-L12", "L12", "risk_engine", "محرك المخاطر", ["المخاطر", "رادار المخاطر"]],
    ["NDSP-CORE-L13", "L13", "nawaf_golden_signal", "الإشارة الذهبية", []],
    ["NDSP-CORE-L14", "L14", "nawaf_enhanced_golden_signal", "الإشارة الذهبية المعززة", []],
    ["NDSP-CORE-L15", "L15", "devils_advocate", "محامي الشيطان", []],
    ["NDSP-CORE-L16", "L16", "decision_readiness_state_machine", "الجاهزية وآلة حالات القرار", ["جاهزية القرار"]]
  ].map(function (row) {
    return {
      id: row[0],
      code: row[1],
      canonical: row[2],
      nameAr: row[3],
      aliases: row[4]
    };
  });

  var STATE = {
    payload: null,
    envelope: null,
    contracts: [],
    contractMap: {},
    requestInFlight: false,
    applyTimer: 0,
    applying: false,
    observer: null,
    mappedCardCount: 0,
    lastAppliedAt: 0,
    lastError: ""
  };

  function text(value) {
    return String(value == null ? "" : value)
      .replace(/\u200f|\u200e/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function key(value) {
    return text(value)
      .toLowerCase()
      .replace(/[’'`]/g, "")
      .replace(/[\s\-–—_/\\.:()[\]{}]+/g, "");
  }

  function normalizeTimeframe(value) {
    var raw = text(value).toLowerCase();
    if (["15m", "15min", "15 دقيقة", "١٥ دقيقة"].indexOf(raw) >= 0) return "15m";
    if (["1h", "60m", "ساعة", "1 ساعة"].indexOf(raw) >= 0) return "1h";
    if (["4h", "240m", "4 ساعات", "٤ ساعات"].indexOf(raw) >= 0) return "4h";
    if (["1d", "d", "day", "daily", "يومي"].indexOf(raw) >= 0) return "daily";
    if (["1w", "w", "week", "weekly", "أسبوعي", "اسبوعي"].indexOf(raw) >= 0) return "weekly";
    if (["1mo", "1month", "month", "monthly", "شهري"].indexOf(raw) >= 0) return "monthly";
    return raw;
  }

  function timeframeLabel(frame) {
    return ({
      "15m": "15 دقيقة",
      "1h": "ساعة",
      "4h": "4 ساعات",
      daily: "يومي",
      weekly: "أسبوعي",
      monthly: "شهري"
    })[normalizeTimeframe(frame)] || text(frame);
  }

  function parseJson(raw) {
    try {
      return JSON.parse(raw);
    } catch (_) {
      return null;
    }
  }

  function contextNow() {
    var params = new URLSearchParams(location.search);
    var stored =
      parseJson(localStorage.getItem(CONTEXT_KEY) || "") ||
      parseJson(sessionStorage.getItem(CONTEXT_KEY) || "") ||
      {};

    return {
      market: text(params.get("market") || stored.market || "CRYPTO").toUpperCase(),
      symbol: text(params.get("symbol") || stored.symbol || stored.asset || "BTCUSDT").toUpperCase(),
      timeframe: normalizeTimeframe(params.get("timeframe") || stored.timeframe || ""),
      mode: text(params.get("mode") || stored.mode || stored.analysis_mode || "speculative"),
      view: text(params.get("view") || stored.view || stored.view_mode || "professional")
    };
  }

  function meaningful(value) {
    if (value == null) return false;
    if (typeof value === "string") {
      var normalized = text(value);
      return normalized !== "" && normalized !== "-" && normalized !== "—" && normalized !== "null";
    }
    if (Array.isArray(value)) return value.length > 0;
    if (typeof value === "object") return Object.keys(value).length > 0;
    return true;
  }

  function first(object, names) {
    for (var i = 0; i < names.length; i += 1) {
      var value = object && object[names[i]];
      if (meaningful(value)) return value;
    }
    return undefined;
  }

  function returnedFrame(payload) {
    return normalizeTimeframe(
      payload && payload.instrument && payload.instrument.timeframe ||
      payload && payload.live_market_analysis && payload.live_market_analysis.selected_timeframe ||
      payload && payload.nmp_timeframe ||
      payload && payload.timeframe ||
      ""
    );
  }

  function layerArray(payload) {
    var candidates = [
      payload && payload.decision_layers,
      payload && payload.layers,
      payload && payload.layer_results,
      payload && payload.governance_summary && payload.governance_summary.decision_layers
    ];

    for (var i = 0; i < candidates.length; i += 1) {
      if (Array.isArray(candidates[i])) return candidates[i];
      if (candidates[i] && typeof candidates[i] === "object") {
        return Object.keys(candidates[i]).map(function (name) {
          var value = candidates[i][name];
          if (value && typeof value === "object") {
            if (!value.layer_id && !value.id) value.layer_id = name;
            return value;
          }
          return { layer_id: name, value: value };
        });
      }
    }

    return [];
  }

  function layerIdentity(item) {
    return [
      item && item.layer_id,
      item && item.id,
      item && item.canonical_id,
      item && item.code,
      item && item.layer_code,
      item && item.canonical_name,
      item && item.name,
      item && item.name_ar,
      item && item.title
    ].filter(Boolean).map(key);
  }

  function findLayer(payload, reg) {
    var layers = layerArray(payload);
    var targets = [reg.id, reg.code, reg.canonical, reg.nameAr].concat(reg.aliases || []).map(key);

    for (var i = 0; i < layers.length; i += 1) {
      var identities = layerIdentity(layers[i]);
      var exact = identities.some(function (identity) {
        return targets.indexOf(identity) >= 0;
      });
      if (exact) return { value: layers[i], path: "decision_layers[" + i + "]" };
    }

    return null;
  }

  function stateArabic(value) {
    var raw = text(value);
    var map = {
      available: "متاح",
      active: "نشطة",
      enabled: "مفعلة",
      ready: "جاهزة",
      complete: "مكتملة",
      completed: "مكتملة",
      confirmed: "مؤكدة",
      aligned: "متوافقة",
      underreview: "تحت المراجعة",
      undermonitoring: "تحت المتابعة",
      monitoring: "تحت المتابعة",
      pending: "قيد المتابعة",
      partial: "جزئية",
      blocked: "محجوبة",
      incomplete: "غير مكتملة",
      unavailable: "غير متاحة",
      neutral: "محايدة",
      bullish: "ميل صاعد",
      bearish: "ميل هابط"
    };
    return map[key(raw)] || raw;
  }

  function summarize(item) {
    var state = first(item, ["state", "status", "layer_state", "runtime_state", "availability", "decision_state"]);
    var value = first(item, ["value", "output", "result", "summary_ar", "summary", "reading", "direction", "signal", "score"]);
    var reason = first(item, ["reason_ar", "reason", "explanation_ar", "explanation", "message", "unavailable_reason"]);
    var confidence = first(item, ["confidence", "confidence_score", "completion", "quality", "strength", "readiness"]);
    var reasons = first(item, ["reasons", "reason_codes"]);

    if (!meaningful(reason) && Array.isArray(reasons)) {
      reason = reasons.map(text).filter(Boolean).join(" · ");
    }

    return {
      state: stateArabic(state),
      value: text(value),
      reason: text(reason),
      confidence: confidence
    };
  }

  function buildContracts(payload, requested) {
    var returned = returnedFrame(payload);
    var frame = normalizeTimeframe(requested);
    var status = frame && returned && frame === returned
      ? "BOUND_EXACT_TIMEFRAME"
      : "QUARANTINED_TIMEFRAME_MISMATCH";

    STATE.envelope = {
      requestedTimeframe: frame,
      returnedTimeframe: returned,
      symbol: text(payload && payload.instrument && payload.instrument.symbol || contextNow().symbol).toUpperCase(),
      status: status,
      contractVersion: text(payload && payload.public_contract_version || CONTRACT_VERSION),
      generatedAt: text(payload && payload.generated_at || "")
    };

    STATE.contracts = [];
    STATE.contractMap = {};

    if (status !== "BOUND_EXACT_TIMEFRAME") return;

    REGISTRY.forEach(function (reg) {
      var found = findLayer(payload, reg);
      var summary = summarize(found ? found.value : {});
      var contract = {
        layer_id: reg.id,
        layer_code: reg.code,
        canonical_name: reg.canonical,
        name_ar: reg.nameAr,
        timeframe: frame,
        state: summary.state,
        value: summary.value,
        reason: summary.reason,
        confidence: summary.confidence,
        received: Boolean(found),
        source_path: found ? found.path : "",
        contract_version: CONTRACT_VERSION
      };
      STATE.contracts.push(contract);
      STATE.contractMap[reg.id] = contract;
    });
  }

  function ensureStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent =
      "[data-ndsp-contract-layer]{position:relative}" +
      ".ndsp-v121-contract-status{margin-top:10px;padding-top:9px;border-top:1px dashed rgba(216,170,47,.28);font-size:13px;line-height:1.75;color:#cdbf9e}" +
      ".ndsp-v121-contract-status strong{color:#f5d878;font-weight:700}" +
      "[data-ndsp-contract-received='yes'] .ndsp-v121-contract-status{border-top-color:rgba(65,202,137,.32)}";
    document.head.appendChild(style);
  }

  function leafNodesExact(value) {
    var expected = text(value);
    return Array.prototype.slice.call(document.querySelectorAll("span,div,p,strong,b,small,em,i,h1,h2,h3,h4,h5,h6"))
      .filter(function (node) {
        if (!node || node.children.length > 0) return false;
        var rect = node.getBoundingClientRect();
        return text(node.textContent) === expected && rect.width > 0 && rect.height > 0;
      });
  }

  function nearestCard(token) {
    if (!token) return null;
    var selectors = [
      "article.layerCard",
      ".layerCard",
      "article",
      "section.card",
      ".card",
      "li",
      "section",
      "[class*='layer']",
      "[class*='card']"
    ];

    for (var i = 0; i < selectors.length; i += 1) {
      var card = token.closest(selectors[i]);
      if (!card) continue;
      if (card.id === "app" || card === document.body || card === document.documentElement) continue;
      if (card.closest("header,nav,.drawer,.bottomNav,.topbar")) continue;
      var rect = card.getBoundingClientRect();
      var content = text(card.innerText);
      if (rect.width >= 140 && rect.height >= 45 && rect.height <= 900 && content.length <= 2400) {
        return card;
      }
    }

    return token.parentElement && token.parentElement.id !== "app" ? token.parentElement : null;
  }

  function cardFor(reg) {
    var existing = document.querySelector('[data-ndsp-contract-layer="' + reg.id + '"]');
    if (existing) return existing;

    var anchors = [reg.id, reg.code, reg.nameAr].concat(reg.aliases || []);
    for (var i = 0; i < anchors.length; i += 1) {
      var nodes = leafNodesExact(anchors[i]);
      for (var n = 0; n < nodes.length; n += 1) {
        var card = nearestCard(nodes[n]);
        if (card) return card;
      }
    }

    return null;
  }

  function genericNodes(card) {
    return Array.prototype.slice.call(card.querySelectorAll("p,span,div,strong,b,small"))
      .filter(function (node) {
        if (node.children.length > 0) return false;
        var value = text(node.textContent);
        return value === "غير متاح" ||
          value === "غير متاحة" ||
          value === GENERIC_MISSING_AR ||
          value.indexOf("لم تصل بيانات محكومة لهذه الخانة") >= 0 ||
          value.indexOf("نشطة · غير متاح") >= 0 ||
          value.indexOf("متاحة · غير متاح") >= 0;
      });
  }

  function compact(value, max) {
    var normalized = text(value);
    return normalized.length > max ? normalized.slice(0, max - 1) + "…" : normalized;
  }

  function contractLine(contract) {
    if (!contract || !contract.received) {
      return "عقد الطبقة غير مستلم للفريم " + timeframeLabel(STATE.envelope && STATE.envelope.requestedTimeframe);
    }

    var parts = [];
    if (contract.state) parts.push(contract.state);
    if (contract.value && key(contract.value) !== key(contract.state)) parts.push(compact(contract.value, 110));
    if (!contract.value && contract.reason) parts.push(compact(contract.reason, 110));
    if (contract.confidence !== undefined && contract.confidence !== null && contract.confidence !== "") {
      var number = Number(contract.confidence);
      if (Number.isFinite(number)) parts.push(Math.round(number) + "%");
    }
    if (!parts.length) parts.push("العقد مستلم");
    return parts.slice(0, 3).join(" · ");
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function bindCard(reg, contract, usedCards) {
    var card = cardFor(reg);
    if (!card || usedCards.indexOf(card) >= 0) return false;
    usedCards.push(card);

    card.setAttribute("data-ndsp-contract-layer", reg.id);
    card.setAttribute("data-ndsp-contract-timeframe", contract.timeframe);
    card.setAttribute("data-ndsp-contract-received", contract.received ? "yes" : "no");
    card.setAttribute("data-ndsp-contract-version", contract.contract_version);

    var line = contractLine(contract);
    var placeholders = genericNodes(card);

    if (contract.received && placeholders.length) {
      placeholders[0].textContent = line;
      placeholders[0].setAttribute("data-ndsp-contract-rendered", "yes");
      for (var i = 1; i < placeholders.length; i += 1) {
        placeholders[i].style.display = "none";
      }
    }

    var status = null;
    try {
      status = card.querySelector(":scope > .ndsp-v121-contract-status");
    } catch (_) {
      status = card.querySelector(".ndsp-v121-contract-status");
    }

    if (!status) {
      status = document.createElement("div");
      status.className = "ndsp-v121-contract-status";
      card.appendChild(status);
    }

    var html = "<strong>عقد " + escapeHtml(timeframeLabel(contract.timeframe)) +
      (contract.received ? " مرتبط" : " غير مكتمل") + "</strong> · " + escapeHtml(line);

    if (status.innerHTML !== html) status.innerHTML = html;
    return true;
  }

  function reconnectObserver() {
    if (!STATE.observer) return;
    try {
      STATE.observer.observe(document.documentElement, { childList: true, subtree: true });
    } catch (_) {}
  }

  function applyContracts() {
    if (STATE.applying || !STATE.payload || !STATE.envelope || STATE.envelope.status !== "BOUND_EXACT_TIMEFRAME") return;
    STATE.applying = true;
    if (STATE.observer) STATE.observer.disconnect();
    ensureStyle();

    var usedCards = [];
    var mapped = 0;
    REGISTRY.forEach(function (reg) {
      var contract = STATE.contractMap[reg.id];
      if (contract && bindCard(reg, contract, usedCards)) mapped += 1;
    });

    STATE.mappedCardCount = mapped;
    STATE.lastAppliedAt = Date.now();
    var runtime = window.__NDSP_TIMEFRAME_LAYER_CONTRACT_V121__;
    runtime.contracts = STATE.contracts;
    runtime.contractMap = STATE.contractMap;
    runtime.lastEnvelope = STATE.envelope;
    runtime.mappedCardCount = mapped;
    runtime.lastAppliedAt = STATE.lastAppliedAt;
    document.documentElement.setAttribute("data-ndsp-v121-ready", "yes");

    STATE.applying = false;
    reconnectObserver();
  }

  function scheduleApply(delay) {
    clearTimeout(STATE.applyTimer);
    STATE.applyTimer = setTimeout(applyContracts, delay == null ? 80 : delay);
  }

  function capture(payload, requested) {
    if (!payload || typeof payload !== "object" || payload.ok === false) return;
    STATE.payload = payload;
    buildContracts(payload, requested);
    var runtime = window.__NDSP_TIMEFRAME_LAYER_CONTRACT_V121__;
    runtime.payload = payload;
    runtime.contracts = STATE.contracts;
    runtime.contractMap = STATE.contractMap;
    runtime.lastEnvelope = STATE.envelope;
    runtime.lastError = "";
    scheduleApply(30);
  }

  function refresh() {
    if (STATE.requestInFlight) return;
    var ctx = contextNow();
    if (!ctx.symbol || !ctx.timeframe) return;
    STATE.requestInFlight = true;

    var params = new URLSearchParams({
      symbol: ctx.symbol,
      timeframe: ctx.timeframe,
      analysis_mode: ctx.mode,
      mode: ctx.mode,
      ndsp_contract: "v121",
      ndsp_contract_ts: String(Date.now())
    });

    fetch(API_PATH + "?" + params.toString(), {
      credentials: "same-origin",
      headers: { Accept: "application/json", "X-NDSP-Contract-Consumer": CONTRACT_VERSION }
    })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP_" + response.status);
        return response.json();
      })
      .then(function (payload) { capture(payload, ctx.timeframe); })
      .catch(function (error) {
        STATE.lastError = String(error && error.message ? error.message : error);
        window.__NDSP_TIMEFRAME_LAYER_CONTRACT_V121__.lastError = STATE.lastError;
      })
      .finally(function () { STATE.requestInFlight = false; });
  }

  function startObserver() {
    if (typeof MutationObserver === "undefined" || STATE.observer) return;
    STATE.observer = new MutationObserver(function (mutations) {
      if (STATE.applying) return;
      var relevant = mutations.some(function (mutation) {
        return Array.prototype.some.call(mutation.addedNodes || [], function (node) {
          return node && node.nodeType === 1 && !(node.classList && node.classList.contains("ndsp-v121-contract-status"));
        });
      });
      if (relevant) scheduleApply(70);
    });
    reconnectObserver();
  }

  window.__NDSP_TIMEFRAME_LAYER_CONTRACT_V121__ = {
    version: VERSION,
    contractVersion: CONTRACT_VERSION,
    registry: REGISTRY,
    contracts: [],
    contractMap: {},
    payload: null,
    lastEnvelope: null,
    mappedCardCount: 0,
    lastAppliedAt: 0,
    lastError: "",
    refresh: refresh,
    rebind: function () { scheduleApply(0); }
  };

  startObserver();
  window.addEventListener("pageshow", function () { refresh(); scheduleApply(120); });
  window.addEventListener("popstate", function () { refresh(); });
  window.addEventListener("storage", function (event) { if (event.key === CONTEXT_KEY) refresh(); });
  document.addEventListener("ndsp:context-locked", refresh);
  document.addEventListener("ndsp:timeframe-change", refresh);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      ensureStyle();
      refresh();
      scheduleApply(300);
    });
  } else {
    ensureStyle();
    refresh();
    scheduleApply(300);
  }

  setTimeout(refresh, 700);
  setTimeout(function () { scheduleApply(0); }, 1600);
  setTimeout(function () { scheduleApply(0); }, 3200);
})();
