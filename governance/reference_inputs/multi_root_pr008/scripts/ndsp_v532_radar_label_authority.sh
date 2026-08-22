#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
PRE="/var/www/ndsp-my/_premium"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V532_RADAR_LABEL_AUTHORITY_$TS.md"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v532-radar-label-authority-$TS"
mkdir -p "$HOME_DIR/ndsp_launch_reports" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -d "$PRE" ] || { log "ERROR=PREMIUM_NOT_FOUND"; exit 1; }
cp -a "$PRE" "$BACKUP/_premium.before_v532_authority"

cat > "$PRE/assets/v532-radar-label-authority.js" <<'JS'
(function(){
  if(window.__NDSP_V532_RADAR_LABEL_AUTHORITY__) return;
  window.__NDSP_V532_RADAR_LABEL_AUTHORITY__ = true;

  const qs = new URLSearchParams(location.search);
  const symbol = (qs.get('symbol') || localStorage.getItem('ndsp_selected_symbol') || 'BTCUSDT').toUpperCase();
  let latest = null;
  let applying = false;

  function asNum(v){ const n = Number(v); return Number.isFinite(n) ? n : null; }
  function riskLabel(score){
    score = asNum(score);
    if(score === null) return 'غير موصول';
    if(score <= 35) return 'منخفض';
    if(score <= 65) return 'حذر';
    if(score <= 79) return 'مرتفع';
    return 'حرج';
  }
  function devilLabel(score){
    score = asNum(score);
    if(score === null) return 'غير موصول';
    if(score <= 35) return 'اجتاز';
    if(score <= 65) return 'اعتراض خفيف';
    if(score <= 79) return 'اعتراض قوي';
    return 'اعتراض حاسم';
  }
  function setNode(label, value){
    document.querySelectorAll('.v501-node').forEach(node=>{
      const small = node.querySelector('small');
      const bold = node.querySelector('b');
      if(small && bold && (small.textContent || '').includes(label) && bold.textContent !== value){
        bold.textContent = value;
      }
    });
  }
  function setBox(label, value){
    document.querySelectorAll('.v501-box small').forEach(small=>{
      if((small.textContent || '').includes(label)){
        const bold = small.parentElement && small.parentElement.querySelector('b');
        if(bold && bold.textContent !== value) bold.textContent = value;
      }
    });
  }
  function setNote(text){
    document.querySelectorAll('.v501-note').forEach(note=>{
      const t = note.textContent || '';
      if(t.includes('المخاطر') || t.includes('محامي الشيطان') || t.includes('JSON') || t.includes('التقييم عكسي')){
        if(note.textContent !== text) note.textContent = text;
      }
    });
  }
  function apply(){
    if(!latest || applying) return;
    applying = true;
    try{
      const r = riskLabel(latest.risk_score);
      const d = devilLabel(latest.devil_advocate_score);
      setNode('المخاطر', r);
      setNode('محامي الشيطان', d);
      setBox('المخاطر', r + (latest.risk_score != null ? ' · ' + latest.risk_score : ''));
      setBox('محامي الشيطان', d + (latest.devil_advocate_score != null ? ' · ' + latest.devil_advocate_score : ''));
      setNote('المخاطر ومحامي الشيطان متصلان. التقييم عكسي: الأقل أفضل. التصنيف الحالي: المخاطر ' + r + '، ومحامي الشيطان ' + d + '.');
    } finally {
      applying = false;
    }
  }
  async function load(){
    try{
      const res = await fetch('/api/decision/quality-contract-v53?symbol=' + encodeURIComponent(symbol) + '&_=' + Date.now(), {cache:'no-store'});
      latest = await res.json();
      apply();
    }catch(e){}
  }
  load();
  [300,800,1500,2500,4000,6500,9000,13000].forEach(ms=>setTimeout(()=>{load(); apply();}, ms));
  setInterval(apply, 1200);
  try{
    const mo = new MutationObserver(()=>{ setTimeout(apply, 60); });
    mo.observe(document.documentElement, {subtree:true, childList:true, characterData:true});
  }catch(e){}
})();
JS

for f in "$PRE/decision-radar.html" "$PRE/decision-center.html"; do
  [ -f "$f" ] || continue
  python3 - "$f" "$TS" <<'PY'
import re,sys
p,ts=sys.argv[1],sys.argv[2]
s=open(p,encoding='utf-8').read()
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/v532-radar-label-authority\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
s=s.replace('</body>',f'<script src="/_premium/assets/v532-radar-label-authority.js?v={ts}"></script></body>')
open(p,'w',encoding='utf-8').write(s)
PY
  log "PATCHED=$f"
done
chown -R www-data:www-data "$PRE" 2>/dev/null || true

log ""
log "== VERIFY =="
for URL in \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS" \
  "https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"; do
  OUT="/tmp/v532_authority.out"
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'v532-radar-label-authority|risk_score|devil_advocate_score' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json, urllib.request
d=json.loads(urllib.request.urlopen('https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT',timeout=10).read().decode())
print('risk_score='+str(d.get('risk_score')))
print('devil_advocate_score='+str(d.get('devil_advocate_score')))
PY
log "FINAL_STATUS=NDSP_V532_RADAR_LABEL_AUTHORITY_DONE"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "REPORT=$REPORT"
