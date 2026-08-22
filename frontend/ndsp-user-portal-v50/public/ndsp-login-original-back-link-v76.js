(function () {
  'use strict';

  var TARGET = 'https://www.ndsp.app/';
  var AR = '\u0627\u0644\u0639\u0648\u062f\u0629 \u0625\u0644\u0649 \u063a\u0631\u0641\u0629 \u0627\u0644\u0642\u0631\u0627\u0631';
  var EN = 'Back to Decision Room';
  var RUNS = 0;
  var MAX_RUNS = 80;

  function normalize(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function isTargetText(value) {
    var text = normalize(value);
    return text === AR || text === EN;
  }

  function visible(el) {
    if (!el || !el.isConnected) return false;
    var style = window.getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) === 0) return false;
    var rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function exactTextNodes() {
    var all = Array.prototype.slice.call(document.querySelectorAll('a,button,[role="button"],[role="link"],div,span,p'));
    return all.filter(function (el) {
      return visible(el) && isTargetText(el.textContent);
    });
  }

  function clickableRoot(el) {
    var current = el;
    var depth = 0;
    while (current && current !== document.body && depth < 5) {
      var tag = String(current.tagName || '').toLowerCase();
      var role = String(current.getAttribute && current.getAttribute('role') || '').toLowerCase();
      var idClass = String((current.id || '') + ' ' + (current.className || '')).toLowerCase();
      if ((tag === 'a' || tag === 'button' || role === 'button' || role === 'link' || /back|return|floating|home/.test(idClass)) && isTargetText(current.textContent)) {
        return current;
      }
      current = current.parentElement;
      depth += 1;
    }
    return el;
  }

  function candidateScore(el) {
    var rect = el.getBoundingClientRect();
    var style = window.getComputedStyle(el);
    var tag = String(el.tagName || '').toLowerCase();
    var score = Math.max(1, rect.width * rect.height);
    var position = String(style.position || '').toLowerCase();
    var fontSize = parseFloat(style.fontSize || '16') || 16;

    if (tag === 'a') score -= 1000000;
    if (position === 'fixed' || position === 'sticky') score += 1000000000;
    if (tag === 'button' || String(el.getAttribute('role') || '').toLowerCase() === 'button') score += 500000000;
    if (fontSize >= 20) score += 10000000;
    if (rect.height >= 55) score += 10000000;
    return score;
  }

  function bindOriginal(el) {
    if (!el) return;
    el.setAttribute('data-ndsp-v76-original-back-link', '1');
    if (String(el.tagName || '').toLowerCase() === 'a') {
      el.setAttribute('href', TARGET);
      el.removeAttribute('target');
    } else {
      el.setAttribute('role', 'link');
      el.setAttribute('tabindex', '0');
      el.style.cursor = 'pointer';
      if (!el.__ndspV76Bound) {
        el.addEventListener('click', function (event) {
          event.preventDefault();
          window.location.assign(TARGET);
        });
        el.addEventListener('keydown', function (event) {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            window.location.assign(TARGET);
          }
        });
        el.__ndspV76Bound = true;
      }
    }
  }

  function removeDuplicate(el, keep) {
    var root = clickableRoot(el);
    if (!root || root === keep || root.contains(keep) || keep.contains(root)) return;
    if (isTargetText(root.textContent)) {
      root.remove();
    }
  }

  function clean() {
    RUNS += 1;
    var nodes = exactTextNodes();
    if (!nodes.length) return;

    var roots = [];
    nodes.forEach(function (node) {
      var root = clickableRoot(node);
      if (roots.indexOf(root) === -1) roots.push(root);
    });

    roots.sort(function (a, b) {
      return candidateScore(a) - candidateScore(b);
    });

    var keep = roots[0];
    bindOriginal(keep);
    roots.slice(1).forEach(function (node) {
      removeDuplicate(node, keep);
    });
  }

  function start() {
    clean();
    var observer = new MutationObserver(function () {
      clean();
      if (RUNS >= MAX_RUNS) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    var timer = window.setInterval(function () {
      clean();
      if (RUNS >= MAX_RUNS) {
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
