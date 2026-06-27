#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(ndsp_backend_root)"
echo "NDSP_DOCTOR=START"
echo "ROOT=$ROOT"

[ -f "$ROOT/framework/index.cjs" ] && echo "ENG001=OK" || echo "ENG001=MISSING"
[ -d "$ROOT/services" ] && echo "SERVICES_DIR=OK" || echo "SERVICES_DIR=MISSING"
[ -f "$ROOT/architecture/registry/SERVICE_REGISTRY_V2.md" ] && echo "SERVICE_REGISTRY=OK" || echo "SERVICE_REGISTRY=MISSING"

echo "== SERVICE COUNT =="
find "$ROOT/services" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l

echo "== SERVICE IDS =="
find "$ROOT/services" -name service.yaml -print0 2>/dev/null | while IFS= read -r -d '' f; do
  sid="$(read_yaml_value "$f" service_id)"
  port="$(read_yaml_value "$f" port)"
  echo "$sid port=$port file=$f"
done

echo "== DUPLICATE SERVICE IDS =="
find "$ROOT/services" -name service.yaml -print0 2>/dev/null | while IFS= read -r -d '' f; do read_yaml_value "$f" service_id; done | sort | uniq -d || true

echo "== DUPLICATE PORTS =="
find "$ROOT/services" -name service.yaml -print0 2>/dev/null | while IFS= read -r -d '' f; do read_yaml_value "$f" port; done | grep -E '^[0-9]+$' | sort | uniq -d || true

echo "NDSP_DOCTOR=DONE"
