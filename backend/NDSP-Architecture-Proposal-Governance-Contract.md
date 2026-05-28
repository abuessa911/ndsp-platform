وثيقة حوكمة التصورات المعمارية لمنظومة NDSP

الاسم: NDSP Architecture Proposal Governance Contract
الإصدار: V1.0
الغرض: منع أي تصور ناقص أو متضارب قبل اعتماده في منظومة القرار.
النطاق: أي تصور جديد، تعديل طبقة، إضافة محرك، تغيير منطق، تعديل قرار نهائي، أو ربط بين الطبقات.

1) القاعدة الحاكمة

لا يُقبل أي تصور جديد داخل NDSP إلا إذا احتوى إلزاميًا على العناصر الستة التالية:

1) ترتيب الطبقات
2) تقسيم كل طبقة فرعية
3) مصدر كل مخرج
4) صلاحية كل طبقة
5) ماذا يُسمح لها أن تغيّر وماذا لا
6) علاقة Final Decision بكل مصدر

أي تصور لا يحتوي هذه العناصر يُعتبر:

غير مكتمل
غير قابل للتنفيذ
غير قابل للاعتماد
المادة الأولى: ترتيب الطبقات

كل تصور يجب أن يبدأ بتسلسل واضح للطبقات من البداية إلى النهاية.

المطلوب

يجب كتابة التسلسل بهذا الشكل:

1) Layer Name
2) Layer Name
3) Layer Name
...
Final) Final Decision / Output
ممنوع

ممنوع تقديم طبقات متفرقة بدون ترتيب.

مثال مرفوض:

نضيف NMP وTDL والتوقيت والزخم ثم القرار.

سبب الرفض: لا يوضح من يسبق من، ولا أين يتدخل كل محرك.

مثال مقبول
1) Price Source
2) Market Profile
3) Timing Authority
4) COT Source Manager
5) TDL v2 Block
6) Dominant Timed Direction
7) Fundamental Macro Block
8) NMP Block
9) Momentum
10) Divergence
11) Black Layer
12) Decision Quality Stack
13) Risk / Governance
14) Final Decision
15) Scenario / Explainability / Alerts
المادة الثانية: تقسيم كل طبقة فرعية

أي طبقة مركبة يجب تقسيمها إلى طبقات فرعية.

القاعدة

إذا كانت الطبقة تحتوي أكثر من وظيفة واحدة، يجب تقسيمها.

أمثلة إلزامية
TDL v2 Block

لا يجوز كتابتها فقط:

TDL v2

بل يجب كتابتها هكذا:

TDL v2 Block
5.1 L&M Macro Direction Layer
5.2 S Macro Direction Layer
5.3 L&M Weekly Direction Layer
5.4 S Weekly Direction Layer
5.5 Correction State Layer
5.6 Participant Conflict State Layer
Fundamental Macro Block

لا يجوز كتابتها فقط:

Fundamental Macro Layer

بل يجب كتابتها هكذا:

Fundamental Macro Block
7.1 Fed Rate Regime Layer
7.2 USD Strength Layer
7.3 Weighted US News Score Layer
7.4 Asset-Specific Macro Effect Layer
Divergence Block

لا يجوز كتابتها فقط:

Divergence Layer

بل يجب كتابتها هكذا:

Divergence Block
11.1 Regular Divergence Layer
11.2 Hidden Divergence Layer
11.3 Divergence Alignment Layer
المادة الثالثة: مصدر كل مخرج

كل مخرج يجب أن يكون له مصدر واضح.

القاعدة

لا يجوز وجود output بدون source.

الصيغة المطلوبة

كل طبقة يجب أن توضّح:

Inputs:
- المصدر 1
- المصدر 2

Outputs:
- المخرج 1 ← مصدره
- المخرج 2 ← مصدره
مثال
Layer: Dominant Timed Direction

Inputs:
- timing_authority.controller
- tdl.weekly.lm_direction
- tdl.weekly.s_direction

Outputs:
- dominant_timed_direction.direction
  ← if controller=L&M then weekly.lm_direction
  ← if controller=S then weekly.s_direction

- dominant_timed_direction.source
  ← timing_authority.direction_source

- dominant_timed_direction.controller
  ← timing_authority.controller
مرفوض
dominant_timed_direction يعطي الاتجاه النهائي.

سبب الرفض: لا يوضح من أين أتى الاتجاه.

المادة الرابعة: صلاحية كل طبقة

كل طبقة يجب أن يكون لها نطاق صلاحية واضح.

الصلاحيات المعتمدة

كل طبقة يجب أن تصنف تحت واحدة أو أكثر من هذه الصلاحيات:

Data Authority
Direction Authority
Timing Authority
Confidence Authority
Quality Authority
Risk Authority
Execution Authority
Narrative Authority
Governance Authority
مثال
Layer: Timing Authority

