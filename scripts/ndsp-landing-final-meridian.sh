set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
SRC="$PROJECT_ROOT/frontend/public-landing/index.html"
LIVE="/var/www/ndsp.app/index.html"
STAMP="$(date +%Y%m%d_%H%M%S)"

cd "$PROJECT_ROOT"

echo "Backup..."
cp "$SRC" "$SRC.before-final-meridian-$STAMP" || true
sudo cp "$LIVE" "$LIVE.before-final-meridian-$STAMP" || true

echo "Write updated landing..."
cat > "$SRC" <<'HTML'
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>NDSP — منصة دعم القرار</title>
  <meta name="description" content="NDSP منصة دعم قرار مؤسسية تجمع الأدلة والسياق داخل إطار محكوم لتقديم اتجاه رسمي واضح وقابل للتفسير والتحقق.">
  <meta property="og:title" content="NDSP — منصة دعم القرار">
  <meta property="og:description" content="الأدلة تتقاطع. القرار يتجه.">
  <meta name="theme-color" content="#080A0D">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root{
      --black:#080A0D;
      --gold:#CDAA56;
      --gold2:#E7BF69;
      --blue:#35AFE3;
      --mist:#D9DDE2;
      --white:#F4F3EF;
      --slate:#77818C;
      --max:1460px;
      --safeTop:env(safe-area-inset-top,0px);
      --safeBottom:env(safe-area-inset-bottom,0px);
    }

    *{box-sizing:border-box}
    html{background:var(--black);overflow-x:hidden;scroll-behavior:smooth}
    body{
      margin:0;
      min-height:100dvh;
      overflow-x:clip;
      color:var(--white);
      font-family:"IBM Plex Sans Arabic","Inter",system-ui,sans-serif;
      background:
        radial-gradient(circle at 68% 12%,rgba(205,170,86,.105),transparent 35rem),
        radial-gradient(circle at 21% 40%,rgba(53,175,227,.09),transparent 35rem),
        linear-gradient(180deg,#080A0D 0%,#0B1016 58%,#080A0D 100%);
    }

    body::before{
      content:"";
      position:fixed;
      inset:0;
      pointer-events:none;
      opacity:.34;
      background-image:
        linear-gradient(rgba(255,255,255,.026) 1px,transparent 1px),
        linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);
      background-size:96px 96px;
      mask-image:radial-gradient(circle at 52% 22%,black,transparent 78%);
    }

    a{color:inherit;text-decoration:none}
    a,button{min-height:44px}
    :focus-visible{outline:2px solid var(--blue);outline-offset:3px;border-radius:10px}

    .shell{width:min(100% - 72px,var(--max));margin-inline:auto}

    .topbar{
      position:fixed;
      inset:0 0 auto 0;
      z-index:50;
      padding-top:var(--safeTop);
      background:linear-gradient(180deg,rgba(8,10,13,.82),rgba(8,10,13,.22),transparent);
      backdrop-filter:blur(12px);
    }

    .nav{
      height:96px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:30px;
    }

    .brand{
      display:flex;
      align-items:center;
      gap:18px;
      order:1;
    }

    .mark{
      width:58px;
      height:58px;
      position:relative;
      border-radius:9px;
    }

    .mark::before{
      content:"";
      position:absolute;
      inset:7px 9px;
      background:
        linear-gradient(35deg,transparent 0 38%,var(--gold) 39% 45%,transparent 46%),
        linear-gradient(-35deg,transparent 0 38%,var(--gold) 39% 45%,transparent 46%),
        linear-gradient(90deg,transparent 0 36%,var(--gold) 37% 43%,transparent 44%),
        linear-gradient(145deg,transparent 0 42%,var(--gold) 43% 49%,transparent 50%);
      filter:drop-shadow(0 0 9px rgba(205,170,86,.18));
    }

    .mark::after{
      content:"";
      position:absolute;
      left:7px;
      top:24px;
      border-top:6px solid transparent;
      border-bottom:6px solid transparent;
      border-right:10px solid var(--blue);
      filter:drop-shadow(0 0 8px rgba(53,175,227,.35));
    }

    .brandText{display:grid;gap:4px;line-height:1}
    .brandText strong{
      font-family:"IBM Plex Mono",monospace;
      font-size:42px;
      letter-spacing:.24em;
      font-weight:700;
      color:var(--mist);
    }
    .brandText small{color:var(--mist);font-size:14px}

    .links{
      order:2;
      display:flex;
      align-items:center;
      gap:42px;
      color:rgba(217,221,226,.75);
      font-size:17px;
    }

    .sep{width:1px;height:30px;background:rgba(217,221,226,.28)}
    .login{
      border:1px solid rgba(205,170,86,.66);
      border-radius:8px;
      padding:11px 22px;
      color:var(--white);
      background:rgba(8,10,13,.34);
      box-shadow:inset 0 0 0 1px rgba(255,255,255,.025);
    }

    .mobileBtn{display:none}

    .hero{
      position:relative;
      min-height:100dvh;
      padding-top:126px;
      isolation:isolate;
    }

    .heroGrid{
      height:calc(100dvh - 126px);
      min-height:710px;
      display:grid;
      grid-template-columns:1.18fr .82fr;
      align-items:center;
      gap:54px;
    }

    .visual{
      order:2;
      position:relative;
      height:620px;
      min-width:0;
      margin-top:-6px;
    }

    .copy{
      order:1;
      align-self:center;
      justify-self:start;
      max-width:640px;
      padding-bottom:60px;
      z-index:2;
    }

    h1{
      margin:0;
      font-size:clamp(54px,5.35vw,86px);
      line-height:1.06;
      letter-spacing:-.045em;
      font-weight:700;
      color:var(--white);
      text-wrap:balance;
    }

    .gold{color:var(--gold)}
    .lead{
      margin:24px 0 0;
      color:rgba(217,221,226,.76);
      font-size:clamp(20px,1.65vw,25px);
      line-height:1.9;
      font-weight:400;
    }

    .actions{
      margin-top:42px;
      display:flex;
      gap:18px;
      align-items:center;
      flex-wrap:wrap;
    }

    .btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-width:210px;
      border-radius:7px;
      padding:15px 28px;
      font-size:18px;
      font-weight:700;
      transition:.18s ease;
    }

    .primary{
      background:linear-gradient(180deg,#E8C06B,#CDAA56);
      color:#111;
      border:1px solid rgba(244,243,239,.25);
      box-shadow:0 16px 44px rgba(205,170,86,.16);
    }

    .secondary{
      color:var(--mist);
      border:1px solid rgba(217,221,226,.27);
      background:rgba(12,15,19,.58);
    }

    .btn:hover{transform:translateY(-2px)}

    .meridianSvg{
      position:absolute;
      inset:-10px -20px auto auto;
      width:min(980px,65vw);
      height:auto;
      overflow:visible;
      direction:ltr;
    }

    .evidencePath{
      stroke-dasharray:800;
      stroke-dashoffset:800;
      animation:draw 1.65s cubic-bezier(.2,.8,.2,1) forwards;
    }

    .evidencePath:nth-child(2){animation-delay:.08s}
    .evidencePath:nth-child(3){animation-delay:.16s}
    .evidencePath:nth-child(4){animation-delay:.24s}
    .evidencePath:nth-child(5){animation-delay:.32s}

    .blueDot{
      filter:drop-shadow(0 0 10px rgba(53,175,227,.62));
      transform-box:fill-box;
      transform-origin:center;
      animation:dotPulse 3s ease-in-out infinite;
    }

    .goldNode{
      transform-box:fill-box;
      transform-origin:center;
      animation:nodePulse 2.45s ease-out 1;
    }

    .corePanel{
      filter:
        drop-shadow(0 0 24px rgba(205,170,86,.15))
        drop-shadow(0 14px 40px rgba(0,0,0,.28));
    }

    .scrollMark{
      position:absolute;
      left:50%;
      bottom:206px;
      transform:translateX(-50%);
      color:rgba(217,221,226,.72);
      display:grid;
      place-items:center;
      gap:8px;
      z-index:3;
    }

    .mouse{
      width:31px;
      height:52px;
      border:2px solid rgba(217,221,226,.72);
      border-radius:999px;
      position:relative;
    }

    .mouse::before{
      content:"";
      width:4px;
      height:10px;
      border-radius:999px;
      background:rgba(217,221,226,.82);
      position:absolute;
      top:10px;
      left:50%;
      transform:translateX(-50%);
    }

    .scrollMark span{
      width:16px;
      height:16px;
      border-inline-end:2px solid rgba(217,221,226,.52);
      border-bottom:2px solid rgba(217,221,226,.52);
      transform:rotate(45deg);
    }

    .stepsBand{
      position:absolute;
      inset:auto 0 0;
      min-height:214px;
      z-index:2;
      border-top:1px solid rgba(217,221,226,.12);
      background:
        radial-gradient(circle at 50% 0%,rgba(53,175,227,.06),transparent 30rem),
        linear-gradient(180deg,rgba(21,26,32,.42),rgba(8,10,13,.74));
      display:flex;
      align-items:center;
    }

    .steps{
      width:min(100% - 72px,var(--max));
      margin-inline:auto;
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:34px;
      direction:rtl;
    }

    .step{
      display:grid;
      grid-template-columns:auto 1fr;
      gap:20px;
      align-items:center;
      min-height:118px;
    }

    .stepIcon{
      width:82px;
      height:82px;
      border-radius:999px;
      border:1px solid rgba(217,221,226,.34);
      display:grid;
      place-items:center;
      color:var(--blue);
      background:rgba(12,15,19,.58);
      position:relative;
      font-size:31px;
    }

    .stepIcon::after{
      content:"";
      position:absolute;
      inset:13px;
      border-radius:inherit;
      border:1px solid rgba(217,221,226,.12);
    }

    .step b{
      display:inline-block;
      color:var(--blue);
      font-family:"IBM Plex Mono",monospace;
      font-size:20px;
      margin-inline-start:10px;
    }

    .step h3{
      display:inline-block;
      margin:0;
      color:var(--white);
      font-size:30px;
      line-height:1.2;
    }

    .step p{
      margin:10px 0 0;
      color:rgba(217,221,226,.66);
      line-height:1.75;
      font-size:16px;
      max-width:330px;
    }

    .content{
      padding:96px 0;
      border-top:1px solid rgba(217,221,226,.08);
    }

    .sectionHead{max-width:760px;display:grid;gap:12px}
    .sectionHead h2{
      margin:0;
      font-size:clamp(34px,4vw,56px);
      line-height:1.16;
      letter-spacing:-.025em;
    }
    .sectionHead p{margin:0;color:var(--slate);font-size:18px;line-height:1.9}

    .authorityCard{
      margin-top:36px;
      display:grid;
      grid-template-columns:1.1fr repeat(3,1fr);
      border:1px solid rgba(205,170,86,.48);
      border-radius:12px;
      overflow:hidden;
      background:
        radial-gradient(circle at 0% 50%,rgba(205,170,86,.13),transparent 30%),
        linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.01)),
        #0C0F13;
      box-shadow:
        0 0 0 1px rgba(205,170,86,.08),
        0 18px 54px rgba(0,0,0,.34),
        0 0 44px rgba(205,170,86,.08);
    }

    .authorityCard > div{
      min-height:92px;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:14px;
      color:var(--mist);
      border-inline-start:1px solid rgba(205,170,86,.20);
      font-size:18px;
    }

    .authorityCard .coreWord{
      border-inline-start:0;
      color:var(--gold);
      font-family:"IBM Plex Mono",monospace;
      font-size:34px;
      font-weight:700;
      letter-spacing:.08em;
    }

    .cards{
      margin-top:34px;
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:1px;
      border:1px solid rgba(217,221,226,.10);
      border-radius:14px;
      overflow:hidden;
      background:rgba(217,221,226,.08);
    }

    .card{
      min-height:170px;
      padding:28px;
      background:linear-gradient(180deg,rgba(21,26,32,.72),rgba(8,10,13,.92));
    }

    .card small{color:var(--blue);font-family:"IBM Plex Mono",monospace;font-weight:700}
    .card h3{margin:16px 0 8px;font-size:25px;color:var(--white)}
    .card p{margin:0;color:var(--slate);line-height:1.75}

    .cta{
      margin:96px 0 0;
      border:1px solid rgba(205,170,86,.30);
      border-radius:18px;
      padding:46px;
      background:
        radial-gradient(circle at 85% 20%,rgba(205,170,86,.11),transparent 34%),
        linear-gradient(180deg,rgba(255,255,255,.03),rgba(255,255,255,.01)),
        #0C0F13;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:28px;
    }

    .cta h2{margin:0;font-size:clamp(32px,4vw,52px)}
    .cta p{margin:12px 0 0;color:var(--slate);font-size:18px}

    footer{
      padding:44px 0 64px;
      border-top:1px solid rgba(217,221,226,.08);
      color:rgba(217,221,226,.58);
    }

    .foot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
    .footLinks{display:flex;gap:16px;flex-wrap:wrap}

    @keyframes draw{to{stroke-dashoffset:0}}
    @keyframes dotPulse{0%,100%{opacity:.72;transform:scale(1)}50%{opacity:1;transform:scale(1.14)}}
    @keyframes nodePulse{0%{opacity:.34;transform:scale(.74)}54%{opacity:1;transform:scale(1.14)}100%{opacity:.95;transform:scale(1)}}

    @media(max-width:1150px){
      .shell{width:min(100% - 36px,var(--max))}
      .links{display:none}
      .mobileBtn{
        display:inline-flex;
        border:1px solid rgba(205,170,86,.44);
        background:rgba(12,15,19,.58);
        color:var(--gold);
        border-radius:9px;
        padding:10px 14px;
      }
      .hero{padding-top:108px}
      .heroGrid{height:auto;min-height:0;grid-template-columns:1fr;gap:34px}
      .copy{order:1;justify-self:stretch;padding-bottom:0}
      .visual{order:2;height:auto;min-height:480px}
      .meridianSvg{position:relative;inset:auto;width:100%}
      .stepsBand{position:relative;margin-top:34px}
      .scrollMark{display:none}
      .steps{grid-template-columns:1fr;padding:30px 0}
      .authorityCard,.cards{grid-template-columns:1fr}
      .authorityCard > div{border-inline-start:0;border-top:1px solid rgba(205,170,86,.18)}
      .authorityCard .coreWord{border-top:0}
      .cta{display:grid}
    }

    @media(max-width:640px){
      .brandText strong{font-size:25px}
      .brandText small{font-size:11px}
      .mark{width:46px;height:46px}
      .nav{height:78px}
      h1{font-size:44px}
      .lead{font-size:17px}
      .btn{width:100%}
      .visual{min-height:360px}
      .step{grid-template-columns:1fr;text-align:center;justify-items:center}
      .step p{max-width:none}
      .content{padding:64px 0}
      .cta{padding:28px}
    }

    @media(prefers-reduced-motion:reduce){
      *,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}
      .evidencePath{stroke-dashoffset:0!important}
    }
  </style>
