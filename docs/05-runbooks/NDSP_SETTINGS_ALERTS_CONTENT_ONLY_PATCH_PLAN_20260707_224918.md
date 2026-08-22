# NDSP Settings & Alerts Content-only Patch Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None
TARGET_PAGES:
- NDSP_Settings_Alerts.html
- settings.html

## Purpose

Prepare a safe content-only improvement plan for the Settings & Alerts pages.

No patch is applied in this step.

## Governance Boundaries

NDSP is a decision-support platform only.

The Settings & Alerts page must explain that alerts are monitoring tools, not final decisions.

It must not imply:

- direct action
- guaranteed outcome
- financial recommendation
- automated trading behavior
- operational instruction

Allowed wording:

- الإعدادات
- التنبيهات
- تفضيلات المتابعة
- الأصول المراقبة
- جودة القراءة
- حالة السيناريو
- سبب الحذر
- قناة التنبيه
- حدود التنبيه
- دعم القرار
- المتابعة

## Current Role of Page

NDSP_Settings_Alerts.html / settings.html is the user’s preferences and monitoring configuration page.

It should answer:

1. What can the user configure?
2. What does an alert mean?
3. Which assets can be monitored?
4. What does reading quality alert mean?
5. What does scenario-state alert mean?
6. What does caution reason alert mean?
7. Why does an alert not equal a completed decision?

## Required Content Improvements

### 1) Header clarification

Arabic:
"صفحة الإعدادات والتنبيهات تساعدك على ضبط تفضيلات المتابعة داخل NDSP. التنبيه يعني وجود قراءة تستحق المراجعة، ولا يعني اكتمال القرار."

English:
"The Settings & Alerts page helps configure monitoring preferences inside NDSP. An alert means a reading deserves review; it does not mean the decision is complete."

### 2) Monitoring preferences explanation

Arabic:
"تفضيلات المتابعة تحدد الأصول والقنوات والحالات التي تريد مراقبتها."

English:
"Monitoring preferences define the assets, channels, and states you want to follow."

### 3) Asset watch explanation

Arabic:
"الأصول المراقبة تساعدك على تنظيم القراءات المهمة دون ازدحام."

English:
"Watched assets help organize important readings without clutter."

### 4) Reading quality alert explanation

Arabic:
"تنبيه جودة القراءة يظهر عندما تتغير درجة اكتمال عناصر القراءة."

English:
"A reading-quality alert appears when the completeness of reading elements changes."

### 5) Scenario state alert explanation

Arabic:
"تنبيه حالة السيناريو يساعدك على متابعة انتقال القراءة بين المتابعة والمراجعة والحذر."

English:
"A scenario-state alert helps follow movement between monitoring, review, and caution."

### 6) Caution reason alert explanation

Arabic:
"تنبيه سبب الحذر يوضح العامل الذي يستحق الانتباه داخل القراءة."

English:
"A caution-reason alert highlights the factor that deserves attention inside the reading."

## Suggested Card Structure

Recommended content cards:

1. الإعدادات
2. تفضيلات المتابعة
3. الأصول المراقبة
4. تنبيه جودة القراءة
5. تنبيه حالة السيناريو
6. تنبيه سبب الحذر
7. تنبيه الحوكمة

## Governance Notice Text

Arabic:
"تنبيه: التنبيهات داخل NDSP مخصصة للفهم والمتابعة. ظهور تنبيه لا يعني اكتمال القراءة."

English:
"Notice: alerts inside NDSP are for understanding and monitoring. An alert does not mean the reading is complete."

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

Approve a small content-only patch for NDSP_Settings_Alerts.html and settings.html after reviewing this plan.

FINAL_STATUS=SETTINGS_ALERTS_CONTENT_ONLY_PATCH_PLAN_CREATED
