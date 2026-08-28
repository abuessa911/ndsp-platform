#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
export LC_ALL=C

ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
BRANCH="feature/naw-18-m2-governed-execution"
APPLY="NO"

while (($#)); do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --apply) APPLY="YES"; shift ;;
    *) printf 'ERROR=UNKNOWN_ARGUMENT:%s\n' "$1"; exit 64 ;;
  esac
done

TS="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE_ROOT="$ROOT/var/evidence/NDSP_M2_${TS}"
CANDIDATE="/tmp/ndsp-m2-candidate-${TS}"
CHECKPOINT="$ROOT/var/checkpoints/NDSP_M2_${TS}"
LIVE_ROOT="/var/www/ndsp-my-portal"
LIVE_LINK="$LIVE_ROOT/current"
UI_SERVICE="ndsp-ui-bridge-api.service"

section(){ printf '\n============================================================\n%s\n============================================================\n' "$1"; }
kv(){ printf '%s=%s\n' "$1" "$2"; }
die(){ printf 'ERROR=%s\nFINAL_STATUS=NDSP_M2_MASTER_FAIL\n' "$1"; exit 1; }

cleanup(){
  if [[ -d "$CANDIDATE" ]]; then
    git -C "$ROOT" worktree remove --force "$CANDIDATE" >/dev/null 2>&1 || rm -rf "$CANDIDATE" || true
  fi
}
trap cleanup EXIT

section "NDSP M2 — GOVERNED MASTER IMPLEMENTATION"
kv MODE "GATED_IMPLEMENTATION"
kv ROOT "$ROOT"
kv BRANCH "$BRANCH"
kv APPLY "$APPLY"
kv UTC "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

[[ -d "$ROOT/.git" ]] || die CANONICAL_ROOT_NOT_GIT
for cmd in git bash python3 npm; do command -v "$cmd" >/dev/null 2>&1 || die "MISSING_COMMAND_${cmd}"; done

mkdir -p "$EVIDENCE_ROOT" "$CHECKPOINT"

section "1/6 — CANONICAL SAFETY SNAPSHOT"
git -C "$ROOT" status --porcelain=v1 > "$EVIDENCE_ROOT/canonical-status-before.txt"
git -C "$ROOT" rev-parse HEAD > "$EVIDENCE_ROOT/canonical-head-before.txt"
readlink -f "$LIVE_LINK" > "$EVIDENCE_ROOT/live-release-before.txt" 2>/dev/null || true
kv CANONICAL_DIRTY_COUNT "$(wc -l < "$EVIDENCE_ROOT/canonical-status-before.txt" | tr -d ' ')"
kv CANONICAL_HEAD "$(cat "$EVIDENCE_ROOT/canonical-head-before.txt")"
kv LIVE_RELEASE_BEFORE "$(cat "$EVIDENCE_ROOT/live-release-before.txt" 2>/dev/null || true)"

# A dirty canonical root is allowed for candidate verification, but never for a blind
# branch checkout/reset. This script always uses an isolated detached worktree.

section "2/6 — FETCH + ISOLATED CANDIDATE"
git -C "$ROOT" fetch --no-tags origin "$BRANCH" 2>&1 | tee "$EVIDENCE_ROOT/git-fetch.txt"
REMOTE_REF="refs/remotes/origin/$BRANCH"
git -C "$ROOT" show-ref --verify --quiet "$REMOTE_REF" || die CANDIDATE_REMOTE_REF_NOT_FOUND
git -C "$ROOT" worktree add --detach "$CANDIDATE" "$REMOTE_REF" 2>&1 | tee "$EVIDENCE_ROOT/worktree-add.txt"
CANDIDATE_SHA="$(git -C "$CANDIDATE" rev-parse HEAD)"
kv CANDIDATE_SHA "$CANDIDATE_SHA"

CERTIFIER="$CANDIDATE/scripts/NDSP_M2_FINAL_READONLY_CERTIFIER.sh"
[[ -f "$CERTIFIER" ]] || die CERTIFIER_NOT_FOUND

section "3/6 — INDEPENDENT CERTIFICATION GATE"
set +e
bash "$CERTIFIER" "$CANDIDATE" 2>&1 | tee "$EVIDENCE_ROOT/certifier.txt"
CERT_RC=${PIPESTATUS[0]}
set -e
kv CERTIFIER_RC "$CERT_RC"
if [[ "$CERT_RC" -eq 2 ]]; then
  kv PRODUCTION_FILES_MODIFIED 0
  kv SERVICES_RESTARTED 0
  kv DATABASE_MODIFIED 0
  kv FINAL_STATUS NDSP_M2_MASTER_BLOCKED_BY_CERTIFIER
  exit 2
fi
[[ "$CERT_RC" -eq 0 ]] || die CERTIFIER_FAILED

section "4/6 — CANDIDATE BUILD ARTIFACT"
FE="$CANDIDATE/frontend/ndsp-sovereign-meridian-ui"
(
  cd "$FE"
  npm ci --ignore-scripts --no-audit --no-fund
  npm run typecheck
  npm run build
) 2>&1 | tee "$EVIDENCE_ROOT/candidate-build.txt"
[[ -f "$FE/dist/client/index.html" ]] || die CANDIDATE_BUILD_OUTPUT_MISSING

if [[ "$APPLY" != "YES" ]]; then
  kv PROJECT_FILES_MODIFIED 0
  kv PRODUCTION_FILES_MODIFIED 0
  kv SERVICES_RESTARTED 0
  kv DATABASE_MODIFIED 0
  kv FINAL_STATUS NDSP_M2_MASTER_VERIFIED_NOT_APPLIED
  exit 0
fi

section "5/6 — CHECKPOINT + CONTROLLED APPLY"
TARGETS=(
  "apps/ndsp-ui-bridge-api/main.py"
  "frontend/ndsp-sovereign-meridian-ui/src/App.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis-governance.css"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis/AnalysisContext.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis/types.ts"
  "frontend/ndsp-sovereign-meridian-ui/src/api/decision.ts"
  "frontend/ndsp-sovereign-meridian-ui/src/auth/RequireUser.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/main.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/pages/AnalysisPage.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/pages/AnalysisSetupPage.tsx"
  "scripts/NDSP_M2_GOVERNED_MASTER_IMPLEMENT.sh"
  "scripts/NDSP_M2_FINAL_READONLY_CERTIFIER.sh"
)

for rel in "${TARGETS[@]}"; do
  [[ -f "$CANDIDATE/$rel" ]] || die "CANDIDATE_TARGET_MISSING:$rel"
done

tar -C "$ROOT" -czf "$CHECKPOINT/source-before.tar.gz" "${TARGETS[@]}" 2>/dev/null || {
  # New files may not exist in canonical yet; preserve every existing target separately.
  rm -f "$CHECKPOINT/source-before.tar.gz"
  mkdir -p "$CHECKPOINT/files"
  for rel in "${TARGETS[@]}"; do
    if [[ -f "$ROOT/$rel" ]]; then
      mkdir -p "$CHECKPOINT/files/$(dirname "$rel")"
      cp -a "$ROOT/$rel" "$CHECKPOINT/files/$rel"
    else
      printf '%s\n' "$rel" >> "$CHECKPOINT/new-files.txt"
    fi
  done
}

LIVE_BEFORE="$(readlink -f "$LIVE_LINK" 2>/dev/null || true)"
printf '%s\n' "$LIVE_BEFORE" > "$CHECKPOINT/live-release-before.txt"

rollback(){
  set +e
  if [[ -f "$CHECKPOINT/source-before.tar.gz" ]]; then
    tar -C "$ROOT" -xzf "$CHECKPOINT/source-before.tar.gz"
  elif [[ -d "$CHECKPOINT/files" ]]; then
    cp -a "$CHECKPOINT/files/." "$ROOT/"
    if [[ -f "$CHECKPOINT/new-files.txt" ]]; then
      while IFS= read -r rel; do rm -f "$ROOT/$rel"; done < "$CHECKPOINT/new-files.txt"
    fi
  fi
  if [[ -n "$LIVE_BEFORE" && -d "$LIVE_BEFORE" ]]; then
    sudo ln -sfn "$LIVE_BEFORE" "$LIVE_LINK"
  fi
  sudo systemctl restart "$UI_SERVICE" >/dev/null 2>&1 || true
  printf 'ROLLBACK_EXECUTED=YES\n' | tee -a "$EVIDENCE_ROOT/apply.txt"
  set -e
}

for rel in "${TARGETS[@]}"; do
  mkdir -p "$ROOT/$(dirname "$rel")"
  cp -a "$CANDIDATE/$rel" "$ROOT/$rel"
done

RELEASE="$LIVE_ROOT/releases/${TS}-ndsp-m2-governed"
sudo mkdir -p "$RELEASE"
sudo rsync -a --delete "$FE/dist/client/" "$RELEASE/"
sudo ln -sfn "$RELEASE" "$LIVE_LINK"

if ! sudo systemctl restart "$UI_SERVICE"; then rollback; die UI_BRIDGE_RESTART_FAILED; fi
sleep 2
if ! systemctl is-active --quiet "$UI_SERVICE"; then rollback; die UI_BRIDGE_NOT_ACTIVE_AFTER_RESTART; fi
if ! curl -fsS "http://127.0.0.1:9066/api/ui-bridge/health" > "$EVIDENCE_ROOT/ui-bridge-health.json"; then rollback; die UI_BRIDGE_HEALTH_FAILED; fi
if ! curl -fsS "https://my.ndsp.app/analysis/setup" > /dev/null; then rollback; die LIVE_ANALYSIS_SETUP_ROUTE_FAILED; fi

section "6/6 — POST-APPLY CERTIFICATION"
set +e
NDSP_M2_LIVE_BASE="https://api.ndsp.app" bash "$ROOT/scripts/NDSP_M2_FINAL_READONLY_CERTIFIER.sh" "$ROOT" 2>&1 | tee "$EVIDENCE_ROOT/post-apply-certifier.txt"
POST_RC=${PIPESTATUS[0]}
set -e
if [[ "$POST_RC" -ne 0 ]]; then rollback; die POST_APPLY_CERTIFIER_FAILED; fi

kv CHECKPOINT "$CHECKPOINT"
kv RELEASE "$RELEASE"
kv PROJECT_FILES_MODIFIED "${#TARGETS[@]}"
kv PRODUCTION_FILES_MODIFIED 1
kv SERVICES_RESTARTED 1
kv DATABASE_MODIFIED 0
kv NGINX_MODIFIED 0
kv SYSTEMD_MODIFIED 0
kv FINAL_STATUS NDSP_M2_MASTER_IMPLEMENTATION_PASS
