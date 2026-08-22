# NDSP Mobile Polish Audit
DATE=2026-07-07T15:47:49+03:00
RUN_FROM=kali
BASE=https://my.ndsp.app
MODE=AUDIT_ONLY
MODIFICATIONS=None

## 1) Fetch locked pages
[200] size=884 title=NDSP /
[200] size=884 title=NDSP /index.html
[200] size=2610 title=NDSP — دعم القرار /decision-support.html
[200] size=2854 title=NDSP — الأسواق والأصول /NDSP_Asset_View.html
[200] size=3310 title=NDSP — مركز القيادة /NDSP_Command_Center.html
[200] size=2611 title=NDSP — الموجز اليومي /NDSP_Daily_Brief.html
[200] size=2579 title=NDSP — الإعدادات والتنبيهات /NDSP_Settings_Alerts.html
[200] size=4677 title=NDSP — إخلاء المسؤولية /disclaimer.html

## 2) Fetch visual CSS assets if present
[200] size=63315 /assets/premium.css
[200] size=14085 /assets/markets-hq.css
[200] size=5526 /assets/ndsp-global-menu.css
[200] size=1081 /assets/ndsp-radar-safe-clean.css

## 3) Mobile readiness static checks
### Page checks
- NDSP_Asset_View.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- NDSP_Command_Center.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- NDSP_Daily_Brief.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- NDSP_Settings_Alerts.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- decision-support.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- disclaimer.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=False
  disclaimer_reference=False
  inline_style_bytes=1895
- home.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0
- index.html.html
  viewport_meta=True
  rtl_dir=True
  arabic_lang=True
  menu_reference=True
  disclaimer_reference=True
  inline_style_bytes=0

### CSS checks
- markets-hq.css
  media_queries=7
  small_breakpoints=3
  overflow_x_controls=1
  grid_rules=25
  flex_wrap_rules=0
- ndsp-global-menu.css
  media_queries=1
  small_breakpoints=0
  overflow_x_controls=0
  grid_rules=2
  flex_wrap_rules=0
- ndsp-radar-safe-clean.css
  media_queries=0
  small_breakpoints=0
  overflow_x_controls=0
  grid_rules=0
  flex_wrap_rules=0
- premium.css
  media_queries=9
  small_breakpoints=1
  overflow_x_controls=2
  grid_rules=53
  flex_wrap_rules=1

