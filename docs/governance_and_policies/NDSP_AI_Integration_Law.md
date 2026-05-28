# قانون الدمج بين أدوات الذكاء — NDSP AI Integration Law
## Official Multi-AI Governance & Path Standard
### Classification: INTERNAL GOVERNANCE CONTRACT
### Scope: ALL AI TOOLS / AGENTS / SCRIPT GENERATORS
### System: NDSP — Multi-Layer Decision Support SaaS

---

# 1) قانون الدمج بين أدوات الذكاء

أي أداة ذكاء اصطناعي خارجية أو داخلية تقوم بـ:

- إنشاء سكربتات
- تعديل ملفات
- توليد اختبارات
- إنشاء تقارير
- بناء طبقات
- تعديل الحوكمة
- تعديل الـ API
- تعديل الـ Runtime
- تعديل الـ User Portal
- تعديل الـ Admin Console
- إنشاء اختبارات E2E
- إنشاء ملفات Governance
- إنشاء ملفات مراقبة أو Logs

يجب أن تلتزم بالكامل بالمسارات الرسمية الخاصة بمنظومة NDSP.

---

# 2) Official NDSP Paths Standard

## المسارات الرسمية المعتمدة

```text
OFFICIAL_ROOT=/home/nawaf511/empire-core-new

OFFICIAL_BACKEND=/home/nawaf511/empire-core-new/backend

OFFICIAL_APP=/home/nawaf511/empire-core-new/backend/app

OFFICIAL_TEST_DIR=/home/nawaf511/empire-core-new/tests

OFFICIAL_REPORT_DIR=/home/nawaf511/ndsp_launch_reports

OFFICIAL_BACKUP_DIR=/home/nawaf511/ndsp_backups

OFFICIAL_SNAPSHOT_DIR=/home/nawaf511/ndsp_snapshots

OFFICIAL_E2E_TEST=/home/nawaf511/empire-core-new/tests/test_ndsp_e2e_layer1_to_layer16.py

OFFICIAL_RUNTIME_ENDPOINT=http://127.0.0.1:9001/decision
```

---

# 3) Forbidden Non-Official Paths

## المسارات غير المعتمدة والمحظورة

```text
/home/nawaf511/empire-core-new/ndsp_launch_reports

/home/nawaf511/empire-core-new/backend/test_e2e_pipeline.py

/home/nawaf511/empire-core-new/backend/ndsp_launch_reports

/home/nawaf511/empire-core-new/backend/reports

/home/nawaf511/empire-core-new/reports

/home/nawaf511/empire-core-new/tests_e2e

/home/nawaf511/empire-core-new/backend/tests_e2e
```

---

# 4) قاعدة اعتماد اختبارات E2E

لا يتم اعتماد أي اختبار End-to-End داخل NDSP إلا إذا تحقق التالي بالكامل:

```text
1) التقرير داخل /home/nawaf511/ndsp_launch_reports

2) النسخة الاحتياطية داخل /home/nawaf511/ndsp_backups

3) ملف الاختبار داخل /home/nawaf511/empire-core-new/tests

4) الاختبار يقرأ من:
   http://127.0.0.1:9001/decision

5) النتيجة تحتوي:
   SOURCE_MODE=http_decision

6) النتيجة تحتوي:
   FAILED_SYMBOLS=[]

7) النتيجة تحتوي:
   FINAL_STATUS=E2E_LAYER1_TO_LAYER16_DONE
```

---

# 5) القاعدة الحاكمة العليا

## The Governing Rule

أي نتيجة اختبار أو تقرير أو Script أو Patch أو Layer أو Runtime Modification:

### تعتبر غير معتمدة بالكامل إذا استخدمت:
- مسارات غير رسمية
- ملفات وهمية
- ملفات غير موجودة
- Runtime غير حقيقي
- بيانات غير حية
- مصادر غير معتمدة

حتى لو بدا الاختبار:
- ناجحًا
- منطقيًا
- صحيحًا ظاهريًا

---

# 6) شرط Runtime الحقيقي

## Real Runtime Validation Rule

أي اختبار E2E حقيقي يجب أن يثبت أنه قرأ من الـ Runtime الحقيقي للمنظومة.

الشرط الرسمي:

```text
SOURCE_MODE=http_decision
```

إذا لم تظهر هذه القيمة، فالاختبار يعتبر:

```text
NON-LIVE
NON-RUNTIME
STRUCTURAL ONLY
NOT OFFICIALLY ACCEPTED
```

---

# 7) قانون توحيد أدوات الذكاء

## Multi-AI Unification Law

أي أداة ذكاء اصطناعي تعمل على NDSP يجب أن:

- تستخدم نفس المسارات
- تستخدم نفس التقارير
- تستخدم نفس مجلدات النسخ الاحتياطية
- تستخدم نفس Runtime Endpoint
- تستخدم نفس Governance Contracts
- تستخدم نفس أسماء الاختبارات
- تستخدم نفس Final Assertions

