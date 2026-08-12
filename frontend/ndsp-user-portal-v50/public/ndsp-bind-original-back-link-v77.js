(function () {
  'use strict';

  var TARGET = 'https://www.ndsp.app/';
  var TEXTS = [
    '\u0627\u0644\u0639\u0648\u062f\u0629 \u0625\u0644\u0649 \u063a\u0631\u0641\u0629 \u0627\u0644\u0642\u0631\u0627\u0631',
    '\u0627\u0644\u0639\u0648\u062f\u0629 \u0627\u0644\u0649 \u063a\u0631\u0641\u0629 \u0627\u0644\u0642\u0631\u0627\u0631',
    'Back to Decision Room',
    'Return to Decision Room'
  ];
  var KNOWN_SELECTOR = [
    '#ndsp-home-link-v75',
    '#ndsp-home-hard-fix-v74',
    '#ndsp-approved-home-link-v73',
    '[data-ndsp-home-link-v75]',
    '[data-ndsp-home-hard-fix-v74]',
    '[data-ndsp-approved-home-link-v73]'
  ].join(',');
  var runs = 0;
  var maxRuns = 120;

  function normalize(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function isBackText(value) {
    var text = normalize(value);
    return TEXTS.indexOf(text) !== -1;
  }

  function visible(element) {
    if (!element || !element.isConnected) return false;
    var style = window.getComputedStyle(element);
    var rect = element.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
  }

  function installGuardStyle() {
    var id = 'ndsp-remove-floating-v77-style';
    var old = document.getElementById(id);
    if (old) return;
    var style = document.createElement('style');
    style.id = id;
    style.textContent = [
      '#ndsp-home-link-v75,#ndsp-home-hard-fix-v74,#ndsp-approved-home-link-v73,',
      '[data-ndsp-home-link-v75],[data-ndsp-home-hard-fix-v74],[data-ndsp-approved-home-link-v73]{',
      'display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;',
      'width:0!important;height:0!important;min-height:0!important;padding:0!important;margin:0!important;border:0!important;overflow:hidden!important;',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function removeKnownFloating() {
    Array.prototype.slice.call(document.querySelectorAll(KNOWN_SELECTOR)).forEach(function (element) {
      if (element && element.getAttribute('data-ndsp-v77-keep') !== '1') {
        element.remove();
      }
    });
  }

  function directTextMatches(element) {
    if (!element) return false;
    var direct = '';
    Array.prototype.forEach.call(element.childNodes || [], function (node) {
      if (node.nodeType === 3) direct += ' ' + node.nodeValue;
    });
    return isBackText(direct) || isBackText(element.textContent);
  }

  function clickableRoot(element) {
    var current = element;
    for (var depth = 0; current && current !== document.body && depth < 6; depth += 1) {
      var tag = String(current.tagName || '').toLowerCase();
      var role = String(current.getAttribute && current.getAttribute('role') || '').toLowerCase();
      if ((tag === 'a' || tag === 'button' || role === 'button' || role === 'link') && directTextMatches(current)) return current;
      current = current.parentElement;
    }
    return element;
  }

  function uniqueRoots() {
    var selectors = 'a,button,[role="button"],[role="link"],div,span,p';
    var roots = [];
    Array.prototype.slice.call(document.querySelectorAll(selectors)).forEach(function (element) {
      if (!visible(element) || !isBackText(element.textContent)) return;
      var childHasSame = Array.prototype.some.call(element.children || [], function (child) {
        return isBackText(child.textContent);
      });
      if (childHasSame && !directTextMatches(element)) return;
      var root = clickableRoot(element);
      if (roots.indexOf(root) === -1) roots.push(root);
    });
    return roots;
  }

  function candidateScore(element) {
    var style = window.getComputedStyle(element);
    var rect = element.getBoundingClientRect();
    var tag = String(element.tagName || '').toLowerCase();
    var position = String(style.position || '').toLowerCase();
    var background = String(style.backgroundColor || '').toLowerCase();
    var score = rect.width * rect.height;

    if (tag === 'a') score -= 1000000000;
    if (position === 'fixed' || position === 'sticky' || position === 'absolute') score += 2000000000;
    if (rect.width >= window.innerWidth * 0.70) score += 1000000000;
    if (rect.height >= 48) score += 500000000;
    if (background !== 'rgba(0, 0, 0, 0)' && background !== 'transparent') score += 250000000;
    if (element.id && /^ndsp-/.test(element.id)) score += 2000000000;
    return score;
  }

  function bindOriginal(element) {
    if (!element) return;
    element.setAttribute('data-ndsp-v77-keep', '1');
    element.removeAttribute('data-ndsp-v76-original-back-link');
    element.style.removeProperty('display');
    element.style.removeProperty('visibility');
    element.style.removeProperty('opacity');
    element.style.removeProperty('pointer-events');

    var tag = String(element.tagName || '').toLowerCase();
    if (tag === 'a') {
      element.setAttribute('href', TARGET);
      element.setAttribute('target', '_top');
      element.setAttribute('rel', 'noopener');
      element.onclick = null;
    } else {
      element.setAttribute('role', 'link');
      element.setAttribute('tabindex', '0');
    }

    if (!element.__ndspV77Bound) {
      element.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        window.top.location.assign(TARGET);
      }, true);
      element.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          event.stopImmediatePropagation();
          window.top.location.assign(TARGET);
        }
      }, true);
      element.__ndspV77Bound = true;
    }
  }

  function removeDuplicate(element, keep) {
    if (!element || element === keep || element.contains(keep) || keep.contains(element)) return;
    element.setAttribute('aria-hidden', 'true');
    element.style.setProperty('display', 'none', 'important');
    element.style.setProperty('visibility', 'hidden', 'important');
    element.style.setProperty('pointer-events', 'none', 'important');
    window.setTimeout(function () {
      if (element && element.isConnected && element !== keep) element.remove();
    }, 0);
  }

  function clean() {
    runs += 1;
    installGuardStyle();
    removeKnownFloating();

    var roots = uniqueRoots();
    if (!roots.length) return;
    roots.sort(function (a, b) { return candidateScore(a) - candidateScore(b); });
    var keep = roots[0];
    bindOriginal(keep);
    roots.slice(1).forEach(function (element) { removeDuplicate(element, keep); });
  }

  function start() {
    clean();
    var observer = new MutationObserver(function () {
      clean();
      if (runs >= maxRuns) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    var timer = window.setInterval(function () {
      clean();
      if (runs >= maxRuns) {
        window.clearInterval(timer);
        observer.disconnect();
      }
    }, 250);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
}());
