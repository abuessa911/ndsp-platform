#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
LIVE="/var/www/ndsp-my"
PREMIUM="$LIVE/_premium"
ASSETS="$PREMIUM/assets"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V5013_NMP_TIMEFRAME_TRUTH_FIX_$TS.md"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v5013-nmp-timeframe-truth-$TS"
CHECKPOINT="$HOME_DIR/ndsp_release_checkpoints/NDSP_V5013_NMP_TIMEFRAME_TRUTH_FIX_$TS"
mkdir -p "$HOME_DIR/ndsp_launch_reports" "$HOME_DIR/ndsp_launch_backups" "$HOME_DIR/ndsp_release_checkpoints"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
if [ "$(id -u)" != "0" ]; then log "ERROR=RUN_WITH_SUDO"; exit 1; fi
[ -d "$PREMIUM" ] || { log "ERROR=PREMIUM_NOT_FOUND"; exit 1; }
mkdir -p "$BACKUP" "$CHECKPOINT"
cp -a "$PREMIUM" "$BACKUP/_premium.before_v5013"
cat > "$ASSETS/v5013-nmp-tf-truth.js" <<'JS'
(function(){
 if(window.__NMP_TF_TRUTH__)return; window.__NMP_TF_TRUTH__=true;
 const frames=['W1','D1','H4','H1','M15'];
 const fmt=v=>{const n=Number(String(v??'').replace(/,/g,''));return Number.isFinite(n)?n.toLocaleString('en-US',{maximumFractionDigits:2}):(v||'—')};
 const canon=t=>{t=String(t||'').toUpperCase(); if(t==='1D'||t==='D')return'D1'; if(t==='1W'||t==='W')return'W1'; if(t==='4H')return'H4'; if(t==='1H')return'H1'; if(t==='15M')return'M15'; return t};
 const params=new URLSearchParams(location.search);
 const sym=(params.get('symbol')||localStorage.getItem('ndsp_selected_symbol')||'BTCUSDT').toUpperCase().replace(/[^A-Z0-9._:-]/g,'');
 function setBox(label, text){document.querySelectorAll('.v501-box small').forEach(s=>{if((s.textContent||'').includes(label)){const b=s.parentElement.querySelector('b'); if(b)b.textContent=text;}})}
 function rewriteTabs(selected, sourceTf){
   const tabs=document.querySelector('.v501-tabs'); if(!tabs)return;
   tabs.innerHTML=frames.map(tf=>`<button class="${selected===tf?'on':''}" data-tf="${tf}">${tf}</button>`).join('');
   tabs.querySelectorAll('button').forEach(b=>b.onclick=()=>{location.href=location.pathname+'?symbol='+encodeURIComponent(sym)+'&tf='+b.dataset.tf});
   document.querySelectorAll('.v501-badge').forEach(x=>{ if((x.textContent||'').includes('الفريم المتصل')) x.textContent='الفريم المتصل من المصدر: '+(sourceTf||'غير مرسل'); });
 }
 async function run(){
   if(!location.pathname.includes('/nmp.html') && !location.pathname.includes('/decision-center.html') && !location.pathname.includes('/decision-radar.html')) return;
   let d={}; try{const r=await fetch('/api/decision/quality-live?symbol='+encodeURIComponent(sym),{cache:'no-store'}); if(r.ok)d=await r.json()}catch(e){}
   const nmp=d.nmp||{};
   const sourceTf=canon(d.nmp_timeframe||nmp.timeframe||'');
   let selected=canon(new URLSearchParams(location.search).get('tf')||sourceTf||'D1');
   const level=d.nmp_level ?? nmp.level ?? nmp.value;
   const status=d.nmp_status ?? nmp.status ?? (level?'AVAILABLE':'غير موصول');
   const connected=!!level && selected===sourceTf;
   if(location.pathname.includes('/nmp.html')){
     rewriteTabs(selected,sourceTf);
     setBox('NMP', connected?fmt(level):'غير موصول لهذا الفريم');
     setBox('الحالة', connected?status:'بانتظار ربط مستقل');
     document.querySelectorAll('.v501-note').forEach(n=>{n.textContent='لا يتم عرض NMP لفريم غير متصل. كل فريم يحتاج قيمة مستقلة من الباك إند.'});
   }
   if(location.pathname.includes('/decision-center.html')){
     setBox('NMP المتصل', level?`مستوى NMP: ${fmt(level)} · الفريم: ${sourceTf||'—'} · الحالة: ${status}`:'غير موصول من المصدر');
   }
   document.querySelectorAll('.v501-node small').forEach(s=>{if((s.textContent||'').trim()==='NMP')s.textContent='تحقق NMP'});
 }
 setTimeout(run,500); setTimeout(run,1200); setTimeout(run,2200);
})();
JS
for f in "$PREMIUM/nmp.html" "$PREMIUM/decision-center.html" "$PREMIUM/decision-radar.html"; do
  [ -f "$f" ] || continue
  python3 - "$f" "$TS" <<'PY'
import re,sys
p,ts=sys.argv[1],sys.argv[2]
s=open(p,encoding='utf-8').read()
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/v5013-nmp-tf-truth\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
s=s.replace('</body>',f'<script src="/_premium/assets/v5013-nmp-tf-truth.js?v={ts}"></script></body>')
open(p,'w',encoding='utf-8').write(s)
PY
  log "PATCHED=$f"
done
chown -R www-data:www-data "$PREMIUM" 2>/dev/null || true
cp -a "$PREMIUM" "$CHECKPOINT/_premium"
for p in nmp decision-center decision-radar; do
  out=/tmp/v5013_check.html
  code=$(curl -skL -o "$out" -w "%{http_code}" "https://my.ndsp.app/_premium/$p.html?symbol=BTCUSDT&v=$TS" || echo 000)
  size=$(wc -c < "$out" 2>/dev/null || echo 0)
  refs=$(grep -Ec 'v5013-nmp-tf-truth\.js' "$out" || true)
  old=$(grep -Ec '/_premium/assets/premium\.js' "$out" || true)
  obj=$(grep -c '\[object Object\]' "$out" || true)
  log "$p HTTP=$code SIZE=$size V5013_REFS=$refs OLD_PREMIUM_JS=$old OBJECT_TEXT=$obj"
done
log "FINAL_STATUS=NDSP_V5013_NMP_TIMEFRAME_TRUTH_FIX_DONE"
log "URL_NMP_D1=https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&tf=D1&v=$TS"
log "URL_NMP_H4=https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&tf=H4&v=$TS"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "CHECKPOINT=$CHECKPOINT"
log "REPORT=$REPORT"
