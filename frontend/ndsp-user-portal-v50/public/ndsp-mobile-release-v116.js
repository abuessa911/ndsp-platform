(() => {
  'use strict';

  if (window.__NDSP_MOBILE_RELEASE_V116__) return;
  window.__NDSP_MOBILE_RELEASE_V116__ = true;

  const mobile = () => window.matchMedia('(max-width: 820px)').matches;
  const frames = ['15m', '1h', '4h', 'daily', 'weekly', 'monthly'];
  const frameSet = new Set(frames);
  const percentPattern = /(?:[٠-٩0-9]+(?:[.,][٠-٩0-9]+)?\s*[%٪]|[%٪]\s*[٠-٩0-9]+(?:[.,][٠-٩0-9]+)?)/g;
  let scheduled = false;

  const normalized = (value) =>
    String(value || '')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();

  const latinDigits = (value) =>
    String(value || '').replace(/[٠-٩]/g, (digit) =>
      String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit))
    );

  const mapFrame = (element) => {
    if (!(element instanceof Element)) return '';

    const attr = normalized(
      element.getAttribute('data-timeframe') ||
      element.getAttribute('data-frame')
    );

    if (frameSet.has(attr)) return attr;

    const text = latinDigits(normalized(element.textContent));

    const map = new Map([
      ['15 دقيقة', '15m'],
      ['15m', '15m'],
      ['ساعة', '1h'],
      ['1h', '1h'],
      ['4 ساعات', '4h'],
      ['4h', '4h'],
      ['يومي', 'daily'],
      ['daily', 'daily'],
      ['أسبوعي', 'weekly'],
      ['اسبوعي', 'weekly'],
      ['weekly', 'weekly'],
      ['شهري', 'monthly'],
      ['monthly', 'monthly'],
    ]);

    return map.get(text) || '';
  };

  const visible = (element) => {
    if (!(element instanceof Element)) return false;
    const style = getComputedStyle(element);
    const box = element.getBoundingClientRect();

    return (
      style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      !element.hidden &&
      box.width > 2 &&
      box.height > 2
    );
  };

  const currentFrame = () => {
    const selectors = [
      '[data-timeframe].selected',
      '[data-timeframe][aria-pressed="true"]',
      '[data-timeframe][data-selected="true"]',
    ];

    for (const selector of selectors) {
      const element = [...document.querySelectorAll(selector)].find(visible);
      const frame = mapFrame(element);
      if (frame) return frame;
    }

    const urlFrame = normalized(
      new URL(location.href).searchParams.get('timeframe')
    );

    return frameSet.has(urlFrame) ? urlFrame : '';
  };

  const findTimeframePanel = () => {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,strong,b,div')]
      .filter((element) =>
        normalized(element.textContent).includes('اختر الفريم')
      );

    let best = null;
    let bestArea = Number.POSITIVE_INFINITY;

    for (const heading of headings) {
      let ancestor = heading;

      for (let depth = 0; ancestor && depth < 7; depth += 1) {
        const controls = [
          ...ancestor.querySelectorAll(
            'button,[role="button"],[data-timeframe],[data-frame]'
          ),
        ].filter((element) => mapFrame(element));

        const unique = new Set(controls.map(mapFrame));

        if (unique.size >= 6) {
          const box = ancestor.getBoundingClientRect();
          const area = Math.max(1, box.width * box.height);

          if (area < bestArea) {
            best = ancestor;
            bestArea = area;
          }

          break;
        }

        ancestor = ancestor.parentElement;
      }
    }

    return best;
  };

  const cleanDuplicateTimeframes = () => {
    const panel = findTimeframePanel();
    if (!panel) return;

    const controls = [
      ...panel.querySelectorAll(
        'button,[role="button"],[data-timeframe],[data-frame]'
      ),
    ].filter((element) => mapFrame(element));

    const byFrame = new Map();

    for (const control of controls) {
      const frame = mapFrame(control);
      if (!byFrame.has(frame)) byFrame.set(frame, []);
      byFrame.get(frame).push(control);
    }

    const selected = currentFrame();

    for (const frame of frames) {
      const list = byFrame.get(frame) || [];

      list.sort((left, right) => {
        const leftNative = left.hasAttribute('data-timeframe') ? 1 : 0;
        const rightNative = right.hasAttribute('data-timeframe') ? 1 : 0;

        if (leftNative !== rightNative) return rightNative - leftNative;

        const leftVisible = visible(left) ? 1 : 0;
        const rightVisible = visible(right) ? 1 : 0;

        if (leftVisible !== rightVisible) return rightVisible - leftVisible;
        return 0;
      });

      const keeper = list[0] || null;

      list.forEach((element, index) => {
        const duplicate = index > 0;

        element.classList.toggle(
          'ndsp-v116-duplicate-timeframe',
          duplicate
        );

        if (duplicate) {
          element.setAttribute('aria-hidden', 'true');
          element.setAttribute('tabindex', '-1');
          element.hidden = true;
          element.classList.remove('selected', 'active');
          element.setAttribute('aria-pressed', 'false');
          element.removeAttribute('data-selected');
        } else {
          element.hidden = false;
          element.removeAttribute('aria-hidden');

          if (
            selected &&
            frame !== selected &&
            (
              element.getAttribute('aria-pressed') === 'true' ||
              element.classList.contains('selected') ||
              element.classList.contains('active') ||
              element.getAttribute('data-selected') === 'true'
            )
          ) {
            element.setAttribute('aria-pressed', 'false');
            element.classList.remove('selected', 'active');
            element.removeAttribute('data-selected');
          }
        }
      });

      if (keeper && selected === frame) {
        keeper.classList.add('selected');
        keeper.setAttribute('aria-pressed', 'true');
        keeper.setAttribute('data-selected', 'true');
      }
    }

    panel.setAttribute('data-ndsp-v116-timeframe-panel', 'clean');
  };

  const exactTextElements = (wanted) =>
    [...document.querySelectorAll('body *')].filter((element) => {
      if (!(element instanceof Element)) return false;
      if (element.children.length > 2) return false;
      return normalized(element.textContent) === normalized(wanted);
    });

  const markContextStripStatic = () => {
    if (
      location.pathname !== '/portal.html' &&
      !document.querySelector('[data-context-locked="true"]')
    ) {
      return;
    }

    const labels = ['السوق', 'الأصل', 'الفريم', 'نوع القراءة'];
    const labelElements = labels
      .map((label) => exactTextElements(label)[0] || null)
      .filter(Boolean);

    if (labelElements.length < 4) return;

    const candidates = new Set();

    for (const label of labelElements) {
      let ancestor = label;

      for (let depth = 0; ancestor && depth < 7; depth += 1) {
        const text = normalized(ancestor.innerText);
        const containsAll = labels.every((item) =>
          text.includes(normalized(item))
        );

        if (containsAll) candidates.add(ancestor);
        ancestor = ancestor.parentElement;
      }
    }

    let best = null;
    let bestArea = Number.POSITIVE_INFINITY;

    for (const candidate of candidates) {
      const box = candidate.getBoundingClientRect();
      const area = Math.max(1, box.width * box.height);

      if (box.height < 540 && area < bestArea) {
        best = candidate;
        bestArea = area;
      }
    }

    if (!best) return;

    best.classList.add('ndsp-v116-context-static');
    best.setAttribute('data-ndsp-v116-context', 'static');

    let ancestor = best.parentElement;

    for (let depth = 0; ancestor && depth < 4; depth += 1) {
      const position = getComputedStyle(ancestor).position;
      const box = ancestor.getBoundingClientRect();

      if (
        (position === 'sticky' || position === 'fixed') &&
        box.height < 640
      ) {
        ancestor.classList.add('ndsp-v116-context-static-parent');
        ancestor.setAttribute(
          'data-ndsp-v116-context-parent',
          'static'
        );
      }

      ancestor = ancestor.parentElement;
    }
  };

  const markArabicText = () => {
    const arabic = /[\u0600-\u06FF]/;

    for (const element of document.querySelectorAll(
      'h1,h2,h3,h4,h5,p,span,small,strong,b,button,summary,label'
    )) {
      const text = String(element.textContent || '');

      if (arabic.test(text)) {
        element.classList.add('ndsp-v116-arabic-text');
      }
    }
  };

  const isolatePercentages = () => {
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          const parent = node.parentElement;

          if (!parent) return NodeFilter.FILTER_REJECT;
          if (parent.closest('script,style,noscript,textarea')) {
            return NodeFilter.FILTER_REJECT;
          }
          if (parent.closest('[data-ndsp-v116-percent="ltr"]')) {
            return NodeFilter.FILTER_REJECT;
          }

          percentPattern.lastIndex = 0;

          return percentPattern.test(node.nodeValue || '')
            ? NodeFilter.FILTER_ACCEPT
            : NodeFilter.FILTER_REJECT;
        },
      }
    );

    const nodes = [];
    let node;

    while ((node = walker.nextNode())) nodes.push(node);

    for (const textNode of nodes) {
      const text = String(textNode.nodeValue || '');
      const fragment = document.createDocumentFragment();
      let cursor = 0;

      percentPattern.lastIndex = 0;

      for (const match of text.matchAll(percentPattern)) {
        const index = match.index || 0;
        const raw = match[0];

        if (index > cursor) {
          fragment.appendChild(
            document.createTextNode(text.slice(cursor, index))
          );
        }

        const number = latinDigits(raw)
          .replace(/[%٪\s]/g, '')
          .replace(',', '.');

        const span = document.createElement('bdi');
        span.className = 'ndsp-v116-percent';
        span.setAttribute('dir', 'ltr');
        span.setAttribute('data-ndsp-v116-percent', 'ltr');
        span.textContent = `${number}%`;

        fragment.appendChild(span);
        cursor = index + raw.length;
      }

      if (cursor < text.length) {
        fragment.appendChild(
          document.createTextNode(text.slice(cursor))
        );
      }

      textNode.parentNode?.replaceChild(fragment, textNode);
    }
  };

  const findCardByHeading = (headingText) => {
    const headings = [...document.querySelectorAll('body *')].filter(
      (element) =>
        element.children.length < 3 &&
        normalized(element.textContent) === normalized(headingText)
    );

    let best = null;
    let bestArea = Number.POSITIVE_INFINITY;

    for (const heading of headings) {
      let ancestor = heading.parentElement;

      for (let depth = 0; ancestor && depth < 6; depth += 1) {
        const box = ancestor.getBoundingClientRect();
        const text = normalized(ancestor.innerText);

        if (
          box.height >= 80 &&
          box.height <= 520 &&
          text.includes(normalized(headingText))
        ) {
          const area = Math.max(1, box.width * box.height);

          if (area < bestArea) {
            best = ancestor;
            bestArea = area;
          }
        }

        ancestor = ancestor.parentElement;
      }
    }

    return best;
  };

  const percentValueInCard = (headingText) => {
    const card = findCardByHeading(headingText);
    if (!card) return null;

    const node = card.querySelector(
      '[data-ndsp-v116-percent="ltr"]'
    );

    if (!node) return null;

    const value = Number(
      latinDigits(node.textContent).replace(/[^0-9.]/g, '')
    );

    return Number.isFinite(value) ? value : null;
  };

  const correctReasonConsistency = () => {
    const strength = percentValueInCard('قوة القراءة');
    const readiness = percentValueInCard('جاهزية القرار');

    const reasonCard = findCardByHeading('لماذا لم يكتمل القرار؟');
    if (!reasonCard) return;

    const reasonElements = [...reasonCard.querySelectorAll('*')]
      .filter((element) => {
        if (element.children.length > 1) return false;
        return normalized(element.textContent).includes(
          'لا توجد موانع مسجلة'
        );
      });

    for (const element of reasonElements) {
      if (!element.dataset.ndspV116OriginalReason) {
        element.dataset.ndspV116OriginalReason =
          String(element.textContent || '').trim();
      }

      if (strength === 0 && readiness === 0) {
        element.textContent =
          'القراءة لم تكتمل لأن قوة الأدلة وجاهزية القرار ما زالت عند 0% في السياق الحالي.';
        element.classList.add('ndsp-v116-reason-corrected');
        element.setAttribute(
          'data-ndsp-v116-reason',
          'zero-evidence-and-readiness'
        );
      }
    }
  };

  const markBottomNav = () => {
    const labels = ['الرئيسية', 'الأسواق', 'القرار', 'الطبقات', 'الدليل'];

    for (const element of document.querySelectorAll('body *')) {
      const style = getComputedStyle(element);

      if (
        style.position !== 'fixed' &&
        style.position !== 'sticky'
      ) {
        continue;
      }

      const box = element.getBoundingClientRect();
      const text = normalized(element.innerText);
      const matches = labels.filter((label) =>
        text.includes(normalized(label))
      ).length;

      const nearBottom =
        box.bottom >= innerHeight - 36 ||
        box.top >= innerHeight * 0.68;

      if (
        matches >= 3 &&
        nearBottom &&
        box.height <= 180
      ) {
        element.classList.add('ndsp-v116-bottom-nav');
        element.setAttribute(
          'data-ndsp-v116-bottom-nav',
          'true'
        );
      }
    }
  };

  const apply = () => {
    if (!mobile()) return;

    cleanDuplicateTimeframes();
    markContextStripStatic();
    markArabicText();
    isolatePercentages();
    correctReasonConsistency();
    markBottomNav();

    document.documentElement.setAttribute(
      'data-ndsp-mobile-release-v116',
      'active'
    );
  };

  const schedule = () => {
    if (scheduled) return;
    scheduled = true;

    requestAnimationFrame(() => {
      scheduled = false;
      apply();
    });
  };

  document.addEventListener('click', (event) => {
    if (
      event.target instanceof Element &&
      event.target.closest(
        '[data-timeframe],[data-frame],button,[role="button"]'
      )
    ) {
      setTimeout(schedule, 0);
      setTimeout(schedule, 100);
      setTimeout(schedule, 350);
    }
  }, true);

  const observer = new MutationObserver(schedule);

  const start = () => {
    observer.observe(
      document.querySelector('#app') || document.body,
      {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: [
          'class',
          'aria-pressed',
          'data-selected',
          'style',
        ],
      }
    );

    apply();
    setTimeout(apply, 300);
    setTimeout(apply, 1200);
  };

  if (document.readyState === 'loading') {
    document.addEventListener(
      'DOMContentLoaded',
      start,
      { once: true }
    );
  } else {
    start();
  }
})();
