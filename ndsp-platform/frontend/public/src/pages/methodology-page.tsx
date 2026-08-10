import { PageShell } from "@/components/ndsp/pages/page-shell"
import { MethodologyFlow } from "@/components/ndsp/pages/methodology-flow"

export function MethodologyPage() {
  return (
    <PageShell
      eyebrow="05 / METHODOLOGY"
      title="من السياق"
      accent="إلى اتجاه رسمي."
      description="تصور عام لمسار المعلومة داخل الواجهة العامة. المخطط يشرح المراحل المفاهيمية فقط ولا يكشف الطبقات أو الصيغ أو المنطق المحمي."
    >
      <div className="sovereign-panel">
        <div className="sovereign-panel__heading">
          <div>
            <span>PUBLIC METHODOLOGY</span>
            <h2>المسار المفاهيمي</h2>
          </div>
        </div>

        <MethodologyFlow />
      </div>
    </PageShell>
  )
}
