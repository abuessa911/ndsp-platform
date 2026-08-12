============================================================
NDSP — Final Browser UI Gate V12
DATE=2026-07-12T21:25:37+02:00
PROJECT=/home/nawaf511/empire-core-new
API_BASE=https://api.ndsp.app
PORTAL_BASE=https://my.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
SYMBOL=ETHUSDT
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537
MODE=READ_ONLY
============================================================

## 1) فحص عدم تراجع عقد API

--- API CHECK ---
TIMEFRAME=daily
HTTP=200
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=daily&_ndsp_cb=20260712_212537_daily
[OK] عقد API للفريم daily سليم

--- API CHECK ---
TIMEFRAME=weekly
HTTP=200
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_cb=20260712_212537_weekly
[OK] عقد API للفريم weekly سليم

--- API CHECK ---
TIMEFRAME=monthly
HTTP=200
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=monthly&_ndsp_cb=20260712_212537_monthly
[OK] عقد API للفريم monthly سليم

## 2) تحديد الملف الذي يحتوي الحالة الخام
RAW_STATE_FILE_COUNT=1
RAW_STATE_FILES:
 - /var/www/ndsp-my/data/command-center-real.json

RAW_STATE_MATCHES:
/var/www/ndsp-my/data/command-center-real.json:26:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:114:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:202:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:290:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:378:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:466:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:554:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:642:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:730:      "scenario_state": "UNDER_MONITORING",
/var/www/ndsp-my/data/command-center-real.json:818:      "scenario_state": "UNDER_MONITORING",
[WARN] وجدت حالات خام في الملفات؛ اختبار المتصفح سيحدد هل تظهر للمستخدم

## 3) اكتشاف Playwright وChromium
[OK] تم اكتشاف Playwright: playwright
SYSTEM_BROWSER=/usr/bin/chromium-browser

## 4) فحص صياغة JavaScript قبل التشغيل
[OK] صياغة سكربت المتصفح سليمة

## 5) تشغيل Playwright
[OK] اكتمل تشغيل Playwright

## 6) تحليل نتائج المتصفح

--- BROWSER desktop:home ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/?_ndsp_cb=20260712_212537_desktop_home
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=3070
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=0
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=True
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_home.png

--- BROWSER desktop:asset_weekly ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Asset_View.html?symbol=ETHUSDT&timeframe=weekly&_ndsp_cb=20260712_212537_desktop_asset_weekly
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=853
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=False
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_asset_weekly.png

--- BROWSER desktop:command_center ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Command_Center.html?_ndsp_cb=20260712_212537_desktop_command_center
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=853
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=False
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_command_center.png

--- BROWSER desktop:daily_brief ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Daily_Brief.html?_ndsp_cb=20260712_212537_desktop_daily_brief
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=853
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_daily_brief.png

--- BROWSER desktop:settings_alerts ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Settings_Alerts.html?_ndsp_cb=20260712_212537_desktop_settings_alerts
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=853
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_settings_alerts.png

--- BROWSER desktop:decision_support ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/decision-support.html?_ndsp_cb=20260712_212537_desktop_decision_support
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=853
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=None
MOBILE_MENU_CLICKED=None
MOBILE_NAV_VISIBLE=None
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=desktop_decision_support.png

--- BROWSER mobile:home ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/?_ndsp_cb=20260712_212537_mobile_home
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=2294
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=0
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=True
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_home.png

--- BROWSER mobile:asset_weekly ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Asset_View.html?symbol=ETHUSDT&timeframe=weekly&_ndsp_cb=20260712_212537_mobile_asset_weekly
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=93
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=False
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_asset_weekly.png

--- BROWSER mobile:command_center ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Command_Center.html?_ndsp_cb=20260712_212537_mobile_command_center
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=93
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=True
LANGUAGE_FIRST_CLICK=True
LANGUAGE_SECOND_CLICK=True
LANGUAGE_CHANGED_FIRST=False
LANGUAGE_CHANGED_SECOND=False
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_command_center.png

--- BROWSER mobile:daily_brief ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Daily_Brief.html?_ndsp_cb=20260712_212537_mobile_daily_brief
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=93
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_daily_brief.png

--- BROWSER mobile:settings_alerts ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/NDSP_Settings_Alerts.html?_ndsp_cb=20260712_212537_mobile_settings_alerts
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=93
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_settings_alerts.png

--- BROWSER mobile:decision_support ---
HTTP_STATUS=200
FINAL_URL=https://my.ndsp.app/decision-support.html?_ndsp_cb=20260712_212537_mobile_decision_support
TITLE=NDSP — Nawaf Decision Support Platform
BODY_TEXT_LENGTH=93
BLANK_PAGE=False
NAVIGATION_ERROR=None
CONSOLE_ERROR_COUNT=1
PAGE_ERROR_COUNT=0
FAILED_REQUEST_COUNT=0
BAD_RESPONSE_COUNT=0
VISIBLE_FORBIDDEN_TOKENS=[]
LANGUAGE_TOGGLE_FOUND=False
LANGUAGE_FIRST_CLICK=None
LANGUAGE_SECOND_CLICK=None
LANGUAGE_CHANGED_FIRST=None
LANGUAGE_CHANGED_SECOND=None
MOBILE_MENU_FOUND=True
MOBILE_MENU_CLICKED=True
MOBILE_NAV_VISIBLE=False
HORIZONTAL_OVERFLOW=False
API_RESPONSE_COUNT=0
SCREENSHOT=mobile_decision_support.png

