import {
  ArrowLeft,
  ChartLineUp,
  CheckCircle,
  CirclesThreePlus,
  Database,
  FileText,
  GitBranch,
  GlobeHemisphereWest,
  Scales,
  ShieldCheck,
  Target,
} from "@phosphor-icons/react";
import type { CSSProperties } from "react";
import { Link } from "react-router-dom";
import { AuthorityBar } from "../components/AuthorityBar";

const inputs = [
  { label: "بيانات مؤسسية", icon: Database },
  { label: "تقارير وتحليلات", icon: ChartLineUp },
  { label: "سياق تشغيلي", icon: GitBranch },
  { label: "معلومات خارجية", icon: GlobeHemisphereWest },
  { label: "معايير وسياسات", icon: Scales },
];

const benefits = [
  ["اتجاه رسمي واضح", "نتيجة واحدة منظمة بدل مجموعة إشارات متعارضة."],
  ["أدلة قابلة للتتبع", "ربط النتيجة بمصادرها وحالتها ووقت تحديثها."],
  ["تفسير منظم للنتيجة", "سياق واضح يساعد على فهم سبب الاتجاه وحدوده."],
  ["إدارة السيناريوهات والمخاطر", "عرض الاحتمالات والمخاطر ضمن إطار قراءة موحد."],
  ["فصل رسمي عن التجارب", "النتيجة العامة تبقى منفصلة عن الاختبارات الداخلية."],
];

