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
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="flex-shrink-0"
      >
        {/* Background circle with gradient */}
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#0ea5e9" />
            <stop offset="50%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22d3ee" />
            <stop offset="100%" stopColor="#a78bfa" />
          </linearGradient>
        </defs>

        {/* Outer ring */}
        <circle
          cx="32"
          cy="32"
          r="30"
          stroke="url(#logoGradient)"
          strokeWidth="2"
          fill="none"
          opacity="0.3"
        />

        {/* Inner filled circle */}
        <circle cx="32" cy="32" r="26" fill="url(#logoGradient)" opacity="0.15" />

        {/* Upward trend line - represents growth */}
        <path
          d="M14 44 L24 34 L32 38 L42 24 L50 20"
          stroke="url(#lineGradient)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />

        {/* Arrow head at the end */}
        <path
          d="M46 18 L50 20 L48 24"
          stroke="url(#lineGradient)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />

        {/* Data points on the line */}
        <circle cx="24" cy="34" r="3" fill="#22d3ee" />
        <circle cx="32" cy="38" r="3" fill="#6366f1" />
        <circle cx="42" cy="24" r="3" fill="#a78bfa" />

        {/* Horizontal baseline */}
        <line
          x1="14"
          y1="48"
          x2="50"
          y2="48"
          stroke="#475569"
          strokeWidth="1.5"
          strokeLinecap="round"
          opacity="0.5"
        />
      </svg>

      {showText && (
        <span
          className={`${text} font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-indigo-400 to-violet-400`}
        >
          Stratos
        </span>
      )}
    </div>
  );
}
