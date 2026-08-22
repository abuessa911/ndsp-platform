import type { PropsWithChildren } from "react";
import type { Tone } from "../../types/ui";

type Props = PropsWithChildren<{
  tone?: Tone;
}>;

export function Badge({
  tone = "neutral",
  children
}: Props) {
  return (
    <span className={`ndsp-badge ndsp-badge--${tone}`}>
      {children}
    </span>
  );
}
