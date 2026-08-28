#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
export LC_ALL=C

ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
BRANCH="feature/ndsp-sovereign-meridian-ui"
REPO_URL="https://github.com/abuessa911/ndsp-platform.git"
APPLY="NO"

while (($#)); do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --apply) APPLY="YES"; shift ;;
    *) printf 'ERROR=UNKNOWN_ARGUMENT:%s\n' "$1"; exit 64 ;;
  esac
done

CANONICAL_ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE_ROOT="$ROOT/var/evidence/NDSP_M2_${TS}"
CANDIDATE="/tmp/ndsp-m2-candidate-${TS}"
CHECKPOINT="$ROOT/var/checkpoints/NDSP_M2_${TS}"
LIVE_ROOT="/var/www/ndsp-my-portal"
LIVE_LINK="$LIVE_ROOT/current"
UI_SERVICE="ndsp-ui-bridge-api.service"
UI_RUNTIME="$ROOT/apps/ndsp-ui-bridge-api"
RUNTIME_REGISTRY="$UI_RUNTIME/capability_registry.json"
DROPIN_DIR="/etc/systemd/system/${UI_SERVICE}.d"
DROPIN_PATH="$DROPIN_DIR/zz-ndsp-m2-governed.conf"
AUTH_SESSION_URL="http://127.0.0.1:19091/api/auth/session"
AUTH_HEALTH_URL="http://127.0.0.1:19091/health"
AUTH_VERSION_URL="http://127.0.0.1:19091/api/auth/version"
MY_SITE_LINK="/etc/nginx/sites-enabled/ndsp-prelaunch-my.ndsp.app.conf"

section(){ printf '\n============================================================\n%s\n============================================================\n' "$1"; }
kv(){ printf '%s=%s\n' "$1" "$2"; }
die(){ printf 'ERROR=%s\nFINAL_STATUS=NDSP_M2_MASTER_FAIL\n' "$1"; exit 1; }

cleanup(){ rm -rf "$CANDIDATE" >/dev/null 2>&1 || true; }
trap cleanup EXIT

section "NDSP M2 — GOVERNED MASTER IMPLEMENTATION"
kv MODE "GATED_IMPLEMENTATION"
kv ROOT "$ROOT"
kv BRANCH "$BRANCH"
kv APPLY "$APPLY"
kv UTC "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

[[ "$ROOT" == "$CANONICAL_ROOT" ]] || die UNSUPPORTED_CANONICAL_ROOT
[[ -d "$ROOT" ]] || die CANONICAL_ROOT_MISSING
for cmd in git bash python3 npm rsync curl sudo systemctl; do
  command -v "$cmd" >/dev/null 2>&1 || die "MISSING_COMMAND_${cmd}"
done
mkdir -p "$EVIDENCE_ROOT" "$CHECKPOINT"

section "1/7 — CANONICAL SNAPSHOT + REMOTE SOURCE IDENTITY"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  kv CANONICAL_SOURCE_TYPE GIT_WORKTREE
  git -C "$ROOT" status --porcelain=v1 > "$EVIDENCE_ROOT/canonical-status-before.txt"
  git -C "$ROOT" rev-parse HEAD > "$EVIDENCE_ROOT/canonical-head-before.txt"
else
  kv CANONICAL_SOURCE_TYPE SOURCE_SNAPSHOT_NO_GIT_METADATA
  printf 'SOURCE_SNAPSHOT_NO_GIT_METADATA\n' > "$EVIDENCE_ROOT/canonical-status-before.txt"
  printf 'SOURCE_SNAPSHOT_NO_GIT_METADATA\n' > "$EVIDENCE_ROOT/canonical-head-before.txt"
fi
readlink -f "$LIVE_LINK" > "$EVIDENCE_ROOT/live-release-before.txt" 2>/dev/null || true
REMOTE_HEAD="$(git ls-remote "$REPO_URL" "refs/heads/$BRANCH" | awk 'NR==1{print $1}')"
[[ "$REMOTE_HEAD" =~ ^[0-9a-f]{40}$ ]] || die REMOTE_BRANCH_NOT_RESOLVED
kv REMOTE_HEAD "$REMOTE_HEAD"
kv LIVE_RELEASE_BEFORE "$(cat "$EVIDENCE_ROOT/live-release-before.txt" 2>/dev/null || true)"

section "2/7 — ISOLATED CANDIDATE"
git clone --filter=blob:none --single-branch --branch "$BRANCH" "$REPO_URL" "$CANDIDATE" 2>&1 | tee "$EVIDENCE_ROOT/git-clone.txt"
git -C "$CANDIDATE" checkout --detach "$REMOTE_HEAD" >/dev/null 2>&1
CANDIDATE_SHA="$(git -C "$CANDIDATE" rev-parse HEAD)"
[[ "$CANDIDATE_SHA" == "$REMOTE_HEAD" ]] || die CANDIDATE_SHA_MISMATCH
kv CANDIDATE_SHA "$CANDIDATE_SHA"

CERTIFIER="$CANDIDATE/scripts/NDSP_M2_FINAL_READONLY_CERTIFIER.sh"
RECONCILER="$CANDIDATE/scripts/NDSP_NAW27_CAPABILITY_RECONCILE.py"
[[ -f "$CERTIFIER" ]] || die CERTIFIER_NOT_FOUND
[[ -f "$RECONCILER" ]] || die RECONCILER_NOT_FOUND

section "3/7 — INDEPENDENT SOURCE CERTIFICATION"
set +e
bash "$CERTIFIER" "$CANDIDATE" 2>&1 | tee "$EVIDENCE_ROOT/certifier.txt"
CERT_RC=${PIPESTATUS[0]}
set -e
kv CERTIFIER_RC "$CERT_RC"
if [[ "$CERT_RC" -eq 2 ]]; then
  kv PRODUCTION_FILES_MODIFIED 0
  kv SERVICES_RESTARTED 0
  kv DATABASE_MODIFIED 0
  kv NGINX_MODIFIED 0
  kv SYSTEMD_MODIFIED 0
  kv FINAL_STATUS NDSP_M2_MASTER_BLOCKED_BY_CERTIFIER
  exit 2
fi
[[ "$CERT_RC" -eq 0 ]] || die CERTIFIER_FAILED

section "4/7 — BUILD + CAP REGISTRY + RUNTIME PREFLIGHT"
FE="$CANDIDATE/frontend/ndsp-sovereign-meridian-ui"
(
  cd "$FE"
  npm ci --ignore-scripts --no-audit --no-fund
  node --test tests/governed-analysis-state-machine.test.mjs
  npm run typecheck
  npm run build
) 2>&1 | tee "$EVIDENCE_ROOT/candidate-build.txt"
[[ -f "$FE/dist/client/index.html" ]] || die CANDIDATE_BUILD_OUTPUT_MISSING

REGISTRY_BUILD="$EVIDENCE_ROOT/capability_registry.json"
python3 "$RECONCILER" --root "$CANDIDATE" --output "$REGISTRY_BUILD" --expected-count 311 2>&1 | tee "$EVIDENCE_ROOT/capability-reconcile.txt"
python3 - "$REGISTRY_BUILD" <<'PY' || die CAPABILITY_REGISTRY_SEMANTICS_FAILED
import json, sys
p=json.load(open(sys.argv[1],encoding='utf-8'))
assert p['global_reconciled'] is True
assert p['record_count']==311
assert p['parsed_record_count']==311
assert p['silent_omission_count']==0
assert p['parse_error_count']==0
assert p['semantics']['record_count_is_runtime_capability_count'] is False
assert p['semantics']['activation_claim'] is False
print('CAPABILITY_REGISTRY_ARTIFACT=PASS')
PY

[[ -d "$UI_RUNTIME" ]] || die UI_BRIDGE_RUNTIME_DIR_MISSING
[[ -f "$UI_RUNTIME/main.py" ]] || die UI_BRIDGE_RUNTIME_MAIN_MISSING
[[ -x "$UI_RUNTIME/venv/bin/uvicorn" ]] || die UI_BRIDGE_RUNTIME_UVICORN_MISSING
systemctl is-active --quiet ndsp-auth-core-clean.service || die AUTH_CORE_SERVICE_NOT_ACTIVE

AUTH_HEALTH_CODE="$(curl -sS --connect-timeout 3 --max-time 8 -o "$EVIDENCE_ROOT/auth-health.json" -w '%{http_code}' "$AUTH_HEALTH_URL" || true)"
AUTH_VERSION_CODE="$(curl -sS --connect-timeout 3 --max-time 8 -o "$EVIDENCE_ROOT/auth-version.json" -w '%{http_code}' "$AUTH_VERSION_URL" || true)"
AUTH_SESSION_CODE="$(curl -sS --connect-timeout 3 --max-time 8 -o "$EVIDENCE_ROOT/auth-session-unauth.json" -w '%{http_code}' "$AUTH_SESSION_URL" || true)"
kv AUTH_HEALTH_HTTP "$AUTH_HEALTH_CODE"
kv AUTH_VERSION_HTTP "$AUTH_VERSION_CODE"
kv AUTH_SESSION_UNAUTH_HTTP "$AUTH_SESSION_CODE"
[[ "$AUTH_HEALTH_CODE" == "200" ]] || die AUTH_CORE_HEALTH_FAILED
[[ "$AUTH_VERSION_CODE" == "200" ]] || die AUTH_CORE_VERSION_FAILED
[[ "$AUTH_SESSION_CODE" == "401" ]] || die AUTH_CORE_UNAUTH_SESSION_CONTRACT_FAILED
python3 - "$EVIDENCE_ROOT/auth-version.json" <<'PY' || die AUTH_CORE_IDENTITY_FAILED
import json, sys
p=json.load(open(sys.argv[1],encoding='utf-8'))
a=p.get('authCore') or {}
assert p.get('ok') is True
assert a.get('service') == 'ndsp-auth-core-clean'
print('AUTH_CORE_IDENTITY=PASS')
PY

MY_SITE_REAL="$(readlink -f "$MY_SITE_LINK" 2>/dev/null || true)"
[[ -f "$MY_SITE_REAL" ]] || die MY_NDSP_NGINX_SITE_NOT_FOUND
NGINX_PATCHED="$EVIDENCE_ROOT/my.ndsp.app.conf.candidate"
python3 - "$MY_SITE_REAL" "$NGINX_PATCHED" <<'PY' || die NGINX_ROUTE_PREFLIGHT_FAILED
from pathlib import Path
import sys
src=Path(sys.argv[1]); out=Path(sys.argv[2])
text=src.read_text(encoding='utf-8')
begin='# NDSP_CANONICAL_AUTH_V13_BEGIN'
end='# NDSP_CANONICAL_AUTH_V13_END'
if text.count(begin)!=1 or text.count(end)!=1:
    raise SystemExit('AUTH_MARKER_COUNT_INVALID')
a=text.index(begin); b=text.index(end,a)
block=text[a:b]
old='proxy_pass http://127.0.0.1:9001;'
new='proxy_pass http://127.0.0.1:19091;'
if old in block:
    if block.count(old)!=1: raise SystemExit('AUTH_PROXY_COUNT_INVALID')
    block=block.replace(old,new,1)
elif block.count(new)!=1:
    raise SystemExit('AUTH_PROXY_TARGET_UNEXPECTED')
text=text[:a]+block+text[b:]
ui_begin='# NDSP_M2_UI_BRIDGE_BEGIN'
ui_end='# NDSP_M2_UI_BRIDGE_END'
ui_block='''    # NDSP_M2_UI_BRIDGE_BEGIN\n    location ^~ /api/ui-bridge/ {\n        proxy_pass http://127.0.0.1:9066;\n        proxy_http_version 1.1;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n        proxy_set_header X-Forwarded-Host $host;\n        proxy_set_header X-Forwarded-Port $server_port;\n        proxy_set_header Authorization $http_authorization;\n        proxy_set_header Cookie $http_cookie;\n        proxy_connect_timeout 5s;\n        proxy_read_timeout 60s;\n        proxy_send_timeout 60s;\n        add_header Cache-Control "no-store" always;\n    }\n    # NDSP_M2_UI_BRIDGE_END\n\n'''
if ui_begin in text or ui_end in text:
    if text.count(ui_begin)!=1 or text.count(ui_end)!=1:
        raise SystemExit('UI_BRIDGE_MARKER_COUNT_INVALID')
    ua=text.index(ui_begin); ub=text.index(ui_end,ua)
    existing=text[ua:ub]
    if 'proxy_pass http://127.0.0.1:9066;' not in existing:
        raise SystemExit('UI_BRIDGE_EXISTING_TARGET_INVALID')
else:
    needle='    location ^~ /api/ {\n        proxy_pass http://127.0.0.1:9001;'
    if text.count(needle)!=1:
        raise SystemExit('GENERIC_API_INSERTION_ANCHOR_INVALID')
    text=text.replace(needle,ui_block+needle,1)
out.write_text(text,encoding='utf-8')
print('NGINX_RUNTIME_ROUTE_CANDIDATE=PASS')
PY

grep -q 'proxy_pass http://127.0.0.1:19091;' "$NGINX_PATCHED" || die NGINX_AUTH_PATCH_NOT_PRESENT
grep -q 'proxy_pass http://127.0.0.1:9066;' "$NGINX_PATCHED" || die NGINX_UI_BRIDGE_PATCH_NOT_PRESENT

if [[ "$APPLY" != "YES" ]]; then
  kv CAPABILITY_REGISTRY "$REGISTRY_BUILD"
  kv PROJECT_FILES_MODIFIED 0
  kv PRODUCTION_FILES_MODIFIED 0
  kv SERVICES_RESTARTED 0
  kv DATABASE_MODIFIED 0
  kv NGINX_MODIFIED 0
  kv SYSTEMD_MODIFIED 0
  kv FINAL_STATUS NDSP_M2_MASTER_VERIFIED_NOT_APPLIED
  exit 0
fi

section "5/7 — CHECKPOINT"
TARGETS=(
  "apps/ndsp-ui-bridge-api/main.py"
  "apps/ndsp-ui-bridge-api/main_governed.py"
  "infrastructure/systemd/ndsp-ui-bridge-api-m2-governed.conf"
  "frontend/ndsp-sovereign-meridian-ui/src/App.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis-governance.css"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis/AnalysisContext.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis/stateMachine.ts"
  "frontend/ndsp-sovereign-meridian-ui/src/analysis/types.ts"
  "frontend/ndsp-sovereign-meridian-ui/src/api/decision.ts"
  "frontend/ndsp-sovereign-meridian-ui/src/auth/RequireUser.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/main.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/pages/AnalysisPage.tsx"
  "frontend/ndsp-sovereign-meridian-ui/src/pages/AnalysisSetupPage.tsx"
  "frontend/ndsp-sovereign-meridian-ui/tests/governed-analysis-state-machine.test.mjs"
  ".github/workflows/naw27-m2-certify.yml"
  "scripts/NDSP_NAW27_CAPABILITY_RECONCILE.py"
  "scripts/NDSP_M2_GOVERNED_MASTER_IMPLEMENT.sh"
  "scripts/NDSP_M2_FINAL_READONLY_CERTIFIER.sh"
)
for rel in "${TARGETS[@]}"; do [[ -f "$CANDIDATE/$rel" ]] || die "CANDIDATE_TARGET_MISSING:$rel"; done

mkdir -p "$CHECKPOINT/source"
: > "$CHECKPOINT/source-new-files.txt"
for rel in "${TARGETS[@]}"; do
  if [[ -f "$ROOT/$rel" ]]; then
    mkdir -p "$CHECKPOINT/source/$(dirname "$rel")"
    cp -a "$ROOT/$rel" "$CHECKPOINT/source/$rel"
  else
    printf '%s\n' "$rel" >> "$CHECKPOINT/source-new-files.txt"
  fi
done

if [[ -f "$RUNTIME_REGISTRY" ]]; then cp -a "$RUNTIME_REGISTRY" "$CHECKPOINT/capability_registry.before.json"; printf 'YES\n' > "$CHECKPOINT/registry-existed.txt"; else printf 'NO\n' > "$CHECKPOINT/registry-existed.txt"; fi
if sudo test -f "$DROPIN_PATH"; then sudo cp -a "$DROPIN_PATH" "$CHECKPOINT/dropin.before.conf"; printf 'YES\n' > "$CHECKPOINT/dropin-existed.txt"; else printf 'NO\n' > "$CHECKPOINT/dropin-existed.txt"; fi
sudo cp -a "$MY_SITE_REAL" "$CHECKPOINT/my.ndsp.app.conf.before"
LIVE_BEFORE="$(readlink -f "$LIVE_LINK" 2>/dev/null || true)"
printf '%s\n' "$LIVE_BEFORE" > "$CHECKPOINT/live-release-before.txt"
systemctl cat "$UI_SERVICE" > "$EVIDENCE_ROOT/ui-service-before.txt" 2>&1 || die UI_SERVICE_NOT_READABLE

rollback(){
  set +e
  if [[ -d "$CHECKPOINT/source" ]]; then cp -a "$CHECKPOINT/source/." "$ROOT/"; fi
  if [[ -f "$CHECKPOINT/source-new-files.txt" ]]; then while IFS= read -r rel; do [[ -n "$rel" ]] && rm -f "$ROOT/$rel"; done < "$CHECKPOINT/source-new-files.txt"; fi
  if [[ "$(cat "$CHECKPOINT/registry-existed.txt" 2>/dev/null)" == "YES" ]]; then cp -a "$CHECKPOINT/capability_registry.before.json" "$RUNTIME_REGISTRY"; else rm -f "$RUNTIME_REGISTRY"; fi
  if [[ "$(cat "$CHECKPOINT/dropin-existed.txt" 2>/dev/null)" == "YES" ]]; then sudo mkdir -p "$DROPIN_DIR"; sudo cp -a "$CHECKPOINT/dropin.before.conf" "$DROPIN_PATH"; else sudo rm -f "$DROPIN_PATH"; fi
  sudo cp -a "$CHECKPOINT/my.ndsp.app.conf.before" "$MY_SITE_REAL" 2>/dev/null || true
  if [[ -n "$LIVE_BEFORE" && -d "$LIVE_BEFORE" ]]; then sudo ln -sfn "$LIVE_BEFORE" "$LIVE_LINK"; fi
  sudo systemctl daemon-reload >/dev/null 2>&1 || true
  sudo nginx -t >/dev/null 2>&1 && sudo systemctl reload nginx >/dev/null 2>&1 || true
  sudo systemctl restart "$UI_SERVICE" >/dev/null 2>&1 || true
  printf 'ROLLBACK_EXECUTED=YES\n' | tee -a "$EVIDENCE_ROOT/apply.txt"
  set -e
}

section "6/7 — CONTROLLED APPLY"
for rel in "${TARGETS[@]}"; do mkdir -p "$ROOT/$(dirname "$rel")"; cp -a "$CANDIDATE/$rel" "$ROOT/$rel"; done
cp -a "$REGISTRY_BUILD" "$RUNTIME_REGISTRY"
sudo mkdir -p "$DROPIN_DIR"
sudo install -m 0644 "$CANDIDATE/infrastructure/systemd/ndsp-ui-bridge-api-m2-governed.conf" "$DROPIN_PATH"
sudo cp -a "$NGINX_PATCHED" "$MY_SITE_REAL"
if ! sudo nginx -t; then rollback; die NGINX_CONFIG_TEST_FAILED; fi
if ! sudo systemctl reload nginx; then rollback; die NGINX_RELOAD_FAILED; fi
sudo systemctl daemon-reload

RELEASE="$LIVE_ROOT/releases/${TS}-ndsp-m2-governed"
sudo mkdir -p "$RELEASE"
sudo rsync -a --delete "$FE/dist/client/" "$RELEASE/"
sudo ln -sfn "$RELEASE" "$LIVE_LINK"

if ! sudo systemctl restart "$UI_SERVICE"; then rollback; die UI_BRIDGE_RESTART_FAILED; fi
sleep 2
if ! systemctl is-active --quiet "$UI_SERVICE"; then rollback; die UI_BRIDGE_NOT_ACTIVE_AFTER_RESTART; fi
systemctl show "$UI_SERVICE" -p ExecStart -p WorkingDirectory > "$EVIDENCE_ROOT/ui-service-show-after.txt" 2>&1 || true
grep -q 'main_governed:app' "$EVIDENCE_ROOT/ui-service-show-after.txt" || { rollback; die GOVERNED_ENTRYPOINT_NOT_ACTIVE; }
cmp -s "$REGISTRY_BUILD" "$RUNTIME_REGISTRY" || { rollback; die RUNTIME_REGISTRY_PARITY_FAILED; }
curl -fsS "http://127.0.0.1:9066/api/ui-bridge/health" > "$EVIDENCE_ROOT/ui-bridge-health.json" || { rollback; die UI_BRIDGE_HEALTH_FAILED; }
LOCAL_GUARD_CODE="$(curl -sS -o "$EVIDENCE_ROOT/ui-bridge-unauth-local.json" -w '%{http_code}' http://127.0.0.1:9066/api/ui-bridge/analysis/setup/options || true)"
[[ "$LOCAL_GUARD_CODE" == "401" || "$LOCAL_GUARD_CODE" == "403" ]] || { rollback; die LOCAL_UI_BRIDGE_AUTH_GUARD_FAILED; }
PUBLIC_AUTH_CODE="$(curl -ksS -o "$EVIDENCE_ROOT/public-auth-session.json" -w '%{http_code}' https://my.ndsp.app/api/auth/session || true)"
[[ "$PUBLIC_AUTH_CODE" == "200" || "$PUBLIC_AUTH_CODE" == "401" || "$PUBLIC_AUTH_CODE" == "403" ]] || { rollback; die PUBLIC_AUTH_ROUTE_FAILED; }
PUBLIC_UI_CODE="$(curl -ksS -o "$EVIDENCE_ROOT/public-ui-bridge-unauth.json" -w '%{http_code}' https://my.ndsp.app/api/ui-bridge/analysis/setup/options || true)"
[[ "$PUBLIC_UI_CODE" == "401" || "$PUBLIC_UI_CODE" == "403" ]] || { rollback; die PUBLIC_UI_BRIDGE_ROUTE_FAILED; }
curl -kfsS "https://my.ndsp.app/analysis/setup" > /dev/null || { rollback; die LIVE_ANALYSIS_SETUP_ROUTE_FAILED; }

section "7/7 — POST-APPLY CERTIFICATION"
set +e
NDSP_M2_LIVE_BASE="https://my.ndsp.app" NDSP_M2_EXPECT_RUNTIME_GOVERNED="YES" bash "$CERTIFIER" "$CANDIDATE" 2>&1 | tee "$EVIDENCE_ROOT/post-apply-certifier.txt"
POST_RC=${PIPESTATUS[0]}
set -e
if [[ "$POST_RC" -ne 0 ]]; then rollback; die POST_APPLY_CERTIFIER_FAILED; fi

kv CHECKPOINT "$CHECKPOINT"
kv RELEASE "$RELEASE"
kv CAPABILITY_REGISTRY "$RUNTIME_REGISTRY"
kv PROJECT_FILES_MODIFIED "${#TARGETS[@]}"
kv PRODUCTION_FILES_MODIFIED 6
kv SERVICES_RESTARTED 1
kv DATABASE_MODIFIED 0
kv NGINX_MODIFIED 1
kv SYSTEMD_MODIFIED 1
kv FINAL_STATUS NDSP_M2_MASTER_IMPLEMENTATION_PASS
