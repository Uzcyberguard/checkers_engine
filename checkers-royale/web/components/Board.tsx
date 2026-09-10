"use client";

import { AnimatePresence, motion } from "motion/react";
import { useMemo } from "react";

import { Disc } from "./Disc";
import { PieceDefs } from "./PieceDefs";
import type { Theme } from "@/lib/themes";
import type { PieceView, Player, Square } from "@/lib/types";

const FILES = ["a", "b", "c", "d", "e", "f", "g", "h"];

export interface BoardProps {
  theme: Theme;
  pieces: PieceView[];
  flipped: boolean;
  selected: Square | null;
  partialPath: Square[];
  stops: Square[];
  captureStops: boolean;
  movableSquares: Square[];
  lastMovePath: Square[] | null;
  animation: { id: number; path: Square[] } | null;
  interactive: boolean;
  onSquareClick: (row: number, col: number) => void;
}

function keyOf(square: Square) {
  return `${square[0]},${square[1]}`;
}

export function Board({
  theme,
  pieces,
  flipped,
  selected,
  partialPath,
  stops,
  captureStops,
  movableSquares,
  lastMovePath,
  animation,
  interactive,
  onSquareClick,
}: BoardProps) {
  const stopSet = useMemo(() => new Set(stops.map(keyOf)), [stops]);
  const movableSet = useMemo(
    () => new Set(movableSquares.map(keyOf)),
    [movableSquares],
  );
  const lastSet = useMemo(
    () =>
      new Set(
        lastMovePath
          ? [lastMovePath[0], lastMovePath[lastMovePath.length - 1]].map(keyOf)
          : [],
      ),
    [lastMovePath],
  );
  const pathSet = useMemo(() => new Set(partialPath.map(keyOf)), [partialPath]);

  const view = (row: number, col: number) =>
    flipped ? { row: 7 - row, col: 7 - col } : { row, col };

  const ranks = flipped ? [1, 2, 3, 4, 5, 6, 7, 8] : [8, 7, 6, 5, 4, 3, 2, 1];
  const files = flipped ? [...FILES].reverse() : FILES;

  return (
    <div
      className="board-frame relative w-full select-none"
      style={{
        background: `linear-gradient(160deg, ${theme.frameEdge}, ${theme.frame} 55%, ${theme.frame})`,
      }}
    >
      <PieceDefs theme={theme} />

      {/* rank numbers, aligned to the eight rows of the playing surface */}
      <div
        className="pointer-events-none absolute left-0 flex flex-col"
        style={{
          width: "var(--gutter)",
          top: "var(--gutter)",
          height: "calc(100% - 2 * var(--gutter))",
        }}
      >
        {ranks.map((rank) => (
          <div
            key={rank}
            className="flex flex-1 items-center justify-center font-mono text-[clamp(8px,1.3vw,13px)] font-semibold"
            style={{ color: theme.label }}
          >
            {rank}
          </div>
        ))}
      </div>

      {/* file letters */}
      <div
        className="pointer-events-none absolute bottom-0 flex"
        style={{
          height: "var(--gutter)",
          left: "var(--gutter)",
          width: "calc(100% - 2 * var(--gutter))",
        }}
      >
        {files.map((file) => (
          <div
            key={file}
            className="flex flex-1 items-center justify-center font-mono text-[clamp(8px,1.3vw,13px)] font-semibold"
            style={{ color: theme.label }}
          >
            {file}
          </div>
        ))}
      </div>

      <div className="board-inner relative aspect-square w-full overflow-hidden">
        {/* squares */}
        <div className="absolute inset-0 grid grid-cols-8 grid-rows-8">
          {Array.from({ length: 64 }, (_, index) => {
            const dRow = Math.floor(index / 8);
            const dCol = index % 8;
            const row = flipped ? 7 - dRow : dRow;
            const col = flipped ? 7 - dCol : dCol;
            const dark = (row + col) % 2 === 1;
            const id = `${row},${col}`;

            return (
              <button
                key={index}
                type="button"
                aria-label={`${FILES[col]}${8 - row}`}
                disabled={!interactive}
                onClick={() => onSquareClick(row, col)}
                className="relative block h-full w-full"
                style={{
                  background: dark ? theme.dark : theme.light,
                  cursor: interactive ? "pointer" : "default",
                }}
              >
                {lastSet.has(id) && (
                  <span
                    className="pointer-events-none absolute inset-0"
                    style={{ background: theme.accent, opacity: 0.26 }}
                  />
                )}
                {pathSet.has(id) && (
                  <span
                    className="pointer-events-none absolute inset-0"
                    style={{ background: theme.accent, opacity: 0.34 }}
                  />
                )}
              </button>
            );
          })}
        </div>

        {/* subtle sheen across the whole playing surface */}
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              "linear-gradient(150deg, rgba(255,255,255,0.10), rgba(255,255,255,0) 42%, rgba(0,0,0,0.16))",
          }}
        />

        {/* move hints */}
        <div className="pointer-events-none absolute inset-0">
          {stops.map((square) => {
            const { row, col } = view(square[0], square[1]);
            return (
              <motion.div
                key={`stop-${keyOf(square)}`}
                initial={{ scale: 0.4, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.4, opacity: 0 }}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
                className="absolute flex items-center justify-center"
                style={{
                  width: "12.5%",
                  height: "12.5%",
                  left: `${col * 12.5}%`,
                  top: `${row * 12.5}%`,
                }}
              >
                {captureStops ? (
                  <span
                    className="block rounded-full"
                    style={{
                      width: "82%",
                      height: "82%",
                      border: `clamp(3px,0.7vw,6px) solid ${theme.accent}`,
                      opacity: 0.9,
                      boxShadow: `0 0 18px ${theme.accent}66`,
                    }}
                  />
                ) : (
                  <span
                    className="block rounded-full"
                    style={{
                      width: "30%",
                      height: "30%",
                      background: theme.accent,
                      opacity: 0.72,
                      boxShadow: `0 0 14px ${theme.accent}55`,
                    }}
                  />
                )}
              </motion.div>
            );
          })}

          {/* pieces that are obliged to capture */}
          {!selected &&
            movableSquares.length > 0 &&
            movableSquares.map((square) => {
              const { row, col } = view(square[0], square[1]);
              return (
                <motion.span
                  key={`must-${keyOf(square)}`}
                  animate={{ opacity: [0.25, 0.6, 0.25] }}
                  transition={{ duration: 2.1, repeat: Infinity, ease: "easeInOut" }}
                  className="absolute rounded-full"
                  style={{
                    width: "12.5%",
                    height: "12.5%",
                    left: `${col * 12.5}%`,
                    top: `${row * 12.5}%`,
                    boxShadow: `inset 0 0 0 clamp(2px,0.45vw,4px) ${theme.accent}`,
                  }}
                />
              );
            })}
        </div>

        {/* pieces */}
        <div className="pointer-events-none absolute inset-0">
          <AnimatePresence>
            {pieces.map((piece) => {
              const { row, col } = view(piece.row, piece.col);
              const isSelected =
                selected != null &&
                selected[0] === piece.row &&
                selected[1] === piece.col;

              const hopping =
                animation && animation.id === piece.id && animation.path.length > 2;

              const target = hopping
                ? {
                    x: animation.path.map(
                      (sq) => `${view(sq[0], sq[1]).col * 100}%`,
                    ),
                    y: animation.path.map(
                      (sq) => `${view(sq[0], sq[1]).row * 100}%`,
                    ),
                  }
                : { x: `${col * 100}%`, y: `${row * 100}%` };

              return (
                <motion.div
                  key={piece.id}
                  className="absolute"
                  style={{ width: "12.5%", height: "12.5%", left: 0, top: 0 }}
                  initial={{
                    x: `${col * 100}%`,
                    y: `${row * 100}%`,
                    scale: 0.4,
                    opacity: 0,
                  }}
                  animate={{ ...target, scale: 1, opacity: 1 }}
                  exit={{
                    scale: 0.35,
                    opacity: 0,
                    rotate: 28,
                    transition: { duration: 0.26, ease: "easeIn" },
                  }}
                  transition={
                    hopping
                      ? {
                          x: { duration: 0.19 * (animation.path.length - 1), ease: "easeInOut" },
                          y: { duration: 0.19 * (animation.path.length - 1), ease: "easeInOut" },
                          scale: { type: "spring", stiffness: 480, damping: 26 },
                          opacity: { duration: 0.18 },
                        }
                      : {
                          type: "spring",
                          stiffness: 430,
                          damping: 34,
                          opacity: { duration: 0.18 },
                        }
                  }
                >
                  <motion.div
                    className="relative h-full w-full"
                    animate={{
                      scale: isSelected ? 1.09 : 1,
                      filter: isSelected
                        ? `drop-shadow(0 0 10px ${theme.accent})`
                        : "drop-shadow(0 3px 5px rgba(0,0,0,0.45))",
                    }}
                    transition={{ type: "spring", stiffness: 400, damping: 26 }}
                    style={{ padding: "7%" }}
                  >
                    <Disc player={piece.player as Player} king={piece.king} theme={theme} />
                  </motion.div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
