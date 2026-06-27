#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

[ -f "$DIR/main.cjs" ]
[ -f "$DIR/service.yaml" ]
[ -f "$DIR/README.md" ]
[ -f "$DIR/CHANGELOG.md" ]
[ -d "$DIR/contracts" ]
[ -d "$DIR/docs" ]
[ -d "$DIR/systemd" ]
[ -d "$DIR/config" ]

echo "LEGACY_STRUCTURE_TEST_PASS=YES"
