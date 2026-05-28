cat > /tmp/ndsp_trial_final_readiness_check.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

APP_URL="${APP_URL:-https://ndsp.app}"
PROJECT_ROOT="${PROJECT_ROOT:-/home/nawaf511/empire-core-new}"
AUTH_DIR="${AUTH_DIR:-$PROJECT_ROOT/backend/auth_api}"
ADMIN_EMAIL="${ADMIN_EMAIL:-ndsp.app@gmail.com}"

REPORT_DIR="${REPORT_DIR:-/home/nawaf511/ndsp_launch_reports}"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORT_DIR/NDSP_TRIAL_FINAL_READINESS_CHECK_${TS}.md"
TMP_DIR="/tmp/ndsp_trial_check_${TS}"

APPLY_NGINX_FIX="${APPLY_NGINX_FIX:-0}"
RUN_REGISTRATION_TEST="${RUN_REGISTRATION_TEST:-0}"
RUN_IP_LOCK_TEST="${RUN_IP_LOCK_TEST:-0}"

mkdir -p "$REPORT_DIR" "$TMP_DIR"

STATUS_OK=1

log() {
  echo "$*" | tee -a "$REPORT"
}

ok() {
  log "✅ $*"
}

warn() {
  log "⚠️ $*"
}

bad() {
  STATUS_OK=0
  log "❌ $*"
}

section() {
  log ""
  log "## $*"
}

need_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "COMMAND_OK=$1"
  else
    bad "COMMAND_MISSING=$1"
  fi
}

curl_status() {
  local method="$1"
  local url="$2"
  local out="$3"
  local code

  if [[ "$method" == "GET" ]]; then
    code="$(curl -k -sS -L --max-time 20 -o "$out" -w "%{http_code}" "$url" || true)"
  else
    code="$(curl -k -sS -L --max-time 20 -X "$method" -H "Content-Type: application/json" -d '{}' -o "$out" -w "%{http_code}" "$url" || true)"
  fi

  echo "$code"
}

svc_check() {
  local svc="$1"
  if systemctl list-unit-files | awk '{print $1}' | grep -qx "${svc}.service"; then
    if systemctl is-active --quiet "$svc"; then
      ok "SERVICE_ACTIVE=$svc"
    else
      bad "SERVICE_INACTIVE=$svc"
      systemctl --no-pager --full status "$svc" | tail -n 30 | sed 's/^/    /' | tee -a "$REPORT" >/dev/null || true
    fi
  else
    warn "SERVICE_UNIT_NOT_FOUND=$svc"
  fi
}

find_database_url() {
  local files=(
    "$AUTH_DIR/.env"
    "$PROJECT_ROOT/backend/.env"
    "$PROJECT_ROOT/.env"
  )

  for f in "${files[@]}"; do
    if [[ -f "$f" ]] && grep -qE '^DATABASE_URL=' "$f"; then
      grep -E '^DATABASE_URL=' "$f" | tail -1 | sed 's/^DATABASE_URL=//' | sed 's/^"//;s/"$//' | sed "s/^'//;s/'$//"
      return 0
    fi
  done

  return 1
}

psql_scalar() {
  local sql="$1"
  if [[ -n "${DATABASE_URL_VALUE:-}" ]]; then
    PGPASSWORD="${PGPASSWORD:-}" psql "$DATABASE_URL_VALUE" -Atqc "$sql" 2>/dev/null || true
  else
    sudo -u postgres psql -Atqc "$sql" 2>/dev/null || true
  fi
}

table_exists() {
  local tbl="$1"
  [[ "$(psql_scalar "SELECT CASE WHEN to_regclass('public.${tbl}') IS NULL THEN '0' ELSE '1' END;")" == "1" ]]
}

has_col() {
  local tbl="$1"
  local col="$2"
  [[ "$(psql_scalar "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='public' AND table_name='${tbl}' AND column_name='${col}';")" == "1" ]]
}

safe_count() {
  local sql="$1"
  local result
  result="$(psql_scalar "$sql")"
  if [[ "$result" =~ ^[0-9]+$ ]]; then
    echo "$result"
  else
    echo "ERR"
  fi
}

