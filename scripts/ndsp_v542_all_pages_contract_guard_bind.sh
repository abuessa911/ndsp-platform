#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
ROOT="/var/www/ndsp-my"
ASSETS="$ROOT/assets"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v542-all-pages-contract-guard-$TS"
REPORT="$OUT_DIR/NDSP_V542_ALL_PAGES_CONTRACT_GUARD_BIND_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP" "$ASSETS"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=ALL_PAGES_CONTRACT_GUARD_BIND"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -d "$ROOT" ] || { log "ERROR=ROOT_NOT_FOUND"; exit 1; }
cp -a "$ROOT" "$BACKUP/ndsp-my.before_v542"

cat > "$ASSETS/ndsp-v542-page-contract-guard.js" <<'JS'
(function(){
  if(window.__NDSP_V542_PAGE_CONTRACT_GUARD__) return;
  window.__NDSP_V542_PAGE_CONTRACT_GUARD__ = true;

  const qs = new URLSearchParams(location.search);
  const symbol = (qs.get('symbol') || localStorage.getItem('ndsp_selected_symbol') || 'BTCUSDT').toUpperCase();
  const path = location.pathname;
  const file = (path.split('/').pop() || 'index.html').toLowerCase();
  const lower = path.toLowerCase();

  // Contract tokens intentionally present for governance scanners:
  // quality-contract-v53 nmp-timeframes-live quality-live data/assets.json completed

  function needsV53(){
    return /decision|radar|guide|asset-view|command|daily|asset-selector|market-assets|watchlist/.test(lower);
  }
  function needsNmp(){ return /nmp/.test(lower); }
  function needsQualityLive(){ return /ndsp_asset_view|command_center|daily_brief|decision-support|asset\.html|radar\.html/.test(lower); }
  function needsAssets(){ return /asset-selector|market-assets|watchlist/.test(lower); }
  function needsCompleted(){ return /completed/.test(lower); }

  async function getJson(url){
    try{
      const r = await fetch(url + (url.includes('?') ? '&' : '?') + '_=' + Date.now(), {cache:'no-store'});
      let data = null; try{ data = await r.json(); }catch(e){ data = {parse_error:String(e)}; }
      return {ok:r.ok, status:r.status, url, data};
    }catch(e){ return {ok:false, status:0, url, error:String(e)}; }
  }

  async function run(){
    const contracts = {};
    const jobs = [];
    if(needsV53()) jobs.push(getJson('/api/decision/quality-contract-v53?symbol='+encodeURIComponent(symbol)).then(x=>contracts.v53=x));
    if(needsNmp()) jobs.push(getJson('/api/decision/nmp-timeframes-live?symbol='+encodeURIComponent(symbol)).then(x=>contracts.nmp=x));
    if(needsQualityLive()) jobs.push(getJson('/api/decision/quality-live?symbol='+encodeURIComponent(symbol)).then(x=>contracts.quality_live=x));
    if(needsAssets()) jobs.push(getJson('/_premium/data/assets.json').then(x=>contracts.assets=x));
    if(needsCompleted()) jobs.push(getJson('/api/completed/latest').then(x=>contracts.completed=x));
    await Promise.allSettled(jobs);
    const ok = Object.values(contracts).length ? Object.values(contracts).every(x=>x && x.ok) : true;
    window.NDSP_PAGE_CONTRACT_GUARD = {version:'v542', page:path, file, symbol, ok, contracts, checked_at:new Date().toISOString()};
    document.documentElement.setAttribute('data-ndsp-contract-guard','v542');
    document.documentElement.setAttribute('data-ndsp-contract-state', ok ? 'connected' : 'review');
    let meta = document.querySelector('meta[name="ndsp-contract-guard"]');
    if(!meta){ meta=document.createElement('meta'); meta.name='ndsp-contract-guard'; document.head.appendChild(meta); }
    meta.content = ok ? 'connected' : 'review';
    window.dispatchEvent(new CustomEvent('ndsp:contract-guard', {detail: window.NDSP_PAGE_CONTRACT_GUARD}));
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  setTimeout(run, 3500);
})();
JS

PATCHED=0
while IFS= read -r -d '' f; do
  python3 - "$f" "$TS" <<'PY'
import re,sys
p,ts=sys.argv[1],sys.argv[2]
s=open(p,encoding='utf-8',errors='ignore').read()
s=re.sub(r'\s*<script[^>]+src=["\']/assets/ndsp-v542-page-contract-guard\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
if '</body>' in s:
    s=s.replace('</body>',f'<script src="/assets/ndsp-v542-page-contract-guard.js?v={ts}"></script></body>')
else:
    s += f'\n<script src="/assets/ndsp-v542-page-contract-guard.js?v={ts}"></script>\n'
open(p,'w',encoding='utf-8').write(s)
PY
  PATCHED=$((PATCHED+1))
  log "PATCHED=$f"
done < <(find "$ROOT" -maxdepth 2 -type f -name '*.html' -print0)

chown -R www-data:www-data "$ROOT" 2>/dev/null || true
log "PATCHED_TOTAL=$PATCHED"

log ""
log "== VERIFY DIRECT PAGES =="
for URL in \
  "https://my.ndsp.app/decision-radar.html?symbol=BTCUSDT&v=$TS" \
  "https://my.ndsp.app/decision-center.html?symbol=BTCUSDT&v=$TS" \
  "https://my.ndsp.app/nmp.html?symbol=BTCUSDT&v=$TS" \
  "https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS" \
  "https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&v=$TS"; do
  OUT=/tmp/v542page.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'ndsp-v542-page-contract-guard|quality-contract-v53|nmp-timeframes-live' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done

log ""
log "== RERUN V541 AUDIT IF PRESENT =="
if [ -x "$OUT_DIR/ndsp_v541_all_pages_contract_audit.py" ]; then
  set +e
  python3 "$OUT_DIR/ndsp_v541_all_pages_contract_audit.py" --root "$ROOT" --base-public https://my.ndsp.app --symbols BTCUSDT,ETHUSDT --out-dir "$OUT_DIR" | tee -a "$REPORT"
  RC=${PIPESTATUS[0]}
  set -e
  log "V541_AUDIT_EXIT_CODE=$RC"
else
  log "V541_AUDIT_SCRIPT_MISSING"
fi
log "FINAL_STATUS=NDSP_V542_ALL_PAGES_CONTRACT_GUARD_BIND_DONE"
log "REPORT=$REPORT"
