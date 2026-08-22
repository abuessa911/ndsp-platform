#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

PROJECT_DIR="/home/nawaf511/empire-core-new"
OUT_BASE="/home/nawaf511/ndsp_full_backups_v2"
PASSPHRASE_FILE=""
KEEP_STAGE=0
HOST="$(hostname -s 2>/dev/null || hostname)"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_ID="NDSP_FULL_BACKUP_${HOST}_${TS}"
LOCK_FILE="/tmp/ndsp_full_backup_v1.lock"

usage() {
  cat <<'EOF'
Usage:
  ndsp_full_backup_v1.sh --passphrase-file PATH [--output-dir PATH] [--project-dir PATH] [--keep-stage]

Creates an encrypted, restorable NDSP backup without restarting services.
The passphrase file is required and is never copied into the backup.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --passphrase-file) PASSPHRASE_FILE="${2:-}"; shift 2 ;;
    --output-dir) OUT_BASE="${2:-}"; shift 2 ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --keep-stage) KEEP_STAGE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

[ -n "$PASSPHRASE_FILE" ] || { echo "ERROR: --passphrase-file is required." >&2; exit 2; }
[ -f "$PASSPHRASE_FILE" ] || { echo "ERROR: passphrase file not found: $PASSPHRASE_FILE" >&2; exit 1; }
[ -s "$PASSPHRASE_FILE" ] || { echo "ERROR: passphrase file is empty." >&2; exit 1; }
[ -d "$PROJECT_DIR" ] || { echo "ERROR: project not found: $PROJECT_DIR" >&2; exit 1; }

