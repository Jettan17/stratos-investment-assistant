"use client";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  showText?: boolean;
}

const sizes = {
  sm: { icon: 32, text: "text-xl" },
  md: { icon: 48, text: "text-3xl" },
  lg: { icon: 64, text: "text-5xl" },
};

export default function Logo({ size = "lg", showText = true }: LogoProps) {
  const { icon, text } = sizes[size];

  return (
    <div className="flex items-center gap-3">
      <svg
        width={icon}
        height={icon}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="flex-shrink-0"
      >
        <defs>
          <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#1e3a5f" />
            <stop offset="100%" stopColor="#2d5a87" />
          </linearGradient>
          <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#4a90d9" />
            <stop offset="100%" stopColor="#6ba3e0" />
          </linearGradient>
        </defs>

        {/* Layered ascending bars */}
        <g transform="translate(4, 6)">
          {/* Bottom layer (widest) */}
          <rect x="0" y="30" width="40" height="7" rx="2" fill="url(#barGradient)" opacity="0.4" />
          {/* Middle layer */}
          <rect x="5" y="20" width="30" height="7" rx="2" fill="url(#barGradient)" opacity="0.7" />
          {/* Top layer (accent color) */}
          <rect x="10" y="10" width="20" height="7" rx="2" fill="url(#accentGradient)" />
          {/* Peak indicator */}
          <polygon points="20,0 25,8 15,8" fill="url(#accentGradient)" />
        </g>
      </svg>

      {showText && (
        <span
          className={`${text} font-semibold tracking-wide text-slate-800 dark:text-slate-100`}
        >
          STRATOS
        </span>
      )}
    </div>
  );
}
