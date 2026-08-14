type BrandProps = {
  compact?: boolean;
  className?: string;
  language?: "ar" | "en";
};

export function Brand({
  compact = false,
  className = "",
  language = "ar",
}: BrandProps) {
  const subtitle = language === "ar" ? "منصة دعم القرار" : "Decision Support Platform";

  return (
    <span
      className={`brand ${compact ? "brand--compact" : ""} ${className}`.trim()}
      aria-label={`NDSP — ${subtitle}`}
    >
      <img src="/assets/ndsp-mark.png" alt="" aria-hidden="true" />
      <span className="brand__wordmark" dir="ltr">NDSP</span>
      <span className="brand__subtitle">{subtitle}</span>
    </span>
  );
}
