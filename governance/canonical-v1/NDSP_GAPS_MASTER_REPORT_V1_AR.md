# NDSP — التقرير الرئيسي الكامل للنواقص وخطة توحيد الحوكمة

**المعرّف:** `NDSP-GAPS-MASTER-001`
**الإصدار:** `1.0.0`
**التاريخ:** `2026-07-30`
**الحالة:** `CANONICAL GAP REPORT — READY FOR GOVERNED INSTALLATION`
**النطاق:** المصدر، الخدمات الحية، العقود العامة، واجهة المستخدم، البيانات، الشارت، الحساب، الاشتراكات، التنبيهات، الاختبارات، النسخ والاستعادة، والإطلاق التجاري.

---

## 1. الملخص التنفيذي

منظومة NDSP تملك قلبًا تحليليًا عاملًا وتظهر مخرجات حقيقية من مسار `quality-live`. لكن المشروع غير جاهز بعد للإطلاق التجاري الكامل؛ لأن بعض القدرات الجوهرية ما تزال مفقودة، وبعضها موجود جزئيًا أو غير مربوط بمسار تشغيل مثبت، وبعض واجهات المستخدم تعرض قيمًا ثابتة أو تجريبية بدل عقد حي كامل.

أهم فجوتين مؤكدتين حاليًا:

1. عدم وجود عقد عام صريح للسيناريو الإيجابي والسيناريو السلبي.
2. عدم وجود عقد عام مستقل ومتكامل لجودة البيانات.

كما أن الواجهة الحالية لا تستهلك هذين العقدين، وتعرض قيمة جودة بيانات ثابتة في بعض المواضع، ويظهر «السيناريو البديل» كنص ثابت بدل سيناريو محسوب.

القرار الحاكم لهذا التقرير:

> لا يجوز إزالة الحوكمة السابقة حذفًا نهائيًا قبل جردها، وفحص مراجعها، وأرشفتها، وتثبيت مرجع حوكمة واحد أعلى أولوية. إزالة التداخل تتحقق بإخراج الوثائق السابقة من المسارات الفعّالة ووضعها في أرشيف Superseded قابل للرجوع.

---

## 2. مستوى الثقة في النتائج

| التصنيف | المعنى |
|---|---|
| مؤكد | ثبت من الخدمة الحية أو المصدر أو الاختبار المباشر. |
| جزئي | يوجد كود أو سجل أو واجهة، لكن الربط الحي أو الاكتمال غير مثبت. |
| غير مثبت | لا توجد أدلة كافية للحكم بأنه يعمل في المسار التجاري. |
| قرار تجاري | يحتاج اعتماد المالك ولا يُحسم بالكود وحده. |

---

## 3. سلسلة التشغيل المثبتة

السلسلة التي تم التحقق منها:

```text
واجهة/بوابة مصادقة عامة
        ↓
Port 9001 — ndsp-platform-gateway
        ↓
Port 9082 — NMP quality-live wrapper
        ↓
Port 9057 — canonical live decision-quality engine
        ↓
backend/ndsp-live-decision-quality/server.py
```

الحالة:

- `9001`: يعيد `AUTH_REQUIRED` دون جلسة، وهذا سلوك صحيح للبوابة.
- `9057`: يعيد `HTTP 200` لعقد `quality-live`.
- `9082`: يعيد `HTTP 200` ويحافظ على استجابة المحرك الأساسي مع إضافة سياق NMP.
- المنافذ `9078/9079/9080/9094/19091` ليست معالج `quality-live` الأساسي.

---

## 4. ما هو موجود ويعمل بدرجة جيدة

هذه القدرات لا تُعد نواقص أساسية حاليًا، مع بقاء الحاجة للاختبارات النهائية:

- TDL للاستثماري والمتوسط والطويل.
- TDL للقصير والمضاربي.
- الاتجاه الحاكم.
- قواعد الفريم والزمن.
- بوابة التصحيح.
- مستويات السيناريو: التفعيل، الوصول، المراجعة، الإلغاء.
- NMP.
- الزخم.
- تأكيد البنية والسيولة داخل القلب.
- ضغط الدولار والسياق الكلي.
- المخاطر.
- محامي الشيطان.
- قوة القراءة وجاهزية القرار.
- حالات القرار: `BLOCKED → ALLOWED → ARMED → EXECUTED`.
- API عام يعيد استجابة `quality-live` حية.

