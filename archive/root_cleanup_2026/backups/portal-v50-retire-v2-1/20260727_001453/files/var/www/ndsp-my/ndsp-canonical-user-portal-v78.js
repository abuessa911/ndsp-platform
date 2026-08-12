(function () {
  'use strict';

  var CANONICAL = '/portal-v50/';
  var LEGACY_PREFIXES = [
    '/decision-room-v30/',
    '/decision-room-v30-1/',
    '/decision-room-v31/',
    '/decision-room-v31/account/'
  ];

  function normalize(path) {
    if (!path) return '/';
    return path.endsWith('/') || path.indexOf('.') !== -1 ? path : path + '/';
  }

  function isCanonical() {
    return normalize(window.location.pathname) === CANONICAL;
  }

  function isLogin() {
    return normalize(window.location.pathname) === '/login/';
  }

  function isLegacyAuthenticatedDestination() {
    var path = normalize(window.location.pathname);
    return LEGACY_PREFIXES.some(function (prefix) {
      return path.indexOf(prefix) === 0;
    });
  }

  function goCanonical(source) {
    if (isCanonical()) return;
    var suffix = '?ndsp_source=' + encodeURIComponent(source || 'v78') + '&ts=' + Date.now();
    window.location.replace(CANONICAL + suffix);
  }

  async function readSession() {
    try {
      var response = await fetch('/api/auth/session', {
        method: 'GET',
        credentials: 'include',
        cache: 'no-store',
        headers: { 'Accept': 'application/json' }
      });
      if (!response.ok) return false;
      var data = await response.json().catch(function () { return {}; });
      return Boolean(
        data && (
          data.authenticated === true ||
          data.ok === true ||
          data.user ||
          data.email ||
          data.session
        )
      );
    } catch (error) {
      return false;
    }
  }

  async function evaluateRoute() {
    var authenticated = await readSession();
    if (!authenticated) return;

    if (isLogin()) {
      goCanonical('login-success');
      return;
    }

    if (isLegacyAuthenticatedDestination()) {
      goCanonical('legacy-user-route');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', evaluateRoute, { once: true });
  } else {
    evaluateRoute();
  }

  if (isLogin()) {
    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      evaluateRoute();
      if (attempts >= 180) window.clearInterval(timer);
    }, 1000);

    window.addEventListener('focus', evaluateRoute);
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) evaluateRoute();
    });
  }
})();
