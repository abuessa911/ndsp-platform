(function(){
  "use strict";

  function text(v){ return String(v == null ? "" : v); }

  function pickArray(data){
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.users)) return data.users;
    if (data && Array.isArray(data.data)) return data.data;
    if (data && data.body && Array.isArray(data.body.users)) return data.body.users;
    return [];
  }

  function normalizeUser(u){
    return {
      id: text(u.id || u.user_id || u.uuid),
      name: text(u.name || u.full_name || u.fullName || u.n || "NDSP User"),
      email: text(u.email || u.e),
      phone: text(u.phone || u.mobile || ""),
      status: text(u.status || "UNKNOWN"),
      role: text(u.role || "user"),
      plan: text(u.plan || u.package || "Elite"),
      created_at: text(u.created_at || u.createdAt || ""),
      kind: /pending|review|verification/i.test(text(u.status)) ? "trial" : "active"
    };
  }

  async function api(path){
    var r = await fetch("/_ndsp_admin_api" + path, {
      cache: "no-store",
      credentials: "include",
      headers: { "Accept": "application/json" }
    });
    if (!r.ok) throw new Error("ADMIN_API_" + r.status);
    return await r.json();
  }

  function renderUsers(users){
    var body = document.querySelector("#usersBody");
    if (!body) return;

    body.innerHTML = users.map(function(u){
      return '<tr>'
        + '<td>' + text(u.name) + '</td>'
        + '<td>' + text(u.email) + '</td>'
        + '<td>' + text(u.phone) + '</td>'
        + '<td>' + text(u.plan) + '</td>'
        + '<td>' + text(u.status) + '</td>'
        + '<td>' + text(u.role) + '</td>'
        + '</tr>';
    }).join("");

    if (!users.length) {
      body.innerHTML = '<tr><td colspan="6">لا توجد بيانات مستخدمين من API الرسمي.</td></tr>';
    }
  }

  function renderTrials(users){
    var body = document.querySelector("#trialsBody");
    if (!body) return;

    var trials = users.filter(function(u){
      return /pending|trial|verification|review/i.test(text(u.status + " " + u.kind));
    });

    body.innerHTML = trials.map(function(u){
      return '<tr>'
        + '<td>' + text(u.name) + '</td>'
        + '<td>' + text(u.email) + '</td>'
        + '<td>16</td>'
        + '<td>' + text(u.status) + '</td>'
        + '<td>' + text(u.created_at) + '</td>'
        + '</tr>';
    }).join("");

    if (!trials.length) {
      body.innerHTML = '<tr><td colspan="5">لا توجد تجارب نشطة أو معلقة من API الرسمي.</td></tr>';
    }
  }

  async function boot(){
    try {
      var data = await api("/users");
      var users = pickArray(data).map(normalizeUser);
      window.NDSP_ADMIN_LIVE_USERS = users;
      renderUsers(users);
      renderTrials(users);
      document.documentElement.setAttribute("data-ndsp-admin-live", "true");
      console.log("NDSP_ADMIN_LIVE_DATA_BOUND", users.length);
    } catch(e) {
      console.warn("NDSP_ADMIN_LIVE_DATA_FAILED", e && e.message || e);
      document.documentElement.setAttribute("data-ndsp-admin-live", "failed");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
