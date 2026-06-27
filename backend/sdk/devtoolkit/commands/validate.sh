#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(ndsp_backend_root)"
TARGET="${1:-all}"

required_files=(service.yaml package.json README.md CHANGELOG.md main.cjs)
required_dirs=(tests contracts docs systemd config)

validate_one(){
  local svc="$1"
  local ok=1

  echo "VALIDATING=$svc"

  for f in "${required_files[@]}"; do
    if [ ! -f "$svc/$f" ]; then echo "MISSING_FILE=$svc/$f"; ok=0; fi
  done

  for d in "${required_dirs[@]}"; do
    if [ ! -d "$svc/$d" ]; then echo "MISSING_DIR=$svc/$d"; ok=0; fi
  done

  if [ -f "$svc/main.cjs" ]; then
    if ! grep -q "createNDSPService" "$svc/main.cjs"; then
      echo "FRAMEWORK_USAGE_MISSING=$svc/main.cjs"
      ok=0
    fi
  fi

  if [ "$ok" -eq 1 ]; then echo "VALIDATION_PASS=$svc"; return 0; fi
  echo "VALIDATION_FAIL=$svc"
  return 1
}

if [ "$TARGET" = "all" ]; then
  rc=0
  for svc in "$ROOT"/services/*; do
    [ -d "$svc" ] || continue
    validate_one "$svc" || rc=1
  done
  exit "$rc"
else
  validate_one "$TARGET"
fi
