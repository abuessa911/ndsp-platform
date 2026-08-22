(function () {
  'use strict';

  var CANONICAL = '/portal-v50/';
  var LOGIN = '/login/';
  var LEGACY_PREFIXES = [
    '/decision-room-v30/',
    '/decision-room-v30-1/',
    '/decision-room-v31/',
    '/decision-room-v31/account/'
  ];

  function normalizedPath() {
    var path = window.location.pathname || '/';
    if (path.indexOf('.') === -1 && !path.endsWith('/')) path += '/';
    return path;
  }

  function isLogin() {
    return normalizedPath() === LOGIN;
  }

  function isCanonical() {
    return normalizedPath() === CANONICAL;
  }

  function isLegacy() {
    var path = normalizedPath();
    return LEGACY_PREFIXES.some(function (prefix) {
      return path.indexOf(prefix) === 0;
    });
  }

  function replaceWith(path, source) {
    var joiner = path.indexOf('?') === -1 ? '?' : '&';
    var target = path + joiner + 'ndsp_source=' + encodeURIComponent(source || 'v79') + '&ts=' + Date.now();
    window.location.replace(target);
  }

  async function hasSession() {
    try {
      var response = await fetch('/api/auth/session', {
        method: 'GET',
        credentials: 'include',
        cache: 'no-store',
        headers: { 'Accept': 'application/json' }
      });
      if (!response.ok) return false;
      var data = await response.json().catch(function () { return {}; });
      return Boolean(data && (data.ok === true || data.authenticated === true || data.user || data.email || data.session));
    } catch (error) {
      return false;
    }
  }

  async function enforceRoute() {
    if (isCanonical()) return;
    var authenticated = await hasSession();

    if (isLogin()) {
      if (authenticated) replaceWith(CANONICAL, 'authenticated-login');
      return;
    }

    if (isLegacy()) {
      if (authenticated) {
        replaceWith(CANONICAL, 'authenticated-legacy-route');
      } else {
        replaceWith(LOGIN + '?next=' + encodeURIComponent(CANONICAL), 'unauthenticated-legacy-route');
      }
    }
  }

  function startGuard() {
    enforceRoute();
    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      enforceRoute();
      if (attempts >= 240 || isCanonical()) window.clearInterval(timer);
    }, 500);

    window.addEventListener('focus', enforceRoute);
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) enforceRoute();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startGuard, { once: true });
  } else {
    startGuard();
  }
})();
