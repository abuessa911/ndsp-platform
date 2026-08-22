import React from "react";
import { MagnifyingGlass, Info, Link as LinkIcon } from "@phosphor-icons/react";

export function DocumentationPage() {
  return (
    <div className="documentation-page">
      <div className="container">
        <div className="documentation-layout">
          
          <aside className="docs-sidebar">
            <span className="eyebrow">NDSP DOCUMENTATION</span>
            <h1>مركز التوثيق</h1>
            
            <div className="docs-search">
              <MagnifyingGlass size={18} />
              <input type="text" placeholder="ابحث في التوثيق..." />
            </div>

            <nav>
              <section>
                <h2>الحوكمة</h2>
                <button className="active">نظرة عامة على الحوكمة</button>
                <button>المصطلحات المعتمدة</button>
                <button>معايير الامتثال</button>
              </section>
            </nav>
          </aside>

          <article className="docs-article">
            <div className="docs-breadcrumb">
              <span>سجل القرارات</span>
              <span style={{ margin: "0 4px", color: "var(--text-muted)" }}>/</span>
              <span dir="ltr" style={{ marginTop: "2px" }}>ADR-042</span>
            </div>

            <header>
              <h2>نموذج العقد (Public Payload)</h2>
              <p>
                يتم تقديم البيانات للمستويات العامة عبر هيكل موحد يضمن حماية المنطق التشغيلي الداخلي، مع توفير مؤشرات واضحة وموثوقة لدعم القرار دون كشف المحركات الأساسية.
              </p>
            </header>

            <section>
              <pre dir="ltr" style={{ textAlign: "left" }}><code>{`{
  "system_tier": "PUBLIC",
  "signal_status": "VERIFIED",
  "trend_index": 1,
  "framework_version": "4.3.2",
  "cycle_id": "2026-W32"
}`}</code></pre>
            </section>

            <div className="docs-callout" style={{ marginTop: "32px" }}>
              <Info size={24} weight="duotone" />
              <p>
                <strong>ملاحظة أمنية:</strong> تم تجريد هذا النموذج من المعلمات التشغيلية الخام (مثل مسارات المحرك الداخلي) ليتوافق مع سياسة العرض العام ومنع الهندسة العكسية.
              </p>
            </div>

            <div className="docs-article__links">
              <button><LinkIcon size={16} /> نسخ رابط القسم</button>
            </div>
          </article>

        </div>
      </div>
    </div>
  );
}
export default DocumentationPage;