ملاحظة: وجود القدرة لا يعفيها من قفل المصدر والاختبار والنسخة والرجوع قبل الإطلاق.

---

# القسم الأول — النواقص الحرجة المؤكدة

## 5. P0-01: عقد السيناريو المزدوج مفقود

**الحالة:** مؤكد
**الأثر:** مرتفع جدًا
**النطاق:** Backend + API + UI + Tests

العقد الحالي يحتوي سيناريو اتجاهيًا واحدًا فقط. لا توجد مخرجات عامة صريحة لكل من:

```text
positive_scenario
negative_scenario
preferred_scenario
conflict_state
```

العقد المطلوب:

```json
{
  "dual_scenario_analysis": {
    "contract_version": "1.0.0",
    "generated_at": "UTC timestamp",
    "preferred_scenario": "positive|negative|balanced|undetermined",
    "conflict_state": "none|minor|material|insufficient_data",
    "positive_scenario": {
      "title": "",
      "state": "",
      "rationale": "",
      "confirmation_conditions": [],
      "invalidation_conditions": [],
      "activation_level": null,
      "target_or_arrival_zone": null,
      "review_zone": null,
      "confidence_band": "",
      "risks": []
    },
    "negative_scenario": {
      "title": "",
      "state": "",
      "rationale": "",
      "confirmation_conditions": [],
      "invalidation_conditions": [],
      "activation_level": null,
      "target_or_arrival_zone": null,
      "review_zone": null,
      "confidence_band": "",
      "risks": []
    },
    "explanatory_notice": "مخرجات تفسيرية وليست أوامر تداول."
  }
}
```

### شروط القبول

- السيناريوهان منفصلان ولا يُنسخ أحدهما من الآخر.
- لا توجد لغة شراء/بيع/دخول/خروج.
- كل سيناريو يملك شروط تأكيد وإلغاء ومخاطر.
- يمر العقد دون فقدان عبر `9057 → 9082 → 9001 → api.ndsp.app`.
- الواجهة تستهلك العقد الحي.
- اختبار Regression يمنع اختفاء الحقول.

---

## 6. P0-02: عقد جودة البيانات العام مفقود

**الحالة:** مؤكد
**الأثر:** مرتفع جدًا
**النطاق:** Data plane + Backend + API + UI

يوجد `decision_quality` وبعض إشارات الجودة الداخلية، لكن لا يوجد عقد عام مستقل يوضح صلاحية البيانات وحدودها.

العقد المطلوب:

```json
{
  "data_quality": {
    "contract_version": "1.0.0",
    "status": "reliable|usable_with_caution|degraded|insufficient",
    "score": null,
    "freshness_status": "fresh|delayed|stale|unknown",
    "generated_at": "UTC timestamp",
    "observed_at": "UTC timestamp",
    "source_report_date": null,
    "source_age_days": null,
    "missing_fields": [],
    "stale_sources": [],
    "provider_checks": {},
    "snapshot_id": null,
    "accepted_snapshot_id": null,
    "warnings": [],
    "limitations": []
  }
}
```

### ممنوع كشفه

- كلمات المرور أو التوكنات.
- مسارات داخلية حساسة.
- معادلات الملكية السرية.
- أسماء طبقات داخلية غير مسموح بها.
- مفاتيح المزوّدين.

### شروط القبول

- القيمة في الواجهة تأتي من API وليست ثابتة.
- حالة freshness واضحة.
- البيانات الناقصة لا تُملأ بقيم مختلقة.
- الحالة `insufficient` تمنع الحكم النهائي عند الحاجة.
- يحفظ العقد عبر جميع الأغلفة والبوابات.

---

## 7. P0-03: الواجهة لا تستهلك العقدين الجديدين

**الحالة:** مؤكد
**الأثر:** مرتفع جدًا

الـNormalizer الحالي يختزل الاستجابة إلى:

```text
instrument
scenario
quality/readiness indicators
blockers
updated_at
```

ولا يحتفظ بعقد سيناريو مزدوج أو كائن جودة بيانات عام.

### المطلوب

- تحديث مصدر الواجهة غير المصغر.
- عدم تعديل `assets/*.min.js` أو حزم Vite المبنية مباشرة.
- تمرير `dual_scenario_analysis` و`data_quality` عبر Adapter واضح.
- دعم حالات Loading/Error/Partial/Stale.
- الحفاظ على Beginner/Professional.

