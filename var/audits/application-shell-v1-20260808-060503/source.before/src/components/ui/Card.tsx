import type { PropsWithChildren } from "react";

type Props = PropsWithChildren<{
  title?: string;
  subtitle?: string;
}>;

export function Card({
  title,
  subtitle,
  children
}: Props) {
  return (
    <section className="ndsp-card ndsp-ui-card">
      {(title || subtitle) && (
        <header className="ndsp-ui-card__header">
          {title && <h2>{title}</h2>}
          {subtitle && <p>{subtitle}</p>}
        </header>
      )}

      <div className="ndsp-ui-card__body">
        {children}
      </div>
    </section>
  );
}
