import type {
  AiReport,
  Board,
  Difficulty,
  PositionReport,
  Player,
  SearchInfo,
} from "./types";

async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body ?? {}),
  });

  const text = await response.text();
  let payload: unknown;
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(
      `The engine returned something that was not JSON (HTTP ${response.status}).`,
    );
  }

  if (!response.ok) {
    const message =
      typeof payload === "object" && payload && "error" in payload
        ? String((payload as { error: unknown }).error)
        : `Request failed with HTTP ${response.status}`;
    throw new Error(message);
  }

  return payload as T;
}

export function newGame(): Promise<PositionReport> {
  return post<PositionReport>("/api/new", {});
}

export function getState(board: Board, player: Player): Promise<PositionReport> {
  return post<PositionReport>("/api/state", { board, player });
}

export function getAiMove(
  board: Board,
  player: Player,
  difficulty: Difficulty,
  seed?: number,
): Promise<AiReport> {
  return post<AiReport>("/api/ai", { board, player, difficulty, seed });
}

export function getHint(
  board: Board,
  player: Player,
): Promise<{ move: AiReport["move"]; search: SearchInfo; evaluation: number }> {
  return post("/api/analyse", { board, player });
}
