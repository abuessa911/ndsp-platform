============================================================
NDSP — Finish Routes and Language V15
DATE=2026-07-12T22:04:08+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_ROUTES_LANGUAGE_V15_20260712_220408.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_ROUTES_LANGUAGE_V15_20260712_220408
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/routes-language-v15-20260712_220408
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) خريطة المسارات المعتمدة ==
{
  "version": "15",
  "aliases": {
    "/NDSP_Asset_View.html": "/markets",
    "/NDSP_Command_Center.html": "/decisions",
    "/NDSP_Daily_Brief.html": "/daily-brief.html",
    "/NDSP_Settings_Alerts.html": "/settings",
    "/decision-support.html": "/support-center.html"
  }
}
[OK] تم تثبيت خريطة خمسة مسارات

== 2) بوابة API قبل تعديل الواجهة ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 3) التحقق من المسارات المستهدفة قبل التعديل ==
PRECHECK_RC=3
{
  "results": [
    {
      "legacy": "/NDSP_Asset_View.html",
      "destination": "/markets",
      "status": 200,
      "finalUrl": "https://my.ndsp.app/markets?_ndsp_precheck=20260712_220408",
      "bodyTextLength": 3257,
      "route404": false,
      "visible404": false,
      "navigationError": null,
      "consoleMessages": [],
      "pageErrors": [],
      "valid": true
    },
    {
      "legacy": "/NDSP_Command_Center.html",
      "destination": "/decisions",
      "status": 200,
      "finalUrl": "https://my.ndsp.app/decisions?_ndsp_precheck=20260712_220408",
      "bodyTextLength": 2000,
      "route404": false,
      "visible404": false,
      "navigationError": null,
      "consoleMessages": [],
      "pageErrors": [],
      "valid": true
    },
    {
      "legacy": "/NDSP_Daily_Brief.html",
      "destination": "/daily-brief.html",
      "status": 200,
      "finalUrl": "https://my.ndsp.app/daily-brief.html?_ndsp_precheck=20260712_220408",
      "bodyTextLength": 842,
      "route404": true,
      "visible404": true,
      "navigationError": null,
      "consoleMessages": [
        "404 Error: User attempted to access non-existent route: /daily-brief.html"
      ],
      "pageErrors": [],
      "valid": false
    },
    {
      "legacy": "/NDSP_Settings_Alerts.html",
      "destination": "/settings",
      "status": 200,
      "finalUrl": "https://my.ndsp.app/settings?_ndsp_precheck=20260712_220408",
      "bodyTextLength": 842,
      "route404": true,
      "visible404": true,
      "navigationError": null,
      "consoleMessages": [
        "404 Error: User attempted to access non-existent route: /settings"
      ],
      "pageErrors": [],
      "valid": false
    },
    {
      "legacy": "/decision-support.html",
      "destination": "/support-center.html",
      "status": 200,
      "finalUrl": "https://my.ndsp.app/support-center.html?_ndsp_precheck=20260712_220408",
      "bodyTextLength": 842,
      "route404": true,
      "visible404": true,
      "navigationError": null,
      "consoleMessages": [
        "404 Error: User attempted to access non-existent route: /support-center.html"
      ],
      "pageErrors": [],
      "valid": false
    }
  ]
}

============================================================
[ROLLBACK] أحد المسارات المستهدفة غير صالح
============================================================
[ROLLBACK] لا توجد ملفات معدلة.
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_ROUTES_LANGUAGE_V15_20260712_220408.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/routes-language-v15-20260712_220408
FINAL_STATUS=ROLLED_BACK
