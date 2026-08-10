import {
  Building2,
  CheckCircle2,
  FileText,
  Globe2,
  Scale,
  Workflow,
} from "lucide-react"

const evidenceSources = [
  {
    label: "بيانات مؤسسية",
    icon: Building2,
  },
  {
    label: "تقارير وتحليلات",
    icon: FileText,
  },
  {
    label: "سياق تشغيلي",
    icon: Workflow,
  },
  {
    label: "معلومات خارجية",
    icon: Globe2,
  },
  {
    label: "معايير وسياسات",
    icon: Scale,
  },
]

function CoreAuthorityCard() {
  return (
    <article
      className="sovereign-core-authority"
      aria-label="CORE — الاتجاه الرسمي"
    >
      <div className="sovereign-core-authority__title">
        <strong dir="ltr">CORE</strong>
        <span>PUBLIC AUTHORITY</span>
      </div>

      <div className="sovereign-core-authority__rule" />

      <div className="sovereign-core-authority__content">
        <strong>الاتجاه الرسمي</strong>

        <span>
          <CheckCircle2 aria-hidden="true" />
          معتمد حوكميًا
        </span>

        <span>
          <CheckCircle2 aria-hidden="true" />
          أدلة قابلة للتحقق
        </span>
      </div>
    </article>
  )
}

export function EvidenceConvergence() {
  return (
    <div
      className="sovereign-evidence"
      aria-label="تقارب الأدلة نحو CORE"
    >
      <div className="sovereign-evidence-map sovereign-evidence-map--desktop">
        <div
          className="sovereign-evidence-map__grid"
          aria-hidden="true"
        />

        <svg
          className="sovereign-evidence-map__svg"
          viewBox="0 0 760 520"
          preserveAspectRatio="xMidYMid meet"
          aria-hidden="true"
        >
          <g className="sovereign-evidence-lines">
            <path d="M188 78 C310 78 352 105 500 260" />
            <path d="M188 168 C330 168 370 188 500 260" />
            <path d="M188 260 C332 260 390 260 500 260" />
            <path d="M188 352 C330 352 370 332 500 260" />
            <path d="M188 442 C310 442 352 415 500 260" />
          </g>

          <g className="sovereign-evidence-particles">
            <circle cx="276" cy="91" r="3" />
            <circle cx="338" cy="176" r="2.5" />
            <circle cx="375" cy="260" r="3" />
            <circle cx="326" cy="344" r="2.5" />
            <circle cx="285" cy="423" r="3" />
          </g>

          <circle
            className="sovereign-evidence-junction"
            cx="500"
            cy="260"
            r="7"
          />

          <path
            className="sovereign-evidence-final-line"
            d="M507 260 H548"
          />
        </svg>

        <div className="sovereign-evidence-sources">
          {evidenceSources.map(({ label, icon: Icon }) => (
            <article
              className="sovereign-evidence-source"
              key={label}
            >
              <span className="sovereign-evidence-source__icon">
                <Icon aria-hidden="true" />
              </span>

              <strong>{label}</strong>

              <span
                className="sovereign-evidence-source__dot"
                aria-hidden="true"
              />
            </article>
          ))}
        </div>

        <CoreAuthorityCard />
      </div>

      <div className="sovereign-evidence-mobile">
        <div className="sovereign-evidence-mobile__sources">
          {evidenceSources.map(({ label, icon: Icon }) => (
            <article
              className="sovereign-evidence-mobile__source"
              key={label}
            >
              <span>
                <Icon aria-hidden="true" />
              </span>

              <strong>{label}</strong>
            </article>
          ))}
        </div>

        <div
          className="sovereign-evidence-mobile__convergence"
          aria-hidden="true"
        >
          <span />
          <i />
        </div>

        <CoreAuthorityCard />
      </div>
    </div>
  )
}
