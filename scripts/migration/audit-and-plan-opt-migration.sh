#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
OPT_ROOT="${OPT_ROOT:-/opt}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

OUTPUT_DIR="${PROJECT_ROOT}/var/audits/opt-migration-${TIMESTAMP}"
REPORT_MD="${OUTPUT_DIR}/OPT_MIGRATION_REPORT.md"
SERVICES_CSV="${OUTPUT_DIR}/OPT_SERVICES.csv"
SERVICES_JSON="${OUTPUT_DIR}/OPT_SERVICES.json"
PLAN_SCRIPT="${OUTPUT_DIR}/PROPOSED_MIGRATION_COMMANDS.sh"
DELETE_CANDIDATES="${OUTPUT_DIR}/DELETE_CANDIDATES.txt"
BLOCKED_PATHS="${OUTPUT_DIR}/BLOCKED_ACTIVE_PATHS.txt"
ERROR_LOG="${OUTPUT_DIR}/ERRORS.log"

mkdir -p "${OUTPUT_DIR}"
touch \
  "${REPORT_MD}" \
  "${SERVICES_CSV}" \
  "${SERVICES_JSON}" \
  "${PLAN_SCRIPT}" \
  "${DELETE_CANDIDATES}" \
  "${BLOCKED_PATHS}" \
  "${ERROR_LOG}"

log() {
  printf '\033[1;34m[OPT-MIGRATION]\033[0m %s\n' "$*"
}

warn() {
  printf '\033[1;33m[WARN]\033[0m %s\n' "$*" >&2
}

fail() {
  printf '\033[1;31m[ERROR]\033[0m %s\n' "$*" >&2
  exit 1
}

command -v systemctl >/dev/null 2>&1 ||
  fail "systemctl غير متوفر."

[[ -d "${PROJECT_ROOT}" ]] ||
  fail "المشروع غير موجود: ${PROJECT_ROOT}"

[[ -d "${OPT_ROOT}" ]] ||
  fail "/opt غير موجود."

cd "${PROJECT_ROOT}"

log "بدء تدقيق خدمات /opt"

printf '%s\n' \
  'service,enabled,active,substate,working_directory,exec_start,opt_path_exists,candidate_path,candidate_exists,classification' \
  > "${SERVICES_CSV}"

echo '[' > "${SERVICES_JSON}"

cat > "${PLAN_SCRIPT}" <<'PLAN_HEADER'
#!/usr/bin/env bash
set -Eeuo pipefail

# هذا الملف مولد تلقائيًا.
# لا تشغله كاملًا دفعة واحدة.
# راجع كل قسم وخدمة قبل التنفيذ.
#
# الخطوات الصحيحة لكل خدمة:
# 1. نسخ المصدر إلى empire-core-new.
# 2. اختبار الخدمة على منفذ بديل.
# 3. أخذ نسخة احتياطية من ملف systemd.
# 4. تعديل WorkingDirectory وExecStart.
# 5. daemon-reload.
# 6. restart.
# 7. health check.
# 8. rollback عند الفشل.

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
PLAN_HEADER

map_candidate_path() {
  local opt_path="$1"
  local base_name

  base_name="$(basename "${opt_path}")"

  case "${base_name}" in
    empire-core)
      printf '%s\n' "${PROJECT_ROOT}"
      ;;

    ndsp16-api)
      printf '%s\n' "${PROJECT_ROOT}/apps/ndsp-layers-api"
      ;;

    ndsp-market-data-bridge-v2)
      printf '%s\n' "${PROJECT_ROOT}/apps/ndsp-raw-cot-gateway"
      ;;

    ndsp-platform-gateway-9002)
      printf '%s\n' "${PROJECT_ROOT}/backend/gateway"
      ;;

    ndsp-admin-user-ops)
      printf '%s\n' "${PROJECT_ROOT}/backend/admin_users_official_api"
      ;;

    ndsp-decision-package-v1)
      printf '%s\n' "${PROJECT_ROOT}/backend/services/completed_decision"
      ;;

    ndsp-auth-core-clean)
      printf '%s\n' "${PROJECT_ROOT}/backend/auth_api"
      ;;

    ndsp-change-password-gateway)
      printf '%s\n' "${PROJECT_ROOT}/backend/password_reset_gateway"
      ;;

    ndsp-registration-mailer-v12-1)
      printf '%s\n' "${PROJECT_ROOT}/backend/integrations"
      ;;

    *)
      printf '%s\n' "${PROJECT_ROOT}/legacy-import/${base_name}"
      ;;
  esac
}

