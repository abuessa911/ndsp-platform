#!/usr/bin/env bash

ndsp_backend_root(){
  local src="${BASH_SOURCE[0]}"
  local dir
  dir="$(cd "$(dirname "$src")/../../.." && pwd)"
  echo "$dir"
}

lower(){
  tr '[:upper:]' '[:lower:]'
}

slugify(){
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
}

sed_escape(){
  printf '%s' "$1" | sed -e 's/[\/&|]/\\&/g'
}

read_yaml_value(){
  local file="$1"
  local key="$2"
  [ -f "$file" ] || return 0
  awk -F':' -v k="$key" '$1==k {sub(/^[ \t]+/,"",$2); print $2; exit}' "$file"
}

service_dir_name(){
  local service_id="$1"
  local slug="$2"
  echo "$(echo "$service_id" | lower)-$(slugify "$slug")"
}

service_id_exists(){
  local root="$1"
  local service_id="$2"
  grep -Rqs "service_id: $service_id" "$root/services" 2>/dev/null
}

port_exists(){
  local root="$1"
  local port="$2"
  grep -Rqs "port: $port" "$root/services" 2>/dev/null
}

find_next_port(){
  local root="$1"
  local start="${2:-9100}"
  local end="${3:-9299}"
  local p
  for p in $(seq "$start" "$end"); do
    if port_exists "$root" "$p"; then
      continue
    fi
    if command -v ss >/dev/null 2>&1 && ss -lnt 2>/dev/null | awk '{print $4}' | grep -q ":$p$"; then
      continue
    fi
    echo "$p"
    return 0
  done
  return 1
}

ensure_architecture_files(){
  local root="$1"
  mkdir -p "$root/architecture/registry" "$root/architecture/contracts"
  [ -f "$root/architecture/registry/SERVICE_REGISTRY_V2.md" ] || cat > "$root/architecture/registry/SERVICE_REGISTRY_V2.md" <<'EOT'
# NDSP Service Registry v2

| ID | Service | Port | Owner | Status |
|---|---|---:|---|---|
EOT
  [ -f "$root/architecture/CHANGELOG.md" ] || echo "# NDSP Architecture Changelog" > "$root/architecture/CHANGELOG.md"
}
