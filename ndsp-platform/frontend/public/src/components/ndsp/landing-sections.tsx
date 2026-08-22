import {
  Activity,
  Clock3,
  FileCheck2,
  Layers3,
  LockKeyhole,
  ShieldCheck,
} from "lucide-react"

import sovereignControl from "@/assets/sovereign/sovereign-control.jpg"

const trustItems = [
  {
    label: "موثوق",
    value: "Governance Protected",
    icon: ShieldCheck,
  },
  {
    label: "الأدلة",
    value: "Authorized Evidence",
    icon: FileCheck2,
  },
  {
    label: "حداثة البيانات",
    value: "Freshness Aware",
    icon: Clock3,
  },
]

export function LandingSections() {
  return (
    <>
      <section className="sovereign-section sovereign-context">
        <div className="sovereign-section__inner">
          <div className="sovereign-section-heading">
            <span>01 / MARKET CONTEXT</span>
            <h2>
              السياق قبل القرار.
              <strong> القرار قبل الضوضاء.</strong>
            </h2>

            <p>
              نعرض للمستخدم العام السياق والمخرجات المصرح بها فقط،
              مع إبقاء المنطق الداخلي والعلاقات المحمية خارج الواجهة.
            </p>
          </div>

          <div className="sovereign-context-grid">
            <article className="sovereign-data-card sovereign-data-card--wide">
              <div className="sovereign-card-label">
                <Activity size={16} />
                CURRENT STATE
              </div>

              <h3>سياق السوق</h3>

              <p>
                مساحة هادئة لتقديم الحالة الحالية والمعلومات الضرورية
                لفهم اتجاه CORE دون تحويل الصفحة إلى لوحة تداول.
              </p>

              <div className="sovereign-signal-lines">
                <span />
                <span />
                <span />
                <span />
              </div>
            </article>

            <article className="sovereign-data-card">
              <div className="sovereign-card-label">
                <Layers3 size={16} />
                PUBLIC PROJECTION
              </div>

              <h3>مخرج مصرح به</h3>
              <p>
                ما يصل إلى الواجهة العامة يمر عبر حدود الحوكمة
                المعتمدة.
              </p>
            </article>

            <article className="sovereign-data-card">
              <div className="sovereign-card-label">
                <LockKeyhole size={16} />
                PROTECTED LOGIC
              </div>

              <h3>المنطق يبقى محميًا</h3>
              <p>
                لا تعرض الصفحة الصيغ أو العلاقات أو الطبقات الداخلية
                أو القيم الخام.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section
        id="methodology"
        className="sovereign-section sovereign-methodology"
      >
        <div className="sovereign-section__inner sovereign-methodology__inner">
          <div>
            <div className="sovereign-section-heading">
              <span>02 / METHODOLOGY</span>

              <h2>
                لماذا هذا الاتجاه؟
              </h2>

              <p>
                شرح عام مختصر لمسار القرار: سياق واضح، أدلة مصرح بها،
                ثم نتيجة CORE المعتمدة. التفسير لا يعني كشف المنطق
                الداخلي.
              </p>
            </div>

            <a
              className="sovereign-text-link"
              href="#governance"
            >
              <span>شاهد مسار الحوكمة</span>
              <ArrowGlyph />
            </a>
          </div>

          <div className="sovereign-methodology-diagram">
            <div className="sovereign-methodology-diagram__node">
              <span>01</span>
              <strong>السياق</strong>
            </div>

            <i />

            <div className="sovereign-methodology-diagram__node">
              <span>02</span>
              <strong>الأدلة</strong>
            </div>

            <i />

            <div className="sovereign-methodology-diagram__node sovereign-methodology-diagram__node--core">
              <span>03</span>
              <strong>CORE</strong>
            </div>
          </div>
        </div>
      </section>

      <section
        id="governance"
        className="sovereign-governance"
        style={{
          backgroundImage: `url(${sovereignControl})`,
        }}
      >
        <div className="sovereign-governance__overlay" />

        <div className="sovereign-governance__inner">
          <div className="sovereign-governance__copy">
            <div className="sovereign-eyebrow">
              <span className="sovereign-eyebrow__line" />
              <span>GOVERNANCE · AUTHORITY · TRUST</span>
            </div>

            <h2>
              الثقة تُبنى على
              <strong> الحوكمة والأدلة.</strong>
            </h2>

            <p>
              المظهر السيادي لا يقتصر على اللون؛ بل يعكس حدود السلطة،
              وضوح الحالة، وفصل ما هو عام عمّا يبقى داخليًا.
            </p>
          </div>

          <div className="sovereign-trust-grid">
            {trustItems.map(({ label, value, icon: Icon }) => (
              <article key={label}>
                <Icon size={27} strokeWidth={1.25} />

                <span>{label}</span>
                <strong>{value}</strong>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="trial" className="sovereign-trial">
        <div className="sovereign-trial__glow" />

        <div className="sovereign-trial__inner">
          <span>NDSP · 16-DAY TRIAL</span>

          <h2>
            اختبر تجربة القرار
            <strong> كما صُممت.</strong>
          </h2>

          <p>
            ابدأ بالتجربة العامة للمنصة وانتقل من السياق إلى الأدلة
            ثم إلى CORE ضمن تجربة مؤسسية متكاملة.
          </p>

          <a
            className="sovereign-button sovereign-button--gold sovereign-trial__button"
            href="/register/"
          >
            ابدأ تجربتك لمدة 16 يومًا
          </a>
        </div>
      </section>
    </>
  )
}

function ArrowGlyph() {
  return (
    <span aria-hidden="true">
      ←
    </span>
  )
}
