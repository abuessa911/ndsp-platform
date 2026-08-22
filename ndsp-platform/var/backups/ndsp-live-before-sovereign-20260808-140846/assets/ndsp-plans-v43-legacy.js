(() => {
  function hideLegacy() {
    document.querySelectorAll('main > section').forEach(node => {
      if (node.id !== 'plans-v43' && /الوصول إلى NDSP|Access to NDSP|مستويات الوصول/i.test(node.textContent || '')) node.style.display = 'none';
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hideLegacy, { once: true }); else hideLegacy();
  window.setTimeout(hideLegacy, 500);
})();
