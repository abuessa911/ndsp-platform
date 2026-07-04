/* NDSP_PHASE4_CONTRACT_RUNTIME_V1_START */
(function () {
  'use strict';

  const DEFAULT_TEXT = 'غير متاح من مصدر البيانات';
  const CONTRACT_VERSION = 'NDSP_PHASE4_DATA_CONTRACT_V1';

  function safeGet(key, fallback) {
    try { return localStorage.getItem(key) || fallback; } catch (_) { return fallback; }
  }

  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (_) {}
  }

  function param(name) {
    return new URLSearchParams(window.location.search).get(name);
  }

  function normalizeSymbol() {
    const raw = param('symbol') || safeGet('ndsp_symbol', safeGet('ndsp_selected_symbol', 'BTCUSDT'));
    const symbol = String(raw || 'BTCUSDT').trim().toUpperCase();
    safeSet('ndsp_symbol', symbol);
    safeSet('ndsp_selected_symbol', symbol);
    return symbol;
  }

  function setLang(lang) {
    const next = lang === 'en' ? 'en' : 'ar';
    document.documentElement.dataset.lang = next;
    document.documentElement.lang = next;
    document.documentElement.dir = next === 'en' ? 'ltr' : 'rtl';
    safeSet('ndsp_lang', next);
  }

  function getPath(obj, path, fallback) {
    const parts = String(path || '').split('.');
    let cur = obj;
    for (const part of parts) {
      if (cur && Object.prototype.hasOwnProperty.call(cur, part)) cur = cur[part];
      else return fallback;
    }
    return cur == null || cur === '' ? fallback : cur;
  }

  function first(obj, paths, fallback) {
    for (const p of paths) {
      const value = getPath(obj, p, undefined);
      if (value !== undefined && value !== null && value !== '') return value;
    }
    return fallback;
  }

  function fmt(value) {
    if (value === undefined || value === null || value === '') return DEFAULT_TEXT;
    if (typeof value === 'number') return Number.isFinite(value) ? value.toLocaleString('en-US', { maximumFractionDigits: 4 }) : DEFAULT_TEXT;
    if (Array.isArray(value)) return value.length ? value.join('، ') : DEFAULT_TEXT;
    if (typeof value === 'object') return DEFAULT_TEXT;
    return String(value);
  }

  function publicState(value) {
    const s = fmt(value);
    const map = {
      UNDER_MONITORING: 'تحت المتابعة',
      ALLOWED: 'مسموح بالقراءة',
      BLOCKED: 'محجوب بعامل حذر',
      CAUTION: 'حذر',
      NEUTRAL: 'محايد',
      SUPPORTIVE: 'داعم',
      PRESSURE: 'ضغط',
      STRONG: 'قوي',
      WEAK: 'ضعيف'
    };
    return map[s] || s;
  }

  function normalize(payload, symbol) {
    const data = payload || {};
    const macro = data.macro || data.usd_macro || {};

    const decisionQuality = first(data, ['decision_quality', 'quality', 'score', 'summary.decision_quality'], DEFAULT_TEXT);
    const scenarioState = publicState(first(data, ['scenario.scenario_state', 'scenario_state', 'state'], DEFAULT_TEXT));
    const directionalContext = first(data, ['scenario.scenario_directional_context', 'directional_context', 'directional_bias', 'summary.directional_context'], DEFAULT_TEXT);
    const cautionReason = first(data, ['caution_reason', 'risk.caution_reason', 'scenario.scenario_risk_note', 'scenario.risk_note'], DEFAULT_TEXT);
    const sanitizedSummary = first(data, ['sanitized_summary', 'summary.sanitized_summary', 'summary', 'scenario.scenario_summary'], DEFAULT_TEXT);
    const usdImpact = first(data, ['macro.usd_impact', 'usd_impact', 'summary.usd_impact'], DEFAULT_TEXT);
    const usdState = publicState(first(data, ['macro.usd_state', 'usd_state', 'dollar_state'], 'تحت المراقبة'));

    return {
      contract_version: CONTRACT_VERSION,
      identity: {
        symbol: first(data, ['instrument.symbol', 'symbol'], symbol),
        market: first(data, ['instrument.market', 'market'], 'غير محدد'),
        timeframe: first(data, ['instrument.timeframe', 'timeframe'], 'غير محدد'),
        updated_at: first(data, ['scenario.scenario_last_updated', 'updated_at', 'timestamp'], new Date().toISOString())
      },
      modes: {
        display_mode: param('display') || safeGet('ndsp_display_mode', 'beginner'),
        reading_horizon: param('horizon') || safeGet('ndsp_reading_horizon', 'investor')
      },
      decision: {
        scenario_state: scenarioState,
        decision_quality: fmt(decisionQuality),
        directional_context: fmt(directionalContext),
        sanitized_summary: fmt(sanitizedSummary),
        caution_reason: fmt(cautionReason)
      },
      levels: {
        activation: fmt(first(data, ['scenario.scenario_activation_level', 'levels.activation', 'activation_level'], undefined)),
        arrival: fmt(first(data, ['scenario.scenario_arrival_level', 'levels.arrival', 'arrival_level'], undefined)),
        review_zone: fmt(first(data, ['scenario.scenario_review_zone', 'levels.review_zone', 'review_zone'], undefined)),
        invalidation: fmt(first(data, ['scenario.scenario_invalidation_level', 'levels.invalidation', 'invalidation_level'], undefined))
      },
      nmp: {
        state: fmt(first(data, ['nmp.state', 'nmp_state', 'scenario.nmp_state'], 'تحت المراجعة')),
        zone: fmt(first(data, ['nmp.zone', 'nmp_zone', 'scenario.nmp_zone'], undefined)),
        note: fmt(first(data, ['nmp.note', 'nmp_note'], 'لا يتم عرض منطقة NMP إلا عند توفرها من مصدر البيانات.'))
      },
      radar: {
        market_state: fmt(first(data, ['market_state', 'scenario.market_state', 'directional_bias'], directionalContext)),
        risk_state: fmt(first(data, ['risk_state', 'scenario.risk_state'], cautionReason)),
        levels_state: fmt(first(data, ['levels.state'], 'مستويات مرجعية للمراقبة')),
        nmp_state: fmt(first(data, ['nmp.state', 'nmp_state'], 'تحت المراجعة')),
        horizon_state: fmt(first(data, ['scenario.scenario_confidence_band', 'horizon_strength', 'confidence_band'], DEFAULT_TEXT)),
        devil_state: fmt(first(data, ['devil_state', 'risk.devil_state'], 'لا يوجد عامل حجب معلن'))
      },
      usd_macro: {
        usd_state: usdState,
        usd_impact: fmt(usdImpact),
        macro_events: Array.isArray(macro.events) ? macro.events : [],
        metals_impact: fmt(first(data, ['macro.metals_impact', 'usd_macro.metals_impact'], 'يعرض عند توفر بيانات الدولار.')),
        fx_impact: fmt(first(data, ['macro.fx_impact', 'usd_macro.fx_impact'], 'يعرض عند توفر بيانات الدولار.')),
        crypto_impact: fmt(first(data, ['macro.crypto_impact', 'usd_macro.crypto_impact'], 'يعرض عند توفر بيانات الدولار.')),
        indices_commodities_impact: fmt(first(data, ['macro.indices_commodities_impact', 'usd_macro.indices_commodities_impact'], 'يعرض عند توفر بيانات الدولار.'))
      },
      daily_brief: {
        headline: fmt(first(data, ['daily_brief.headline'], 'الإيجاز اليومي ينتظر بيانات المصدر.')),
        bullets: Array.isArray(data.daily_brief && data.daily_brief.bullets) ? data.daily_brief.bullets : [],
        next_watch: fmt(first(data, ['daily_brief.next_watch'], 'راقب تحديث القراءة عند تغير السعر أو الماكرو.'))
      },
      monitoring: {
        watchlist: JSON.parse(safeGet('ndsp_watchlist', '[]') || '[]'),
        alerts: JSON.parse(safeGet('ndsp_alerts', '[]') || '[]'),
        completed_readings: JSON.parse(safeGet('ndsp_completed_readings', '[]') || '[]')
      },
      disclaimers: {
        decision_support_only: 'هذه قراءة دعم قرار وليست توصية مالية أو أمر تنفيذ.'
      }
    };
  }

  async function fetchPayload(symbol) {
    const endpoints = [
      '/api/decision/quality-live?symbol=' + encodeURIComponent(symbol),
      '/decision/quality-live?symbol=' + encodeURIComponent(symbol),
      'https://api.ndsp.app/api/decision/quality-live?symbol=' + encodeURIComponent(symbol)
    ];

    let lastError = '';

    for (const endpoint of endpoints) {
      try {
        const res = await fetch(endpoint, { cache: 'no-store' });
        if (!res.ok) { lastError = endpoint + ' HTTP ' + res.status; continue; }
        const json = await res.json();
        if (json && (json.ok === true || json.instrument || json.scenario)) return { endpoint, json };
        lastError = endpoint + ' invalid payload';
      } catch (error) {
        lastError = endpoint + ' ' + (error && error.message ? error.message : 'fetch failed');
      }
    }

    throw new Error(lastError || 'No data source responded');
  }

  function bindText(contract) {
    document.querySelectorAll('[data-contract-text]').forEach(function (node) {
      const key = node.getAttribute('data-contract-text');
      node.textContent = fmt(getPath(contract, key, DEFAULT_TEXT));
    });

    document.querySelectorAll('[data-contract-list]').forEach(function (node) {
      const key = node.getAttribute('data-contract-list');
      const values = getPath(contract, key, []);
      node.innerHTML = '';

      if (Array.isArray(values) && values.length) {
        values.forEach(function (item) {
          const li = document.createElement('li');
          li.textContent = fmt(item);
          node.appendChild(li);
        });
      } else {
        const li = document.createElement('li');
        li.textContent = 'لا توجد عناصر معلنة من مصدر البيانات.';
        node.appendChild(li);
      }
    });
  }

  function bindModes(contract) {
    const display = contract.modes.display_mode === 'professional' ? 'professional' : 'beginner';
    const horizon = contract.modes.reading_horizon === 'tactical' ? 'tactical' : 'investor';

    safeSet('ndsp_display_mode', display);
    safeSet('ndsp_reading_horizon', horizon);

    document.documentElement.dataset.ndspDisplayMode = display;
    document.documentElement.dataset.ndspReadingHorizon = horizon;

    document.querySelectorAll('[data-ndsp-display-mode]').forEach(function (btn) {
      btn.classList.toggle('is-active', btn.getAttribute('data-ndsp-display-mode') === display);
      btn.addEventListener('click', function () {
        const next = btn.getAttribute('data-ndsp-display-mode') === 'professional' ? 'professional' : 'beginner';
        safeSet('ndsp_display_mode', next);
        const url = new URL(location.href);
        url.searchParams.set('display', next);
        location.href = url.pathname + url.search;
      });
    });

    document.querySelectorAll('[data-ndsp-reading-horizon]').forEach(function (btn) {
      btn.classList.toggle('is-active', btn.getAttribute('data-ndsp-reading-horizon') === horizon);
      btn.addEventListener('click', function () {
        const next = btn.getAttribute('data-ndsp-reading-horizon') === 'tactical' ? 'tactical' : 'investor';
        safeSet('ndsp_reading_horizon', next);
        const url = new URL(location.href);
        url.searchParams.set('horizon', next);
        location.href = url.pathname + url.search;
      });
    });
  }

  function bindAssets(symbol) {
    document.querySelectorAll('[data-ndsp-symbol]').forEach(function (node) {
      node.textContent = symbol;
    });

    document.querySelectorAll('[data-ndsp-symbol-option]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const next = String(btn.getAttribute('data-ndsp-symbol-option') || symbol).toUpperCase();
        safeSet('ndsp_symbol', next);
        safeSet('ndsp_selected_symbol', next);
        location.href = '/decision-center.html?symbol=' + encodeURIComponent(next);
      });
    });

    document.querySelectorAll('a[href]').forEach(function (a) {
      const href = a.getAttribute('href') || '';
      if (!href.startsWith('/')) return;
      if (!/decision-center|decision-radar|nmp|daily-brief|usd-pulse|dollar-impact/.test(href)) return;
      const url = new URL(href, location.origin);
      if (!url.searchParams.get('symbol')) url.searchParams.set('symbol', symbol);
      a.setAttribute('href', url.pathname + url.search);
    });
  }

  function bindStatus(ok, sourceOrError) {
    document.querySelectorAll('[data-contract-status]').forEach(function (node) {
      if (ok) {
        node.textContent = 'تم تحديث القراءة من مصدر البيانات.';
        node.classList.remove('ndsp-contract-error');
        node.classList.add('ndsp-contract-ok');
      } else {
        node.textContent = 'تعذر تحديث البيانات الآن. الصفحة تعرض هيكل القراءة دون اختراع قيم. السبب: ' + sourceOrError;
        node.classList.remove('ndsp-contract-ok');
        node.classList.add('ndsp-contract-error');
      }
    });
  }

  function bindLocalMonitoring(contract) {
    const symbol = contract.identity.symbol;

    document.querySelectorAll('[data-watchlist-add]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        let list = [];
        try { list = JSON.parse(safeGet('ndsp_watchlist', '[]') || '[]'); } catch (_) {}
        if (!list.includes(symbol)) list.push(symbol);
        safeSet('ndsp_watchlist', JSON.stringify(list));
        location.reload();
      });
    });
  }

  async function main() {
    setLang(safeGet('ndsp_lang', 'ar'));

    document.addEventListener('click', function (event) {
      const target = event.target && event.target.closest('[data-ndsp-lang-toggle]');
      if (!target) return;
      const current = document.documentElement.dataset.lang === 'en' ? 'en' : 'ar';
      setLang(current === 'en' ? 'ar' : 'en');
    });

    const symbol = normalizeSymbol();
    bindAssets(symbol);

    let contract = normalize({}, symbol);
    let ok = false;
    let source = 'لم يتم الاتصال بالمصدر بعد';

    try {
      const result = await fetchPayload(symbol);
      contract = normalize(result.json, symbol);
      ok = true;
      source = result.endpoint;
    } catch (error) {
      source = error && error.message ? error.message : 'غير معروف';
    }

    window.NDSP_DECISION_CONTRACT = contract;

    bindModes(contract);
    bindText(contract);
    bindStatus(ok, source);
    bindLocalMonitoring(contract);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', main);
  else main();
})();
/* NDSP_PHASE4_CONTRACT_RUNTIME_V1_END */
