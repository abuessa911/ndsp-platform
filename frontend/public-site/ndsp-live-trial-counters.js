(function () {
  "use strict";

  if (window.__NDSP_SINGLE_VISIBLE_COUNTERS_FINAL__) return;
  window.__NDSP_SINGLE_VISIBLE_COUNTERS_FINAL__ = true;

  const endpoints = [
    window.location.origin + "/api/trial/status?v=" + Date.now(),
    "https://ndsp.app/api/trial/status?v=" + Date.now(),
    "https://api.ndsp.app/api/trial/status?v=" + Date.now()
  ];

  const styleId = "ndsp-single-visible-counter-style-final";
  if (!document.getElementById(styleId)) {
    const style = document.createElement("style");
    style.id = styleId;
    style.textContent = `
      .ndsp-live-counter-single {
        display: inline-block !important;
        direction: ltr !important;
        unicode-bidi: isolate !important;
        font-weight: 900 !important;
        color: #f6d776 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
      }
      .ndsp-counter-cleaned-card .num {
        overflow: visible !important;
      }
      .ndsp-counter-cleaned-card .ndsp-seat-live-ratio,
      .ndsp-counter-cleaned-card .ndsp-seat-live-total {
        display: none !important;
      }
    `;
    document.head.appendChild(style);
  }

  function normalizeDigits(s) {
    return String(s || "")
      .replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); })
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function removeOldOverlays() {
    document.querySelectorAll(".ndsp-seat-live-ratio,.ndsp-seat-live-total").forEach(function (el) {
      el.remove();
    });

    document.querySelectorAll("[data-ndsp-stale-counter-hidden]").forEach(function (el) {
      el.removeAttribute("data-ndsp-stale-counter-hidden");
      el.style.visibility = "";
      el.style.opacity = "";
    });
  }

  function findCard(labelRegex) {
    const nodes = Array.from(document.querySelectorAll("section,article,div,li,td,th,p,span,strong,b"));
    const candidates = [];

    nodes.forEach(function (node) {
      const t = normalizeDigits(node.innerText || node.textContent || "");
      if (!t || t.length > 500) return;
      if (!labelRegex.test(t)) return;

      let cur = node;
      for (let i = 0; i < 8 && cur; i++) {
        const ct = normalizeDigits(cur.innerText || cur.textContent || "");
        const hasNum = cur.querySelector && cur.querySelector(".num");
        const hasCounterText = /[0-9٠-٩]+\s*\/\s*[0-9٠-٩]+|[0-9٠-٩]+/.test(ct);
        const looksLikeSeat = /مقعد|مقاعد|تجربة|seat|trial|خاص|مميز|متخصص|أكاديمي|اكاديمي|مبتدئ|عادي|إجمالي|اجمالي/i.test(ct);

        if (looksLikeSeat && (hasNum || hasCounterText)) {
          candidates.push(cur);
          break;
        }

        cur = cur.parentElement;
      }
    });

    candidates.sort(function (a, b) {
      const at = normalizeDigits(a.innerText || a.textContent || "");
      const bt = normalizeDigits(b.innerText || b.textContent || "");
      return at.length - bt.length;
    });

    return candidates[0] || null;
  }

  function putValueIntoCard(card, value, key) {
    if (!card) return false;

    card.classList.add("ndsp-counter-cleaned-card");

    const html = '<span class="ndsp-live-counter-single" data-ndsp-counter="' + key + '" data-ndsp-live-value="' + String(value) + '">' + String(value) + '</span>';

    let target = null;

    if (card.querySelector) {
      target = card.querySelector(".num");
    }

    if (!target && card.classList && card.classList.contains("num")) {
      target = card;
    }

    if (!target) {
      const numeric = Array.from(card.querySelectorAll("span,strong,b,h1,h2,h3,h4,h5,div"))
        .filter(function (el) {
          const t = normalizeDigits(el.textContent || "");
          return /^[0-9]+$/.test(t) || /^[0-9]+\s*\/\s*[0-9]+$/.test(t);
        })
        .sort(function (a, b) {
          return normalizeDigits(a.textContent).length - normalizeDigits(b.textContent).length;
        });

      target = numeric[0] || card;
    }

    target.innerHTML = html;
    target.setAttribute("data-ndsp-counter-slot", key);

    return true;
  }

  function forceKnownIds(d) {
    const mapping = {
      s1: `${d.ordinary_used}/${d.ordinary_limit}`,
      s2: `${d.professional_used}/${d.professional_limit}`,
      s3: `${d.private_invite_used}/${d.private_invite_limit}`
    };

    Object.keys(mapping).forEach(function (id) {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = '<span class="ndsp-live-counter-single" data-ndsp-counter="' + id + '">' + mapping[id] + '</span>';
    });
  }

  function applyCounters(d) {
    removeOldOverlays();

    const privateValue = `${d.private_invite_used}/${d.private_invite_limit}`;
    const professionalValue = `${d.professional_used}/${d.professional_limit}`;
    const ordinaryValue = `${d.ordinary_used}/${d.ordinary_limit}`;
    const totalValue = `${d.total_used}`;

    forceKnownIds(d);

    const privateCard = findCard(/خاص|مميز|دعوة|private|premium|invite/i);
    const professionalCard = findCard(/متخصص|أكاديمي|اكاديمي|professional|academic|specialist|analyst/i);
    const ordinaryCard = findCard(/مبتدئ|عادي|ordinary|beginner/i);
    const totalCard = findCard(/إجمالي|اجمالي|المجموع|total|capacity/i);

    const privateOk = putValueIntoCard(privateCard, privateValue, "private_invite_ratio");
    const professionalOk = putValueIntoCard(professionalCard, professionalValue, "professional_ratio");
    const ordinaryOk = putValueIntoCard(ordinaryCard, ordinaryValue, "ordinary_ratio");
    const totalOk = putValueIntoCard(totalCard, totalValue, "total_used");

    document.documentElement.setAttribute("data-ndsp-counters-source", "official-api-single-visible");
    document.documentElement.setAttribute("data-ndsp-private-card-fixed", String(privateOk));
    document.documentElement.setAttribute("data-ndsp-professional-card-fixed", String(professionalOk));
    document.documentElement.setAttribute("data-ndsp-ordinary-card-fixed", String(ordinaryOk));
    document.documentElement.setAttribute("data-ndsp-total-card-fixed", String(totalOk));
    document.documentElement.setAttribute("data-ndsp-trial-private-ratio", privateValue);
    document.documentElement.setAttribute("data-ndsp-trial-professional-ratio", professionalValue);
    document.documentElement.setAttribute("data-ndsp-trial-ordinary-ratio", ordinaryValue);
    document.documentElement.setAttribute("data-ndsp-trial-total-used", String(d.total_used));

    window.NDSP_TRIAL_COUNTERS_OFFICIAL = {
      fetched_at: new Date().toISOString(),
      data: d
    };
  }

  async function fetchStatus() {
    let lastError = null;

    for (const url of endpoints) {
      try {
        const r = await fetch(url, {
          method: "GET",
          cache: "no-store",
          credentials: "omit",
          headers: {
            "Accept": "application/json",
            "Cache-Control": "no-cache"
          }
        });

        if (!r.ok) {
          lastError = new Error("HTTP " + r.status + " " + url);
          continue;
        }

        const d = await r.json();
        if (d && d.total_capacity !== undefined) return d;
      } catch (e) {
        lastError = e;
      }
    }

    throw lastError || new Error("trial status unavailable");
  }

  async function refreshCounters() {
    try {
      const d = await fetchStatus();
      applyCounters(d);
      window.dispatchEvent(new CustomEvent("ndsp:trial-counters-updated", { detail: d }));
    } catch (e) {
      console.warn("[NDSP] single visible trial counters failed", e);
      document.documentElement.setAttribute("data-ndsp-counters-source", "failed");
    }
  }

  try {
    localStorage.removeItem("ndsp_trial_status");
    localStorage.removeItem("trial_status");
    sessionStorage.removeItem("ndsp_trial_status");
    sessionStorage.removeItem("trial_status");
  } catch (_) {}

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.getRegistrations()
      .then(function (regs) {
        regs.forEach(function (r) {
          r.unregister().catch(function () {});
        });
      })
      .catch(function () {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", refreshCounters);
  } else {
    refreshCounters();
  }

  setTimeout(refreshCounters, 300);
  setTimeout(refreshCounters, 900);
  setTimeout(refreshCounters, 1800);
  setTimeout(refreshCounters, 3200);
  setInterval(refreshCounters, 3000);

  try {
    const observer = new MutationObserver(function () {
      clearTimeout(window.__NDSP_SINGLE_VISIBLE_COUNTER_TIMER__);
      window.__NDSP_SINGLE_VISIBLE_COUNTER_TIMER__ = setTimeout(refreshCounters, 180);
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  } catch (_) {}
})();
