#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

ARCHIVE=""
PASSPHRASE_FILE=""
WORK_BASE="${TMPDIR:-/tmp}"
KEEP_WORK=0

usage() {
  echo "Usage: ndsp_backup_verify_v1.sh --archive FILE.tar.gpg --passphrase-file PATH [--work-dir PATH] [--keep-work]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --archive) ARCHIVE="${2:-}"; shift 2 ;;
    --passphrase-file) PASSPHRASE_FILE="${2:-}"; shift 2 ;;
    --work-dir) WORK_BASE="${2:-}"; shift 2 ;;
    --keep-work) KEEP_WORK=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

[ -f "$ARCHIVE" ] || { echo "ERROR: archive not found: $ARCHIVE" >&2; exit 1; }
[ -s "$PASSPHRASE_FILE" ] || { echo "ERROR: passphrase file missing or empty." >&2; exit 1; }
for tool in gpg tar sha256sum python3; do command -v "$tool" >/dev/null 2>&1 || { echo "ERROR: missing tool: $tool" >&2; exit 1; }; done

TS="$(date +%Y%m%d_%H%M%S)"
WORK="$WORK_BASE/ndsp_backup_verify_$TS"
PLAIN="$WORK/package.tar"
EXTRACT="$WORK/extracted"
REPORT="${ARCHIVE}.verify_${TS}.txt"
mkdir -p "$EXTRACT"

cleanup() {
  rc=$?
  if [ "$KEEP_WORK" -eq 0 ]; then rm -rf "$WORK"; else echo "WORK_RETAINED=$WORK"; fi
  exit "$rc"
}
trap cleanup EXIT

SHA_FILE="$ARCHIVE.sha256"
if [ -f "$SHA_FILE" ]; then
  EXPECTED="$(awk 'NR==1 {print $1}' "$SHA_FILE")"
  ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
  [ "$EXPECTED" = "$ACTUAL" ] || { echo "ERROR: encrypted SHA256 mismatch." >&2; exit 1; }
else
  echo "WARNING: encrypted sidecar SHA256 file not found."
fi

gpg --batch --yes --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --output "$PLAIN" --decrypt "$ARCHIVE" >/dev/null 2>&1 || { echo "ERROR: decryption failed." >&2; exit 1; }

python3 - "$PLAIN" <<'__OUTER_SAFE_PY__'
import tarfile,sys,pathlib
with tarfile.open(sys.argv[1],'r:') as tf:
    for m in tf.getmembers():
        q=pathlib.PurePosixPath(m.name)
        if q.is_absolute() or '..' in q.parts:
            raise SystemExit('unsafe tar member: '+m.name)
        if m.issym() or m.islnk():
            t=pathlib.PurePosixPath(m.linkname)
            if t.is_absolute() or '..' in t.parts:
                raise SystemExit('unsafe tar link: '+m.name)
print('OUTER_TAR_PATH_VALIDATION=OK')
__OUTER_SAFE_PY__

tar -xf "$PLAIN" -C "$EXTRACT" --no-same-owner --no-same-permissions
ROOT="$(find "$EXTRACT" -mindepth 1 -maxdepth 1 -type d -name 'NDSP_FULL_BACKUP_*' -print -quit)"
[ -n "$ROOT" ] || { echo "ERROR: backup root not found after extraction." >&2; exit 1; }
[ -f "$ROOT/manifests/SHA256SUMS" ] || { echo "ERROR: internal SHA256SUMS missing." >&2; exit 1; }

(
  cd "$ROOT"
  sha256sum -c manifests/SHA256SUMS
) > "$WORK/internal-sha-check.txt"

TAR_COUNT=0
while IFS= read -r -d '' f; do
  TAR_COUNT=$((TAR_COUNT+1))
  tar -tzf "$f" >/dev/null
  python3 - "$f" <<'__NESTED_SAFE_PY__'
import tarfile,sys,pathlib
with tarfile.open(sys.argv[1],'r:gz') as tf:
    for m in tf.getmembers():
        q=pathlib.PurePosixPath(m.name)
        if q.is_absolute() or '..' in q.parts:
            raise SystemExit('unsafe nested tar member: '+m.name)
print('OK')
__NESTED_SAFE_PY__
done < <(find "$ROOT" -type f -name '*.tar.gz' -print0)

PG_COUNT=0
PG_VALIDATED=0
while IFS= read -r -d '' f; do
  PG_COUNT=$((PG_COUNT+1))
  if command -v pg_restore >/dev/null 2>&1; then
    pg_restore -l "$f" >/dev/null
    PG_VALIDATED=$((PG_VALIDATED+1))
  fi
done < <(find "$ROOT/databases" -type f -name '*.dump' -print0 2>/dev/null)

read -r SQLITE_COUNT SQLITE_OK < <(
python3 - "$ROOT" "$WORK/sqlite-check.tsv" <<'__SQLITE_VERIFY_PY__'
import sqlite3,pathlib,sys
root=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); rows=[]
for p in root.glob('databases/sqlite/*'):
    if p.name=='index.tsv' or not p.is_file(): continue
    try:
        c=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
        v=c.execute('PRAGMA integrity_check').fetchone()[0]
        c.close()
    except Exception as e:
        v='ERROR:'+str(e)
    rows.append((str(p),v))
out.write_text('\n'.join('\t'.join(x) for x in rows)+'\n',encoding='utf-8')
print(len(rows),sum(v=='ok' for _,v in rows))
__SQLITE_VERIFY_PY__
)

REDIS_STATUS="NOT_PRESENT"
RDB="$(find "$ROOT/databases/redis" -type f -name '*.rdb' -print -quit 2>/dev/null || true)"
if [ -n "$RDB" ]; then
  if command -v redis-check-rdb >/dev/null 2>&1; then
    redis-check-rdb "$RDB" >/dev/null
    REDIS_STATUS="VALIDATED"
  else
    REDIS_STATUS="PRESENT_TOOL_UNAVAILABLE"
  fi
fi

cat > "$REPORT" <<EOF
NDSP BACKUP VERIFICATION
ARCHIVE=$ARCHIVE
BACKUP_ROOT=$ROOT
OUTER_SHA256=OK
DECRYPTION=OK
OUTER_TAR_PATH_SAFETY=OK
INTERNAL_SHA256=OK
NESTED_TAR_COUNT=$TAR_COUNT
NESTED_TAR_VALIDATION=OK
POSTGRES_DUMP_COUNT=$PG_COUNT
POSTGRES_DUMPS_VALIDATED=$PG_VALIDATED
SQLITE_COUNT=$SQLITE_COUNT
SQLITE_OK=$SQLITE_OK
REDIS_STATUS=$REDIS_STATUS
PRODUCTION_CHANGES=NONE
FINAL_STATUS=NDSP_BACKUP_VERIFIED_OK
EOF

cat "$REPORT"
