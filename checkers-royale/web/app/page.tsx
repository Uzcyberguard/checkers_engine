"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { motion } from "motion/react";

import { Board } from "@/components/Board";
import { EvalBar } from "@/components/EvalBar";
import { GameOverOverlay, type Outcome } from "@/components/GameOverOverlay";
import { SidePanel } from "@/components/SidePanel";
import * as api from "@/lib/api";
import {
  applyMoveToPieces,
  completedMove,
  freshDrawState,
  movesFromSquare,
  nextStops,
  piecesFromBoard,
  recordPosition,
  sameSquare,
  type DrawState,
} from "@/lib/game";
import { sounds } from "@/lib/sound";
import { DEFAULT_THEME, themeById } from "@/lib/themes";
import type {
  ApiMove,
  Board as BoardType,
  Difficulty,
  HistoryEntry,
  Material,
  PieceView,
  Player,
  SearchInfo,
  Square,
  Status,
} from "@/lib/types";

interface Snapshot {
  board: BoardType;
  pieces: PieceView[];
  turn: Player;
  moves: ApiMove[];
  material: Material;
  evaluation: number;
  mustCapture: boolean;
  history: HistoryEntry[];
  draw: DrawState;
  lastMovePath: Square[] | null;
}

const EMPTY_MATERIAL: Material = {
  whiteMen: 12,
  whiteKings: 0,
  blackMen: 12,
  blackKings: 0,
};

