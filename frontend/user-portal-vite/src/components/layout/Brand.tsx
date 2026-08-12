type Props = {
  compact?: boolean;
};

export function Brand({ compact = false }: Props) {
  return (
    <div className="ndsp-brand">
      <div className="ndsp-brand__mark" aria-hidden="true">
        N
      </div>

      {!compact && (
        <div className="ndsp-brand__copy">
          <strong>NDSP</strong>
          <span>Decision Support</span>
        </div>
      )}
    </div>
  );
}
