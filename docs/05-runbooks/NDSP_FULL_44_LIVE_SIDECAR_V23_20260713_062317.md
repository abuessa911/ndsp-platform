============================================================
NDSP — Full 16 Layers + 28 Capabilities Live Sidecar V23
DATE=2026-07-13T06:23:21+02:00
MODE=ADDITIVE_NO_FRONTEND_REBUILD
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
WRAPPER=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v23-20260713_062317
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
[OK] pre-change API gate passed
[OK] public governance projection module installed
[OK] public API exposes all 16 layers and 28 capabilities
[OK] live sidecar installed without rebuilding or replacing the current frontend bundle
[OK] compatibility aliases preserved
PUBLIC_ASSET=ndsp-governance-44-v23.js HTTP=200
PUBLIC_ASSET=ndsp-governance-44-v23.css HTTP=200
[OK] sidecar is publicly reachable
{
  "errors": [
    "desktop:language_failed:state",
    "desktop:decisions_ar:count_0_expected_16",
    "desktop:decisions_ar:api_error",
    "desktop:decisions_ar:navigation",
    "desktop:governance_ar:count_0_expected_28",
    "desktop:governance_ar:api_error",
    "desktop:governance_ar:navigation",
    "desktop:decisions_en:count_0_expected_16",
    "desktop:decisions_en:api_error",
    "desktop:decisions_en:navigation",
    "desktop:governance_en:count_0_expected_28",
    "desktop:governance_en:api_error",
    "desktop:governance_en:navigation",
    "mobile:language_failed:state",
    "mobile:decisions_ar:count_0_expected_16",
    "mobile:decisions_ar:api_error",
    "mobile:decisions_ar:navigation",
    "mobile:governance_ar:count_0_expected_28",
    "mobile:governance_ar:api_error",
    "mobile:governance_ar:navigation",
    "mobile:decisions_en:count_0_expected_16",
    "mobile:decisions_en:api_error",
    "mobile:decisions_en:navigation",
    "mobile:governance_en:count_0_expected_28",
    "mobile:governance_en:api_error",
    "mobile:governance_en:navigation"
  ],
  "results": [
    {
      "viewport": "desktop",
      "page": "home",
      "status": 200,
      "language": {
        "first": false,
        "second": true,
        "error": null,
        "initial": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        },
        "firstState": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        },
        "secondState": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        }
      },
      "menu": null,
      "pageErrors": [],
      "screenshot": "desktop_home.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_ar",
      "status": 200,
      "count": 0,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-layer-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:218:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916647271' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "desktop_decisions_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_ar",
      "status": 200,
      "count": 0,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-capability-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:219:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916682959' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "desktop_governance_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_en",
      "status": 200,
      "count": 0,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-layer-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:235:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916719155' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "desktop_decisions_en.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_en",
      "status": 200,
      "count": 0,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-capability-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:236:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916754811' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "desktop_governance_en.png"
    },
    {
      "viewport": "mobile",
      "page": "home",
      "status": 200,
      "language": {
        "first": false,
        "second": true,
        "error": null,
        "initial": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        },
        "firstState": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        },
        "secondState": {
          "values": {
            "ndsp_lang_final": null,
            "ndsp_final_lang": null,
            "ndsp_lang": null
          },
          "lang": "ar",
          "dir": "rtl",
          "v20": true
        }
      },
      "menu": {
        "found": true,
        "clicked": true,
        "changed": true
      },
      "pageErrors": [],
      "screenshot": "mobile_home.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_ar",
      "status": 200,
      "count": 0,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-layer-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:218:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916810674' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "mobile_decisions_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_ar",
      "status": 200,
      "count": 0,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-capability-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:219:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916846238' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "mobile_governance_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_en",
      "status": 200,
      "count": 0,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-layer-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:235:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916881981' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "mobile_decisions_en.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_en",
      "status": 200,
      "count": 0,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 1,
      "notFound": false,
      "overflow": false,
      "navigationError": "page.waitForSelector: Timeout 35000ms exceeded. Call log: \u001b[2m - waiting for locator('[data-ndsp-capability-card]') to be visible\u001b[22m at testRoute (/tmp/tmp.X4Q06T9AvH/verify-v23.js:151:16) at async /tmp/tmp.X4Q06T9AvH/verify-v23.js:236:18",
      "pageErrors": [],
      "consoleErrors": [
        "Access to fetch at 'https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_ui=1783916917537' from origin 'https://my.ndsp.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.",
        "Failed to load resource: net::ERR_FAILED",
        "NDSP44_FETCH_ERROR TypeError: Failed to fetch at render (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:384:28) at boot (https://my.ndsp.app/assets/ndsp-governance-44-v23.js?v=20260713_062317:427:5)"
      ],
      "screenshot": "mobile_governance_en.png"
    }
  ]
}
============================================================
[ROLLBACK] unexpected error line=1314 rc=2
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-governance-44-v23.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-governance-44-v23.css
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-governance-44-v23.js
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-governance-44-v23.css
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v23-20260713_062317
FINAL_STATUS=ROLLED_BACK
============================================================
[ROLLBACK] unexpected error line=1322 rc=2
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-governance-44-v23.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-governance-44-v23.css
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-governance-44-v23.js
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-governance-44-v23.css
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Asset_View.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Command_Center.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Daily_Brief.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/NDSP_Settings_Alerts.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/decision-support.html
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V23_20260713_062317
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-live-sidecar-v23-20260713_062317
FINAL_STATUS=ROLLED_BACK
