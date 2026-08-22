import type {
  ButtonHTMLAttributes,
  PropsWithChildren
} from "react";

import { cn } from "../../lib/cn";

type Variant = "primary" | "secondary" | "ghost" | "danger";

type Props = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: Variant;
  }
>;

export function Button({
  children,
  variant = "primary",
  className,
  ...props
}: Props) {
  return (
    <button
      className={cn(
        "ndsp-button",
        `ndsp-button--${variant}`,
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
