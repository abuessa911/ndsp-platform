#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
QUARANTINE_ROOT="${QUARANTINE_ROOT:-/opt/.ndsp-quarantine-20260806-100615}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

OUTPUT_DIR="${PROJECT_ROOT}/var/audits/finalization-${TIMESTAMP}"
SYSTEMD_BACKUP="${OUTPUT_DIR}/systemd"
FINAL_REPORT="${OUTPUT_DIR}/FINALIZATION_REPORT.md"
OPT_SERVICES="${OUTPUT_DIR}/ACTIVE_OPT_SERVICES.txt"
STALE_SERVICES="${OUTPUT_DIR}/STALE_MISSING_PATH_SERVICES.txt"
QUARANTINE_MANIFEST="${OUTPUT_DIR}/QUARANTINE_MANIFEST.txt"
QUARANTINE_SHA="${OUTPUT_DIR}/QUARANTINE_MANIFEST.sha256"

UI_PLAN_DIR="${PROJECT_ROOT}/docs/product-ui"
BUILD_READINESS="${UI_PLAN_DIR}/BUILD_READINESS.md"
PAGE_REGISTRY="${UI_PLAN_DIR}/PAGE_REGISTRY.md"
RUNTIME_MAP="${UI_PLAN_DIR}/RUNTIME_DEPENDENCY_MAP.md"

mkdir -p \
  "${OUTPUT_DIR}" \
  "${SYSTEMD_BACKUP}" \
  "${UI_PLAN_DIR}"

log() {
  printf '\033[1;34m[FINALIZE]\033[0m %s\n' "$*"
}

ok() {
  printf '\033[1;32m[OK]\033[0m %s\n' "$*"
}

fail() {
  printf '\033[1;31m[BLOCKED]\033[0m %s\n' "$*" >&2
  exit 1
}

[[ -d "${PROJECT_ROOT}" ]] ||
  fail "المشروع الرئيسي غير موجود: ${PROJECT_ROOT}"

cd "${PROJECT_ROOT}"

log "حفظ حالة المشروع"

{
  echo "Generated: $(date --iso-8601=seconds)"
  echo
  git status --short --branch 2>/dev/null || true
  echo
  git log --oneline -n 20 2>/dev/null || true
} > "${OUTPUT_DIR}/GIT_STATE.txt"

log "حفظ ملفات خدمات systemd ذات العلاقة"

while IFS= read -r unit_file; do
  [[ -e "${unit_file}" ]] || continue

  resolved_file="$(
    readlink -f "${unit_file}" 2>/dev/null || true
  )"

  [[ -n "${resolved_file}" ]] || continue
  [[ -f "${resolved_file}" ]] || continue

  # استخدام مسار كامل مشفر لتجنب تصادم أسماء الملفات،
  # ونسخ المحتوى الحقيقي بدل الرابط الرمزي.
  safe_name="$(
    printf '%s' "${resolved_file}" |
    sed 's#^/##; s#/#__#g'
  )"

  destination="${SYSTEMD_BACKUP}/${safe_name}"

  if [[ -e "${destination}" ]]; then
    continue
  fi

  sudo cp --dereference \
    --preserve=mode,timestamps \
    "${resolved_file}" \
    "${destination}"

  sudo chown "$(id -u):$(id -g)" "${destination}"
done < <(
  sudo grep -RIlE \
    '/opt/|empire-core-new|ndsp|ndip|empire' \
    /etc/systemd/system \
    /lib/systemd/system \
    2>/dev/null |
  sort -u
)

log "حصر الخدمات النشطة التي ما زالت تعتمد على /opt"

: > "${OPT_SERVICES}"
: > "${STALE_SERVICES}"

