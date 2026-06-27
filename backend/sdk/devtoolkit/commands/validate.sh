#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(ndsp_backend_root)"
TARGET="${1:-all}"

required_files=(service.yaml package.json README.md CHANGELOG.md main.cjs)
required_files_legacy=(service.yaml README.md CHANGELOG.md main.cjs)
required_dirs=(tests contracts docs systemd config)

validate_one(){
  local svc="$1"
  local ok=1
  local yaml="$svc/service.yaml"
  local framework=""

  echo "VALIDATING=$svc"

  if [ -f "$yaml" ]; then
    framework="$(read_yaml_value "$yaml" framework || true)"
  fi

  if [ "$framework" = "LEGACY" ]; then
    echo "LEGACY_SERVICE=YES"
    for f in "${required_files_legacy[@]}"; do
      if [ ! -f "$svc/$f" ]; then echo "MISSING_FILE=$svc/$f"; ok=0; fi
    done
  else
    for f in "${required_files[@]}"; do
      if [ ! -f "$svc/$f" ]; then echo "MISSING_FILE=$svc/$f"; ok=0; fi
    done
  fi

  for d in "${required_dirs[@]}"; do
    if [ ! -d "$svc/$d" ]; then echo "MISSING_DIR=$svc/$d"; ok=0; fi
  done

  if [ "$framework" = "LEGACY" ]; then
    echo "FRAMEWORK_CHECK=SKIPPED_LEGACY_PENDING_MIGRATION"
  else
    if [ -f "$svc/main.cjs" ]; then
      if ! grep -q "createNDSPService" "$svc/main.cjs"; then
        echo "FRAMEWORK_USAGE_MISSING=$svc/main.cjs"
        ok=0
      fi
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