classify_service() {
  local active="$1"
  local opt_exists="$2"
  local candidate_exists="$3"

  if [[ "${active}" == "active" && "${opt_exists}" == "yes" ]]; then
    if [[ "${candidate_exists}" == "yes" ]]; then
      printf '%s\n' "ACTIVE_CANDIDATE_EXISTS_VERIFY_BEFORE_CUTOVER"
    else
      printf '%s\n' "ACTIVE_BLOCKED_MIGRATION_REQUIRED"
    fi
    return
  fi

  if [[ "${active}" != "active" && "${opt_exists}" == "yes" ]]; then
    if [[ "${candidate_exists}" == "yes" ]]; then
      printf '%s\n' "INACTIVE_DUPLICATE_REVIEW"
    else
      printf '%s\n' "INACTIVE_ARCHIVE_CANDIDATE"
    fi
    return
  fi

  printf '%s\n' "BROKEN_SERVICE_REFERENCE"
}

json_escape() {
  python3 -c '
import json, sys
print(json.dumps(sys.stdin.read().rstrip("\n")))
'
}

discover_units() {
  {
    sudo grep -RIl '/opt/' \
      /etc/systemd/system \
      /lib/systemd/system \
      2>/dev/null || true
  } |
  while IFS= read -r file; do
    basename "${file}"
  done |
  sed 's/\.wants$//' |
  grep '\.service$' |
  sort -u
}

mapfile -t UNITS < <(discover_units)

if [[ "${#UNITS[@]}" -eq 0 ]]; then
  warn "لم يتم العثور على خدمات تشير إلى /opt."
fi

JSON_FIRST=1