Authority:
- Timing Authority

Allowed:
- تحديد controller
- تحديد direction_source
- تحديد day_group

Forbidden:
- لا تحسب direction
- لا تغير confidence
- لا تغير risk
- لا تصدر Final Decision
المادة الخامسة: ماذا يُسمح للطبقة أن تغيّر وماذا لا

كل طبقة يجب أن تحتوي قسمين إلزاميين:

Allowed Effects
Forbidden Effects
مثال صارم
Layer: Momentum Dual

Allowed Effects:
- confidence_effect
- quality_effect
- momentum_context

Forbidden Effects:
- لا تغير decision.direction
- لا تغير dominant_timed_direction.direction
- لا تتجاوز Timing Authority
- لا تصدر أمر تنفيذ
مثال آخر
Layer: Black Layer

Allowed Effects:
- تخفيض confidence
- رفع risk_state
- تحويل decision_state إلى caution أو blocked
- منع قابلية التنفيذ

Forbidden Effects:
- لا تختار direction جديد
- لا تعكس direction
- لا تحذف مخرجات TDL
المادة السادسة: علاقة Final Decision بكل مصدر

هذه أهم مادة في الوثيقة.

القاعدة

Final Decision لا يفكر ولا يستنتج من الصفر.

هو فقط يجمع مخرجات محددة من مصادر محددة.

عقد Final Decision
decision.direction
← dominant_timed_direction.direction

decision.direction_authority
← dominant_timed_direction.decision_authority

decision.direction_source
← dominant_timed_direction.source

decision.timing_controller
← timing_authority.controller

decision.confidence
← decision_quality_stack.final_confidence

decision.confidence_source
← decision_quality_stack

decision.quality_score
← decision_quality_stack.quality_score

decision.grade
← decision_quality_stack.grade

decision.quality_label
← decision_quality_stack.quality_label

decision.risk_state
← risk_state + black_layer.state

decision.decision_state
← governance_runtime + risk_state + black_layer

decision.execution_allowed
← governance.execution_allowed

decision.execution_mode
← governance.execution_mode

decision.scenario_state
← scenario.state
المادة السابعة: قاعدة منع تضارب الاتجاه
القاعدة الذهبية
decision.direction = dominant_timed_direction.direction
مصادر الاتجاه الوحيدة
Timing Authority
+
TDL v2 Weekly Direction
+
Dominant Timed Direction
ممنوع على هذه الطبقات تغيير الاتجاه
Fundamental Macro Block
NMP
NMP-TDL Quality
Momentum Dual
Divergence
Black Layer
Risk
Compliance
Governance
Scenario
Explainability
Alerts

هذه الطبقات تؤثر فقط على:

confidence
quality
risk_state
decision_state
warnings
scenario
alerts
المادة الثامنة: قاعدة فصل الاتجاه عن الثقة
القاعدة

الاتجاه والثقة لا يأتيان من نفس المصدر.

Direction Source:
dominant_timed_direction

Confidence Source:
decision_quality_stack
ممنوع

ممنوع جعل الزخم أو NMP أو الأخبار تغير الاتجاه مباشرة.

مسموح

مسموح لهذه الطبقات أن تؤثر في:

decision_quality_stack.final_confidence
decision_quality_stack.grade
decision_quality_stack.quality_label
المادة التاسعة: Decision Quality Stack إلزامية

أي تصور يحتوي أكثر من طبقة تؤثر على جودة القرار يجب أن يحتوي Decision Quality Stack.

وظيفة هذه الطبقة

تجميع تأثيرات الطبقات في مصدر واحد للثقة والجودة.

Inputs إلزامية
TDL base confidence
Timing authority clarity
COT source quality
Correction state
Participant conflict state
Fed Rate Regime effect
USD Strength effect
Weighted US News effect
Asset-Specific Macro effect
NMP-TDL Quality effect
Momentum Dual effect
Divergence Alignment effect
Black Layer penalty
Risk penalty
Data quality penalty
Session quality penalty
Outputs إلزامية
final_confidence
quality_score
grade
quality_label
confidence_breakdown
ممنوع

ممنوع أن تعدل كل طبقة decision.confidence مباشرة.

القاعدة:

كل طبقة تعطي effect
Decision Quality Stack تجمع effects
Final Decision يأخذ confidence النهائي منها
المادة العاشرة: طبقات الخطر والمنع
مصادر الخطر
Black Layer
Risk State Layer
Market Session State
Data Validity
Governance Runtime
الصلاحية

هذه الطبقات لا تغيّر الاتجاه.

لكن تستطيع تغيير:

decision_state
risk_state
execution_allowed
confidence_penalty
warnings
مثال
direction = bearish
black_layer = danger_block

