"use client";

import { AnimatePresence, motion } from "motion/react";
import {
  ChevronDown,
  Cpu,
  Lightbulb,
  RotateCcw,
  Undo2,
  Volume2,
  VolumeX,
  FlipVertical2,
} from "lucide-react";
import { useState } from "react";

import { Disc } from "./Disc";
import { formatEval } from "./EvalBar";
import { historyPairs } from "@/lib/game";
import { THEMES, type Theme } from "@/lib/themes";
import {
  DIFFICULTY_BLURB,
  DIFFICULTY_LABELS,
  type Difficulty,
  type HistoryEntry,
  type Material,
  type Player,
  type SearchInfo,
} from "@/lib/types";

interface SidePanelProps {
  theme: Theme;
  themeId: string;
  onThemeChange: (id: string) => void;
  difficulty: Difficulty;
  onDifficultyChange: (value: Difficulty) => void;
  humanSide: Player;
  onSideChange: (side: Player) => void;
  soundOn: boolean;
  onToggleSound: () => void;
  onFlip: () => void;
  onNewGame: () => void;
  onUndo: () => void;
  onHint: () => void;
  canUndo: boolean;
  canHint: boolean;
  thinking: boolean;
  hintPending: boolean;
  turn: Player;
  material: Material;
  evaluation: number;
  search: SearchInfo | null;
  history: HistoryEntry[];
  mustCapture: boolean;
  error: string | null;
}

function Section({
  title,
  children,
  right,
}: {
  title: string;
  children: React.ReactNode;
  right?: React.ReactNode;
}) {
  return (
    <div className="px-4 py-3.5">
      <div className="mb-2.5 flex items-center justify-between">
        <h3 className="text-[10.5px] font-semibold uppercase tracking-[0.14em] text-[var(--text-faint)]">
          {title}
        </h3>
        {right}
      </div>
      {children}
    </div>
  );
}

