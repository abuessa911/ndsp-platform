============================================================
NDSP — Final Grouped Language and Alias V18
DATE=2026-07-12T22:25:58+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_GROUPED_LANGUAGE_ALIAS_V18_20260712_222558.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_GROUPED_LANGUAGE_ALIAS_V18_20260712_222558
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/grouped-language-alias-v18-20260712_222558
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة روابط التوافق ==
{
  "version": "18",
  "aliases": {
    "/NDSP_Asset_View.html": "/markets",
    "/NDSP_Command_Center.html": "/decisions",
    "/NDSP_Daily_Brief.html": "/decisions?ndsp_compat=daily-brief",
    "/NDSP_Settings_Alerts.html": "/?ndsp_compat=settings-alerts",
    "/decision-support.html": "/decisions?ndsp_compat=decision-support"
  }
}
[OK] خريطة الروابط تحتوي خمسة مسارات

== 2) بوابة API قبل التعديل ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 3) تحديد ملفات index ومجلدات النشر ==
INDEX_TARGET=/var/www/ndsp-my/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
ALIAS_DIRECTORY=/var/www/ndsp-my

== 4) تثبيت تبديل اللغة المجمع ==
[OK] INDEX_PATCHED=/var/www/ndsp-my/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[OK] تم تثبيت تبديل اللغة للمفاتيح الثلاثة

== 5) إنشاء روابط التوافق ==
[OK] ALIAS=/var/www/ndsp-my/NDSP_Asset_View.html -> /markets
[OK] ALIAS=/var/www/ndsp-my/NDSP_Command_Center.html -> /decisions
[OK] ALIAS=/var/www/ndsp-my/NDSP_Daily_Brief.html -> /decisions?ndsp_compat=daily-brief
[OK] ALIAS=/var/www/ndsp-my/NDSP_Settings_Alerts.html -> /?ndsp_compat=settings-alerts
[OK] ALIAS=/var/www/ndsp-my/decision-support.html -> /decisions?ndsp_compat=decision-support
[OK] تم إنشاء روابط التوافق الخمسة

== 6) التحقق من النشر العام ==
PUBLIC_ALIAS=/NDSP_Asset_View.html HTTP=200
PUBLIC_ALIAS=/NDSP_Command_Center.html HTTP=200
PUBLIC_ALIAS=/NDSP_Daily_Brief.html HTTP=200
PUBLIC_ALIAS=/NDSP_Settings_Alerts.html HTTP=200
PUBLIC_ALIAS=/decision-support.html HTTP=200
[OK] التعديلات ظاهرة عبر my.ndsp.app

== 7) اختبار الكمبيوتر والجوال ==

== 8) تحليل النتائج ==

--- desktop:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v18=20260712_222558_desktop_home&fresh=1783887983382
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr"}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr"}

--- desktop:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
BODY_TEXT_LENGTH=3315
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2124
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=daily-brief
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2124
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_compat=settings-alerts
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=3214
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=decision-support
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2124
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- mobile:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v18=20260712_222558_mobile_home&fresh=1783888032653
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=2294
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr"}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr"}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
BODY_TEXT_LENGTH=2555
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=daily-brief
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_compat=settings-alerts
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=2421
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=decision-support
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

VALIDATION_ERRORS=["desktop:home:LANGUAGE_SECOND_FAILED", "mobile:home:LANGUAGE_SECOND_FAILED"]
VALIDATION_WARNINGS=[]

============================================================
[ROLLBACK] استمر خطأ مانع بعد V18
============================================================
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_GROUPED_LANGUAGE_ALIAS_V18_20260712_222558.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/grouped-language-alias-v18-20260712_222558
FINAL_STATUS=ROLLED_BACK
