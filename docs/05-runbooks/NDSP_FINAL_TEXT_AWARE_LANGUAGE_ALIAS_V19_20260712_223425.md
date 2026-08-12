============================================================
NDSP — Final Text-Aware Language and Alias V19
DATE=2026-07-12T22:34:25+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_TEXT_AWARE_LANGUAGE_ALIAS_V19_20260712_223425.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_TEXT_AWARE_LANGUAGE_ALIAS_V19_20260712_223425
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/text-aware-language-alias-v19-20260712_223425
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة روابط التوافق ==
{
  "version": "19",
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

== 4) تثبيت الإصلاح النصي للغة ==
[OK] INDEX_PATCHED=/var/www/ndsp-my/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[OK] تم تثبيت اعتراض زر اللغة بالنص والسمات

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
FINAL_URL=https://my.ndsp.app/?_ndsp_v19=20260712_223425_desktop_home
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=False
LANGUAGE_SECOND=True
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}

--- desktop:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
BODY_TEXT_LENGTH=3257
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=daily-brief
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_compat=settings-alerts
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=decision-support
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- mobile:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v19=20260712_223425_mobile_home
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=2294
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=False
LANGUAGE_SECOND=True
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl"}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
BODY_TEXT_LENGTH=2514
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
BODY_TEXT_LENGTH=1257
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
BODY_TEXT_LENGTH=1257
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
BODY_TEXT_LENGTH=2294
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
BODY_TEXT_LENGTH=1257
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

VALIDATION_ERRORS=["desktop:home:LANGUAGE_FIRST_FAILED", "mobile:home:LANGUAGE_FIRST_FAILED"]
VALIDATION_WARNINGS=[]

============================================================
[ROLLBACK] استمر خطأ مانع بعد V19
============================================================
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_TEXT_AWARE_LANGUAGE_ALIAS_V19_20260712_223425.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/text-aware-language-alias-v19-20260712_223425
FINAL_STATUS=ROLLED_BACK
