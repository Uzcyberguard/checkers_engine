"use client";

import type { Theme } from "@/lib/themes";

interface DiscProps {
  player: 1 | -1;
  king: boolean;
  theme: Theme;
  /** Small standalone rendering, e.g. in the captured-pieces tray. */
  compact?: boolean;
}

export function Disc({ player, king, theme, compact = false }: DiscProps) {
  const key = player === 1 ? "light" : "dark";
  const shade = player === 1 ? theme.pieceLight[2] : theme.pieceDark[2];
  const crown = player === 1 ? theme.crownLight : theme.crownDark;

  return (
    <svg
      viewBox="0 0 100 100"
      className="h-full w-full"
      style={{ overflow: "visible" }}
    >
      {!compact && (
        <ellipse cx="50" cy="84" rx="33" ry="7.5" fill="rgba(0,0,0,0.38)" />
      )}

      {/* the side wall, which gives the disc its thickness */}
      <circle cx="50" cy="55" r="37" fill={`url(#pc-${key}-wall)`} />
      <circle cx="50" cy="55" r="37" fill="rgba(0,0,0,0.22)" />

      {/* top face */}
      <circle cx="50" cy="49" r="37" fill={`url(#pc-${key}-face)`} />

      {/* turned grooves */}
      <circle
        cx="50"
        cy="49"
        r="30.5"
        fill="none"
        stroke={shade}
        strokeOpacity="0.34"
        strokeWidth="1.6"
      />
      <circle
        cx="50"
        cy="49"
        r="26"
        fill="none"
        stroke={shade}
        strokeOpacity="0.22"
        strokeWidth="1.1"
      />
      <circle cx="50" cy="49" r="23" fill={`url(#pc-${key}-inner)`} />

      {king ? (
        <g
          transform="translate(50 49) scale(0.30) translate(-50 -49)"
          fill={crown}
          stroke="rgba(0,0,0,0.35)"
          strokeWidth="2.5"
          strokeLinejoin="round"
        >
          <path d="M31 58 L26 34 L39.5 44 L50 27 L60.5 44 L74 34 L69 58 Z" />
          <rect x="30" y="59" width="40" height="9" rx="4.5" />
          <circle cx="26" cy="32" r="5" />
          <circle cx="50" cy="25" r="5.5" />
          <circle cx="74" cy="32" r="5" />
        </g>
      ) : (
        <circle
          cx="50"
          cy="49"
          r="12"
          fill="none"
          stroke={shade}
          strokeOpacity="0.16"
          strokeWidth="1"
        />
      )}

      {/* specular highlight */}
      <ellipse
        cx="37"
        cy="32"
        rx="17"
        ry="10.5"
        fill="url(#pc-gloss)"
        transform="rotate(-28 37 32)"
      />
    </svg>
  );
}