BROWSER_VALIDATION_ERRORS=["desktop:asset_weekly:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Asset_View.html", "desktop:command_center:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Command_Center.html", "desktop:daily_brief:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Daily_Brief.html", "desktop:settings_alerts:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Settings_Alerts.html", "desktop:decision_support:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /decision-support.html", "mobile:asset_weekly:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Asset_View.html", "mobile:command_center:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Command_Center.html", "mobile:daily_brief:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Daily_Brief.html", "mobile:settings_alerts:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /NDSP_Settings_Alerts.html", "mobile:decision_support:CONSOLE_ERRORS:404 Error: User attempted to access non-existent route: /decision-support.html"]
BROWSER_VALIDATION_WARNINGS=["desktop:home:LANGUAGE_SECOND_CLICK_NO_CHANGE", "desktop:asset_weekly:LANGUAGE_FIRST_CLICK_NO_CHANGE", "desktop:asset_weekly:LANGUAGE_SECOND_CLICK_NO_CHANGE", "desktop:asset_weekly:QUALITY_API_NOT_OBSERVED", "desktop:command_center:LANGUAGE_FIRST_CLICK_NO_CHANGE", "desktop:command_center:LANGUAGE_SECOND_CLICK_NO_CHANGE", "mobile:home:LANGUAGE_SECOND_CLICK_NO_CHANGE", "mobile:home:MOBILE_NAV_NOT_DETECTED", "mobile:asset_weekly:LANGUAGE_FIRST_CLICK_NO_CHANGE", "mobile:asset_weekly:LANGUAGE_SECOND_CLICK_NO_CHANGE", "mobile:asset_weekly:MOBILE_NAV_NOT_DETECTED", "mobile:asset_weekly:QUALITY_API_NOT_OBSERVED", "mobile:command_center:LANGUAGE_FIRST_CLICK_NO_CHANGE", "mobile:command_center:LANGUAGE_SECOND_CLICK_NO_CHANGE", "mobile:command_center:MOBILE_NAV_NOT_DETECTED", "mobile:daily_brief:MOBILE_NAV_NOT_DETECTED", "mobile:settings_alerts:MOBILE_NAV_NOT_DETECTED", "mobile:decision_support:MOBILE_NAV_NOT_DETECTED"]
[FAIL] فحص المتصفح كشف أخطاء مانعة

## 7) لقطات الشاشة
desktop_asset_weekly.png
desktop_command_center.png
desktop_daily_brief.png
desktop_decision_support.png
desktop_home.png
desktop_settings_alerts.png
mobile_asset_weekly.png
mobile_command_center.png
mobile_daily_brief.png
mobile_decision_support.png
mobile_home.png
mobile_settings_alerts.png
SCREENSHOT_COUNT=12
[OK] تم إنشاء لقطات الكمبيوتر والجوال كاملة: 12

## 8) ملخص عقد الأسبوعي
{
  "ok": true,
  "public_contract_version": "quality-live-public-v9",
  "instrument": {
    "symbol": "ETHUSDT",
    "market": "CRYPTO",
    "timeframe": "weekly",
    "live_price": 1821.42
  },
  "scenario": {
    "scenario_state": "UNDER_MONITORING",
    "scenario_directional_context": "قراءة أسبوعي · ضغط هابط",
    "scenario_activation_level": "1,721.40",
    "scenario_arrival_level": "1,575.91",
    "scenario_review_zone": "1,944.29",
    "scenario_invalidation_level": "1,994.19",
    "scenario_risk_note": "تبقى القراءة الهابطة تحت المتابعة؛ لا يتفعّل السيناريو إلا بعد كسر مستوى التفعيل 1,721.40، بينما تستدعي العودة فوق منطقة المراجعة 1,944.29 إعادة تقييم القراءة."
  },
  "nmp": {
    "status": "AVAILABLE",
    "value": 1678.12,
    "timeframe": "weekly",
    "source_interval": "1w"
  },
  "golden_status": "inputs_incomplete",
  "golden_alignment": {
    "golden_status": "inputs_incomplete",
    "reason_code": "MISSING_CANONICAL_COT_DIRECTIONS",
    "missing_inputs": [
      "asset_managers_overall",
      "asset_managers_weekly",
      "leveraged_funds_weekly"
    ],
    "decision_authority": false
  },
  "cross_timeframe_state": "SHORT_TERM_BULLISH_WITHIN_SELECTED_BEARISH",
  "cross_timeframe_divergence": true,
  "live_price_bound": true,
  "data_provider": "binance",
  "generated_at": "2026-07-12T19:25:41Z"
}

## 9) كتابة التقرير النهائي

## Final Browser UI Gate Summary

- Project: /home/nawaf511/empire-core-new
- API endpoint: https://api.ndsp.app
- Portal endpoint: https://my.ndsp.app
- Symbol: ETHUSDT
- Public contract: quality-live-public-v9
- API daily checked: YES
- API weekly checked: YES
- API monthly checked: YES
- Desktop pages checked: 6
- Mobile pages checked: 6
- Language button tested twice: YES
- Mobile menu tested: YES
- JavaScript syntax checked: YES
- JavaScript runtime errors checked: YES
- Blank pages checked: YES
- Raw public states checked: YES
- Horizontal overflow checked: YES
- API calls inside browser observed: YES
- Screenshot count: 12
- Browser results: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537/browser-results.json
- Screenshots directory: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537
- Raw state file list: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537/raw-state-files.txt
- Production files modified: NO
- Services restarted: NO
- Nginx modified: NO
- Mode: READ ONLY

PASS_COUNT=7
WARN_COUNT=1
FAIL_COUNT=1

============================================================
PASS_COUNT=7
WARN_COUNT=1
FAIL_COUNT=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537.md
BROWSER_RESULT=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537/browser-results.json
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537
RAW_STATE_FILES=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINAL_BROWSER_UI_GATE_V12_20260712_212537/raw-state-files.txt
FINAL_STATUS=NDSP_FINAL_BROWSER_UI_GATE_V12_FAILED
============================================================
