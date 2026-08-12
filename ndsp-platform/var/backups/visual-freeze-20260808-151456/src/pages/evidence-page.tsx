import { useQuery } from "@tanstack/react-query"

import { EvidenceGrid } from "@/components/ndsp/pages/evidence-grid"
import { Freshness } from "@/components/ndsp/pages/freshness"
import { PageShell } from "@/components/ndsp/pages/page-shell"
import { getPublicEvidence } from "@/services/public-api"

export function EvidencePage() {
  const query = useQuery({
    queryKey: ["public", "evidence"],
    queryFn: getPublicEvidence,
  })

  if (query.isLoading) {
    return <div className="sovereign-page-loading">جارٍ التحميل…</div>
  }

  if (query.isError || !query.data) {
    return (
      <div className="sovereign-page-loading">
        تعذر تحميل الأدلة.
      </div>
    )
  }

  const data = query.data

  return (
    <PageShell
      eyebrow="04 / EVIDENCE"
      title="الأدلة"
      accent="القابلة للتحقق."
      description="عرض عام للأدلة المصرح بها فقط، مع الحالة والحداثة دون كشف البيانات الخام أو العلاقات الداخلية."
      demo={data.mode === "demo"}
    >
      <div className="sovereign-panel">
        <div className="sovereign-panel__heading">
          <div>
            <span>AUTHORIZED EVIDENCE</span>
            <h2>سجل الأدلة العامة</h2>
          </div>

          <Freshness updatedAt={data.updatedAt} />
        </div>

        <EvidenceGrid rows={data.rows} />
      </div>
    </PageShell>
  )
}
