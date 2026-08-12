import { formatDistanceToNow } from "date-fns"
import { ar } from "date-fns/locale"
import { Clock3 } from "lucide-react"

type FreshnessProps = {
  updatedAt: string
}

export function Freshness({ updatedAt }: FreshnessProps) {
  const date = new Date(updatedAt)

  return (
    <div className="sovereign-freshness">
      <Clock3 size={15} strokeWidth={1.4} />
      <span>
        آخر تحديث{" "}
        {formatDistanceToNow(date, {
          addSuffix: true,
          locale: ar,
        })}
      </span>
    </div>
  )
}
