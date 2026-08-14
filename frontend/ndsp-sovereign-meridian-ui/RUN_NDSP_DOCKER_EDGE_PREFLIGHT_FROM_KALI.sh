#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

EXPECTED_LOCAL_USER="nawaf"
FORBIDDEN_HOST="vmi2934783"
REMOTE="nawaf511@161.97.144.189"
DOWNLOAD_DIR="${HOME}/Downloads"

if [[ "$(id -un)" != "$EXPECTED_LOCAL_USER" ]]; then
  printf 'ERROR=RUN_AS_KALI_USER_NAWAF\n' >&2
  exit 1
fi

if [[ "$(hostname)" == "$FORBIDDEN_HOST" ]]; then
  printf 'ERROR=RUN_FROM_KALI_NOT_SERVER\n' >&2
  exit 1
fi

for command_name in ssh scp base64 awk tee tr date sha256sum; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'ERROR=MISSING_LOCAL_COMMAND:%s\n' "$command_name" >&2
    exit 1
  fi
done

mkdir -p "$DOWNLOAD_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RAW_LOG="$DOWNLOAD_DIR/NDSP_DOCKER_EDGE_PREFLIGHT_${STAMP}.raw.log"
CLEAN_LOG="$DOWNLOAD_DIR/NDSP_DOCKER_EDGE_PREFLIGHT_${STAMP}.log"

PAYLOAD="$({
  base64 -w0 <<'REMOTE'
set -Eeuo pipefail
umask 077

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT="/home/nawaf511/NDSP_DOCKER_EDGE_PREFLIGHT_${STAMP}.txt"

exec > >(tee "$REPORT") 2>&1

on_error() {
  local exit_code="$?"
  local failed_line="${BASH_LINENO[0]:-unknown}"
  printf '\nFINAL_STATUS=DOCKER_EDGE_PREFLIGHT_FAILED\n'
  printf 'FAILED_LINE=%s\n' "$failed_line"
  printf 'FAILED_EXIT=%s\n' "$exit_code"
  printf 'FILES_DELETED=0\n'
  printf 'SERVICES_MODIFIED=0\n'
  printf 'NGINX_MODIFIED=0\n'
  printf 'DOCKER_MODIFIED=0\n'
  printf 'DATABASE_MODIFIED=0\n'
  printf 'REPORT=%s\n' "$REPORT"
  exit "$exit_code"
}
trap on_error ERR

printf 'AUDIT=NDSP_DOCKER_EDGE_PREFLIGHT\n'
printf 'AUDIT_MODE=READ_ONLY_EXCEPT_REPORT\n'
printf 'HOST=%s\n' "$(hostname)"
printf 'USER=%s\n' "$(id -un)"
printf 'TIMESTAMP_UTC=%s\n' "$STAMP"
printf 'REPORT=%s\n' "$REPORT"

printf '\n===== SUDO AUTHORIZATION =====\n'
printf 'INFO=Password may be requested once for read-only inspection\n'
sudo -v

for command_name in docker ss findmnt readlink stat curl awk sed; do
  command -v "$command_name" >/dev/null 2>&1 || {
    printf 'ERROR=MISSING_REMOTE_COMMAND:%s\n' "$command_name" >&2
    exit 1
  }
done

printf '\n===== PUBLIC HTTP STATUS =====\n'
for url in \
  https://ndsp.app/ \
  https://www.ndsp.app/ \
  https://my.ndsp.app/ \
  https://my.ndsp.app/login \
  https://admin.ndsp.app/ \
  https://api.ndsp.app/health \
  https://api.ndsp.app/api/health; do
  status="$(curl -kLsS --max-time 12 -o /dev/null -w '%{http_code}' "$url" || true)"
  printf 'HTTP=%s URL=%s\n' "${status:-000}" "$url"
done

printf '\n===== HOST EDGE LISTENERS =====\n'
sudo ss -ltnp | awk 'NR == 1 || $4 ~ /:80$/ || $4 ~ /:443$/'
printf 'HOST_NGINX_STATE=%s\n' "$(systemctl is-active nginx 2>/dev/null || true)"

printf '\n===== DOCKER VERSION =====\n'
sudo docker version --format 'SERVER_VERSION={{.Server.Version}}' 2>/dev/null || sudo docker version

printf '\n===== RUNNING CONTAINERS =====\n'
sudo docker ps --no-trunc --format 'ID={{.ID}} NAME={{.Names}} IMAGE={{.Image}} STATUS={{.Status}} PORTS={{.Ports}}'