---

## 8. P0-04: السيناريو البديل الحالي نص ثابت

**الحالة:** مؤكد

العرض الحالي للسيناريو البديل لا يعتمد على API؛ بل يعرض فقرة عامة ثابتة.

### المطلوب

- إبقاؤه مغلقًا افتراضيًا.
- عند فتحه يعرض السيناريو المقابل الحقيقي.
- يظهر سبب تفضيل السيناريو الرئيسي.
- يوضح شروط التحول بين السيناريوهين.
- لا يشتت المستخدم المبتدئ.

---

## 9. P0-05: قيمة جودة بيانات ثابتة في الواجهة

**الحالة:** مؤكد

توجد قيمة ثابتة مثل:

```text
88%
```

في بطاقات متعددة.

### المطلوب

- إزالة كل القيم الثابتة في Live Mode.
- في Mock Mode يجب وسم البيانات بأنها تجريبية بوضوح.
- عند غياب الجودة الحية تظهر `غير متاحة` بدل قيمة مختلقة.

---

# القسم الثاني — نواقص البيانات والأسعار والشارت

## 10. P0-06: Feed الشموع الحقيقية غير مثبت

**الحالة:** جزئي/غير مثبت
**الأثر:** مرتفع جدًا

يوجد توليد محلي لشموع المعاينة، لكنه ليس بديلًا عن OHLC حي.

### المطلوب

- مصدر OHLC حقيقي.
- توحيد الرمز والفريم.
- Closed-candle validation.
- حالة المصدر: Live/Delayed/Stale/Unavailable.
- منع fallback صامت إلى بيانات تجريبية.
- Cache policy واضحة.
- اختبارات اختلاف الفريمات.

---

## 11. P0-07: الشارت الاحترافي غير مكتمل تجاريًا

**الحالة:** جزئي

المطلوب في النسخة النهائية:

- Candlestick حقيقي.
- Zoom وPan.
- Crosshair وTooltip.
- Fullscreen.
- OHLC.
- مستويات التفعيل والوصول والمراجعة والإلغاء.
- منطقة NMP.
- Panels زمنية لـ RSI وMACD Histogram وOBV وCCI.
- الانحراف المنتظم والخفي عند توفره.
- ارتفاع متجاوب حسب المقاس.

---

## 12. P1-01: المؤشرات الفنية تظهر كقيم لا كسلاسل زمنية

**الحالة:** جزئي

المطلوب:

- نفس snapshot ونفس timeframe.
- عدم حساب مؤشر من فريم وعرضه على فريم آخر.
- توثيق source timestamp لكل سلسلة.
- منع الاختلاق عند نقص البيانات.

---

## 13. P1-02: الانحراف المنتظم والخفي غير مثبت في العرض

**الحالة:** جزئي

المطلوب:

- مخرج صريح للانحراف.
- نوعه: regular/hidden.
- اتجاهه.
- المؤشر المستخدم.
- نطاق الشموع.
- دليل بصري على الشارت.
- حالة `not_confirmed` بدل نص عام غير مبني على البيانات.

---

# القسم الثالث — قدرات موجودة اسميًا وغير مثبتة في المسار الحي

## 14. P1-03: الأخبار والسرد السوقي

**الحالة:** غير مثبت حيًا

المطلوب:

- مصدر أخبار موثوق.
- تطبيع الكيانات والأصول.
- إزالة التكرار.
- توقيت UTC.
- درجة relevance.
- عدم تغيير TDL مباشرة.
- التأثير فقط عبر السياق/الجاهزية/الحذر.

---

## 15. P1-04: التقويم والأحداث الاقتصادية

**الحالة:** غير مثبت حيًا

المطلوب:

- تقويم اقتصادي حقيقي.
- ربط الحدث بالأصول المتأثرة.
- نافذة قبل/بعد الحدث.
- أثر على المخاطر والجاهزية.
- منع القرارات النهائية عند حدث حرج وفق السياسة.

---

## 16. P1-05: محرك التعارض بين الطبقات

**الحالة:** موجود كفكرة/سجل وغير مثبت حيًا

المطلوب:

- `conflict_state` موحد.
- reason codes.
- فرق بين تعارض مادي وتعارض بسيط.
- أثر واضح على readiness.
- عدم إعادة حساب الطبقات.

