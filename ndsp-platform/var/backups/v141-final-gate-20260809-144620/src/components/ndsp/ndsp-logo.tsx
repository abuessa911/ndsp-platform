type NdspLogoProps = {
  compact?: boolean
}

export function NdspLogo({ compact = false }: NdspLogoProps) {
  return (
    <a
      className="sovereign-logo"
      href="/"
      aria-label="NDSP — منصة نواف لدعم القرار"
    >
      <svg
        className="sovereign-logo__mark"
        viewBox="0 0 64 64"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="ndspGold" x1="8" y1="5" x2="55" y2="58">
            <stop offset="0" stopColor="#F1D58B" />
            <stop offset="0.35" stopColor="#D4AF37" />
            <stop offset="0.7" stopColor="#A97D2D" />
            <stop offset="1" stopColor="#E5C36D" />
          </linearGradient>

          <filter id="ndspMarkGlow">
            <feGaussianBlur stdDeviation="2.3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <path
          d="M11 8v14l17 10-17 10v14"
          fill="none"
          stroke="url(#ndspGold)"
          strokeWidth="3"
          strokeLinecap="square"
        />

        <path
          d="M11 22h24M11 42h24"
          fill="none"
          stroke="url(#ndspGold)"
          strokeWidth="3"
        />

        <path
          d="M34 10v44"
          fill="none"
          stroke="url(#ndspGold)"
          strokeWidth="2.4"
        />

        <path
          d="M34 32h12"
          fill="none"
          stroke="url(#ndspGold)"
          strokeWidth="2"
        />

        <path
          d="M53 32l-9-6v12z"
          fill="#29B6F6"
          filter="url(#ndspMarkGlow)"
        />
      </svg>

      {!compact && (
        <span className="sovereign-logo__copy">
          <strong>NDSP</strong>
          <span>منصة نواف لدعم القرار</span>
        </span>
      )}
    </a>
  )
}
