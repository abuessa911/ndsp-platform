import type { ReactNode } from "react"

type PageShellProps = {
  eyebrow: string
  title: string
  accent?: string
  description: string
  children: ReactNode
  demo?: boolean
}

export function PageShell({
  eyebrow,
  title,
  accent,
  description,
  children,
  demo = false,
}: PageShellProps) {
  return (
    <section className="sovereign-page">
      <div className="sovereign-page__glow" />

      <div className="sovereign-page__container">
        <header className="sovereign-page__header">
          <div className="sovereign-eyebrow">
            <span className="sovereign-eyebrow__line" />
            <span>{eyebrow}</span>
          </div>

          <h1>
            {title}
            {accent && <strong> {accent}</strong>}
          </h1>

          <p>{description}</p>

          {demo && (
            <div className="sovereign-demo-notice">
              DEMO UI · بيانات توضيحية للواجهة وليست نتيجة قرار فعلية
            </div>
          )}
        </header>

        {children}
      </div>
    </section>
  )
}
