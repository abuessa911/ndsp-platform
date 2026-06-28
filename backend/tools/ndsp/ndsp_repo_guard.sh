#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

FAILS=0
WARNS=0

fail(){ echo "FAIL=$*"; FAILS=$((FAILS+1)); }
warn(){ echo "WARN=$*"; WARNS=$((WARNS+1)); }
pass(){ echo "PASS=$*"; }

echo "# NDSP Repo Guard"
echo "ROOT=$ROOT"
echo "HEAD=$(git log -1 --oneline)"
echo "BRANCH=$(git rev-parse --abbrev-ref HEAD)"

echo "== 1) TRACKED RUNTIME / SECRET ARTIFACTS =="

BAD_TRACKED=""
while IFS= read -r f; do
  case "$f" in
    .env|*/.env|*.env.local|*/.env.local|*.env.production|*/.env.production|*.env.development|*/.env.development|*.env.staging|*/.env.staging)
      BAD_TRACKED+="$f"$'\n'
      ;;
    backend/runtime/*|runtime/*)
      BAD_TRACKED+="$f"$'\n'
      ;;
    node_modules/*|*/node_modules/*|venv/*|*/venv/*|.venv/*|*/.venv/*|__pycache__/*|*/__pycache__/*)
      BAD_TRACKED+="$f"$'\n'
      ;;
    *core-services.env|*.pem|*.key|*.p12)
      BAD_TRACKED+="$f"$'\n'
      ;;
  esac
done < <(git ls-files)

BAD_TRACKED="$(printf "%s" "$BAD_TRACKED" | sed '/^$/d' || true)"

if [ -n "$BAD_TRACKED" ]; then
  echo "$BAD_TRACKED"
  fail "TRACKED_RUNTIME_OR_SECRET_FILES"
else
  pass "NO_TRACKED_RUNTIME_OR_SECRET_FILES"
fi

echo "== 2) ENV EXAMPLE FILES =="
ENV_EXAMPLES="$(git ls-files | grep -E '(^|/).*\.env(\..*)?\.example$|(^|/)\.env\.example$' || true)"
if [ -n "$ENV_EXAMPLES" ]; then
  echo "$ENV_EXAMPLES"
  pass "ENV_EXAMPLES_ALLOWED"
else
  warn "NO_ENV_EXAMPLE_FILES_FOUND"
fi

echo "== 3) SERVICE YAML CHECK =="
if [ ! -d backend/services ]; then
  fail "backend/services_NOT_FOUND"
else
  mapfile -t SERVICE_FILES < <(find backend/services -mindepth 2 -maxdepth 2 -name service.yaml | sort)
  echo "SERVICE_COUNT=${#SERVICE_FILES[@]}"
  if [ "${#SERVICE_FILES[@]}" -eq 0 ]; then
    fail "NO_SERVICE_YAML_FILES"
  fi

  IDS_TMP="$(mktemp)"
  PORTS_TMP="$(mktemp)"

  for f in "${SERVICE_FILES[@]}"; do
    SID="$(sed -n 's/^service_id:[[:space:]]*//p' "$f" | head -n 1 | tr -d '\r')"
    PORT="$(sed -n 's/^port:[[:space:]]*//p' "$f" | head -n 1 | tr -d '\r')"

    echo "${SID:-MISSING_ID} file=$f port=${PORT:-MISSING_PORT}"
    echo "${SID:-MISSING_ID}" >> "$IDS_TMP"
    echo "${PORT:-MISSING_PORT}" >> "$PORTS_TMP"

    if [ -z "${SID:-}" ]; then
      fail "MISSING_SERVICE_ID_IN_$f"
    fi

    if [ -z "${PORT:-}" ]; then
      fail "MISSING_PORT_IN_$f"
    fi
  done

  DUP_IDS="$(sort "$IDS_TMP" | uniq -d | grep -v '^MISSING_ID$' || true)"
  DUP_PORTS="$(sort "$PORTS_TMP" | uniq -d | grep -v '^MISSING_PORT$' || true)"

  if [ -n "$DUP_IDS" ]; then
    echo "$DUP_IDS"
    fail "DUPLICATE_SERVICE_IDS"
  else
    pass "NO_DUPLICATE_SERVICE_IDS"
  fi

  if [ -n "$DUP_PORTS" ]; then
    echo "$DUP_PORTS"
    fail "DUPLICATE_SERVICE_PORTS"
  else
    pass "NO_DUPLICATE_SERVICE_PORTS"
  fi

  rm -f "$IDS_TMP" "$PORTS_TMP"
fi

echo "== 4) LARGE TRACKED FILES =="
LARGE_FOUND=0

while IFS= read -r f; do
  [ -f "$f" ] || continue
  size="$(wc -c < "$f" 2>/dev/null || echo 0)"
  if [ "$size" -gt 10485760 ]; then
    echo "LARGE_FILE=$size $f"
    LARGE_FOUND=1
  fi
done < <(git ls-files)

if [ "$LARGE_FOUND" -eq 1 ]; then
  fail "LARGE_TRACKED_FILES_OVER_10MB"
else
  pass "NO_LARGE_TRACKED_FILES_OVER_10MB"
fi

echo "== 5) LITERAL SECRET PATTERN SCAN =="
SECRET_HITS="$(git grep -InE 'AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{20,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----' -- . ':!backend/architecture/reports' ':!*.md' || true)"

if [ -n "$SECRET_HITS" ]; then
  echo "$SECRET_HITS"
  fail "LITERAL_SECRET_PATTERN_FOUND"
else
  pass "NO_LITERAL_SECRET_PATTERN_FOUND"
fi

echo "== 6) SUMMARY =="
echo "FAIL_COUNT=$FAILS"
echo "WARN_COUNT=$WARNS"

if [ "$FAILS" -eq 0 ]; then
  echo "NDSP_REPO_GUARD=PASS"
  exit 0
else
  echo "NDSP_REPO_GUARD=FAIL"
  exit 1
fi
