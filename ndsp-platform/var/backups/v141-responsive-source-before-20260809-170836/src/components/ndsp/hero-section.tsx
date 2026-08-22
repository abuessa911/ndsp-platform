import {
  ArrowLeft,
  ArrowUpLeft,
} from "lucide-react"

import { DecisionJourney } from "@/components/ndsp/decision-journey"
import { EvidenceConvergence } from "@/components/ndsp/evidence-convergence"

export function HeroSection() {
  return (
    <>
      <section id="home" className="sovereign-hero">
        <div className="sovereign-hero__ambient sovereign-hero__ambient--gold" />
        <div className="sovereign-hero__ambient sovereign-hero__ambient--blue" />

        <div className="sovereign-hero__inner">
          <div className="sovereign-hero__copy">
            <div className="sovereign-eyebrow">
              <span className="sovereign-eyebrow__line" />
              <span>NDSP · DECISION INTELLIGENCE</span>
            </div>

            <h1>
              منصة نواف
              <br />
              لدعم القرار
              <span>
                كل الأدلة.
                <strong> اتجاه رسمي واحد.</strong>
              </span>
            </h1>

            <p className="sovereign-hero__lead">
              تجربة مؤسسية للقرار تجمع السياق والأدلة العامة المصرح
              بها في مخرج CORE واضح، قابل للتفسير ومحكوم.
            </p>

            <div className="sovereign-hero__actions">
              <a
                className="sovereign-button sovereign-button--gold"
                href="#trial"
              >
                <span>ابدأ تجربتك لمدة 16 يومًا</span>
                <ArrowLeft size={17} />
              </a>

              <a
                className="sovereign-button sovereign-button--outline"
                href="#methodology"
              >
                <span>اعرف لماذا</span>
                <ArrowUpLeft size={16} />
              </a>
            </div>

            <div className="sovereign-hero__microcopy">
              <span>GOVERNANCE AUTHORIZED</span>
              <i />
              <span>PUBLIC PROJECTION</span>
              <i />
              <span>AR / EN</span>
            </div>
          </div>

          <div className="sovereign-hero__visual">
            <EvidenceConvergence />
          </div>
        </div>
      </section>

      <DecisionJourney />
    </>
  )
}
