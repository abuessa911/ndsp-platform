#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
failed=0
for t in "$ROOT"/29_TESTS/test_*.sh; do
  [[ "$(basename "$t")" == "test_all.sh" ]] && continue
  bash "$t" || failed=1
done
exit "$failed"
