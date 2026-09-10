"use client";

import confetti from "canvas-confetti";
import { AnimatePresence, motion } from "motion/react";
import { useEffect } from "react";
import { RotateCcw, Trophy, Handshake, Frown } from "lucide-react";

export type Outcome = "win" | "loss" | "draw";

const COPY: Record<Outcome, { title: string; blurb: string }> = {
  win: { title: "You win", blurb: "The engine has no legal reply." },
  loss: { title: "Engine wins", blurb: "You have no legal reply." },
  draw: { title: "Draw", blurb: "" },
};

export function GameOverOverlay({
  outcome,
  detail,
  onRestart,
  onReview,
}: {
  outcome: Outcome | null;
  detail?: string;
  onRestart: () => void;
  onReview: () => void;
}) {
  useEffect(() => {
    if (outcome !== "win") return;
    const end = Date.now() + 1100;
    const colors = ["#e8c27a", "#f0ead9", "#c9a24a", "#ffffff"];
    const tick = () => {
      confetti({
        particleCount: 4,
        angle: 60,
        spread: 62,
        origin: { x: 0, y: 0.62 },
        colors,
        scalar: 0.9,
      });
      confetti({
        particleCount: 4,
        angle: 120,
        spread: 62,
        origin: { x: 1, y: 0.62 },
        colors,
        scalar: 0.9,
      });
      if (Date.now() < end) requestAnimationFrame(tick);
    };
    tick();
  }, [outcome]);

  const Icon = outcome === "win" ? Trophy : outcome === "draw" ? Handshake : Frown;

  return (
    <AnimatePresence>
      {outcome && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          style={{ background: "rgba(4,5,8,.72)", backdropFilter: "blur(8px)" }}
        >
          <motion.div
            className="panel w-full max-w-sm p-8 text-center"
            initial={{ scale: 0.9, y: 18, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.95, y: 10, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 26 }}
          >
            <div
              className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full"
              style={{
                background:
                  outcome === "win"
                    ? "linear-gradient(180deg, rgba(232,194,122,.28), rgba(232,194,122,.10))"
                    : "rgba(255,255,255,.06)",
                boxShadow: "inset 0 0 0 1px rgba(255,255,255,.12)",
              }}
            >
              <Icon
                size={30}
                strokeWidth={1.6}
                color={outcome === "win" ? "#e8c27a" : "#9ba1ae"}
              />
            </div>

            <h2 className="font-[family-name:var(--font-playfair)] text-3xl font-semibold tracking-tight">
              {COPY[outcome].title}
            </h2>
            <p className="mt-2 text-sm text-[var(--text-dim)]">
              {detail || COPY[outcome].blurb}
            </p>

            <div className="mt-7 flex gap-3">
              <button
                type="button"
                onClick={onReview}
                className="chip flex-1 px-4 py-2.5 text-sm font-medium text-[var(--text-dim)]"
              >
                Review board
              </button>
              <button
                type="button"
                onClick={onRestart}
                className="chip chip-active flex flex-1 items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold"
              >
                <RotateCcw size={15} />
                New game
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