---

## 17. P1-06: محاكاة السيناريوهات

**الحالة:** غير مثبت حيًا

المطلوب:

- محاكاة تفسيرية لا توقعات مضمونة.
- مدخلات snapshot ثابتة.
- سيناريوهات قابلة لإعادة الإنتاج.
- فصل simulation عن العقد الحاكم.
- عدم تعديل القرار التاريخي.

---

## 18. P1-07: Provider Reconciliation وData Lineage

**الحالة:** جزئي

المطلوب:

- مقارنة المزوّدين.
- سبب قبول/رفض المصدر.
- snapshot خام وغير قابل للتعديل.
- snapshot مقبول.
- lineage من المدخل إلى القرار.
- trace_id.

---

## 19. P1-08: Evidence Ledger وHistorical Replay

**الحالة:** جزئي/غير مثبت

المطلوب:

- حفظ عقد القرار ومصادره وإصدارات المحركات.
- replay قابل للتكرار.
- عدم تعديل السجل التاريخي.
- outcome evaluation منفصل عن القرار الأصلي.
- calibration لاحقة لا تعيد كتابة الماضي.

---

# القسم الرابع — نواقص وظائف المستخدم

## 20. P0-08: المحفظة ليست Backend تجاريًا كاملًا

**الحالة:** مؤكد جزئيًا

النسخة الحالية تستخدم Local adapter أو `localStorage` في المعاينة.

المطلوب:

- جداول قاعدة بيانات.
- ملكية كل سجل للمستخدم.
- CRUD حقيقي.
- صلاحيات.
- مزامنة الأجهزة.
- سجل تغييرات.
- ربط الأسعار الحية.
- ربط غرفة القرار والتنبيهات.
- Empty/Error/Loading states.

---

## 21. P1-09: Watchlist ليست دائمة بالكامل

المطلوب:

- Backend persistence.
- منع التكرار.
- limits حسب الباقة.
- مزامنة متعددة الأجهزة.
- ربط بالتنبيهات.

---

## 22. P0-09: التنبيهات غير مكتملة تجاريًا

المطلوب:

- حفظ القواعد في قاعدة البيانات.
- Email provider حقيقي.
- Telegram ربط واختبار حقيقي.
- إشعار داخل المنصة.
- Deduplication.
- Retry policy.
- Quiet Hours.
- Timezone.
- Delivery log.
- حالة القناة.
- Entitlements.

---

## 23. P1-10: مركز الدعم تجريبي

المطلوب:

- Ticket ID حقيقي.
- قاعدة بيانات.
- الحالة والأولوية.
- مرفقات عند الحاجة.
- سجل ردود.
- صلاحيات Admin/Owner.

---

## 24. P1-11: الحساب والأمان

المطلوب:

- الجلسات والأجهزة.
- إنهاء جميع الجلسات.
- سجل الدخول.
- 2FA.
- تغيير كلمة المرور.
- تصدير البيانات.
- حذف الحساب.
- سياسات الاحتفاظ والخصوصية.

---

# القسم الخامس — الباقات والفوترة

## 25. P0-10: إنفاذ الباقات Server-side غير مثبت بالكامل

إخفاء الواجهة لا يكفي.

المطلوب:

- Middleware صلاحيات.
- منع الحقول غير المسموحة من API.
- Free/Basic/Professional/Admin/Owner.
- Trial 16 يومًا.
- اختبارات تجاوز الصلاحيات.
- لا CSS-only locking.

---

## 26. P0-11: الاشتراكات والفوترة

المطلوب:

- الخطة الحالية.
- بدء/نهاية التجربة.
- checkout.
- Webhooks موثقة.
- Idempotency.
- التجديد والإلغاء.
- فشل الدفع.
- Grace Period.
- فواتير.
- Audit log.
- عدم كشف أسرار الدفع.

---

## 27. P1-12: قرارات تجارية غير معتمدة نهائيًا

تحتاج قرار المالك:

- أسماء الباقات.
- الأسعار.
- الحدود.
- عدد الأصول والفريمات.
- عدد التنبيهات.
- سياسة ما بعد التجربة.
- مدة حفظ البيانات.

---

# القسم السادس — الواجهة واللغة وإمكانية الوصول

## 28. P0-12: ربط مصدر الواجهة بالإصدار المنشور غير مقفول

المطلوب إثبات:

