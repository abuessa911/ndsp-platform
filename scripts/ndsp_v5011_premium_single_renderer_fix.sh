#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
LIVE="/var/www/ndsp-my"
PREMIUM="$LIVE/_premium"
REAL_USER="${SUDO_USER:-nawaf511}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$REAL_HOME/ndsp_launch_reports/NDSP_V5011_PREMIUM_SINGLE_RENDERER_FIX_$TS.md"
BACKUP="$REAL_HOME/ndsp_launch_backups/ndsp-v5011-premium-single-renderer-$TS"
CHECKPOINT="$REAL_HOME/ndsp_release_checkpoints/NDSP_V5011_PREMIUM_SINGLE_RENDERER_FIX_$TS"
mkdir -p "$REAL_HOME/ndsp_launch_reports" "$REAL_HOME/ndsp_launch_backups" "$REAL_HOME/ndsp_release_checkpoints"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
if [ "$(id -u)" != "0" ]; then log "ERROR=RUN_WITH_SUDO"; exit 1; fi
[ -d "$PREMIUM" ] || { log "ERROR=PREMIUM_NOT_FOUND"; exit 1; }
mkdir -p "$BACKUP" "$CHECKPOINT"
cp -a "$PREMIUM" "$BACKUP/_premium.before_v5011"
log "BACKUP=$BACKUP/_premium.before_v5011"
PAGES=(decision-center decision-radar nmp decision-guide)
for p in "${PAGES[@]}"; do
  f="$PREMIUM/$p.html"
  [ -f "$f" ] || { log "MISSING=$f"; continue; }
  python3 - "$f" "$TS" <<'PY'
import re,sys
path,ts=sys.argv[1],sys.argv[2]
s=open(path,encoding='utf-8').read()
# remove only the old V5 renderer; keep premium.css for theme base
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/premium\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/premium\.js["\'][^>]*>\s*</script>','',s)
# avoid duplicate V501 renderer/css, then add one fresh cache-busted pair
s=re.sub(r'\s*<link[^>]+href=["\']/_premium/assets/v501-honest\.css\?v=[^"\']+["\'][^>]*>','',s)
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/v501-honest\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
if '</head>' in s:
    s=s.replace('</head>',f'<link rel="stylesheet" href="/_premium/assets/v501-honest.css?v={ts}" /></head>')
if '</body>' in s:
    s=s.replace('</body>',f'<script src="/_premium/assets/v501-honest.js?v={ts}"></script></body>')
open(path,'w',encoding='utf-8').write(s)
PY
  log "PATCHED=$f"
done
chown -R www-data:www-data "$PREMIUM" 2>/dev/null || true
cp -a "$PREMIUM" "$CHECKPOINT/_premium"
ROLLBACK="$REAL_HOME/ndsp_launch_backups/rollback_v5011_$TS.sh"
cat > "$ROLLBACK" <<EOF
#!/usr/bin/env bash
set -euo pipefail
rm -rf "$PREMIUM"
cp -a "$BACKUP/_premium.before_v5011" "$PREMIUM"
chown -R www-data:www-data "$PREMIUM" 2>/dev/null || true
echo ROLLBACK_OK
EOF
chmod +x "$ROLLBACK"
log ""
log "== VERIFY LOCAL =="
for p in "${PAGES[@]}"; do
  f="$PREMIUM/$p.html"
  old_js=$(grep -Ec '/_premium/assets/premium\.js' "$f" || true)
  v501_js=$(grep -Ec '/_premium/assets/v501-honest\.js' "$f" || true)
  v501_css=$(grep -Ec '/_premium/assets/v501-honest\.css' "$f" || true)
  log "$p OLD_PREMIUM_JS=$old_js V501_JS=$v501_js V501_CSS=$v501_css"
done
log ""
log "== PUBLIC CHECK =="
for p in "${PAGES[@]}"; do
  out="/tmp/v5011_check.html"
  code=$(curl -skL -o "$out" -w "%{http_code}" "https://my.ndsp.app/_premium/$p.html?symbol=BTCUSDT&v=$TS" || echo 000)
  size=$(wc -c < "$out" 2>/dev/null || echo 0)
  old_js=$(grep -Ec '/_premium/assets/premium\.js' "$out" || true)
  v501_refs=$(grep -Ec 'v501-honest\.(css|js)' "$out" || true)
  obj=$(grep -c '\[object Object\]' "$out" || true)
  log "$p HTTP=$code SIZE=$size OLD_PREMIUM_JS=$old_js V501_REFS=$v501_refs OBJECT_TEXT=$obj"
done
log "FINAL_STATUS=NDSP_V5011_PREMIUM_SINGLE_RENDERER_FIX_DONE"
log "URL_NMP=https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&v=$TS"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "URL_GUIDE=https://my.ndsp.app/_premium/decision-guide.html?symbol=BTCUSDT&v=$TS"
log "CHECKPOINT=$CHECKPOINT"
log "ROLLBACK=$ROLLBACK"
log "REPORT=$REPORT"
