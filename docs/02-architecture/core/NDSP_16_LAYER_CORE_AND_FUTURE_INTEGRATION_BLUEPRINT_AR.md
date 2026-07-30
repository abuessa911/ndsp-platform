# مخطط دمج قلب NDSP المكوّن من 16 طبقة مع الطبقات المستقبلية

**الاسم الرسمي:** NDSP — Nawaf Decision Support Platform
**معرّف الوثيقة:** `NDSP-16-CORE-INTEGRATION-001`
**الإصدار:** `1.0.0`
**تاريخ الاعتماد:** `2026-07-11`
**الحالة:** `GOVERNING BLUEPRINT — لا يجيز تعديل الحسابات قبل قفل المصدر`
**المالك:** Nawaf

---

## 1. الغرض

تحدد هذه الوثيقة موقع الطبقات الـ16 الحالية داخل المعمارية المستقبلية لـNDSP، وتمنع التعامل معها كـ16 خدمة منفصلة أو دمجها حسابيًا بصورة عشوائية.

القاعدة الحاكمة:

> **الـ16 طبقة الحالية هي قلب القرار. الطبقات المستقبلية توضع قبلها لحماية البيانات، وحولها لتنسيق السياق، وبعدها لإثبات القرار وتفسيره وتقييمه.**

---

## 2. ما الذي لا تعنيه الوثيقة؟

- لا تعني إنشاء 56 محرك قرار.
- لا تعني تحويل كل طبقة إلى Microservice.
- لا تعني تعديل معادلات TDL أو NMP أو المخاطر.
- لا تعني أن القائمة الوظيفية تغني عن قفل المصدر الفعلي.
- لا تسمح بحذف أو دمج خدمة قبل إثبات مستهلكيها.
- لا تبدأ طبقة مستقبلية قبل نجاح النسخة والاستعادة وقفل المصدر وإغلاق P0.

---

## 3. السجل الحاكم للطبقات الـ16

المعرفات `NDSP-CORE-L01` إلى `NDSP-CORE-L16` ثابتة. تبقى ثابتة حتى لو تغير الاسم الظاهر أو انتقلت الطبقة بين الخدمات.

| المعرف | الاسم الحاكم | العائلة | الوظيفة | قادرة على المنع |
|---|---|---|---|---|
| NDSP-CORE-L01 | منطق القرار الزمني — المتوسط والطويل | DIRECTION_AND_TIME | تحديد الاتجاه الاستثماري والمتوسط والطويل وفق الفئات الحاكمة وقواعد TDL. | نعم |
| NDSP-CORE-L02 | منطق القرار الزمني — القصير والمضاربي | DIRECTION_AND_TIME | تحديد الاتجاه القصير والمضاربي وحد الاحتفاظ وفق الإغلاق الأسبوعي. | نعم |
| NDSP-CORE-L03 | اتجاه السوق الحاكم | DIRECTION_AND_TIME | توحيد مخرجات الاتجاه في سياق واحد قابل للاستهلاك من بقية الطبقات. | نعم |
| NDSP-CORE-L04 | بوابة التصحيح | DIRECTION_AND_TIME | التحقق من وجود التصحيح الإلزامي قبل السماح بالانتقال إلى حالة ALLOWED. | نعم |
| NDSP-CORE-L05 | محرك الانحراف | DIRECTION_AND_TIME | قياس الانحراف المنتظم والخفي باستخدام مجموعة المؤشرات المعتمدة. | لا |
| NDSP-CORE-L06 | منطق الزمن والأيام | DIRECTION_AND_TIME | تطبيق قواعد Day Logic V2 والفريمات والأفق الزمني. | نعم |
| NDSP-CORE-L07 | مستويات السيناريو | STRUCTURE_AND_SCENARIO | حساب مستويات التفعيل والوصول والمراجعة والإلغاء لكل أصل وفريم. | نعم |
| NDSP-CORE-L08 | نقطة الالتقاء NMP | STRUCTURE_AND_SCENARIO | تحديد منطقة الالتقاء الحرجة والتأكيد المطلوب للتنفيذ الآلي. | نعم |
| NDSP-CORE-L09 | محرك الزخم | CONFIRMATION_AND_CONVERGENCE | قياس قوة الحركة وتناسقها مع اتجاه السيناريو. | لا |
| NDSP-CORE-L10 | تأكيد البنية والسيولة | CONFIRMATION_AND_CONVERGENCE | تقييم البنية والسلوك حول مستويات السيناريو دون إنشاء اتجاه مستقل. | لا |
| NDSP-CORE-L11 | فلتر الدولار والسياق الكلي | RISK_AND_OPPOSITION | إضافة ضغط أو دعم سياقي وفق الدولار والبيئة الكلية دون تغيير TDL مباشرة. | لا |
| NDSP-CORE-L12 | محرك المخاطر | RISK_AND_OPPOSITION | قياس المخاطر السوقية والتشغيلية والزمنية وتخفيض الجاهزية عند الحاجة. | نعم |
| NDSP-CORE-L13 | إشارة نواف الذهبية | CONFIRMATION_AND_CONVERGENCE | تمثيل تقارب محكوم بين الطبقات الأساسية؛ تظهر جزئيًا أو تحت المتابعة وفق الحوكمة. | لا |
| NDSP-CORE-L14 | إشارة نواف الذهبية المعززة | CONFIRMATION_AND_CONVERGENCE | تقارب معزز يتطلب شروطًا إضافية ولا يعد أمر تنفيذ مستقلًا. | لا |
| NDSP-CORE-L15 | محامي الشيطان | RISK_AND_OPPOSITION | اختبار القراءة ضد الاعتراضات والتعارضات بعد المخاطر والسياق الكلي. | نعم |
| NDSP-CORE-L16 | الجاهزية وآلة حالات القرار | READINESS_AND_FINAL_STATE | تجميع المخرجات وتحديد القوة والجاهزية والنضج والحالة النهائية للقرار. | نعم |

