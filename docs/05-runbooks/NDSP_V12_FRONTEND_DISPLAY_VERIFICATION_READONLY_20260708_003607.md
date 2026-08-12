# NDSP V1.2 Frontend Display Verification Read-only
DATE=2026-07-08T00:36:07+02:00
MODE=READ_ONLY_FRONTEND_DISPLAY_VERIFICATION
MODIFICATIONS=None
LIVE=/var/www/ndsp-my

## 1) Public API Scenario Levels Contract
ETHUSDT: API_SCENARIO_LEVELS=OK
{"activation": {"price": 1673.42, "label_ar": "مستوى التفعيل", "label_en": "Activation level", "source": "computed", "raw_value": "1,673.42"}, "arrival": {"price": 1527.36, "label_ar": "مستوى الوصول", "label_en": "Arrival level", "source": "computed", "raw_value": "1,527.36"}, "review": {"price": 1960.54, "label_ar": "مستوى المراجعة", "label_en": "Review level", "source": "computed", "raw_value": "1,960.54"}, "invalidation": {"price": 1947.29, "label_ar": "مستوى الإلغاء", "label_en": "Invalidation level", "source": "computed", "raw_value": "1,947.29"}}
BTCUSDT: API_SCENARIO_LEVELS=OK
{"activation": {"price": 60722.02, "label_ar": "مستوى التفعيل", "label_en": "Activation level", "source": "computed", "raw_value": "60,722.02"}, "arrival": {"price": 56791.96, "label_ar": "مستوى الوصول", "label_en": "Arrival level", "source": "computed", "raw_value": "56,791.96"}, "review": {"price": 69199.1, "label_ar": "مستوى المراجعة", "label_en": "Review level", "source": "computed", "raw_value": "69,199.10"}, "invalidation": {"price": 68090.89, "label_ar": "مستوى الإلغاء", "label_en": "Invalidation level", "source": "computed", "raw_value": "68,090.89"}}
XAUUSD: API_SCENARIO_LEVELS=OK
{"activation": {"price": 3983.84, "label_ar": "مستوى التفعيل", "label_en": "Activation level", "source": "computed", "raw_value": "3,983.84"}, "arrival": {"price": 3819.45, "label_ar": "مستوى الوصول", "label_en": "Arrival level", "source": "computed", "raw_value": "3,819.45"}, "review": {"price": 4455.31, "label_ar": "مستوى المراجعة", "label_en": "Review level", "source": "computed", "raw_value": "4,455.31"}, "invalidation": {"price": 4312.62, "label_ar": "مستوى الإلغاء", "label_en": "Invalidation level", "source": "computed", "raw_value": "4,312.62"}}
USOIL: API_SCENARIO_LEVELS=OK
{"activation": {"price": 64.534, "label_ar": "مستوى التفعيل", "label_en": "Activation level", "source": "computed", "raw_value": "64.534"}, "arrival": {"price": 54.574, "label_ar": "مستوى الوصول", "label_en": "Arrival level", "source": "computed", "raw_value": "54.574"}, "review": {"price": 82.679, "label_ar": "مستوى المراجعة", "label_en": "Review level", "source": "computed", "raw_value": "82.679"}, "invalidation": {"price": 84.454, "label_ar": "مستوى الإلغاء", "label_en": "Invalidation level", "source": "computed", "raw_value": "84.454"}}
API_CONTRACT_STATUS=OK

## 2) Live Frontend Files Search
FRONTEND_MATCH_COUNT=27
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:25:      text.indexOf('"scenario_activation_level"') !== -1 ||
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:161:      '<div class="ndsp-bind-cell-v24"><small>مستوى التفعيل</small><b data-b-activation>--</b></div>'+
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:162:      '<div class="ndsp-bind-cell-v24"><small>مستوى الوصول</small><b data-b-arrival>--</b></div>'+
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:163:      '<div class="ndsp-bind-cell-v24"><small>منطقة المراجعة</small><b data-b-review>--</b></div>'+
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:164:      '<div class="ndsp-bind-cell-v24"><small>مستوى الإلغاء</small><b data-b-invalidation>--</b></div>'+
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:189:      txt("[data-b-activation]",sc.scenario_activation_level); txt("[data-b-arrival]",sc.scenario_arrival_level);
/var/www/ndsp-my/assets/ndsp-radar-safe-clean.js:190:      txt("[data-b-review]",sc.scenario_review_zone); txt("[data-b-invalidation]",sc.scenario_invalidation_level);
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:51:        <div class="ndsp-ds-cell"><small>مستوى التفعيل</small><b data-ds-activation>--</b></div>
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:52:        <div class="ndsp-ds-cell"><small>مستوى الوصول</small><b data-ds-arrival>--</b></div>
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:53:        <div class="ndsp-ds-cell"><small>منطقة المراجعة</small><b data-ds-review>--</b></div>
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:54:        <div class="ndsp-ds-cell"><small>مستوى الإلغاء</small><b data-ds-invalidation>--</b></div>
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:98:        activation: sc.scenario_activation_level || "--",
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:99:        arrival: sc.scenario_arrival_level || "--",
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:100:        review: sc.scenario_review_zone || "--",
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:101:        invalidation: sc.scenario_invalidation_level || "--",
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:112:      set("[data-ds-activation]",data.activation);
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:113:      set("[data-ds-arrival]",data.arrival);
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:114:      set("[data-ds-review]",data.review);
/var/www/ndsp-my/assets/ndsp-decision-support-bind.js:115:      set("[data-ds-invalidation]",data.invalidation);
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:89:          <div class="ndsp-asset-cell"><small>التفعيل</small><b data-av-activation>--</b></div>
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:90:          <div class="ndsp-asset-cell"><small>الوصول</small><b data-av-arrival>--</b></div>
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:91:          <div class="ndsp-asset-cell"><small>المراجعة</small><b data-av-review>--</b></div>
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:92:          <div class="ndsp-asset-cell"><small>الإلغاء</small><b data-av-invalidation>--</b></div>
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:139:      q("[data-av-activation]",card).textContent=fmt(sc.scenario_activation_level);
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:140:      q("[data-av-arrival]",card).textContent=fmt(sc.scenario_arrival_level);
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:141:      q("[data-av-review]",card).textContent=fmt(sc.scenario_review_zone);
/var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js:142:      q("[data-av-invalidation]",card).textContent=fmt(sc.scenario_invalidation_level);

## 3) Public Pages HTTP Check
/decision-support.html HTTP_CODE=200
/NDSP_Asset_View.html HTTP_CODE=200
/NDSP_Command_Center.html HTTP_CODE=200
/NDSP_Daily_Brief.html HTTP_CODE=200
/index.html HTTP_CODE=200

## 4) Frontend Binding Evaluation
HAS_NEW_SCENARIO_LEVELS_CONTRACT_BINDING=0
HAS_OLD_FLAT_SCENARIO_BINDING=1
HAS_AR_LEVEL_LABELS=1
FRONTEND_DISPLAY_BINDING_STATUS=LIKELY_PRESENT

## 5) Runtime Safety
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m9.9%[39m | [1mram usage[22m: [32m10.1%[39m | [1mlo[22m: ⇓ [32m0.012mb/s[39m ⇑ [32m0.012mb/s[39m | [1meth0[22m: ⇓ [32m0.174mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.185mb/s[39m [90m/[39m [1m[33m81.98%[39m[22m |

FINAL_STATUS=V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_20260708_003607.md
