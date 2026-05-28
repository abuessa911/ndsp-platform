#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT="./install_ndsp_checkout_plans_package.sh"

if [ ! -f "$SCRIPT" ]; then
  echo "ERROR: $SCRIPT not found in current directory"
  exit 1
fi

BACKUP="${SCRIPT}.broken_$(date +%Y%m%d_%H%M%S).bak"
cp "$SCRIPT" "$BACKUP"

python3 - "$SCRIPT" <<'PY'
from pathlib import Path
import sys

script_path = Path(sys.argv[1])
content = script_path.read_text()

marker = 'cat > "$ROOT/README_RUN.md" <<\'MD\''

idx = content.find(marker)
if idx == -1:
    print("ERROR: README heredoc marker not found")
    sys.exit(1)

head = content[:idx]

fixed_tail = r'''cat > "$ROOT/README_RUN.md" <<'MD'
# NDSP Checkout + Admin Plans Package

## 1) PostgreSQL Migration

```sh
cd ndsp_checkout_plans_package
DATABASE_URL='postgresql://user:password@127.0.0.1:5432/ndsp' bash scripts/run_migration.sh
