# NDSP Daily Brief Content-only Patch Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None
TARGET_PAGES:
- NDSP_Daily_Brief.html
- daily-brief.html

## Purpose

Prepare a safe content-only improvement plan for the Daily Brief pages.

No patch is applied in this step.

## Governance Boundaries

NDSP is a decision-support platform only.

The Daily Brief page must explain that the brief is a monitoring summary, not a final decision.

It must not imply:

- direct action
- execution
- guaranteed outcome
- financial recommendation
- automated trading behavior

Allowed wording:

- الموجز اليومي
- قراءة السوق
- المتابعة
- جودة القراءة
- حالة السيناريو
- سبب الحذر
- السياق العام
- دعم القرار
- تحت المتابعة
- اكتمال القراءة

## Current Role of Page

NDSP_Daily_Brief.html / daily-brief.html is the user’s daily monitoring summary.

It should answer:

1. What is the daily market context?
2. Which readings are under monitoring?
3. What changed today?
4. What is strong but not complete?
5. What needs caution?
6. What should the user watch next for understanding?
7. Why does a strong reading not equal a complete decision?

## Required Content Improvements

### 1) Header clarification

Arabic:
"الموجز اليومي يعرض ملخصًا للقراءات المهمة تحت المتابعة. قوة القراءة لا تعني اكتمال القرار، بل تساعد على فهم السياق اليومي."

English:
"The Daily Brief summarizes important readings under monitoring. A strong reading does not mean the decision is complete; it helps explain the daily context."

### 2) Daily context explanation

Arabic:
"السياق اليومي يربط حركة الأصل بجودة القراءة وحالة السيناريو وسبب الحذر."

English:
"Daily context connects asset movement with reading quality, scenario state, and caution reason."

### 3) Strong reading explanation

Arabic:
"القراءة القوية تعني أن بعض عناصر التحليل واضحة، لكنها لا تكفي وحدها للحكم على اكتمال القراءة."

English:
"A strong reading means some analysis elements are clear, but it is not enough by itself to confirm completeness."

### 4) Under monitoring explanation

Arabic:
"تحت المتابعة تعني أن القراءة ما زالت تحتاج مراقبة أو تحققًا إضافيًا."

English:
"Under monitoring means the reading still requires observation or additional confirmation."

### 5) Caution explanation

Arabic:
"سبب الحذر يوضح العامل الذي يمنع اعتبار القراءة مكتملة أو ناضجة."

English:
"The caution reason explains what prevents the reading from being considered complete or mature."

### 6) Next focus explanation

Arabic:
"ركّز على جودة القراءة، حالة السيناريو، والسياق العام قبل الانتقال إلى صفحة دعم القرار."

English:
"Focus on reading quality, scenario state, and general context before moving to the Decision Support page."

## Suggested Card Structure

Recommended content cards:

1. الموجز اليومي
2. السياق اليومي
3. جودة القراءة
4. تحت المتابعة
5. سبب الحذر
6. ما الذي تراقبه اليوم
7. تنبيه الحوكمة

## Governance Notice Text

Arabic:
"تنبيه: الموجز اليومي مخصص للفهم والمتابعة. لا يمثل قرارًا مكتملًا ولا توجيهًا لاتخاذ إجراء."

English:
"Notice: the Daily Brief is for understanding and monitoring. It does not represent a completed decision or operational direction."

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

Approve a small content-only patch for NDSP_Daily_Brief.html and daily-brief.html after reviewing this plan.

FINAL_STATUS=DAILY_BRIEF_CONTENT_ONLY_PATCH_PLAN_CREATED
