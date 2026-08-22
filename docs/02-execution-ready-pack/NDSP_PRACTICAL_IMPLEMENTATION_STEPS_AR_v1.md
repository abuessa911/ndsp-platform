# NDSP Practical Implementation Steps
## الخطوات التطبيقية النهائية لإقفال التخطيط وبدء التنفيذ

**المشروع:** NDSP — Nawaf Decision Support Platform  
**الإصدار:** v1.0  
**التاريخ:** 2026-07-06  
**الغرض:** هذه الوثيقة هي آخر ملف قبل الانتقال للأداة الثانية. هدفها إعطاء خطوات تطبيقية مرتبة وواضحة لإدخال الملفات داخل المشروع، تشغيل الفحص، تثبيت الواقع الحالي، أخذ نسخة احتياطية، ثم بدء أول تعديل آمن.

---

# 0. القاعدة الذهبية

لا يبدأ أي تعديل برمجي قبل تنفيذ هذا التسلسل:

```txt
1. إدخال ملفات الحوكمة والكتالوج داخل المشروع.
2. تشغيل Audit.
3. تثبيت المسارات والخدمات الحقيقية.
4. إنشاء V1 Freeze.
5. تشغيل Backup.
6. تنفيذ أول تعديل صغير.
7. تشغيل Post Patch Test.
8. حفظ التقرير.
```

أي أداة تتجاوز هذه الخطوات لا تُعطى صلاحية تعديل المشروع.

---

# 1. تجهيز مجلد العمل

ادخل إلى السيرفر ثم إلى مسار المشروع الرئيسي.

> إذا كان مسار المشروع مختلفاً، عدّل قيمة `PROJECT_DIR` فقط.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"

cd "$PROJECT_DIR"

mkdir -p docs/00-build-catalog
mkdir -p docs/01-build-control-pack
mkdir -p docs/02-execution-ready-pack
mkdir -p docs/03-final-transition
mkdir -p docs/04-legal
mkdir -p docs/05-runbooks

mkdir -p scripts/audit
mkdir -p scripts/backup
mkdir -p scripts/tests
mkdir -p scripts/deploy

echo "OK: NDSP docs/scripts folders prepared inside: $PROJECT_DIR"
```

---

# 2. إدخال الملفات السابقة داخل المشروع

ارفع ملفات ZIP التي تم تجهيزها سابقاً إلى السيرفر، مثلاً إلى:

```txt
/tmp/ndsp-docs/
```

ثم فكها داخل المشروع حسب نوعها.

مثال تطبيقي:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
UPLOAD_DIR="/tmp/ndsp-docs"

cd "$PROJECT_DIR"

mkdir -p "$UPLOAD_DIR"
mkdir -p docs/00-build-catalog docs/01-build-control-pack docs/02-execution-ready-pack docs/03-final-transition
mkdir -p scripts/audit scripts/backup scripts/tests scripts/deploy

# عدّل أسماء الملفات حسب الموجود لديك في /tmp/ndsp-docs
if [ -f "$UPLOAD_DIR/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_SYSTEM_BUILD_AND_READINESS_CATALOG_AR_EN_v1.zip" -d docs/00-build-catalog/
fi

if [ -f "$UPLOAD_DIR/NDSP_BUILD_TOOLS_AND_CONTROL_PACK_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_BUILD_TOOLS_AND_CONTROL_PACK_AR_EN_v1.zip" -d docs/01-build-control-pack/
fi

if [ -f "$UPLOAD_DIR/NDSP_EXECUTION_READY_PACK_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_EXECUTION_READY_PACK_AR_EN_v1.zip" -d docs/02-execution-ready-pack/
fi

if [ -f "$UPLOAD_DIR/NDSP_FINAL_PRE_IMPLEMENTATION_TRANSITION_PLAN_AR_EN_v1.zip" ]; then
  unzip -o "$UPLOAD_DIR/NDSP_FINAL_PRE_IMPLEMENTATION_TRANSITION_PLAN_AR_EN_v1.zip" -d docs/03-final-transition/
fi

echo "OK: NDSP documentation packs imported."
```

---

# 3. استخراج سكربتات الفحص والنسخ والاختبار

