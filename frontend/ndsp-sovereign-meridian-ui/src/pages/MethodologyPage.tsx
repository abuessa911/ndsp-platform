import {
  ArrowLeft,
  CheckCircle,
  Clock,
  Database,
  FileMagnifyingGlass,
  GitBranch,
  ShieldCheck,
  Target,
} from "@phosphor-icons/react";
import { Link } from "react-router-dom";

const stages = [
  { icon: Database, title: "الاستيعاب", text: "جمع تقارير COT وTFF والبيانات المساندة من مزودين موثّقين." },
  { icon: FileMagnifyingGlass, title: "التطبيع", text: "توحيد البنية الزمنية والأدوات والفئات مع توثيق جودة كل حقل." },
  { icon: GitBranch, title: "تركيب الأدلة", text: "ربط المنظور المؤسسي والسياق الكلي وحالة السوق ضمن الأسبوع نفسه." },
  { icon: ShieldCheck, title: "بوابة الحوكمة", text: "التحقق من الاكتمال والحداثة والصلاحية قبل السماح بإصدار نتيجة." },
  { icon: Target, title: "اتجاه CORE", text: "نشر الاتجاه الرسمي الوحيد مع أسبابه وإصداره ووقت اعتماده." },
];

export function MethodologyPage() {
  return (
    <div className="page-surface">
      <section className="page-hero">
        <div className="container page-hero__grid">
          <div>
            <span className="eyebrow">METHODOLOGY</span>
            <h1>منهجية تحوّل الأدلة إلى اتجاه يمكن تفسيره</h1>
            <p>مسار مؤسسي ثابت يربط المصدر بالنتيجة، ويمنع أي قفزة غير معتمدة إلى الواجهة العامة.</p>
          </div>
          <div className="page-hero__seal">
            <ShieldCheck size={38} />
            <strong>CORE</strong>
            <span>Official Direction Contract</span>
          </div>
        </div>
      </section>

      <section className="container methodology-flow" aria-label="مراحل المنهجية">
        {stages.map((stage, index) => {
          const Icon = stage.icon;
          return (
            <article key={stage.title} className="methodology-stage">
              <span className="methodology-stage__index">{String(index + 1).padStart(2, "0")}</span>
              <div className="methodology-stage__icon"><Icon size={24} /></div>
              <div><h2>{stage.title}</h2><p>{stage.text}</p></div>
              {index < stages.length - 1 && <ArrowLeft className="methodology-stage__arrow" size={18} />}
            </article>
          );
        })}
      </section>

      <section className="container methodology-details">
        <article className="detail-panel">
          <span className="eyebrow">QUALITY GATES</span>
          <h2>أربع بوابات قبل النشر</h2>
          <ul className="check-list">
            <li><CheckCircle size={19} weight="fill" /> اكتمال جميع المدخلات الإلزامية</li>
            <li><CheckCircle size={19} weight="fill" /> اتساق الأسبوع الفعّال عبر المصادر</li>
            <li><CheckCircle size={19} weight="fill" /> سلامة عقود البيانات والإصدار</li>
            <li><CheckCircle size={19} weight="fill" /> اعتماد القرار ضمن سجل الحوكمة</li>
          </ul>
        </article>
        <article className="detail-panel">
          <span className="eyebrow">TIME POLICY</span>
          <h2>توقيت واحد غير ملتبس</h2>
          <p>تُحفظ جميع أوقات التشغيل والتفعيل والاعتماد بصيغة التوقيت العالمي، بينما تُعرض للمستخدم مع مرجع زمني واضح.</p>
          <div className="code-sample" dir="ltr">
            <Clock size={18} />
            <code>2026-08-07T20:30:00Z</code>
          </div>
        </article>
      </section>

      <section className="container boundary-banner">
        <div><span className="eyebrow">PUBLIC BOUNDARY</span><h2>ما يظهر للعامة هو النتيجة المعتمدة فقط</h2></div>
        <Link className="button button--primary" to="/analysis">عرض التحليل الحالي <ArrowLeft size={17} /></Link>
      </section>
    </div>
  );
}
