import { ClipboardText, ShieldCheck } from "@phosphor-icons/react";

type AuthorityBarProps = {
  compact?: boolean;
};

export function AuthorityBar({ compact = false }: AuthorityBarProps) {
  return (
    <section className={`authority-bar ${compact ? "authority-bar--compact" : ""}`} aria-label="حدود النتيجة الرسمية">
      <strong className="authority-bar__core" dir="ltr">CORE</strong>
      <span className="authority-bar__item">
        <ShieldCheck size={compact ? 20 : 24} weight="regular" aria-hidden="true" />
        <span>الاتجاه الرسمي</span>
      </span>
      <span className="authority-bar__item">
        <ShieldCheck size={compact ? 20 : 24} weight="regular" aria-hidden="true" />
        <span>معتمد حوكميًا</span>
      </span>
      <span className="authority-bar__item">
        <ClipboardText size={compact ? 20 : 24} weight="regular" aria-hidden="true" />
        <span>أدلة قابلة للتحقق</span>
      </span>
    </section>
  );
}
