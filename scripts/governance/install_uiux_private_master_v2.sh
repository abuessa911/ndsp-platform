#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-}"
if [[ -z "$SOURCE_DIR" ]]; then
  echo "usage: $0 /path/to/source-directory" >&2
  exit 2
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "error=SOURCE_DIRECTORY_MISSING path=$SOURCE_DIR" >&2
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
DEST_DIR="$REPO_ROOT/docs/99-governance/private/uiux-v2"
MANIFEST="$REPO_ROOT/docs/99-governance/ui-architecture/NDSP_UIUX_PRIVATE_MASTER_MANIFEST_V2.yaml"

if [[ ! -f "$MANIFEST" ]]; then
  echo "error=PRIVATE_MASTER_MANIFEST_MISSING path=$MANIFEST" >&2
  exit 1
fi

FILES=(
  "NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.md"
  "NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.pdf"
  "NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.docx"
  "NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_SHA256SUMS.txt"
)

HASHES=(
  "806be2bb2fbc72ae4192ec68d14d5b0e52162af4b5a9238ca9932b96c08c9d70"
  "43ee65c41ee4451e7956c8242cc637ae80c2e3b28a72a27cf74593281365b3e5"
  "f6f7cdf097c827faa58c9a71e1a06cb4104fbe9ee0417d1bad6aa9ad0dff1bd8"
  "a5005e2c70c9bc4cff6287bea4420984ad9a7bebee1ad7cbc62bc4ba81e45a60"
)

echo "status=VERIFYING_SOURCE"
for i in "${!FILES[@]}"; do
  file="${FILES[$i]}"
  expected="${HASHES[$i]}"
  src="$SOURCE_DIR/$file"

  if [[ ! -f "$src" ]]; then
    echo "error=SOURCE_FILE_MISSING file=$file" >&2
    exit 1
  fi

  actual="$(sha256sum "$src" | awk '{print $1}')"
  if [[ "$actual" != "$expected" ]]; then
    echo "error=SHA256_MISMATCH file=$file expected=$expected actual=$actual" >&2
    exit 1
  fi
  echo "verified_source=$file sha256=$actual"
done

mkdir -p "$DEST_DIR"
chmod 700 "$REPO_ROOT/docs/99-governance/private" "$DEST_DIR" 2>/dev/null || true

if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  for file in "${FILES[@]}"; do
    probe="docs/99-governance/private/uiux-v2/$file"
    if ! git -C "$REPO_ROOT" check-ignore -q "$probe"; then
      echo "error=PRIVATE_PATH_NOT_GIT_IGNORED path=$probe" >&2
      exit 1
    fi
  done
fi

echo "status=INSTALLING_PRIVATE_MASTER"
for i in "${!FILES[@]}"; do
  file="${FILES[$i]}"
  expected="${HASHES[$i]}"
  src="$SOURCE_DIR/$file"
  dst="$DEST_DIR/$file"

  install -m 600 "$src" "$dst"
  actual="$(sha256sum "$dst" | awk '{print $1}')"
  if [[ "$actual" != "$expected" ]]; then
    rm -f "$dst"
    echo "error=POST_COPY_SHA256_MISMATCH file=$file expected=$expected actual=$actual" >&2
    exit 1
  fi
  echo "installed=$file sha256=$actual"
done

UTC_NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
GIT_COMMIT="UNKNOWN"
if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse HEAD >/dev/null 2>&1; then
  GIT_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD)"
fi

LOCK_FILE="$DEST_DIR/INSTALLATION_LOCK_V2.txt"
cat > "$LOCK_FILE" <<EOF
NDSP_UIUX_PRIVATE_MASTER_V2
status=INSTALLED_VERIFIED_FROZEN
installed_at_utc=$UTC_NOW
repository_commit=$GIT_COMMIT
manifest=docs/99-governance/ui-architecture/NDSP_UIUX_PRIVATE_MASTER_MANIFEST_V2.yaml
classification=CONFIDENTIAL_PROPRIETARY
merge_rule=MERGE_NOT_REWRITE
unique_content_preserved=true
true_duplicates_only_may_be_consolidated=true
EOF
chmod 600 "$LOCK_FILE"

echo "validation=PASS"
echo "status=NDSP_UIUX_PRIVATE_MASTER_V2_INSTALLED"
echo "destination=$DEST_DIR"
echo "lock_file=$LOCK_FILE"