</head>

<body>
  <header class="topbar">
    <div class="shell nav">
      <a class="brand" href="/" aria-label="NDSP منصة دعم القرار">
        <span class="mark" aria-hidden="true"></span>
        <span class="brandText">
          <strong>NDSP</strong>
          <small>منصة دعم القرار</small>
        </span>
      </a>

      <nav class="links" aria-label="التنقل الرئيسي">
        <a href="#methodology">المنهجية</a>
        <span class="sep"></span>
        <a href="#governance">الحوكمة</a>
        <a class="login" href="https://my.ndsp.app/login">تسجيل الدخول</a>
      </nav>

      <button class="mobileBtn" type="button">القائمة</button>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="shell heroGrid">
        <div class="copy">
          <h1>
            منصة دعم القرار<br>
            كل الأدلة. <span class="gold">اتجاه رسمي واحد.</span>
          </h1>

          <p class="lead">
            ذكاء مؤسسي محكوم يحوّل السياق المعقد إلى قرار واضح يمكن تفسيره.
          </p>

          <div class="actions">
            <a class="btn primary" href="https://my.ndsp.app/register?trial=elite&days=16">ابدأ تجربتك لمدة 16 يومًا</a>
            <a class="btn secondary" href="#methodology">اعرف لماذا</a>
          </div>
        </div>

        <div class="visual" aria-label="تدفق الأدلة إلى CORE">
          <svg class="meridianSvg" viewBox="0 0 980 620" role="img" aria-label="مصادر الأدلة تتقاطع ثم تدخل CORE">
            <defs>
              <linearGradient id="lineBlueGold" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0" stop-color="#35AFE3" stop-opacity=".78"/>
                <stop offset=".68" stop-color="#35AFE3" stop-opacity=".30"/>
                <stop offset="1" stop-color="#CDAA56" stop-opacity=".95"/>
              </linearGradient>

              <linearGradient id="goldStroke" x1="0" x2="1">
                <stop offset="0" stop-color="#CDAA56" stop-opacity=".35"/>
                <stop offset=".55" stop-color="#F0CD75" stop-opacity=".95"/>
                <stop offset="1" stop-color="#CDAA56" stop-opacity=".18"/>
              </linearGradient>

              <radialGradient id="nodeGold" cx="50%" cy="50%" r="50%">
                <stop offset="0" stop-color="#F6D987"/>
                <stop offset=".42" stop-color="#CDAA56"/>
                <stop offset="1" stop-color="#CDAA56" stop-opacity="0"/>
              </radialGradient>

              <filter id="softGlow" x="-100%" y="-100%" width="300%" height="300%">
                <feGaussianBlur stdDeviation="10" result="b"/>
                <feMerge>
                  <feMergeNode in="b"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>

              <filter id="panelGlow" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#CDAA56" flood-opacity=".18"/>
                <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity=".36"/>
              </filter>
            </defs>

            <rect width="980" height="620" fill="transparent"/>

            <g opacity=".22">
              <path d="M140 70 L390 185 L455 270" fill="none" stroke="#D9DDE2" stroke-width="18"/>
              <path d="M210 200 L420 255" fill="none" stroke="#D9DDE2" stroke-width="16"/>
              <path d="M250 440 L420 350" fill="none" stroke="#D9DDE2" stroke-width="15"/>
              <path d="M460 132 L460 277" fill="none" stroke="#D9DDE2" stroke-width="42"/>
            </g>

            <g font-family="IBM Plex Sans Arabic" font-size="19" fill="#D9DDE2">
              <text x="88" y="96">بيانات مؤسسية</text>
              <text x="72" y="200">تقارير وتحليلات</text>
              <text x="92" y="304">سياق تشغيلي</text>
              <text x="78" y="408">معلومات خارجية</text>
              <text x="70" y="512">معايير وسياسات</text>
            </g>

            <g fill="#35AFE3">
              <circle class="blueDot" cx="228" cy="92" r="5.5"/>
              <circle class="blueDot" cx="228" cy="196" r="5.5"/>
              <circle class="blueDot" cx="228" cy="300" r="5.5"/>
              <circle class="blueDot" cx="228" cy="404" r="5.5"/>
              <circle class="blueDot" cx="228" cy="508" r="5.5"/>
            </g>

            <g fill="none" stroke="url(#lineBlueGold)" stroke-width="2">
              <path class="evidencePath" d="M235 92 C330 96 394 156 470 276"/>
              <path class="evidencePath" d="M235 196 C330 200 395 234 470 292"/>
              <path class="evidencePath" d="M235 300 C334 300 394 300 470 300"/>
              <path class="evidencePath" d="M235 404 C333 396 394 360 470 316"/>
              <path class="evidencePath" d="M235 508 C334 488 394 432 470 332"/>
            </g>

            <g fill="none" stroke="#35AFE3" stroke-width="2" stroke-linecap="round" opacity=".75">
              <path d="M346 162 C382 194 404 232 430 272" stroke-dasharray="2 10"/>
              <path d="M333 278 C370 282 400 286 432 292" stroke-dasharray="2 10"/>
              <path d="M335 324 C372 320 402 316 432 312" stroke-dasharray="2 10"/>
              <path d="M346 442 C382 406 406 364 432 328" stroke-dasharray="2 10"/>
            </g>

            <circle class="goldNode" cx="484" cy="304" r="34" fill="url(#nodeGold)" filter="url(#softGlow)"/>

            <g class="corePanel" filter="url(#panelGlow)">
              <path d="M497 304 L532 258 H950 Q964 258 964 272 V336 Q964 350 950 350 H532 Z"
                    fill="#0C0F13"
                    stroke="url(#goldStroke)"
                    stroke-width="1.6"/>

              <line x1="660" y1="276" x2="660" y2="332" stroke="rgba(205,170,86,.30)"/>
              <line x1="794" y1="276" x2="794" y2="332" stroke="rgba(205,170,86,.30)"/>
              <line x1="905" y1="276" x2="905" y2="332" stroke="rgba(205,170,86,.30)"/>

              <text x="585" y="316" fill="#CDAA56" font-family="IBM Plex Mono" font-size="34" font-weight="700">CORE</text>

              <g font-family="IBM Plex Sans Arabic" font-size="17" fill="#D9DDE2">
                <text x="722" y="312" text-anchor="middle">الاتجاه الرسمي</text>
                <text x="850" y="312" text-anchor="middle">محكوم حوكميًا</text>
                <text x="932" y="312" text-anchor="middle">أدلة قابلة للتحقق</text>
              </g>

              <g fill="none" stroke="#CDAA56" stroke-width="2">
                <path d="M690 292 L704 286 L718 292 V310 Q704 321 690 310 Z"/>
                <path d="M818 292 L832 286 L846 292 V310 Q832 321 818 310 Z"/>
                <rect x="914" y="287" width="24" height="32" rx="3"/>
                <path d="M919 297 H933 M919 305 H933 M919 313 H928"/>
              </g>
            </g>

            <path d="M484 304 L532 304" stroke="#F1D27A" stroke-width="3" filter="url(#softGlow)"/>
          </svg>
        </div>
      </div>

      <div class="scrollMark" aria-hidden="true">
        <div class="mouse"></div>
        <span></span>
      </div>

      <div class="stepsBand">
        <div class="steps">
          <article class="step">
            <div class="stepIcon">◎</div>
            <div>
              <b>01</b>
              <h3>السياق</h3>
              <p>نستوعب الصورة الكاملة من داخل المؤسسة وخارجها.</p>
            </div>
          </article>

          <article class="step">
            <div class="stepIcon">⋮</div>
            <div>
              <b>02</b>
              <h3>الأدلة</h3>
              <p>تُجمع الأدلة الموثوقة وتحلل ضمن إطار حوكمي واضح.</p>
            </div>
          </article>

          <article class="step">
            <div class="stepIcon">↗</div>
            <div>
              <b>03</b>
              <h3>الاتجاه الرسمي</h3>
              <p>نقدم اتجاهًا رسميًا واحدًا واضحًا وقابلًا للتفسير.</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section id="methodology" class="content">
      <div class="shell">
        <div class="sectionHead">
          <h2>من السياق إلى اتجاه رسمي</h2>
          <p>تعرض الصفحة العامة المسار العام فقط. التفاصيل المتقدمة تبقى داخل غرفة القرار حسب الصلاحيات.</p>
        </div>

        <div class="authorityCard">
          <div class="coreWord">CORE</div>
          <div>◇ الاتجاه الرسمي</div>
          <div>◇ محكوم حوكميًا</div>
          <div>▣ أدلة قابلة للتحقق</div>
        </div>
      </div>
    </section>

    <section id="governance" class="content">
      <div class="shell">
        <div class="sectionHead">
          <h2>الثقة تُبنى على الحوكمة والأدلة.</h2>
          <p>NDSP لا تنفذ صفقات ولا تقدم أوامر تنفيذ. هي منصة دعم قرار تعرض نتيجة رسمية قابلة للتفسير والتحقق.</p>
        </div>

        <div class="cards">
          <article class="card">
            <small>01</small>
            <h3>مصدر واضح</h3>
            <p>كل نتيجة ترتبط بسياق ومصدر ووقت تحديث مصرح به.</p>
          </article>
          <article class="card">
            <small>02</small>
            <h3>أدلة قابلة للتتبع</h3>
            <p>تظهر الأدلة المتاحة حسب الباقة دون كشف الطبقات الداخلية.</p>
          </article>
          <article class="card">
            <small>03</small>
            <h3>تفسير منظم</h3>
            <p>الهدف فهم النتيجة، لا مطاردة مؤشرات متفرقة.</p>
          </article>
        </div>

        <div class="cta">
          <div>
            <h2>جرّب Elite لمدة 16 يومًا.</h2>
            <p>دون بطاقة دفع — ودون خصم تلقائي.</p>
          </div>
          <a class="btn primary" href="https://my.ndsp.app/register?trial=elite&days=16">ابدأ الآن</a>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="shell foot">
      <div><strong>NDSP</strong><br>منصة دعم القرار</div>
      <div class="footLinks">
        <a href="#methodology">المنهجية</a>
        <a href="#governance">الحوكمة</a>
        <a href="https://my.ndsp.app/login">تسجيل الدخول</a>
        <a href="/privacy">الخصوصية</a>
        <a href="/terms">الشروط</a>
        <a href="/support">الدعم</a>
      </div>
    </div>
  </footer>
</body>
</html>
HTML

echo "Deploy..."
sudo cp "$SRC" "$LIVE"
sudo chown www-data:www-data "$LIVE"
sudo chmod 644 "$LIVE"

echo "Reload nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "Verify..."
curl -I https://ndsp.app
curl -sL https://ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "ndsp.app clean"
curl -sL https://ndsp.app | grep -E "إشارة شراء|إشارة بيع|ربح مضمون|دقة مضمونة" || echo "no forbidden claims"

echo "DONE"
echo "Updated source: $SRC"
echo "Updated live:   $LIVE"