```text
frontend/user-portal-vite/src
→ package lock
→ build command
→ release directory
→ /portal-next/
→ Nginx route
→ browser artifact hash
```

لا يجوز تعديل الملفات المصغرة مباشرة.

---

## 29. P0-13: الفصل بين Live وMock

المطلوب:

- لا fallback صامت.
- Mock موسوم بوضوح.
- Live لا يختلق قيمة ناقصة.
- حالة المصدر وآخر تحديث.
- API timeout/error/stale.

---

## 30. P1-13: اكتمال العربية والإنجليزية

المطلوب:

- قاموس مركزي.
- لا DOM translation patch.
- لا أحرف إنجليزية غير مقصودة في العربية.
- لا letter-spacing للعربية.
- RTL/LTR صحيح.
- اختبار النصوص الطويلة.

---

## 31. P1-14: Responsive والمقاسات

الاختبارات المطلوبة:

```text
320×568
360×800
390×844
430×932
768×1024
1024×768
1366×768
1440×900
1920×1080
```

مع Zoom: `125% / 150% / 200%`.

---

## 32. P1-15: Accessibility

المطلوب:

- Keyboard navigation.
- Focus visible.
- Focus trap.
- Escape.
- Focus restore.
- ARIA.
- Reduced motion.
- Contrast.
- 200% zoom.
- عدم الاعتماد على اللون وحده.

---

# القسم السابع — قفل المصدر والحوكمة

## 33. P0-14: قفل المصدر للطبقات الـ16 غير مكتمل

لكل طبقة يجب ملء:

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

المسار الذي تم تثبيته جيدًا حتى الآن هو `quality-live`، وليس كل الطبقات.

---

## 34. P0-15: تعدد وثائق الحوكمة وتضارب الأولوية

المشكلة ليست في وجود وثائق كثيرة فقط؛ بل في عدم وجود مرجع واحد أعلى أولوية مع سجل Superseded واضح.

### الحل الحاكم

- تثبيت مجلد واحد:

```text
governance/canonical-v1/
```

- إنشاء مؤشر:

```text
governance/CANONICAL_GOVERNANCE.md
```

- نقل الوثائق السابقة من مساراتها الفعالة إلى:

```text
governance/archive/superseded/<timestamp>/
```

- عدم حذفها نهائيًا قبل نجاح verify وrollback drill.
- منع أي وثيقة أقدم من تجاوز المرجع الجديد.

---

## 35. P1-16: Git worktree والمصادر المهجورة

المطلوب:

- فصل source عن build.
- فصل backup عن project source.
- تعليم deprecated services.
- حذف source maps من الإنتاج.
- عدم اعتماد ملف غير tracked كمصدر حاكم.
- commit واضح لكل إصدار.

---

## 36. P1-17: تكرار الخدمات والأغلفة

لكل خدمة يجب تصنيفها:

```text
CANONICAL
ACTIVE_COMPATIBILITY
DEPRECATED
UNKNOWN_CONSUMER
SAFE_TO_ARCHIVE
SAFE_TO_REMOVE
```

لا حذف قبل consumer scan.

---

# القسم الثامن — النسخ والاستعادة

## 37. P0-16: Restore Drill حديث غير مثبت

وجود أدوات النسخ لا يساوي نجاح الاستعادة.

المطلوب:

```text
Fresh encrypted backup
→ Hash verification
→ Archive inspection
→ Database restore into isolated environment
→ Application file restore
→ Config validation
→ Health tests
→ RTO/RPO recording
→ Rollback proof
```

---

# القسم التاسع — الاختبارات والإطلاق

## 38. P0-17: Regression للعقد الجديد

يجب أن يمنع اختفاء:

```text
dual_scenario_analysis
positive_scenario
negative_scenario
data_quality
```

من:

```text
9057
9082
9001
api.ndsp.app
frontend normalizer
browser rendering
```

---

## 39. P0-18: بوابات الإصدار غير مكتملة

المطلوب PASS لكل:

- Syntax.
- Unit.
- Contract.
- Integration.
- Typecheck.
- Lint.
- Build.
- Playwright Desktop/Mobile.
- Arabic/English.
- Route refresh.
- Back/forward.
- URL/context persistence.
- Session renewal.
- Trial expiry.
- Entitlements.
- API timeout/error/stale.
- Console errors = 0.
- Unexpected failed requests = 0.
- Visual review.
- Backup.
- Rollback.
- Owner approval.

