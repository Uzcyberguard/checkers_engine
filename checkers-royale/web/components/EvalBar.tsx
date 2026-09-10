"use client";

import { motion } from "motion/react";

/** Map a centipawn score onto 0..1 the way a chess eval bar does. */
export function evalFraction(score: number) {
  return 1 / (1 + Math.exp(-score / 380));
}

export function formatEval(score: number) {
  if (Math.abs(score) >= 900_000) {
    return score > 0 ? "+M" : "-M";
  }
  const pawns = score / 100;
  return `${pawns > 0 ? "+" : ""}${pawns.toFixed(1)}`;
}

export function EvalBar({
  score,
  flipped,
}: {
  score: number;
  flipped: boolean;
}) {
  const whiteShare = evalFraction(score);
  // The bar always shows the side at the bottom of the screen at the bottom.
  const bottomShare = flipped ? 1 - whiteShare : whiteShare;

  return (
    <div className="hidden shrink-0 flex-col items-center gap-2 lg:flex">
      <span className="font-mono text-[10px] tracking-wider text-[var(--text-faint)]">
        {flipped ? "BLACK" : "WHITE"}
      </span>
      <div
        className="relative w-3 flex-1 overflow-hidden rounded-full"
        style={{
          background: "#20222a",
          boxShadow:
            "inset 0 0 0 1px rgba(255,255,255,.09), inset 0 2px 6px rgba(0,0,0,.55)",
        }}
        title={`Engine evaluation: ${formatEval(score)}`}
      >
        <motion.div
          className="absolute inset-x-0 bottom-0"
          style={{
            background:
              "linear-gradient(180deg, var(--white-side), #cfc7b0)",
          }}
          animate={{ height: `${bottomShare * 100}%` }}
          transition={{ type: "spring", stiffness: 120, damping: 22 }}
        />
        <div
          className="absolute inset-x-0"
          style={{
            top: "50%",
            height: 1,
            background: "rgba(0,0,0,.55)",
          }}
        />
      </div>
      <span className="font-mono text-[11px] font-semibold tabular-nums text-[var(--text-dim)]">
        {formatEval(score)}
      </span>
    </div>
  );
}