mapfile -t EDGE_IDS < <(
  sudo docker ps --format '{{.ID}} {{.Ports}}' |
    awk '$0 ~ /(^|, | )0\.0\.0\.0:80->/ || $0 ~ /(^|, | ):::80->/ || $0 ~ /(^|, | )0\.0\.0\.0:443->/ || $0 ~ /(^|, | ):::443->/ {print $1}' |
    sort -u
)

printf 'EDGE_CONTAINER_COUNT=%s\n' "${#EDGE_IDS[@]}"
if ((${#EDGE_IDS[@]} == 0)); then
  printf 'ERROR=NO_RUNNING_CONTAINER_PUBLISHES_80_OR_443\n' >&2
  exit 1
fi

for container_id in "${EDGE_IDS[@]}"; do
  name="$(sudo docker inspect --format '{{.Name}}' "$container_id" | sed 's#^/##')"
  printf '\n===== EDGE CONTAINER: %s =====\n' "$name"
  sudo docker inspect --format 'ID={{.Id}} IMAGE={{.Config.Image}} STATE={{.State.Status}} NETWORK_MODE={{.HostConfig.NetworkMode}}' "$container_id"
  sudo docker inspect --format 'ENTRYPOINT={{json .Config.Entrypoint}} CMD={{json .Config.Cmd}}' "$container_id"
  sudo docker inspect --format 'PORT_BINDINGS={{json .HostConfig.PortBindings}}' "$container_id"
  sudo docker inspect --format '{{range .Mounts}}MOUNT TYPE={{.Type}} SOURCE={{.Source}} DESTINATION={{.Destination}} RW={{.RW}}{{println}}{{end}}' "$container_id"

  printf '%s\n' '--- CONTAINER WEBROOT VISIBILITY ---'
  set +e
  sudo docker exec "$container_id" sh -c '
    for path in \
      /var/www/ndsp-my-portal/current \
      /var/www/ndsp-my-portal \
      /var/www/ndsp-admin \
      /var/www/ndsp.app \
      /usr/share/nginx/html; do
      if [ -L "$path" ]; then
        printf "TYPE=SYMLINK PATH=%s TARGET=%s\n" "$path" "$(readlink "$path")"
      elif [ -d "$path" ]; then
        printf "TYPE=DIRECTORY PATH=%s\n" "$path"
      elif [ -f "$path" ]; then
        printf "TYPE=FILE PATH=%s\n" "$path"
      else
        printf "TYPE=ABSENT PATH=%s\n" "$path"
      fi
    done
  ' 2>&1
  visibility_status="$?"
  set -e
  printf 'WEBROOT_VISIBILITY_EXIT=%s\n' "$visibility_status"

  printf '%s\n' '--- FILTERED EDGE CONFIGURATION ---'
  set +e
  sudo docker exec "$container_id" sh -c '
    if command -v nginx >/dev/null 2>&1; then
      nginx -T 2>&1 | grep -E "configuration file|server_name|listen |root |alias |location |proxy_pass|try_files|include |ssl_certificate"
    elif command -v caddy >/dev/null 2>&1; then
      caddy version
      for file in /etc/caddy/Caddyfile /config/caddy/Caddyfile; do
        [ -f "$file" ] && sed -n "1,260p" "$file"
      done
    elif command -v traefik >/dev/null 2>&1; then
      traefik version
      printf "INFO=Traefik detected; routing labels intentionally not printed because labels can carry credentials.\n"
    else
      printf "INFO=No nginx, caddy, or traefik executable detected in container.\n"
    fi
  ' 2>&1
  config_status="$?"
  set -e
  printf 'FILTERED_CONFIG_EXIT=%s\n' "$config_status"
done

printf '\n===== HOST DEPLOYMENT PATHS =====\n'
for path in \
  /var/www/ndsp-my-portal \
  /var/www/ndsp-my-portal/current \
  /var/www/ndsp-admin \
  /var/www/ndsp.app \
  /home/nawaf511/empire-core-new/frontend/public-site/dist; do
  if [[ -L "$path" ]]; then
    printf 'TYPE=SYMLINK PATH=%s TARGET=%s RESOLVED=%s\n' "$path" "$(readlink "$path")" "$(readlink -f "$path" 2>/dev/null || true)"
  elif [[ -d "$path" ]]; then
    printf 'TYPE=DIRECTORY PATH=%s\n' "$path"
  elif [[ -f "$path" ]]; then
    printf 'TYPE=FILE PATH=%s\n' "$path"
  else
    printf 'TYPE=ABSENT PATH=%s\n' "$path"
  fi
done

printf '\n===== HOST FILESYSTEM AND ENTRYPOINTS =====\n'
findmnt -T /var/www/ndsp-my-portal 2>/dev/null || true
for root in /var/www/ndsp-my-portal /var/www/ndsp-admin /home/nawaf511/empire-core-new/frontend/public-site/dist; do
  [[ -e "$root" || -L "$root" ]] || continue
  find "$root" -maxdepth 3 -type f -name index.html -printf 'ENTRY=%p SIZE=%s MTIME=%TY-%Tm-%TdT%TH:%TM:%TSZ\n' 2>/dev/null | sort
done

printf '\n===== ACTIVE HOST NGINX NDSP DIRECTIVES =====\n'
set +e
sudo nginx -T 2>&1 |
  grep -E 'configuration file|server_name.*ndsp\.app|listen |root |alias |location |proxy_pass|try_files' |
  sed -n '1,420p'
host_nginx_exit="${PIPESTATUS[0]}"
set -e
printf 'HOST_NGINX_DUMP_EXIT=%s\n' "$host_nginx_exit"

printf '\nFINAL_STATUS=DOCKER_EDGE_PREFLIGHT_COMPLETE\n'
printf 'SOURCE_FILES_MODIFIED=0\n'
printf 'REPORT_FILES_CREATED=1\n'
printf 'FILES_DELETED=0\n'
printf 'SERVICES_MODIFIED=0\n'
printf 'NGINX_MODIFIED=0\n'
printf 'DOCKER_MODIFIED=0\n'
printf 'DATABASE_MODIFIED=0\n'
printf 'NEXT_ACTION=UPLOAD_DOCKER_EDGE_PREFLIGHT_REPORT\n'
printf 'REPORT=%s\n' "$REPORT"
REMOTE
})"

printf 'LOCAL_HOST=%s\n' "$(hostname)"
printf 'LOCAL_USER=%s\n' "$(id -un)"
printf 'REMOTE_TARGET=%s\n' "$REMOTE"
printf 'INFO=Enter the SSH password, then the server sudo password when requested.\n'

set +e
ssh -tt "$REMOTE" "printf '%s' '$PAYLOAD' | base64 -d | bash" 2>&1 | tee "$RAW_LOG"
SSH_STATUS="${PIPESTATUS[0]}"
set -e

tr -d '\r' <"$RAW_LOG" >"$CLEAN_LOG"

REMOTE_REPORT="$({
  awk -F= '
    /^REPORT=\/home\/nawaf511\/NDSP_DOCKER_EDGE_PREFLIGHT_[0-9TZ]+\.txt$/ {report=$2}
    END {print report}
  ' "$CLEAN_LOG"
})"

