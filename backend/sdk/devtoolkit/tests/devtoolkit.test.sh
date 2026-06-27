#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TMPROOT="$(mktemp -d)"
trap 'rm -rf "$TMPROOT"' EXIT

mkdir -p "$TMPROOT/backend"

cp -a "$ROOT/framework" "$TMPROOT/backend/framework"
cp -a "$ROOT/sdk" "$TMPROOT/backend/sdk"
cp -a "$ROOT/tools" "$TMPROOT/backend/tools"
cp -a "$ROOT/templates" "$TMPROOT/backend/templates"

mkdir -p "$TMPROOT/backend/services"
mkdir -p "$TMPROOT/backend/architecture/registry"
mkdir -p "$TMPROOT/backend/architecture/contracts"

if [ -d "$ROOT/node_modules" ]; then
  ln -s "$ROOT/node_modules" "$TMPROOT/backend/node_modules"
fi

if [ -f "$ROOT/package.json" ]; then
  cp -a "$ROOT/package.json" "$TMPROOT/backend/package.json"
fi

if [ -f "$ROOT/package-lock.json" ]; then
  cp -a "$ROOT/package-lock.json" "$TMPROOT/backend/package-lock.json"
fi

cd "$TMPROOT/backend"

./tools/ndsp version | grep -q "1.0.0"

./tools/ndsp create service TST-001 test-service "Test Service" --port 9199 --domain Testing

[ -f "$TMPROOT/backend/services/tst-001-test-service/main.cjs" ]
[ -f "$TMPROOT/backend/services/tst-001-test-service/service.yaml" ]
[ -f "$TMPROOT/backend/services/tst-001-test-service/tests/service.test.cjs" ]

cd "$TMPROOT/backend/services/tst-001-test-service"
node tests/service.test.cjs | tee /tmp/dev001_generated_service_test.out
grep -q "TST-001_TEST_PASS=YES" /tmp/dev001_generated_service_test.out

cd "$TMPROOT/backend"
./tools/ndsp validate all
./tools/ndsp doctor | grep -q "NDSP_DOCTOR=DONE"

echo "DEV001_TEST_PASS=YES"
