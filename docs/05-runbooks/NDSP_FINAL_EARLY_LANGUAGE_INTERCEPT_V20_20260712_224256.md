============================================================
NDSP — Final Early Language Intercept V20
DATE=2026-07-12T22:42:56+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/early-language-intercept-v20-20260712_224256
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة روابط التوافق ==
{
  "version": "20",
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

== 4) تثبيت اعتراض اللغة المبكر ==
[OK] INDEX_PATCHED=/var/www/ndsp-my/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[OK] INDEX_PATCHED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
[OK] تم تثبيت اعتراض pointerdown المبكر

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
FINAL_URL=https://my.ndsp.app/?_ndsp_v20=20260712_224256_desktop_home&fresh=1783888995770
FINAL_PATH=/
EXPECTED_PATH=/
COMPATIBILITY_ONLY=False
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=True
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl", "v20": true}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr", "v20": true}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl", "v20": true}

--- desktop:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
COMPATIBILITY_ONLY=False
BODY_TEXT_LENGTH=3257
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:command_center ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
COMPATIBILITY_ONLY=False
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:daily_brief ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=daily-brief
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
COMPATIBILITY_ONLY=True
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:settings_alerts ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?ndsp_compat=settings-alerts
FINAL_PATH=/
EXPECTED_PATH=/
COMPATIBILITY_ONLY=True
BODY_TEXT_LENGTH=3070
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- desktop:decision_support ---
HTTP=200
FINAL_URL=https://my.ndsp.app/decisions?ndsp_compat=decision-support
FINAL_PATH=/decisions
EXPECTED_PATH=/decisions
COMPATIBILITY_ONLY=True
BODY_TEXT_LENGTH=2000
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False

--- mobile:home ---
HTTP=200
FINAL_URL=https://my.ndsp.app/?_ndsp_v20=20260712_224256_mobile_home&fresh=1783889030245
FINAL_PATH=/
EXPECTED_PATH=/
COMPATIBILITY_ONLY=False
BODY_TEXT_LENGTH=2296
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
LANGUAGE_FOUND=True
LANGUAGE_FIRST=True
LANGUAGE_SECOND=True
LANGUAGE_INITIAL_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl", "v20": true}
LANGUAGE_FIRST_STATE={"values": {"ndsp_lang_final": "en", "ndsp_final_lang": "en", "ndsp_lang": "en"}, "lang": "en", "dir": "ltr", "v20": true}
LANGUAGE_SECOND_STATE={"values": {"ndsp_lang_final": null, "ndsp_final_lang": null, "ndsp_lang": null}, "lang": "ar", "dir": "rtl", "v20": true}
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

--- mobile:asset ---
HTTP=200
FINAL_URL=https://my.ndsp.app/markets?symbol=ETHUSDT&timeframe=weekly
FINAL_PATH=/markets
EXPECTED_PATH=/markets
COMPATIBILITY_ONLY=False
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
COMPATIBILITY_ONLY=False
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
COMPATIBILITY_ONLY=True
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
COMPATIBILITY_ONLY=True
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
COMPATIBILITY_ONLY=True
BODY_TEXT_LENGTH=1257
ROUTE_404=False
VISIBLE_404=False
OVERFLOW=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_MENU_CHANGED=True

VALIDATION_ERRORS=[]
VALIDATION_WARNINGS=["desktop:daily_brief:COMPATIBILITY_REDIRECT_ONLY", "desktop:settings_alerts:COMPATIBILITY_REDIRECT_ONLY", "desktop:decision_support:COMPATIBILITY_REDIRECT_ONLY", "mobile:daily_brief:COMPATIBILITY_REDIRECT_ONLY", "mobile:settings_alerts:COMPATIBILITY_REDIRECT_ONLY", "mobile:decision_support:COMPATIBILITY_REDIRECT_ONLY"]
[WARN] نجحت الوظائف مع روابط توافق لصفحات غير مبنية بعد

== 9) لقطات الشاشة ==
SCREENSHOT_COUNT=12
[OK] تم إنشاء 12 لقطة شاشة

== 10) بوابة API بعد التعديل ==
POST_API_HTTP=200
[OK] عقد API لم يتأثر

== 11) تسجيل الحوكمة ==

## Final Governance Summary

- Portal: https://my.ndsp.app
- API: https://api.ndsp.app
- Route map: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256/route-map.json
- Browser result: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256/browser-results.json
- Backup directory: /home/nawaf511/ndsp_ui_backups/early-language-intercept-v20-20260712_224256
- Rollback manifest: /home/nawaf511/ndsp_ui_backups/early-language-intercept-v20-20260712_224256/rollback-manifest.tsv
- Language keys:
  - ndsp_lang_final
  - ndsp_final_lang
  - ndsp_lang
- Language interception:
  - window capture
  - pointerdown
  - mousedown
  - touchstart
  - click
  - keyboard
- English state: all language keys equal en
- Arabic state: all language keys removed
- Language first click: tested
- Language second click: tested
- Mobile menu: tested
- Legacy aliases: 5
- Exact current routes:
  - /markets
  - /decisions
- Compatibility-only redirects:
  - Daily Brief -> /decisions
  - Settings and Alerts -> /
  - Decision Support -> /decisions
- Backend changed: NO
- API changed: NO
- Nginx changed: NO
- React source components changed: NO
- Existing visual design changed: NO
- Services restarted: NO
- Desktop tests: 6
- Mobile tests: 6
- Screenshot count: 12
- Rollback available: YES

PASS_COUNT=7
WARN_COUNT=1
FAIL_COUNT=0
PATCH_COUNT=8

============================================================
PASS_COUNT=7
WARN_COUNT=1
FAIL_COUNT=0
PATCH_COUNT=8
SCREENSHOT_COUNT=12
LANGUAGE_KEYS=ndsp_lang_final,ndsp_final_lang,ndsp_lang
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256.md
BROWSER_RESULT=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256/browser-results.json
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_EARLY_LANGUAGE_INTERCEPT_V20_20260712_224256
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/early-language-intercept-v20-20260712_224256
FINAL_STATUS=NDSP_EARLY_LANGUAGE_INTERCEPT_V20_PASS_WITH_COMPATIBILITY_REDIRECTS
============================================================