PASS_REAL="$(realpath -m "$PASSPHRASE_FILE")"
PROJECT_REAL="$(realpath -m "$PROJECT_DIR")"
OUT_REAL="$(realpath -m "$OUT_BASE")"
case "$PASS_REAL" in
  "$PROJECT_REAL"|"$PROJECT_REAL"/*|"$OUT_REAL"|"$OUT_REAL"/*)
    echo "ERROR: passphrase file must not be stored inside the project or backup output directory." >&2
    exit 1
    ;;
esac

MODE="$(stat -c '%a' "$PASSPHRASE_FILE" 2>/dev/null || true)"
case "$MODE" in 600|400) ;; *) echo "ERROR: passphrase file mode must be 600 or 400; actual=$MODE" >&2; exit 1 ;; esac

for tool in tar gzip sha256sum find stat du df flock gpg openssl python3 sudo; do
  command -v "$tool" >/dev/null 2>&1 || { echo "ERROR: required tool missing: $tool" >&2; exit 1; }
done

mkdir -p "$OUT_BASE"
chmod 700 "$OUT_BASE"
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "ERROR: another NDSP full backup is running." >&2; exit 1; }

RUN_ROOT="$OUT_BASE/.work_${BACKUP_ID}"
STAGE="$RUN_ROOT/$BACKUP_ID"
LOG="$OUT_BASE/${BACKUP_ID}.log"
REPORT="$OUT_BASE/${BACKUP_ID}.report.txt"
PLAIN_TAR="$OUT_BASE/${BACKUP_ID}.tar"
ENCRYPTED="$OUT_BASE/${BACKUP_ID}.tar.gpg"
SHA_FILE="$ENCRYPTED.sha256"
META_FILE="$ENCRYPTED.meta.json"

mkdir -p "$STAGE"/{filesystem,databases/local-postgresql,databases/docker-postgresql,databases/sqlite,databases/redis,docker-volumes,runtime,inventory,manifests}
chmod 700 "$RUN_ROOT" "$STAGE"
: > "$LOG"

CURRENT_STAGE="initialization"
WARNINGS=0

log() { printf '%s | %s\n' "$(date -Is)" "$*" | tee -a "$LOG"; }
warn() { WARNINGS=$((WARNINGS + 1)); log "WARNING | $*"; }
fail() { log "ERROR | stage=$CURRENT_STAGE | $*"; echo "FINAL_STATUS=NDSP_FULL_BACKUP_FAILED" | tee -a "$LOG"; exit 1; }

cleanup_on_exit() {
  rc=$?
  if [ "$rc" -ne 0 ]; then
    rm -f "$PLAIN_TAR" "$ENCRYPTED"
    printf '\nBackup failed. Restricted work directory retained for diagnosis:\n%s\n' "$RUN_ROOT" >&2
  fi
}
trap cleanup_on_exit EXIT

archive_paths() {
  local output="$1"; shift
  local -a rels=()
  local p rc
  for p in "$@"; do
    if sudo test -e "$p"; then rels+=("${p#/}"); else warn "path not found and skipped: $p"; fi
  done
  if [ "${#rels[@]}" -eq 0 ]; then warn "no existing paths for archive: $output"; return 0; fi
  log "Creating filesystem archive: $output"
  set +e
  sudo tar --xattrs --acls --numeric-owner --warning=no-file-changed -C / -czf "$output" "${rels[@]}" >>"$LOG" 2>&1
  rc=$?
  set -e
  if [ "$rc" -gt 1 ]; then fail "tar failed for $output with code $rc"; fi
  if [ "$rc" -eq 1 ]; then warn "files changed while archiving $output"; fi
  sudo chown "$(id -u):$(id -g)" "$output"
  chmod 600 "$output"
  tar -tzf "$output" >/dev/null || fail "archive validation failed: $output"
}

CURRENT_STAGE="capacity"
FREE_KB="$(df -Pk "$OUT_BASE" | awk 'NR==2 {print $4}')"
PROJECT_KB="$(du -sk "$PROJECT_DIR" | awk '{print $1}')"
MIN_KB=$((PROJECT_KB * 4 + 5 * 1024 * 1024))
log "FREE_KB=$FREE_KB PROJECT_KB=$PROJECT_KB REQUIRED_ESTIMATE_KB=$MIN_KB"
[ "$FREE_KB" -ge "$MIN_KB" ] || fail "insufficient free space for staged encrypted backup"

CURRENT_STAGE="identity-and-baseline"
{
  echo "BACKUP_ID=$BACKUP_ID"
  echo "HOST=$HOST"
  echo "STARTED_AT=$(date -Is)"
  echo "PROJECT_DIR=$PROJECT_DIR"
  echo "OUT_BASE=$OUT_BASE"
  id
  uname -a
  df -hT
} > "$STAGE/inventory/identity.txt"
find "$PROJECT_DIR" -xdev -type f -printf '%P\t%s\t%T@\n' 2>/dev/null | LC_ALL=C sort > "$STAGE/manifests/project_before.tsv"

CURRENT_STAGE="runtime-inventory"
{
  systemctl list-unit-files --no-pager 2>/dev/null || true
  echo
  systemctl list-units --all --no-pager 2>/dev/null || true
} > "$STAGE/runtime/systemd-state.txt"
sudo systemctl cat 'ndsp-*' 'ndip-*' 'empire-*' 2>/dev/null > "$STAGE/runtime/systemd-selected-units.txt" || true
sudo systemctl show 'ndsp-*' 'ndip-*' 'empire-*' 2>/dev/null > "$STAGE/runtime/systemd-selected-properties.txt" || true

if command -v pm2 >/dev/null 2>&1; then
  pm2 jlist > "$STAGE/runtime/pm2-jlist.json" 2>/dev/null || true
  pm2 status > "$STAGE/runtime/pm2-status.txt" 2>&1 || true
  pm2 report > "$STAGE/runtime/pm2-report.txt" 2>&1 || true
fi

if command -v docker >/dev/null 2>&1; then
  sudo -n docker ps -a --no-trunc > "$STAGE/runtime/docker-ps-a.txt" 2>&1 || true
  mapfile -t ALL_CONTAINERS < <(sudo -n docker ps -aq 2>/dev/null || true)
  [ "${#ALL_CONTAINERS[@]}" -eq 0 ] || sudo -n docker inspect "${ALL_CONTAINERS[@]}" > "$STAGE/runtime/docker-inspect.json" 2>/dev/null || true
  mapfile -t ALL_VOLUMES < <(sudo -n docker volume ls -q 2>/dev/null || true)
  [ "${#ALL_VOLUMES[@]}" -eq 0 ] || sudo -n docker volume inspect "${ALL_VOLUMES[@]}" > "$STAGE/runtime/docker-volumes.json" 2>/dev/null || true
fi

sudo nginx -T > "$STAGE/runtime/nginx-T.txt" 2>&1 || warn "nginx -T returned nonzero"
sudo ss -lntup > "$STAGE/runtime/listening-ports.txt" 2>&1 || true
sudo ufw status verbose > "$STAGE/runtime/ufw-status.txt" 2>&1 || true
crontab -l > "$STAGE/runtime/crontab-user.txt" 2>&1 || true
sudo crontab -l > "$STAGE/runtime/crontab-root.txt" 2>&1 || true
dpkg-query -W -f='${binary:Package}\t${Version}\n' > "$STAGE/inventory/dpkg-packages.tsv" 2>/dev/null || true
snap list > "$STAGE/inventory/snap-list.txt" 2>&1 || true
python3 --version > "$STAGE/inventory/python-version.txt" 2>&1 || true
node --version > "$STAGE/inventory/node-version.txt" 2>&1 || true
npm --version > "$STAGE/inventory/npm-version.txt" 2>&1 || true

CURRENT_STAGE="filesystem-project"
archive_paths "$STAGE/filesystem/project-full.tar.gz" "$PROJECT_DIR"

CURRENT_STAGE="filesystem-home-runtime"
archive_paths "$STAGE/filesystem/home-runtime.tar.gz" \
  "/home/nawaf511/ndsp_ops" \
  "/home/nawaf511/.pm2"

CURRENT_STAGE="filesystem-live-apps"
archive_paths "$STAGE/filesystem/live-apps.tar.gz" \
  "/opt/ndsp-current-user-display" \
  "/opt/ndsp-change-password-gateway" \
  "/opt/ndsp-v3-portal-gateway" \
  "/opt/ndsp-v52-contract" \
  "/opt/ndsp-v53-bridge" \
  "/opt/execution-engine" \
  "/var/www"

CURRENT_STAGE="filesystem-system-config"
archive_paths "$STAGE/filesystem/system-config.tar.gz" \
  "/etc/nginx" "/etc/systemd/system" "/etc/ndsp" "/etc/empire" \
  "/etc/postgresql" "/etc/redis" "/etc/cron.d" "/etc/letsencrypt" "/var/spool/cron/crontabs"

CURRENT_STAGE="referenced-executables"
grep -E '^(ExecStart|ExecStartPre|ExecStartPost)=' "$STAGE/runtime/systemd-selected-units.txt" 2>/dev/null \
  | grep -oE '/[^ ;"]+' \
  | sed 's/[\\]$//' \
  | while IFS= read -r candidate; do [ -f "$candidate" ] && printf '%s\n' "$candidate"; done \
  | LC_ALL=C sort -u > "$STAGE/manifests/referenced-executables.txt" || true
mapfile -t REF_EXE < "$STAGE/manifests/referenced-executables.txt"
if [ "${#REF_EXE[@]}" -gt 0 ]; then archive_paths "$STAGE/filesystem/referenced-executables.tar.gz" "${REF_EXE[@]}"; else warn "no referenced executable files discovered"; fi

CURRENT_STAGE="local-postgresql"
if command -v pg_dump >/dev/null 2>&1 && sudo -n -u postgres psql -XAtqc 'SELECT 1' postgres >/dev/null 2>&1; then
  sudo -n -u postgres pg_dumpall --globals-only > "$STAGE/databases/local-postgresql/globals.sql"
  mapfile -t LOCAL_DBS < <(sudo -n -u postgres psql -XAtqc "SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate ORDER BY 1" postgres)
  printf '%s\n' "${LOCAL_DBS[@]}" > "$STAGE/databases/local-postgresql/databases.txt"
  for db in "${LOCAL_DBS[@]}"; do
    safe="$(printf '%s' "$db" | tr -c 'A-Za-z0-9_.-' '_')"
    log "Dumping local PostgreSQL database: $db"
    sudo -n -u postgres pg_dump -Fc "$db" > "$STAGE/databases/local-postgresql/${safe}.dump" || fail "local pg_dump failed for $db"
    pg_restore -l "$STAGE/databases/local-postgresql/${safe}.dump" >/dev/null || fail "local pg dump validation failed for $db"
  done
else
  warn "local PostgreSQL logical dump unavailable"
fi

CURRENT_STAGE="docker-postgresql"
if command -v docker >/dev/null 2>&1; then
  mapfile -t PG_CONTAINERS < <(sudo -n docker ps --format '{{.Names}}\t{{.Image}}' | awk 'tolower($2) ~ /(postgres|timescale)/ {print $1}')
  for c in "${PG_CONTAINERS[@]}"; do
    c_safe="$(printf '%s' "$c" | tr -c 'A-Za-z0-9_.-' '_')"
    c_dir="$STAGE/databases/docker-postgresql/$c_safe"
    mkdir -p "$c_dir"
    log "Dumping Docker PostgreSQL container: $c"
    if ! sudo -n docker exec "$c" sh -lc 'u="${POSTGRES_USER:-postgres}"; d="${POSTGRES_DB:-postgres}"; export PGPASSWORD="${POSTGRES_PASSWORD:-}"; psql -U "$u" -d "$d" -XAtqc "SELECT 1"' >/dev/null 2>&1; then
      warn "cannot authenticate to PostgreSQL container: $c"
      continue
    fi
    sudo -n docker exec "$c" sh -lc 'u="${POSTGRES_USER:-postgres}"; d="${POSTGRES_DB:-postgres}"; export PGPASSWORD="${POSTGRES_PASSWORD:-}" PGDATABASE="$d"; pg_dumpall -U "$u" --globals-only' > "$c_dir/globals.sql"
    mapfile -t CDBS < <(sudo -n docker exec "$c" sh -lc 'u="${POSTGRES_USER:-postgres}"; d="${POSTGRES_DB:-postgres}"; export PGPASSWORD="${POSTGRES_PASSWORD:-}"; psql -U "$u" -d "$d" -XAtqc "SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate ORDER BY 1"')
    printf '%s\n' "${CDBS[@]}" > "$c_dir/databases.txt"
    for db in "${CDBS[@]}"; do
      safe="$(printf '%s' "$db" | tr -c 'A-Za-z0-9_.-' '_')"
      sudo -n docker exec -e NDSP_DB="$db" "$c" sh -lc 'u="${POSTGRES_USER:-postgres}"; export PGPASSWORD="${POSTGRES_PASSWORD:-}"; pg_dump -U "$u" -Fc "$NDSP_DB"' > "$c_dir/${safe}.dump" || fail "docker pg_dump failed for $c/$db"
      pg_restore -l "$c_dir/${safe}.dump" >/dev/null || fail "docker pg dump validation failed for $c/$db"
    done
  done
fi

CURRENT_STAGE="sqlite"
python3 - "$PROJECT_DIR" "$STAGE/databases/sqlite" <<'__SQLITE_BACKUP_PY__'
import os, sys, sqlite3, hashlib, pathlib, urllib.parse
roots=[pathlib.Path(sys.argv[1]), pathlib.Path('/opt/ndsp-current-user-display'), pathlib.Path('/opt/ndsp-change-password-gateway'), pathlib.Path('/var/www')]
out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
prune={'node_modules','venv','.venv','.git','__pycache__','.cache','backups','backup','logs'}
rows=[]
for root in roots:
    if not root.exists(): continue
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in prune and not d.startswith('.pytest')]
        for name in files:
            if pathlib.Path(name).suffix.lower() not in {'.db','.sqlite','.sqlite3'}: continue
            src=pathlib.Path(base)/name
            try:
                with src.open('rb') as f:
                    if f.read(16) != b'SQLite format 3\x00': continue
                digest=hashlib.sha256(str(src).encode()).hexdigest()[:16]
                dst=out/f'{digest}_{src.name}'
                uri='file:'+urllib.parse.quote(str(src))+'?mode=ro'
                s=sqlite3.connect(uri, uri=True, timeout=30)
                d=sqlite3.connect(dst)
                s.backup(d)
                ok=d.execute('PRAGMA integrity_check').fetchone()[0]
                d.close(); s.close()
                rows.append((str(src), str(dst.name), ok, src.stat().st_size))
            except Exception as e:
                rows.append((str(src), '', 'ERROR:'+str(e).replace('\t',' '), src.stat().st_size if src.exists() else -1))
with (out/'index.tsv').open('w', encoding='utf-8') as f:
    f.write('source\tbackup_file\tintegrity\tsource_size\n')
    for r in rows: f.write('\t'.join(map(str,r))+'\n')
__SQLITE_BACKUP_PY__

CURRENT_STAGE="redis"
if command -v redis-cli >/dev/null 2>&1; then
  redis-cli -h 127.0.0.1 -p 6379 INFO persistence > "$STAGE/databases/redis/info-persistence.txt" 2>&1 || true
  if timeout 180 redis-cli -h 127.0.0.1 -p 6379 --rdb "$STAGE/databases/redis/redis.rdb" >>"$LOG" 2>&1; then
    log "Redis RDB transfer completed"
  elif sudo test -f /var/lib/redis/dump.rdb; then
    warn "redis-cli RDB transfer failed; copying current filesystem RDB"
    sudo cp -a /var/lib/redis/dump.rdb "$STAGE/databases/redis/redis.rdb"
    sudo chown "$(id -u):$(id -g)" "$STAGE/databases/redis/redis.rdb"
  else
    warn "Redis backup unavailable"
  fi
fi

CURRENT_STAGE="docker-volumes"
if command -v docker >/dev/null 2>&1; then
  while IFS= read -r vol; do
    [ -n "$vol" ] || continue
    case "$vol" in *ndsp*|*ndip*|*empire*) ;; *) continue ;; esac
    mountpoint="$(sudo -n docker volume inspect -f '{{.Mountpoint}}' "$vol" 2>/dev/null || true)"
    [ -n "$mountpoint" ] || { warn "cannot resolve Docker volume: $vol"; continue; }
    running="$(sudo -n docker ps -q --filter volume="$vol" 2>/dev/null || true)"
    is_active_pg=0
    if [ -n "$running" ]; then
      for cid in $running; do
        image="$(sudo -n docker inspect -f '{{.Config.Image}}' "$cid" 2>/dev/null || true)"
        case "${image,,}" in *postgres*|*timescale*) is_active_pg=1 ;; esac
      done
    fi
    if [ "$is_active_pg" -eq 1 ]; then
      printf '%s\t%s\n' "$vol" "SKIPPED_ACTIVE_POSTGRES_LOGICAL_DUMP_IS_AUTHORITATIVE" >> "$STAGE/docker-volumes/status.tsv"
      continue
    fi
    safe="$(printf '%s' "$vol" | tr -c 'A-Za-z0-9_.-' '_')"
    log "Archiving Docker volume: $vol"
    sudo tar --xattrs --acls --numeric-owner -C "$mountpoint" -czf "$STAGE/docker-volumes/${safe}.tar.gz" . >>"$LOG" 2>&1 || fail "Docker volume archive failed: $vol"
    sudo chown "$(id -u):$(id -g)" "$STAGE/docker-volumes/${safe}.tar.gz"
    printf '%s\t%s\n' "$vol" "ARCHIVED" >> "$STAGE/docker-volumes/status.tsv"
  done < <(sudo -n docker volume ls -q 2>/dev/null || true)
fi

CURRENT_STAGE="consistency-check"
find "$PROJECT_DIR" -xdev -type f -printf '%P\t%s\t%T@\n' 2>/dev/null | LC_ALL=C sort > "$STAGE/manifests/project_after.tsv"
if ! cmp -s "$STAGE/manifests/project_before.tsv" "$STAGE/manifests/project_after.tsv"; then
  warn "project files changed during backup; see project-consistency.diff"
  diff -u "$STAGE/manifests/project_before.tsv" "$STAGE/manifests/project_after.tsv" > "$STAGE/manifests/project-consistency.diff" || true
else
  echo "PROJECT_CONSISTENCY=STABLE" > "$STAGE/manifests/project-consistency.txt"
fi

CURRENT_STAGE="internal-manifest"
cat > "$STAGE/README_FIRST.txt" <<EOF
NDSP encrypted full backup
Backup ID: $BACKUP_ID
Host: $HOST
Created: $(date -Is)
Project: $PROJECT_DIR

This package contains source, live files, system configuration, secrets, database dumps, runtime inventory and verification manifests.
It must remain encrypted. The passphrase is not included.
Use ndsp_backup_verify_v1.sh and ndsp_restore_drill_v1.sh before any production restore.
EOF

python3 - "$STAGE/manifests/backup-meta.json" "$BACKUP_ID" "$HOST" "$PROJECT_DIR" "$WARNINGS" <<'__BACKUP_META_PY__'
import json, sys, datetime
p,bid,host,project,w=sys.argv[1:]
obj={
 "schema_version":"1.0.0",
 "backup_id":bid,
 "host":host,
 "project":project,
 "created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "warnings":int(w),
 "encryption":"GPG symmetric AES256",
 "production_services_restarted":False,
 "database_write_intended":False,
 "restore_policy":"verify and drill before gated production restore"
}
open(p,'w',encoding='utf-8').write(json.dumps(obj,indent=2)+'\n')
__BACKUP_META_PY__

(
  cd "$STAGE"
  find . -type f ! -path './manifests/SHA256SUMS' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > manifests/SHA256SUMS
)

CURRENT_STAGE="outer-package"
log "Creating plaintext container tar"
tar -C "$RUN_ROOT" -cf "$PLAIN_TAR" "$BACKUP_ID"
PLAIN_SHA="$(sha256sum "$PLAIN_TAR" | awk '{print $1}')"

log "Encrypting package with GPG AES256"
gpg --batch --yes --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" \
  --symmetric --cipher-algo AES256 --compress-algo none \
  --output "$ENCRYPTED" "$PLAIN_TAR" >>"$LOG" 2>&1 || fail "GPG encryption failed"
chmod 600 "$ENCRYPTED"

CURRENT_STAGE="encrypted-verification"
VERIFY_SHA="$(gpg --batch --quiet --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --decrypt "$ENCRYPTED" 2>>"$LOG" | sha256sum | awk '{print $1}')"
[ "$VERIFY_SHA" = "$PLAIN_SHA" ] || fail "encrypted package decrypt verification mismatch"

sha256sum "$ENCRYPTED" > "$SHA_FILE"
chmod 600 "$SHA_FILE"
ENC_SHA="$(awk '{print $1}' "$SHA_FILE")"

python3 - "$META_FILE" "$BACKUP_ID" "$ENC_SHA" "$PLAIN_SHA" "$WARNINGS" "$ENCRYPTED" <<'__OUTER_META_PY__'
import json,sys,datetime,os
p,bid,enc,plain,w,archive=sys.argv[1:]
obj={
 "schema_version":"1.0.0",
 "backup_id":bid,
 "created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "encrypted_archive":os.path.basename(archive),
 "encrypted_sha256":enc,
 "plaintext_tar_sha256":plain,
 "warnings":int(w),
 "contains_secrets":True,
 "encrypted":True,
 "required_tools_for_restore":["gpg","tar","sha256sum","python3"],
 "production_changes":"NONE"
}
open(p,'w',encoding='utf-8').write(json.dumps(obj,indent=2)+'\n')
__OUTER_META_PY__
chmod 600 "$META_FILE"

cat > "$REPORT" <<EOF
NDSP FULL BACKUP COMPLETED
BACKUP_ID=$BACKUP_ID
ARCHIVE=$ENCRYPTED
SHA256_FILE=$SHA_FILE
META_FILE=$META_FILE
ENCRYPTED_SHA256=$ENC_SHA
PLAINTEXT_TAR_SHA256=$PLAIN_SHA
WARNINGS=$WARNINGS
PRODUCTION_SERVICES_RESTARTED=NONE
PRODUCTION_CONFIGURATION_CHANGED=NONE
DATABASE_WRITES_INTENDED=NONE
EOF
chmod 600 "$REPORT"

rm -f "$PLAIN_TAR"
if [ "$KEEP_STAGE" -eq 0 ]; then rm -rf "$RUN_ROOT"; else log "Stage retained by request: $RUN_ROOT"; fi
trap - EXIT

echo "============================================================"
echo "NDSP FULL BACKUP COMPLETED"
echo "BACKUP_ID=$BACKUP_ID"
echo "ARCHIVE=$ENCRYPTED"
echo "SHA256_FILE=$SHA_FILE"
echo "META_FILE=$META_FILE"
echo "REPORT=$REPORT"
echo "ENCRYPTED_SHA256=$ENC_SHA"
echo "WARNINGS=$WARNINGS"
echo "PRODUCTION_CHANGES=NONE"
echo "FINAL_STATUS=NDSP_FULL_BACKUP_ENCRYPTED_READY"
echo "============================================================"
