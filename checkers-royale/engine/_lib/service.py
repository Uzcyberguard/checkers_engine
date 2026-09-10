"""Request handling shared by the /api endpoints, kept free of any web framework."""

from typing import Any, Dict, List, Optional

from .evaluate import evaluate
from .rules import (
    Move,
    count_material,
    legal_moves,
    starting_board,
    validate_board,
)
from .search import DIFFICULTY, choose_move


class ApiError(Exception):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status = status


def _read_board(payload: Dict[str, Any]):
    raw = payload.get("board")
    if raw is None:
        return starting_board()
    problem = validate_board(raw)
    if problem:
        raise ApiError(problem)
    return [list(row) for row in raw]


def _read_player(payload: Dict[str, Any]) -> int:
    player = payload.get("player", 1)
    if player not in (1, -1):
        raise ApiError("player must be 1 (white) or -1 (black)")
    return player


def _serialise(moves: List[Move]) -> List[dict]:
    return [move.to_dict() for move in moves]


def _status(moves: List[Move], player: int) -> str:
    if moves:
        return "playing"
    # The side to move has no legal reply, so it has lost.
    return "black_wins" if player == 1 else "white_wins"


def _position_report(board, player: int) -> Dict[str, Any]:
    moves = legal_moves(board, player)
    return {
        "board": board,
        "player": player,
        "moves": _serialise(moves),
        "mustCapture": bool(moves and moves[0].captured),
        "status": _status(moves, player),
        "material": count_material(board),
        "evaluation": evaluate(board),
    }


def state(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Legal moves and status for a position."""
    board = _read_board(payload)
    player = _read_player(payload)
    return _position_report(board, player)


def new_game(payload: Dict[str, Any]) -> Dict[str, Any]:
    board = starting_board()
    return _position_report(board, 1)


def ai(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Pick a move for `player`, and report the position the opponent then faces."""
    board = _read_board(payload)
    player = _read_player(payload)

    difficulty = payload.get("difficulty", "normal")
    if difficulty not in DIFFICULTY:
        raise ApiError(
            "difficulty must be one of: {}".format(", ".join(sorted(DIFFICULTY)))
        )

    seed = payload.get("seed")
    if seed is not None and not isinstance(seed, int):
        raise ApiError("seed must be an integer")

    budget: Optional[float] = None
    raw_budget = payload.get("timeBudget")
    if raw_budget is not None:
        try:
            budget = max(0.02, min(float(raw_budget), 8.0))
        except (TypeError, ValueError):
            raise ApiError("timeBudget must be a number of seconds")

    move, stats, level = choose_move(board, player, difficulty, seed, budget)

    if move is None:
        return {
            "move": None,
            "status": _status([], player),
            "board": board,
            "material": count_material(board),
            "evaluation": evaluate(board),
            "search": {
                "depth": 0,
                "nodes": 0,
                "elapsedMs": round(stats.elapsed * 1000),
                "score": 0,
                "difficulty": level,
            },
        }

    after = _position_report(move.board, -player)
    after["move"] = move.to_dict()
    after["search"] = {
        "depth": stats.depth,
        "nodes": stats.nodes,
        "elapsedMs": round(stats.elapsed * 1000),
        "score": stats.score,
        "ttHits": stats.tt_hits,
        "difficulty": level,
    }
    return after


def analyse(payload: Dict[str, Any]) -> Dict[str, Any]:
    """A hint for the human: the engine's preferred move in this position."""
    board = _read_board(payload)
    player = _read_player(payload)
    move, stats, _ = choose_move(board, player, "hard", payload.get("seed"))
    return {
        "move": move.to_dict() if move else None,
        "search": {
            "depth": stats.depth,
            "nodes": stats.nodes,
            "elapsedMs": round(stats.elapsed * 1000),
            "score": stats.score,
        },
        "evaluation": evaluate(board),
    }


ROUTES = {
    "state": state,
    "new": new_game,
    "ai": ai,
    "analyse": analyse,
}
