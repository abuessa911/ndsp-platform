(function(){
  'use strict';

  const ID = 'ndspTopControlsV13';
  const ROUTES = [["01", "الرئيسية", "Home", "/"], ["02", "مراقبة الأسواق", "Markets", "/markets"], ["03", "محرك المراحل", "Phase Engine", "/phase"], ["04", "محرك الذكاء", "Intelligence", "/intelligence"], ["05", "محرك القرار", "Decisions", "/decisions"], ["06", "الحوكمة والمخاطر", "Governance & Risk", "/governance"], ["07", "بنية البيانات", "Data Infrastructure", "/data-infra"], ["08", "مختبر الاستراتيجية", "Strategy Lab", "/strategy-lab"], ["09", "المعمارية", "Architecture", "/architecture"]];
  const LANG_KEYS = ['ndsp_lang_final','ndsp_final_lang','ndsp_lang'];

  function getLang(){
    return localStorage.getItem('ndsp_lang_final')
      || localStorage.getItem('ndsp_final_lang')
      || localStorage.getItem('ndsp_lang')
      || 'ar';
  }

  function setLang(lang){
    LANG_KEYS.forEach(k => localStorage.setItem(k, lang));
    const url = new URL(window.location.href);
    url.searchParams.set('fresh', String(Date.now()));
    window.location.href = url.toString();
  }

  function hideLegacyControls(){
    const candidates = Array.from(document.querySelectorAll('button,a,div,span'));
    for (const el of candidates) {
      if (!el || el.closest('#' + ID)) continue;
      const txt = (el.textContent || '').replace(/\s+/g,' ').trim();
      if (!txt) continue;

      const isPages =
        txt === 'الصفحات' ||
        txt === 'Pages' ||
        txt === 'الصفحات ☰' ||
        txt === 'Pages ☰';

      const isLang =
        /^(AR\s*EN|EN\s*AR|AR\s*\|\s*EN|EN\s*\|\s*AR)$/.test(txt);

      if (isPages || isLang) {
        el.classList.add('ndsp-legacy-control-hidden-v13');
      }
    }
  }

  function ensureControls(){
    hideLegacyControls();

    let dock = document.getElementById(ID);
    if (!dock) {
      dock = document.createElement('div');
      dock.id = ID;
      document.body.appendChild(dock);
    }

    const lang = getLang();
    const isAr = lang === 'ar';

    dock.dir = 'rtl';
    dock.innerHTML = `
      <button type="button" class="ndsp-pages-btn" data-ndsp-pages>
        <span>${isAr ? 'الصفحات' : 'Pages'}</span>
        <span>☰</span>
      </button>

      <div class="ndsp-lang-wrap" aria-label="Language switch">
        <button type="button" class="ndsp-lang-btn ${isAr ? 'is-active' : ''}" data-ndsp-lang="ar">AR</button>
        <button type="button" class="ndsp-lang-btn ${!isAr ? 'is-active' : ''}" data-ndsp-lang="en">EN</button>
      </div>

      <div class="ndsp-pages-panel" data-ndsp-pages-panel>
        ${ROUTES.map(function(r){
          const num = r[0];
          const ar = r[1];
          const en = r[2];
          const href = r[3];
          const label = isAr ? ar : en;
          return `
            <a class="ndsp-page-link" href="${href}">
              <span>${num}</span>
              <strong>${label}</strong>
            </a>
          `;
        }).join('')}
      </div>
    `;

    dock.querySelector('[data-ndsp-pages]').addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      dock.classList.toggle('is-open');
    });

    dock.querySelectorAll('[data-ndsp-lang]').forEach(function(btn){
      btn.addEventListener('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        const selected = btn.getAttribute('data-ndsp-lang');
        if (selected && selected !== getLang()) setLang(selected);
      });
    });

    document.addEventListener('click', function(e){
      if (!dock.contains(e.target)) dock.classList.remove('is-open');
    }, { passive: true });
  }

  function boot(){
    ensureControls();
    setTimeout(ensureControls, 300);
    setTimeout(ensureControls, 1000);
    setTimeout(ensureControls, 2500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
