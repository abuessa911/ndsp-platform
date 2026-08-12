import {
  CircleDot,
  FileSearch2,
  ShieldCheck,
} from "lucide-react"

const items = [
  {
    number: "01",
    title: "السياق",
    description:
      "استيعاب الصورة العامة وتقديم السياق المصرح به بصورة مركزة.",
    icon: CircleDot,
  },
  {
    number: "02",
    title: "الأدلة",
    description:
      "عرض الأدلة العامة المصرح بها ضمن إطار واضح وقابل للتتبع.",
    icon: FileSearch2,
  },
  {
    number: "03",
    title: "الاتجاه الرسمي",
    description:
      "مخرج CORE عام واحد، واضح، معتمد وقابل للتفسير.",
    icon: ShieldCheck,
  },
]

export function DecisionJourney() {
  return (
    <section
      className="sovereign-journey"
      aria-label="رحلة القرار"
    >
      <div className="sovereign-journey__inner">
        {items.map(({ number, title, description, icon: Icon }, index) => (
          <div className="sovereign-journey__step" key={number}>
            <span className="sovereign-journey__number">
              {number}
            </span>

            <span className="sovereign-journey__icon">
              <Icon size={25} strokeWidth={1.25} />
            </span>

            <div>
              <h2>{title}</h2>
              <p>{description}</p>
            </div>

            {index < items.length - 1 && (
              <span
                className="sovereign-journey__connector"
                aria-hidden="true"
              />
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