> **ملاحظة حوكمة:** الأسماء أعلاه سجل وظيفي حاكم. يجب خلال مرحلة `NDSP_CANONICAL_SOURCE_LOCK` ربط كل طبقة بمسار المصدر الحقيقي، الخدمة، العقد، الإصدار، الاختبارات، وGit commit. لا يجوز استخدام الوثيقة لتغيير الحسابات قبل هذا الربط.

---

## 4. العائلات الخمس

### 4.1 الاتجاه والزمن

تضم `L01–L06` وتجيب عن:

- ما الاتجاه؟
- لأي أفق؟
- ما الفئة الحاكمة؟
- هل التصحيح موجود؟
- هل يوجد انحراف؟
- هل قواعد اليوم والفريم مطبقة؟

هذه العائلة تملك الاتجاه الأساسي. الأخبار لا تغيرها مباشرة.

### 4.2 البنية والسيناريو

تضم `L07–L08` وتجيب عن:

- أين يتفعل السيناريو؟
- أين يصل؟
- متى يراجع؟
- متى يلغى؟
- هل NMP مؤكد؟

### 4.3 التأكيد والتقارب

تضم `L09–L10` و`L13–L14` وتجيب عن:

- هل الزخم والبنية يدعمان القراءة؟
- هل التقارب جزئي أم معزز؟
- هل الإشارة تحت المتابعة؟
- هل جودة القراءة ارتفعت؟

### 4.4 المخاطر والاعتراض

تضم `L11–L12` و`L15`.

الترتيب الإلزامي:

```text
USD / MACRO CONTEXT
        ↓
RISK ENGINE
        ↓
DEVIL'S ADVOCATE
```

### 4.5 الجاهزية والحالة النهائية

تضم `L16` وتجمع المخرجات من دون إعادة حساب الطبقات.

الحالات:

```text
BLOCKED → ALLOWED → ARMED → EXECUTED
```

مع بقاء NDSP منصة دعم قرار، وليس نظام تنفيذ.

---

## 5. موقع الطبقات المستقبلية

### 5.1 قبل القلب — مستوى الحقيقة والبيانات

```text
Asset Master Registry
Source Registry
Market Data Ingestion
Immutable Raw Snapshot Store
Normalization
Data Quality Gate
Provider Reconciliation
Freshness Control
Data Lineage
Economic Calendar Normalization
```

