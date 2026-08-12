#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

ARCHIVE=""
PASSPHRASE_FILE=""
DRILL_BASE="/home/nawaf511/ndsp_restore_drills"
MODE="full"
KEEP=0

usage() {
  cat <<'EOF'
Usage:
  ndsp_restore_drill_v1.sh --archive FILE.tar.gpg --passphrase-file PATH [--drill-dir PATH] [--metadata-only] [--keep]

The drill never writes to production paths or production databases.
Full mode extracts all filesystem archives into an isolated directory and restores PostgreSQL dumps into a temporary Docker container when Docker is available.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --archive) ARCHIVE="${2:-}"; shift 2 ;;
    --passphrase-file) PASSPHRASE_FILE="${2:-}"; shift 2 ;;
    --drill-dir) DRILL_BASE="${2:-}"; shift 2 ;;
    --metadata-only) MODE="metadata"; shift ;;
    --keep) KEEP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

[ -f "$ARCHIVE" ] || { echo "ERROR: archive not found." >&2; exit 1; }
[ -s "$PASSPHRASE_FILE" ] || { echo "ERROR: passphrase file missing or empty." >&2; exit 1; }
for tool in gpg tar sha256sum python3; do command -v "$tool" >/dev/null 2>&1 || { echo "ERROR: missing tool: $tool" >&2; exit 1; }; done

TS="$(date +%Y%m%d_%H%M%S)"
DRILL_ID="NDSP_RESTORE_DRILL_$TS"
WORK="$DRILL_BASE/$DRILL_ID"
PLAIN="$WORK/package.tar"
PACKAGE_ROOT="$WORK/package"
FILES_ROOT="$WORK/filesystem-restored"
REPORT="$WORK/RESTORE_DRILL_REPORT.txt"
CONTAINER="ndsp-restore-drill-${TS,,}"

mkdir -p "$PACKAGE_ROOT" "$FILES_ROOT"
chmod 700 "$DRILL_BASE" "$WORK"

cleanup() {
  rc=$?
  if command -v docker >/dev/null 2>&1; then sudo -n docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; fi
  rm -f "$PLAIN"
  if [ "$rc" -eq 0 ] && [ "$KEEP" -eq 0 ]; then rm -rf "$PACKAGE_ROOT" "$FILES_ROOT"; fi
  exit "$rc"
}
trap cleanup EXIT

gpg --batch --yes --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --output "$PLAIN" --decrypt "$ARCHIVE" >/dev/null 2>&1
tar -tf "$PLAIN" >/dev/null
tar -xf "$PLAIN" -C "$PACKAGE_ROOT" --no-same-owner --no-same-permissions
ROOT="$(find "$PACKAGE_ROOT" -mindepth 1 -maxdepth 1 -type d -name 'NDSP_FULL_BACKUP_*' -print -quit)"
[ -n "$ROOT" ] || { echo "ERROR: backup root missing." >&2; exit 1; }
(
  cd "$ROOT"
  sha256sum -c manifests/SHA256SUMS
) > "$WORK/internal-sha-check.txt"

NESTED=0
EXTRACTED=0
while IFS= read -r -d '' f; do
  NESTED=$((NESTED+1))
  tar -tzf "$f" >/dev/null
  if [ "$MODE" = "full" ]; then
    dest="$FILES_ROOT/$(basename "$f" .tar.gz)"
    mkdir -p "$dest"
    tar -xzf "$f" -C "$dest" --no-same-owner --no-same-permissions
    EXTRACTED=$((EXTRACTED+1))
  fi
done < <(find "$ROOT/filesystem" "$ROOT/docker-volumes" -type f -name '*.tar.gz' -print0 2>/dev/null)

PG_DUMPS=0
PG_LIST_OK=0
while IFS= read -r -d '' f; do
  PG_DUMPS=$((PG_DUMPS+1))
  if command -v pg_restore >/dev/null 2>&1; then
    pg_restore -l "$f" >/dev/null
    PG_LIST_OK=$((PG_LIST_OK+1))
  fi
done < <(find "$ROOT/databases" -type f -name '*.dump' -print0 2>/dev/null)