function CapturedTray({
  count,
  kings,
  player,
  theme,
}: {
  count: number;
  kings: number;
  player: Player;
  theme: Theme;
}) {
  if (count <= 0) {
    return (
      <span className="text-xs text-[var(--text-faint)]">none yet</span>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-[3px]">
      {Array.from({ length: count }, (_, i) => (
        <span key={i} className="h-4 w-4 shrink-0">
          <Disc player={player} king={i < kings} theme={theme} compact />
        </span>
      ))}
    </div>
  );
}

export function SidePanel(props: SidePanelProps) {
  const {
    theme,
    themeId,
    onThemeChange,
    difficulty,
    onDifficultyChange,
    humanSide,
    onSideChange,
    soundOn,
    onToggleSound,
    onFlip,
    onNewGame,
    onUndo,
    onHint,
    canUndo,
    canHint,
    thinking,
    hintPending,
    turn,
    material,
    evaluation,
    search,
    history,
    mustCapture,
    error,
  } = props;

  const [settingsOpen, setSettingsOpen] = useState(false);

  const whiteLeft = material.whiteMen + material.whiteKings;
  const blackLeft = material.blackMen + material.blackKings;
  const rows = historyPairs(history);
  const humanIsWhite = humanSide === 1;
  const yourTurn = turn === humanSide;

  return (
    <aside className="flex w-full flex-col gap-4 lg:w-[350px]">
      {/* status */}
      <div className="panel overflow-hidden">
        <div className="flex items-center gap-3 px-4 py-4">
          <span
            className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-full"
            style={{
              background: turn === 1 ? "var(--white-side)" : "#22252e",
              boxShadow:
                "inset 0 0 0 1px rgba(255,255,255,.18), 0 2px 8px rgba(0,0,0,.5)",
            }}
          >
            {thinking && (
              <motion.span
                className="absolute inset-0 rounded-full"
                style={{ border: "2px solid var(--gold)" }}
                animate={{ opacity: [0.15, 0.85, 0.15], scale: [1, 1.14, 1] }}
                transition={{ duration: 1.25, repeat: Infinity, ease: "easeInOut" }}
              />
            )}
          </span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold">
              {thinking
                ? "Engine is thinking…"
                : yourTurn
                  ? "Your move"
                  : "Engine to move"}
            </p>
            <p className="truncate text-xs text-[var(--text-dim)]">
              {turn === 1 ? "White" : "Black"} to play
              {mustCapture && yourTurn ? " · capture is forced" : ""}
            </p>
          </div>
          <span className="font-mono text-sm font-semibold tabular-nums text-[var(--gold)]">
            {formatEval(evaluation)}
          </span>
        </div>

        <div className="hairline" />

        <Section title="Captured">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="mb-1.5 text-[11px] text-[var(--text-dim)]">
                You took · {12 - (humanIsWhite ? blackLeft : whiteLeft)}
              </p>
              <CapturedTray
                count={12 - (humanIsWhite ? blackLeft : whiteLeft)}
                kings={0}
                player={humanIsWhite ? -1 : 1}
                theme={theme}
              />
            </div>
            <div>
              <p className="mb-1.5 text-[11px] text-[var(--text-dim)]">
                Engine took · {12 - (humanIsWhite ? whiteLeft : blackLeft)}
              </p>
              <CapturedTray
                count={12 - (humanIsWhite ? whiteLeft : blackLeft)}
                kings={0}
                player={humanIsWhite ? 1 : -1}
                theme={theme}
              />
            </div>
          </div>
        </Section>

        <div className="hairline" />

        <Section
          title="Engine"
          right={
            <span className="flex items-center gap-1.5 text-[10.5px] text-[var(--text-faint)]">
              <Cpu size={12} />
              {DIFFICULTY_LABELS[difficulty]}
            </span>
          }
        >
          <div className="grid grid-cols-3 gap-2">
            {[
              { label: "depth", value: search ? search.depth : "—" },
              {
                label: "nodes",
                value: search ? search.nodes.toLocaleString() : "—",
              },
              {
                label: "time",
                value: search ? `${(search.elapsedMs / 1000).toFixed(2)}s` : "—",
              },
            ].map((stat) => (
              <div
                key={stat.label}
                className="rounded-lg px-2 py-2 text-center"
                style={{ background: "rgba(255,255,255,.035)" }}
              >
                <p className="font-mono text-[13px] font-semibold tabular-nums">
                  {stat.value}
                </p>
                <p className="mt-0.5 text-[9.5px] uppercase tracking-wider text-[var(--text-faint)]">
                  {stat.label}
                </p>
              </div>
            ))}
          </div>
        </Section>
      </div>

      {/* actions */}
      <div className="panel p-3">
        <div className="grid grid-cols-2 gap-2">
          <button
            type="button"
            onClick={onNewGame}
            className="chip flex items-center justify-center gap-2 px-3 py-2.5 text-[13px] font-medium"
          >
            <RotateCcw size={14} />
            New game
          </button>
          <button
            type="button"
            onClick={onUndo}
            disabled={!canUndo}
            className="chip flex items-center justify-center gap-2 px-3 py-2.5 text-[13px] font-medium"
          >
            <Undo2 size={14} />
            Undo
          </button>
          <button
            type="button"
            onClick={onHint}
            disabled={!canHint || hintPending}
            className="chip flex items-center justify-center gap-2 px-3 py-2.5 text-[13px] font-medium"
          >
            <Lightbulb size={14} />
            {hintPending ? "Thinking…" : "Hint"}
          </button>
          <button
            type="button"
            onClick={onFlip}
            className="chip flex items-center justify-center gap-2 px-3 py-2.5 text-[13px] font-medium"
          >
            <FlipVertical2 size={14} />
            Flip
          </button>
        </div>

        <button
          type="button"
          onClick={() => setSettingsOpen((open) => !open)}
          className="mt-2 flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-[13px] font-medium text-[var(--text-dim)] transition-colors hover:text-[var(--text)]"
        >
          Settings
          <motion.span animate={{ rotate: settingsOpen ? 180 : 0 }}>
            <ChevronDown size={15} />
          </motion.span>
        </button>

        <AnimatePresence initial={false}>
          {settingsOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.22, ease: "easeOut" }}
              className="overflow-hidden"
            >
              <div className="space-y-4 px-1 pb-1 pt-2">
                <div>
                  <p className="mb-2 text-[10.5px] font-semibold uppercase tracking-[0.14em] text-[var(--text-faint)]">
                    Difficulty
                  </p>
                  <div className="grid grid-cols-5 gap-1.5">
                    {(Object.keys(DIFFICULTY_LABELS) as Difficulty[]).map((key) => (
                      <button
                        key={key}
                        type="button"
                        onClick={() => onDifficultyChange(key)}
                        className={`chip px-1 py-2 text-[11px] font-medium ${
                          difficulty === key ? "chip-active" : ""
                        }`}
                      >
                        {DIFFICULTY_LABELS[key].slice(0, 4)}
                      </button>
                    ))}
                  </div>
                  <p className="mt-2 text-[11px] leading-relaxed text-[var(--text-dim)]">
                    {DIFFICULTY_BLURB[difficulty]}
                  </p>
                </div>

                <div>
                  <p className="mb-2 text-[10.5px] font-semibold uppercase tracking-[0.14em] text-[var(--text-faint)]">
                    You play
                  </p>
                  <div className="grid grid-cols-2 gap-1.5">
                    {([1, -1] as Player[]).map((side) => (
                      <button
                        key={side}
                        type="button"
                        onClick={() => onSideChange(side)}
                        className={`chip px-3 py-2 text-[12px] font-medium ${
                          humanSide === side ? "chip-active" : ""
                        }`}
                      >
                        {side === 1 ? "White (first)" : "Black"}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <p className="mb-2 text-[10.5px] font-semibold uppercase tracking-[0.14em] text-[var(--text-faint)]">
                    Board
                  </p>
                  <div className="grid grid-cols-4 gap-1.5">
                    {THEMES.map((option) => (
                      <button
                        key={option.id}
                        type="button"
                        title={option.name}
                        onClick={() => onThemeChange(option.id)}
                        className="relative h-9 overflow-hidden rounded-lg transition-transform hover:scale-105"
                        style={{
                          boxShadow:
                            themeId === option.id
                              ? `0 0 0 2px ${option.accent}`
                              : "inset 0 0 0 1px rgba(255,255,255,.12)",
                        }}
                      >
                        {/* a 2x2 checker, so the swatch reads as a board */}
                        <span
                          className="absolute inset-0"
                          style={{ background: option.dark }}
                        />
                        <span
                          className="absolute left-0 top-0 h-1/2 w-1/2"
                          style={{ background: option.light }}
                        />
                        <span
                          className="absolute bottom-0 right-0 h-1/2 w-1/2"
                          style={{ background: option.light }}
                        />
                        <span
                          className="absolute inset-0"
                          style={{
                            boxShadow: `inset 0 0 0 2px ${option.frame}`,
                          }}
                        />
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={onToggleSound}
                  className="chip flex w-full items-center justify-center gap-2 px-3 py-2.5 text-[13px] font-medium"
                >
                  {soundOn ? <Volume2 size={14} /> : <VolumeX size={14} />}
                  Sound {soundOn ? "on" : "off"}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* history */}
      <div className="panel flex min-h-0 flex-1 flex-col overflow-hidden">
        <div className="px-4 pb-2 pt-3.5">
          <h3 className="text-[10.5px] font-semibold uppercase tracking-[0.14em] text-[var(--text-faint)]">
            Moves
          </h3>
        </div>
        <div className="hairline" />
        <div className="scroll-thin max-h-[240px] min-h-[92px] flex-1 overflow-y-auto px-2 py-2 lg:max-h-none">
          {rows.length === 0 ? (
            <p className="px-2 py-4 text-center text-xs text-[var(--text-faint)]">
              No moves yet. White opens.
            </p>
          ) : (
            <ol className="space-y-0.5">
              {rows.map((row) => (
                <li
                  key={row.index}
                  className="grid grid-cols-[26px_1fr_1fr] items-center gap-1 rounded-md px-2 py-1 font-mono text-[12.5px]"
                >
                  <span className="text-[var(--text-faint)]">{row.index}.</span>
                  <span className="tabular-nums">
                    {row.white?.notation ?? ""}
                    {row.white?.promoted ? "♔" : ""}
                  </span>
                  <span className="tabular-nums text-[var(--text-dim)]">
                    {row.black?.notation ?? ""}
                    {row.black?.promoted ? "♔" : ""}
                  </span>
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>

      {error && (
        <div
          className="panel px-4 py-3 text-xs"
          style={{ borderColor: "rgba(248,124,124,.4)", color: "var(--bad)" }}
        >
          {error}
        </div>
      )}
    </aside>
  );
}
