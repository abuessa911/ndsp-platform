#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
LIVE="/var/www/ndsp-my"
PREMIUM="$LIVE/_premium"
ASSETS="$PREMIUM/assets"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V5012_NMP_DISPLAY_FIX_$TS.md"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v5012-nmp-display-$TS"
CHECKPOINT="$HOME_DIR/ndsp_release_checkpoints/NDSP_V5012_NMP_DISPLAY_FIX_$TS"
mkdir -p "$HOME_DIR/ndsp_launch_reports" "$HOME_DIR/ndsp_launch_backups" "$HOME_DIR/ndsp_release_checkpoints"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
if [ "$(id -u)" != "0" ]; then log "ERROR=RUN_WITH_SUDO"; exit 1; fi
[ -d "$PREMIUM" ] || { log "ERROR=PREMIUM_NOT_FOUND"; exit 1; }
mkdir -p "$BACKUP" "$CHECKPOINT"
cp -a "$PREMIUM" "$BACKUP/_premium.before_v5012"
cat > "$ASSETS/v5012-nmp-display.js" <<'JS'
(function(){
 if(window.__NMP_DISPLAY_FIX__)return; window.__NMP_DISPLAY_FIX__=true;
 const fmt=v=>{const n=Number(String(v??'').replace(/,/g,''));return Number.isFinite(n)?n.toLocaleString('en-US',{maximumFractionDigits:2}):(v||'—')};
 const sym=(new URLSearchParams(location.search).get('symbol')||localStorage.getItem('ndsp_selected_symbol')||'BTCUSDT').toUpperCase().replace(/[^A-Z0-9._:-]/g,'');
 function setBox(label, text){document.querySelectorAll('.v501-box small').forEach(s=>{if((s.textContent||'').includes(label)){const b=s.parentElement.querySelector('b'); if(b)b.textContent=text;}})}
 function renameRadar(){document.querySelectorAll('.v501-node small').forEach(s=>{if((s.textContent||'').trim()==='NMP')s.textContent='تحقق NMP';});}
 async function run(){
   let d={}; try{const r=await fetch('/api/decision/quality-live?symbol='+encodeURIComponent(sym),{cache:'no-store'}); if(r.ok)d=await r.json()}catch(e){}
   const nmp=d.nmp||{};
   const level=d.nmp_level ?? nmp.level ?? nmp.value;
   const tf=d.nmp_timeframe ?? nmp.timeframe ?? '—';
   const status=d.nmp_status ?? nmp.status ?? (level?'AVAILABLE':'غير موصول');
   if(location.pathname.includes('decision-center')) setBox('NMP المتصل', level?`مستوى NMP: ${fmt(level)} · الفريم: ${tf} · الحالة: ${status}`:'غير موصول من المصدر');
   if(location.pathname.includes('nmp')){setBox('NMP', level?fmt(level):'بانتظار ربط NMP مستقل');setBox('الحالة', status);}
   renameRadar();
 }
 setTimeout(run,700); setTimeout(run,1600);
})();
JS
for f in "$PREMIUM/decision-center.html" "$PREMIUM/decision-radar.html" "$PREMIUM/nmp.html"; do
  [ -f "$f" ] || continue
  python3 - "$f" "$TS" <<'PY'
import re,sys
p,ts=sys.argv[1],sys.argv[2]
s=open(p,encoding='utf-8').read()
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/v5012-nmp-display\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
s=s.replace('</body>',f'<script src="/_premium/assets/v5012-nmp-display.js?v={ts}"></script></body>')
open(p,'w',encoding='utf-8').write(s)
PY
  log "PATCHED=$f"
done
chown -R www-data:www-data "$PREMIUM" 2>/dev/null || true
cp -a "$PREMIUM" "$CHECKPOINT/_premium"
for p in decision-center decision-radar nmp; do
  out=/tmp/v5012_check.html
  code=$(curl -skL -o "$out" -w "%{http_code}" "https://my.ndsp.app/_premium/$p.html?symbol=BTCUSDT&v=$TS" || echo 000)
  size=$(wc -c < "$out" 2>/dev/null || echo 0)
  refs=$(grep -Ec 'v5012-nmp-display\.js' "$out" || true)
  old=$(grep -Ec '/_premium/assets/premium\.js' "$out" || true)
  obj=$(grep -c '\[object Object\]' "$out" || true)
  log "$p HTTP=$code SIZE=$size V5012_REFS=$refs OLD_PREMIUM_JS=$old OBJECT_TEXT=$obj"
done
log "FINAL_STATUS=NDSP_V5012_NMP_DISPLAY_FIX_DONE"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "URL_NMP=https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&v=$TS"
log "CHECKPOINT=$CHECKPOINT"
log "REPORT=$REPORT"
