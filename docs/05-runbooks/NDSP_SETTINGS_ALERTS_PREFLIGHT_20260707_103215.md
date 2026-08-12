# NDSP Settings Alerts Preflight
DATE=2026-07-07T10:32:15+02:00
FRONTEND=/var/www/ndsp-my

## 1) Target file
-rw-rw-r-- 1 nawaf511 nawaf511 2.5K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Settings_Alerts.html

## 2) HTML markers
1:<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#040405"><title>NDSP — الإعدادات والتنبيهات</title><link rel="stylesheet" href="/assets/premium.css?v=22-restore-radar">    <link rel="stylesheet" href="/assets/ndsp-global-menu.css?v=24-page-match">
2:  <link rel="stylesheet" href="/assets/ndsp-page-name-sync-v25.css?v=25-page-name">
3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
4:  <!-- NDSP_CANONICAL_PAGE_ALIAS_V1 source=settings.html -->
5:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>الإعدادات والتنبيهات</h1><p>إعدادات العرض والتنبيهات.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>
6:  <script src="/assets/ndsp-page-name-sync-v25.js?v=25-page-name"></script>

## 3) Script references
1:<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#040405"><title>NDSP — الإعدادات والتنبيهات</title><link rel="stylesheet" href="/assets/premium.css?v=22-restore-radar">    <link rel="stylesheet" href="/assets/ndsp-global-menu.css?v=24-page-match">
2:  <link rel="stylesheet" href="/assets/ndsp-page-name-sync-v25.css?v=25-page-name">
3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
5:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>الإعدادات والتنبيهات</h1><p>إعدادات العرض والتنبيهات.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>
6:  <script src="/assets/ndsp-page-name-sync-v25.js?v=25-page-name"></script>

## 4) Existing alert/config files

## 5) HTTP checks
[200] size=2514 https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=2611 https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=2854 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=2610 https://my.ndsp.app/decision-support.html
[200] size=3310 https://my.ndsp.app/NDSP_Command_Center.html

## 6) API sample
ok= True
symbol= ETHUSDT
live_price= 1771.24
quality= 86
scenario= UNDER_MONITORING
direction= قراءة أسبوعي · ضغط هابط
nmp= AVAILABLE 1583.4

FINAL_STATUS=SETTINGS_ALERTS_PREFLIGHT_DONE
REPORT=docs/05-runbooks/NDSP_SETTINGS_ALERTS_PREFLIGHT_20260707_103215.md
