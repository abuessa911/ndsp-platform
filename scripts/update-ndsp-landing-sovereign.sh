set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-new"
SRC="$PROJECT_ROOT/frontend/public-landing/index.html"
LIVE="/var/www/ndsp.app/index.html"
STAMP="$(date +%Y%m%d_%H%M%S)"

cd "$PROJECT_ROOT"

echo "Backup current files..."
cp "$SRC" "$PROJECT_ROOT/frontend/public-landing/index.before-sovereign-$STAMP.html" || true
sudo cp "$LIVE" "/var/www/ndsp.app/index.before-sovereign-$STAMP.html" || true

cat > "$SRC" <<'HTML'
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NDSP — منصة دعم القرار</title>
  <meta name="description" content="NDSP منصة دعم قرار مؤسسية تجمع الأدلة والسياق داخل إطار محكوم لتقديم اتجاه رسمي واضح وقابل للتفسير والتحقق.">
  <meta property="og:title" content="NDSP — منصة دعم القرار">
  <meta property="og:description" content="الأدلة تتقاطع. القرار يتجه.">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="NDSP">
  <meta name="theme-color" content="#080A0D">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --carbon: #080A0D;
      --graphite: #151A20;
      --surface-deep: #0C0F13;
      --surface-soft: #111820;
      --gold: #CDAA56;
      --blue: #35AFE3;
      --mist: #D9DDE2;
      --alabaster: #F4F3EF;
      --green: #2DAA77;
      --amber: #D19038;
      --red: #CF565D;
      --purple: #796286;
      --slate: #77818C;
      --line-soft: rgba(217, 221, 226, .10);
      --gold-line: rgba(205, 170, 86, .38);
      --gold-glow: rgba(205, 170, 86, .12);
      --blue-glow: rgba(53, 175, 227, .24);
      --max: 1280px;
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 0px);
    }

    * {
      box-sizing: border-box;
    }

    html {
      background: var(--carbon);
      color: var(--alabaster);
      scroll-behavior: smooth;
      overflow-x: hidden;
      text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
    }

    body {
      margin: 0;
      min-width: 0;
      overflow-x: clip;
      background:
        radial-gradient(circle at 78% 8%, rgba(205, 170, 86, .13), transparent 34rem),
        radial-gradient(circle at 14% 24%, rgba(53, 175, 227, .10), transparent 34rem),
        linear-gradient(180deg, #080A0D 0%, #0A0D11 54%, #080A0D 100%);
      color: var(--alabaster);
      font-family: "IBM Plex Sans Arabic", "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body.menu-open {
      overflow: hidden;
      touch-action: none;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    button,
    input,
    select,
    textarea {
      font: inherit;
    }

    button,
    a,
    [role="button"] {
      min-height: 44px;
    }

    :focus-visible {
      outline: 2px solid var(--blue);
      outline-offset: 3px;
      border-radius: 10px;
    }

    .container {
      width: min(100% - 48px, var(--max));
      margin-inline: auto;
    }

    .site-header {
      position: sticky;
      top: 0;
      z-index: 50;
      padding-top: var(--safe-top);
      background: rgba(8, 10, 13, .52);
      backdrop-filter: blur(18px);
      border-bottom: 1px solid rgba(205, 170, 86, .14);
    }

    .nav-inner {
      height: 82px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 28px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      min-width: 190px;
    }

    .brand-mark {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      position: relative;
      border: 1px solid rgba(205, 170, 86, .38);
      background:
        linear-gradient(135deg, rgba(205,170,86,.22), transparent 45%),
        #0C0F13;
      box-shadow: 0 0 28px rgba(205, 170, 86, .09);
    }

    .brand-mark::before,
    .brand-mark::after {
      content: "";
      position: absolute;
      background: var(--gold);
      border-radius: 999px;
      transform-origin: center;
    }

    .brand-mark::before {
      width: 25px;
      height: 3px;
      right: 9px;
      top: 15px;
      transform: rotate(-35deg);
      box-shadow: 0 8px 0 var(--gold), 0 16px 0 var(--gold);
    }

    .brand-mark::after {
      width: 0;
      height: 0;
      background: transparent;
      border-top: 5px solid transparent;
      border-bottom: 5px solid transparent;
      border-right: 8px solid var(--blue);
      left: 7px;
      top: 17px;
      border-radius: 0;
    }

    .brand-copy {
      display: grid;
      gap: 3px;
      line-height: 1.1;
    }

    .brand-copy strong {
      font-family: "IBM Plex Mono", monospace;
      letter-spacing: .18em;
      color: var(--mist);
      font-size: 28px;
      font-weight: 700;
    }

    .brand-copy span {
      color: var(--mist);
      font-size: 13px;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 30px;
      color: rgba(217, 221, 226, .78);
      font-size: 15px;
    }

    .nav-links a:hover {
      color: var(--alabaster);
    }

    .login-link {
      border: 1px solid rgba(205, 170, 86, .52);
      color: var(--alabaster);
      border-radius: 10px;
      padding: 10px 16px;
      background: rgba(8, 10, 13, .38);
    }

    .menu-button {
      display: none;
      border: 1px solid rgba(205, 170, 86, .42);
      color: var(--gold);
      background: rgba(8,10,13,.5);
      border-radius: 12px;
      padding: 10px 14px;
      cursor: pointer;
    }

    .mobile-panel {
      position: fixed;
      inset: 0 0 0 auto;
      width: min(92vw, 430px);
      height: 100dvh;
      z-index: 100;
      display: none;
      overflow-y: auto;
      overscroll-behavior: contain;
      padding: calc(18px + var(--safe-top)) 20px calc(24px + var(--safe-bottom));
      background: rgba(8, 10, 13, .98);
      border-inline-start: 1px solid rgba(205, 170, 86, .28);
      box-shadow: -22px 0 90px rgba(0,0,0,.46);
    }

    .mobile-panel.open {
      display: block;
    }

    .mobile-panel button,
    .mobile-panel a {
      width: 100%;
      min-height: 48px;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      margin: 8px 0;
      border-radius: 12px;
    }

    .mobile-panel a {
      padding: 12px 14px;
      color: var(--mist);
    }

    .mobile-panel .primary {
      justify-content: center;
      color: var(--carbon);
    }

    .close-menu {
      border: 1px solid rgba(205,170,86,.38);
      background: transparent;
      color: var(--gold);
      padding: 10px 14px;
      cursor: pointer;
    }

    main {
      padding-top: 64px;
    }

    .hero {
      display: grid;
      grid-template-columns: 1fr 1.05fr;
      align-items: center;
      gap: clamp(42px, 6vw, 88px);
      min-height: calc(100dvh - 116px);
      padding-bottom: 34px;
    }

    .hero-copy {
      max-width: 650px;
      justify-self: start;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
      letter-spacing: .12em;
      font-size: 12px;
      text-transform: uppercase;
      margin-bottom: 22px;
    }

    .eyebrow::before {
      content: "";
      width: 32px;
      height: 1px;
      background: var(--gold);
      opacity: .72;
    }

    h1 {
      margin: 0;
      font-size: clamp(48px, 6.5vw, 92px);
      line-height: 1.02;
      letter-spacing: -.045em;
      color: var(--alabaster);
    }

    h2 {
      margin: 0;
      font-size: clamp(30px, 4vw, 54px);
      line-height: 1.15;
      letter-spacing: -.025em;
    }

    h3 {
      margin: 0;
      color: var(--gold);
      font-size: 18px;
      font-weight: 600;
    }

    p {
      color: var(--slate);
      line-height: 1.9;
    }

    .gold {
      color: var(--gold);
    }

    .lead {
      margin: 24px 0 0;
      color: var(--mist);
      font-size: clamp(18px, 1.7vw, 23px);
      line-height: 1.85;
    }

    .actions {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 30px;
    }

    .primary,
    .secondary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      padding: 13px 22px;
      font-weight: 700;
      transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }

    .primary {
      color: var(--carbon);
      background: linear-gradient(180deg, #E5BF69, var(--gold));
      border: 1px solid rgba(244, 243, 239, .22);
      box-shadow:
        0 0 0 1px rgba(205, 170, 86, .14),
        0 16px 42px rgba(205, 170, 86, .16);
    }

    .secondary {
      color: var(--mist);
      background: rgba(21, 26, 32, .64);
      border: 1px solid rgba(217, 221, 226, .18);
    }

    .primary:hover,
    .secondary:hover {
      transform: translateY(-2px);
    }

    .micro {
      margin-top: 14px;
      color: rgba(217, 221, 226, .58);
      font-size: 14px;
    }

    .visual {
      padding: 0;
      overflow: hidden;
      border-radius: 28px;
      border: 1px solid rgba(217,221,226,.08);
      background:
        radial-gradient(circle at 33% 50%, rgba(205,170,86,.08), transparent 32%),
        linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,0)),
        #080A0D;
      box-shadow:
        0 0 0 1px rgba(205,170,86,.04),
        0 28px 80px rgba(0,0,0,.38);
    }

    .hero-meridian-svg {
      width: 100%;
      display: block;
    }

    .evidence-lines path {
      stroke-dasharray: 560;
      stroke-dashoffset: 560;
      animation: evidenceDraw 1.6s cubic-bezier(.2,.75,.2,1) forwards;
    }

    .evidence-lines path:nth-child(2) { animation-delay: .08s; }
    .evidence-lines path:nth-child(3) { animation-delay: .16s; }
    .evidence-lines path:nth-child(4) { animation-delay: .24s; }
    .evidence-lines path:nth-child(5) { animation-delay: .32s; }

    .data-dots circle {
      filter: drop-shadow(0 0 8px rgba(53,175,227,.55));
      animation: dotPulse 2.8s ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: center;
    }

    .convergence-node {
      animation: corePulse 2.4s ease-out 1;
      transform-box: fill-box;
      transform-origin: center;
    }

    .svg-core-card {
      height: 100%;
      border-radius: 16px;
      border: 1px solid rgba(205,170,86,.44);
      background:
        radial-gradient(circle at 0% 100%, rgba(205,170,86,.18), transparent 42%),
        linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.01)),
        #0C0F13;
      box-shadow:
        inset 0 0 0 1px rgba(255,255,255,.03),
        0 0 36px rgba(205,170,86,.10);
      display: grid;
      align-content: center;
      justify-items: center;
      gap: 8px;
      color: #D9DDE2;
      font-family: "IBM Plex Sans Arabic", sans-serif;
    }

    .svg-core-card strong {
      color: #CDAA56;
      font-family: "IBM Plex Mono", monospace;
      font-size: 34px;
      letter-spacing: .04em;
    }

    .svg-core-card span {
      font-size: 14px;
    }

    .core-authority-section {
      padding: 18px 0 76px;
      border-top: none;
    }

    .core-authority-card {
      max-width: 920px;
      margin-inline: auto;
      display: grid;
      grid-template-columns: 1.2fr repeat(3, 1fr);
      align-items: center;
      overflow: hidden;
      border-radius: 16px;
      border: 1px solid var(--gold-line);
      background:
        radial-gradient(circle at 0% 50%, rgba(205,170,86,.13), transparent 30%),
        linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.01)),
        var(--surface-deep);
      box-shadow:
        0 0 0 1px rgba(205,170,86,.08),
        0 10px 30px rgba(0,0,0,.35),
        0 0 40px rgba(205,170,86,.08);
    }

    .core-word {
      padding: 26px 32px;
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
      font-size: 30px;
      font-weight: 800;
      letter-spacing: .08em;
    }

    .authority-item {
      min-height: 88px;
      padding: 22px 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: var(--mist);
      border-inline-start: 1px solid rgba(205,170,86,.22);
      white-space: nowrap;
    }

    .authority-icon {
      color: var(--gold);
      font-size: 22px;
      line-height: 1;
    }

    section {
      padding: 78px 0;
      border-top: 1px solid rgba(217,221,226,.075);
    }

    .section-head {
      display: grid;
      gap: 12px;
      max-width: 760px;
    }

    .section-head p {
      margin: 0;
      font-size: 18px;
    }

    .steps-line {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1px;
      margin-top: 34px;
      border: 1px solid var(--line-soft);
      border-radius: 16px;
      overflow: hidden;
      background: rgba(217,221,226,.08);
    }

    .steps-line article {
      background:
        linear-gradient(180deg, rgba(21,26,32,.72), rgba(8,10,13,.9));
      padding: 28px;
      min-height: 180px;
    }

    .steps-line article span {
      color: var(--blue);
      font-family: "IBM Plex Mono", monospace;
      font-weight: 700;
    }

    .steps-line article h3 {
      margin-top: 18px;
      color: var(--alabaster);
      font-size: 24px;
    }

    .steps-line article p {
      color: var(--slate);
      line-height: 1.8;
      margin-bottom: 0;
    }

    .method-visual {
      margin-top: 36px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      align-items: stretch;
    }

    .circle-core,
    .layers-core {
      min-height: 380px;
      border-radius: 22px;
      border: 1px solid rgba(217,221,226,.10);
      background:
        radial-gradient(circle at 50% 50%, rgba(205,170,86,.10), transparent 34%),
        linear-gradient(180deg, rgba(21,26,32,.70), rgba(8,10,13,.90));
      position: relative;
      overflow: hidden;
      padding: 28px;
    }

    .circle-center {
      position: absolute;
      inset: 50% auto auto 50%;
      transform: translate(-50%, -50%);
      width: 172px;
      height: 172px;
      border-radius: 999px;
      border: 1px solid rgba(205,170,86,.52);
      display: grid;
      place-items: center;
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
      font-size: 32px;
      font-weight: 800;
      box-shadow: 0 0 42px rgba(205,170,86,.12);
      background: rgba(8,10,13,.70);
    }

    .orbit-label {
      position: absolute;
      min-width: 132px;
      padding: 10px 12px;
      border-radius: 999px;
      border: 1px solid rgba(53,175,227,.26);
      color: var(--mist);
      background: rgba(8,10,13,.72);
      font-size: 14px;
      text-align: center;
    }

    .orbit-label:nth-child(2) { top: 36px; left: 50%; transform: translateX(-50%); }
    .orbit-label:nth-child(3) { top: 42%; right: 28px; }
    .orbit-label:nth-child(4) { bottom: 38px; right: 80px; }
    .orbit-label:nth-child(5) { bottom: 38px; left: 80px; }
    .orbit-label:nth-child(6) { top: 42%; left: 28px; }

    .layer-stack {
      display: grid;
      gap: 12px;
      margin-top: 18px;
    }

    .layer {
      border: 1px solid rgba(217,221,226,.10);
      background: rgba(8,10,13,.42);
      color: var(--mist);
      border-radius: 12px;
      padding: 16px 18px;
    }

    .layer:nth-child(1) { margin-inline: 0 110px; }
    .layer:nth-child(2) { margin-inline: 26px 84px; }
    .layer:nth-child(3) { margin-inline: 52px 58px; }
    .layer:nth-child(4) { margin-inline: 78px 32px; }
    .layer:nth-child(5) { margin-inline: 104px 0; }

    .mini-core {
      margin-top: 18px;
      border: 1px solid rgba(205,170,86,.42);
      border-radius: 14px;
      padding: 18px;
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
      text-align: center;
      background: rgba(205,170,86,.05);
    }

    .benefit-row {
      margin-top: 32px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .benefit-row span {
      border: 1px solid rgba(217,221,226,.12);
      background: rgba(21,26,32,.58);
      color: var(--mist);
      border-radius: 999px;
      padding: 12px 16px;
    }

    .decision-preview-card {
      display: grid;
      grid-template-columns: 1fr 1.05fr;
      gap: 34px;
      align-items: center;
      border-radius: 22px;
      border: 1px solid rgba(205,170,86,.28);
      background:
        radial-gradient(circle at 100% 0%, rgba(53,175,227,.10), transparent 32%),
        radial-gradient(circle at 0% 100%, rgba(205,170,86,.10), transparent 34%),
        linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01)),
        #0C0F13;
      padding: clamp(28px, 5vw, 56px);
      box-shadow:
        0 22px 70px rgba(0,0,0,.36),
        0 0 40px rgba(205,170,86,.05);
    }

    .decision-preview-card p {
      max-width: 560px;
    }

    .preview-surface {
      border-radius: 18px;
      border: 1px solid rgba(217,221,226,.12);
      background:
        linear-gradient(180deg, rgba(21,26,32,.86), rgba(8,10,13,.92));
      padding: 24px;
    }

    .preview-head {
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid rgba(217,221,226,.10);
      padding-bottom: 18px;
      margin-bottom: 18px;
      color: var(--mist);
    }

    .preview-head b {
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
    }

    .preview-lines {
      display: grid;
      gap: 12px;
    }

    .preview-lines i {
      display: block;
      height: 12px;
      border-radius: 999px;
      background: linear-gradient(90deg, rgba(217,221,226,.22), rgba(217,221,226,.06));
    }

    .preview-lines i:nth-child(1) { width: 92%; }
    .preview-lines i:nth-child(2) { width: 76%; }
    .preview-lines i:nth-child(3) { width: 58%; }

    .preview-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 24px;
    }

    .preview-pills span {
      border: 1px solid rgba(53,175,227,.24);
      color: var(--mist);
      border-radius: 999px;
      padding: 8px 12px;
      font-size: 13px;
    }

    .plans-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 34px;
    }

    .plan {
      border-radius: 16px;
      border: 1px solid rgba(217,221,226,.11);
      background:
        linear-gradient(180deg, rgba(21,26,32,.72), rgba(8,10,13,.92));
      padding: 24px;
      min-height: 250px;
      transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }

    .plan:hover {
      transform: translateY(-3px);
      border-color: rgba(205,170,86,.34);
      box-shadow: 0 14px 42px rgba(0,0,0,.26);
    }

    .plan.featured {
      border-color: rgba(205,170,86,.44);
      box-shadow: 0 0 36px rgba(205,170,86,.07);
    }

    .plan small {
      color: var(--gold);
      font-family: "IBM Plex Mono", monospace;
    }

    .plan h3 {
      margin-top: 16px;
      color: var(--alabaster);
      font-size: 26px;
    }

    .plan strong {
      display: block;
      color: var(--gold);
      margin-top: 18px;
      font-size: 20px;
    }

    .trial-cta {
      border-radius: 24px;
      border: 1px solid rgba(205,170,86,.32);
      background:
        radial-gradient(circle at 80% 20%, rgba(205,170,86,.12), transparent 34%),
        linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01)),
        #0C0F13;
      padding: clamp(32px, 6vw, 72px);
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 28px;
    }

    .trial-points {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }

    .trial-points span {
      color: var(--mist);
      border: 1px solid rgba(217,221,226,.12);
      border-radius: 999px;
      padding: 9px 12px;
      font-size: 14px;
    }

    .faq-list {
      margin-top: 32px;
      display: grid;
      gap: 10px;
    }

    details {
      border-radius: 14px;
      border: 1px solid rgba(217,221,226,.11);
      background: rgba(21,26,32,.50);
      padding: 18px 20px;
    }

    summary {
      cursor: pointer;
      color: var(--mist);
      font-weight: 600;
    }

    footer {
      padding: 46px 0 68px;
      border-top: 1px solid rgba(217,221,226,.08);
      color: var(--slate);
    }

    .footer-inner {
      display: flex;
      justify-content: space-between;
      gap: 28px;
      flex-wrap: wrap;
    }

    .footer-links {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      color: rgba(217,221,226,.62);
    }

    @keyframes evidenceDraw {
      to { stroke-dashoffset: 0; }
    }

    @keyframes dotPulse {
      0%, 100% { opacity: .72; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.16); }
    }

    @keyframes corePulse {
      0% { opacity: .35; transform: scale(.78); }
      55% { opacity: 1; transform: scale(1.12); }
      100% { opacity: .9; transform: scale(1); }
    }

    @media (max-width: 1080px) {
      .hero,
      .method-visual,
      .decision-preview-card,
      .trial-cta {
        grid-template-columns: 1fr;
      }

      .plans-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .nav-links {
        display: none;
      }

      .menu-button {
        display: inline-flex;
      }

      .hero-copy {
        max-width: 100%;
      }
    }

    @media (max-width: 700px) {
      .container {
        width: min(100% - 32px, var(--max));
      }

      .nav-inner {
        height: 72px;
      }

      .brand-copy strong {
        font-size: 22px;
      }

      .brand-copy span {
        font-size: 12px;
      }

      main {
        padding-top: 36px;
      }

      .hero {
        min-height: auto;
        gap: 30px;
      }

      h1 {
        font-size: clamp(42px, 13vw, 60px);
      }

      .lead {
        font-size: 17px;
      }

      .visual {
        border-radius: 20px;
      }

      .core-authority-card,
      .steps-line,
      .plans-grid {
        grid-template-columns: 1fr;
      }

      .authority-item {
        border-inline-start: none;
        border-top: 1px solid rgba(205,170,86,.16);
      }

      .steps-line article {
        min-height: auto;
      }

      .circle-core,
      .layers-core {
        min-height: 340px;
      }

      .orbit-label {
        position: static;
        transform: none !important;
        display: block;
        margin: 8px auto;
      }

      .circle-center {
        position: static;
        transform: none;
        margin: 20px auto;
      }

      .layer {
        margin-inline: 0 !important;
      }

      .trial-cta {
        padding: 30px 22px;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .001ms !important;
        scroll-behavior: auto !important;
      }

      .evidence-lines path {
        stroke-dashoffset: 0 !important;
      }
    }
  </style>
