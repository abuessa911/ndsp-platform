# NDSP Command Center Content-only Patch Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None
TARGET_PAGES:
- NDSP_Command_Center.html
- decision-radar.html

## Purpose

Prepare a safe content-only improvement plan for the Command Center and Decision Radar pages.

No patch is applied in this step.

## Governance Boundaries

NDSP is a decision-support platform only.

The Command Center page must explain the radar as a monitoring and risk-context view.

It must not imply:

- direct action
- guaranteed outcome
- financial recommendation
- automated trading behavior
- operational direction

Allowed wording:

- مركز القيادة
- رادار القرار
- حالة القراءة
- توازن المخاطر
- جودة القراءة
- حالة السيناريو
- سبب الحذر
- تحت المتابعة
- دعم القرار
- مراقبة
- قراءة مكتملة / غير مكتملة

## Protected Components

The following must not be modified without explicit approval:

- Radar JS
- Radar safe-clean asset
- Menu JS
- Disclaimer JS
- API gateway
- PM2 runtime
- Nginx
- Backend runtime

## Current Role of Page

NDSP_Command_Center.html / decision-radar.html is the user’s high-level monitoring room.

It should answer:

1. What is the current radar state?
2. What does the radar summarize?
3. What does green/yellow/red mean?
4. What is decision quality?
5. What is risk context?
6. Why can a reading be strong but still need caution?
7. What should the user observe next for understanding?

## Required Content Improvements

### 1) Header clarification

Arabic:
"مركز القيادة يعرض حالة القراءة العامة وتوازن المخاطر عبر الرادار. الرادار يساعد على الفهم والمتابعة ولا يمثل قرارًا مكتملًا بذاته."

English:
"The Command Center shows the general reading state and risk balance through the radar. The radar supports understanding and monitoring and does not represent a completed decision by itself."

### 2) Radar explanation

Arabic:
"الرادار يلخص حالة القراءة، جودة القرار، وحالة المخاطر بشكل بصري."

English:
"The radar summarizes reading state, decision quality, and risk context visually."

### 3) Color legend explanation

Arabic:
"الألوان تعبّر عن حالة المتابعة: أخضر للقراءة المسموحة، أصفر للحذر، وأحمر للمنع أو عدم الاكتمال."

English:
"Colors represent monitoring status: green for allowed reading, yellow for caution, and red for blocked or incomplete state."

### 4) Risk context explanation

Arabic:
"سياق المخاطر يوضح لماذا قد تحتاج القراءة إلى انتظار أو تحقق إضافي."

English:
"Risk context explains why the reading may require waiting or additional confirmation."

### 5) Strong vs complete explanation

Arabic:
"قوة القراءة لا تعني اكتمالها. قد تكون بعض العناصر قوية بينما تبقى عناصر أخرى تحت المتابعة."

English:
"Reading strength does not mean completeness. Some elements may be strong while others remain under monitoring."

### 6) Governance notice

Arabic:
"تنبيه: مركز القيادة مخصص للفهم والمتابعة ضمن إطار دعم القرار فقط."

English:
"Notice: the Command Center is for understanding and monitoring within the decision-support framework only."

## Suggested Card Structure

Recommended content cards:

1. مركز القيادة
2. رادار القرار
3. دلالة الألوان
4. توازن المخاطر
5. قوة القراءة مقابل اكتمالها
6. ما الذي تراقبه الآن
7. تنبيه الحوكمة

## Patch Scope Later

Allowed later:

- HTML text blocks
- static explanatory cards
- CSS-only polish if needed
- cache-busting target HTML references if needed

Not allowed later without explicit approval:

- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- API changes
- PM2 changes
- Nginx changes
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

Approve a small content-only patch for NDSP_Command_Center.html and decision-radar.html only after reviewing this plan.

FINAL_STATUS=COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_CREATED
