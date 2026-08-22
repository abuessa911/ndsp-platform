#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(ndsp_backend_root)"
TEMPLATE_ROOT="$ROOT/templates/service"

if [ $# -lt 3 ]; then
  echo "Usage: ndsp create service SERVICE_ID slug \"Service Name\" [--port PORT] [--product PRODUCT] [--domain DOMAIN]"
  exit 1
fi

SERVICE_ID="$1"
SLUG="$2"
SERVICE_NAME="$3"
shift 3

PRODUCT="SYS-001"
DOMAIN="Operating System"
SERVICE_TYPE="infrastructure_service"
VERSION="1.0.0"
RELEASE="REL-1.1"
SPRINT="SPR-003"
PORT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT="${2:-}"; shift 2 ;;
    --product) PRODUCT="${2:-}"; shift 2 ;;
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --type) SERVICE_TYPE="${2:-}"; shift 2 ;;
    *) echo "UNKNOWN_OPTION=$1"; exit 1 ;;
  esac
done

DIR_NAME="$(service_dir_name "$SERVICE_ID" "$SLUG")"
SERVICE_PATH="$ROOT/services/$DIR_NAME"
PORT="${PORT:-$(find_next_port "$ROOT" 9100 9299)}"
DATE="$(date +%Y%m%d_%H%M%S)"

if service_id_exists "$ROOT" "$SERVICE_ID"; then
  echo "ERROR=SERVICE_ID_ALREADY_EXISTS:$SERVICE_ID"
  exit 1
fi

if [ -d "$SERVICE_PATH" ]; then
  echo "ERROR=SERVICE_PATH_ALREADY_EXISTS:$SERVICE_PATH"
  exit 1
fi

if port_exists "$ROOT" "$PORT"; then
  echo "ERROR=PORT_ALREADY_EXISTS:$PORT"
  exit 1
fi

mkdir -p "$SERVICE_PATH"/{src,config,docs,contracts,tests,systemd,scripts}

replace_tpl(){
  local src="$1"
  local dst="$2"
  sed \
    -e "s|__SERVICE_ID__|$(sed_escape "$SERVICE_ID")|g" \
    -e "s|__SERVICE_NAME__|$(sed_escape "$SERVICE_NAME")|g" \
    -e "s|__DIR_NAME__|$(sed_escape "$DIR_NAME")|g" \
    -e "s|__PRODUCT__|$(sed_escape "$PRODUCT")|g" \
    -e "s|__DOMAIN__|$(sed_escape "$DOMAIN")|g" \
    -e "s|__VERSION__|$(sed_escape "$VERSION")|g" \
    -e "s|__RELEASE__|$(sed_escape "$RELEASE")|g" \
    -e "s|__SPRINT__|$(sed_escape "$SPRINT")|g" \
    -e "s|__PORT__|$(sed_escape "$PORT")|g" \
    -e "s|__SERVICE_TYPE__|$(sed_escape "$SERVICE_TYPE")|g" \
    -e "s|__DATE__|$(sed_escape "$DATE")|g" \
    -e "s|__USER__|$(sed_escape "${USER:-nawaf511}")|g" \
    -e "s|__SERVICE_PATH__|$(sed_escape "$SERVICE_PATH")|g" \
    "$src" > "$dst"
}

replace_tpl "$TEMPLATE_ROOT/package.json.tpl" "$SERVICE_PATH/package.json"
replace_tpl "$TEMPLATE_ROOT/service.yaml.tpl" "$SERVICE_PATH/service.yaml"
replace_tpl "$TEMPLATE_ROOT/main.cjs.tpl" "$SERVICE_PATH/main.cjs"
replace_tpl "$TEMPLATE_ROOT/README.md.tpl" "$SERVICE_PATH/README.md"
replace_tpl "$TEMPLATE_ROOT/CHANGELOG.md.tpl" "$SERVICE_PATH/CHANGELOG.md"
replace_tpl "$TEMPLATE_ROOT/contracts/CONTRACT.md.tpl" "$SERVICE_PATH/contracts/$SERVICE_ID-CONTRACT.md"
replace_tpl "$TEMPLATE_ROOT/docs/ARCHITECTURE.md.tpl" "$SERVICE_PATH/docs/ARCHITECTURE.md"
replace_tpl "$TEMPLATE_ROOT/tests/service.test.cjs.tpl" "$SERVICE_PATH/tests/service.test.cjs"
replace_tpl "$TEMPLATE_ROOT/systemd/service.service.tpl" "$SERVICE_PATH/systemd/ndsp-$DIR_NAME.service"
replace_tpl "$TEMPLATE_ROOT/config/default.env.tpl" "$SERVICE_PATH/config/default.env"

ensure_architecture_files "$ROOT"

if ! grep -q "| $SERVICE_ID |" "$ROOT/architecture/registry/SERVICE_REGISTRY_V2.md"; then
  cat >> "$ROOT/architecture/registry/SERVICE_REGISTRY_V2.md" <<EOT

| $SERVICE_ID | $SERVICE_NAME | $PORT | NDSP Engineering | Generated |
EOT
fi

cp "$SERVICE_PATH/contracts/$SERVICE_ID-CONTRACT.md" "$ROOT/architecture/contracts/$SERVICE_ID-CONTRACT.md"

cat >> "$ROOT/architecture/CHANGELOG.md" <<EOT

## $DATE

DEV-001 generated service $SERVICE_ID — $SERVICE_NAME.

Path:
- backend/services/$DIR_NAME

Port:
- $PORT
EOT

echo "SERVICE_CREATED=$SERVICE_PATH"
echo "SERVICE_ID=$SERVICE_ID"
echo "SERVICE_NAME=$SERVICE_NAME"
echo "PORT=$PORT"
echo "SYSTEMD_TEMPLATE=$SERVICE_PATH/systemd/ndsp-$DIR_NAME.service"
echo "TEST_COMMAND=cd $SERVICE_PATH && node tests/service.test.cjs"
echo "COMMIT_SUGGESTION=git add backend/services/$DIR_NAME backend/architecture && git commit -m \"feat($SERVICE_ID): add $SERVICE_NAME service\""
