============================================================
NDSP — Final Language and Alias Fix V17
DATE=2026-07-12T22:19:53+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_LANGUAGE_ALIAS_FIX_V17_20260712_221953.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_LANGUAGE_ALIAS_FIX_V17_20260712_221953
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/final-language-alias-v17-20260712_221953
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة الروابط الآمنة ==
{
  "version": "17",
  "aliases": {
    "/NDSP_Asset_View.html": "/markets",
    "/NDSP_Command_Center.html": "/decisions",
    "/NDSP_Daily_Brief.html": "/decisions?ndsp_compat=daily-brief",
    "/NDSP_Settings_Alerts.html": "/?ndsp_compat=settings-alerts",
    "/decision-support.html": "/decisions?ndsp_compat=decision-support"
  }
}
[OK] خريطة الروابط تحتوي خمسة مسارات

== 2) بوابة API ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 3) اكتشاف مفتاح اللغة الحقيقي ==
LANGUAGE_PROBE_RC=0
{
  "before": {
    "lang": "ar",
    "dir": "rtl",
    "url": "https://my.ndsp.app/?_ndsp_language_probe=20260712_221953"
  },
  "after": {
    "lang": "en",
    "dir": "ltr",
    "url": "https://my.ndsp.app/?_ndsp_language_probe=20260712_221953&fresh=1783887620365"
  },
  "selected": {
    "type": "localStorage",
    "key": "ndsp_lang_final",
    "beforeExists": false,
    "beforeValue": null,
    "afterExists": true,
    "afterValue": "en",
    "score": 350
  },
  "all_changes": [
    {
      "type": "localStorage",
      "key": "ndsp_lang_final",
      "beforeExists": false,
      "beforeValue": null,
      "afterExists": true,
      "afterValue": "en",
      "score": 350
    },
    {
      "type": "localStorage",
      "key": "ndsp_final_lang",
      "beforeExists": false,
      "beforeValue": null,
      "afterExists": true,
      "afterValue": "en",
      "score": 350
    },
    {
      "type": "localStorage",
      "key": "ndsp_lang",
      "beforeExists": false,
      "beforeValue": null,
      "afterExists": true,
      "afterValue": "en",
      "score": 350
    }
  ]
}
LANGUAGE_STORAGE_TYPE=localStorage
LANGUAGE_STORAGE_KEY=ndsp_lang_final
[OK] تم اكتشاف مفتاح اللغة الحقيقي

== 4) تحديد ملفات index ومجلدات النشر ==
INDEX_TARGET=/var/www/ndsp-my/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
ALIAS_DIRECTORY=/var/www/ndsp-my

== 5) تثبيت الإصلاح الحتمي للغة ==
[OK] INDEX_PATCHED=/var/www/ndsp-my/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[OK] تم تثبيت إصلاح اللغة

== 6) إنشاء روابط التوافق ==
[OK] ALIAS=/var/www/ndsp-my/NDSP_Asset_View.html -> /markets
[OK] ALIAS=/var/www/ndsp-my/NDSP_Command_Center.html -> /decisions
[OK] ALIAS=/var/www/ndsp-my/NDSP_Daily_Brief.html -> /decisions?ndsp_compat=daily-brief
[OK] ALIAS=/var/www/ndsp-my/NDSP_Settings_Alerts.html -> /?ndsp_compat=settings-alerts
[OK] ALIAS=/var/www/ndsp-my/decision-support.html -> /decisions?ndsp_compat=decision-support
[OK] تم إنشاء روابط التوافق الخمسة

== 7) التحقق من النشر العام ==
PUBLIC_ALIAS=/NDSP_Asset_View.html HTTP=200
PUBLIC_ALIAS=/NDSP_Command_Center.html HTTP=200
PUBLIC_ALIAS=/NDSP_Daily_Brief.html HTTP=200
PUBLIC_ALIAS=/NDSP_Settings_Alerts.html HTTP=200
PUBLIC_ALIAS=/decision-support.html HTTP=200
[OK] الإصلاحات منشورة عبر my.ndsp.app

== 8) الاختبار النهائي ==

== 9) تحليل النتائج ==

--- desktop:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v17=20260712_221953_desktop_home&fresh=1783887633568
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False
LANGUAGE_INITIAL_STATE={"exists": false, "value": null}
LANGUAGE_FIRST_STATE={"exists": true, "value": "en"}
LANGUAGE_SECOND_STATE={"exists": true, "value": "en"}

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
FINAL_URL=https://my.ndsp.app/?_ndsp_v17=20260712_221953_mobile_home&fresh=1783887684700
FINAL_PATH=/
EXPECTED_PATH=/
BODY_TEXT_LENGTH=2294
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False
LANGUAGE_INITIAL_STATE={"exists": false, "value": null}
LANGUAGE_FIRST_STATE={"exists": true, "value": "en"}
LANGUAGE_SECOND_STATE={"exists": true, "value": "en"}
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
[ROLLBACK] استمر خطأ مانع بعد V17
============================================================
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_LANGUAGE_ALIAS_FIX_V17_20260712_221953.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/final-language-alias-v17-20260712_221953
FINAL_STATUS=ROLLED_BACK
