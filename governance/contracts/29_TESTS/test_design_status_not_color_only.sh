#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
python3 "$ROOT/28_VALIDATORS/validate_contracts.py" "$ROOT"
echo "PASS test_design_status_not_color_only.sh"
