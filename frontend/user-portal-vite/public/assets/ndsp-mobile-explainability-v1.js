(() => {
  'use strict';

  const VERSION = '20260714-v1';
  const TECH_KEYS = [
    'governing_direction',
    'governing_source',
    'timing_rule_applied',
    'asset_managers_weekly_alignment',
    'correction_state',
    'leveraged_funds_weekly_alignment',
    'correction_risk',
    'readiness_allowed'
  ];

  const labels = {
    governing_direction: 'الاتجاه الحاكم',
    governing_source: 'مصدر القراءة الحاكمة',
    timing_rule_applied: 'تطبيق قاعدة التوقيت',
    asset_managers_weekly_alignment: 'توافق مديري الأصول أسبوعيًا',
    correction_state: 'حالة التصحيح',
    leveraged_funds_weekly_alignment: 'توافق الصناديق ذات الرافعة أسبوعيًا',
    correction_risk: 'مخاطر التصحيح',
    readiness_allowed: 'جاهزية الانتقال للمرحلة التالية'
  };

  const maps = {
    governing_direction: {
      unknown: 'غير محسوم',
      bullish: 'صاعد',
      bearish: 'هابط',
      neutral: 'محايد',
      mixed: 'مختلط'
    },
    governing_source: {
      asset_managers_overall: 'مديرو الأصول — القراءة العامة',
      asset_managers_weekly: 'مديرو الأصول — القراءة الأسبوعية',
      leveraged_funds_overall: 'الصناديق ذات الرافعة — القراءة العامة',
      leveraged_funds_weekly: 'الصناديق ذات الرافعة — القراءة الأسبوعية',
      commercials_overall: 'التجاريون — القراءة العامة',
      non_commercials_overall: 'غير التجاريين — القراءة العامة',
      unknown: 'غير محدد'
    },
    correction_state: {
      active: 'نشط',
      inactive: 'غير نشط',
      pending: 'قيد الانتظار',
      completed: 'مكتمل',
      unknown: 'غير محدد'
    },
    correction_risk: {
      elevated: 'مرتفعة',
      high: 'مرتفعة',
      moderate: 'متوسطة',
      low: 'منخفضة',
      unknown: 'غير محددة'
    }
  };

  const boolLabels = {
    timing_rule_applied: ['مطبقة', 'غير مطبقة'],
    asset_managers_weekly_alignment: ['متحقق', 'غير متحقق'],
    leveraged_funds_weekly_alignment: ['متحقق', 'غير متحقق'],
    readiness_allowed: ['مسموحة', 'غير مسموحة حاليًا']
  };

  function textOf(el) {
    return (el?.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function normalizeJsonText(raw) {
    if (!raw) return '';
    let text = raw.trim();
    text = text.replace(/^```(?:json)?/i, '').replace(/```$/i, '').trim();
    return text;
  }

  function parseTechnicalJson(raw) {
    const text = normalizeJsonText(raw);
    if (!text || !TECH_KEYS.some((key) => text.includes(`"${key}"`) || text.includes(key))) {
      return null;
    }

    const candidates = [text];
    const firstBrace = text.indexOf('{');
    const lastBrace = text.lastIndexOf('}');
    if (firstBrace >= 0 && lastBrace > firstBrace) {
      candidates.push(text.slice(firstBrace, lastBrace + 1));
    }

    for (const candidate of candidates) {
      try {
        const parsed = JSON.parse(candidate);
        if (parsed && typeof parsed === 'object' && TECH_KEYS.some((key) => key in parsed)) {
          return parsed;
        }
      } catch (_) {}
    }

    return null;
  }

  function displayValue(key, value) {
    if (typeof value === 'boolean' && boolLabels[key]) {
      return value ? boolLabels[key][0] : boolLabels[key][1];
    }
    if (value === null || value === undefined || value === '') return 'غير متوفر';
    const normalized = String(value).toLowerCase();
    return maps[key]?.[normalized] || String(value).replaceAll('_', ' ');
  }

  function valueState(key, value) {
    if (key === 'readiness_allowed') return value === true ? 'ok' : 'warn';
    if (key === 'correction_risk') {
      const v = String(value).toLowerCase();
      if (['elevated', 'high'].includes(v)) return 'danger';
      if (v === 'moderate') return 'warn';
      if (v === 'low') return 'ok';
    }
    if (typeof value === 'boolean') return value ? 'ok' : 'muted';
    if (String(value).toLowerCase() === 'unknown') return 'muted';
    return 'normal';
  }

  function buildSummary(data) {
    const reasons = [];
    if (data.governing_direction === 'unknown') reasons.push('الاتجاه الحاكم غير محسوم');
    if (data.timing_rule_applied === false) reasons.push('قاعدة التوقيت لم تُطبق بعد');
    if (data.asset_managers_weekly_alignment === false) reasons.push('توافق مديري الأصول الأسبوعي غير متحقق');
    if (data.leveraged_funds_weekly_alignment === false) reasons.push('توافق الصناديق ذات الرافعة غير متحقق');
    if (['elevated', 'high'].includes(String(data.correction_risk).toLowerCase())) reasons.push('مخاطر التصحيح مرتفعة');
    if (data.readiness_allowed === false) reasons.push('الجاهزية غير مسموحة حاليًا');

    if (!reasons.length) {
      return 'تمت قراءة المخرجات التقنية، ولا توجد عوائق رئيسية ظاهرة في هذه الوحدة.';
    }

    return `القراءة ما زالت تحت المراجعة: ${reasons.join('، ')}.`;
  }

  function createRow(key, value) {
    const row = document.createElement('div');
    row.className = 'ndsp-explainability-row';

    const label = document.createElement('span');
    label.className = 'ndsp-explainability-label';
    label.textContent = labels[key] || key;

    const result = document.createElement('span');
    result.className = `ndsp-explainability-value is-${valueState(key, value)}`;
    result.textContent = displayValue(key, value);

    row.append(label, result);
    return row;
  }

  function findCard(start) {
    let current = start;
    let fallback = start.parentElement;
    for (let i = 0; current && i < 8; i += 1, current = current.parentElement) {
      if (!(current instanceof HTMLElement)) continue;
      const rect = current.getBoundingClientRect();
      const style = getComputedStyle(current);
      const radius = parseFloat(style.borderRadius || '0');
      if (rect.width >= 240 && rect.height >= 120 && rect.height < window.innerHeight * 1.7 && radius >= 10) {
        fallback = current;
        if (/الأسباب والمخرجات|TDL|اتجاه السوق|بوابة التصحيح/.test(textOf(current))) return current;
      }
    }
    return fallback;
  }

  function fixContradictoryMessage(card) {
    if (!card) return;
    const elements = card.querySelectorAll('p, span, div, li');
    for (const el of elements) {
      if (el.children.length > 0) continue;
      const t = textOf(el);
      if (t === 'لا توجد أسباب إضافية' || t.includes('لا توجد أسباب إضافية')) {
        el.textContent = 'الأسباب والنتائج موضحة أدناه.';
        el.classList.add('ndsp-reason-message-fixed');
      }
    }
  }

  function enhanceTechnicalBlock(block) {
    if (!(block instanceof HTMLElement) || block.dataset.ndspExplainabilityDone === VERSION) return;

    const raw = block.textContent || '';
    const data = parseTechnicalJson(raw);
    if (!data) return;

    block.dataset.ndspExplainabilityDone = VERSION;
    const card = findCard(block);
    card?.classList.add('ndsp-card-has-explainability');
    fixContradictoryMessage(card);

    const panel = document.createElement('section');
    panel.className = 'ndsp-explainability-panel';
    panel.setAttribute('dir', 'rtl');

    const summary = document.createElement('p');
    summary.className = 'ndsp-explainability-summary';
    summary.textContent = buildSummary(data);
    panel.appendChild(summary);

    const rows = document.createElement('div');
    rows.className = 'ndsp-explainability-rows';
    TECH_KEYS.forEach((key) => {
      if (Object.prototype.hasOwnProperty.call(data, key)) rows.appendChild(createRow(key, data[key]));
    });
    panel.appendChild(rows);

    const details = document.createElement('details');
    details.className = 'ndsp-technical-details';

    const toggle = document.createElement('summary');
    toggle.textContent = 'عرض التفاصيل التقنية';

    const pre = document.createElement('pre');
    pre.className = 'ndsp-technical-json';
    pre.textContent = JSON.stringify(data, null, 2);

    details.append(toggle, pre);
    panel.appendChild(details);

    block.hidden = true;
    block.setAttribute('aria-hidden', 'true');
    block.insertAdjacentElement('afterend', panel);
  }

  function addStatusClass(card, text) {
    if (!card || card.dataset.ndspStatusDone === VERSION) return;
    card.dataset.ndspStatusDone = VERSION;
    card.classList.add('ndsp-status-card');

    if (/مكتمل|جاهز|مسموحة/.test(text)) card.classList.add('is-complete');
    else if (/محظور|إلغاء|خطر مرتفع|مخاطر.*مرتفعة/.test(text)) card.classList.add('is-blocked');
    else if (/تحت المراجعة|تحت المتابعة|مراقبة|انتظار/.test(text)) card.classList.add('is-review');
    else card.classList.add('is-neutral');
  }

  function classifyCards() {
    const headings = document.querySelectorAll('h1, h2, h3, h4, [role="heading"]');
    headings.forEach((heading) => {
      const t = textOf(heading);
      if (!/TDL|اتجاه السوق|بوابة التصحيح|NMP|محامي الشيطان|المخاطر|الإشارة/.test(t)) return;
      const card = findCard(heading);
      addStatusClass(card, textOf(card));
    });
  }

  function fixAccordionLabels() {
    const controls = document.querySelectorAll('button, summary, [role="button"], [aria-expanded]');
    controls.forEach((control) => {
      const t = textOf(control);
      if (!t.includes('الأسباب والمخرجات')) return;
      if (control.dataset.ndspAccordionDone === VERSION) return;

      control.dataset.ndspAccordionDone = VERSION;
      control.classList.add('ndsp-accordion-control');

      const cleaned = t.replace(/[▼▲◀▶►◄]\s*/g, '').trim();
      if (cleaned && cleaned !== t && control.children.length === 0) control.textContent = cleaned;

      const icon = document.createElement('span');
      icon.className = 'ndsp-accordion-chevron';
      icon.setAttribute('aria-hidden', 'true');
      control.prepend(icon);

      const update = () => {
        const expanded = control.getAttribute('aria-expanded');
        if (expanded !== null) {
          control.classList.toggle('is-open', expanded === 'true');
          return;
        }
        if (control.tagName.toLowerCase() === 'summary') {
          control.classList.toggle('is-open', Boolean(control.parentElement?.open));
        }
      };

      update();
      control.addEventListener('click', () => requestAnimationFrame(update));
    });
  }

  function findHeader() {
    const candidates = [...document.querySelectorAll('header, nav, section, div')]
      .filter((el) => {
        const t = textOf(el);
        if (!t.includes('NDSP') || !t.includes('القائمة') || !(t.includes('AR') && t.includes('EN'))) return false;
        const r = el.getBoundingClientRect();
        return r.width >= Math.min(300, window.innerWidth * 0.75) && r.height >= 80 && r.height <= 330;
      })
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return ar.width * ar.height - br.width * br.height;
      });

    return candidates[0] || document.querySelector('header');
  }

  function fixHeader() {
    const header = findHeader();
    if (!header || header.dataset.ndspHeaderDone === VERSION) return;
    header.dataset.ndspHeaderDone = VERSION;
    header.classList.add('ndsp-mobile-header-fix');
    document.documentElement.classList.add('ndsp-mobile-ui-fix-active');
  }

  function processAll() {
    document.querySelectorAll('pre, code').forEach(enhanceTechnicalBlock);
    classifyCards();
    fixAccordionLabels();
    fixHeader();
  }

  let scheduled = false;
  function scheduleProcess() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      processAll();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processAll, { once: true });
  } else {
    processAll();
  }

  const observer = new MutationObserver(scheduleProcess);
  observer.observe(document.documentElement, { childList: true, subtree: true });

  window.addEventListener('resize', scheduleProcess, { passive: true });
})();