for unit in "${UNITS[@]}"; do
  log "تحليل ${unit}"

  enabled="$(
    systemctl is-enabled "${unit}" 2>/dev/null ||
    echo "unknown"
  )"

  active="$(
    systemctl is-active "${unit}" 2>/dev/null ||
    echo "inactive"
  )"

  substate="$(
    systemctl show "${unit}" \
      -p SubState \
      --value \
      2>/dev/null ||
    echo "unknown"
  )"

  working_directory="$(
    systemctl show "${unit}" \
      -p WorkingDirectory \
      --value \
      2>/dev/null ||
    true
  )"

  exec_start="$(
    systemctl show "${unit}" \
      -p ExecStart \
      --value \
      2>/dev/null ||
    true
  )"

  opt_path=""

  if [[ "${working_directory}" == /opt/* ]]; then
    opt_path="${working_directory}"
  else
    opt_path="$(
      printf '%s\n' "${exec_start}" |
      grep -oE '/opt/[^ ;}]+' |
      head -n 1 ||
      true
    )"
  fi

  if [[ -z "${opt_path}" ]]; then
    continue
  fi

  while [[ ! -e "${opt_path}" && "${opt_path}" != "/opt" ]]; do
    opt_path="$(dirname "${opt_path}")"
  done

  if [[ -e "${opt_path}" ]]; then
    opt_exists="yes"
  else
    opt_exists="no"
  fi

  candidate_path="$(map_candidate_path "${opt_path}")"

  if [[ -e "${candidate_path}" ]]; then
    candidate_exists="yes"
  else
    candidate_exists="no"
  fi

  classification="$(
    classify_service \
      "${active}" \
      "${opt_exists}" \
      "${candidate_exists}"
  )"

  printf '%s,%s,%s,%s,%q,%q,%s,%q,%s,%s\n' \
    "${unit}" \
    "${enabled}" \
    "${active}" \
    "${substate}" \
    "${working_directory}" \
    "${exec_start}" \
    "${opt_exists}" \
    "${candidate_path}" \
    "${candidate_exists}" \
    "${classification}" \
    >> "${SERVICES_CSV}"

  if [[ "${JSON_FIRST}" -eq 0 ]]; then
    echo ',' >> "${SERVICES_JSON}"
  fi

  JSON_FIRST=0

  UNIT="${unit}" \
  ENABLED="${enabled}" \
  ACTIVE="${active}" \
  SUBSTATE="${substate}" \
  WORKING_DIRECTORY="${working_directory}" \
  EXEC_START_VALUE="${exec_start}" \
  OPT_PATH="${opt_path}" \
  OPT_EXISTS="${opt_exists}" \
  CANDIDATE_PATH="${candidate_path}" \
  CANDIDATE_EXISTS="${candidate_exists}" \
  CLASSIFICATION="${classification}" \
  python3 <<'PY' >> "${SERVICES_JSON}"
import json
import os

print(json.dumps({
    "service": os.environ["UNIT"],
    "enabled": os.environ["ENABLED"],
    "active": os.environ["ACTIVE"],
    "substate": os.environ["SUBSTATE"],
    "workingDirectory": os.environ["WORKING_DIRECTORY"],
    "execStart": os.environ["EXEC_START_VALUE"],
    "optPath": os.environ["OPT_PATH"],
    "optPathExists": os.environ["OPT_EXISTS"] == "yes",
    "candidatePath": os.environ["CANDIDATE_PATH"],
    "candidateExists": os.environ["CANDIDATE_EXISTS"] == "yes",
    "classification": os.environ["CLASSIFICATION"],
}, ensure_ascii=False, indent=2))
PY

  if [[ "${active}" == "active" ]]; then
    printf '%s | %s | %s\n' \
      "${unit}" \
      "${opt_path}" \
      "${classification}" \
      >> "${BLOCKED_PATHS}"
  fi

  cat >> "${PLAN_SCRIPT}" <<PLAN_ENTRY

# ==============================================================================
# الخدمة: ${unit}
# الحالة: ${active}
# التصنيف: ${classification}
# المصدر: ${opt_path}
# الوجهة المقترحة: ${candidate_path}
# ==============================================================================

echo "مراجعة ${unit}"

# نسخة احتياطية لملف الخدمة:
# sudo cp -a \
#   "/etc/systemd/system/${unit}" \
#   "/etc/systemd/system/${unit}.bak-${TIMESTAMP}"

# إنشاء الوجهة:
# mkdir -p "${candidate_path}"

# نسخ مبدئي دون حذف المصدر:
# sudo rsync -aHAX --numeric-ids \
#   "${opt_path}/" \
#   "${candidate_path}/"

# بعد تعديل الخدمة يدويًا:
# sudo systemctl daemon-reload
# sudo systemctl restart "${unit}"
# sudo systemctl status "${unit}" --no-pager

PLAN_ENTRY
done

echo ']' >> "${SERVICES_JSON}"

log "تحليل مجلدات /opt غير المستخدمة مباشرة"

declare -A ACTIVE_TOP_PATHS=()

while IFS='|' read -r unit path classification; do
  path="$(echo "${path}" | xargs)"
  [[ -n "${path}" ]] || continue

  top="/opt/$(echo "${path#/opt/}" | cut -d/ -f1)"
  ACTIVE_TOP_PATHS["${top}"]=1
done < "${BLOCKED_PATHS}"

while IFS= read -r top_path; do
  [[ -n "${top_path}" ]] || continue

  base="$(basename "${top_path}")"

  case "${base}" in
    containerd|brave.com|metasploit-framework)
      continue
      ;;
  esac

  if [[ -n "${ACTIVE_TOP_PATHS[${top_path}]:-}" ]]; then
    continue
  fi

  if sudo grep -Rqs "${top_path}" \
    /etc/systemd/system \
    /lib/systemd/system \
    /etc/cron.d \
    /etc/crontab \
    2>/dev/null
  then
    continue
  fi

  if ps auxww | grep -F "${top_path}" | grep -v grep >/dev/null; then
    continue
  fi

  printf '%s\n' "${top_path}" >> "${DELETE_CANDIDATES}"
done < <(
  sudo find /opt \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    -print \
    2>/dev/null |
  sort
)

log "إنشاء التقرير النهائي"

TOTAL_SERVICES="$(tail -n +2 "${SERVICES_CSV}" | wc -l)"
ACTIVE_SERVICES="$(
  awk -F',' 'NR > 1 && $3 == "active" {count++} END {print count+0}' \
    "${SERVICES_CSV}"
)"
BLOCKED_SERVICES="$(
  grep -c 'ACTIVE_BLOCKED_MIGRATION_REQUIRED' \
    "${SERVICES_CSV}" ||
  true
)"
CANDIDATE_EXISTS_COUNT="$(
  awk -F',' 'NR > 1 && $9 == "yes" {count++} END {print count+0}' \
    "${SERVICES_CSV}"
)"
DELETE_COUNT="$(
  grep -c . "${DELETE_CANDIDATES}" ||
  true
)"

cat > "${REPORT_MD}" <<EOF
# NDSP /opt Migration Report

Generated: $(date --iso-8601=seconds)

Project root:

\`\`\`text
${PROJECT_ROOT}
\`\`\`

## Executive Summary

| Metric | Count |
|---|---:|
| Services referencing /opt | ${TOTAL_SERVICES} |
| Active services | ${ACTIVE_SERVICES} |
| Active services blocked on migration | ${BLOCKED_SERVICES} |
| Services with candidate path in empire-core-new | ${CANDIDATE_EXISTS_COUNT} |
| Potential archive/delete candidates | ${DELETE_COUNT} |

## Decision

لا يجوز حذف \`/opt\` كاملًا.

الأسباب:

1. توجد خدمات systemd نشطة تعتمد على مسارات داخله.
2. توجد مكونات نظامية مثل containerd وبرامج مثبتة مثل Brave وMetasploit.
3. بعض الخدمات لا يوجد لها بديل مؤكد داخل empire-core-new حتى الآن.
4. يجب نقل كل خدمة واختبارها منفردة قبل إزالة المصدر القديم.

## Active Blocked Paths

\`\`\`text
$(cat "${BLOCKED_PATHS}" 2>/dev/null || true)
\`\`\`

## Potential Archive Candidates

هذه القائمة لا تعني أن الحذف آمن تلقائيًا. هي قائمة أولية لمجلدات لا يظهر أنها مستخدمة مباشرة من systemd أو العمليات أو cron.

\`\`\`text
$(cat "${DELETE_CANDIDATES}" 2>/dev/null || true)
\`\`\`

## Generated Files

- Services CSV: \`${SERVICES_CSV}\`
- Services JSON: \`${SERVICES_JSON}\`
- Proposed commands: \`${PLAN_SCRIPT}\`
- Active blocked paths: \`${BLOCKED_PATHS}\`
- Delete candidates: \`${DELETE_CANDIDATES}\`
- Errors: \`${ERROR_LOG}\`

## Recommended Execution Order

1. ابدأ بالخدمات غير النشطة.
2. بعد ذلك الخدمات التي يوجد لها مسار مقابل داخل empire-core-new.
3. اختبر كل خدمة على منفذ بديل.
4. انقل ملف systemd بعد نجاح الاختبار.
5. راقب السجلات والمنافذ.
6. اترك المصدر القديم مدة استقرار.
7. انقل المصدر القديم إلى أرشيف بدل حذفه مباشرة.
8. لا تحذف أي مجلد نظامي تحت /opt.

EOF

chmod +x "${PLAN_SCRIPT}"

ARCHIVE="${PROJECT_ROOT}/var/audits/OPT_MIGRATION_AUDIT_${TIMESTAMP}.tar.gz"

tar \
  -czf "${ARCHIVE}" \
  -C "$(dirname "${OUTPUT_DIR}")" \
  "$(basename "${OUTPUT_DIR}")"

log "اكتمل التدقيق"

cat <<EOF

============================================================
اكتمل تدقيق /opt وخطة الانتقال
============================================================

التقرير:
${REPORT_MD}

الخدمات CSV:
${SERVICES_CSV}

الخدمات JSON:
${SERVICES_JSON}

خطة أوامر مقترحة:
${PLAN_SCRIPT}

المجلدات النشطة المحظورة من الحذف:
${BLOCKED_PATHS}

مرشحو الأرشفة:
${DELETE_CANDIDATES}

الملف المضغوط:
${ARCHIVE}

عرض الملخص:
sed -n '1,220p' "${REPORT_MD}"

عرض الخدمات النشطة:
awk -F',' 'NR==1 || \$3=="active"' "${SERVICES_CSV}" | column -s, -t

مهم:
لم يتم حذف أي ملف.
لم يتم إيقاف أو إعادة تشغيل أي خدمة.
لم يتم تعديل systemd.
============================================================

EOF
