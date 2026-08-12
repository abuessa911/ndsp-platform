#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

LATEST_STAGE="$(
  ls -1dt "${PROJECT_ROOT}"/var/audits/opt-stage-* 2>/dev/null |
  head -n 1
)"

[[ -n "${LATEST_STAGE}" ]] || {
  echo "[ERROR] لا يوجد تقرير opt-stage."
  exit 1
}

MANIFEST="${LATEST_STAGE}/SERVICES.tsv"
AUDIT_DIR="${PROJECT_ROOT}/var/audits/opt-cutover-${TIMESTAMP}"
BACKUP_DIR="${AUDIT_DIR}/systemd-backups"
REPORT="${AUDIT_DIR}/CUTOVER_REPORT.tsv"
LOG_FILE="${AUDIT_DIR}/CUTOVER.log"

mkdir -p "${AUDIT_DIR}" "${BACKUP_DIR}"

printf '%s\t%s\t%s\t%s\t%s\n' \
  "service" \
  "source" \
  "destination" \
  "result" \
  "details" \
  > "${REPORT}"

log() {
  printf '\033[1;34m[CUTOVER]\033[0m %s\n' "$*" |
    tee -a "${LOG_FILE}"
}

ok() {
  printf '\033[1;32m[OK]\033[0m %s\n' "$*" |
    tee -a "${LOG_FILE}"
}

warn() {
  printf '\033[1;33m[WARN]\033[0m %s\n' "$*" |
    tee -a "${LOG_FILE}" >&2
}

fail() {
  printf '\033[1;31m[ERROR]\033[0m %s\n' "$*" |
    tee -a "${LOG_FILE}" >&2
  exit 1
}

[[ -f "${MANIFEST}" ]] ||
  fail "ملف SERVICES.tsv غير موجود: ${MANIFEST}"

command -v rsync >/dev/null 2>&1 ||
  fail "rsync غير مثبت."

get_ports_for_pid() {
  local pid="$1"

  if [[ ! "${pid}" =~ ^[0-9]+$ ]] || [[ "${pid}" -le 0 ]]; then
    return 0
  fi

  sudo ss -lntp 2>/dev/null |
    grep -E "pid=${pid}([,)]|$)" |
    awk '{print $4}' |
    sed 's/.*://' |
    sort -u ||
    true
}

rollback_service() {
  local unit="$1"
  local fragment_backup="$2"
  local fragment_path="$3"

  warn "بدء Rollback للخدمة ${unit}"

  sudo systemctl stop "${unit}" 2>/dev/null || true

  if [[ -f "${fragment_backup}" ]]; then
    sudo cp -a "${fragment_backup}" "${fragment_path}"
  fi

  sudo systemctl daemon-reload
  sudo systemctl restart "${unit}" 2>/dev/null || true

  if systemctl is-active --quiet "${unit}"; then
    warn "تمت استعادة ${unit} إلى مسارها السابق."
  else
    warn "Rollback تم، لكن الخدمة لم تعد active. راجع journalctl."
  fi
}

