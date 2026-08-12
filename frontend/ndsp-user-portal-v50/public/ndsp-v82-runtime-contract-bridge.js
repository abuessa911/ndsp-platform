(function () {
  'use strict';

  if (window.__NDSP_V82_INSTALLED__) return;
  window.__NDSP_V82_INSTALLED__ = true;

  var CFG = {
    timeframe: 'weekly',
    timeframeAr: 'أسبوعي',
    analysisMode: 'speculative',
    analysisModeAr: 'مضاربية'
  };

  var diagnostics = window.__NDSP_V82_DIAGNOSTICS__ = window.__NDSP_V82_DIAGNOSTICS__ || {
    requests: [],
    responses: [],
    patchedResponses: 0,
    patchedRequests: 0,
    errors: []
  };

  function safeUrl(input) {
    try {
      var raw = typeof input === 'string' ? input : (input && input.url ? input.url : '');
      return raw ? new URL(raw, window.location.origin) : null;
    } catch (_) {
      return null;
    }
  }

  function isDecisionRequest(url) {
    if (!url || !/^https?:$/i.test(url.protocol)) return false;
    if (url.origin !== window.location.origin) return false;
    if (!/\/api\//i.test(url.pathname)) return false;
    if (/(decision|quality|scenario|contract|reading|support|completed)/i.test(url.pathname)) return true;
    return url.searchParams.has('symbol') && (url.searchParams.has('timeframe') || url.searchParams.has('timeFrame'));
  }

  function normalizeDecisionUrl(input) {
    var url = safeUrl(input);
    if (!isDecisionRequest(url)) return { url: url, changed: false, decision: false };

    var changed = false;
    var frame = String(url.searchParams.get('timeframe') || url.searchParams.get('timeFrame') || '').toLowerCase();
    if (!frame || frame === '1h' || frame === 'hourly' || frame === 'unspecified' || frame !== CFG.timeframe) {
      url.searchParams.delete('timeFrame');
      url.searchParams.set('timeframe', CFG.timeframe);
      changed = true;
    }
    var mode = String(url.searchParams.get('analysisMode') || url.searchParams.get('analysis_mode') || '').trim();
    if (!mode) {
      url.searchParams.set('analysisMode', CFG.analysisMode);
      changed = true;
    }
    if (changed) diagnostics.patchedRequests += 1;
    diagnostics.requests.push({ time: Date.now(), url: url.toString(), changed: changed, transport: 'normalize' });
    return { url: url, changed: changed, decision: true };
  }

  function parseBody(body) {
    if (!body || typeof body !== 'string') return null;
    try { return JSON.parse(body); } catch (_) { return null; }
  }

  function normalizeBody(body) {
    var parsed = parseBody(body);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return body;
    var changed = false;
    var frame = String(parsed.timeframe || parsed.timeFrame || '').toLowerCase();
    if (!frame || frame === '1h' || frame === 'hourly' || frame === 'unspecified' || frame !== CFG.timeframe) {
      delete parsed.timeFrame;
      parsed.timeframe = CFG.timeframe;
      changed = true;
    }
    if (!parsed.analysisMode && !parsed.analysis_mode) {
      parsed.analysisMode = CFG.analysisMode;
      changed = true;
    }
    return changed ? JSON.stringify(parsed) : body;
  }

  function meaningful(value) {
    if (value === null || value === undefined) return false;
    var s = String(value).trim().toLowerCase();
    return s !== '' && s !== 'unspecified' && s !== 'unknown' && s !== '1h' && s !== 'hourly';
  }

  function requestContext(url, body) {
    var parsed = parseBody(body) || {};
    return {
      symbol: (url && url.searchParams.get('symbol')) || parsed.symbol || '',
      timeframe: CFG.timeframe,
      analysisMode: CFG.analysisMode
    };
  }

  function patchObjectContext(data, ctx) {
    if (!data || typeof data !== 'object' || Array.isArray(data)) return { value: data, changed: false };
    var changed = false;

    if (!meaningful(data.symbol) && ctx.symbol) { data.symbol = ctx.symbol; changed = true; }
    if (!meaningful(data.timeframe)) { data.timeframe = ctx.timeframe; changed = true; }
    if (!meaningful(data.analysisMode) && !meaningful(data.analysis_mode)) { data.analysisMode = ctx.analysisMode; changed = true; }

    if (data.instrument && typeof data.instrument === 'object') {
      if (!meaningful(data.instrument.symbol) && ctx.symbol) { data.instrument.symbol = ctx.symbol; changed = true; }
      if (!meaningful(data.instrument.timeframe)) { data.instrument.timeframe = ctx.timeframe; changed = true; }
    }

    if (data.request_meta && typeof data.request_meta === 'object') {
      if (!meaningful(data.request_meta.symbol) && ctx.symbol) { data.request_meta.symbol = ctx.symbol; changed = true; }
      if (!meaningful(data.request_meta.timeframe)) { data.request_meta.timeframe = ctx.timeframe; changed = true; }
      if (!meaningful(data.request_meta.analysisMode) && !meaningful(data.request_meta.analysis_mode)) {
        data.request_meta.analysisMode = ctx.analysisMode;
        changed = true;
      }
    }

    if (data.display_context && typeof data.display_context === 'object') {
      if (!meaningful(data.display_context.symbol) && ctx.symbol) { data.display_context.symbol = ctx.symbol; changed = true; }
      if (!meaningful(data.display_context.timeframe)) { data.display_context.timeframe = ctx.timeframe; changed = true; }
      if (!meaningful(data.display_context.analysisMode) && !meaningful(data.display_context.analysis_mode)) {
        data.display_context.analysisMode = ctx.analysisMode;
        changed = true;
      }
    }

    return { value: data, changed: changed };
  }

  function patchJsonText(text, ctx) {
    if (!text || typeof text !== 'string') return { text: text, changed: false };
    try {
      var parsed = JSON.parse(text);
      var patched = patchObjectContext(parsed, ctx);
      return patched.changed ? { text: JSON.stringify(patched.value), changed: true } : { text: text, changed: false };
    } catch (_) {
      return { text: text, changed: false };
    }
  }

  function rememberResponse(url, status, changed, transport) {
    diagnostics.responses.push({ time: Date.now(), url: url || '', status: status || 0, changed: !!changed, transport: transport });
    if (changed) diagnostics.patchedResponses += 1;
  }

  var nativeFetch = window.fetch;
  if (typeof nativeFetch === 'function') {
    window.fetch = function (input, init) {
      var normalized = normalizeDecisionUrl(input);
      if (!normalized.decision) return nativeFetch.apply(this, arguments);

      var nextInit = Object.assign({}, init || {});
      var originalBody = nextInit.body;
      nextInit.body = normalizeBody(originalBody);
      nextInit.headers = new Headers(nextInit.headers || (input instanceof Request ? input.headers : undefined) || {});
      nextInit.headers.set('X-NDSP-Timeframe', CFG.timeframe);
      nextInit.headers.set('X-NDSP-Analysis-Mode', CFG.analysisMode);
      var ctx = requestContext(normalized.url, nextInit.body || originalBody);
      var requestInput = normalized.url.toString();

      if (input instanceof Request) {
        var method = nextInit.method || input.method;
        var requestInit = {
          method: method,
          headers: nextInit.headers,
          body: nextInit.body !== undefined ? nextInit.body : (method !== 'GET' && method !== 'HEAD' ? input.body : undefined),
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
        requestInput = new Request(normalized.url.toString(), requestInit);
      }

      return nativeFetch.call(this, requestInput, nextInit).then(function (response) {
        var contentType = String(response.headers.get('content-type') || '').toLowerCase();
        if (!contentType.includes('json') || response.status === 204) {
          rememberResponse(normalized.url.toString(), response.status, false, 'fetch');
          return response;
        }
        return response.clone().text().then(function (text) {
          var patched = patchJsonText(text, ctx);
          rememberResponse(normalized.url.toString(), response.status, patched.changed, 'fetch');
          if (!patched.changed) return response;
          var headers = new Headers(response.headers);
          headers.delete('content-length');
          return new Response(patched.text, {
            status: response.status,
            statusText: response.statusText,
            headers: headers
          });
        }).catch(function () {
          rememberResponse(normalized.url.toString(), response.status, false, 'fetch-error');
          return response;
        });
      });
    };
  }

  var NativeXHR = window.XMLHttpRequest;
  if (NativeXHR && NativeXHR.prototype) {
    var nativeOpen = NativeXHR.prototype.open;
    var nativeSend = NativeXHR.prototype.send;
    var responseTextDescriptor = Object.getOwnPropertyDescriptor(NativeXHR.prototype, 'responseText');
    var responseDescriptor = Object.getOwnPropertyDescriptor(NativeXHR.prototype, 'response');

    NativeXHR.prototype.open = function (method, url) {
      var normalized = normalizeDecisionUrl(url);
      this.__ndspV82 = {
        decision: normalized.decision,
        url: normalized.url ? normalized.url.toString() : String(url || ''),
        body: null,
        method: method
      };
      var args = Array.prototype.slice.call(arguments);
      if (normalized.decision && normalized.url) args[1] = normalized.url.toString();

      if (normalized.decision) {
        var xhr = this;
        try {
          if (responseTextDescriptor && responseTextDescriptor.get) {
            Object.defineProperty(xhr, 'responseText', {
              configurable: true,
              get: function () {
                var raw = responseTextDescriptor.get.call(xhr);
                if (xhr.readyState !== 4) return raw;
                var ctx = requestContext(safeUrl(xhr.__ndspV82.url), xhr.__ndspV82.body);
                var patched = patchJsonText(raw, ctx);
                if (patched.changed && !xhr.__ndspV82.textRemembered) {
                  xhr.__ndspV82.textRemembered = true;
                  rememberResponse(xhr.__ndspV82.url, xhr.status, true, 'xhr-text');
                }
                return patched.text;
              }
            });
          }
          if (responseDescriptor && responseDescriptor.get) {
            Object.defineProperty(xhr, 'response', {
              configurable: true,
              get: function () {
                var raw = responseDescriptor.get.call(xhr);
                if (xhr.readyState !== 4) return raw;
                var ctx = requestContext(safeUrl(xhr.__ndspV82.url), xhr.__ndspV82.body);
                if (xhr.responseType === 'json' && raw && typeof raw === 'object') {
                  var patchedObj = patchObjectContext(raw, ctx);
                  if (patchedObj.changed && !xhr.__ndspV82.objectRemembered) {
                    xhr.__ndspV82.objectRemembered = true;
                    rememberResponse(xhr.__ndspV82.url, xhr.status, true, 'xhr-json');
                  }
                  return patchedObj.value;
                }
                if (!xhr.responseType || xhr.responseType === 'text') {
                  var patchedText = patchJsonText(String(raw || ''), ctx);
                  if (patchedText.changed && !xhr.__ndspV82.objectRemembered) {
                    xhr.__ndspV82.objectRemembered = true;
                    rememberResponse(xhr.__ndspV82.url, xhr.status, true, 'xhr-response');
                  }
                  return patchedText.text;
                }
                return raw;
              }
            });
          }
        } catch (error) {
          diagnostics.errors.push('xhr-shadow:' + String(error && error.message ? error.message : error));
        }
      }
      return nativeOpen.apply(this, args);
    };

    NativeXHR.prototype.send = function (body) {
      if (this.__ndspV82 && this.__ndspV82.decision) {
        this.__ndspV82.body = normalizeBody(body);
        try { this.setRequestHeader('X-NDSP-Timeframe', CFG.timeframe); } catch (_) {}
        try { this.setRequestHeader('X-NDSP-Analysis-Mode', CFG.analysisMode); } catch (_) {}
        diagnostics.requests.push({ time: Date.now(), url: this.__ndspV82.url, changed: true, transport: 'xhr' });
        return nativeSend.call(this, this.__ndspV82.body);
      }
      return nativeSend.apply(this, arguments);
    };
  }

  function normalizeStorage(storage) {
    try {
      var standard = {
        timeframe: CFG.timeframe,
        timeFrame: CFG.timeframe,
        analysisMode: CFG.analysisMode,
        analysis_mode: CFG.analysisMode
      };
      Object.keys(standard).forEach(function (key) {
        var current = storage.getItem(key);
        if (current !== null && (!meaningful(current) || /^(1h|hourly)$/i.test(current))) storage.setItem(key, standard[key]);
      });
      for (var i = 0; i < storage.length; i += 1) {
        var key = storage.key(i);
        if (!key || !/(timeframe|time_frame|analysisMode|analysis_mode|readingMode|reading_mode)/i.test(key)) continue;
        var value = storage.getItem(key);
        if (/^(1h|hourly)$/i.test(String(value || ''))) storage.setItem(key, CFG.timeframe);
        if (value === '') storage.setItem(key, CFG.analysisMode);
      }
    } catch (_) {}
  }

  normalizeStorage(window.localStorage);
  normalizeStorage(window.sessionStorage);

  function exactLeaf(text) {
    var all = document.querySelectorAll('body *');
    for (var i = 0; i < all.length; i += 1) {
      var el = all[i];
      if (el.children.length === 0 && String(el.textContent || '').trim() === text) return el;
    }
    return null;
  }

  function fixVisibleContext() {
    var all = document.querySelectorAll('body *');
    for (var i = 0; i < all.length; i += 1) {
      var el = all[i];
      if (el.children.length !== 0) continue;
      var text = String(el.textContent || '').trim();
      if (/^(1H|1h|hourly)$/i.test(text)) {
        el.textContent = CFG.timeframeAr;
        el.setAttribute('data-ndsp-v82-timeframe', CFG.timeframe);
      }
    }

    var typeLabel = exactLeaf('نوع القراءة');
    if (typeLabel && typeLabel.parentElement) {
      var leaves = typeLabel.parentElement.querySelectorAll('*');
      for (var j = 0; j < leaves.length; j += 1) {
        var leaf = leaves[j];
        if (leaf.children.length === 0 && String(leaf.textContent || '').trim() === '') {
          leaf.textContent = CFG.analysisModeAr;
          leaf.setAttribute('data-ndsp-v82-analysis-mode', CFG.analysisMode);
          break;
        }
      }
    }
  }

  function apply() {
    fixVisibleContext();
    document.documentElement.setAttribute('data-ndsp-v82-ready', 'true');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
  var observer = new MutationObserver(function () { window.requestAnimationFrame(apply); });
  observer.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
  window.setTimeout(apply, 250);
  window.setTimeout(apply, 1000);
  window.setTimeout(apply, 3000);
})();
