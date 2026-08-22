(() => {
  'use strict';

  if (window.__NDSP_SELECTION_SUMMARY_TIMEFRAME_SYNC_V113__) return;
  window.__NDSP_SELECTION_SUMMARY_TIMEFRAME_SYNC_V113__ = true;

  const frames = new Set(['15m', '1h', '4h', 'daily', 'weekly', 'monthly']);
  let pending = false;

  const visible = (el) => {
    if (!(el instanceof Element)) return false;
    const style = getComputedStyle(el);
    const box = el.getBoundingClientRect();
    return style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      box.width > 2 &&
      box.height > 2;
  };

  const selectedFrame = () => {
    const selectors = [
      '[data-timeframe].selected',
      '[data-timeframe][aria-pressed="true"]',
      '[data-timeframe][data-selected="true"]'
    ];

    for (const selector of selectors) {
      const el = [...document.querySelectorAll(selector)].find(visible);
      const value = String(el?.getAttribute('data-timeframe') || '').toLowerCase();
      if (frames.has(value)) return value;
    }

    const urlValue = String(new URL(location.href).searchParams.get('timeframe') || '').toLowerCase();
    return frames.has(urlValue) ? urlValue : '';
  };

  const sync = () => {
    const frame = selectedFrame();
    if (!frame) return;

    const summaries = [...document.querySelectorAll('.selectionSummary')].filter(visible);

    for (const summary of summaries) {
      const root = summary.querySelector('.summaryTokens');
      if (!root) continue;

      const tokens = [...root.children];
      let target = tokens.find((el) => frames.has(String(el.textContent || '').trim().toLowerCase()));

      if (!target && tokens.length >= 5) target = tokens[2];
      if (!target) continue;

      if (String(target.textContent || '').trim().toLowerCase() !== frame) {
        target.textContent = frame;
      }

      target.setAttribute('data-ndsp-summary-timeframe-v113', frame);
      summary.setAttribute('data-ndsp-summary-frame-v113', frame);
    }
  };

  const schedule = () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => {
      pending = false;
      sync();
    });
  };

  document.addEventListener('click', (event) => {
    const button = event.target instanceof Element
      ? event.target.closest('[data-timeframe]')
      : null;

    if (!button) return;

    setTimeout(schedule, 0);
    setTimeout(schedule, 80);
    setTimeout(schedule, 250);
  }, true);

  const observer = new MutationObserver(schedule);

  const start = () => {
    observer.observe(document.querySelector('#app') || document.body, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ['class', 'aria-pressed', 'data-selected']
    });

    schedule();
    setTimeout(schedule, 500);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
