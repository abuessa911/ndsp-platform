# NDSP Asset View Content-only Patch Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None
TARGET_PAGES:
- NDSP_Asset_View.html
- asset-selector.html

## Purpose

Prepare a safe content-only improvement plan for the Asset View / Asset Selector pages.

No patch is applied in this step.

## Governance Boundaries

NDSP is a decision-support platform only.

The asset page must explain that selecting an asset loads the decision-support reading context only.

It must not imply:

- direct action
- execution
- guaranteed outcome
- financial recommendation
- automated trading behavior

Allowed wording:

- الأصل
- السوق
- القراءة الحية
- جودة القرار
- حالة السيناريو
- السياق الاتجاهي
- المتابعة
- دعم القرار
- اختيار الأصل
- تحميل القراءة

## Current Role of Page

NDSP_Asset_View.html / asset-selector.html is the user’s market and asset selection point.

It should answer:

1. What market group is the user viewing?
2. What asset is selected?
3. What reading will be loaded after selection?
4. What does live price mean?
5. What does decision quality mean?
6. What does scenario state mean?
7. Why does asset selection not equal a final decision?
8. Where should the user go next?

## Required Content Improvements

### 1) Header clarification

Arabic:
"اختر الأصل لعرض القراءة الحية وسياق دعم القرار. اختيار الأصل لا يعني اكتمال القرار، بل يحدد نطاق القراءة التي سيتم عرضها."

English:
"Select an asset to load the live reading and decision-support context. Asset selection does not mean the decision is complete; it defines the reading scope."

### 2) Market group explanation

Arabic:
"تقسيم الأسواق يساعد على تنظيم القراءة بين العملات، العملات الرقمية، المؤشرات، السلع، المعادن، والطاقة."

English:
"Market grouping helps organize readings across currencies, crypto assets, indices, commodities, metals, and energy."

### 3) Live price explanation

Arabic:
"السعر الحي يستخدم كمرجع لحظة القراءة، ولا يكفي وحده لفهم حالة القرار."

English:
"Live price is used as a reference at the time of reading. It is not enough by itself to understand the decision state."

### 4) Decision quality explanation

Arabic:
"جودة القرار تعكس اكتمال عناصر القراءة المرتبطة بالأصل المختار."

English:
"Decision quality reflects the completeness of the reading elements connected to the selected asset."

### 5) Scenario state explanation

Arabic:
"حالة السيناريو توضّح ما إذا كانت القراءة تحت المتابعة أو تحتاج مراجعة أو وصلت إلى منطقة مهمة."

English:
"Scenario state shows whether the reading is under monitoring, needs review, or has reached an important area."

### 6) Next step explanation

Arabic:
"بعد اختيار الأصل، انتقل إلى صفحة دعم القرار لفهم جودة القراءة وحالة السيناريو والسياق الاتجاهي."

English:
"After selecting an asset, go to the Decision Support page to understand decision quality, scenario state, and directional context."

## Suggested Card Structure

Recommended content cards:

1. اختيار الأصل
2. مجموعة السوق
3. السعر الحي
4. جودة القرار
5. حالة السيناريو
6. الخطوة التالية
7. تنبيه الحوكمة

## Governance Notice Text

Arabic:
"تنبيه: اختيار الأصل يفتح قراءة دعم القرار فقط. لا يمثل ذلك قرارًا مكتملًا أو توجيهًا لاتخاذ إجراء."

English:
"Notice: selecting an asset only opens a decision-support reading. It does not represent a completed decision or operational direction."

## Patch Scope Later

Allowed later:

- HTML text blocks
- static explanatory cards
- minor CSS-only polish if needed
- cache-busting target HTML references if needed

Not allowed later without explicit approval:

- API changes
- PM2 changes
- Nginx changes
- radar JS changes
- menu JS changes
- disclaimer JS changes
- backend runtime changes
- route deletion or rename

## Required Test After Any Future Patch

After any future patch, run:

- required pages HTTP 200
- decision API fields check
- protected UI presence check
- forbidden wording scan
- PM2 runtime check

## Recommendation

Approve a small content-only patch for NDSP_Asset_View.html and asset-selector.html after reviewing this plan.

FINAL_STATUS=ASSET_VIEW_CONTENT_ONLY_PATCH_PLAN_CREATED