export default function Page() {
  const [board, setBoard] = useState<BoardType | null>(null);
  const [pieces, setPieces] = useState<PieceView[]>([]);
  const [turn, setTurn] = useState<Player>(1);
  const [moves, setMoves] = useState<ApiMove[]>([]);
  const [material, setMaterial] = useState<Material>(EMPTY_MATERIAL);
  const [evaluation, setEvaluation] = useState(0);
  const [mustCapture, setMustCapture] = useState(false);
  const [status, setStatus] = useState<Status>("playing");

  const [selected, setSelected] = useState<Square | null>(null);
  const [partialPath, setPartialPath] = useState<Square[]>([]);
  const [lastMovePath, setLastMovePath] = useState<Square[] | null>(null);
  const [animation, setAnimation] = useState<{ id: number; path: Square[] } | null>(
    null,
  );

  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [search, setSearch] = useState<SearchInfo | null>(null);
  const [thinking, setThinking] = useState(false);
  const [hintPending, setHintPending] = useState(false);
  const [hintMove, setHintMove] = useState<ApiMove | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [difficulty, setDifficulty] = useState<Difficulty>("normal");
  const [themeId, setThemeId] = useState(DEFAULT_THEME.id);
  const [humanSide, setHumanSide] = useState<Player>(1);
  const [flipped, setFlipped] = useState(false);
  const [soundOn, setSoundOn] = useState(true);

  const [drawState, setDrawState] = useState<DrawState>(freshDrawState);
  const [drawReason, setDrawReason] = useState<string | null>(null);
  const [overlayDismissed, setOverlayDismissed] = useState(false);

  const undoStack = useRef<Snapshot[]>([]);
  const [undoDepth, setUndoDepth] = useState(0);
  const bootstrapped = useRef(false);
  const busy = useRef(false);

  const theme = useMemo(() => themeById(themeId), [themeId]);

  useEffect(() => {
    sounds.enabled = soundOn;
  }, [soundOn]);

  // -- persistence of preferences ---------------------------------------

  useEffect(() => {
    try {
      const raw = localStorage.getItem("checkers-royale:prefs");
      if (!raw) return;
      const prefs = JSON.parse(raw);
      if (typeof prefs.themeId === "string") setThemeId(prefs.themeId);
      if (typeof prefs.difficulty === "string") setDifficulty(prefs.difficulty);
      if (typeof prefs.soundOn === "boolean") setSoundOn(prefs.soundOn);
    } catch {
      /* preferences are a nicety; ignore a blocked or corrupt store */
    }
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(
        "checkers-royale:prefs",
        JSON.stringify({ themeId, difficulty, soundOn }),
      );
    } catch {
      /* ignore */
    }
  }, [themeId, difficulty, soundOn]);

  // -- helpers -----------------------------------------------------------

  const applyReport = useCallback(
    (report: {
      board: BoardType;
      player: Player;
      moves: ApiMove[];
      material: Material;
      evaluation: number;
      mustCapture: boolean;
      status: Status;
    }) => {
      setBoard(report.board);
      setTurn(report.player);
      setMoves(report.moves);
      setMaterial(report.material);
      setEvaluation(report.evaluation);
      setMustCapture(report.mustCapture);
      setStatus(report.status);
    },
    [],
  );

  const playMoveSound = useCallback((move: ApiMove) => {
    if (move.captured.length > 0) {
      sounds.play("capture", 1 + Math.min(move.captured.length - 1, 3) * 0.06);
    } else {
      sounds.play("move", 0.96 + Math.random() * 0.08);
    }
    if (move.promoted) {
      window.setTimeout(() => sounds.play("king"), 180);
    }
  }, []);

  const runAnimation = useCallback((movedId: number | undefined, move: ApiMove) => {
    if (movedId == null || move.path.length <= 2) {
      setAnimation(null);
      return;
    }
    setAnimation({ id: movedId, path: move.path });
    window.setTimeout(
      () => setAnimation(null),
      190 * (move.path.length - 1) + 120,
    );
  }, []);

  // -- engine turn -------------------------------------------------------

  const engineTurn = useCallback(
    async (
      fromBoard: BoardType,
      enginePlayer: Player,
      currentPieces: PieceView[],
      draw: DrawState,
    ) => {
      setThinking(true);
      setError(null);
      try {
        const report = await api.getAiMove(
          fromBoard,
          enginePlayer,
          difficulty,
          Math.floor(Math.random() * 1_000_000),
        );
        setSearch(report.search);

        if (!report.move) {
          // The engine has no legal reply: the human has won.
          setStatus(report.status);
          setThinking(false);
          return;
        }

        const move = report.move;
        const movedId = currentPieces.find(
          (piece) =>
            piece.row === move.path[0][0] && piece.col === move.path[0][1],
        )?.id;

        const nextPieces = applyMoveToPieces(currentPieces, move);
        setPieces(nextPieces);
        setLastMovePath(move.path);
        runAnimation(movedId, move);
        playMoveSound(move);

        applyReport(report);
        setHistory((prev) => [
          ...prev,
          {
            notation: move.notation,
            player: enginePlayer,
            captured: move.captured.length,
            promoted: move.promoted,
            board: report.board,
            evaluation: report.evaluation,
          },
        ]);

        const { state, drawReason: reason } = recordPosition(
          draw,
          report.board,
          report.player,
          move,
        );
        setDrawState(state);
        if (reason) setDrawReason(reason);
      } catch (caught) {
        setError(
          caught instanceof Error ? caught.message : "The engine did not respond.",
        );
      } finally {
        setThinking(false);
        busy.current = false;
      }
    },
    [applyReport, difficulty, playMoveSound, runAnimation],
  );

  // -- new game ----------------------------------------------------------

  const startGame = useCallback(
    async (side: Player) => {
      busy.current = true;
      setError(null);
      setSelected(null);
      setPartialPath([]);
      setLastMovePath(null);
      setAnimation(null);
      setHistory([]);
      setSearch(null);
      setHintMove(null);
      setDrawReason(null);
      setOverlayDismissed(false);
      setDrawState(freshDrawState());
      undoStack.current = [];
      setUndoDepth(0);
      setFlipped(side === -1);

      try {
        const report = await api.newGame();
        const startPieces = piecesFromBoard(report.board);
        setPieces(startPieces);
        applyReport(report);

        if (side === -1) {
          await engineTurn(report.board, 1, startPieces, freshDrawState());
        } else {
          busy.current = false;
        }
      } catch (caught) {
        setError(
          caught instanceof Error
            ? caught.message
            : "Could not reach the engine to start a game.",
        );
        busy.current = false;
      }
    },
    [applyReport, engineTurn],
  );

  useEffect(() => {
    if (bootstrapped.current) return;
    bootstrapped.current = true;
    void startGame(1);
  }, [startGame]);

  // -- interaction -------------------------------------------------------

  const humanTurn = turn === humanSide && status === "playing" && !drawReason;
  const interactive = humanTurn && !thinking && !busy.current;

  const selectableMoves = useMemo(
    () => (selected ? movesFromSquare(moves, selected) : []),
    [moves, selected],
  );

  const stops = useMemo(
    () => (partialPath.length ? nextStops(selectableMoves, partialPath) : []),
    [selectableMoves, partialPath],
  );

  const movableSquares = useMemo(() => {
    if (!humanTurn || !mustCapture) return [];
    const seen = new Set<string>();
    const out: Square[] = [];
    moves.forEach((move) => {
      const key = `${move.path[0][0]},${move.path[0][1]}`;
      if (!seen.has(key)) {
        seen.add(key);
        out.push(move.path[0]);
      }
    });
    return out;
  }, [humanTurn, mustCapture, moves]);

  const commitHumanMove = useCallback(
    async (move: ApiMove) => {
      if (!board) return;
      busy.current = true;

      undoStack.current.push({
        board,
        pieces,
        turn,
        moves,
        material,
        evaluation,
        mustCapture,
        history,
        draw: drawState,
        lastMovePath,
      });
      setUndoDepth(undoStack.current.length);

      const movedId = pieces.find(
        (piece) => piece.row === move.path[0][0] && piece.col === move.path[0][1],
      )?.id;

      const nextPieces = applyMoveToPieces(pieces, move);
      setPieces(nextPieces);
      setSelected(null);
      setPartialPath([]);
      setHintMove(null);
      setLastMovePath(move.path);
      runAnimation(movedId, move);
      playMoveSound(move);

      setHistory((prev) => [
        ...prev,
        {
          notation: move.notation,
          player: humanSide,
          captured: move.captured.length,
          promoted: move.promoted,
          board: move.board,
          evaluation,
        },
      ]);

      const engineSide = (humanSide === 1 ? -1 : 1) as Player;
      setBoard(move.board);
      setTurn(engineSide);
      setMoves([]);

      const { state, drawReason: reason } = recordPosition(
        drawState,
        move.board,
        engineSide,
        move,
      );
      setDrawState(state);
      if (reason) {
        setDrawReason(reason);
        busy.current = false;
        return;
      }

      await engineTurn(move.board, engineSide, nextPieces, state);
    },
    [
      board,
      drawState,
      engineTurn,
      evaluation,
      history,
      humanSide,
      lastMovePath,
      material,
      mustCapture,
      moves,
      pieces,
      playMoveSound,
      runAnimation,
      turn,
    ],
  );

  const handleSquareClick = useCallback(
    (row: number, col: number) => {
      sounds.preload();
      if (!interactive || !board) return;
      const square: Square = [row, col];

      // Continuing or completing a sequence already begun.
      if (partialPath.length) {
        const isStop = stops.some((stop) => sameSquare(stop, square));
        if (isStop) {
          const extended = [...partialPath, square];
          const done = completedMove(selectableMoves, extended);
          if (done) {
            void commitHumanMove(done);
          } else {
            setPartialPath(extended);
            sounds.play("select", 1.08);
          }
          return;
        }
      }

      // Selecting one of your own pieces.
      const owned = moves.some((move) => sameSquare(move.path[0], square));
      if (owned) {
        setSelected(square);
        setPartialPath([square]);
        sounds.play("select");
        return;
      }

      const occupiedByYou = pieces.some(
        (piece) =>
          piece.row === row && piece.col === col && piece.player === humanSide,
      );
      if (occupiedByYou && mustCapture) {
        sounds.play("illegal");
      }

      setSelected(null);
      setPartialPath([]);
    },
    [
      board,
      commitHumanMove,
      humanSide,
      interactive,
      moves,
      mustCapture,
      partialPath,
      pieces,
      selectableMoves,
      stops,
    ],
  );

  // -- controls ----------------------------------------------------------

  const handleUndo = useCallback(() => {
    const snapshot = undoStack.current.pop();
    if (!snapshot) return;
    setUndoDepth(undoStack.current.length);
    sounds.play("ui");
    setBoard(snapshot.board);
    setPieces(snapshot.pieces);
    setTurn(snapshot.turn);
    setMoves(snapshot.moves);
    setMaterial(snapshot.material);
    setEvaluation(snapshot.evaluation);
    setMustCapture(snapshot.mustCapture);
    setHistory(snapshot.history);
    setDrawState(snapshot.draw);
    setLastMovePath(snapshot.lastMovePath);
    setSelected(null);
    setPartialPath([]);
    setHintMove(null);
    setDrawReason(null);
    setStatus("playing");
    setOverlayDismissed(false);
    setAnimation(null);
  }, []);

  const handleHint = useCallback(async () => {
    if (!board || !humanTurn) return;
    setHintPending(true);
    try {
      const report = await api.getHint(board, humanSide);
      if (report.move) {
        setHintMove(report.move);
        setSelected(report.move.path[0]);
        setPartialPath([report.move.path[0]]);
        sounds.play("ui");
      }
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Hint unavailable.");
    } finally {
      setHintPending(false);
    }
  }, [board, humanSide, humanTurn]);

  const handleSideChange = useCallback(
    (side: Player) => {
      if (side === humanSide) return;
      setHumanSide(side);
      void startGame(side);
    },
    [humanSide, startGame],
  );

  // -- outcome -----------------------------------------------------------

  const outcome: Outcome | null = useMemo(() => {
    if (drawReason) return "draw";
    if (status === "playing") return null;
    const humanWon =
      (status === "white_wins" && humanSide === 1) ||
      (status === "black_wins" && humanSide === -1);
    return humanWon ? "win" : "loss";
  }, [drawReason, humanSide, status]);

  const outcomeAnnounced = useRef<Outcome | null>(null);
  useEffect(() => {
    if (!outcome) {
      outcomeAnnounced.current = null;
      return;
    }
    if (outcomeAnnounced.current === outcome) return;
    outcomeAnnounced.current = outcome;
    window.setTimeout(() => {
      sounds.play(outcome === "win" ? "win" : outcome === "draw" ? "draw" : "lose");
    }, 380);
  }, [outcome]);

  const hintSquares = useMemo<Square[]>(
    () => (hintMove ? nextStops([hintMove], [hintMove.path[0]]) : []),
    [hintMove],
  );

  const shownStops = partialPath.length ? stops : hintSquares;

  return (
    <div className="scene-glow relative min-h-dvh">
      <main className="relative z-10 mx-auto flex min-h-dvh max-w-[1260px] flex-col gap-6 px-4 py-6 sm:px-6 lg:py-8">
        <header className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <motion.h1
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="font-[family-name:var(--font-playfair)] text-[28px] font-semibold leading-none tracking-tight sm:text-[34px]"
            >
              Checkers <span style={{ color: "var(--gold)" }}>Royale</span>
            </motion.h1>
            <p className="mt-1.5 text-[12.5px] text-[var(--text-dim)]">
              Russian draughts · flying kings · captures are compulsory
            </p>
          </div>
          <div className="flex items-center gap-2 text-[11px] text-[var(--text-faint)]">
            <span
              className="inline-block h-1.5 w-1.5 rounded-full"
              style={{
                background: error ? "var(--bad)" : "var(--good)",
                boxShadow: `0 0 8px ${error ? "var(--bad)" : "var(--good)"}`,
              }}
            />
            {error ? "engine offline" : "engine ready"}
          </div>
        </header>

        <div className="flex flex-1 flex-col items-start gap-6 lg:flex-row lg:gap-8">
          <div className="flex w-full min-w-0 flex-1 gap-3">
            <EvalBar score={evaluation} flipped={flipped} />
            <div
              className="mx-auto w-full"
              style={{ maxWidth: "min(100%, 760px, calc(100dvh - 216px))" }}
            >
              {board ? (
                <Board
                  theme={theme}
                  pieces={pieces}
                  flipped={flipped}
                  selected={selected}
                  partialPath={partialPath}
                  stops={shownStops}
                  captureStops={mustCapture}
                  movableSquares={movableSquares}
                  lastMovePath={lastMovePath}
                  animation={animation}
                  interactive={interactive}
                  onSquareClick={handleSquareClick}
                />
              ) : (
                <div
                  className="board-frame w-full"
                  style={{ background: theme.frame }}
                >
                  <div className="board-inner aspect-square w-full animate-pulse bg-white/5" />
                </div>
              )}
            </div>
          </div>

          <SidePanel
            theme={theme}
            themeId={themeId}
            onThemeChange={(id) => {
              setThemeId(id);
              sounds.play("ui");
            }}
            difficulty={difficulty}
            onDifficultyChange={(value) => {
              setDifficulty(value);
              sounds.play("ui");
            }}
            humanSide={humanSide}
            onSideChange={handleSideChange}
            soundOn={soundOn}
            onToggleSound={() => {
              setSoundOn((on) => !on);
              sounds.enabled = true;
              sounds.play("ui");
            }}
            onFlip={() => {
              setFlipped((value) => !value);
              sounds.play("ui");
            }}
            onNewGame={() => void startGame(humanSide)}
            onUndo={handleUndo}
            onHint={() => void handleHint()}
            canUndo={undoDepth > 0 && !thinking}
            canHint={humanTurn && !thinking}
            thinking={thinking}
            hintPending={hintPending}
            turn={turn}
            material={material}
            evaluation={evaluation}
            search={search}
            history={history}
            mustCapture={mustCapture}
            error={error}
          />
        </div>

        <footer className="pt-2 text-center text-[11px] leading-relaxed text-[var(--text-faint)]">
          <p className="flex flex-wrap items-center justify-center gap-x-2 gap-y-1">
            <span>
              Search engine in Python by{" "}
              <a
                href="https://github.com/Uzcyberguard/checkers_engine"
                target="_blank"
                rel="noreferrer"
                className="font-medium text-[var(--text-dim)] underline decoration-dotted underline-offset-2 transition-colors hover:text-[var(--gold)]"
              >
                Hasan Normamatov
              </a>
            </span>
            {/* the separator only earns its place when both credits share a line */}
            <span aria-hidden className="hidden opacity-40 sm:inline">
              ·
            </span>
            <span>
              Web interface, engine integration and deployment by{" "}
              <span className="font-medium text-[var(--text-dim)]">
                Asadbek Abduxalilov
              </span>
            </span>
          </p>
          <p className="mt-1.5 opacity-75">
            Alpha-beta search with iterative deepening, a transposition table and
            move ordering.
          </p>
        </footer>
      </main>

      <GameOverOverlay
        outcome={overlayDismissed ? null : outcome}
        detail={drawReason ?? undefined}
        onRestart={() => void startGame(humanSide)}
        onReview={() => setOverlayDismissed(true)}
      />
    </div>
  );
}
