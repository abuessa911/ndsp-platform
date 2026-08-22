============================================================
NDSP — Legacy Routes and Language Final Fix V13
DATE=2026-07-12T21:33:56+02:00
PROJECT=/home/nawaf511/empire-core-new
PORTAL_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_LEGACY_ROUTES_LANGUAGE_FINAL_V13_20260712_213356.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FIX_LEGACY_ROUTES_LANGUAGE_FINAL_V13_20260712_213356
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/legacy-routes-language-v13-20260712_213356
============================================================

PLAYWRIGHT_MODULE=playwright
BROWSER_EXECUTABLE=/usr/bin/chromium-browser

== 1) التأكد من سلامة API ==
API_DAILY_HTTP=200
API_WEEKLY_HTTP=200
API_MONTHLY_HTTP=200
[OK] عقد API العام سليم

== 2) اكتشاف المسارات الصحيحة الموجودة فعليًا ==

============================================================
[ROLLBACK] فشل السكربت عند السطر 930، exit=3
============================================================
[ROLLBACK] لا توجد ملفات مثبتة لاستعادتها.
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_LEGACY_ROUTES_LANGUAGE_FINAL_V13_20260712_213356.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/legacy-routes-language-v13-20260712_213356
FINAL_STATUS=ROLLED_BACK

============================================================
[ROLLBACK] فشل السكربت عند السطر 938، exit=2
============================================================
[ROLLBACK] لا توجد ملفات مثبتة لاستعادتها.
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_LEGACY_ROUTES_LANGUAGE_FINAL_V13_20260712_213356.md
BACKUP_DIR=/home/nawaf511/ndsp_ui_backups/legacy-routes-language-v13-20260712_213356
FINAL_STATUS=ROLLED_BACK
