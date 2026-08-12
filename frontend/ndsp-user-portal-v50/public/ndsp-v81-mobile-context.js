(function () {
  'use strict';

  var V81 = {
    timeframe: 'weekly',
    timeframeAr: 'أسبوعي',
    analysisMode: 'speculative'
  };

  function normalizeUrl(input) {
    try {
      var raw = typeof input === 'string' ? input : (input && input.url ? input.url : '');
      if (!raw) return null;
      var url = new URL(raw, window.location.origin);
      if (!/\/api\/decision\/(quality-live|quality|scenario|support)/i.test(url.pathname)) return null;
      var current = String(url.searchParams.get('timeframe') || '').toLowerCase();
      if (!current || current !== V81.timeframe) url.searchParams.set('timeframe', V81.timeframe);
      if (!url.searchParams.get('analysisMode')) url.searchParams.set('analysisMode', V81.analysisMode);
      return url;
    } catch (_) {
      return null;
    }
  }

  function normalizeBody(body) {
    if (!body || typeof body !== 'string') return body;
    try {
      var obj = JSON.parse(body);
      if (obj && typeof obj === 'object') {
        obj.timeframe = V81.timeframe;
        if (!obj.analysisMode) obj.analysisMode = V81.analysisMode;
        return JSON.stringify(obj);
      }
    } catch (_) {}
    return body;
  }

  var nativeFetch = window.fetch;
  if (typeof nativeFetch === 'function') {
    window.fetch = function (input, init) {
      var url = normalizeUrl(input);
      if (!url) return nativeFetch.apply(this, arguments);

      var nextInit = Object.assign({}, init || {});
      nextInit.headers = new Headers(nextInit.headers || (input instanceof Request ? input.headers : undefined) || {});
      nextInit.headers.set('X-NDSP-Timeframe', V81.timeframe);
      nextInit.headers.set('X-NDSP-Analysis-Mode', V81.analysisMode);
      if (nextInit.body) nextInit.body = normalizeBody(nextInit.body);

      if (input instanceof Request) {
        var reqInit = {
          method: nextInit.method || input.method,
          headers: nextInit.headers,
          body: nextInit.body !== undefined ? nextInit.body : (input.method !== 'GET' && input.method !== 'HEAD' ? input.body : undefined),
          mode: input.mode,
          credentials: input.credentials,
          cache: input.cache,
          redirect: input.redirect,
          referrer: input.referrer,
          referrerPolicy: input.referrerPolicy,
          integrity: input.integrity,
          keepalive: input.keepalive,
          signal: input.signal
        };
        return nativeFetch.call(this, new Request(url.toString(), reqInit));
      }
      return nativeFetch.call(this, url.toString(), nextInit);
    };
  }

  function normalizeStorage(storage) {
    try {
      for (var i = 0; i < storage.length; i += 1) {
        var key = storage.key(i);
        if (!key || !/(timeframe|time_frame|analysisMode|analysis_mode|readingMode|reading_mode)/i.test(key)) continue;
        var value = storage.getItem(key);
        if (value === '1H' || value === '1h' || value === 'hourly') storage.setItem(key, V81.timeframe);
        else if (value === '') storage.setItem(key, V81.analysisMode);
        else {
          try {
            var parsed = JSON.parse(value);
            var changed = false;
            if (parsed && typeof parsed === 'object') {
              if (parsed.timeframe && String(parsed.timeframe).toLowerCase() !== V81.timeframe) {
                parsed.timeframe = V81.timeframe;
                changed = true;
              }
              if ('analysisMode' in parsed && !parsed.analysisMode) {
                parsed.analysisMode = V81.analysisMode;
                changed = true;
              }
              if (changed) storage.setItem(key, JSON.stringify(parsed));
            }
          } catch (_) {}
        }
      }
    } catch (_) {}
  }

  normalizeStorage(window.localStorage);
  normalizeStorage(window.sessionStorage);

  function exactTextElement(text) {
    var all = document.querySelectorAll('body *');
    for (var i = 0; i < all.length; i += 1) {
      var el = all[i];
      if (el.children.length === 0 && String(el.textContent || '').trim() === text) return el;
    }
    return null;
  }

  function findTitle() {
    return exactTextElement('لوحة المستخدم') || exactTextElement('غرفة القرار');
  }

  function fixMobileShell() {
    if (!window.matchMedia('(max-width: 900px)').matches) return;

    var title = findTitle();
    var main = title ? (title.closest('main,[role="main"]') || title.parentElement) : document.querySelector('main,[role="main"]');
    if (!main) main = document.getElementById('root');
    if (!main) return;

    main.setAttribute('data-ndsp-v81-main', 'true');
    var node = main;
    while (node && node !== document.body) {
      var rect = node.getBoundingClientRect();
      var style = window.getComputedStyle(node);
      if (style.display === 'grid' && style.gridTemplateColumns && style.gridTemplateColumns.split(' ').length > 1) {
        node.setAttribute('data-ndsp-v81-shell', 'true');
      }
      if (rect.width < window.innerWidth * 0.82 || rect.left > window.innerWidth * 0.12) {
        node.style.setProperty('width', '100%', 'important');
        node.style.setProperty('max-width', 'none', 'important');
        node.style.setProperty('min-width', '0', 'important');
        node.style.setProperty('margin-left', '0', 'important');
        node.style.setProperty('margin-right', '0', 'important');
        node.style.setProperty('transform', 'none', 'important');
        if (style.display === 'flex') node.style.setProperty('flex', '1 1 100%', 'important');
      }
      node = node.parentElement;
    }

    var asides = document.querySelectorAll('aside');
    for (var i = 0; i < asides.length; i += 1) {
      var aside = asides[i];
      var r = aside.getBoundingClientRect();
      var cs = window.getComputedStyle(aside);
      var text = String(aside.textContent || '').trim();
      var visuallyClosed = cs.visibility === 'hidden' || cs.opacity === '0' || r.width === 0 || text === '';
      if (r.height > window.innerHeight * 0.45 && visuallyClosed) {
        aside.setAttribute('data-ndsp-v81-collapsed', 'true');
      }
    }
  }

  function fixDisplayedContext() {
    var frameLabel = exactTextElement('الفريم');
    if (frameLabel) {
      var box = frameLabel.parentElement;
      if (box) {
        var leaves = box.querySelectorAll('*');
        for (var i = 0; i < leaves.length; i += 1) {
          var leaf = leaves[i];
          var value = String(leaf.textContent || '').trim();
          if (leaf.children.length === 0 && /^(1H|1h|hourly)$/i.test(value)) {
            leaf.textContent = V81.timeframeAr;
            leaf.setAttribute('data-ndsp-v81-timeframe', 'weekly');
          }
        }
      }
    }

    var mismatch = Array.from(document.querySelectorAll('body *')).find(function (el) {
      return String(el.textContent || '').includes('تم حجب الاستجابة بسبب اختلاف السياق');
    });
    if (mismatch) {
      var noBlock = Array.from(document.querySelectorAll('body *')).find(function (el) {
        return el.children.length === 0 && String(el.textContent || '').trim() === 'لا توجد موانع مسجلة في العقد المستلم.';
      });
      if (noBlock) {
        noBlock.textContent = 'تعذر اعتماد القرار لأن بيانات الخدمة لم تطابق سياق الأصل والفريم المحدد.';
        noBlock.setAttribute('data-ndsp-v81-consistency', 'true');
      }
    }
  }

  function apply() {
    fixMobileShell();
    fixDisplayedContext();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();

  window.addEventListener('resize', apply, { passive: true });
  var observer = new MutationObserver(function () { window.requestAnimationFrame(apply); });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.setTimeout(apply, 300);
  window.setTimeout(apply, 1200);
  window.setTimeout(apply, 3000);
})();