---

# القسم العاشر — ترتيب التنفيذ المعتمد

## 40. المرحلة A — تثبيت الحقيقة والحوكمة

1. تثبيت حزمة الحوكمة الموحّدة.
2. جرد وثائق الحوكمة السابقة.
3. أرشفتها من المسارات الفعالة.
4. تثبيت precedence واحد.
5. تثبيت قفل source لمسار quality-live.
6. Restore Drill حديث.

## 41. المرحلة B — العقود الحرجة

1. Dual-scenario backend contract.
2. Public data-quality contract.
3. Wrapper preservation.
4. Regression tests.
5. Public API verification.

## 42. المرحلة C — الواجهة

1. قفل source→build→release.
2. تحديث normalizer.
3. إزالة 88% الثابتة.
4. ربط السيناريو البديل الحقيقي.
5. حالات Partial/Stale/Error.
6. AR/EN.

## 43. المرحلة D — البيانات والشارت

1. OHLC feed.
2. Indicators time series.
3. Divergence contract.
4. Chart interactions.
5. Source status and freshness.

## 44. المرحلة E — وظائف المستخدم والتجارة

1. Portfolio backend.
2. Watchlist backend.
3. Alerts.
4. Account/security.
5. Entitlements.
6. Billing.

## 45. المرحلة F — الإطلاق

1. Full test matrix.
2. Commercial staging.
3. Backup and rollback.
4. Visual approval.
5. Controlled production cutover.

---

# القسم الحادي عشر — معايير GO / NO-GO

## 46. NO-GO الحالي

الحالة الحالية:

```text
COMMERCIAL_GO_LIVE = NO_GO
```

للأسباب التالية:

- dual scenario مفقود.
- data quality contract مفقود.
- الواجهة لا تستهلكهما.
- قيمة جودة ثابتة.
- OHLC الحقيقي غير مثبت.
- المحفظة والتنبيهات والفوترة غير مكتملة.
- source lock غير كامل.
- restore drill حديث غير مثبت.
- release gates غير مكتملة.

## 47. شروط GO

```text
P0_COUNT = 0
P1 accepted with documented exception only
BACKUP_RESTORE = VERIFIED
CANONICAL_SOURCE = LOCKED
CONTRACT_TESTS = PASS
FRONTEND_LIVE_MODE = NO_FAKE_VALUES
ENTITLEMENTS = SERVER_SIDE
BILLING = VERIFIED
VISUAL_REVIEW = APPROVED
ROLLBACK = VERIFIED
OWNER_APPROVAL = YES
```

---

# القسم الثاني عشر — سياسة إزالة الحوكمة السابقة

## 48. ما الذي يُزال؟

يُزال من المسارات الفعالة فقط:

- ملفات governance القديمة.
- locks القديمة.
- blueprints المستبدلة.
- registries المستبدلة.
- pins القديمة.
- تقارير حوكمة أصبحت مرجعًا تاريخيًا.

## 49. ما الذي لا يُزال؟

لا يُمس:

- كود التشغيل.
- systemd units.
- Nginx.
- قواعد البيانات.
- secrets.
- ملفات runtime.
- الاختبارات النشطة.
- عقود API المستهلكة.
- ملفات backup.

## 50. طريقة الإزالة الآمنة

```text
Inventory
→ Reference scan
→ Backup manifest
→ Move to superseded archive
→ Install canonical governance
→ Verify precedence
→ Run project checks
→ Rollback test
→ Optional hard delete later
```

الحذف النهائي المباشر ممنوع في هذه الحزمة.

---

# القسم الثالث عشر — النتيجة النهائية

هذه الحزمة لا تدّعي أن كل النواقص أُصلحت. وظيفتها:

1. إعطاء سجل واحد كامل ونظيف للنواقص.
2. منع تضارب وثائق الحوكمة.
3. وضع مرجع واحد أعلى أولوية.
4. إخراج الحوكمة السابقة من المسارات الفعالة بطريقة قابلة للرجوع.
5. تحويل المشروع من تراكم وثائق إلى خطة تنفيذ واختبارات قابلة للقياس.

**الحالة النهائية للتقرير:** `APPROVED AS CONSOLIDATED GAP BASELINE`
**الحالة التجارية:** `NO-GO UNTIL P0 CLOSURE`.
