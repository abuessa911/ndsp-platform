#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/empire-core-new}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

LATEST_AUDIT="$(
  ls -1dt "${PROJECT_ROOT}"/var/audits/opt-migration-* 2>/dev/null |
  head -n 1
)"

[[ -n "${LATEST_AUDIT}" ]] || {
  echo "لا يوجد تقرير opt-migration."
  exit 1
}

CANDIDATES_FILE="${LATEST_AUDIT}/DELETE_CANDIDATES.txt"
QUARANTINE_ROOT="/opt/.ndsp-quarantine-${TIMESTAMP}"
REPORT="${LATEST_AUDIT}/QUARANTINE_REPORT_${TIMESTAMP}.txt"

[[ -f "${CANDIDATES_FILE}" ]] || {
  echo "ملف المرشحين غير موجود: ${CANDIDATES_FILE}"
  exit 1
}

sudo mkdir -p "${QUARANTINE_ROOT}"

{
  echo "OPT Quarantine Report"
  echo "Generated: $(date --iso-8601=seconds)"
  echo "Quarantine: ${QUARANTINE_ROOT}"
  echo
} > "${REPORT}"

is_referenced() {
  local path="$1"

  sudo grep -RqsF "${path}" \
    /etc/systemd/system \
    /lib/systemd/system \
    /etc/cron.d \
    /etc/crontab \
    /etc/nginx \
    2>/dev/null
}

is_running() {
  local path="$1"

  ps auxww |
    grep -F "${path}" |
    grep -v grep \
    >/dev/null
}

has_open_files() {
  local path="$1"

  if command -v lsof >/dev/null 2>&1; then
    sudo lsof +D "${path}" 2>/dev/null |
      tail -n +2 |
      grep -q .
  else
    return 1
  fi
}

while IFS= read -r path; do
  [[ -n "${path}" ]] || continue

  echo "فحص: ${path}"

  if [[ ! -e "${path}" ]]; then
    echo "MISSING | ${path}" >> "${REPORT}"
    continue
  fi

  if is_referenced "${path}"; then
    echo "BLOCKED_REFERENCE | ${path}" >> "${REPORT}"
    echo "محظور بسبب مرجع في systemd/cron/nginx: ${path}"
    continue
  fi

  if is_running "${path}"; then
    echo "BLOCKED_PROCESS | ${path}" >> "${REPORT}"
    echo "محظور بسبب عملية نشطة: ${path}"
    continue
  fi

  if has_open_files "${path}"; then
    echo "BLOCKED_OPEN_FILES | ${path}" >> "${REPORT}"
    echo "محظور بسبب ملفات مفتوحة: ${path}"
    continue
  fi

  destination="${QUARANTINE_ROOT}/$(basename "${path}")"

  if [[ -e "${destination}" ]]; then
    destination="${destination}-${TIMESTAMP}"
  fi

  sudo mv "${path}" "${destination}"

  echo "QUARANTINED | ${path} -> ${destination}" >> "${REPORT}"
  echo "تم الحجر: ${path}"
done < "${CANDIDATES_FILE}"

sudo chown -R root:root "${QUARANTINE_ROOT}"
sudo chmod 700 "${QUARANTINE_ROOT}"

echo
echo "تمت العملية دون حذف."
echo "التقرير:"
echo "${REPORT}"
echo
echo "مجلد الحجر:"
echo "${QUARANTINE_ROOT}"
echo
echo "لا تحذف مجلد الحجر قبل فترة مراقبة."
