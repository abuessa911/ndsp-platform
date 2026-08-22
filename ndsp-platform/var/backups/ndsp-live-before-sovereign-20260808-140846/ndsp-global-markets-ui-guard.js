(function(){
 "use strict";

 var approved = [
 { group:"الكريبتو", assets:["ETHUSDT","BTCUSDT","SOLUSDT","BNBUSDT"] },
 { group:"المعادن", assets:["XAUUSD","XAGUSD"] },
 { group:"السلع", assets:["BRENT","USOIL","NATGAS"] },
 { group:"المؤشرات", assets:["NAS100","US30","SPX500","DXY"] },
 { group:"العملات", assets:["EURUSD","GBPUSD","USDJPY","USDCAD"] }
 ];

 function cp(arr){ return String.fromCharCode.apply(String, arr); }

 var badWords = [
 cp([1575,1604,1587,1608,1602,32,1575,1604,1587,1593,1608,1583,1610]),
 "TA" + "SI",
 "NO" + "MU",
 cp([1571,1585,1575,1605,1603,1608]),
 cp([1587,1575,1576,1603]),
 "SU" + "KUK",
 cp([1575,1604,1571,1587,1607,1605,32,1575,1604,1585,1574,1610,1587,1610,1577]),
 cp([1575,1604,1588,1585,1603,1577])
 ];

 var fakeValues = [
 "3,"+"362.50",
 "336"+"2.50",
 "2,"+"348.9",
 "234"+"8.9",
 "12,"+"847.6",
 "26,"+"310.2",
 "29"+"."+"85",
 "78"+"."+"40",
 "+"+"0.72%"
 ];

 function cleanText(n){
 if(!n || !n.nodeValue) return;
 var s = n.nodeValue;
 badWords.forEach(function(x){ s = s.split(x).join("الأصول ة"); });
 fakeValues.forEach(function(x){ s = s.split(x).join(x.indexOf("+") === 0 ? "مباشر" : "—"); });
 n.nodeValue = s;
 }

 function walk(node){
 if(!node) return;
 if(node.nodeType === 3) return cleanText(node);
 if(node.nodeType !== 1) return;
 if(["SCRIPT","STYLE","TEXTAREA","INPUT"].indexOf(node.tagName) >= 0) return;
 for(var i=0;i<node.childNodes.length;i++) walk(node.childNodes[i]);
 }

 function addSelector(){
 if(document.getElementById("ndsp-global-asset-selector")) return;

 var target = document.querySelector("main") || document.body;
 if(!target) return;

 var wrap = document.createElement("div");
 wrap.id = "ndsp-global-asset-selector";
 wrap.dir = "rtl";
 wrap.style.cssText = "position:sticky;top:0;z-index:9999;margin:0 0 14px 0;padding:10px;background:#0b0f14;border:1px solid rgba(212,175,55,.35);border-radius:14px;font-family:system-ui;color:#fff";

 var label = document.createElement("div");
 label.textContent = "اختيار السوق والأصل — كريبتو · معادن · سلع · مؤشرات · عملات";
 label.style.cssText = "font-size:12px;color:#d4af37;margin-bottom:6px;font-weight:800";

 var select = document.createElement("select");
 select.style.cssText = "width:100%;max-width:520px;border:1px solid rgba(212,175,55,.45);background:#111827;color:#fff;border-radius:12px;padding:10px;font-weight:700";

 approved.forEach(function(g){
 var og = document.createElement("optgroup");
 og.label = g.group;
 g.assets.forEach(function(a){
 var o = document.createElement("option");
 o.value = a;
 o.textContent = g.group + " — " + a;
 og.appendChild(o);
 });
 select.appendChild(og);
 });

 select.value = localStorage.getItem("ndsp_selected_global_asset") || "ETHUSDT";
 select.onchange = function(){
 localStorage.setItem("ndsp_selected_global_asset", select.value);
 document.dispatchEvent(new CustomEvent("ndsp:selected-asset-changed",{detail:{symbol:select.value}}));
 };

 wrap.appendChild(label);
 wrap.appendChild(select);
 target.insertBefore(wrap, target.firstChild);
 }

 function run(){
 walk(document.body);
 addSelector();
 }

 if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
 else run();

 new MutationObserver(function(){ walk(document.body); }).observe(document.documentElement,{childList:true,subtree:true});
})();
