# NDSP Decision Support Content-only Patch Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None
TARGET_PAGES:
- decision-support.html
- decision-center.html

## Purpose

Prepare a safe content-only improvement plan for the main Decision Support page.

No patch is applied in this step.

## Governance Boundaries

NDSP is a decision support platform only.

This page must not say or imply:

- buy
- sell
- execute
- trading bot
- financial recommendation
- guaranteed profit
- direct entry or exit order

Allowed wording:

- قراءة القرار
- جودة القرار
- حالة السيناريو
- السياق الاتجاهي
- سبب الحذر
- تحت المتابعة
- دعم القرار
- اكتمال القراءة
- الجاهزية ليست مساوية للقوة

## Current Role of Page

decision-support.html / decision-center.html is the main place where the user understands the current reading.

It should answer:

1. What asset is being read?
2. What is the current live price?
3. What is the decision quality?
4. What is the scenario state?
5. What is the directional context?
6. Is NMP available?
7. Why is the reading under monitoring or caution?
8. What should the user understand, without receiving execution instructions?

## Required Content Improvements

### 1) Header clarification

Add or improve a short explanation near the top:

Arabic:
"هذه الصفحة تعرض قراءة دعم القرار للأصل المحدد. القراءة توضّح جودة القرار، حالة السيناريو، والسياق الاتجاهي دون إصدار توصية مالية أو أمر تنفيذ."

English:
"This page shows the decision-support reading for the selected asset. It explains decision quality, scenario state, and directional context without issuing financial advice or execution instructions."

### 2) Decision Quality explanation

Arabic:
"جودة القرار تعكس اكتمال عناصر القراءة. ارتفاع الجودة لا يعني أن القرار جاهز للتنفيذ."

English:
"Decision quality reflects how complete the reading is. A higher quality score does not mean the decision is ready for execution."

### 3) Scenario State explanation

Arabic:
"حالة السيناريو توضّح موقع القراءة الحالي: مراقبة، وصول، مراجعة، أو إلغاء."

English:
"Scenario state shows where the reading currently stands: monitoring, arrival, review, or invalidation."

### 4) Directional Context explanation

Arabic:
"السياق الاتجاهي يصف ميل القراءة العام، لكنه ليس أمر شراء أو بيع."

English:
"Directional context describes the general reading bias, but it is not a buy or sell instruction."

### 5) NMP explanation

Arabic:
"NMP يظهر فقط عندما يتم حسابه من الخلفية. عدم ظهوره لا يعني وجود خطأ؛ قد يعني أن القراءة لم تكتمل مكانيًا."

English:
"NMP appears only when it is calculated by the backend. If it is unavailable, that does not mean there is an error; it may mean the spatial reading is incomplete."

### 6) Caution reason explanation

Arabic:
"سبب الحذر يوضح لماذا لا تزال القراءة بحاجة إلى متابعة أو تحقق إضافي."

English:
"The caution reason explains why the reading still requires monitoring or additional confirmation."

## Suggested Card Structure

Recommended content cards:

1. قراءة الأصل
2. جودة القرار
3. حالة السيناريو
4. السياق الاتجاهي
5. NMP
6. سبب الحذر
7. تنبيه الحوكمة

## Governance Notice Text

Arabic:
"تنبيه: NDSP منصة دعم قرار فقط. لا تعرض أوامر تنفيذ ولا توصيات مالية. استخدم القراءة للفهم والمتابعة."

English:
"Notice: NDSP is a decision-support platform only. It does not provide execution orders or financial advice. Use the reading for understanding and monitoring."

## Patch Scope Later

Allowed later:

- HTML text blocks
- Static explanatory cards
- CSS-only polish if needed
- Cache-busting HTML references if needed

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

Approve a small content-only patch for decision-support.html and decision-center.html after reviewing this plan.

FINAL_STATUS=DECISION_SUPPORT_CONTENT_ONLY_PATCH_PLAN_CREATED
