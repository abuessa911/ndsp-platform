============================================================
NDSP — Capability Runtime Activation and Governed Layer Exposure V27.2
DATE=2026-07-13T07:35:12+02:00
MODE=TRUTHFUL_RUNTIME_EVIDENCE_NO_FRONTEND_REBUILD
PROJECT=/home/nawaf511/empire-core-new
LIVE=/var/www/ndsp-my
EVIDENCE=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_2_20260713_073505.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_073505
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-2-20260713_073505
============================================================
PRE_API_DAILY_HTTP=200
PRE_API_WEEKLY_HTTP=200
PRE_API_MONTHLY_HTTP=200
PRE_SAME_ORIGIN_HTTP=200
[OK] V26 baseline and public contract verified
[OK] missing personalized-experience capability module installed safely
[OK] capability runtime controller installed
Created symlink /etc/systemd/system/timers.target.wants/ndsp-capability-runtime-controller.timer → /etc/systemd/system/ndsp-capability-runtime-controller.timer.
[OK] all 28 capabilities are installed and functionally verified; live states are evidence-based
WRAPPER_READY_ATTEMPT=2
LOCAL_9082_HTTP=200
[OK] V27 projection binds runtime evidence and governed-redacted layer summaries
[OK] V27 runtime-evidence details added without rebuilding the live bundle
SAME_ORIGIN_V27_HTTP=200
PUBLIC_ASSET=ndsp-capability-activation-v27.js HTTP=200
PUBLIC_ASSET=ndsp-capability-activation-v27.css HTTP=200
[OK] V27 evidence contract and enhancer are publicly reachable
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
        }
      },
      "menu": null,
      "screenshot": "desktop_home.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
        }
      },
      "menu": {
        "found": true,
        "clicked": true,
        "changed": true
      },
      "screenshot": "mobile_home.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
        }
      },
      "menu": null,
      "screenshot": "desktop_home.png"
    },
    {
      "viewport": "desktop",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
        }
      },
      "menu": {
        "found": true,
        "clicked": true,
        "changed": true
      },
      "screenshot": "mobile_home.png"
    },
    {
      "viewport": "mobile",
      "page": "decisions_ar",
      "status": 200,
      "count": 16,
      "expected": 16,
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "ar",
      "expectedLanguage": "ar",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 4,
      "expectedEnhancer": 4,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
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
      "enhancerCount": 28,
      "expectedEnhancer": 28,
      "rootLanguage": "en",
      "expectedLanguage": "en",
      "contract": "ndsp-public-governance-projection-v2",
      "apiError": 0,
      "overflow": false,
      "navigationError": null,
      "pageErrors": [],
      "consoleErrors": [],
      "screenshot": "mobile_governance_en.png"
    }
  ]
}
[OK] browser verified runtime evidence, governed redaction, bilingual display and mobile preservation
FINAL_API_DAILY_HTTP=200
FINAL_API_WEEKLY_HTTP=200
FINAL_API_MONTHLY_HTTP=200
[OK] final API gate passed across daily weekly monthly
[WARN] all capabilities are functionally verified, but only evidence-backed production bindings are labelled live

## V27.2 governance closure

- Capability total: 28
- Installed capabilities: 28
- Functional probes passed: 28
- Operationally ready capabilities: 28
- Live verified capabilities: 1
- Partially live capabilities: 8
- Ready verified, not live-bound: 19
- Governed-redacted decision layers: 4
- Not-exposed decision layers: 0
- Runtime evidence timer: ACTIVE
- Runtime evidence refresh: every 15 minutes
- Frontend rebuild: NO
- Live bundle replaced: NO
- V20 language bridge preserved: YES
- Mobile menu preserved: YES
- Decision authority boundary: ONLY_NDSP_CORE_L01_TO_L16
- Backup: /home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-2-20260713_073505
============================================================
API_LAYER_COUNT=16
API_CAPABILITY_COUNT=28
CAPABILITY_INSTALLED_COUNT=28
CAPABILITY_FUNCTIONAL_PROBE_COUNT=28
CAPABILITY_OPERATIONAL_READY_COUNT=28
CAPABILITY_LIVE_VERIFIED_COUNT=1
CAPABILITY_PARTIALLY_LIVE_COUNT=8
CAPABILITY_READY_VERIFIED_COUNT=19
LAYER_GOVERNED_REDACTED_COUNT=4
LAYER_NOT_EXPOSED_COUNT=0
VISIBLE_LAYER_CARDS=16
VISIBLE_CAPABILITY_CARDS=28
VISIBLE_CAPABILITY_EVIDENCE_PANELS=28
VISIBLE_GOVERNED_REDACTION_NOTICES=4
CAPABILITY_RUNTIME_TIMER=ACTIVE
CAPABILITY_RUNTIME_REFRESH=15_MINUTES
BILINGUAL_DISPLAY=OK
LANGUAGE_FIRST_SECOND_DESKTOP_MOBILE=OK
MOBILE_MENU=OK
SCREENSHOT_COUNT=10
FRONTEND_REBUILD=NO
LIVE_BUNDLE_REPLACED=NO
SAME_ORIGIN_PORTAL_BRIDGE=OK
PASS_COUNT=9
WARN_COUNT=1
FAIL_COUNT=0
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_2_20260713_073505.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_073505
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-2-20260713_073505
FINAL_STATUS=NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_2_PASS_WITH_TRUTHFUL_GRADUAL_LIVE_STATES
============================================================
