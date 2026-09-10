import type {
  ApiMove,
  Board,
  HistoryEntry,
  PieceView,
  Player,
  Square,
} from "./types";

let nextPieceId = 1;

export function piecesFromBoard(board: Board): PieceView[] {
  const pieces: PieceView[] = [];
  for (let row = 0; row < 8; row += 1) {
    for (let col = 0; col < 8; col += 1) {
      const value = board[row][col];
      if (value === 0) continue;
      pieces.push({
        id: nextPieceId++,
        row,
        col,
        player: value > 0 ? 1 : -1,
        king: value === 3 || value === -3,
      });
    }
  }
  return pieces;
}

/**
 * Move the piece rather than rebuilding the list, so every disc keeps its
 * React key and animates from where it actually was.
 */
export function applyMoveToPieces(
  pieces: PieceView[],
  move: ApiMove,
): PieceView[] {
  const [fromRow, fromCol] = move.path[0];
  const [toRow, toCol] = move.path[move.path.length - 1];
  const taken = new Set(move.captured.map(([r, c]) => `${r},${c}`));

  return pieces
    .filter((piece) => !taken.has(`${piece.row},${piece.col}`))
    .map((piece) => {
      if (piece.row !== fromRow || piece.col !== fromCol) return piece;
      return {
        ...piece,
        row: toRow,
        col: toCol,
        king: piece.king || move.promoted,
      };
    });
}

export function sameSquare(a: Square, b: Square): boolean {
  return a[0] === b[0] && a[1] === b[1];
}

export function movesFromSquare(moves: ApiMove[], square: Square): ApiMove[] {
  return moves.filter((move) => sameSquare(move.path[0], square));
}

/** Squares the piece may step to next, given the jumps already chosen. */
export function nextStops(moves: ApiMove[], partial: Square[]): Square[] {
  const stops: Square[] = [];
  const seen = new Set<string>();
  for (const move of moves) {
    if (move.path.length <= partial.length) continue;
    let matches = true;
    for (let i = 0; i < partial.length; i += 1) {
      if (!sameSquare(move.path[i], partial[i])) {
        matches = false;
        break;
      }
    }
    if (!matches) continue;
    const stop = move.path[partial.length];
    const key = `${stop[0]},${stop[1]}`;
    if (!seen.has(key)) {
      seen.add(key);
      stops.push(stop);
    }
  }
  return stops;
}

/** The move completed by exactly this path, if any. */
export function completedMove(
  moves: ApiMove[],
  partial: Square[],
): ApiMove | null {
  for (const move of moves) {
    if (move.path.length !== partial.length) continue;
    let matches = true;
    for (let i = 0; i < partial.length; i += 1) {
      if (!sameSquare(move.path[i], partial[i])) {
        matches = false;
        break;
      }
    }
    if (matches) return move;
  }
  return null;
}

export function positionKey(board: Board, player: Player): string {
  return `${board.map((row) => row.join("")).join("|")}#${player}`;
}

export const DRAW_PLY_LIMIT = 30;

export interface DrawState {
  quietPlies: number;
  repetitions: Map<string, number>;
}

export function freshDrawState(): DrawState {
  return { quietPlies: 0, repetitions: new Map() };
}

export function recordPosition(
  state: DrawState,
  board: Board,
  player: Player,
  move: ApiMove | null,
): { state: DrawState; drawReason: string | null } {
  const repetitions = new Map(state.repetitions);
  const key = positionKey(board, player);
  const count = (repetitions.get(key) ?? 0) + 1;
  repetitions.set(key, count);

  // Only king moves with no capture count toward the quiet-move limit.
  const quiet = move && move.captured.length === 0 && !move.wasMan;
  const quietPlies = quiet ? state.quietPlies + 1 : 0;

  let drawReason: string | null = null;
  if (count >= 3) drawReason = "Threefold repetition";
  else if (quietPlies >= DRAW_PLY_LIMIT) {
    drawReason = `${DRAW_PLY_LIMIT / 2} moves by kings with nothing taken`;
  }

  return { state: { quietPlies, repetitions }, drawReason };
}

export function squareName([row, col]: Square): string {
  return `${"abcdefgh"[col]}${8 - row}`;
}

export function historyPairs(history: HistoryEntry[]) {
  const rows: { index: number; white?: HistoryEntry; black?: HistoryEntry }[] = [];
  history.forEach((entry) => {
    if (entry.player === 1) {
      rows.push({ index: rows.length + 1, white: entry });
    } else if (rows.length && rows[rows.length - 1].black === undefined) {
      rows[rows.length - 1].black = entry;
    } else {
      rows.push({ index: rows.length + 1, black: entry });
    }
  });
  return rows;
}
