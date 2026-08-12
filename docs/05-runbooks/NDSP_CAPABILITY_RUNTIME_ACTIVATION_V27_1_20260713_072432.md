============================================================
NDSP — Capability Runtime Activation and Governed Layer Exposure V27.1
DATE=2026-07-13T07:24:32+02:00
MODE=TRUTHFUL_RUNTIME_EVIDENCE_NO_FRONTEND_REBUILD
PROJECT=/home/nawaf511/empire-core-new
LIVE=/var/www/ndsp-my
EVIDENCE=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_1_20260713_072432.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_072432
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-1-20260713_072432
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
  "errors": [
    "desktop:decisions_en:page_error",
    "desktop:governance_en:page_error",
    "mobile:decisions_en:page_error",
    "mobile:governance_en:page_error"
  ],
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
      "pageErrors": [
        "TypeError: Cannot read properties of null (reading 'setAttribute') at <anonymous>:2:90 at <anonymous>:2:169 at <anonymous>:3:7"
      ],
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
      "pageErrors": [
        "TypeError: Cannot read properties of null (reading 'setAttribute') at <anonymous>:2:90 at <anonymous>:2:169 at <anonymous>:3:7"
      ],
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
      "pageErrors": [
        "TypeError: Cannot read properties of null (reading 'setAttribute') at <anonymous>:2:90 at <anonymous>:2:169 at <anonymous>:3:7"
      ],
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
      "pageErrors": [
        "TypeError: Cannot read properties of null (reading 'setAttribute') at <anonymous>:2:90 at <anonymous>:2:169 at <anonymous>:3:7"
      ],
      "consoleErrors": [],
      "screenshot": "mobile_governance_en.png"
    }
  ]
}
============================================================
[ROLLBACK] unexpected error line=1093 rc=2
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.js
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.timer
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.service
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/platform/runtime/capability_runtime_controller_v1.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/personalization.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/__init__.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_1_20260713_072432.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_072432
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-1-20260713_072432
FINAL_STATUS=ROLLED_BACK
============================================================
[ROLLBACK] unexpected error line=1094 rc=2
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
[ROLLBACK] RESTORED=/var/www/ndsp-my/index.html
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/frontend/user-portal-vite/public/assets/ndsp-capability-activation-v27.js
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.css
[ROLLBACK] REMOVED=/var/www/ndsp-my/assets/ndsp-capability-activation-v27.js
[ROLLBACK] RESTORED=/home/nawaf511/empire-core-new/backend/app/runtime/ndsp_public_governance_projection_v1.py
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.timer
[ROLLBACK] REMOVED=/etc/systemd/system/ndsp-capability-runtime-controller.service
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/var/runtime/NDSP_CAPABILITY_RUNTIME_EVIDENCE_V1.json
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/platform/runtime/capability_runtime_controller_v1.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/personalization.py
[ROLLBACK] REMOVED=/home/nawaf511/empire-core-new/backend/personalization/canonical_v1/__init__.py
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_1_20260713_072432.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_CAPABILITY_RUNTIME_ACTIVATION_V27_20260713_072432
BACKUP_DIR=/home/nawaf511/ndsp_integration_backups/capability-runtime-activation-v27-1-20260713_072432
FINAL_STATUS=ROLLED_BACK
