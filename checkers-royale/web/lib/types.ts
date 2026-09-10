export type Piece = 0 | 1 | -1 | 3 | -3;
export type Board = Piece[][];
export type Player = 1 | -1;
export type Square = [number, number];

export type Difficulty = "beginner" | "easy" | "normal" | "hard" | "master";

export interface ApiMove {
  path: Square[];
  board: Board;
  captured: Square[];
  promoted: boolean;
  wasMan: boolean;
  notation: string;
}

export interface Material {
  whiteMen: number;
  whiteKings: number;
  blackMen: number;
  blackKings: number;
}

export type Status = "playing" | "white_wins" | "black_wins";

export interface SearchInfo {
  depth: number;
  nodes: number;
  elapsedMs: number;
  score: number;
  ttHits?: number;
  difficulty?: string;
}

export interface PositionReport {
  board: Board;
  player: Player;
  moves: ApiMove[];
  mustCapture: boolean;
  status: Status;
  material: Material;
  evaluation: number;
}

export interface AiReport extends PositionReport {
  move: ApiMove | null;
  search: SearchInfo;
}

/** A rendered piece keeps a stable identity so it can animate between squares. */
export interface PieceView {
  id: number;
  row: number;
  col: number;
  player: Player;
  king: boolean;
}

export interface HistoryEntry {
  notation: string;
  player: Player;
  captured: number;
  promoted: boolean;
  board: Board;
  evaluation: number;
}

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  beginner: "Beginner",
  easy: "Easy",
  normal: "Normal",
  hard: "Hard",
  master: "Master",
};

export const DIFFICULTY_BLURB: Record<Difficulty, string> = {
  beginner: "Looks two moves ahead and often wanders off.",
  easy: "Four moves deep, with the odd slip.",
  normal: "A solid club opponent. No deliberate mistakes.",
  hard: "Nearly two seconds of search. Punishes loose play.",
  master: "Four seconds a move, full depth. Good luck.",
};