هذه الطبقات لا تنتج قرارًا. وظيفتها ضمان أن مدخلات القلب صحيحة ومعروفة المصدر.

القانون:

```text
NO APPROVED DATA = NO DECISION COMPUTATION
```

### 5.2 حول القلب — مستوى السياق

```text
Economic Event Layer
News & Narrative Intelligence
Macro Context
Cross-Asset Transmission
Market Regime
Liquidity Context
```

قواعد الربط:

- الأخبار لا تغير TDL مباشرة.
- الحدث الاقتصادي يخفض الجاهزية أو يرفع الحذر.
- سياق الدولار يمر إلى `L11`.
- المخاطر تمر إلى `L12`.
- الاعتراضات تمر إلى `L15`.
- التفسير يستفيد من السياق بعد اكتمال العقد.

### 5.3 فوق القلب — مستوى التنسيق والحوكمة

```text
Cross-Layer Conflict Engine
Reading Strength
Decision Readiness
Reading Maturity
Completion Checklist
Decision Governance
```

هذه تقرأ مخرجات الـ16 ولا تعيد احتسابها.

### 5.4 بعد القلب — مستوى الأدلة والتقييم

```text
Decision Evidence Ledger
Historical Replay Lab
Outcome Evaluation
Confidence Calibration
Engine and Model Registry
Audit Trail
```

هذه الطبقات تحفظ وتعيد وتقيّم القرار، ولا تؤثر رجعيًا على الحقيقة التاريخية.

### 5.5 مستوى التفسير والتجربة

```text
Decision Explainability
Beginner View
Professional View
Admin View
Owner View
Arabic / English / French Localization
Reports
Share Cards
Alerts
Watchlists
```

كلها تستهلك عقد قرار نهائي فقط.

### 5.6 مستوى التكامل الخارجي

```text
External Integration Gateway
Partner API
Webhooks
Notification Delivery
Subscription and Entitlements
NDSP Bot
```

المسار الصحيح:

```text
16-Layer Core
→ Decision Governance
→ Completed Decision Contract
→ External Integration Gateway
→ Bot / Partner / Alert
```

---

## 6. ترتيب التنفيذ الحاكم

```text
APPROVED DATA
→ L01 / L02
→ L03
→ L04 / L05 / L06
→ L07
→ L08
→ L09 / L10
→ L11
→ L12
→ L13
→ L14
→ L15
→ L16
→ COMPLETED DECISION CONTRACT
→ EVIDENCE LEDGER
→ EXPLANATION / ALERTS / INTEGRATIONS
```

يُسمح بالتوازي فقط داخل عائلة واحدة عندما تكون المدخلات مستقلة ومثبتة في عقدها.

---

## 7. ما الذي يمكن دمجه؟

### 7.1 دمج العرض

للمستخدم البسيط تظهر خمس بطاقات:

1. الاتجاه.
2. السيناريو.
3. التأكيد.
4. المخاطر.
5. القرار.

لا يعني هذا دمج الطبقات حسابيًا.

### 7.2 دمج التشغيل

يمكن أن تعمل طبقات متعددة داخل Runtime واحد مع بقاء مخرجاتها منفصلة.

```text
One Service ≠ One Layer
One Layer ≠ One Microservice
```

### 7.3 دمج المكتبات المشتركة

يسمح بتوحيد:

- حل الرموز.
- التوقيت والفريمات.
- إغلاق الشموع.
- المؤشرات المشتركة.
- التحقق من العقود.
- السجلات والمراقبة.

ولا يسمح بدمج منطق القرار نفسه من دون اختبار تكافؤ.

---

## 8. متى يسمح بدمج طبقتين حسابيًا؟

فقط بعد:

```text
Freeze contracts
→ Capture baseline outputs
→ Parallel run
→ Historical replay
→ Shadow production
→ Compare
→ Prove equivalence or improvement
→ Owner approval
→ Deprecation window
→ Rollback readiness
```

---

## 9. العقد الموحد لكل طبقة

