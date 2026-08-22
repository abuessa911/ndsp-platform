# NDSP Priority 1 Content Plan

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None

## Purpose

This document defines what should be improved in Priority 1 pages without changing runtime, API, PM2, Nginx, radar JS, menu JS, or disclaimer JS.

## Governance

NDSP is a decision support platform only.

Do not use public wording that implies:

- buy
- sell
- execution
- financial recommendation
- guaranteed profit

Allowed wording:

- reading
- scenario
- monitoring
- decision quality
- directional context
- caution reason
- support decision
- under monitoring

## Priority 1 Pages

### 1) index.html

Purpose:
Main portal entry.

Needed improvement later:
- Clarify that this is the entry point to the decision room.
- Show the five core user paths clearly.
- Avoid heavy text.
- Keep current structure stable.

Suggested content direction:
- "ابدأ من اختيار الأصل، ثم انتقل إلى قراءة القرار، ثم راقب الرادار والموجز اليومي."
- "NDSP لا يصدر أوامر تنفيذ، بل يعرض قراءة سياقية لدعم القرار."

Patch priority:
Low unless landing clarity is weak.

---

### 2) NDSP_Asset_View.html / asset-selector.html

Purpose:
Asset and market selection.

Needed improvement later:
- Clarify market groups.
- Explain that asset choice only loads reading context.
- Add simple explanation of live price, quality, and scenario state.
- Keep both routes.

Suggested content direction:
- "اختر الأصل لعرض القراءة الحية وسياق السيناريو."
- "الأسعار والقراءات مخصصة للفهم والمتابعة وليست أمرًا للتنفيذ."

Patch priority:
High.

---

### 3) decision-support.html / decision-center.html

Purpose:
Main decision reading page.

Needed improvement later:
- Explain decision quality.
- Explain scenario state.
- Explain directional context.
- Explain why NMP may be available or unavailable.
- Improve simple user interpretation.

Suggested content direction:
- "جودة القرار تعكس اكتمال القراءة، ولا تعني الجاهزية للتنفيذ."
- "حالة السيناريو توضّح أين تقع القراءة: مراقبة، وصول، مراجعة، أو إلغاء."
- "NMP يظهر فقط عندما يكون محسوبًا من الخلفية."

Patch priority:
Very High.

---

### 4) NDSP_Command_Center.html / decision-radar.html

Purpose:
Command center and radar.

Needed improvement later:
- Keep radar protected.
- Improve explanation around radar states.
- Clarify that radar is decision support, not a trade signal.
- Avoid touching radar JS.

Suggested content direction:
- "الرادار يعرض حالة القراءة وتوازن المخاطر، ولا يصدر توصية مالية."
- "الألوان تعبّر عن حالة مراقبة ودعم قرار وليست أمرًا مباشرًا."

Patch priority:
High, but visual only and carefully.

---

### 5) NDSP_Daily_Brief.html / daily-brief.html

Purpose:
Daily market brief.

Needed improvement later:
- Explain daily summary.
- Clarify that daily brief is a monitoring view.
- Separate strong readings from ready decisions.
- Add caution language.

Suggested content direction:
- "الموجز اليومي يلخص أهم القراءات تحت المتابعة."
- "القراءة القوية لا تعني اكتمال القرار."

Patch priority:
High.

---

### 6) NDSP_Settings_Alerts.html / settings.html

Purpose:
Settings and monitoring alerts.

Needed improvement later:
- Clarify monitoring alerts vs recommendations.
- Explain alert threshold.
- Explain notification channels if enabled later.
- Do not imply automated trading.

Suggested content direction:
- "التنبيه يعني تغيّرًا في القراءة أو جودة المتابعة، وليس توصية مالية."
- "الإعدادات تتحكم في المراقبة والتنبيه فقط."

Patch priority:
Medium-High.

---

### 7) disclaimer.html

Purpose:
Legal/user acknowledgement.

Needed improvement later:
- Do not modify unless legal wording is explicitly approved.
- Current disclaimer role is valid.

Patch priority:
Locked.

## Recommended Order

1. decision-support.html / decision-center.html
2. NDSP_Asset_View.html / asset-selector.html
3. NDSP_Daily_Brief.html / daily-brief.html
4. NDSP_Command_Center.html / decision-radar.html
5. NDSP_Settings_Alerts.html / settings.html
6. index.html
7. disclaimer.html only if explicitly approved

## Next Safe Step

Create a content-only patch plan for decision-support.html.

Do not patch yet.

FINAL_STATUS=PRIORITY1_CONTENT_PLAN_CREATED
