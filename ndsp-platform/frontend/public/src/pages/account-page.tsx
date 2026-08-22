import {
  LockKeyhole,
  ShieldCheck,
  UserRound,
} from "lucide-react"

import { PageShell } from "@/components/ndsp/pages/page-shell"

export function AccountPage() {
  return (
    <PageShell
      eyebrow="06 / ACCOUNT"
      title="الوصول"
      accent="إلى NDSP."
      description="إدارة الوصول والتجربة العامة للمنصة ضمن حدود الصلاحيات المعتمدة."
    >
      <div className="sovereign-account-grid">
        <article className="sovereign-account-card">
          <UserRound />
          <h2>تسجيل الدخول</h2>
          <p>الدخول للحساب الحالي ومتابعة حالة الاشتراك.</p>
          <a href="/login/">تسجيل الدخول</a>
        </article>

        <article className="sovereign-account-card sovereign-account-card--gold">
          <ShieldCheck />
          <h2>تجربة 16 يومًا</h2>
          <p>ابدأ التجربة العامة ضمن الصلاحيات والحدود المعتمدة.</p>
          <a href="/register/">ابدأ التجربة</a>
        </article>

        <article className="sovereign-account-card">
          <LockKeyhole />
          <h2>وصول محكوم</h2>
          <p>المحتوى المتاح يعتمد على مستوى الوصول والصلاحيات.</p>
        </article>
      </div>
    </PageShell>
  )
}