PG_RESTORED=0
PG_RESTORE_FAILED=0
if [ "$MODE" = "full" ] && [ "$PG_DUMPS" -gt 0 ] && command -v docker >/dev/null 2>&1 && command -v openssl >/dev/null 2>&1 && sudo -n docker image inspect postgres:16 >/dev/null 2>&1; then
  DRILL_PASSWORD="$(openssl rand -hex 24)"
  sudo -n docker run -d --rm --name "$CONTAINER" -e POSTGRES_PASSWORD="$DRILL_PASSWORD" postgres:16 >/dev/null
  ready=0
  for _ in $(seq 1 60); do
    if sudo -n docker exec "$CONTAINER" pg_isready -U postgres >/dev/null 2>&1; then ready=1; break; fi
    sleep 1
  done
  [ "$ready" -eq 1 ] || { echo "ERROR: temporary PostgreSQL did not become ready." >&2; exit 1; }

  i=0
  while IFS= read -r -d '' f; do
    i=$((i+1)); db="drill_${i}"
    sudo -n docker exec "$CONTAINER" createdb -U postgres "$db"
    sudo -n docker cp "$f" "$CONTAINER:/tmp/db.dump" >/dev/null
    if sudo -n docker exec "$CONTAINER" pg_restore -U postgres --no-owner --no-privileges --exit-on-error -d "$db" /tmp/db.dump >/dev/null 2>&1; then
      PG_RESTORED=$((PG_RESTORED+1))
    else
      PG_RESTORE_FAILED=$((PG_RESTORE_FAILED+1))
    fi
    sudo -n docker exec "$CONTAINER" rm -f /tmp/db.dump
  done < <(find "$ROOT/databases" -type f -name '*.dump' -print0 2>/dev/null)
fi

SQLITE_COUNT=0
SQLITE_OK=0
while IFS= read -r -d '' f; do
  SQLITE_COUNT=$((SQLITE_COUNT+1))
  result="$(python3 - "$f" <<'__SQLITE_DRILL_PY__'
import sqlite3,sys
c=sqlite3.connect(f'file:{sys.argv[1]}?mode=ro',uri=True)
print(c.execute('PRAGMA integrity_check').fetchone()[0])
c.close()
__SQLITE_DRILL_PY__
)"
  [ "$result" = "ok" ] && SQLITE_OK=$((SQLITE_OK+1))
done < <(find "$ROOT/databases/sqlite" -type f ! -name 'index.tsv' -print0 2>/dev/null)

REDIS_STATUS="NOT_PRESENT"
RDB="$(find "$ROOT/databases/redis" -type f -name '*.rdb' -print -quit 2>/dev/null || true)"
if [ -n "$RDB" ]; then
  if command -v redis-check-rdb >/dev/null 2>&1; then redis-check-rdb "$RDB" >/dev/null; REDIS_STATUS="VALIDATED"; else REDIS_STATUS="PRESENT"; fi
fi

FINAL="NDSP_RESTORE_DRILL_OK"
if [ "$PG_RESTORE_FAILED" -gt 0 ] || [ "$SQLITE_COUNT" -ne "$SQLITE_OK" ]; then FINAL="NDSP_RESTORE_DRILL_PARTIAL_FAILURE"; fi

cat > "$REPORT" <<EOF
NDSP RESTORE DRILL
DRILL_ID=$DRILL_ID
ARCHIVE=$ARCHIVE
MODE=$MODE
NESTED_ARCHIVES=$NESTED
FILESYSTEM_ARCHIVES_EXTRACTED=$EXTRACTED
POSTGRES_DUMPS=$PG_DUMPS
POSTGRES_LIST_VALIDATED=$PG_LIST_OK
POSTGRES_ACTUALLY_RESTORED_TO_TEMP_CONTAINER=$PG_RESTORED
POSTGRES_RESTORE_FAILED=$PG_RESTORE_FAILED
SQLITE_COUNT=$SQLITE_COUNT
SQLITE_OK=$SQLITE_OK
REDIS_STATUS=$REDIS_STATUS
PRODUCTION_PATHS_WRITTEN=NONE
PRODUCTION_DATABASES_WRITTEN=NONE
PRODUCTION_SERVICES_CHANGED=NONE
FINAL_STATUS=$FINAL
EOF

cat "$REPORT"
[ "$FINAL" = "NDSP_RESTORE_DRILL_OK" ]
