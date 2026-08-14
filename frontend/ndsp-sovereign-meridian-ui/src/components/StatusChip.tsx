import {
  CheckCircle,
  Info,
  MagnifyingGlass,
  WarningCircle,
  XCircle,
} from "@phosphor-icons/react";
import type { Tone } from "../data";

type StatusChipProps = {
  label: string;
  tone?: Tone;
  compact?: boolean;
};

export function StatusChip({ label, tone = "neutral", compact = false }: StatusChipProps) {
  const Icon =
    tone === "success"
      ? CheckCircle
      : tone === "warning"
        ? WarningCircle
        : tone === "danger"
          ? XCircle
          : tone === "review"
            ? MagnifyingGlass
            : Info;

  return (
    <span className={`status-chip status-chip--${tone} ${compact ? "status-chip--compact" : ""}`}>
      <Icon size={compact ? 14 : 16} weight="fill" aria-hidden="true" />
      <span>{label}</span>
    </span>
  );
}