```json
{
  "layer_id": "NDSP-CORE-L08",
  "canonical_name": "nmp_confirmation",
  "layer_version": "1.4.0",
  "contract_version": "1.0.0",
  "asset_id": "NDSP-CRYPTO-BTC-USD",
  "timeframe": "1W",
  "as_of_utc": "2026-07-11T00:00:00Z",
  "state": "PENDING",
  "value": null,
  "confidence": 0.72,
  "blocking": true,
  "readiness_effect": -18,
  "reason_codes": ["NMP_NOT_CONFIRMED"],
  "source_snapshot_ids": [],
  "engine_commit": "git-commit",
  "trace_id": "trace-id"
}
```

القواعد:

- لا يغيّر أي مستهلك المخرج.
- كل طبقة تعلن نسختها.
- كل سبب يستخدم `reason_code`.
- الوقت UTC.
- الأصل يستخدم `asset_id` موحدًا.
- أي مخرج غير صالح يذهب إلى Quarantine.

---

## 10. عقد تجميع القلب

```json
{
  "decision_id": "ndsp-decision-id",
  "asset_id": "NDSP-CRYPTO-BTC-USD",
  "contract_version": "1.0.0",
  "core_registry_version": "1.0.0",
  "layers": {
    "NDSP-CORE-L01": {},
    "NDSP-CORE-L02": {},
    "NDSP-CORE-L03": {},
    "NDSP-CORE-L04": {},
    "NDSP-CORE-L05": {},
    "NDSP-CORE-L06": {},
    "NDSP-CORE-L07": {},
    "NDSP-CORE-L08": {},
    "NDSP-CORE-L09": {},
    "NDSP-CORE-L10": {},
    "NDSP-CORE-L11": {},
    "NDSP-CORE-L12": {},
    "NDSP-CORE-L13": {},
    "NDSP-CORE-L14": {},
    "NDSP-CORE-L15": {},
    "NDSP-CORE-L16": {}
  },
  "final_state": "ALLOWED",
  "direction": "BULLISH",
  "strength": 74,
  "readiness": 52,
  "maturity": "PARTIAL",
  "conflict_state": "MATERIAL_CONFLICT",
  "completed_at_utc": null
}
```

---

## 11. مصفوفة الرؤية

| الدور | ما يراه |
|---|---|
| Beginner | خمس مجموعات، تفسير مبسط، أسباب الحذر، المستويات، الحالة النهائية |
| Professional | مخرجات الطبقات الـ16 المسموح بها، التعارضات، التأثيرات، نسخ العقد |
| Admin | صحة الخدمات والعقود والبيانات، دون الملكية السرية |
| Owner | السجل الكامل، الأدلة، الإصدارات، Manual Override المصرح |

الأسماء العامة المسموحة تبقى محكومة بسياسة الرؤية.

---

## 12. الربط المطلوب خلال قفل المصدر

لكل طبقة يجب تعبئة:

```text
source_path
runtime_service
runtime_user
port
health_endpoint
input_contract
output_contract
engine_version
git_commit
test_suite
owner
consumers
rollback_version
status
```

ولا تُعتبر الطبقة مثبتة حتى تكتمل هذه الحقول.

---

## 13. بوابات القبول

قبل اعتماد السجل:

- تطابق الطبقات مع الكود.
- عدم وجود طبقتين بالمعنى نفسه.
- عدم وجود خدمة مجهولة.
- عقود JSON قابلة للتحقق.
- اختبار Unit لكل طبقة.
- اختبار Integration لمسار القلب.
- إعادة تاريخية مرجعية.
- اختبار تعارض.
- اختبار حالات BLOCKED وALLOWED وARMED.
- إثبات أن التفسير لا يغير القرار.

---

## 14. حالة الوثيقة والبدء

هذه الوثيقة تحفظ المعمارية المستهدفة، لكنها لا تجيز تعديل الحسابات قبل:

```text
BACKUP_RESTORE = VERIFIED
CANONICAL_SOURCE = LOCKED
P0_RISKS = CLOSED
CURRENT_16_LAYER_REGISTRY = VERIFIED_AGAINST_SOURCE
```

**الحالة النهائية:** `NDSP_16_LAYER_CORE_INTEGRATION_BLUEPRINT_ACTIVE`
