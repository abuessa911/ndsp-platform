============================================================
NDSP — Legacy Navigation and Language V16
DATE=2026-07-12T22:09:50+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_LEGACY_NAVIGATION_LANGUAGE_V16_20260712_220950.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_LEGACY_NAVIGATION_LANGUAGE_V16_20260712_220950
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/legacy-navigation-language-v16-20260712_220950
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة التوافق ==
{
  "version": "16",
  "aliases": {
    "/NDSP_Asset_View.html": {
      "mode": "route",
      "value": "/markets"
    },
    "/NDSP_Command_Center.html": {
      "mode": "route",
      "value": "/decisions"
    },
    "/NDSP_Daily_Brief.html": {
      "mode": "target",
      "value": "daily-brief"
    },
    "/NDSP_Settings_Alerts.html": {
      "mode": "target",
      "value": "settings-alerts"
    },
    "/decision-support.html": {
      "mode": "target",
      "value": "decision-support"
    }
  }
}
[OK] خريطة التوافق تحتوي خمسة روابط

== 2) بوابة API ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 3) تحديد ملفات index ومجلدات النشر ==
INDEX_TARGET=/var/www/ndsp-my/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
INDEX_TARGET=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
ALIAS_DIRECTORY=/var/www/ndsp-my

== 4) تثبيت جسر التنقل واللغة ==
[OK] INDEX_PATCHED=/var/www/ndsp-my/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[OK] تم تثبيت جسر التنقل واللغة

== 5) إنشاء ملفات التوافق ==
[OK] ALIAS=/var/www/ndsp-my/NDSP_Asset_View.html MODE=route VALUE=/markets
[OK] ALIAS=/var/www/ndsp-my/NDSP_Command_Center.html MODE=route VALUE=/decisions
[OK] ALIAS=/var/www/ndsp-my/NDSP_Daily_Brief.html MODE=target VALUE=daily-brief
[OK] ALIAS=/var/www/ndsp-my/NDSP_Settings_Alerts.html MODE=target VALUE=settings-alerts
[OK] ALIAS=/var/www/ndsp-my/decision-support.html MODE=target VALUE=decision-support
[OK] تم إنشاء ملفات التوافق الخمسة

== 6) التحقق من النشر العام ==
PUBLIC_ALIAS=/NDSP_Asset_View.html HTTP=200
PUBLIC_ALIAS=/NDSP_Command_Center.html HTTP=200
PUBLIC_ALIAS=/NDSP_Daily_Brief.html HTTP=200
PUBLIC_ALIAS=/NDSP_Settings_Alerts.html HTTP=200
PUBLIC_ALIAS=/decision-support.html HTTP=200
[OK] جميع التعديلات ظاهرة عبر my.ndsp.app

== 7) اختبار المتصفح ==

== 8) تحليل النتائج ==

--- desktop:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v16=20260712_220950_desktop_home&fresh=1783887010576
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False

--- desktop:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
BODY_TEXT_LENGTH=3315
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null

--- desktop:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
BODY_TEXT_LENGTH=2124
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null

--- desktop:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_legacy_fallback=daily-brief
BODY_TEXT_LENGTH=2124
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "daily-brief", "status": "fallback", "destination": "/decisions", "completedAt": 1783887049832}

--- desktop:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_legacy_fallback=settings-alerts
BODY_TEXT_LENGTH=3214
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "settings-alerts", "status": "fallback", "destination": "/", "completedAt": 1783887063501}

--- desktop:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
BODY_TEXT_LENGTH=2132
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "decision-support", "status": "clicked", "score": 40, "text": "decision engine", "route": "/decisions", "completedAt": 1783887068589}

--- mobile:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v16=20260712_220950_mobile_home&fresh=1783887086949
BODY_TEXT_LENGTH=2294
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
BODY_TEXT_LENGTH=2555
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE=null
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_legacy_fallback=daily-brief
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "daily-brief", "status": "fallback", "destination": "/decisions", "completedAt": 1783887127502}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_legacy_fallback=settings-alerts
BODY_TEXT_LENGTH=2421
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "settings-alerts", "status": "fallback", "destination": "/", "completedAt": 1783887142577}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
BODY_TEXT_LENGTH=1364
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LEGACY_STATE={"target": "decision-support", "status": "clicked", "score": 40, "text": "view engine →", "route": "/decisions", "completedAt": 1783887147849}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

VALIDATION_ERRORS=["desktop:home:LANGUAGE_SECOND_FAILED", "mobile:home:LANGUAGE_SECOND_FAILED"]
VALIDATION_WARNINGS=["desktop:daily_brief:LEGACY_FALLBACK:/decisions", "desktop:settings_alerts:LEGACY_FALLBACK:/", "mobile:daily_brief:LEGACY_FALLBACK:/decisions", "mobile:settings_alerts:LEGACY_FALLBACK:/"]

============================================================
[ROLLBACK] استمرت أخطاء مانعة بعد V16
============================================================
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] REMOVED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_LEGACY_NAVIGATION_LANGUAGE_V16_20260712_220950.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/legacy-navigation-language-v16-20260712_220950
FINAL_STATUS=ROLLED_BACK
