(function(){
 function findTextNodeElement(needles){
 var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
 var node;
 while((node = walker.nextNode())){
 var txt = (node.nodeValue || "").trim();
 if(!txt) continue;
 for(var i=0; i<needles.length; i++){
 if(txt.indexOf(needles[i]) !== -1) return node.parentElement;
 }
 }
 return null;
 }

 function nearestCard(el){
 var cur = el;
 for(var i=0; i<12 && cur; i++){
 var cls = String(cur.className || "");
 var txt = (cur.innerText || cur.textContent || "");
 if(cur.tagName === "SECTION" || (cls.indexOf("rounded") !== -1 && cls.indexOf("border") !== -1) || (txt.length > 40 && cls.indexOf("card") !== -1)){
 return cur;
 }
 cur = cur.parentElement;
 }
 return el;
 }

 function makeCard(){
 var card = document.createElement("section");
 card.id = "ndsp-devil-advocate-integrated-card";
 card.dir = "rtl";
 card.innerHTML =
 '<div class="ndsp-devil-inner">' +
 '<div class="ndsp-devil-head">' +
 '<div class="ndsp-devil-title-wrap">' +
 '<span class="ndsp-devil-icon">⚖</span>' +
 '<div>' +
 '<h2>محامي الشيطان</h2>' +
 '<p class="ndsp-devil-sub">اختبار الاعتراض المعاكس داخل مسار القرار</p>' +
 '</div>' +
 '</div>' +
 '<span class="ndsp-devil-badge">مخرجات مدمجة</span>' +
 '</div>' +
 '<div class="ndsp-devil-grid">' +
 '<div class="ndsp-devil-box"><div class="ndsp-devil-label">حالة الاعتراض</div><div class="ndsp-devil-value">متوسط</div><p class="ndsp-devil-text">توجد عوامل عكسية كافية لمنع رفع الثقة النهائية بدون تأكيد إضافي.</p></div>' +
 '<div class="ndsp-devil-box"><div class="ndsp-devil-label">سبب الحذر</div><p class="ndsp-devil-text">ضغط الدولار والتذبذب الحالي قد يضعفان جودة القراءة رغم بقاء البيئة داعمة.</p></div>' +
 '<div class="ndsp-devil-box"><div class="ndsp-devil-label">نقطة الإبطال</div><p class="ndsp-devil-text">كسر المستوى المحوري مع ارتفاع التذبذب يقلل صلاحية السيناريو الحاكم.</p></div>' +
 '</div>' +
 '<div class="ndsp-devil-summary"><strong>الخلاصة العكسية</strong><span>القرار قابل للمتابعة، لكن الاعتراض المعاكس يمنع تحويله إلى ثقة نهائية غير مشروطة قبل تحسن شروط التأكيد.</span></div>' +
 '</div>';
 return card;
 }

 function mount(){
 if(!/^\/(?:index\.html)?$/.test(window.location.pathname || "/")) return;
 if(document.getElementById("ndsp-devil-advocate-integrated-card")) return;

 var goldenEl = findTextNodeElement(["إشارة التوافق الذهبية", "إشارة نواف الذهبية"]);
 var summaryEl = findTextNodeElement(["الملخص الاتخاذ إجراءي"]);
 var decisionEl = findTextNodeElement(["القرار الحاكم"]);

 var target = goldenEl ? nearestCard(goldenEl) : null;
 var before = summaryEl ? nearestCard(summaryEl) : null;
 var card = makeCard();

 if(target && target.parentElement){ target.insertAdjacentElement("afterend", card); return; }
 if(before && before.parentElement){ before.parentElement.insertBefore(card, before); return; }

 if(decisionEl){
 var d = nearestCard(decisionEl);
 if(d && d.parentElement){ d.insertAdjacentElement("afterend", card); return; }
 }

 (document.querySelector("main") || document.body).appendChild(card);
 }

 if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
 else mount();

 setTimeout(mount, 800);
 setTimeout(mount, 1800);
})();
