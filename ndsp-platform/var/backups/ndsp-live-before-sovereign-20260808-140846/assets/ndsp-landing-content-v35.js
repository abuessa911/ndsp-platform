(() => {
  'use strict';

  const room = 'https://my.ndsp.app/decision-room-v31/';
  const login = `${room}account/?mode=login`;
  const register = `${room}account/?mode=register`;
  const admin = `${room}account/admin-owner.html`;

  const copy = {
    ar: {
      nav: ['غرفة القرار', 'بناء القراءة', 'تغطية الأصول', 'الوصول', 'دخول المستخدم', 'ابدأ تجربة 16 يومًا'],
      mobile: 'الصفحات',
      hero: {
        over: 'منصة نواف لدعم القرار — NDSP',
        start: 'غرفة دعم قرار ', gold: 'متكاملة', end: 'للقراءات الواضحة.',
        lead: 'واجهة واحدة تجمع الأصل والسوق والفريم والحالة الحاكمة، ثم تعرض قوة القراءة وجاهزية القرار والمستويات المرجعية بترتيب واضح للمستخدم العادي والمحترف.',
        primary: 'ابدأ تجربة 16 يومًا',
        secondary: 'استعرض غرفة القرار',
        kpis: [['56', 'أصلًا محكومًا'], ['4', 'أسواق مترابطة'], ['16', 'طبقة مؤثرة في القرار']],
        radarOver: 'رادار اكتمال القراءة',
        radarTitle: 'رادار واحد يوضح الاكتمال لا الدقة الرقمية',
        radarLead: 'الأخضر داعم أو مكتمل، الذهبي للمتابعة أو التقارب، البرتقالي للحذر، الأحمر للخطر أو الإلغاء، والرمادي لغير المكتمل.',
        badges: ['بيانات حية ومحكومة', 'قوة القراءة ≠ الجاهزية', 'إفصاح آمن عن الأثر']
      },
      how: {
        over: 'غرفة القرار',
        title: 'من البيانات الحية إلى قرار شخصي قابل للمراجعة.',
        lead: 'يبدأ المسار بملخص قرار واحد وحالته الحاكمة، ثم يوضح ما ينقص القراءة، ومستويات السيناريو، والتفسير المناسب لنمط المستخدم؛ من دون لغة شراء أو بيع.',
        cards: [
          ['ملخص القرار والحالة', 'يرى المستخدم الأصل والسوق والفريم والسعر ووقت التحديث، ثم خلاصة القرار والحالة التي تحكمه فور فتح الصفحة.'],
          ['مستويات السيناريو', 'المراقبة والتفعيل والوصول والمراجعة والإلغاء تظهر كبطاقات مرجعية واضحة، لا كأوامر أو توصيات.'],
          ['نمطا القراءة', 'الوضع البسيط يركز على الملخص والمستويات والتفسير المباشر؛ والوضع المحترف يفتح التفاصيل اللازمة للمراجعة المتقدمة.']
        ]
      },
      method: {
        over: 'كيف تُبنى القراءة',
        title: 'ست عشرة طبقة تؤثر في القرار، مع إفصاح آمن عن أثرها.',
        lead: 'كل طبقة مربوطة تدخل في الحالة الحاكمة للقرار من الخلفية. تختلف الواجهة فقط في مستوى الإفصاح: ما يلزم للفهم والمراجعة ظاهر، بينما تبقى المعادلات والأدلة الداخلية محمية.',
        cards: [
          ['TDL', 'يضع القراءة في سياقها الزمني ويشرح علاقة الأفق الحالي بما سبقه من حالة.'],
          ['NMP — نقطة التقاء نواف', 'مرجع يوضح موضع الالتقاء داخل القراءة وحالته، من دون كشف المنطق الداخلي للحساب.'],
          ['محامي الشيطان', 'يفحص التعارضات والمخاطر وما ينقص اكتمال القراءة؛ وقد يمنع تفعيل السيناريو رغم وجود عناصر داعمة.']
        ]
      },
      plans: {
        over: 'الوصول إلى NDSP',
        title: 'ابدأ من غرفة القرار، ثم وسّع مستوى الوصول عند الحاجة.',
        lead: 'الجوهر واحد: قراءة محكومة ولا وعود بنتيجة. يختلف مستوى العرض والوصول، لا منطق القرار أو طريقة تأثير الطبقات الحاكمة.',
        cards: [
          ['الاستكشاف', 'تعرف على غرفة القرار ومحتواها العام.', 'تعريفي'],
          ['تجربة NDSP', 'ادخل تجربة مدتها 16 يومًا لواجهة القرار.', '16 يومًا'],
          ['وصول متقدم', 'مساحة أوسع للمراجعة والحوكمة والتقارير.', 'حسب الاحتياج']
        ]
      },
      footer: ['© NDSP — منصة نواف لدعم القرار', 'غرفة دعم قرار، وليست منصة تداول أو توصيات مالية أو ضمانًا لأي نتيجة.'],
      drawerTitle: 'تنقّل NDSP',
      drawer: ['الرئيسية', 'غرفة القرار', 'الأسواق والأصول', 'تسجيل الدخول', 'مستخدم جديد', 'الإدارة والمالك', 'كيف تُبنى القراءة', 'تغطية البيانات', 'مستويات الوصول']
    },
    en: {
      nav: ['Decision Room', 'Reading Design', 'Asset Coverage', 'Access', 'Sign in', 'Start 16-day trial'],
      mobile: 'Pages',
      hero: {
        over: 'Nawaf Decision Support Platform — NDSP',
        start: 'An advanced ', gold: 'decision room', end: 'for clear readings.',
        lead: 'One interface brings together the asset, market, timeframe, governing state, reading strength, decision readiness, and reference levels in a clear order for both newcomers and professionals.',
        primary: 'Start 16-day trial',
        secondary: 'Explore the Decision Room',
        kpis: [['56', 'governed assets'], ['4', 'connected markets'], ['16', 'decision-impact layers']],
        radarOver: 'Reading-completion radar',
        radarTitle: 'One radar for completion, not numeric comparison',
        radarLead: 'Green is supportive or complete, gold is monitoring or convergence, orange is caution, red is risk or cancellation, and gray is incomplete.',
        badges: ['Live governed data', 'Strength ≠ readiness', 'Safe impact disclosure']
      },
      how: {
        over: 'The Decision Room',
        title: 'From live data to a reviewable personal decision.',
        lead: 'The path begins with one decision summary and its governing state, then explains what is missing, scenario levels, and the interpretation suited to the selected reading mode—without execution language.',
        cards: [
          ['Decision summary & state', 'See the asset, market, timeframe, price, update time, decision summary, and governing state as soon as the page opens.'],
          ['Scenario levels', 'Monitor, activation, reach, review, and cancellation appear as clear reference cards—not instructions or recommendations.'],
          ['Reading modes', 'Beginner mode focuses on the summary, levels, and direct explanation; Professional mode reveals the advanced review details.']
        ]
      },
      method: {
        over: 'How the reading is built',
        title: 'Sixteen layers affect the decision, with safe disclosure of their impact.',
        lead: 'Every connected layer feeds the governing state from the background. Only disclosure differs: what is needed for understanding and review is visible, while internal equations and evidence remain protected.',
        cards: [
          ['TDL', 'Places the reading in time and explains how the current horizon relates to its prior state.'],
          ['NMP — Nawaf Meet Point', 'A reference that shows the point of convergence within the reading and its state, without exposing internal calculation logic.'],
          ["Devil's Advocate", 'Examines conflicts, risks, and missing inputs; it can prevent scenario activation even when supporting signals are present.']
        ]
      },
      plans: {
        over: 'Access to NDSP',
        title: 'Start in the Decision Room, then expand access when needed.',
        lead: 'The core remains the same: governed reading with no outcome promise. Access and presentation differ; the decision logic and the governing impact of layers do not.',
        cards: [
          ['Explore', 'Get to know the Decision Room and its public content.', 'Overview'],
          ['NDSP Trial', 'Enter a 16-day Decision Room experience.', '16 days'],
          ['Advanced access', 'A broader space for review, governance, and reporting.', 'By need']
        ]
      },
      footer: ['© NDSP — Nawaf Decision Support Platform', 'A decision-support room, not a trading platform, financial recommendation, or promise of any result.'],
      drawerTitle: 'NDSP navigation',
      drawer: ['Home', 'Decision Room', 'Markets & assets', 'Sign in', 'New user', 'Admin & Owner', 'How readings are built', 'Data coverage', 'Access levels']
    }
  };

  const isArabic = () => document.documentElement.dir === 'rtl' || document.documentElement.lang.toLowerCase().startsWith('ar');
  const setText = (el, value) => {
    if (!el || typeof value !== 'string' || el.dataset.ndspV35Text === value) return;
    el.textContent = value;
    el.dataset.ndspV35Text = value;
  };
  const setHref = (el, href) => {
    if (el && href && el.getAttribute('href') !== href) el.setAttribute('href', href);
  };
  const setHeading = (el, prefix, gold, suffix) => {
    if (!el) return;
    const key = `${prefix}|${gold}|${suffix}`;
    if (el.dataset.ndspV35Text === key) return;
    el.innerHTML = '';
    el.append(document.createTextNode(prefix));
    const span = document.createElement('span');
    span.className = 'gold';
    span.textContent = gold;
    el.append(span, document.createElement('br'), document.createTextNode(suffix));
    el.dataset.ndspV35Text = key;
  };

  const rewriteLinks = (language) => {
    const nav = Array.from(document.querySelectorAll('header nav a'));
    const values = language.nav;
    nav.forEach((link, index) => {
      if (values[index]) setText(link, values[index]);
    });
    const headerLinks = Array.from(document.querySelectorAll('header a'));
    const loginLink = headerLinks.find((link) => /login|دخول/i.test(link.getAttribute('href') || '') || /دخول|Sign in/i.test(link.textContent || ''));
    const registerLink = headerLinks.find((link) => /register|تجربة/i.test(link.getAttribute('href') || '') || /تجربة|trial/i.test(link.textContent || ''));
    setHref(loginLink, login);
    setHref(registerLink, register);
    setText(registerLink, language.nav[5]);
  };

  const rewriteDrawer = (language) => {
    const drawer = document.getElementById('ndsp-mobile-pages-drawer');
    const drawerTitle = drawer?.querySelector('.ndsp-mobile-pages-title span');
    setText(drawerTitle, language.drawerTitle);
    const drawerLinks = drawer ? Array.from(drawer.querySelectorAll('a.ndsp-mobile-pages-link')) : [];
    const panelLinks = Array.from(document.querySelectorAll('#ndspTopControlsV13 .ndsp-page-link'));
    const routes = ['/', room, `${room}#asset-universe`, login, register, admin, '/#how', '/#radar', '/#plans'];
    [drawerLinks, panelLinks].forEach((links) => links.forEach((link, index) => {
      const label = link.querySelector('span:not(.ndsp-mobile-pages-index), strong') || link;
      if (language.drawer[index]) setText(label, language.drawer[index]);
      setHref(link, routes[index]);
      if (link.dataset.ndspRoute !== undefined) link.dataset.ndspRoute = routes[index];
    }));
    setText(document.querySelector('#ndsp-mobile-pages-button'), `☰ ${language.mobile}`);
    const pagesButton = document.querySelector('#ndspTopControlsV13 .ndsp-pages-btn span');
    setText(pagesButton, language.mobile);
  };

  const rewrite = () => {
    const main = document.querySelector('main');
    if (!main) return;
    const language = copy[isArabic() ? 'ar' : 'en'];
    const [hero, how, method, plans] = Array.from(main.children).filter((el) => el.tagName === 'SECTION');
    if (!hero || !how || !method || !plans) return;

    rewriteLinks(language);
    rewriteDrawer(language);

    setText(hero.querySelector('.hero-copy > .over'), language.hero.over);
    setHeading(hero.querySelector('h1'), language.hero.start, language.hero.gold, language.hero.end);
    setText(hero.querySelector('.hero-copy > p'), language.hero.lead);
    const heroButtons = Array.from(hero.querySelectorAll('.cta-row a'));
    setText(heroButtons[0], language.hero.primary);
    setText(heroButtons[1], language.hero.secondary);
    setHref(heroButtons[0], register);
    setHref(heroButtons[1], room);
    Array.from(hero.querySelectorAll('.kpi')).forEach((kpi, index) => {
      const [number, label] = language.hero.kpis[index] || [];
      setText(kpi.querySelector('strong'), number);
      setText(kpi.querySelector('span'), label);
    });
    setText(hero.querySelector('.hero-panel > .over'), language.hero.radarOver);
    setText(hero.querySelector('.hero-panel h2'), language.hero.radarTitle);
    setText(hero.querySelector('.hero-panel p'), language.hero.radarLead);
    Array.from(hero.querySelectorAll('.legend span')).forEach((badge, index) => setText(badge, language.hero.badges[index] || ''));

    const writeSection = (section, block) => {
      setText(section.querySelector(':scope > .over'), block.over);
      setText(section.querySelector(':scope > h2'), block.title);
      setText(section.querySelector(':scope > .lead'), block.lead);
      Array.from(section.querySelectorAll('.card')).forEach((card, index) => {
        const [title, description] = block.cards[index] || [];
        setText(card.querySelector('h3'), title);
        setText(card.querySelector('p'), description);
      });
    };
    writeSection(how, language.how);
    writeSection(method, language.method);

    setText(plans.querySelector(':scope > .over'), language.plans.over);
    setText(plans.querySelector(':scope > h2'), language.plans.title);
    setText(plans.querySelector(':scope > .lead'), language.plans.lead);
    Array.from(plans.querySelectorAll('.package')).forEach((card, index) => {
      const [title, description, price] = language.plans.cards[index] || [];
      setText(card.querySelector('h3'), title);
      setText(card.querySelector('p'), description);
      setText(card.querySelector('.price'), price);
    });

    const footer = document.querySelector('footer');
    if (footer) {
      const nodes = Array.from(footer.querySelectorAll('*')).filter((el) => el.children.length === 0 && (el.textContent || '').trim());
      setText(nodes[0], language.footer[0]);
      setText(nodes[1], language.footer[1]);
    }
  };

  const start = () => {
    rewrite();
    let queued = false;
    const rerun = () => {
      if (queued) return;
      queued = true;
      window.setTimeout(() => { queued = false; rewrite(); }, 120);
    };
    new MutationObserver(rerun).observe(document.documentElement, { childList: true, subtree: true });
    document.addEventListener('click', (event) => {
      if (event.target.closest('[data-ndsp-lang], [data-ndsp-pages], #ndsp-mobile-pages-button')) rerun();
    });
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