النتيجة:
direction يبقى bearish كسياق
decision_state = blocked
execution_allowed = false
المادة الحادية عشرة: الحوكمة والتنفيذ
القاعدة

NDSP هو نظام دعم قرار وليس نظام تنفيذ مباشر.

السياسة الثابتة
Decision Active
Execution Sanitized
No Direct Execution
All Layers Participating
Governance مسموح لها
تنظيف المخرجات
منع أوامر التنفيذ المباشر
إخفاء المنطق الحساس
تحديد execution_allowed=false
Governance ممنوع عليها
لا تعطل TDL
لا تعطل Timing
لا تصفر القرار
لا تغير direction
لا تحذف مخرجات الطبقات
المادة الثانية عشرة: قالب قبول أي تصور جديد

أي تصور جديد يجب أن يقدم بهذا القالب فقط:

Layer Name:
Purpose:
Position in Sequence:
Sub-layers:
Inputs:
Outputs:
Output Sources:
Authority:
Allowed Effects:
Forbidden Effects:
Downstream Consumer:
Effect on Final Decision:
Risk if Misused:
Test Requirements:
مثال مختصر
Layer Name:
Divergence Alignment Layer

Purpose:
تحويل regular/hidden divergence إلى تأثير جودة.

Position in Sequence:
داخل Divergence Block بعد Regular و Hidden.

Inputs:
- regular_divergence
- hidden_divergence
- dominant_timed_direction
- nmp_context
- momentum_context

Outputs:
- divergence_alignment.state
- divergence_alignment.confidence_effect
- divergence_alignment.warning

Output Sources:
- state ← مقارنة divergence مع dominant direction
- confidence_effect ← درجة التوافق أو التعارض

Authority:
- Quality Authority

Allowed Effects:
- رفع أو خفض confidence_effect
- إضافة warning

Forbidden Effects:
- لا تغير decision.direction
- لا تتجاوز Timing Authority

Downstream Consumer:
- Decision Quality Stack

Effect on Final Decision:
- يؤثر على confidence فقط عبر quality_stack

Risk if Misused:
- قد يعكس الاتجاه خطأ إذا أعطي صلاحية Direction

Test Requirements:
- اختبار regular ضد الاتجاه
- اختبار hidden مع الاتجاه
- اختبار neutral
المادة الثالثة عشرة: أسباب رفض التصور

يُرفض أي تصور إذا وقع في أحد الأخطاء التالية:

1) لا يحتوي ترتيب طبقات.
2) لا يقسم الطبقات المركبة.
3) لا يذكر مصدر كل output.
4) لا يحدد صلاحية الطبقة.
5) يسمح لأكثر من طبقة بتغيير direction.
6) يجعل Final Decision يستنتج بدل أن يجمع.
7) يجعل كل طبقة تعدل confidence مباشرة.
8) لا يوضح علاقة الطبقة بـ Decision Quality Stack.
9) لا يوضح أثر الطبقة على risk.
10) لا يوضح اختبارات القبول.
المادة الرابعة عشرة: عقد القرار النهائي المختصر

يجب حفظ هذا العقد كمرجع دائم:

Final Decision لا يفكر.
Final Decision يجمع.

Direction:
من Dominant Timed Direction فقط.

Confidence:
من Decision Quality Stack فقط.

Quality / Grade:
من Decision Quality Stack فقط.

Risk:
من Black Layer + Risk State + Data/Session Validity.

Execution:
من Governance فقط.

Scenario:
من Scenario Layer.

Explanation:
من Explainability Layer.

Alerts:
من Alerts Layer.
المادة الخامسة عشرة: النص الحاكم للمشروع

أي تعديل مستقبلي يجب أن يمر بهذا السؤال:

هل هذا التعديل يغير الاتجاه؟

إذا كانت الإجابة نعم، فلا يسمح به إلا إذا كان داخل:

Timing Authority
TDL v2 Weekly Direction
Dominant Timed Direction

أما إذا كان خارجها، فيجب تحويله إلى:

confidence_effect
quality_effect
risk_effect
warning
scenario_context
الخلاصة التنفيذية

من الآن، أي تصور جديد داخل NDSP يجب أن يكون:

مرتّب
مقسّم
مصدري
محدد الصلاحية
محدد التأثير
مرتبط بعقد Final Decision
قابل للاختبار

وهذه هي القاعدة النهائية:

لا اتجاه بدون Timing + TDL.
لا ثقة بدون Decision Quality Stack.
لا منع بدون Risk/Black/Governance.
لا شرح بدون Scenario/Explainability.
لا تنفيذ مباشر أبدًا.

هذه الوثيقة هي المرجع الذي نلتزم به قبل أي كود أو تعديل جديد.
