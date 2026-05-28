#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOMAIN="${1:-ndsp.app}"
DNS_SERVER="${DNS_SERVER:-1.1.1.1}"
STRICT_ENV="${STRICT_ENV:-0}"
FAILURES=0

ok()   { printf "\033[32m[PASS]\033[0m %s\n" "$1"; }
warn() { printf "\033[33m[WARN]\033[0m %s\n" "$1"; }
err()  { printf "\033[31m[FAIL]\033[0m %s\n" "$1"; FAILURES=$((FAILURES + 1)); }

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "Missing required command: $1"
    return 1
  fi
}

check_dns() {
  echo "== DNS Check =="
  need_cmd dig || return 0

  local raw ips
  raw="$(dig +short @"$DNS_SERVER" "$DOMAIN" 2>/dev/null || true)"
  ips="$(printf '%s\n' "$raw" | rg '^[0-9a-fA-F:.]+$' | tr '\n' ' ' | xargs || true)"

  if [[ -z "${ips}" ]]; then
    err "No DNS A/AAAA result for ${DOMAIN} via ${DNS_SERVER}."
    return 0
  fi

  ok "${DOMAIN} resolves via ${DNS_SERVER}: ${ips}"
}

check_env_templates() {
  echo "== Environment Readiness =="
  local required=(PAYMENT_PROVIDER PAYMENT_WEBHOOK_SECRET DISCOUNT_ENGINE_ENABLED PACKAGE_ADMIN_ENABLED SMTP_HOST SMTP_USER SMTP_PASS)
  local missing=0
  for v in "${required[@]}"; do
    if [[ -z "${!v-}" ]]; then
      warn "Env var not set in current shell: ${v}"
      missing=$((missing + 1))
    fi
  done
  [[ "$missing" -eq 0 ]] && ok "All priority env vars are available in current shell." || warn "${missing} env vars missing. Add them before production publish."

  if [[ "$missing" -eq 0 ]]; then
    ok "All priority env vars are available in current shell."
    return 0
  fi

  warn "${missing} env vars missing. Add them before production publish."
  if [[ "$STRICT_ENV" == "1" ]]; then
    err "STRICT_ENV=1 and required env vars are missing."
  fi
}

check_priority_files() {
  echo "== Priority Feature Footprint =="
  local patterns=("payment|checkout|invoice|subscription" "discount|coupon|promo" "package|plan|pricing")
  for p in "${patterns[@]}"; do
    rg -n -i "$p" "$ROOT_DIR" >/dev/null 2>&1 && ok "Code footprint found for pattern: ${p}" || warn "No clear code footprint found for pattern: ${p}"
  done
}

check_security_basics() {
  echo "== Security Basics =="
  local rules=("rate\\s*limit|ratelimit" "cors" "admin" "audit" "backup")
  for r in "${rules[@]}"; do
    rg -n -i "$r" "$ROOT_DIR" >/dev/null 2>&1 && ok "Security signal exists: ${r}" || warn "Security signal not found: ${r}"
  done
}

print_manual_release_checklist() {
  echo "== Manual Release Checklist (Top Priority) =="
  cat <<'TXT'
1) الدفع والاشتراكات: ربط البوابة + تفعيل تلقائي + فواتير + أكواد خصم.
2) إدارة الباقات: تعديل السعر/المزايا/الطبقات/مدة التجربة من لوحة الإدارة.
3) إدارة الأصول: تفعيل/إيقاف BTC/ETH/XRP وباقي الأسواق من لوحة الإدارة.
4) البريد: رسائل الترحيب + قبول/رفض الترقية + اعتماد الخصم + نهاية التجربة.
5) الأمان والإنتاج: Rate limit قوي + حماية admin + CORS + نسخ احتياطي + مراقبة logs.
6) اختبارات E2E: التسجيل/الدخول/الدفع/الترقية/الاستبيان/الخصم/لوحة الإدارة.
TXT
}

main() {
  echo "NDSP prelaunch gate for domain: ${DOMAIN}"
  echo "Repository: ${ROOT_DIR}"
  echo "Options: STRICT_ENV=${STRICT_ENV} DNS_SERVER=${DNS_SERVER}"
  echo

  check_dns
  check_env_templates
  check_priority_files
  check_security_basics
  print_manual_release_checklist

  echo
  if [[ "$FAILURES" -gt 0 ]]; then
    err "Prelaunch gate finished with ${FAILURES} blocking failure(s)."
    return 1
  fi

  ok "Prelaunch gate finished with no blocking failures."
  echo "Address WARN items before real production launch."
}

main "$@"
