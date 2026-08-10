import {
  ArrowLeft,
  CheckCircle2,
  Clock3,
  Database,
  ShieldCheck,
} from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

const statusItems = [
  {
    label: "الحالة",
    value: "بانتظار Public Projection",
    icon: Database,
  },
  {
    label: "آخر تحديث",
    value: "—",
    icon: Clock3,
  },
  {
    label: "صلاحية البيانات",
    value: "غير متاحة بعد",
    icon: CheckCircle2,
  },
  {
    label: "الحوكمة",
    value: "Governance Protected",
    icon: ShieldCheck,
  },
]

export function CoreHero() {
  return (
    <section className="relative overflow-hidden border-b border-white/10">
      <div
        className="pointer-events-none absolute inset-0 opacity-50"
        style={{
          background:
            "radial-gradient(circle at 75% 15%, rgba(62,153,196,0.12), transparent 30%), radial-gradient(circle at 20% 40%, rgba(185,151,91,0.12), transparent 35%)",
        }}
      />

      <div className="relative mx-auto grid min-h-[720px] max-w-7xl items-center gap-14 px-5 py-20 lg:grid-cols-[1.1fr_0.9fr] lg:px-8">
        <div className="max-w-3xl">
          <Badge
            variant="outline"
            className="mb-6 border-[#B9975B]/30 bg-[#B9975B]/10 px-3 py-1 text-[#D7B873]"
          >
            NDSP · Institutional Decision Intelligence
          </Badge>

          <h1 className="max-w-3xl text-4xl font-semibold leading-[1.25] tracking-tight text-[#F7F3EA] sm:text-5xl lg:text-6xl">
            اتجاه القرار،
            <span className="block text-[#D7B873]">
              بصياغة مؤسسية واضحة.
            </span>
          </h1>

          <p className="mt-7 max-w-2xl text-base leading-8 text-white/55 sm:text-lg">
            منصة دعم قرار مصممة لعرض المخرجات العامة المصرح بها من الحوكمة
            بصورة مختصرة، واضحة، وقابلة للتفسير دون كشف المنطق الداخلي
            أو البنية المحمية.
          </p>

          <div className="mt-9 flex flex-wrap gap-3">
            <Button
              asChild
              className="h-11 bg-[#C5A464] px-6 text-[#111315] hover:bg-[#D2B474]"
            >
              <a href="#current-analysis">
                استعراض التحليل الحالي
                <ArrowLeft className="mr-2 size-4" />
              </a>
            </Button>

            <Button
              asChild
              variant="outline"
              className="h-11 border-white/15 bg-white/[0.03] px-6 text-white/80 hover:bg-white/[0.07] hover:text-white"
            >
              <a href="#methodology">كيف تعمل المنصة؟</a>
            </Button>
          </div>

          <div className="mt-12 flex flex-wrap gap-x-8 gap-y-3 text-xs text-white/40">
            <span>Governance Authorized</span>
            <span>Public Projection Only</span>
            <span>Arabic RTL / English LTR</span>
          </div>
        </div>

        <Card className="border-white/10 bg-[#111417]/85 shadow-2xl shadow-black/20 backdrop-blur">
          <CardHeader className="border-b border-white/10 pb-5">
            <div className="mb-3 flex items-center justify-between gap-4">
              <Badge className="border border-[#B9975B]/25 bg-[#B9975B]/10 text-[#D7B873]">
                CORE
              </Badge>

              <span className="text-xs text-white/30">
                Public Authorized Output
              </span>
            </div>

            <CardTitle className="text-2xl font-medium text-[#F5F2EA]">
              CORE Official Direction
            </CardTitle>

            <p className="mt-2 text-sm leading-6 text-white/45">
              ستظهر هنا النتيجة الرسمية المصرح بها بعد ربط Public API.
            </p>
          </CardHeader>

          <CardContent className="p-0">
            <div className="divide-y divide-white/10">
              {statusItems.map((item) => {
                const Icon = item.icon

                return (
                  <div
                    key={item.label}
                    className="flex items-center justify-between gap-6 px-6 py-5"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex size-9 items-center justify-center rounded-lg border border-[#4E9FC6]/15 bg-[#4E9FC6]/10">
                        <Icon className="size-4 text-[#69B2D4]" />
                      </div>

                      <span className="text-sm text-white/45">
                        {item.label}
                      </span>
                    </div>

                    <span className="text-sm font-medium text-white/80">
                      {item.value}
                    </span>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
