#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "${DATABASE_URL:-}" ]; then
  echo "ERROR: DATABASE_URL is required"
  echo "Example:"
  echo "DATABASE_URL='postgresql://user:pass@127.0.0.1:5432/ndsp' bash scripts/run_migration.sh"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATION="$ROOT_DIR/database/migrations/20260524_001_checkout_plans.sql"

psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$MIGRATION"

echo "MIGRATION_OK=True"