while IFS= read -r unit; do
  [[ -n "${unit}" ]] || continue

  active="$(
    systemctl is-active "${unit}" 2>/dev/null ||
    echo inactive
  )"

  working_directory="$(
    systemctl show \
      "${unit}" \
      -p WorkingDirectory \
      --value \
      2>/dev/null ||
    true
  )"

  exec_start="$(
    systemctl show \
      "${unit}" \
      -p ExecStart \
      --value \
      2>/dev/null ||
    true
  )"

  if [[ "${active}" == "active" ]] &&
     {
       [[ "${working_directory}" == /opt/* ]] ||
       [[ "${exec_start}" == *"/opt/"* ]]
     }
  then
    printf '%s | %s | %s\n' \
      "${unit}" \
      "${working_directory}" \
      "${exec_start}" \
      >> "${OPT_SERVICES}"
  fi

  if [[ -n "${working_directory}" ]] &&
     [[ "${working_directory}" == /opt/* ]] &&
     [[ ! -e "${working_directory}" ]]
  then
    printf '%s | %s | active=%s\n' \
      "${unit}" \
      "${working_directory}" \
      "${active}" \
      >> "${STALE_SERVICES}"
  fi
done < <(
  systemctl list-unit-files \
    --type=service \
    --no-legend |
  awk '{print $1}'
)

log "فحص مجلد الحجر"

if [[ ! -e "${QUARANTINE_ROOT}" ]]; then
  echo "مجلد الحجر غير موجود أصلًا." \
    > "${QUARANTINE_MANIFEST}"
else
  sudo find "${QUARANTINE_ROOT}" \
    -printf '%y|%M|%u:%g|%s|%TY-%Tm-%TdT%TH:%TM:%TS|%p\n' \
    2>/dev/null \
    > "${QUARANTINE_MANIFEST}"

  sha256sum "${QUARANTINE_MANIFEST}" \
    > "${QUARANTINE_SHA}"

  if ps auxww |
     grep -F "${QUARANTINE_ROOT}" |
     grep -v grep \
     >/dev/null
  then
    fail "توجد عملية تستخدم مجلد الحجر."
  fi

  if sudo grep -RqsF "${QUARANTINE_ROOT}" \
    /etc/systemd/system \
    /lib/systemd/system \
    /etc/cron.d \
    /etc/crontab \
    /etc/nginx \
    2>/dev/null
  then
    fail "يوجد مرجع نظامي مباشر إلى مجلد الحجر."
  fi

  if command -v lsof >/dev/null 2>&1; then
    if sudo lsof +D "${QUARANTINE_ROOT}" \
       2>/dev/null |
       tail -n +2 |
       grep -q .
    then
      fail "توجد ملفات مفتوحة داخل مجلد الحجر."
    fi
  fi

  log "حذف مجلد الحجر بعد نجاح الفحص"

  sudo rm -rf --one-file-system "${QUARANTINE_ROOT}"

  [[ ! -e "${QUARANTINE_ROOT}" ]] ||
    fail "تعذر حذف مجلد الحجر كاملًا."
fi

ok "تم حذف الحجر فقط، ولم يُحذف /opt."

log "إنشاء خريطة جاهزية الصفحات والواجهات"

cat > "${BUILD_READINESS}" <<EOF
# NDSP Product UI Build Readiness

Generated: $(date --iso-8601=seconds)

## Canonical repository

\`\`\`text
${PROJECT_ROOT}
\`\`\`

## الحالة

- محرك COT الأسبوعي مثبت ومختبر.
- الحالة الأساسية محفوظة في صورة \`[L,S]\`.
- طبقات canonical_v1 موجودة.
- إطار الخدمات والعقود والحوكمة موجود.
- خدمات إنتاج ما زالت تعتمد على \`/opt\` ويجب ترحيلها تدريجيًا.
- حذف \`/opt\` كاملًا غير معتمد في هذه المرحلة.

## بوابات البناء

قبل توصيل أي صفحة ببيانات حية، يجب تحديد:

1. عقد البيانات المستخدم.
2. مالك الخدمة canonical owner.
3. منفذ أو Gateway الوصول.
4. مستوى ظهور الطبقة.
5. سياسة إخراج القرار.
6. سياسة الخصوصية والصلاحيات.
7. حالة الخدمة: canonical أو legacy أو bridge.

## ترتيب بناء الواجهات

1. الهيكل العام والتنقل.
2. المصادقة والحساب.
3. لوحة المستخدم.
4. صفحة السوق والبيانات الحية.
5. صفحة تحليل COT.
6. طبقات الاتجاه والجودة والمخاطر.
7. حزمة القرار المكتمل.
8. التنبيهات والقنوات.
9. الإدارة والحوكمة.
10. الصفحات العامة والتجارية.
EOF

cat > "${PAGE_REGISTRY}" <<'EOF'
# NDSP Page Registry

| Page | Purpose | Data owner | Status |
|---|---|---|---|
| Landing | التعريف بالمنصة والباقات | Public gateway | Planned |
| Login | تسجيل الدخول | Auth API | Planned |
| Register | التسجيل والموافقة | Registration services | Planned |
| User Dashboard | عرض ملخص المستخدم | User dashboard service | Planned |
| Market Overview | السوق والبيانات الحية | Market adapter/bridge | Planned |
| COT Analysis | قراءة COT الأسبوعية والتحالفات | COT direction engine | Ready for API integration |
| Analytical Layers | عرض الطبقات التحليلية | Layers API | Planned |
| Decision Package | حزمة القرار المكتمل | Completed decision service | Planned |
| Alerts | قنوات وتنبيهات المستخدم | Alert channels | Planned |
| Admin Console | الإدارة والعمليات | Admin services | Existing/Review |
| Governance | العقود والسياسات والحالة | Governance bridge | Planned |
EOF

cat > "${RUNTIME_MAP}" <<EOF
# NDSP Runtime Dependency Map

Generated: $(date --iso-8601=seconds)

## المشروع الرئيسي

\`\`\`text
${PROJECT_ROOT}
\`\`\`

## الخدمات النشطة التي ما زالت تعتمد على /opt

\`\`\`text
$(cat "${OPT_SERVICES}" 2>/dev/null || true)
\`\`\`

## الخدمات ذات مسارات مفقودة أو قديمة

\`\`\`text
$(cat "${STALE_SERVICES}" 2>/dev/null || true)
\`\`\`

## قاعدة الحذف

لا يتم حذف أي مسار من /opt إذا كان واحد من الآتي صحيحًا:

- خدمة active تشير إليه.
- ExecStart يستخدمه.
- عملية حية تستخدمه.
- Nginx أو cron يشير إليه.
- لا يوجد بديل مختبر في empire-core-new.
EOF

cat > "${FINAL_REPORT}" <<EOF
# NDSP Main Repository Finalization

Generated: $(date --iso-8601=seconds)

## تم

- حذف مجلد الحجر:
  \`${QUARANTINE_ROOT}\`
- الاحتفاظ بسجل كامل لمحتواه قبل الحذف.
- حفظ ملفات systemd ذات العلاقة.
- حصر الخدمات النشطة المعتمدة على /opt.
- إنشاء سجل الصفحات.
- إنشاء خريطة اعتماد Runtime.
- تجهيز مرحلة بناء الصفحات والواجهات.

## لم يتم

- لم يُحذف /opt كاملًا.
- لم تتوقف خدمة إنتاج.
- لم تتغير ملفات systemd.
- لم تتغير إعدادات Nginx.
- لم تُنقل خدمات حية آليًا.

## الخدمات النشطة المعتمدة على /opt

\`\`\`text
$(cat "${OPT_SERVICES}" 2>/dev/null || true)
\`\`\`

## الملفات الناتجة

- Git state: \`${OUTPUT_DIR}/GIT_STATE.txt\`
- Systemd backup: \`${SYSTEMD_BACKUP}\`
- Active /opt services: \`${OPT_SERVICES}\`
- Stale services: \`${STALE_SERVICES}\`
- Quarantine manifest: \`${QUARANTINE_MANIFEST}\`
- UI readiness: \`${BUILD_READINESS}\`
- Page registry: \`${PAGE_REGISTRY}\`
- Runtime map: \`${RUNTIME_MAP}\`
EOF

log "تشغيل الاختبارات الحالية"

npm run test:cot-direction

log "فحص خدمات النظام"

systemctl --failed --no-pager \
  > "${OUTPUT_DIR}/FAILED_SERVICES_AFTER.txt" ||
  true

ARCHIVE="${PROJECT_ROOT}/var/audits/FINALIZATION_${TIMESTAMP}.tar.gz"

tar \
  -czf "${ARCHIVE}" \
  -C "$(dirname "${OUTPUT_DIR}")" \
  "$(basename "${OUTPUT_DIR}")"

ok "اكتملت عملية الإنهاء."

cat <<EOF

============================================================
اكتملت مرحلة التنظيف والتهيئة
============================================================

تم حذف الحجر:
${QUARANTINE_ROOT}

لم يتم حذف /opt لأن خدمات إنتاج ما زالت تعتمد عليه.

التقرير:
${FINAL_REPORT}

خطة الصفحات:
${PAGE_REGISTRY}

جاهزية البناء:
${BUILD_READINESS}

خريطة التشغيل:
${RUNTIME_MAP}

الخدمات النشطة على /opt:
${OPT_SERVICES}

الأرشيف:
${ARCHIVE}

عرض التقرير:
sed -n '1,240p' "${FINAL_REPORT}"

============================================================

EOF
