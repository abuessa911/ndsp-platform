(function(){
  "use strict";

  function el(id){ return document.getElementById(id); }
  function setStatus(t){ var s=el("ndspAdminOpsStatus"); if(s) s.textContent=t; }

  async function api(path, opts){
    var r = await fetch("/_ndsp_admin_api" + path, Object.assign({
      credentials:"same-origin",
      headers:{ "Content-Type":"application/json", "Accept":"application/json" }
    }, opts || {}));
    var data = await r.json().catch(function(){ return {}; });
    if(!r.ok) throw new Error(data.error || data.message || ("HTTP " + r.status));
    return data;
  }

  function safe(v){ return String(v == null ? "" : v).replace(/[<>&]/g, function(c){ return {"<":"&lt;",">":"&gt;","&":"&amp;"}[c]; }); }

  async function loadUsers(){
    setStatus("جاري تحميل المستخدمين من قاعدة البيانات...");
    var data = await api("/users");
    renderUsers(data.rows || []);
    setStatus("تم تحميل المستخدمين: " + ((data.rows || []).length));
  }

  function renderUsers(rows){
    var table = el("ndspAdminOpsTable");
    if(!table) return;

    table.innerHTML =
      "<thead><tr>" +
      "<th>المستخدم</th><th>الحالة</th><th>الدور</th><th>الباقة</th><th>إجراءات</th>" +
      "</tr></thead><tbody>" +
      rows.map(function(u){
        var id = safe(u.id);
        var name = safe(u.full_name || u.name || "");
        var email = safe(u.email || "");
        var status = safe(u.status || "");
        var role = safe(u.role || "");
        var plan = safe(u.plan || u.package || u.subscription_plan || "");
        return "<tr data-id='" + id + "'>" +
          "<td><b>" + (name || email || id) + "</b><br><small>" + email + "</small></td>" +
          "<td>" + status + "</td>" +
          "<td>" + role + "</td>" +
          "<td>" +
            "<select class='ndspPlan'>" +
              ["Free","Pro","Elite","Institutional Suite"].map(function(p){
                return "<option " + (String(plan).toLowerCase()===p.toLowerCase()?"selected":"") + ">" + p + "</option>";
              }).join("") +
            "</select>" +
          "</td>" +
          "<td>" +
            "<button class='ndspActivate'>تفعيل</button> " +
            "<button class='ndspSuspend'>تعليق</button> " +
            "<button class='ndspSavePlan'>حفظ الباقة</button>" +
          "</td>" +
        "</tr>";
      }).join("") +
      "</tbody>";

    Array.prototype.slice.call(table.querySelectorAll(".ndspActivate")).forEach(function(b){
      b.onclick = function(){ changeStatus(b.closest("tr").dataset.id, "ACTIVE"); };
    });
    Array.prototype.slice.call(table.querySelectorAll(".ndspSuspend")).forEach(function(b){
      b.onclick = function(){ changeStatus(b.closest("tr").dataset.id, "SUSPENDED"); };
    });
    Array.prototype.slice.call(table.querySelectorAll(".ndspSavePlan")).forEach(function(b){
      var tr = b.closest("tr");
      b.onclick = function(){ changePlan(tr.dataset.id, tr.querySelector(".ndspPlan").value); };
    });
  }

  async function changeStatus(id,status){
    if(!confirm("تأكيد تغيير حالة المستخدم إلى " + status + "؟")) return;
    setStatus("جاري تحديث الحالة...");
    await api("/users/" + encodeURIComponent(id) + "/status", { method:"POST", body:JSON.stringify({status:status}) });
    await loadUsers();
  }

  async function changePlan(id,plan){
    if(!confirm("تأكيد تغيير الباقة إلى " + plan + "؟")) return;
    setStatus("جاري تحديث الباقة...");
    await api("/subscriptions/" + encodeURIComponent(id) + "/plan", { method:"POST", body:JSON.stringify({plan:plan}) });
    await loadUsers();
  }

  function build(){
    if(document.getElementById("ndspAdminOpsPanel")) return;

    var panel = document.createElement("section");
    panel.id = "ndspAdminOpsPanel";
    panel.innerHTML =
      "<h2>مركز عمليات المستخدمين والاشتراكات</h2>" +
      "<div class='ndsp-admin-actions'>" +
        "<button id='ndspLoadUsers'>إدارة المستخدمين</button>" +
        "<button id='ndspLoadSubs'>الاشتراكات والباقات</button>" +
        "<button id='ndspRefreshOps'>تحديث</button>" +
      "</div>" +
      "<div id='ndspAdminOpsStatus'>جاهز. اختر إدارة المستخدمين أو الاشتراكات.</div>" +
      "<div style='overflow:auto'><table id='ndspAdminOpsTable'></table></div>";

    document.body.prepend(panel);

    document.getElementById("ndspLoadUsers").onclick = loadUsers;
    document.getElementById("ndspLoadSubs").onclick = loadUsers;
    document.getElementById("ndspRefreshOps").onclick = loadUsers;

    window.NDSP_ADMIN_CONTROLS = { ok:true, bound:true };
  }

  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