</head>

<body>
  <header class="site-header">
    <div class="container nav-inner">
      <a class="brand" href="/" aria-label="NDSP منصة دعم القرار">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-copy">
          <strong>NDSP</strong>
          <span>منصة دعم القرار</span>
        </span>
      </a>

      <nav class="nav-links" aria-label="التنقل الرئيسي">
        <a href="#methodology">المنهجية</a>
        <a href="#current">التحليل الحالي</a>
        <a href="#governance">الحوكمة</a>
        <a href="#plans">الباقات</a>
        <a href="#docs">التوثيق</a>
        <a class="login-link" href="https://my.ndsp.app/login">تسجيل الدخول</a>
      </nav>

      <button class="menu-button" id="openMenu" type="button">القائمة</button>
    </div>
  </header>

  <aside class="mobile-panel" id="mobilePanel" aria-label="قائمة الجوال" aria-modal="true">
    <button class="close-menu" id="closeMenu" type="button">إغلاق ×</button>
    <a href="#methodology">المنهجية</a>
    <a href="#current">التحليل الحالي</a>
    <a href="#governance">الحوكمة</a>
    <a href="#plans">الباقات</a>
    <a href="#docs">التوثيق</a>
    <a href="https://my.ndsp.app/login">تسجيل الدخول</a>
    <a class="primary" href="https://my.ndsp.app/register?trial=elite&days=16">ابدأ تجربة Elite لمدة 16 يومًا</a>
  </aside>

  <main class="container">
    <div class="hero">
      <section class="hero-copy">
        <span class="eyebrow">Decision Support Platform</span>
        <h1>
          الأدلة تتقاطع.<br>
          <span class="gold">القرار يتجه.</span>
        </h1>
        <p class="lead">
          تجمع NDSP البيانات المؤسسية والتقارير والسياق التشغيلي والمعلومات الخارجية والمعايير داخل إطار محكوم، لتقديم اتجاه رسمي واضح وقابل للتفسير والتحقق.
        </p>

        <div class="actions">
          <a class="primary" href="https://my.ndsp.app/register?trial=elite&days=16">ابدأ تجربة Elite لمدة 16 يومًا</a>
          <a class="secondary" href="#methodology">استكشف المنهجية</a>
        </div>

        <p class="micro">تجربة كاملة لمدة 16 يومًا — دون بطاقة دفع — ودون خصم تلقائي.</p>
      </section>

      <section class="visual" aria-label="مخطط تقاطع الأدلة إلى CORE">
        <svg class="hero-meridian-svg" viewBox="0 0 860 560" role="img" aria-label="مصادر أدلة تتقاطع داخل CORE">
          <defs>
            <linearGradient id="evidenceLine" x1="1" y1="0" x2="0" y2="0">
              <stop offset="0%" stop-color="#35AFE3" stop-opacity=".85"/>
              <stop offset="72%" stop-color="#35AFE3" stop-opacity=".42"/>
              <stop offset="100%" stop-color="#CDAA56" stop-opacity=".95"/>
            </linearGradient>

            <radialGradient id="goldNode" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#F4D47A"/>
              <stop offset="45%" stop-color="#CDAA56"/>
              <stop offset="100%" stop-color="#CDAA56" stop-opacity="0"/>
            </radialGradient>

            <filter id="softGoldGlow" x="-80%" y="-80%" width="260%" height="260%">
              <feGaussianBlur stdDeviation="8" result="blur"/>
              <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          <rect width="860" height="560" rx="28" fill="#080A0D"/>

          <g font-family="IBM Plex Sans Arabic" font-size="18" fill="#D9DDE2">
            <text x="705" y="92">بيانات مؤسسية</text>
            <text x="695" y="178">تقارير وتحليلات</text>
            <text x="708" y="280">سياق تشغيلي</text>
            <text x="690" y="382">معلومات خارجية</text>
            <text x="690" y="468">معايير وسياسات</text>
          </g>

          <g class="evidence-lines" fill="none" stroke="url(#evidenceLine)" stroke-width="2">
            <path d="M680 86 C560 92 470 150 388 254"/>
            <path d="M680 174 C560 178 470 210 388 268"/>
            <path d="M680 278 C555 278 470 278 388 278"/>
            <path d="M680 382 C560 374 470 336 388 292"/>
            <path d="M680 468 C560 454 470 398 388 306"/>
          </g>

          <g class="data-dots" fill="#35AFE3">
            <circle cx="658" cy="86" r="5"/>
            <circle cx="658" cy="174" r="5"/>
            <circle cx="658" cy="278" r="5"/>
            <circle cx="658" cy="382" r="5"/>
            <circle cx="658" cy="468" r="5"/>
          </g>

          <circle class="convergence-node" cx="374" cy="280" r="30" fill="url(#goldNode)" filter="url(#softGoldGlow)"/>
          <path d="M356 280 C320 280 292 280 250 280" stroke="#CDAA56" stroke-width="3" fill="none"/>

          <foreignObject x="36" y="206" width="232" height="150">
            <div xmlns="http://www.w3.org/1999/xhtml" class="svg-core-card">
              <strong>CORE</strong>
              <span>الاتجاه الرسمي</span>
              <span>محكوم حوكميًا</span>
              <span>أدلة قابلة للتحقق</span>
            </div>
          </foreignObject>

          <text x="152" y="410" text-anchor="middle" fill="#CDAA56" font-family="IBM Plex Sans Arabic" font-size="23" font-weight="700">
            اتجاه رسمي واحد
          </text>
          <text x="152" y="444" text-anchor="middle" fill="#D9DDE2" font-family="IBM Plex Sans Arabic" font-size="17">
            واضح وقابل للتفسير.
          </text>
        </svg>
      </section>
    </div>

    <section class="core-authority-section" aria-label="CORE authority">
      <div class="core-authority-card">
        <div class="core-word">CORE</div>

        <div class="authority-item">
          <span class="authority-icon">◇</span>
          <span>اتجاه رسمي</span>
        </div>

        <div class="authority-item">
          <span class="authority-icon">◇</span>
          <span>محكوم حوكميًا</span>
        </div>

        <div class="authority-item">
          <span class="authority-icon">▣</span>
          <span>أدلة قابلة للتحقق</span>
        </div>
      </div>
    </section>

    <section id="methodology">
      <div class="section-head">
        <h2>من السياق إلى اتجاه رسمي</h2>
        <h3>Align → Resolve → Single Pulse</h3>
        <p>مسار مختصر يحوّل تعدد المصادر إلى نتيجة رسمية واحدة قابلة للمراجعة.</p>
      </div>

      <div class="steps-line">
        <article>
          <span>01</span>
          <h3>السياق</h3>
          <p>استيعاب الصورة الكاملة من داخل المؤسسة وخارجها.</p>
        </article>

        <article>
          <span>02</span>
          <h3>الأدلة</h3>
          <p>جمع الأدلة الموثوقة وتحليلها ضمن إطار قابل للمراجعة.</p>
        </article>

        <article>
          <span>03</span>
          <h3>الاتجاه الرسمي</h3>
          <p>نتيجة واحدة، واضحة، قابلة للتفسير والتحقق.</p>
        </article>
      </div>
    </section>

    <section>
      <div class="section-head">
        <h2>كيف تعمل NDSP؟</h2>
        <h3>من مصادر متعددة إلى CORE.</h3>
      </div>

      <div class="method-visual">
        <div class="circle-core" aria-label="المصادر العامة حول CORE">
          <div class="circle-center">CORE</div>
          <span class="orbit-label">بيانات مؤسسية</span>
          <span class="orbit-label">تقارير وتحليلات</span>
          <span class="orbit-label">سياق تشغيلي</span>
          <span class="orbit-label">معلومات خارجية</span>
          <span class="orbit-label">معايير وسياسات</span>
        </div>

        <div class="layers-core" aria-label="تراكم الأدلة والسياق">
          <div class="section-head">
            <h3>القرار لا يبدأ من مؤشر واحد.</h3>
            <p>بل من أدلة تتراكم ضمن سياق واضح حتى تصبح اتجاهًا رسميًا.</p>
          </div>

          <div class="layer-stack">
            <div class="layer">بيانات مؤسسية</div>
            <div class="layer">تقارير وتحليلات</div>
            <div class="layer">سياق تشغيلي</div>
            <div class="layer">معلومات خارجية</div>
            <div class="layer">معايير وسياسات</div>
          </div>

          <div class="mini-core">CORE</div>
        </div>
      </div>
    </section>

    <section>
      <div class="section-head">
        <h2>ما الذي تقدمه NDSP؟</h2>
        <h3>وضوح مؤسسي دون ضجيج.</h3>
      </div>

      <div class="benefit-row">
        <span>اتجاه رسمي واضح</span>
        <span>أدلة قابلة للتتبع</span>
        <span>تفسير منظم</span>
        <span>إدارة مخاطر</span>
        <span>فصل التجارب عن النتيجة</span>
      </div>
    </section>

    <section id="current">
      <div class="decision-preview-card">
        <div>
          <span class="eyebrow">Current CORE</span>
          <h2>التحليل الحالي يظهر النتيجة الرسمية فقط.</h2>
          <p>
            عند توفر نتيجة CORE من المصدر الرسمي، يتم عرضها دون كشف التجارب الداخلية أو القراءات غير المعتمدة.
          </p>
        </div>

        <div class="preview-surface">
          <div class="preview-head">
            <span>حالة النتيجة</span>
            <b>CORE</b>
          </div>
          <div class="preview-lines">
            <i></i><i></i><i></i>
          </div>
          <div class="preview-pills">
            <span>النتيجة الرسمية غير متاحة حاليًا</span>
            <span>لا توجد بيانات وهمية</span>
          </div>
        </div>
      </div>
    </section>

    <section id="governance">
      <div class="decision-preview-card">
        <div>
          <span class="eyebrow">Decision Room</span>
          <h2>غرفة قرار مصممة للفهم، لا لمطاردة المؤشرات.</h2>
          <p>
            معاينة منظمة للنتيجة الرسمية، حالة القراءة، التفسير، المخاطر، والأدلة المتاحة حسب الباقة.
          </p>
          <div class="actions">
            <a class="secondary" href="https://my.ndsp.app/register?next=/decision-room&trial=elite&days=16">استكشف غرفة القرار</a>
          </div>
        </div>

        <div class="preview-surface">
          <div class="preview-head">
            <span>ملخص القرار</span>
            <b>CORE</b>
          </div>
          <div class="preview-lines">
            <i></i><i></i><i></i>
          </div>
          <div class="preview-pills">
            <span>حالة القراءة</span>
            <span>المخاطر</span>
            <span>الأدلة</span>
          </div>
        </div>
      </div>
    </section>

    <section id="plans">
      <div class="section-head">
        <h2>الباقات</h2>
        <h3>اختر مستوى الوصول المناسب.</h3>
      </div>

      <div class="plans-grid" id="plansGrid">
        <article class="plan">
          <small>FREE</small>
          <h3>المجانية</h3>
          <p>استكشاف النتيجة الرسمية والتعرف على منهجية دعم القرار.</p>
          <strong>0 ر.س</strong>
        </article>

        <article class="plan">
          <small>PRO</small>
          <h3>Pro</h3>
          <p>غرفة قرار قياسية ومتابعة منظمة للأصول التي تهم المستخدم الفردي.</p>
          <strong>149 ر.س / شهريًا</strong>
        </article>

        <article class="plan featured">
          <small>ELITE</small>
          <h3>Elite</h3>
          <p>وصول أعمق إلى التفسير، الأدلة، المقارنات، والتقارير.</p>
          <strong>399 ر.س / شهريًا</strong>
        </article>

        <article class="plan">
          <small>SAAS</small>
          <h3>SaaS للمؤسسات</h3>
          <p>مساحات عمل آمنة، صلاحيات، تكاملات، وحوكمة مؤسسية متقدمة.</p>
          <strong>تواصل معنا</strong>
        </article>
      </div>

      <div class="actions">
        <a class="secondary" href="https://my.ndsp.app/subscription">قارن جميع الباقات</a>
      </div>
    </section>

    <section>
      <div class="trial-cta">
        <div>
          <h2>جرّب Elite لمدة 16 يومًا.</h2>
          <p>استكشف غرفة القرار والتقارير والمقارنات قبل اختيار الباقة المناسبة.</p>
          <div class="trial-points">
            <span>دون بطاقة دفع</span>
            <span>دون خصم تلقائي</span>
            <span>تجربة واحدة لكل حساب موثق</span>
            <span>الانتقال إلى المجانية عند الانتهاء</span>
          </div>
        </div>

        <a class="primary" href="https://my.ndsp.app/register?trial=elite&days=16">ابدأ تجربتك الآن</a>
      </div>
    </section>

    <section id="docs">
      <div class="section-head">
        <h2>أسئلة مختصرة</h2>
        <h3>تعريف واضح دون وعود مبالغ فيها.</h3>
      </div>

      <div class="faq-list">
        <details>
          <summary>ما هي NDSP؟</summary>
          <p>NDSP منصة دعم قرار تجمع الأدلة والسياق ضمن إطار محكوم لتقديم اتجاه رسمي قابل للتفسير والتحقق.</p>
        </details>

        <details>
          <summary>هل NDSP منصة تداول؟</summary>
          <p>لا. NDSP لا تنفذ صفقات ولا تعمل كوسيط مالي ولا تقدم أوامر تنفيذ.</p>
        </details>

        <details>
          <summary>ما المقصود بالاتجاه الرسمي؟</summary>
          <p>هو نتيجة CORE المصرح بها ضمن إطار الحوكمة، وليست تجربة داخلية أو قراءة غير معتمدة.</p>
        </details>

        <details>
          <summary>ما المقصود بالتنبيه؟</summary>
          <p>تنبيهات NDSP هي تحديثات لدعم القرار وليست أوامر تداول أو توصيات تنفيذ.</p>
        </details>

        <details>
          <summary>ماذا يحدث بعد انتهاء تجربة 16 يومًا؟</summary>
          <p>ينتقل الحساب إلى المجانية عند عدم الاشتراك، مع قفل المزايا المدفوعة وفق سياسة الاحتفاظ.</p>
        </details>
      </div>
    </section>
  </main>

  <footer>
    <div class="container footer-inner">
      <div>
        <strong>NDSP</strong><br>
        <span>منصة دعم القرار</span>
      </div>

      <div class="footer-links">
        <a href="#methodology">المنهجية</a>
        <a href="#governance">الحوكمة</a>
        <a href="#plans">الباقات</a>
        <a href="https://my.ndsp.app/login">تسجيل الدخول</a>
        <a href="/privacy">الخصوصية</a>
        <a href="/terms">الشروط</a>
        <a href="/disclaimer">إخلاء المسؤولية</a>
        <a href="/support">الدعم</a>
      </div>
    </div>
  </footer>

  <script>
    const panel = document.getElementById('mobilePanel');
    const openMenu = document.getElementById('openMenu');
    const closeMenu = document.getElementById('closeMenu');
    let lastFocus = null;

    function openNav() {
      lastFocus = document.activeElement;
      panel.classList.add('open');
      document.body.classList.add('menu-open');
      closeMenu.focus();
    }

    function closeNav() {
      panel.classList.remove('open');
      document.body.classList.remove('menu-open');
      if (lastFocus) lastFocus.focus();
    }

    openMenu?.addEventListener('click', openNav);
    closeMenu?.addEventListener('click', closeNav);

    panel?.addEventListener('click', event => {
      if (event.target === panel) closeNav();
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeNav();
    });
  </script>
</body>
</html>
HTML

echo "Deploy to live Nginx root..."
sudo cp "$SRC" "$LIVE"
sudo chown www-data:www-data "$LIVE"
sudo chmod 644 "$LIVE"

echo "Verify nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "Verify page..."
curl -I https://ndsp.app
curl -sL https://ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "ndsp.app clean"
curl -sL https://ndsp.app | grep -E "إشارة شراء|إشارة بيع|ربح مضمون|دقة مضمونة" || echo "no forbidden claims"

echo
echo "DONE"
echo "Updated source: $SRC"
echo "Updated live:   $LIVE"
