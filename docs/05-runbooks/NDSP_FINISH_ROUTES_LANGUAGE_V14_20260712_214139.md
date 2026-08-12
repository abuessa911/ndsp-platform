============================================================
NDSP — Finish Routes and Language V14
DATE=2026-07-12T21:41:39+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_ROUTES_LANGUAGE_V14_20260712_214139.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_ROUTES_LANGUAGE_V14_20260712_214139
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/routes-language-v14-20260712_214139
============================================================
PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) بوابة API قبل تعديل الواجهة ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 2) اكتشاف روابط الواجهة الحقيقية ==
DISCOVERY_RC=3

DISCOVERY_SUMMARY:
{
  "aliases": {
    "/NDSP_Asset_View.html": "/markets",
    "/NDSP_Command_Center.html": "/decisions"
  },
  "unresolved": [
    "/NDSP_Daily_Brief.html",
    "/NDSP_Settings_Alerts.html",
    "/decision-support.html"
  ]
}

============================================================
[ROLLBACK] تعذر اكتشاف مسار صحيح لكل رابط قديم
============================================================
[ROLLBACK] لا توجد ملفات معدلة.
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_ROUTES_LANGUAGE_V14_20260712_214139.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/routes-language-v14-20260712_214139
FINAL_STATUS=ROLLED_BACK
