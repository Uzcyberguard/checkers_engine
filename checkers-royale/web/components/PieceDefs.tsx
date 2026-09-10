"use client";

import type { Theme } from "@/lib/themes";

/**
 * Gradient definitions live once per board rather than once per disc, so 24
 * pieces share four gradients instead of duplicating ids across the document.
 */
export function PieceDefs({ theme }: { theme: Theme }) {
  const sets: [string, [string, string, string]][] = [
    ["light", theme.pieceLight],
    ["dark", theme.pieceDark],
  ];

  return (
    <svg width="0" height="0" aria-hidden className="absolute">
      <defs>
        {sets.map(([key, [highlight, base, shade]]) => (
          <g key={key}>
            <radialGradient id={`pc-${key}-face`} cx="34%" cy="28%" r="82%">
              <stop offset="0%" stopColor={highlight} />
              <stop offset="52%" stopColor={base} />
              <stop offset="100%" stopColor={shade} />
            </radialGradient>
            <radialGradient id={`pc-${key}-inner`} cx="38%" cy="32%" r="70%">
              <stop offset="0%" stopColor={highlight} stopOpacity="0.9" />
              <stop offset="100%" stopColor={base} stopOpacity="0.15" />
            </radialGradient>
            <linearGradient id={`pc-${key}-wall`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={base} />
              <stop offset="100%" stopColor={shade} />
            </linearGradient>
          </g>
        ))}
        <radialGradient id="pc-gloss" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.55" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
        </radialGradient>
      </defs>
    </svg>
  );
}
