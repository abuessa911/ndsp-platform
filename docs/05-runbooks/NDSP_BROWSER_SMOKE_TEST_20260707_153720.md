# NDSP Browser Smoke Test
DATE=2026-07-07T15:37:20+03:00
RUN_FROM=kali
BASE=https://my.ndsp.app
API=https://api.ndsp.app

## 1) Public Pages
[200] size=884 title=NDSP https://my.ndsp.app/
[200] size=884 title=NDSP https://my.ndsp.app/index.html
[200] size=2610 title=NDSP — دعم القرار https://my.ndsp.app/decision-support.html
[200] size=2854 title=NDSP — الأسواق والأصول https://my.ndsp.app/NDSP_Asset_View.html
[200] size=3310 title=NDSP — مركز القيادة https://my.ndsp.app/NDSP_Command_Center.html
[200] size=2611 title=NDSP — الموجز اليومي https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=2579 title=NDSP — الإعدادات والتنبيهات https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=4677 title=NDSP — إخلاء المسؤولية https://my.ndsp.app/disclaimer.html

## 2) Locked Assets
[200] size=9846 https://my.ndsp.app/assets/ndsp-radar-safe-clean.js?v=24-command-bind
[200] size=6709 https://my.ndsp.app/assets/ndsp-decision-support-bind.js?v=1
[200] size=10160 https://my.ndsp.app/assets/ndsp-asset-view-live-bind.js?v=1
[200] size=9632 https://my.ndsp.app/assets/ndsp-daily-brief-live-bind.js?v=1
[200] size=11545 https://my.ndsp.app/assets/ndsp-settings-alerts-bind.js?v=1
[200] size=500 https://my.ndsp.app/assets/ndsp-disclaimer-gate.js?v=1
[200] size=10444 https://my.ndsp.app/assets/ndsp-global-menu.js?v=25-canonical-page-match

## 3) API Live Samples
[200] ETHUSDT
  ok= True
  symbol= ETHUSDT
  live_price= 1780.77
  quality= 86
  scenario= UNDER_MONITORING
  direction= قراءة أسبوعي · ضغط هابط
  nmp= AVAILABLE 1583.4
[200] BTCUSDT
  ok= True
  symbol= BTCUSDT
  live_price= 63406.0
  quality= 86
  scenario= UNDER_MONITORING
  direction= قراءة أسبوعي · ضغط هابط
  nmp= AVAILABLE 61056.47
[200] XAUUSD
  ok= True
  symbol= XAUUSD
  live_price= 4176.2998046875
  quality= 59
  scenario= UNDER_MONITORING
  direction= قراءة أسبوعي · ضغط سفلي
  nmp= UNAVAILABLE None
[200] USOIL
  ok= True
  symbol= USOIL
  live_price= 69.02999877929688
  quality= 56
  scenario= UNDER_MONITORING
  direction= قراءة أسبوعي · ضغط سفلي
  nmp= UNAVAILABLE None

## 4) Public Forbidden Language Scan
Scanning public HTML pages only.
[OK] / no obvious forbidden public wording
[OK] /index.html no obvious forbidden public wording
[CHECK] /decision-support.html has possible matches:
        1 بيع
        1 تنفيذ
        1 توصية مالية
        1 شراء
[OK] /NDSP_Asset_View.html no obvious forbidden public wording
[CHECK] /NDSP_Command_Center.html has possible matches:
        1 بيع
        1 تنفيذ
        1 توصية مالية
        1 شراء
[CHECK] /NDSP_Daily_Brief.html has possible matches:
        1 بيع
        1 تنفيذ
        1 توصية مالية
        1 شراء
[CHECK] /NDSP_Settings_Alerts.html has possible matches:
        1 بيع
        1 تنفيذ
        1 توصية مالية
        1 شراء
[CHECK] /disclaimer.html has possible matches:
        1 execute
        2 تنفيذ
        2 توصية مالية

## 5) Local Release Files
-rw-rw-r-- 1 nawaf nawaf 8.3K ‏Jul ‏ 7 ‏12:‏21 NDSP_FINAL_GOVERNANCE_CLOSEOUT_20260707_111907.tar.gz
-rw-rw-r-- 1 nawaf nawaf 112K ‏Jul ‏ 7 ‏11:‏59 NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz

## Final
FINAL_STATUS=BROWSER_SMOKE_TEST_DONE
REPORT=NDSP_BROWSER_SMOKE_TEST_20260707_153720.md
