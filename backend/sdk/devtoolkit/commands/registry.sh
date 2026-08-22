#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(ndsp_backend_root)"
REG="$ROOT/architecture/registry/SERVICE_REGISTRY_V2.md"

if [ ! -f "$REG" ]; then
  echo "SERVICE_REGISTRY_NOT_FOUND=$REG"
  exit 1
fi

cat "$REG"
