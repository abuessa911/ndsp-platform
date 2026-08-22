import {
  BarChart3,
  Database,
  FileCheck2,
  Globe2,
  Settings2,
  ShieldCheck,
} from "lucide-react"

const evidenceSources = [
  {
    label: "بيانات مؤسسية",
    icon: Database,
    top: 54,
  },
  {
    label: "تقارير وتحليلات",
    icon: BarChart3,
    top: 145,
  },
  {
    label: "سياق تشغيلي",
    icon: Settings2,
    top: 236,
  },
  {
    label: "معلومات خارجية",
    icon: Globe2,
    top: 327,
  },
  {
    label: "معايير وسياسات",
    icon: FileCheck2,
    top: 418,
  },
]

export function EvidenceConvergence() {
  return (
    <div
      className="sovereign-evidence-map"
      aria-label="مسار الأدلة وصولاً إلى CORE"
    >
      <div className="sovereign-evidence-map__grid" />

      <svg
        className="sovereign-evidence-map__svg"
        viewBox="0 0 760 510"
        role="img"
        aria-label="تدفق خمسة مصادر أدلة نحو CORE"
      >
        <defs>
          <linearGradient
            id="evidenceLine"
            x1="0"
            y1="0"
            x2="1"
            y2="0"
          >
            <stop offset="0" stopColor="#29B6F6" stopOpacity="0.78" />
            <stop offset="0.58" stopColor="#4989A9" stopOpacity="0.58" />
            <stop offset="1" stopColor="#D4AF37" stopOpacity="0.96" />
          </linearGradient>

          <radialGradient id="convergenceGlow">
            <stop offset="0" stopColor="#F2CE70" stopOpacity="1" />
            <stop offset="0.18" stopColor="#D4AF37" stopOpacity="0.72" />
            <stop offset="0.58" stopColor="#A97D2D" stopOpacity="0.16" />
            <stop offset="1" stopColor="#A97D2D" stopOpacity="0" />
          </radialGradient>

          <filter
            id="goldGlow"
            x="-200%"
            y="-200%"
            width="400%"
            height="400%"
          >
            <feGaussianBlur stdDeviation="8" />
          </filter>
        </defs>

        <g className="sovereign-evidence-lines">
          <path d="M155 54 C310 54 344 78 425 166 C463 207 492 229 526 255" />
          <path d="M155 145 C302 145 346 158 414 205 C462 238 491 246 526 255" />
          <path d="M155 236 C315 236 414 246 526 255" />
          <path d="M155 327 C302 327 346 314 414 286 C462 267 491 262 526 255" />
          <path d="M155 418 C310 418 344 394 425 344 C463 320 492 284 526 255" />
        </g>

        <g
          className="sovereign-evidence-particles"
          aria-hidden="true"
        >
          <circle r="2.1">
            <animateMotion
              dur="4.4s"
              repeatCount="indefinite"
              path="M155 54 C310 54 344 78 425 166 C463 207 492 229 526 255"
            />
          </circle>

          <circle r="2.1">
            <animateMotion
              dur="3.9s"
              begin=".45s"
              repeatCount="indefinite"
              path="M155 145 C302 145 346 158 414 205 C462 238 491 246 526 255"
            />
          </circle>

          <circle r="2.3">
            <animateMotion
              dur="3.4s"
              begin=".8s"
              repeatCount="indefinite"
              path="M155 236 C315 236 414 246 526 255"
            />
          </circle>

          <circle r="2.1">
            <animateMotion
              dur="4.1s"
              begin="1.1s"
              repeatCount="indefinite"
              path="M155 327 C302 327 346 314 414 286 C462 267 491 262 526 255"
            />
          </circle>

          <circle r="2.1">
            <animateMotion
              dur="4.7s"
              begin="1.5s"
              repeatCount="indefinite"
              path="M155 418 C310 418 344 394 425 344 C463 320 492 284 526 255"
            />
          </circle>
        </g>

        <circle
          cx="526"
          cy="255"
          r="72"
          fill="url(#convergenceGlow)"
          filter="url(#goldGlow)"
        />

        <circle
          className="sovereign-evidence-junction"
          cx="526"
          cy="255"
          r="4.5"
        />

        <path
          className="sovereign-evidence-final-line"
          d="M526 255H578"
        />
      </svg>

      <div className="sovereign-evidence-sources">
        {evidenceSources.map(({ label, icon: Icon, top }) => (
          <div
            className="sovereign-evidence-source"
            key={label}
            style={{ top }}
          >
            <span className="sovereign-evidence-source__icon">
              <Icon size={15} strokeWidth={1.5} />
            </span>

            <span>{label}</span>

            <span className="sovereign-evidence-source__dot" />
          </div>
        ))}
      </div>

      <div className="sovereign-core-authority">
        <div className="sovereign-core-authority__title">
          <span>CORE</span>
          <small>PUBLIC AUTHORITY</small>
        </div>

        <div className="sovereign-core-authority__rule" />

        <div className="sovereign-core-authority__content">
          <div>
            <ShieldCheck size={18} strokeWidth={1.5} />
            <span>الاتجاه الرسمي</span>
          </div>

          <div>
            <ShieldCheck size={18} strokeWidth={1.5} />
            <span>معتمد حوكميًا</span>
          </div>

          <div>
            <FileCheck2 size={18} strokeWidth={1.5} />
            <span>أدلة قابلة للتحقق</span>
          </div>
        </div>
      </div>
    </div>
  )
}