cutover_service() {
  local unit="$1"
  local source="$2"
  local destination="$3"

  log "بدء تحويل ${unit}"
  log "المصدر: ${source}"
  log "الوجهة: ${destination}"

  [[ "${source}" == /opt/* ]] || {
    warn "المصدر ليس داخل /opt: ${source}"
    return 1
  }

  [[ -d "${source}" ]] || {
    warn "المصدر غير موجود: ${source}"
    return 1
  }

  [[ -d "${destination}" ]] || {
    warn "النسخة المرحلية غير موجودة: ${destination}"
    return 1
  }

  systemctl is-active --quiet "${unit}" || {
    warn "الخدمة ليست active: ${unit}"
    return 1
  }

  local fragment_path
  fragment_path="$(
    systemctl show "${unit}" \
      -p FragmentPath \
      --value
  )"

  [[ -f "${fragment_path}" ]] || {
    warn "ملف الخدمة غير موجود: ${fragment_path}"
    return 1
  }

  local safe_unit
  safe_unit="${unit//\//_}"

  local fragment_backup
  fragment_backup="${BACKUP_DIR}/${safe_unit}.service.bak"

  sudo cp -a "${fragment_path}" "${fragment_backup}"
  sudo chown "$(id -u):$(id -g)" "${fragment_backup}"

  systemctl cat "${unit}" \
    > "${AUDIT_DIR}/${safe_unit}.before.txt"

  systemctl show "${unit}" \
    -p MainPID \
    -p WorkingDirectory \
    -p ExecStart \
    -p Environment \
    > "${AUDIT_DIR}/${safe_unit}.before-runtime.txt"

  local old_pid
  old_pid="$(
    systemctl show "${unit}" \
      -p MainPID \
      --value
  )"

  local old_ports
  old_ports="$(get_ports_for_pid "${old_pid}")"

  printf '%s\n' "${old_ports}" \
    > "${AUDIT_DIR}/${safe_unit}.ports-before.txt"

  log "مزامنة أولية للخدمة وهي تعمل"

  sudo rsync -aHAX \
    --numeric-ids \
    --delete \
    --exclude='.git/' \
    --exclude='node_modules/.cache/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    "${source}/" \
    "${destination}/"

  log "إيقاف ${unit} للمزامنة النهائية"

  sudo systemctl stop "${unit}"

  if systemctl is-active --quiet "${unit}"; then
    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "تعذر إيقاف الخدمة."
    return 1
  fi

  log "تنفيذ المزامنة النهائية"

  sudo rsync -aHAX \
    --numeric-ids \
    --delete \
    --exclude='.git/' \
    --exclude='node_modules/.cache/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    "${source}/" \
    "${destination}/"

  local dry_run
  dry_run="$(
    sudo rsync -aHAXn \
      --numeric-ids \
      --delete \
      --itemize-changes \
      --exclude='.git/' \
      --exclude='node_modules/.cache/' \
      --exclude='__pycache__/' \
      --exclude='*.pyc' \
      "${source}/" \
      "${destination}/" ||
    true
  )"

  if [[ -n "${dry_run//[[:space:]]/}" ]]; then
    printf '%s\n' "${dry_run}" \
      > "${AUDIT_DIR}/${safe_unit}.final-diff.txt"

    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "فشل التطابق النهائي."
    return 1
  fi

  log "تحديث ملف systemd"

  local temporary_unit
  temporary_unit="$(mktemp)"

  sudo cat "${fragment_path}" |
    sed "s#${source}#${destination}#g" \
    > "${temporary_unit}"

  if cmp -s "${temporary_unit}" "${fragment_backup}"; then
    rm -f "${temporary_unit}"

    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "لم يتغير ملف systemd؛ قد يكون مسار /opt داخل drop-in."
    return 1
  fi

  sudo cp "${temporary_unit}" "${fragment_path}"
  sudo chmod --reference="${fragment_backup}" "${fragment_path}"
  sudo chown root:root "${fragment_path}"

  rm -f "${temporary_unit}"

  sudo systemctl daemon-reload

  log "تشغيل ${unit} من المشروع الرئيسي"

  if ! sudo systemctl restart "${unit}"; then
    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "فشل restart."
    return 1
  fi

  sleep 3

  if ! systemctl is-active --quiet "${unit}"; then
    sudo journalctl \
      -u "${unit}" \
      -n 100 \
      --no-pager \
      > "${AUDIT_DIR}/${safe_unit}.failed-journal.txt" ||
      true

    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "الخدمة ليست active بعد التحويل."
    return 1
  fi

  local new_working_directory
  new_working_directory="$(
    systemctl show "${unit}" \
      -p WorkingDirectory \
      --value
  )"

  local new_exec_start
  new_exec_start="$(
    systemctl show "${unit}" \
      -p ExecStart \
      --value
  )"

  if [[ "${new_working_directory}" == *"${source}"* ]] ||
     [[ "${new_exec_start}" == *"${source}"* ]]
  then
    rollback_service \
      "${unit}" \
      "${fragment_backup}" \
      "${fragment_path}"

    warn "systemd ما زال يشير إلى المصدر القديم."
    return 1
  fi

  local new_pid
  new_pid="$(
    systemctl show "${unit}" \
      -p MainPID \
      --value
  )"

  local new_ports
  new_ports="$(get_ports_for_pid "${new_pid}")"

  printf '%s\n' "${new_ports}" \
    > "${AUDIT_DIR}/${safe_unit}.ports-after.txt"

  if [[ -n "${old_ports}" ]]; then
    local missing_port=0

    while IFS= read -r port; do
      [[ -n "${port}" ]] || continue

      if ! grep -qx "${port}" \
        "${AUDIT_DIR}/${safe_unit}.ports-after.txt"
      then
        warn "المنفذ ${port} لم يعد ظاهرًا بعد التحويل."
        missing_port=1
      fi
    done <<< "${old_ports}"

    if [[ "${missing_port}" -eq 1 ]]; then
      rollback_service \
        "${unit}" \
        "${fragment_backup}" \
        "${fragment_path}"

      return 1
    fi
  fi

  systemctl cat "${unit}" \
    > "${AUDIT_DIR}/${safe_unit}.after.txt"

  systemctl show "${unit}" \
    -p MainPID \
    -p WorkingDirectory \
    -p ExecStart \
    -p ActiveState \
    -p SubState \
    > "${AUDIT_DIR}/${safe_unit}.after-runtime.txt"

  sudo journalctl \
    -u "${unit}" \
    -n 60 \
    --no-pager \
    > "${AUDIT_DIR}/${safe_unit}.journal.txt" ||
    true

  printf '%s\t%s\t%s\t%s\t%s\n' \
    "${unit}" \
    "${source}" \
    "${destination}" \
    "CUTOVER_OK" \
    "active-and-runtime-path-updated" \
    >> "${REPORT}"

  ok "تم تحويل ${unit} بنجاح."
}

MODE="${1:---all}"
REQUESTED_SERVICE="${2:-}"

mapfile -t READY_ROWS < <(
  awk -F '\t' '
    NR > 1 &&
    $5 == "copied" &&
    $6 == "rsync-dry-run-clean" {
      print $1 "\t" $2 "\t" $3
    }
  ' "${MANIFEST}"
)

[[ "${#READY_ROWS[@]}" -gt 0 ]] ||
  fail "لا توجد خدمات جاهزة للـCutover."

if [[ "${MODE}" == "--service" ]]; then
  [[ -n "${REQUESTED_SERVICE}" ]] ||
    fail "حدد اسم الخدمة بعد --service."

  found=0

  for row in "${READY_ROWS[@]}"; do
    IFS=$'\t' read -r unit source destination <<< "${row}"

    if [[ "${unit}" != "${REQUESTED_SERVICE}" ]]; then
      continue
    fi

    found=1

    if ! cutover_service \
      "${unit}" \
      "${source}" \
      "${destination}"
    then
      printf '%s\t%s\t%s\t%s\t%s\n' \
        "${unit}" \
        "${source}" \
        "${destination}" \
        "ROLLED_BACK" \
        "cutover-failed" \
        >> "${REPORT}"

      exit 1
    fi
  done

  [[ "${found}" -eq 1 ]] ||
    fail "الخدمة غير موجودة ضمن الخدمات الجاهزة."

elif [[ "${MODE}" == "--all" ]]; then
  for row in "${READY_ROWS[@]}"; do
    IFS=$'\t' read -r unit source destination <<< "${row}"

    if ! cutover_service \
      "${unit}" \
      "${source}" \
      "${destination}"
    then
      printf '%s\t%s\t%s\t%s\t%s\n' \
        "${unit}" \
        "${source}" \
        "${destination}" \
        "ROLLED_BACK" \
        "cutover-failed-stopped-batch" \
        >> "${REPORT}"

      fail "توقفت الدفعة عند ${unit}. لم تُحوّل الخدمات التالية."
    fi
  done
else
  fail "الاستخدام: --all أو --service اسم.service"
fi

echo
echo "============================================================"
echo "اكتملت عملية Cutover"
echo "============================================================"
echo
echo "التقرير:"
echo "${REPORT}"
echo
echo "السجل:"
echo "${LOG_FILE}"
echo
echo "الخدمات التي ما زالت تعمل من /opt:"
echo

while IFS= read -r unit; do
  [[ -n "${unit}" ]] || continue

  active="$(
    systemctl is-active "${unit}" 2>/dev/null ||
    true
  )"

  [[ "${active}" == "active" ]] || continue

  wd="$(
    systemctl show "${unit}" \
      -p WorkingDirectory \
      --value 2>/dev/null ||
    true
  )"

  exec_start="$(
    systemctl show "${unit}" \
      -p ExecStart \
      --value 2>/dev/null ||
    true
  )"

  if [[ "${wd}" == /opt/* ]] ||
     [[ "${exec_start}" == *"/opt/"* ]]
  then
    echo "${unit} | ${wd}"
  fi
done < <(
  systemctl list-unit-files \
    --type=service \
    --no-legend |
  awk '{print $1}'
)

echo "============================================================"
