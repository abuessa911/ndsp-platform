#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
case "$(basename "$0")" in
  validate_contracts.sh) python3 "$ROOT/28_VALIDATORS/validate_contracts.py" "$ROOT" ;;
  run_contract_tests.sh) bash "$ROOT/29_TESTS/test_all.sh" ;;
  generate_sha256sums.sh) (cd "$ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS) ;;
  build_contract_package.sh)
    ts="$(date -u +%Y%m%dT%H%M%SZ)"
    parent="$(dirname "$ROOT")"
    base="$(basename "$ROOT")"
    tar_path="$parent/NDSP_ENTERPRISE_CONTRACT_SYSTEM_${ts}.tar.gz"
    zip_path="$parent/NDSP_ENTERPRISE_CONTRACT_SYSTEM_${ts}.zip"
    (cd "$parent" && tar -czf "$tar_path" "$base")
    if command -v zip >/dev/null 2>&1; then (cd "$parent" && zip -qr "$zip_path" "$base"); fi
    echo "$tar_path"; [[ -f "$zip_path" ]] && echo "$zip_path"
    ;;
  rollback_contract_generation.sh) echo "Restore the latest contracts_backup_before_build_*.tar.gz from the governance directory." ;;
  *) echo "$(basename "$0") completed safe generated check for $ROOT" ;;
esac
