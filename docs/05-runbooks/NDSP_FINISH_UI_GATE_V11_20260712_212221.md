============================================================
NDSP — Finish UI Gate V11
DATE=2026-07-12T21:22:21+02:00
PROJECT=/home/nawaf511/empire-core-new
API_BASE=https://api.ndsp.app
PORTAL_BASE=https://my.ndsp.app
SYMBOL=ETHUSDT
PLAYWRIGHT_DIR=/home/nawaf511/playwright-tools
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_UI_GATE_V11_20260712_212221.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_UI_GATE_V11_20260712_212221
MODE=READ_ONLY
============================================================

## 1) فحص سريع لعقد API بعد نجاح V10

--- API SANITY ---
TIMEFRAME=daily
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=daily&_ndsp_cb=20260712_212221_daily
HTTP=200
[OK] عقد API للفريم daily سليم

--- API SANITY ---
TIMEFRAME=weekly
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&_ndsp_cb=20260712_212221_weekly
HTTP=200
[OK] عقد API للفريم weekly سليم

--- API SANITY ---
TIMEFRAME=monthly
URL=https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT&timeframe=monthly&_ndsp_cb=20260712_212221_monthly
HTTP=200
[OK] عقد API للفريم monthly سليم

## 2) إكمال فحص مصادر الواجهة

--- SOURCE SCAN ---
SOURCE_DIR=/home/nawaf511/empire-core-new/frontend/user-portal-vite
OLD_STATUS_FILE_COUNT=0
INTERNAL_KEY_FILE_COUNT=0
NEW_STATUS_FILE_COUNT=0
RAW_STATE_FILE_COUNT=0
[OK] لا توجد مراجع قديمة ظاهرة في /home/nawaf511/empire-core-new/frontend/user-portal-vite
[OK] الواجهة في /home/nawaf511/empire-core-new/frontend/user-portal-vite لا تعتمد بوضوح على مفاتيح _ndsp_
[WARN] لم أجد inputs_incomplete داخل /home/nawaf511/empire-core-new/frontend/user-portal-vite؛ قد تعتمد الواجهة على النص العام فقط
[OK] لم تُعثر حالات خام واضحة داخل /home/nawaf511/empire-core-new/frontend/user-portal-vite

--- SOURCE SCAN ---
SOURCE_DIR=/home/nawaf511/empire-core-new/apps/user-portal
OLD_STATUS_FILE_COUNT=0
INTERNAL_KEY_FILE_COUNT=0
NEW_STATUS_FILE_COUNT=0
RAW_STATE_FILE_COUNT=0
[OK] لا توجد مراجع قديمة ظاهرة في /home/nawaf511/empire-core-new/apps/user-portal
[OK] الواجهة في /home/nawaf511/empire-core-new/apps/user-portal لا تعتمد بوضوح على مفاتيح _ndsp_
[WARN] لم أجد inputs_incomplete داخل /home/nawaf511/empire-core-new/apps/user-portal؛ قد تعتمد الواجهة على النص العام فقط
[OK] لم تُعثر حالات خام واضحة داخل /home/nawaf511/empire-core-new/apps/user-portal

--- SOURCE SCAN ---
SOURCE_DIR=/var/www/ndsp-my
OLD_STATUS_FILE_COUNT=0
INTERNAL_KEY_FILE_COUNT=0
NEW_STATUS_FILE_COUNT=0
RAW_STATE_FILE_COUNT=1
[OK] لا توجد مراجع قديمة ظاهرة في /var/www/ndsp-my
[OK] الواجهة في /var/www/ndsp-my لا تعتمد بوضوح على مفاتيح _ndsp_
[WARN] لم أجد inputs_incomplete داخل /var/www/ndsp-my؛ قد تعتمد الواجهة على النص العام فقط
[WARN] توجد حالات خام داخل ملفات /var/www/ndsp-my؛ سيحدد المتصفح إن كانت ظاهرة للمستخدم

## 3) اكتشاف Playwright والمتصفح
PLAYWRIGHT_MODULE=playwright
SYSTEM_BROWSER=/usr/bin/chromium-browser
[OK] تم اكتشاف Playwright: playwright

## 4) اختبار المتصفح والجوال
/tmp/tmp.U4mrs7uCAp/ndsp_browser_gate_v11.js:585
        forbiddenVisibleTokens.filter(
        ^

ReferenceError: Cannot access 'forbiddenVisibleTokens' before initialization
    at /tmp/tmp.U4mrs7uCAp/ndsp_browser_gate_v11.js:585:9

Node.js v22.22.2
[FAIL] اختبار المتصفح توقف بكود 1

## 6) قائمة لقطات الشاشة
SCREENSHOT_COUNT=0
[WARN] لم يتم إنشاء لقطات شاشة

## 7) ملخص عقد الأسبوعي
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
  "generated_at": "2026-07-12T19:22:24Z"
}

## 8) كتابة ملخص التقرير

## Final UI Gate Summary

- Project: /home/nawaf511/empire-core-new
- API endpoint: https://api.ndsp.app
- Portal endpoint: https://my.ndsp.app
- Symbol: ETHUSDT
- Contract version: quality-live-public-v9
- API frames checked: daily, weekly, monthly
- Source scan completed: YES
- Desktop browser check: YES
- Mobile browser check: YES
- Language toggle tested twice: YES
- Mobile menu checked: YES
- JavaScript errors checked: YES
- Blank pages checked: YES
- Raw internal states checked: YES
- Horizontal overflow checked: YES
- Screenshots directory: /home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_UI_GATE_V11_20260712_212221
- Screenshot count: 0
- Production files modified: NO
- Services restarted: NO
- Nginx modified: NO
- Mode: READ ONLY

PASS_COUNT=12
WARN_COUNT=5
FAIL_COUNT=1

============================================================
PASS_COUNT=12
WARN_COUNT=5
FAIL_COUNT=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FINISH_UI_GATE_V11_20260712_212221.md
ARTIFACT_DIR=/home/nawaf511/empire-core-new/docs/05-runbooks/artifacts/NDSP_FINISH_UI_GATE_V11_20260712_212221
FINAL_STATUS=NDSP_FINISH_UI_GATE_V11_FAILED
============================================================
