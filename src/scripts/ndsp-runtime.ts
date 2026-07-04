const storedLang = localStorage.getItem('ndsp_lang') || 'ar';
document.documentElement.dataset.lang = storedLang;
document.documentElement.lang = storedLang === 'en' ? 'en' : 'ar';
document.documentElement.dir = storedLang === 'en' ? 'ltr' : 'rtl';

window.addEventListener('click', (event) => {
  const target = event.target as HTMLElement | null;
  if (!target) return;

  const langButton = target.closest('[data-ndsp-lang-toggle]');
  if (!langButton) return;

  const current = document.documentElement.dataset.lang === 'en' ? 'en' : 'ar';
  const next = current === 'en' ? 'ar' : 'en';
  localStorage.setItem('ndsp_lang', next);
  document.documentElement.dataset.lang = next;
  document.documentElement.lang = next;
  document.documentElement.dir = next === 'en' ? 'ltr' : 'rtl';
});
