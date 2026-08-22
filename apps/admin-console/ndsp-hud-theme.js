(function(){if(window.__NDSP_HUD__)return;window.__NDSP_HUD__=1;
function ready(f){document.readyState!=="loading"?f():document.addEventListener("DOMContentLoaded",f)}
ready(function(){
var isAR=(document.documentElement.lang||"").indexOf("ar")===0||document.body.dir==="rtl"||document.documentElement.dir==="rtl";
var nav=document.querySelector("nav");
if(nav&&!document.querySelector(".ndsp-hud-strip")){
var s=document.createElement("div");s.className="ndsp-hud-strip";s.setAttribute("aria-hidden","true");
s.innerHTML='<div class="in"><span class="it"><span class="dot"></span>'+(isAR?"الشبكة متصلة":"GRID ONLINE")+'</span><span class="sep">/</span><span class="it">'+(isAR?"الطبقات 16/16":"LAYERS 16/16")+'</span><span class="sep hide-m">/</span><span class="it hide-m">'+(isAR?"مخرجات محكومة":"GOVERNED OUTPUT")+'</span><span class="it clock" id="ndspHudClock"></span></div>';
nav.insertAdjacentElement("afterend",s);
var c=document.getElementById("ndspHudClock");
function tick(){var d=new Date();function p(n){return(n<10?"0":"")+n}
c.textContent=p(d.getUTCHours())+":"+p(d.getUTCMinutes())+":"+p(d.getUTCSeconds())+" UTC"}
tick();setInterval(tick,1000)}
var ns=document.querySelectorAll(".pkg,.seat-card,.prop,.card,.panel,.layer,.step,.opt,[data-hud]");
for(var i=0;i<ns.length;i++){var el=ns[i];
if(el.classList.contains("ndsp-hud-frame"))continue;
if(getComputedStyle(el).position==="static")el.style.position="relative";
el.classList.add("ndsp-hud-frame");
["tl","tr","bl","br"].forEach(function(k){var sp=document.createElement("span");
sp.className="ndsp-c "+k;sp.setAttribute("aria-hidden","true");el.appendChild(sp)})}
if("IntersectionObserver" in window){
var io=new IntersectionObserver(function(es){es.forEach(function(e){
if(e.isIntersecting){e.target.classList.add("ndsp-in");io.unobserve(e.target)}})},{threshold:.25});
document.querySelectorAll(".ndsp-hud-frame").forEach(function(el){io.observe(el)})
}else{document.querySelectorAll(".ndsp-hud-frame").forEach(function(el){el.classList.add("ndsp-in")})}
var h=document.querySelector("header.hero,.hero,[data-hud-scan]");
if(h&&!h.querySelector(".ndsp-hud-scan")){
if(getComputedStyle(h).position==="static")h.style.position="relative";
var sc=document.createElement("div");sc.className="ndsp-hud-scan";sc.setAttribute("aria-hidden","true");h.appendChild(sc)}
if(!document.querySelector(".ndsp-hud-ruler")){["l","r"].forEach(function(side){
var r=document.createElement("div");r.className="ndsp-hud-ruler "+side;
r.setAttribute("aria-hidden","true");document.body.appendChild(r)})}
})})();