بعد فك حزمة `Execution Ready Pack`، انسخ السكربتات إلى مجلد `scripts`.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

find docs/02-execution-ready-pack -type f -name "ndsp_server_and_project_audit_AR.sh" -exec cp -f {} scripts/audit/ \;
find docs/02-execution-ready-pack -type f -name "ndsp_safe_backup_before_patch_AR.sh" -exec cp -f {} scripts/backup/ \;
find docs/02-execution-ready-pack -type f -name "ndsp_post_patch_test_AR.sh" -exec cp -f {} scripts/tests/ \;

chmod +x scripts/audit/*.sh scripts/backup/*.sh scripts/tests/*.sh

echo "OK: audit/backup/test scripts installed."
```

---

# 4. تشغيل Audit لمعرفة الوضع الحقيقي

هذه الخطوة تكشف الوضع الحالي قبل أي تعديل.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$PROJECT_DIR" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/audit/ndsp_server_and_project_audit_AR.sh
```

## مخرجات مطلوبة من Audit
يجب أن تحصل على تقرير فيه:

```txt
- حالة الصفحات.
- حالة API.
- حالة Nginx.
- حالة SSL.
- حالة systemd.
- حالة PM2.
- وجود الرادار.
- وجود القائمة الجانبية.
- وجود إخلاء المسؤولية.
- وجود أي كلمات ممنوعة.
```

---

# 5. إنشاء ملف تثبيت الواقع الحالي

بعد قراءة تقرير Audit، أنشئ ملف:

```txt
docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md
```

استخدم هذا القالب:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_CURRENT_REALITY_LOCK_AR.md <<'EOF'
# NDSP Current Reality Lock — تثبيت الواقع الحالي

## Frontend
FRONTEND_DIR=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app

## Backend
BACKEND_DIR=$HOME/empire-core-new
API_BASE=https://api.ndsp.app

## Official Pages
- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html

## Services
- ndsp-api
- ndip-api-new
- ndsp-next أو خدمة PM2 حسب الواقع

## Decision API
/api/decision/quality-live?symbol=ETHUSDT

## Required Decision Fields
- symbol
- live_price
- decision_quality
- scenario_state
- directional_context
- market_state
- reading_horizon
- horizon_strength
- caution_reason
- sanitized_summary

## Protected UI Elements
- Sidebar
- Radar
- Disclaimer
- Official page links

## Forbidden Output
- Buy Now
- Sell Now
- اشتر الآن
- بيع الآن
- ادخل صفقة
- ربح مضمون
EOF

echo "OK: Current reality lock created."
```

> بعد إنشاء الملف، عدّل القيم حسب تقرير Audit الحقيقي. لا تخمّن.

---

# 6. إنشاء V1 Freeze

هذا الملف يمنع إضافة أفكار جديدة قبل اكتمال النسخة الأولى.

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_V1_FREEZE_AR.md <<'EOF'
# NDSP V1 Freeze — تجميد نطاق النسخة الأولى

## القاعدة
هذه هي نسخة V1. أي شيء خارج النطاق يؤجل حتى تكتمل V1 وتنجح اختبارات القبول.

## داخل V1
- صفحة الهبوط
- التسجيل
- تسجيل الدخول
- تجربة 16 يوم
- إخلاء المسؤولية
- بوابة المستخدم
- صفحة دعم القرار
- صفحة عرض الأصل
- مركز القرار
- يوميات القرار
- الإعدادات والتنبيهات
- API القرار الحي
- السعر الحي
- الرادار
- القائمة الجانبية
- منع Buy/Sell
- إخفاء المحركات السرية

## خارج V1
- بوت تداول
- تنفيذ صفقات
- تطبيق جوال مستقل
- كشف كامل للمحركات
- ربط وسيط تداول
- توصيات مالية مباشرة
- نظام مؤسسي معقد

## ممنوع أثناء V1
- لا تغيير أسماء الصفحات الرسمية.
- لا حذف الرادار.
- لا حذف القائمة الجانبية.
- لا كشف الطبقات السرية.
- لا إضافة أوامر شراء أو بيع.
- لا تعديل الباك إند لإصلاح واجهة إلا عند الحاجة المثبتة.
EOF

echo "OK: V1 freeze created."
```

---

# 7. إنشاء Legal Disclaimer النهائي

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/04-legal/NDSP_LEGAL_DISCLAIMER_MASTER_AR.md <<'EOF'
# NDSP Legal Disclaimer — إخلاء المسؤولية الرسمي

NDSP — Nawaf Decision Support Platform هي منصة دعم قرار وتحليل، وليست منصة توصيات مالية أو أوامر تنفيذ.

باستخدامك للمنصة، تقر بأن:
- المنصة لا تقدم توصيات شراء أو بيع.
- المنصة لا تضمن أرباحاً أو نتائج.
- القراءات المعروضة تحليلية ومساندة فقط.
- البيانات قد تتأخر أو تنقطع أو تختلف حسب المصدر.
- المستخدم مسؤول مسؤولية كاملة عن قراراته المالية والاستثمارية.
- أي قرار مالي يجب أن يتم بناءً على تقدير المستخدم واستشارة مختص مرخص عند الحاجة.
- NDSP لا تتحمل مسؤولية أي خسائر ناتجة عن استخدام القراءات أو إساءة فهمها.

يجب قبول هذا الإخلاء قبل دخول بوابة المستخدم.
EOF

echo "OK: legal disclaimer created."
```

---

# 8. إنشاء Backlog التنفيذ

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

cat > docs/05-runbooks/NDSP_IMPLEMENTATION_TASKS_AR.md <<'EOF'
# NDSP Implementation Tasks — مهام التنفيذ

## TASK-001 — إدخال الوثائق داخل المشروع
الهدف: جعل الوثائق مصدر الحقيقة داخل الريبو.
الاختبار: وجود docs و scripts بالهيكل الصحيح.
Rollback: حذف المجلدات المستحدثة فقط إذا لم تحتوي تعديلات مهمة.

## TASK-002 — تشغيل Audit
الهدف: معرفة الواقع الحالي قبل التعديل.
الاختبار: وجود تقرير Audit.
Rollback: لا يوجد، لأنه فحص فقط.

## TASK-003 — تثبيت المسارات الحقيقية
الهدف: توثيق المسارات والخدمات والدومينات.
الاختبار: ملف Current Reality Lock مكتمل.
Rollback: تعديل الملف بالقيم الصحيحة.

## TASK-004 — إنشاء V1 Freeze
الهدف: منع توسع النطاق.
الاختبار: وجود ملف V1 Freeze.
Rollback: مراجعة الملف وليس حذف الحوكمة.

## TASK-005 — تشغيل Backup قبل أول تعديل
الهدف: حفظ نقطة رجوع.
الاختبار: وجود BACKUP_DIR و REPORT.
Rollback: استخدام النسخة عند فشل التعديل.

## TASK-006 — تثبيت إخلاء المسؤولية
الهدف: منع دخول المستخدم دون قبول الإخلاء.
الاختبار: ظهور الإخلاء قبل البوابة.

## TASK-007 — تثبيت القائمة الجانبية
الهدف: منع اختفاء التنقل.
الاختبار: القائمة موجودة في الصفحات الرسمية.

## TASK-008 — تثبيت الرادار
الهدف: منع اختفاء الرادار عند فشل البيانات.
الاختبار: الرادار موجود أو يظهر fallback واضح.

## TASK-009 — تثبيت API القرار
الهدف: مطابقة حقول JSON مع الواجهة.
الاختبار: curl يرجع الحقول المطلوبة.

## TASK-010 — تثبيت السعر الحي
الهدف: عرض السعر بدون اختفاء عند تعطل المصدر.
الاختبار: LIVE أو STALE أو UNAVAILABLE تظهر بوضوح.

## TASK-011 — منع Buy/Sell
الهدف: حماية المنصة من توصيات تنفيذية.
الاختبار: grep لا يجد أوامر تداول مباشرة.

## TASK-012 — إخفاء المحركات السرية
الهدف: عدم كشف الطبقات المحمية.
الاختبار: لا تظهر أسماء الطبقات السرية في الواجهة.

## TASK-013 — اختبار الجوال
الهدف: ضمان عدم تداخل البطاقات والقائمة والرادار.
الاختبار: فحص يدوي أو Playwright لاحقاً.

## TASK-014 — Post Patch Test
الهدف: اختبار بعد كل تعديل.
الاختبار: سكربت post patch ينجح.

## TASK-015 — نشر V1
الهدف: إطلاق نسخة مستقرة.
الاختبار: الصفحات 200، API يعمل، SSL يعمل، لا أخطاء حرجة.
EOF

echo "OK: implementation tasks created."
```

---

# 9. تشغيل Backup قبل أول تعديل

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
BACKEND_DIR="$PROJECT_DIR" \
scripts/backup/ndsp_safe_backup_before_patch_AR.sh
```

لا تنتقل للتعديل إلا إذا ظهر:

```txt
BACKUP_DIR=...
REPORT=...
```

---

# 10. أول تعديل مسموح بعد الجاهزية

أول تعديل لا يكون كبيراً.  
الأفضل:

```txt
تثبيت إخلاء المسؤولية + التأكد من عدم اختفاء القائمة والرادار.
```

لا تبدأ بربط كبير أو إعادة بناء. ابدأ بتعديل صغير وقابل للاختبار.

---

# 11. تشغيل اختبار ما بعد التعديل

بعد أول تعديل:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="$HOME/empire-core-new"
cd "$PROJECT_DIR"

FRONTEND_DIR="/var/www/ndsp-my" \
FRONTEND_BASE="https://my.ndsp.app" \
API_BASE="https://api.ndsp.app" \
scripts/tests/ndsp_post_patch_test_AR.sh
```

إذا فشل الاختبار:
```txt
1. لا تنشر فوق الفشل.
2. راجع التقرير.
3. أصلح السبب إن كان بسيطاً.
4. أو ارجع للنسخة الاحتياطية.
```

---

# 12. أمر جاهز تعطيه للأداة الثانية

انسخ هذا النص للأداة الثانية:

```txt
أنت تعمل على مشروع NDSP — Nawaf Decision Support Platform.

المطلوب الآن هو تطبيق مرحلة الإقفال وبدء التنفيذ، وليس بناء ميزات جديدة.

نفذ بالترتيب:
1. أنشئ مجلدات docs و scripts حسب الهيكل الرسمي.
2. أدخل حزم الوثائق السابقة داخل docs.
3. انسخ سكربتات audit/backup/test إلى scripts.
4. شغل Audit Script.
5. استخرج القيم الحقيقية من تقرير Audit.
6. أنشئ NDSP_CURRENT_REALITY_LOCK_AR.md.
7. أنشئ NDSP_V1_FREEZE_AR.md.
8. أنشئ NDSP_LEGAL_DISCLAIMER_MASTER_AR.md.
9. أنشئ NDSP_IMPLEMENTATION_TASKS_AR.md.
10. شغل Backup Script.
11. لا تبدأ أي تعديل برمجي قبل نجاح الخطوات السابقة.
12. بعد ذلك ابدأ بأول تعديل صغير: تثبيت إخلاء المسؤولية مع الحفاظ على القائمة والرادار.
13. بعد التعديل شغل Post Patch Test.

ممنوع:
- حذف صفحات.
- تغيير التصميم العام.
- تعديل API بدون سبب.
- كشف محركات سرية.
- إضافة Buy/Sell.
- تنفيذ تعديل كبير قبل Audit وBackup.
- تكديس سكربتات غير موثقة.

المطلوب في النهاية:
- تقرير Audit.
- مسار Backup.
- ملفات Runbook الأربعة.
- نتيجة Post Patch Test إذا تم تنفيذ أول تعديل.
```

---

# 13. نقطة الإغلاق

بعد تنفيذ هذه الوثيقة، نعتبر التخطيط مقفلاً، ونبدأ التطبيق العملي.

الانتقال الصحيح:

```txt
Planning Closed
→ Documentation Installed
→ Audit Done
→ Reality Locked
→ V1 Frozen
→ Backup Ready
→ First Patch
→ Post Patch Test
→ Continue V1 Tasks
```

هذه هي نقطة الانطلاق للأداة الثانية.