ويُمنع عليها:

- اختراع مسارات جديدة
- إنشاء Runtime بديل
- إنشاء مجلد Reports خاص بها
- إنشاء Tests خارج المسار الرسمي
- استخدام Endpoints غير معتمدة
- إنشاء Logic موازٍ غير موثق

---

# 8) قانون كشف الملفات الوهمية

## Ghost Detection Law

أي ملف اختبار أو تقرير أو Runtime Path غير معتمد يعتبر:

```text
GHOST_FILE
GHOST_PATH
UNOFFICIAL_RUNTIME
NON-GOVERNED_OUTPUT
```

ويجب اكتشافه والإبلاغ عنه تلقائيًا.

---

# 9) Official Verification Script

## سكربت التحقق الرسمي الموحد

```sh
#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
TEST_DIR="$ROOT/tests"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups"

OFFICIAL_TEST="$TEST_DIR/test_ndsp_e2e_layer1_to_layer16.py"

log() {
  echo "$@"
}

section() {
  echo ""
  echo "$1"
  echo "------------------------------------------------------------"
}

section "1) Detect conflicting or ghost test paths"

GHOSTS=(
"$ROOT/ndsp_launch_reports"
"$BACKEND/test_e2e_pipeline.py"
"$BACKEND/ndsp_launch_reports"
)

FOUND_GHOSTS=0

for g in "${GHOSTS[@]}"; do
  if [ -e "$g" ]; then
    FOUND_GHOSTS=$((FOUND_GHOSTS+1))
    log "GHOST_FOUND=$g"
  else
    log "GHOST_NOT_FOUND=$g"
  fi
done

log "FOUND_GHOSTS=$FOUND_GHOSTS"

section "2) Verify official E2E test exists"

if [ -f "$OFFICIAL_TEST" ]; then
  log "OFFICIAL_E2E_TEST_EXISTS=True"
  log "OFFICIAL_E2E_TEST=$OFFICIAL_TEST"
else
  log "OFFICIAL_E2E_TEST_EXISTS=False"
  log "WARNING: official E2E test file not found"
fi

section "3) Verify latest official E2E report"

LATEST_E2E="$(ls -t "$REPORT_DIR"/NDSP_E2E_LAYER1_TO_LAYER16_*.md 2>/dev/null | head -1 || true)"

if [ -n "$LATEST_E2E" ]; then

  log "LATEST_E2E_REPORT=$LATEST_E2E"

  if grep -q "SOURCE_MODE= http_decision" "$LATEST_E2E" || \
     grep -q "source_mode.*http_decision" "$LATEST_E2E"; then

    log "LATEST_E2E_SOURCE_MODE_HTTP_DECISION=True"

  else

    log "LATEST_E2E_SOURCE_MODE_HTTP_DECISION=False"

  fi

  if grep -q "FINAL_STATUS=E2E_LAYER1_TO_LAYER16_DONE" "$LATEST_E2E"; then
    log "LATEST_E2E_FINAL_STATUS_OK=True"
  else
    log "LATEST_E2E_FINAL_STATUS_OK=False"
  fi

else

  log "LATEST_E2E_REPORT_NOT_FOUND=True"

fi

section "4) Final Assertions"

ASSERT_OK=True

if [ "$FOUND_GHOSTS" -gt 0 ]; then
  ASSERT_OK=False
fi

if [ "$ASSERT_OK" = "True" ]; then
  log "ASSERT_OK=True"
  log "FINAL_STATUS=E2E_TEST_STANDARD_LOCKED"
else
  log "ASSERT_OK=False"
  log "FINAL_STATUS=E2E_TEST_STANDARD_FAILED"
  exit 1
fi

log "REPORT_DIR=$REPORT_DIR"
log "BACKUP_DIR=$BACKUP_DIR"
log "DONE"
```

---

# 10) Final Governance Contract

## العقد النهائي الموحد

من الآن:

- لا يوجد Runtime بديل.
- لا يوجد Test Path بديل.
- لا يوجد Report Directory بديل.
- لا يوجد Backup Directory بديل.
- لا يوجد Endpoint بديل.
- لا يوجد E2E Logic بديل.

المنظومة تعتمد فقط:

```text
THE OFFICIAL NDSP GOVERNED PATH STANDARD
```

وأي أداة لا تلتزم بهذا القانون تعتبر:

```text
NON-GOVERNED
NON-OFFICIAL
NON-ACCEPTED
```

---

# 11) Golden Rule

## القاعدة الذهبية

```text
All AI tools must obey the same governed architecture,
the same runtime,
the same paths,
the same contracts,
and the same validation standards.

Otherwise the result is not officially trusted.
```
