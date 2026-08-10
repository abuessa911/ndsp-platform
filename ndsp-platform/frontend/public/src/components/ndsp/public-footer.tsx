import { NdspLogo } from "@/components/ndsp/ndsp-logo"

export function PublicFooter() {
  return (
    <footer className="sovereign-footer">
      <div className="sovereign-footer__inner">
        <NdspLogo />

        <div className="sovereign-footer__meta">
          <span>Governed Decision Intelligence Platform</span>
          <span>© 2026 NDSP</span>
          <span>
            تنبيه: NDSP منصة دعم قرار وتحليل سياقي. لا تقدم توصيات مالية، ولا تنفذ أوامر، ولا تدير رأس مال المستخدم.
          </span>
        </div>
      </div>
    </footer>
  )
}