nginx_duplicate_report() {
  nginx -T 2>&1 | grep -iE 'conflicting server name|duplicate|server_names_hash' || true
}

try_fix_nginx_duplicate_server_names() {
  section "Nginx Duplicate server_name Fix"

  if [[ "$APPLY_NGINX_FIX" != "1" ]]; then
    warn "APPLY_NGINX_FIX=0 لذلك لن يتم تعديل Nginx. سيتم الفحص فقط."
    return 0
  fi

  local backup_dir="/root/nginx_ndsp_duplicate_fix_${TS}"
  mkdir -p "$backup_dir"

  ok "NGINX_BACKUP_DIR=$backup_dir"

  cp -a /etc/nginx "$backup_dir/nginx_backup"

  mapfile -t matches < <(
    grep -RInE '^[[:space:]]*server_name[[:space:]]+.*(ndsp\.app|www\.ndsp\.app).*;' /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null || true
  )

  if (( ${#matches[@]} <= 1 )); then
    ok "NGINX_DUPLICATE_SERVER_NAME_LINES_NOT_FOUND_OR_SINGLE"
    return 0
  fi

  ok "NGINX_SERVER_NAME_MATCHES=${#matches[@]}"
  log "سيتم إبقاء أول server_name وتعليق الباقي ثم اختبار nginx -t."

  local first_seen=0
  local item file line content

  for item in "${matches[@]}"; do
    file="$(echo "$item" | cut -d: -f1)"
    line="$(echo "$item" | cut -d: -f2)"
    content="$(echo "$item" | cut -d: -f3-)"

    if [[ "$first_seen" == "0" ]]; then
      first_seen=1
      ok "NGINX_KEEP=${file}:${line}:${content}"
      continue
    fi

    ok "NGINX_COMMENT_DUPLICATE=${file}:${line}:${content}"
    sed -i "${line}s/^[[:space:]]*server_name/# NDSP_DUPLICATE_SERVER_NAME_DISABLED server_name/" "$file"
  done

  if nginx -t >/tmp/nginx_test_${TS}.log 2>&1; then
    ok "NGINX_CONFIG_OK_AFTER_DUPLICATE_FIX=True"
    systemctl reload nginx
    ok "NGINX_RELOAD_OK=True"
  else
    bad "NGINX_CONFIG_FAILED_AFTER_FIX=True"
    cat /tmp/nginx_test_${TS}.log | sed 's/^/    /' | tee -a "$REPORT" >/dev/null
    rm -rf /etc/nginx
    cp -a "$backup_dir/nginx_backup" /etc/nginx
    nginx -t >/dev/null 2>&1 && systemctl reload nginx || true
    bad "NGINX_ROLLBACK_DONE=True"
  fi
}

post_json_try() {
  local endpoint="$1"
  local payload="$2"
  local out="$3"
  curl -k -sS -L --max-time 25 \
    -X POST "$APP_URL$endpoint" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    -o "$out" \
    -w "%{http_code}" || true
}

run_registration_test() {
  section "Optional Registration Test"

  if [[ "$RUN_REGISTRATION_TEST" != "1" ]]; then
    warn "RUN_REGISTRATION_TEST=0 لذلك لن يتم إنشاء مستخدم تجريبي."
    warn "لتفعيل اختبار التسجيل: RUN_REGISTRATION_TEST=1 bash /tmp/ndsp_trial_final_readiness_check.sh"
    return 0
  fi

  local email="ndsp.trial.${TS}@example.com"
  local pass="NDSP_Test_${TS}_Strong!"
  local payload
  payload="$(cat <<JSON
{"name":"NDSP Trial Test","email":"$email","password":"$pass"}
JSON
)"

  local endpoints=(
    "/api/auth/register"
    "/api/register"
    "/auth/register"
    "/register"
  )

  local success_endpoint=""
  local code=""
  local out="$TMP_DIR/register_response.json"

  for ep in "${endpoints[@]}"; do
    code="$(post_json_try "$ep" "$payload" "$out")"
    log "REGISTER_TRY_ENDPOINT=$ep STATUS_CODE=$code"
    if [[ "$code" == "200" || "$code" == "201" ]]; then
      success_endpoint="$ep"
      break
    fi
  done

  if [[ -z "$success_endpoint" ]]; then
    bad "REGISTRATION_TEST_FAILED=True"
    warn "قد يكون مسار التسجيل مختلف أو التسجيل مقفل أو يحتاج حقول إضافية."
    [[ -s "$out" ]] && head -c 1200 "$out" | tee -a "$REPORT" >/dev/null || true
    return 0
  fi

  ok "REGISTRATION_TEST_OK=True"
  ok "REGISTRATION_ENDPOINT=$success_endpoint"

  if grep -Eiq 'trial|16|تجربة' "$out"; then
    ok "NEW_USER_TRIAL_HINT_FOUND=True"
  else
    warn "NEW_USER_TRIAL_HINT_NOT_FOUND_IN_REGISTER_RESPONSE=True"
  fi

  local dup_out="$TMP_DIR/register_duplicate_response.json"
  local dup_code
  dup_code="$(post_json_try "$success_endpoint" "$payload" "$dup_out")"
  log "DUPLICATE_EMAIL_REGISTER_STATUS_CODE=$dup_code"

  if [[ "$dup_code" == "400" || "$dup_code" == "401" || "$dup_code" == "403" || "$dup_code" == "409" || "$dup_code" == "429" ]]; then
    ok "DUPLICATE_EMAIL_BLOCK_OK=True"
  else
    warn "DUPLICATE_EMAIL_BLOCK_UNCLEAR=True"
  fi

  if [[ "$RUN_IP_LOCK_TEST" == "1" ]]; then
    local email2="ndsp.trial.ip.${TS}@example.com"
    local payload2
    payload2="$(cat <<JSON
{"name":"NDSP IP Lock Test","email":"$email2","password":"$pass"}
JSON
)"
    local ip_out="$TMP_DIR/register_same_ip_response.json"
    local ip_code
    ip_code="$(post_json_try "$success_endpoint" "$payload2" "$ip_out")"
    log "SAME_IP_SECOND_ACCOUNT_STATUS_CODE=$ip_code"

    if [[ "$ip_code" == "403" || "$ip_code" == "409" || "$ip_code" == "429" ]]; then
      ok "SAME_IP_SECOND_ACCOUNT_BLOCK_OK=True"
    else
      warn "SAME_IP_SECOND_ACCOUNT_BLOCK_UNCLEAR=True"
    fi
  else
    warn "RUN_IP_LOCK_TEST=0 لم يتم اختبار منع التسجيل الثاني من نفس IP حتى لا يتم قفل تجربة الجهاز."
  fi
}

{
  log "# NDSP Trial Final Readiness Check"
  log "- DATE=$(date -Is)"
  log "- APP_URL=$APP_URL"
  log "- PROJECT_ROOT=$PROJECT_ROOT"
  log "- AUTH_DIR=$AUTH_DIR"
  log "- ADMIN_EMAIL=$ADMIN_EMAIL"
  log "- APPLY_NGINX_FIX=$APPLY_NGINX_FIX"
  log "- RUN_REGISTRATION_TEST=$RUN_REGISTRATION_TEST"
  log "- RUN_IP_LOCK_TEST=$RUN_IP_LOCK_TEST"
} >/dev/null

section "Preconditions"
need_cmd curl
need_cmd grep
need_cmd awk
need_cmd sed
need_cmd nginx
need_cmd systemctl
need_cmd psql

if [[ -d "$PROJECT_ROOT" ]]; then
  ok "PROJECT_ROOT_EXISTS=True"
else
  bad "PROJECT_ROOT_EXISTS=False"
fi

if [[ -d "$AUTH_DIR" ]]; then
  ok "AUTH_DIR_EXISTS=True"
else
  warn "AUTH_DIR_EXISTS=False"
fi

section "Services"
svc_check "ndsp-auth-api"
svc_check "nginx"
svc_check "postgresql"

section "Nginx"
if nginx -t >/tmp/nginx_test_${TS}.log 2>&1; then
  ok "NGINX_CONFIG_OK=True"
else
  bad "NGINX_CONFIG_OK=False"
  cat /tmp/nginx_test_${TS}.log | sed 's/^/    /' | tee -a "$REPORT" >/dev/null
fi

DUP_WARN="$(nginx_duplicate_report)"
if [[ -n "$DUP_WARN" ]]; then
  warn "NGINX_DUPLICATE_OR_WARNING_FOUND=True"
  echo "$DUP_WARN" | sed 's/^/    /' | tee -a "$REPORT" >/dev/null
else
  ok "NGINX_DUPLICATE_OR_WARNING_FOUND=False"
fi

try_fix_nginx_duplicate_server_names

section "Public HTTP Checks"
HOME_OUT="$TMP_DIR/home.html"
HOME_CODE="$(curl_status GET "$APP_URL" "$HOME_OUT")"
log "HOME_HTTP_CODE=$HOME_CODE"
if [[ "$HOME_CODE" == "200" ]]; then ok "HOME_HTTP_OK=True"; else bad "HOME_HTTP_OK=False"; fi

CHECKOUT_OUT="$TMP_DIR/checkout.html"
CHECKOUT_CODE="$(curl_status GET "$APP_URL/#/checkout-nowpayments" "$CHECKOUT_OUT")"
log "CHECKOUT_HASH_HTTP_CODE=$CHECKOUT_CODE"
if [[ "$CHECKOUT_CODE" == "200" ]]; then ok "CHECKOUT_PAGE_SHELL_OK=True"; else bad "CHECKOUT_PAGE_SHELL_OK=False"; fi

section "API Checks"
for endpoint in "/api/webhooks/nowpayments" "/api/nowpayments/health" "/api/plans"; do
  out="$TMP_DIR/api_$(echo "$endpoint" | tr '/?' '__').json"
  code="$(curl_status GET "$APP_URL$endpoint" "$out")"
  log "GET $endpoint HTTP_CODE=$code"
  if [[ "$code" == "200" ]]; then
    ok "API_GET_OK=$endpoint"
  else
    bad "API_GET_FAILED=$endpoint"
    [[ -s "$out" ]] && head -c 800 "$out" | tee -a "$REPORT" >/dev/null || true
  fi
done

IPN_POST_OUT="$TMP_DIR/ipn_post.json"
IPN_POST_CODE="$(curl_status POST "$APP_URL/api/webhooks/nowpayments" "$IPN_POST_OUT")"
log "POST /api/webhooks/nowpayments WITHOUT_SIGNATURE HTTP_CODE=$IPN_POST_CODE"
if grep -Eiq 'INVALID_IPN_SIGNATURE|signature' "$IPN_POST_OUT"; then
  ok "NOWPAYMENTS_INVALID_SIGNATURE_PROTECTION_OK=True"
else
  warn "NOWPAYMENTS_INVALID_SIGNATURE_PROTECTION_UNCLEAR=True"
  [[ -s "$IPN_POST_OUT" ]] && head -c 1000 "$IPN_POST_OUT" | tee -a "$REPORT" >/dev/null || true
fi

section "Trial Welcome Message Search"
if grep -Eiq '16|تجربة|trial|استبيان|مقاعد|seats' "$HOME_OUT"; then
  ok "TRIAL_MESSAGE_HINT_FOUND_IN_HOME_HTML=True"
else
  warn "TRIAL_MESSAGE_HINT_NOT_FOUND_IN_HOME_HTML=True"
fi

TRIAL_SEARCH_OUT="$TMP_DIR/trial_source_search.txt"
grep -RInE '16[[:space:]]*(يوم|day|days)|تجربة|trial|استبيان|survey|مقاعد|seats' \
  "$PROJECT_ROOT" \
  --exclude-dir=node_modules \
  --exclude-dir=.next \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude-dir=.git \
  --include='*.js' \
  --include='*.jsx' \
  --include='*.ts' \
  --include='*.tsx' \
  --include='*.html' \
  --include='*.json' \
  2>/dev/null | head -80 > "$TRIAL_SEARCH_OUT" || true

if [[ -s "$TRIAL_SEARCH_OUT" ]]; then
  ok "TRIAL_MESSAGE_HINT_FOUND_IN_SOURCE=True"
  sed 's/^/    /' "$TRIAL_SEARCH_OUT" | tee -a "$REPORT" >/dev/null
else
  warn "TRIAL_MESSAGE_HINT_NOT_FOUND_IN_SOURCE=True"
fi

section "Database Checks"
DATABASE_URL_VALUE="$(find_database_url || true)"

if [[ -n "${DATABASE_URL_VALUE:-}" ]]; then
  ok "DATABASE_URL_FOUND=True"
else
  warn "DATABASE_URL_FOUND=False - سيتم استخدام sudo -u postgres psql إن أمكن"
fi

DB_PING="$(psql_scalar "SELECT 1;")"
if [[ "$DB_PING" == "1" ]]; then
  ok "POSTGRES_QUERY_OK=True"
else
  bad "POSTGRES_QUERY_OK=False"
fi

TABLES=(
  users
  ndsp_plans
  ndsp_layers
  ndsp_plan_layers
  ndsp_assets
  ndsp_settings
  ndsp_audit_log
  ndsp_nowpayments_payments
  ndsp_subscriptions
  ndsp_registration_locks
)

for tbl in "${TABLES[@]}"; do
  if table_exists "$tbl"; then
    ok "DB_TABLE_EXISTS=$tbl"
  else
    bad "DB_TABLE_MISSING=$tbl"
  fi
done

if table_exists "users"; then
  ADMIN_COUNT="$(safe_count "SELECT COUNT(*) FROM users WHERE lower(email)=lower('${ADMIN_EMAIL}') AND lower(role)='admin';")"
  OTHER_ADMIN_COUNT="$(safe_count "SELECT COUNT(*) FROM users WHERE lower(role)='admin' AND lower(email)<>lower('${ADMIN_EMAIL}');")"

  log "ADMIN_REQUIRED_COUNT=$ADMIN_COUNT"
  log "OTHER_ADMIN_COUNT=$OTHER_ADMIN_COUNT"

  if [[ "$ADMIN_COUNT" == "1" ]]; then ok "REQUIRED_ADMIN_OK=True"; else bad "REQUIRED_ADMIN_OK=False"; fi
  if [[ "$OTHER_ADMIN_COUNT" == "0" ]]; then ok "ONLY_REQUIRED_ADMIN_OK=True"; else warn "OTHER_ADMINS_EXIST=True"; fi
fi

if table_exists "ndsp_plans"; then
  PLAN_WHERE=""
  if has_col ndsp_plans name; then PLAN_WHERE="${PLAN_WHERE}lower(coalesce(name,''))='trial' OR "; fi
  if has_col ndsp_plans slug; then PLAN_WHERE="${PLAN_WHERE}lower(coalesce(slug,''))='trial' OR "; fi
  if has_col ndsp_plans code; then PLAN_WHERE="${PLAN_WHERE}lower(coalesce(code,''))='trial' OR "; fi
  PLAN_WHERE="${PLAN_WHERE}false"

  TRIAL_COUNT="$(safe_count "SELECT COUNT(*) FROM ndsp_plans WHERE ${PLAN_WHERE};")"
  log "TRIAL_PLAN_COUNT=$TRIAL_COUNT"

  if [[ "$TRIAL_COUNT" =~ ^[1-9][0-9]*$ ]]; then
    ok "TRIAL_PLAN_EXISTS=True"
  else
    bad "TRIAL_PLAN_EXISTS=False"
  fi

  if has_col ndsp_plans trial_days; then
    TRIAL_16_COUNT="$(safe_count "SELECT COUNT(*) FROM ndsp_plans WHERE (${PLAN_WHERE}) AND trial_days=16;")"
    log "TRIAL_16_DAYS_COUNT=$TRIAL_16_COUNT"
    if [[ "$TRIAL_16_COUNT" =~ ^[1-9][0-9]*$ ]]; then ok "TRIAL_16_DAYS_OK=True"; else bad "TRIAL_16_DAYS_OK=False"; fi
  else
    warn "TRIAL_DAYS_COLUMN_NOT_FOUND_IN_ndsp_plans"
  fi
fi

if table_exists "ndsp_assets"; then
  for asset in BTC ETH XRP SOL GOLD NASDAQ; do
    if has_col ndsp_assets symbol; then
      C="$(safe_count "SELECT COUNT(*) FROM ndsp_assets WHERE upper(symbol)=upper('${asset}');")"
    elif has_col ndsp_assets code; then
      C="$(safe_count "SELECT COUNT(*) FROM ndsp_assets WHERE upper(code)=upper('${asset}');")"
    elif has_col ndsp_assets name; then
      C="$(safe_count "SELECT COUNT(*) FROM ndsp_assets WHERE upper(name)=upper('${asset}');")"
    else
      C="ERR"
    fi

    log "ASSET_${asset}_COUNT=$C"
    if [[ "$C" =~ ^[1-9][0-9]*$ ]]; then ok "ASSET_EXISTS=$asset"; else warn "ASSET_NOT_CONFIRMED=$asset"; fi
  done
fi

section "NOWPayments Secrets Presence Check"
SECRET_FOUND_API=0
SECRET_FOUND_IPN=0

for f in "$AUTH_DIR/.env" "$PROJECT_ROOT/backend/.env" "$PROJECT_ROOT/.env"; do
  [[ -f "$f" ]] || continue
  if grep -qE '^NOWPAYMENTS_API_KEY=' "$f"; then SECRET_FOUND_API=1; fi
  if grep -qE '^NOWPAYMENTS_IPN_SECRET=' "$f"; then SECRET_FOUND_IPN=1; fi
done

if [[ "$SECRET_FOUND_API" == "1" ]]; then ok "NOWPAYMENTS_API_KEY_PRESENT=True"; else warn "NOWPAYMENTS_API_KEY_PRESENT=False"; fi
if [[ "$SECRET_FOUND_IPN" == "1" ]]; then ok "NOWPAYMENTS_IPN_SECRET_PRESENT=True"; else warn "NOWPAYMENTS_IPN_SECRET_PRESENT=False"; fi

run_registration_test

section "Manual Browser Checks Required"
log "- افتح Incognito: $APP_URL"
log "- تأكد أن رسالة تجربة 16 يوم تظهر فور فتح الموقع."
log "- سجّل مستخدم جديد يدويًا إذا لم تفعل RUN_REGISTRATION_TEST."
log "- تأكد من دخوله على trial لمدة 16 يوم."
log "- افتح لوحة الأدمن بحساب: $ADMIN_EMAIL"
log "- افحص الصفحات:"
log "  - $APP_URL/#/admin-users"
log "  - $APP_URL/#/admin-plans"
log "  - $APP_URL/#/admin-layers"
log "  - $APP_URL/#/admin-assets"
log "  - $APP_URL/#/admin-settings"
log "  - $APP_URL/#/admin-audit"

section "Final Status"
if [[ "$STATUS_OK" == "1" ]]; then
  ok "ASSERT_OK=True"
  ok "FINAL_STATUS=NDSP_TRIAL_READY_FOR_MANUAL_BROWSER_QA"
else
  bad "ASSERT_OK=False"
  bad "FINAL_STATUS=NDSP_TRIAL_NEEDS_FIXES_BEFORE_LAUNCH"
fi

ok "REPORT=$REPORT"

echo ""
echo "============================================================"
echo "REPORT: $REPORT"
echo "============================================================"
grep -E 'FINAL_STATUS|ASSERT_OK|REPORT|ERROR|FAILED|MISSING|WARNING|NGINX_DUPLICATE|TRIAL_16|REQUIRED_ADMIN|NOWPAYMENTS|HOME_HTTP|API_GET|REGISTRATION' "$REPORT" || true
SH

chmod +x /tmp/ndsp_trial_final_readiness_check.sh

sudo bash /tmp/ndsp_trial_final_readiness_check.sh