### Potential mobile overflow risks
- fixed_width_px in markets-hq.css: ="ltr"] body{font-family:Inter,system-ui,Arial,sans-serif} @media(max-width:900px){ body{padding:11px 9px 28px}.catalog-head{border-radius:27px;paddin
- fixed_width_px in markets-hq.css: portant; } /* ضغط الهيدر على الجوال ليظهر المحتوى أسرع */ @media(max-width:900px){ body{ padding-inline:8px !important; } .catalog-head{
- fixed_width_px in markets-hq.css: border-radius:24px !important; } } /* iPhone narrow */ @media(max-width:430px){ .title h1{ font-size:28px !important; } .title p{ fo
- fixed_width_px in markets-hq.css: 5,239,227,.58); font-weight:850; text-align:center; } @media(max-width:900px){ .market-section{ padding:12px; border-radius:25px; ma
- fixed_width_px in markets-hq.css: -grid{ grid-template-columns:1fr; gap:11px; } } @media(max-width:430px){ .market-section{ margin-inline:-1px; padding:11px; }
- fixed_width_px in markets-hq.css: di:isolate !important; white-space:nowrap !important; } @media(max-width:900px){ .market-accordion{ border-radius:24px; margin-bottom:11px
- fixed_width_px in markets-hq.css: adius:14px; } .asset-row{ min-height:64px; } } @media(max-width:430px){ .market-left{ gap:10px; } .market-left b{ font-size:
- multi_column_grid in markets-hq.css: ,96,.16);color:var(--gold2)} .summary{ margin-top:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px } .sum{ border:1px solid var(--line);border-radius:20
- multi_column_grid in markets-hq.css: ont-size:18px;color:var(--gold2);font-weight:1000} .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px} .asset{ border:1px solid var(--line);borde
- multi_column_grid in markets-hq.css: px}.topbar{align-items:flex-start}.title h1{font-size:25px} .summary{grid-template-columns:repeat(3,1fr)}.sum{padding:11px}.sum b{font-size:21px} .searchbar{grid-templa
- multi_column_grid in markets-hq.css: -width:100% !important; order:-1 !important; } .summary{ grid-template-columns:repeat(3,1fr) !important; gap:8px !important; margin-top:12px !importa
- multi_column_grid in markets-hq.css: ight:1000; direction:ltr; } .market-assets-grid{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; } .empty-market{ border:1px dashed rgb
- nowrap in markets-hq.css: rollbar-width:none} .filters::-webkit-scrollbar{display:none} .filter{white-space:nowrap;border:1px solid var(--line);border-radius:999px;padding:10px 13px;ba
- nowrap in markets-hq.css: px;padding:7px 10px;color:var(--gold);font-size:12px;font-weight:1000;white-space:nowrap} .asset-foot{margin-top:18px;display:grid;grid-template-columns:1fr 1
- nowrap in markets-hq.css: t:center; font-size:17px; } /* إصلاح رقم العد 54 / 54 */ .count{ white-space:nowrap !important; direction:ltr !important; unicode-bidi:isolate !impor
- nowrap in markets-hq.css: lor:#ffe18a; background:rgba(244,210,96,.08); font-weight:1000; white-space:nowrap; } .empty-market{ border:1px dashed rgba(244,210,96,.25); border
- nowrap in markets-hq.css: unt{ direction:ltr !important; unicode-bidi:isolate !important; white-space:nowrap !important; } @media(max-width:900px){ .market-accordion{ bord
- fixed_width_px in ndsp-global-menu.css: line-height:1.6; background:rgba(255,255,255,.02); } @media(max-width:520px){ .ndsp-menu-button{ height:44px; min-width:44px; paddi
- fixed_position in ndsp-global-menu.css: 3; --ndsp-menu-muted:rgba(245,239,227,.62); } .ndsp-menu-button{ position:fixed; z-index:99990; inset-block-start:calc(env(safe-area-inset-top, 0
- fixed_position in ndsp-global-menu.css: 5px} .ndsp-menu-button .bars::after{bottom:0} .ndsp-menu-backdrop{ position:fixed; z-index:99991; inset:0; background:rgba(0,0,0,.48); backdrop
- fixed_position in ndsp-global-menu.css: r-events:none; transition:opacity .22s ease; } .ndsp-menu-panel{ position:fixed; z-index:99992; inset-block:10px; inset-inline-start:10px; wi
- fixed_width_px in premium.css: isplay:grid;grid-template-columns:390px minmax(0,1fr);gap:18px}.radar{width:330px;height:330px;border-radius:50%;margin:auto;position:relative;border:1
- fixed_width_px in premium.css: id var(--line);border-radius:18px;padding:14px;color:#ddd} @media(max-width:920px){.shell{display:block}.sidebar{display:none}.main{padding:14px}.mobil
- fixed_width_px in premium.css: }h1{font-size:28px}.hero{padding:20px}.table-wrap{overflow:auto}table{min-width:980px}.radar{width:285px;height:285px}.core{inset:98px}.node{width:82px;fon
- fixed_width_px in premium.css: o{padding:20px}.table-wrap{overflow:auto}table{min-width:980px}.radar{width:285px;height:285px}.core{inset:98px}.node{width:82px;font-size:10px}.n1{top
- fixed_width_px in premium.css: COLOR_V11_END */ /* NDSP_MOBILE_COMMAND_DECK_V4_START */ @media(max-width:920px){ html,body{ overflow-x:hidden !important; overflow-y:auto
- fixed_width_px in premium.css: in(86vw,430px) !important; height:min(86vw,430px) !important; max-width:430px !important; max-height:430px !important; border-radius:50% !impor
- fixed_width_px in premium.css: ize:16px; line-height:1; } .radar .node{ z-index:4 !important; width:112px !important; min-height:58px !important; border-radius:18px !impor
- fixed_width_px in premium.css: rgba(4,4,5,.94)); font-weight:900; line-height:1.7; } @media(max-width:520px){ .radar{ width:calc(100vw - 58px) !important; height:calc(
- fixed_width_px in premium.css: in(86vw,440px) !important; height:min(86vw,440px) !important; max-width:440px !important; max-height:440px !important; margin:0 auto !important
- fixed_width_px in premium.css: ize:14px; line-height:1; } .radar .node{ z-index:6 !important; width:106px !important; min-height:56px !important; padding:8px 8px !importan
- fixed_width_px in premium.css: line-height:1.7 !important; direction:rtl !important; } @media(max-width:520px){ .radar{ width:calc(100vw - 58px) !important; height:calc(
- fixed_width_px in premium.css: rp-gold-hi); width:min(86vw,440px); height:min(86vw,440px); max-width:440px; max-height:440px; margin:0 auto; position:relative; border-r
- fixed_width_px in premium.css: line-height:1; } .ndsp-pro-node{ position:absolute; z-index:7; width:106px; min-height:56px; padding:8px 8px; border-radius:18px; border
- fixed_width_px in premium.css: font-weight:900; line-height:1.7; direction:rtl; } @media(max-width:520px){ .radar-box.ndsp-pro-activated{ padding:18px 8px 16px !importa
- fixed_width_px in premium.css: ow:visible; } .ndsp-svg-v8-node{ position:absolute; z-index:5; width:105px; min-height:58px; border-radius:19px; border:1px solid rgba(255
- fixed_width_px in premium.css: 8-radar[data-state="unknown"]{--ndsp-state-color:#ffe18a} @media(max-width:520px){ .ndsp-svg-v8-radar{ width:calc(100vw - 48px); height:calc
- fixed_width_px in premium.css: ow:visible; } .ndsp-svg-v9-node{ position:absolute; z-index:8; width:104px; min-height:58px; border-radius:18px; border:1px solid rgba(255
- fixed_width_px in premium.css: 9-radar[data-state="unknown"]{--ndsp-state-color:#ffe18a} @media(max-width:520px){ .ndsp-svg-v9-radar{ width:calc(100vw - 44px); height:calc
- fixed_width_px in premium.css: rgba(4,4,5,.95)); font-weight:900; line-height:1.7; } @media(max-width:520px){ .radar-box.ndsp-art-v10-active{ padding:18px 7px 16px !import
- fixed_width_px in premium.css: ircle at 50% 46%,rgba(244,210,96,.65),transparent 42%); } @media(max-width:520px){ .radar-box.ndsp-exact-ref-v11-active{ padding:0 !important;
- multi_column_grid in premium.css: in{min-width:0;padding:24px}.mobile{display:none}.topbar{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}.metric,.card,.control,.radar-box,.b
- multi_column_grid in premium.css: }p{color:var(--muted);line-height:1.9;margin:0}.controls{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:16px 0}.pills{display:flex;flex-wrap:wrap;gap:8px}.pi
- multi_column_grid in premium.css: ext);border-radius:14px;padding:12px;outline:none}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}.card h3{margin:0 0 8px}.big{font-si
- multi_column_grid in premium.css: nt; } .mobile-nav > [data-nav]{ display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:7px !important; width:100% !im
- multi_column_grid in premium.css: tant; width:min(94%,760px) !important; display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:8px !important; border:1px solid r
- multi_column_grid in premium.css: .radar .core .state-dots{font-size:12px} .ndsp-radar-legend{ grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:6px !important; padding:8px !i
- multi_column_grid in premium.css: tant; width:min(94%,760px) !important; display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:8px !important; border:1px solid r
- multi_column_grid in premium.css: .radar .core .state-dots{font-size:11px} .ndsp-radar-legend{ grid-template-columns:repeat(4,minmax(0,1fr)) !important; gap:6px !important; padding:8px !i
- multi_column_grid in premium.css: gend{ margin:14px auto 0; width:min(94%,760px); display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; border:1px solid rgba(244,210,96,.28);
- multi_column_grid in premium.css: size:7.5px} .ndsp-pro-dots{font-size:11px} .ndsp-pro-legend{ grid-template-columns:repeat(4,minmax(0,1fr)); gap:6px; padding:8px; } .ndsp-pro-legend
- multi_column_grid in premium.css: gend{ margin:14px auto 0; width:min(94%,760px); display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; direction:ltr; border:1px solid rgba(2
- multi_column_grid in premium.css: gend{ margin:14px auto 0; width:min(94%,760px); display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; direction:ltr; border:1px solid rgba(2
- multi_column_grid in premium.css: gend{ margin:14px auto 0; width:min(94%,760px); display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; direction:ltr; border:1px solid rgba(2
- fixed_position in premium.css: -family:Arial,Tahoma,sans-serif;direction:rtl} body:before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(cir

### Safe polish recommendation
- Start with CSS-only polish where possible.
- Prefer premium.css and markets-hq.css for spacing, gaps, font scaling, and responsive grids.
- Do not touch radar/menu/disclaimer JS unless explicitly approved.
- If any HTML is touched later, keep changes limited to class names, wrappers, or text spacing only.

## 4) Audit conclusion
- This was an audit-only mobile polish scan.
- No server files were modified.
- No runtime files were modified.
- Use this report to decide whether a later CSS-only patch is needed.

FINAL_STATUS=MOBILE_POLISH_AUDIT_DONE
REPORT=NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
