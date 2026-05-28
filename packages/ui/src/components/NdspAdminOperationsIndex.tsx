"use client";

const links = [
  ["/live-alerts-control", "Live Alerts Control", "Send sanitized backend alerts."],
  ["/delivery-control", "Delivery Control", "Test delivery channels."],
  ["/delivery-settings", "Delivery Settings", "Enable or disable delivery channels."],
  ["/alert-rules", "Alert Rules Engine", "Monitor rules, spam guard, and audit logs."],
];

export default function NdspAdminOperationsIndex() {
  return (
    <section className="min-h-screen bg-[#05070b] text-white">
      <div className="mx-auto max-w-7xl px-5 py-10">
        <div className="rounded-3xl border border-yellow-400/20 bg-black/40 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.35em] text-yellow-300">NDSP Admin Console</p>
          <h1 className="mt-3 text-3xl font-semibold md:text-5xl">Operations Control Center</h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300">
            Protected operational navigation. Authorization remains server-side and outputs are sanitized.
          </p>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {links.map(([href, title, desc]) => (
            <a key={href} href={href} className="rounded-3xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur hover:border-yellow-300/40">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Operation</p>
              <h2 className="mt-3 text-xl font-semibold">{title}</h2>
              <p className="mt-3 text-sm leading-7 text-slate-300">{desc}</p>
              <p className="mt-5 text-sm text-yellow-200">{href}</p>
            </a>
          ))}
        </div>

        <div className="mt-6 rounded-3xl border border-emerald-300/20 bg-emerald-950/10 p-5 text-sm text-emerald-100">
          Decision Active · Execution Sanitized · Route Fixed
        </div>
      </div>
    </section>
  );
}
