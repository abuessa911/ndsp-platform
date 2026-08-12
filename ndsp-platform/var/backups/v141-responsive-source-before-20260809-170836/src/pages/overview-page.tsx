import { useQuery } from "@tanstack/react-query"

import { Freshness } from "@/components/ndsp/pages/freshness"
import { OverviewChart } from "@/components/ndsp/pages/overview-chart"
import { PageShell } from "@/components/ndsp/pages/page-shell"
import { getPublicOverview } from "@/services/public-api"

export function OverviewPage() {
  const query = useQuery({
    queryKey: ["public", "overview"],
    queryFn: getPublicOverview,
  })

  if (query.isLoading) {
    return <div className="sovereign-page-loading">جارٍ التحميل…</div>
  }

  if (query.isError || !query.data) {
    return (
      <div className="sovereign-page-loading">
        تعذر تحميل النظرة العامة.
      </div>
    )
  }

  const data = query.data

  return (
    <PageShell
      eyebrow="01 / OVERVIEW"
      title="نظرة عامة"
      accent="على القرار."
      description="ملخص عام عالي المستوى يجمع الحالة والحوكمة وحداثة البيانات ضمن Public Projection."
      demo={data.mode === "demo"}
    >
      <div className="sovereign-kpi-grid">
        {data.kpis.map((kpi) => (
          <article className="sovereign-kpi" key={kpi.id}>
            <span>{kpi.label}</span>
            <strong>{kpi.value}</strong>
            <small>{kpi.detail}</small>
          </article>
        ))}
      </div>

      <div className="sovereign-panel sovereign-panel--chart">
        <div className="sovereign-panel__heading">
          <div>
            <span>PUBLIC CONTEXT</span>
            <h2>الحالة العامة</h2>
          </div>

          <Freshness updatedAt={data.updatedAt} />
        </div>

        <OverviewChart points={data.trend} />
      </div>
    </PageShell>
  )
}
