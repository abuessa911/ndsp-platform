============================================================
NDSP — Full 16 Layers + 28 Capabilities Same-Origin Bridge Live Sidecar V26
DATE=2026-07-13T06:48:28+02:00
MODE=ADDITIVE_NO_FRONTEND_REBUILD_SAME_ORIGIN_BRIDGE
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
WRAPPER=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V26_20260713_064828.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V26_20260713_064828
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-same-origin-sidecar-v26-20260713_064828
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
[OK] pre-change API gate passed
[OK] public governance projection module installed
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
SAME_ORIGIN_BRIDGE_HTTP=200
SAME_ORIGIN_RUNTIME_BRIDGE=OK
[OK] same-origin portal bridge exposes all 16 layers and 28 capabilities
[OK] live sidecar installed without rebuilding or replacing the current frontend bundle
[OK] compatibility aliases preserved
PUBLIC_ASSET=ndsp-governance-44-v26.js HTTP=200
PUBLIC_ASSET=ndsp-governance-44-v26.css HTTP=200
[OK] sidecar is publicly reachable
{
  "errors": [],
  "results": [
    {
      "viewport": "desktop",
      "page": "home",
      "status": 200,
      "language": {
        "first": true,
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
            "ndsp_lang_final": "en",
            "ndsp_final_lang": "en",
            "ndsp_lang": "en"
          },
          "lang": "en",
          "dir": "ltr",
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
        },
        "firstSelector": "scored-visible-control",
        "secondSelector": "scored-visible-control"
      },
      "menu": null,
      "pageErrors": [],
      "screenshot": "desktop_home.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_decisions_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_ar",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_governance_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_en",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_decisions_en.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_en",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_governance_en.png"
    },
    {
      "viewport": "mobile",
      "page": "home",
      "status": 200,
      "language": {
        "first": true,
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
            "ndsp_lang_final": "en",
            "ndsp_final_lang": "en",
            "ndsp_lang": "en"
          },
          "lang": "en",
          "dir": "ltr",
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
        },
        "firstSelector": "scored-visible-control",
        "secondSelector": "scored-visible-control"
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
      "count": 16,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_decisions_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_ar",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_governance_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_en",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_decisions_en.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_en",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_governance_en.png"
    }
  ]
}
{
  "results": [
    {
      "viewport": "desktop",
      "page": "home",
      "status": 200,
      "language": {
        "first": true,
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
            "ndsp_lang_final": "en",
            "ndsp_final_lang": "en",
            "ndsp_lang": "en"
          },
          "lang": "en",
          "dir": "ltr",
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
        },
        "firstSelector": "scored-visible-control",
        "secondSelector": "scored-visible-control"
      },
      "menu": null,
      "pageErrors": [],
      "screenshot": "desktop_home.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_decisions_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_ar",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_governance_ar.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_en",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_decisions_en.png"
    },
    {
      "viewport": "desktop",
      "page": "governance_en",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "desktop_governance_en.png"
    },
    {
      "viewport": "mobile",
      "page": "home",
      "status": 200,
      "language": {
        "first": true,
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
            "ndsp_lang_final": "en",
            "ndsp_final_lang": "en",
            "ndsp_lang": "en"
          },
          "lang": "en",
          "dir": "ltr",
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
        },
        "firstSelector": "scored-visible-control",
        "secondSelector": "scored-visible-control"
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
      "count": 16,
      "expected": 16,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_decisions_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_ar",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "ar",
      "rootLanguage": "ar",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_governance_ar.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_en",
      "status": 200,
      "count": 16,
      "expected": 16,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_decisions_en.png"
    },
    {
      "viewport": "mobile",
      "page": "governance_en",
      "status": 200,
      "count": 28,
      "expected": 28,
      "expectedLanguage": "en",
      "rootLanguage": "en",
      "apiError": 0,
      "notFound": false,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_governance_en.png"
    }
  ]
}
[OK] browser verified 16+28 in Arabic and English while preserving V20 and mobile menu
FINAL_API_DAILY_HTTP=200
FINAL_API_WEEKLY_HTTP=200
FINAL_API_MONTHLY_HTTP=200
[OK] final API gate passed across daily weekly monthly
[WARN] full display is active with truthful non-live and non-exposed states

## Governance closure

- Frontend rebuild: NO
- Current live bundle replaced: NO
- V20 language bridge preserved: YES
- Mobile menu preserved: YES
- Same-origin bridge decision layers: 16
- Same-origin bridge platform capabilities: 28
- Installed capabilities: 27
- Live capabilities: 0
- Layers whose details remain not exposed: 4
- Arabic display verified: YES
- English display verified: YES
- Desktop display verified: YES
- Mobile display verified: YES
- Screenshots: 10
- Decision authority boundary: ONLY_NDSP_CORE_L01_TO_L16
- Rollback manifest: /home/nawaf511/ndsp_integration_backups/full-44-same-origin-sidecar-v26-20260713_064828/manifest.tsv
============================================================
API_LAYER_COUNT=16
API_CAPABILITY_COUNT=28
CAPABILITY_INSTALLED_COUNT=27
CAPABILITY_LIVE_COUNT=0
LAYER_NOT_EXPOSED_COUNT=4
VISIBLE_LAYER_CARDS=16
VISIBLE_CAPABILITY_CARDS=28
BILINGUAL_DISPLAY=OK
LANGUAGE_FIRST_SECOND_DESKTOP_MOBILE=OK
MOBILE_MENU=OK
SCREENSHOT_COUNT=10
FRONTEND_REBUILD=NO
LIVE_BUNDLE_REPLACED=NO
SAME_ORIGIN_PORTAL_BRIDGE=OK
PASS_COUNT=8
WARN_COUNT=1
FAIL_COUNT=0
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FULL_44_LIVE_SIDECAR_V26_20260713_064828.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FULL_44_LIVE_SIDECAR_V26_20260713_064828
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/full-44-same-origin-sidecar-v26-20260713_064828
FINAL_STATUS=NDSP_FULL_44_LIVE_SIDECAR_V26_PASS_WITH_TRUTHFUL_NONLIVE_STATES
============================================================
