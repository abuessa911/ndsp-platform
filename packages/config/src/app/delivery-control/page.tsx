export const dynamic = "force-dynamic";
export default function Page() {
  return (
    <section className="min-h-screen bg-[#05070b] text-white">
      <div className="mx-auto max-w-5xl px-5 py-10">
        <div className="rounded-3xl border border-yellow-400/20 bg-black/40 p-6">
          <p className="text-xs uppercase tracking-[0.35em] text-yellow-300">NDSP Admin Console</p>
          <h1 className="mt-3 text-3xl font-semibold capitalize">delivery control</h1>
          <p className="mt-4 text-sm text-slate-300">Decision Active · Execution Sanitized · Route Available</p>
        </div>
        <a href="/operations" className="mt-6 inline-block rounded-2xl border border-white/10 px-5 py-3 text-cyan-100">Back to Operations</a>
      </div>
    </section>
  );
}