export function HomePage() {
  return (
    <>
      <section className="hero-section">
        <div className="hero-section__grid" aria-hidden="true" />
        <div className="hero-section__halo hero-section__halo--gold" aria-hidden="true" />
        <div className="hero-section__halo hero-section__halo--blue" aria-hidden="true" />

        <div className="container hero-grid">
          <div className="hero-copy">
            <span className="eyebrow">SOVEREIGN MERIDIAN · NDSP</span>
            <h1>
              الأدلة تتقاطع.
              <br />
              <span>القرار يتجه.</span>
            </h1>
            <p className="hero-lead">
              تجمع NDSP البيانات المؤسسية والتقارير والسياق التشغيلي والمعلومات الخارجية والمعايير
              داخل إطار محكوم، لتقديم اتجاه رسمي واضح وقابل للتفسير والتحقق.
            </p>

            <div className="hero-actions">
              <Link className="button button--primary" to="/register">
                ابدأ تجربة Elite لمدة 16 يومًا
                <ArrowLeft size={18} />
              </Link>
              <Link className="button button--outline" to="/methodology">
                استكشف المنهجية
              </Link>
            </div>

            <p className="hero-trial-note">
              <CheckCircle size={17} />
              تجربة كاملة لمدة 16 يومًا — دون بطاقة دفع — ودون خصم تلقائي.
            </p>
          </div>

          <div className="evidence-convergence" aria-label="تتقاطع خمسة مصادر أدلة في CORE">
            <div className="evidence-convergence__flow" dir="ltr">
              <img
                src="/assets/decision-convergence.png"
                alt="خمسة مسارات أدلة تتقاطع تدريجيًا في نقطة قرار ذهبية"
              />
              <div className="evidence-convergence__labels" dir="rtl">
                {inputs.map(({ label, icon: Icon }) => (
                  <span key={label}>
                    <Icon size={17} aria-hidden="true" />
                    {label}
                  </span>
                ))}
              </div>
              <span className="evidence-convergence__junction" aria-hidden="true" />
              <i className="evidence-convergence__data-dot evidence-convergence__data-dot--one" aria-hidden="true" />
              <i className="evidence-convergence__data-dot evidence-convergence__data-dot--two" aria-hidden="true" />
              <i className="evidence-convergence__data-dot evidence-convergence__data-dot--three" aria-hidden="true" />
            </div>

            <article className="core-card">
              <span className="core-card__kicker">PUBLIC AUTHORITY</span>
              <strong dir="ltr">CORE</strong>
              <div className="core-card__rule" />
              <span><ShieldCheck size={20} /> الاتجاه الرسمي</span>
              <span><ShieldCheck size={20} /> محكوم حوكميًا</span>
              <span><FileText size={20} /> أدلة قابلة للتحقق</span>
              <footer>
                <b>اتجاه رسمي واحد</b>
                <small>واضح وقابل للتفسير.</small>
              </footer>
            </article>
          </div>
        </div>
      </section>

      <section className="authority-strip" aria-label="حدود سلطة CORE">
        <div className="container">
          <AuthorityBar />
        </div>
      </section>

      <section className="process-section" aria-labelledby="process-title">
        <div className="container">
          <div className="section-heading section-heading--center">
            <span className="eyebrow">ALIGN · RESOLVE · SINGLE PULSE</span>
            <h2 id="process-title">من السياق إلى اتجاه رسمي</h2>
            <p>تجمع المنصة مصادر متعددة، وتربطها ضمن إطار محكوم، ثم تقدم نتيجة رسمية واضحة يمكن تفسيرها وتتبع أدلتها.</p>
          </div>

          <div className="meridian-process">
            <article>
              <span className="meridian-process__number">01</span>
              <div className="meridian-process__icon"><Target size={25} /></div>
              <h3>السياق</h3>
              <p>استيعاب الصورة الكاملة من داخل المؤسسة وخارجها.</p>
            </article>
            <span className="meridian-process__connector" aria-hidden="true" />
            <article>
              <span className="meridian-process__number">02</span>
              <div className="meridian-process__icon"><CirclesThreePlus size={25} /></div>
              <h3>الأدلة</h3>
              <p>جمع الأدلة الموثوقة وتحليلها ضمن إطار واضح وقابل للمراجعة.</p>
            </article>
            <span className="meridian-process__connector" aria-hidden="true" />
            <article className="meridian-process__official">
              <span className="meridian-process__number">03</span>
              <div className="meridian-process__icon"><ShieldCheck size={25} /></div>
              <h3>الاتجاه الرسمي</h3>
              <p>تقديم نتيجة رسمية واحدة، واضحة، قابلة للتفسير والتحقق.</p>
            </article>
          </div>
        </div>
      </section>

      <section className="method-orbit-section">
        <div className="container method-orbit-grid">
          <div className="method-orbit-copy section-heading">
            <span className="eyebrow">HOW NDSP WORKS</span>
            <h2>من مصادر متعددة إلى نتيجة واحدة</h2>
            <p>تبقى الأدلة في مساراتها المعلومة، ثم تتقاطع داخل CORE بدل أن تتحول الواجهة إلى ضوضاء من المؤشرات.</p>
            <Link className="text-link" to="/methodology">
              استكشف المنهجية <ArrowLeft size={16} />
            </Link>
          </div>

          <div className="method-orbit" aria-label="خمسة مصادر عامة تحيط بـ CORE">
            <div className="method-orbit__ring method-orbit__ring--outer" aria-hidden="true" />
            <div className="method-orbit__ring method-orbit__ring--inner" aria-hidden="true" />
            <div className="method-orbit__core">
              <strong dir="ltr">CORE</strong>
              <span><ShieldCheck size={17} /> الاتجاه الرسمي</span>
              <span><ShieldCheck size={17} /> محكوم حوكميًا</span>
              <span><FileText size={17} /> أدلة قابلة للتحقق</span>
            </div>
            {inputs.map(({ label, icon: Icon }, index) => (
              <div className={`method-orbit__node method-orbit__node--${index + 1}`} key={label}>
                <span><Icon size={21} /></span>
                <b>{label}</b>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="evidence-layers-section">
        <div className="container evidence-layers-grid">
          <div className="evidence-staircase" aria-label="طبقات الأدلة العامة التي تصعد نحو CORE">
            <div className="evidence-staircase__core">
              <strong dir="ltr">CORE</strong>
              <span>اتجاه رسمي · محكوم حوكميًا</span>
            </div>
            {inputs.map(({ label, icon: Icon }, index) => (
              <article key={label} style={{ "--step": index } as CSSProperties}>
                <Icon size={19} />
                <span>{label}</span>
                <i aria-hidden="true" />
              </article>
            ))}
          </div>

          <div className="section-heading evidence-layers-copy">
            <span className="eyebrow">EVIDENCE LAYERS</span>
            <h2>القرار لا يبدأ من مؤشر واحد.</h2>
            <p>بل من أدلة تتراكم ضمن سياق واضح حتى تصبح اتجاهًا رسميًا يمكن تفسيره ومراجعته.</p>
            <Link className="button button--outline" to="/analysis">
              شاهد التحليل الحالي <ArrowLeft size={17} />
            </Link>
          </div>
        </div>
      </section>

      <section className="benefits-section">
        <div className="container">
          <div className="section-heading">
            <span className="eyebrow">INSTITUTIONAL CLARITY</span>
            <h2>ما الذي تقدمه المنصة؟</h2>
          </div>
          <div className="benefits-grid">
            {benefits.map(([title, description], index) => (
              <article key={title}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="trial-section">
        <div className="container trial-panel">
          <div>
            <span className="eyebrow">16-DAY ELITE EXPERIENCE</span>
            <h2>جرّب تجربة Elite الكاملة لمدة 16 يومًا.</h2>
            <p>استكشف غرفة القرار والطبقات العامة والتقارير والمقارنات قبل اختيار الباقة المناسبة لك.</p>
          </div>
          <div className="trial-panel__actions">
            <ul>
              <li><CheckCircle size={17} /> دون بطاقة دفع</li>
              <li><CheckCircle size={17} /> دون خصم تلقائي</li>
              <li><CheckCircle size={17} /> تجربة واحدة لكل حساب موثق</li>
            </ul>
            <Link className="button button--primary" to="/register">
              ابدأ تجربتك الآن <ArrowLeft size={18} />
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
