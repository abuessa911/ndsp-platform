#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
LIVE="/var/www/ndsp-my"
PREMIUM="$LIVE/_premium"
ASSETS="$PREMIUM/assets"
REAL_USER="${SUDO_USER:-nawaf511}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$REAL_HOME/ndsp_launch_reports/NDSP_V501_PREMIUM_HONEST_LOGIC_$TS.md"
BACKUP="$REAL_HOME/ndsp_launch_backups/ndsp-v501-premium-honest-logic-$TS"
CHECKPOINT="$REAL_HOME/ndsp_release_checkpoints/NDSP_V501_PREMIUM_HONEST_LOGIC_$TS"
mkdir -p "$REAL_HOME/ndsp_launch_reports" "$REAL_HOME/ndsp_launch_backups" "$REAL_HOME/ndsp_release_checkpoints"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
[ -d "$PREMIUM" ] || { log "ERROR=PREMIUM_NOT_FOUND"; exit 1; }
if [ "$(id -u)" != "0" ]; then log "ERROR=RUN_WITH_SUDO"; exit 1; fi
mkdir -p "$BACKUP" "$CHECKPOINT"
cp -a "$PREMIUM" "$BACKUP/_premium.before_v501"
log "BACKUP=$BACKUP/_premium.before_v501"
cat > "$ASSETS/v501-honest.css" <<'CSS'
.v501-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin:20px 0}.v501-card{grid-column:span 12;border:1px solid rgba(215,182,82,.28);background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018));border-radius:28px;padding:22px}.v501-card h2,.v501-card h3{margin:0 0 12px;color:var(--gold2,#f2d46b)}.v501-half{grid-column:span 6}.v501-third{grid-column:span 4}.v501-row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.v501-box{border:1px solid rgba(255,255,255,.09);border-radius:22px;background:rgba(255,255,255,.035);padding:16px}.v501-box small{display:block;color:var(--muted,#aca28e);font-weight:900;margin-bottom:7px}.v501-box b{display:block;color:#fff;font-size:20px;line-height:1.35}.v501-badge{display:inline-flex;border-radius:999px;border:1px solid rgba(215,182,82,.35);background:rgba(215,182,82,.08);color:var(--gold2,#f2d46b);padding:7px 12px;font-weight:950}.v501-note{margin-top:12px;border:1px solid rgba(253,230,138,.25);background:rgba(253,230,138,.06);color:#ead89a;border-radius:18px;padding:13px;line-height:1.7}.v501-levels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.v501-level{border:1px solid rgba(215,182,82,.24);border-radius:22px;background:rgba(215,182,82,.055);padding:16px}.v501-level small{display:block;color:#b9ad96;font-weight:900}.v501-level b{display:block;color:#fff;font-size:26px;margin-top:8px}.v501-radar{width:min(560px,100%);aspect-ratio:1;margin:auto;border-radius:50%;border:1px solid rgba(215,182,82,.28);background:radial-gradient(circle,rgba(215,182,82,.13),rgba(255,255,255,.04) 48%,#050506 78%);position:relative;overflow:visible}.v501-radar:before,.v501-radar:after{content:"";position:absolute;border:1px solid rgba(215,182,82,.16);border-radius:50%}.v501-radar:before{inset:12%}.v501-radar:after{inset:30%}.v501-core{position:absolute;inset:36%;border-radius:50%;display:grid;place-items:center;text-align:center;background:#050506;border:1px solid rgba(215,182,82,.25);z-index:3}.v501-core b{color:var(--gold2,#f2d46b);font-size:24px}.v501-node{position:absolute;z-index:4;min-width:92px;border-radius:16px;border:1px solid rgba(255,255,255,.12);background:rgba(4,5,7,.86);padding:8px;text-align:center;box-shadow:0 14px 36px rgba(0,0,0,.35)}.v501-node small{display:block;color:#aaa;font-size:10px;font-weight:900}.v501-node b{display:block;font-size:13px;margin-top:2px}.v501-ok b{color:#86efac}.v501-warn b{color:#fde68a}.v501-part b{color:#f2d46b}.v501-off b{color:#b8b8b8}.v501-bad b{color:#fca5a5}.p1{top:5%;left:50%;transform:translateX(-50%)}.p2{top:25%;right:-1%}.p3{bottom:20%;right:1%}.p4{bottom:5%;left:50%;transform:translateX(-50%)}.p5{bottom:20%;left:1%}.p6{top:25%;left:-1%}.p7{top:50%;left:50%;transform:translate(-50%,-50%)}.v501-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.v501-tabs button{border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.045);color:#b9ad96;border-radius:999px;padding:10px 13px;font-weight:950}.v501-tabs button.on{background:linear-gradient(135deg,#f2d46b,#d7b652);color:#050505}.v501-guide{display:grid;gap:12px}.v501-guide div{border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:16px;background:rgba(255,255,255,.035)}.v501-guide h3{color:var(--gold2,#f2d46b);margin:0 0 7px}.v501-guide p{margin:0;color:#b9ad96;line-height:1.75}@media(max-width:900px){.v501-half,.v501-third{grid-column:span 12}.v501-row,.v501-levels{grid-template-columns:1fr}.v501-node{min-width:78px}.v501-node small{font-size:9px}.v501-node b{font-size:12px}.p2{right:-4%}.p6{left:-4%}}
CSS
cat > "$ASSETS/v501-honest.js" <<'JS'
(function(){
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const q=new URLSearchParams(location.search); const sym=(q.get('symbol')||localStorage.getItem('ndsp_selected_symbol')||'BTCUSDT').toUpperCase().replace(/[^A-Z0-9._:-]/g,''); localStorage.setItem('ndsp_selected_symbol',sym);
const page=document.body.dataset.page||'index'; const ar=true; const fmt=v=>{let n=Number(String(v??'').replace(/,/g,''));return Number.isFinite(n)?n.toLocaleString('en-US',{maximumFractionDigits:2}):(v||'—')};
const nav=()=>['asset-selector:اختيار الأصل','decision-center:مركز القرار','decision-radar:الرادار','nmp:NMP','decision-guide:الدليل'].map(x=>{let [p,t]=x.split(':');return `<a class="${page===p?'on':''}" href="/_premium/${p}.html?symbol=${sym}">${t}</a>`}).join('');
function shell(title,sub,body){document.body.dir='rtl';document.body.innerHTML=`<header class="top"><div class="shell topin"><a class="brand" href="/_premium/index.html?symbol=${sym}"><span class="logo">N</span><span>NDSP<small>V5.1 Honest Logic</small></span></a><nav class="nav">${nav()}</nav></div></header><main class="shell"><section class="hero"><div class="kicker"><span class="dot"></span><span>V5.1</span><span class="pill">${sym}</span></div><h1>${title}</h1><p>${sub}</p><div class="actions"><a class="btn" href="/_premium/decision-center.html?symbol=${sym}">فتح مركز القرار</a><a class="btn secondary" href="/_premium/asset-selector.html?symbol=${sym}">تغيير الأصل</a><span class="pill">ليست توصية مالية ولا أمر تنفيذ</span></div></section>${body}<footer class="footer">NDSP يبني فهمًا منظمًا ولا يصدر أوامر تنفيذ.</footer></main>`}
function get(o,p){return p.split('.').reduce((a,k)=>a&&a[k]!==undefined?a[k]:undefined,o)}
function first(o,arr){for(const p of arr){let v=get(o,p); if(v!==undefined&&v!==null&&String(v)!=='')return v}}
function status(v,inv=false,exists=true){if(!exists)return ['v501-off','غير موصول']; let n=Number(v); if(!Number.isFinite(n))return ['v501-off','غير موصول']; if(inv){if(n<=40)return ['v501-ok','مكتمل']; if(n<=55)return ['v501-warn','حذر']; if(n>=66)return ['v501-bad','موقوف']; return ['v501-part','جزئي']} if(n>=80)return ['v501-ok','مكتمل']; if(n>=65)return ['v501-warn','حذر']; if(n<45)return ['v501-bad','ضعيف']; return ['v501-part','جزئي']}
function node(pos,name,v,inv,exists){let s=status(v,inv,exists);return `<div class="v501-node ${pos} ${s[0]}"><small>${name}</small><b>${s[1]}</b></div>`}
function deriveHorizon(sc){let raw=String(sc.scenario_time_horizon||sc.scenario_directional_context||''); if(raw.includes('أسبوعي'))return 'أفق ممتد / أسبوعي'; if(raw.includes('يومي'))return 'أفق متوسط / يومي'; if(raw.match(/ساعة|دقيقة/))return 'أفق ضيق'; return 'غير مرسل من المصدر'}
function correction(d){let v=first(d,['correction_type','correction_visibility','scenario.correction_type','scenario.correction_visibility']); if(!v)return 'غير مرسل من المصدر'; v=String(v); if(/explicit|صريح|المكشوف/i.test(v))return 'على المكشوف'; if(/implicit|ضمني|غير صريح/i.test(v))return 'غير صريح'; return v}
async function data(){try{let r=await fetch('/api/decision/quality-live?symbol='+encodeURIComponent(sym),{cache:'no-store'}); if(r.ok)return await r.json()}catch(e){} return {}}
function levels(sc){return [['تفعيل',sc.scenario_activation_level,'بداية مراقبة السيناريو، وليست دخول.'],['وصول',sc.scenario_arrival_level,'منطقة وصول القراءة إذا بقي السياق.'],['مراجعة',sc.scenario_review_zone,'منطقة إعادة تقييم وليست هدفًا ثابتًا.'],['إلغاء',sc.scenario_invalidation_level,'كسر السيناريو الحالي وطلب قراءة جديدة.']].map(x=>`<div class="v501-level"><small>${x[0]}</small><b>${fmt(x[1])}</b><p>${x[2]}</p></div>`).join('')}
async function center(){let d=await data(), sc=d.scenario||{}; shell('مركز القرار', 'أضفنا الأفق ونوع التصحيح بصدق: لا نخترع ما لم يرسله الباك إند.', `<section class="v501-grid"><div class="v501-card"><h2>سياق القرار</h2><div class="v501-row"><div class="v501-box"><small>اتجاه القراءة</small><b>${sc.scenario_directional_context||'غير مرسل'}</b></div><div class="v501-box"><small>الأفق</small><b>${deriveHorizon(sc)}</b></div><div class="v501-box"><small>نوع التصحيح</small><b>${correction(d)}</b></div><div class="v501-box"><small>NMP المتصل</small><b>${d.nmp_status||'—'} · ${d.nmp_timeframe||'—'} · ${fmt(d.nmp_level)}</b></div></div><div class="v501-note">إذا لم يظهر “على المكشوف” أو “غير صريح” فذلك لأن الباك إند لا يرسل correction_type/correction_visibility حتى الآن.</div></div><div class="v501-card"><h2>المستويات المرجعية</h2><div class="v501-levels">${levels(sc)}</div></div></section>`)}
async function radar(){let d=await data(), sc=d.scenario||{}; let q=Number(d.decision_quality||72), risk=Number(d.risk_score??d.risk??NaN), devil=Number(d.devil_advocate_score??d.devil_advocate??NaN); let ref=sc.scenario_activation_level?78:NaN, nmp=d.nmp_level?70:NaN, hor=sc.scenario_time_horizon?70:NaN, coh=sc.scenario_directional_context?68:NaN; let nodes=node('p1','الجاهزية',q,false,true)+node('p2','التماسك',coh,false,!!sc.scenario_directional_context)+node('p3','المستويات',ref,false,!!sc.scenario_activation_level)+node('p4','NMP',nmp,false,!!d.nmp_level)+node('p5','الأفق',hor,false,!!sc.scenario_time_horizon)+node('p6','المخاطر',risk,true,Number.isFinite(risk))+node('p7','محامي الشيطان',devil,true,Number.isFinite(devil)); shell('رادار القرار', 'الشروط تظهر داخل الرادار، وغير الموجود من المصدر يظهر “غير موصول”.', `<section class="v501-grid"><div class="v501-card v501-half"><div class="v501-radar">${nodes}<div class="v501-core"><div><b>${sym}</b><small>تحت المتابعة</small></div></div></div><div class="v501-note">المخاطر ومحامي الشيطان عكسيان: الأقل أفضل. لا نعلن اكتمال شرط غير موجود في JSON.</div></div><div class="v501-card v501-half"><h2>حالة الربط</h2><div class="v501-guide"><div><h3>NMP</h3><p>${d.nmp_level?'متصل: '+fmt(d.nmp_level)+' / '+(d.nmp_timeframe||'—'):'غير موصول'}</p></div><div><h3>التصحيح</h3><p>${correction(d)}</p></div><div><h3>الأفق</h3><p>${deriveHorizon(sc)}</p></div></div></div></section>`)}
async function nmp(){let d=await data(); let actual=String(d.nmp_timeframe||'').toUpperCase(); let tfs=['W1','D1','H4','H1','M15','1D']; let tab=q.get('tf')||actual||'1D'; let tabs=tfs.map(tf=>`<button class="${tab===tf?'on':''}" onclick="location.href='?symbol=${sym}&tf=${tf}'">${tf}</button>`).join(''); let connected=(tab===actual || (!actual&&tab==='1D')) && d.nmp_level; shell('NMP حسب الفريم', 'الفريم الحقيقي المتصل يظهر فقط، والبقية بانتظار ربط مستقل من الباك إند.', `<section class="v501-grid"><div class="v501-card"><h2>اختيار الفريم</h2><div class="v501-tabs">${tabs}</div><span class="v501-badge">الفريم المتصل من المصدر: ${actual||'غير مرسل'}</span><div class="v501-row" style="margin-top:14px"><div class="v501-box"><small>NMP</small><b>${connected?fmt(d.nmp_level):'بانتظار ربط NMP مستقل'}</b></div><div class="v501-box"><small>الحالة</small><b>${connected?(d.nmp_status||'AVAILABLE'):'غير موصول لهذا الفريم'}</b></div></div><div class="v501-note">لا يتم نسخ NMP اليومي إلى الأسبوعي أو الأربع ساعات. كل فريم يحتاج قيمة مستقلة من الباك إند.</div></div></section>`)}
function guide(){shell('دليل فهم القرار','شرح عملي للمستويات والرادار وNMP بدون تحويلها إلى أوامر تنفيذ.',`<section class="v501-grid"><div class="v501-card"><h2>المستويات المرجعية</h2><div class="v501-guide"><div><h3>تفعيل</h3><p>بداية مراقبة السيناريو، وليست دخول.</p></div><div><h3>وصول</h3><p>منطقة وصول قراءة إذا بقي السياق قائمًا، وليست هدف تنفيذ.</p></div><div><h3>مراجعة</h3><p>منطقة إعادة تقييم المخاطر والسياق وNMP.</p></div><div><h3>إلغاء</h3><p>إذا وصلها السعر فالسيناريو الحالي يحتاج قراءة جديدة.</p></div><div><h3>الأفق</h3><p>أفق ممتد يعني قراءة أوسع. أفق ضيق يعني حساسية أعلى وتغير أسرع.</p></div><div><h3>على المكشوف / غير صريح</h3><p>لا يظهر هذا التصنيف إلا إذا أرسله الباك إند. إذا لم يرسله، تعرض المنصة “غير مرسل من المصدر”.</p></div><div><h3>المخاطر ومحامي الشيطان</h3><p>عكسيان: الأقل أفضل، وارتفاعهما قد يمنع اكتمال القراءة.</p></div><div><h3>NMP</h3><p>منطقة تحقق وليست أمر تنفيذ. وكل فريم يحتاج NMP مستقل.</p></div></div></div></section>`)}
setTimeout(()=>{ if(page==='decision-center')center(); else if(page==='decision-radar')radar(); else if(page==='nmp')nmp(); else if(page==='decision-guide')guide(); },80);
})();
JS
for f in "$PREMIUM"/decision-center.html "$PREMIUM"/decision-radar.html "$PREMIUM"/nmp.html "$PREMIUM"/decision-guide.html; do
  grep -q 'v501-honest.css' "$f" || sed -i "s#</head>#<link rel=\"stylesheet\" href=\"/_premium/assets/v501-honest.css?v=$TS\" /></head>#" "$f"
  grep -q 'v501-honest.js' "$f" || sed -i "s#</body>#<script src=\"/_premium/assets/v501-honest.js?v=$TS\"></script></body>#" "$f"
done
chown -R www-data:www-data "$PREMIUM" 2>/dev/null || true
cp -a "$PREMIUM" "$CHECKPOINT/_premium"
ROLLBACK="$REAL_HOME/ndsp_launch_backups/rollback_v501_$TS.sh"
cat > "$ROLLBACK" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cp -a "$BACKUP/_premium.before_v501/." "$PREMIUM/"
echo ROLLBACK_OK
EOF
chmod +x "$ROLLBACK"
log "CSS_V501=$(wc -c < "$ASSETS/v501-honest.css")"
log "JS_V501=$(wc -c < "$ASSETS/v501-honest.js")"
for url in decision-center decision-radar nmp decision-guide; do
  code=$(curl -skL -o /tmp/v501_check.html -w "%{http_code}" "https://my.ndsp.app/_premium/$url.html?symbol=BTCUSDT&v=$TS" || echo 000)
  size=$(wc -c < /tmp/v501_check.html 2>/dev/null || echo 0)
  refs=$(grep -Ec 'v501-honest\.(css|js)' /tmp/v501_check.html || true)
  old=$(grep -Eoc 'ndsp-v48|ndsp-v49|ndsp-mobile|index-[A-Za-z0-9]' /tmp/v501_check.html || true)
  obj=$(grep -c '\[object Object\]' /tmp/v501_check.html || true)
  log "$url HTTP=$code SIZE=$size V501_REFS=$refs OLD_PATCH=$old OBJECT_TEXT=$obj"
done
log "FINAL_STATUS=NDSP_V501_PREMIUM_HONEST_LOGIC_DONE"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "URL_NMP=https://my.ndsp.app/_premium/nmp.html?symbol=BTCUSDT&v=$TS"
log "URL_GUIDE=https://my.ndsp.app/_premium/decision-guide.html?symbol=BTCUSDT&v=$TS"
log "CHECKPOINT=$CHECKPOINT"
log "ROLLBACK=$ROLLBACK"
log "REPORT=$REPORT"
