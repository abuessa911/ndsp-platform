import { useQuery } from "@tanstack/react-query"

import { Freshness } from "@/components/ndsp/pages/freshness"
import { MarketContextChart } from "@/components/ndsp/pages/market-context-chart"
import { PageShell } from "@/components/ndsp/pages/page-shell"
import { getMarketContext } from "@/services/public-api"

export function MarketContextPage() {
  const query = useQuery({
    queryKey: ["public", "market-context"],
    queryFn: getMarketContext,
  })

  if (query.isLoading) {
    return <div className="sovereign-page-loading">جارٍ التحميل…</div>
  }

  if (query.isError || !query.data) {
    return (
      <div className="sovereign-page-loading">
        تعذر تحميل سياق السوق.
      </div>
    )
  }

  const data = query.data

  return (
    <PageShell
      eyebrow="03 / MARKET CONTEXT"
      title={data.title}
      accent="قبل الاتجاه."
      description={data.summary}
      demo={data.mode === "demo"}
    >
      <div className="sovereign-panel sovereign-panel--chart">
        <div className="sovereign-panel__heading">
          <div>
            <span>CONTEXT VIEW</span>
            <h2>السياق العام</h2>
          </div>

          <Freshness updatedAt={data.updatedAt} />
        </div>

        <MarketContextChart points={data.contextSeries} />
      </div>
    </PageShell>
  )
}
