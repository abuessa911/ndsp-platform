import { useQuery } from "@tanstack/react-query"
import {
  Clock3,
  FileCheck2,
  ShieldCheck,
} from "lucide-react"

import { Freshness } from "@/components/ndsp/pages/freshness"
import { PageShell } from "@/components/ndsp/pages/page-shell"
import { getPublicCore } from "@/services/public-api"

export function CorePage() {
  const query = useQuery({
    queryKey: ["public", "core"],
    queryFn: getPublicCore,
  })

  if (query.isLoading) {
    return (
      <div className="sovereign-page-loading">
        جارٍ التحميل…
      </div>
    )
  }

  if (query.isError || !query.data) {
    return (
      <div className="sovereign-page-loading">
        تعذر تحميل CORE.
      </div>
    )
  }

  const data = query.data

  return (
    <PageShell
      eyebrow="02 / CORE"
      title="CORE"
      accent="— الاتجاه الرسمي"
      description="المخرج العام المصرح به للقرار، دون كشف المنطق الداخلي أو العلاقات المحمية."
      demo={data.mode === "demo"}
    >
      <div className="sovereign-core-page-card">
        <div className="sovereign-core-page-card__brand">
          <span dir="ltr">CORE</span>
          <small>PUBLIC AUTHORITY</small>
        </div>

        <div className="sovereign-core-page-card__body">
          <span>الاتجاه</span>
          <h2>{data.direction}</h2>
          <p>{data.summary}</p>

          <Freshness updatedAt={data.updatedAt} />
        </div>
      </div>

      <div className="sovereign-trust-cards">
        <article>
          <ShieldCheck aria-hidden="true" />
          <span>الحوكمة</span>
          <strong>{data.governanceStatus}</strong>
        </article>

        <article>
          <FileCheck2 aria-hidden="true" />
          <span>الأدلة</span>
          <strong>{data.evidenceStatus}</strong>
        </article>

        <article>
          <Clock3 aria-hidden="true" />
          <span>الحداثة</span>
          <strong>{data.freshnessStatus}</strong>
        </article>
      </div>
    </PageShell>
  )
}
