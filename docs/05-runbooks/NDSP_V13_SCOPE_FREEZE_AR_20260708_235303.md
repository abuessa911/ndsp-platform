# NDSP V1.3 — تجميد النطاق الرسمي

تاريخ التجميد: 20260708_235303  
الوضع: SCOPE_FREEZE  
المرحلة السابقة المعتمدة: P3 Final  
مرجع baseline: docs/05-runbooks/NDSP_V13_PLANNING_BASELINE_AUDIT_READONLY_20260708_234638.md  
مرجع draft: docs/05-runbooks/NDSP_V13_SCOPE_DRAFT_20260708_234638.md  

---

## 1) تعريف V1.3

V1.3 ليست مرحلة إنقاذ وليست مرحلة إصلاح طارئ.  
V1.3 هي مرحلة تحسين منتج مضبوطة مبنية على Runtime نظيف ومغلق بعد P3.

قاعدة المرحلة:

> لا يتم تنفيذ أي كود قبل Backup + Report + Post Patch Test.

---

## 2) حالة baseline المعتمدة

تم اعتماد baseline التالي:

- P3 Final مغلق.
- systemctl --failed = 0.
- Nginx active.
- PM2 active/enabled.
- ndsp-portal online.
- API health = 200.
- quality-live = 200.
- my.ndsp.app = 200.
- admin.ndsp.app = 200.
- port 9001 listening.
- الملفات المحمية تم أخذ SHA256 لها.
- صفحات بوابة المستخدم تم فهرستها.
- ملفات البيانات تم فهرستها.
- حزم الإصدار محفوظة ومفهرسة.

---

## 3) ملاحظة baseline

ظهر في baseline:

- command-center-real.json مملوك root:root.
- GOVENANCE_WORDING_HITS=11.

التصنيف:

- GOVENANCE_WORDING_HITS الحالية لا تُعامل كفشل مباشر لأنها ناتجة غالبًا من كلمات مثل "اتجاه" و أسماء أصول/طاقة داخل data/assets.
- ملف command-center-real.json بملكية root:root يحتاج مراجعة ملكية ضمن Patch مستقل إذا كان يؤثر على تحديث البيانات.

لا يتم تعديلها داخل Scope Freeze.

---

## 4) نطاق V1.3 المعتمد

### 4.1 إكمال تجربة غرفة القرار

مسموح:

- تحسين عناوين الصفحات.
- تحسين شرح حالات القراءة.
- تحسين التنقل داخل الصفحات.
- تحسين حالات التحميل والفارغ والخطأ.
- تحسين الفصل بين Beginner و Advanced.
- توضيح القراءة بدون تغيير منطق القرار.

ممنوع:

- تغيير منطق TDL/NMP/Golden/Risk/Devil.
- إضافة توصيات تداول.
- إضافة Buy/Sell.
- إضافة أوامر تنفيذ.

---

### 4.2 لوحة ثقة البيانات وحداثتها

مسموح:

- عرض ملخص data-quality.json.
- عرض آخر تحديث.
- عرض صحة المصادر.
- إظهار تحذير عند stale data.
- توضيح أن القراءة تعتمد على حداثة البيانات.

ممنوع:

- إخفاء stale data.
- تزوير وقت تحديث.
- عرض ثقة غير مبنية على مصدر.

---

### 4.3 تقوية عارض القرارات المكتملة

مسموح:

- فلترة حسب الأصل.
- فلترة حسب الحالة.
- عرض readiness مقابل strength.
- عرض why_not_completed.
- عرض scenario levels.
- عرض أسباب الحذر أو الاعتراض.

ممنوع:

- أزرار تنفيذ.
- ربط Bot داخل NDSP core.
- تحويل completed decisions إلى أوامر تداول.

---

### 4.4 صفحة أدلة الإصدار للإدارة

مسموح:

- عرض آخر Release Package.
- عرض SHA256.
- عرض آخر Report.
- عرض حالة Reality Lock.
- عرض النظام كقراءة إدارية فقط.

ممنوع:

- تشغيل shell من الواجهة.
- أزرار restart/stop/disable من المتصفح.
- أي تحكم مباشر بالخدمات من UI.

---

### 4.5 تحسين بصري بدون Script Stacking

مسموح:

- CSS-only refinements.
- تحسين ترتيب الكروت والجداول.
- تحسين اللغة العربية والإنجليزية.
- إزالة التكرار البصري.
- توحيد نمط الأزرار والعناوين.

ممنوع:

- استبدال الملفات المحمية:
  - ndsp-radar-safe-clean.js
  - ndsp-global-menu.js
  - ndsp-disclaimer-gate.js
- إضافة سكربتات global جديدة بدون Removal Plan.
- تعديل الرادار بطريقة تكسر القائمة أو الصفحات.

---

## 5) خارج نطاق V1.3

- لا bot integration داخل NDSP core.
- لا enable لـ ndip-api-new.service.
- لا enable لأي legacy service معطلة.
- لا تغيير Nginx إلا Patch مستقل.
- لا reboot إلا Reboot Drill مستقل.
- لا direct trading advice.
- لا Buy/Sell.
- لا Execution Workflow.
- لا تغيير engine logic.
- لا تغيير DB schema بدون Migration Plan مستقل.

---

## 6) ترتيب التنفيذ المعتمد

V1.3 تنفذ على دفعات صغيرة:

1. V13-A: Evidence/Admin Release Page Docs and UI.
2. V13-B: Data Freshness and Trust Panel.
3. V13-C: Decision Room UX Copy Cleanup.
4. V13-D: Completed Decisions Viewer Hardening.
5. V13-E: Visual Polish and Duplicate Cleanup.

كل دفعة يجب أن تحتوي:

- Backup.
- Patch Report.
- Runtime health test.
- Endpoint test.
- Governance wording scan.
- Reality Lock update عند النجاح.

---

## 7) قاعدة الإغلاق

لا يتم إغلاق V1.3 إلا عند وجود:

- V13 final audit.
- systemctl --failed = 0.
- Nginx active.
- PM2 active.
- ndsp-portal online.
- API health 200.
- quality-live 200.
- my/admin 200.
- package + sha256.
- local download + sha256 verification.

