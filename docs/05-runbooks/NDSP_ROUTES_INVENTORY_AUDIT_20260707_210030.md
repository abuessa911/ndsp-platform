# NDSP Routes Inventory Audit
DATE=2026-07-07T21:00:30+03:00
RUN_FROM=kali
BASE=https://my.ndsp.app
MODE=READ_ONLY
MODIFICATIONS=None

## 1) Server HTML inventory
alerts-log.html
asset-selector.html
completed-decisions.html
daily-brief.html
decision-center.html
decision-guide.html
decision-modes-guide.html
decision-radar.html
decision-support.html
disclaimer.html
dollar-impact.html
dollar-news.html
index.html
my-watchlist.html
NDSP_Asset_View.html
NDSP_Command_Center.html
NDSP_Daily_Brief.html
NDSP_Settings_Alerts.html
nmp.html
pro-guide.html
settings.html
support-center.html
usd-pulse.html
user-guide.html

## 2) Public HTTP check for all HTML routes
[200] size=2491 menu_refs=2 disclaimer_refs=1 title=NDSP — سجل التنبيهات /alerts-log.html
[200] size=2738 menu_refs=2 disclaimer_refs=1 title=NDSP — Markets & Assets /asset-selector.html
[200] size=2519 menu_refs=2 disclaimer_refs=1 title=NDSP — سجل القرار /completed-decisions.html
[200] size=2503 menu_refs=2 disclaimer_refs=1 title=NDSP — موجز اليوم /daily-brief.html
[200] size=2502 menu_refs=2 disclaimer_refs=1 title=NDSP — مركز القرار /decision-center.html
[200] size=2442 menu_refs=2 disclaimer_refs=1 title=NDSP — الدليل /decision-guide.html
[200] size=2436 menu_refs=2 disclaimer_refs=1 title=NDSP — أنماط القرار /decision-modes-guide.html
[200] size=3271 menu_refs=2 disclaimer_refs=1 title=NDSP — رادار القرار /decision-radar.html
[200] size=2639 menu_refs=2 disclaimer_refs=1 title=NDSP — دعم القرار /decision-support.html
[200] size=4677 menu_refs=0
0 disclaimer_refs=0
0 title=NDSP — إخلاء المسؤولية /disclaimer.html
[200] size=2492 menu_refs=2 disclaimer_refs=1 title=NDSP — أثر الدولار /dollar-impact.html
[200] size=2502 menu_refs=2 disclaimer_refs=1 title=NDSP — أخبار الدولار /dollar-news.html
[200] size=913 menu_refs=2 disclaimer_refs=1 title=NDSP /index.html
[200] size=3667 menu_refs=2 disclaimer_refs=1 title=NDSP — قائمة المتابعة /my-watchlist.html
[200] size=2883 menu_refs=2 disclaimer_refs=1 title=NDSP — الأسواق والأصول /NDSP_Asset_View.html
[200] size=3339 menu_refs=2 disclaimer_refs=1 title=NDSP — مركز القيادة /NDSP_Command_Center.html
[200] size=2640 menu_refs=2 disclaimer_refs=1 title=NDSP — الموجز اليومي /NDSP_Daily_Brief.html
[200] size=2608 menu_refs=2 disclaimer_refs=1 title=NDSP — الإعدادات والتنبيهات /NDSP_Settings_Alerts.html
[200] size=2496 menu_refs=2 disclaimer_refs=1 title=NDSP — NMP /nmp.html
[200] size=2441 menu_refs=2 disclaimer_refs=1 title=NDSP — دليل المحترف /pro-guide.html
[200] size=2439 menu_refs=2 disclaimer_refs=1 title=NDSP — الإعدادات /settings.html
[200] size=2420 menu_refs=2 disclaimer_refs=1 title=NDSP — مركز الدعم /support-center.html
[200] size=2488 menu_refs=2 disclaimer_refs=1 title=NDSP — نبض الدولار /usd-pulse.html
[200] size=2431 menu_refs=2 disclaimer_refs=1 title=NDSP — دليل المستخدم /user-guide.html

## 3) Core locked routes check
[200] size=913 title=NDSP /
[200] size=913 title=NDSP /index.html
[200] size=2639 title=NDSP — دعم القرار /decision-support.html
[200] size=2883 title=NDSP — الأسواق والأصول /NDSP_Asset_View.html
[200] size=3339 title=NDSP — مركز القيادة /NDSP_Command_Center.html
[200] size=2640 title=NDSP — الموجز اليومي /NDSP_Daily_Brief.html
[200] size=2608 title=NDSP — الإعدادات والتنبيهات /NDSP_Settings_Alerts.html
[200] size=4677 title=NDSP — إخلاء المسؤولية /disclaimer.html

## 4) Findings summary
- This audit only lists routes and checks public availability.
- No server files were modified.
- No runtime files were modified.
- Next step is to classify pages into: keep / alias / improve later / remove only if approved.

FINAL_STATUS=ROUTES_INVENTORY_AUDIT_DONE
REPORT=NDSP_ROUTES_INVENTORY_AUDIT_20260707_210030.md