if [[ ! "$REMOTE_REPORT" =~ ^/home/nawaf511/NDSP_DOCKER_EDGE_PREFLIGHT_[0-9]{8}T[0-9]{6}Z\.txt$ ]]; then
  printf 'ERROR=VALID_REMOTE_REPORT_PATH_NOT_FOUND\n' >&2
  printf 'SSH_EXIT=%s\n' "$SSH_STATUS" >&2
  printf 'LOG=%s\n' "$CLEAN_LOG" >&2
  exit 1
fi

printf 'INFO=Enter the SSH password once more to download the report.\n'
scp "$REMOTE:$REMOTE_REPORT" "$DOWNLOAD_DIR/"
LOCAL_REPORT="$DOWNLOAD_DIR/$(basename -- "$REMOTE_REPORT")"
test -s "$LOCAL_REPORT"

sha256sum "$LOCAL_REPORT"
printf 'REPORT_READY=%s\n' "$LOCAL_REPORT"
printf 'RUN_LOG=%s\n' "$CLEAN_LOG"

if (( SSH_STATUS != 0 )); then
  printf 'ERROR=REMOTE_PREFLIGHT_FAILED\n' >&2
  printf 'SSH_EXIT=%s\n' "$SSH_STATUS" >&2
  exit "$SSH_STATUS"
fi

PREFLIGHT_STATUS="$({
  awk -F= '/^FINAL_STATUS=/ {status=$2} END {print status}' "$CLEAN_LOG"
})"
if [[ "$PREFLIGHT_STATUS" != "DOCKER_EDGE_PREFLIGHT_COMPLETE" ]]; then
  printf 'ERROR=UNEXPECTED_REMOTE_FINAL_STATUS:%s\n' "$PREFLIGHT_STATUS" >&2
  exit 1
fi

printf 'FINAL_STATUS=DOCKER_EDGE_PREFLIGHT_COLLECTED_SUCCESSFULLY\n'
