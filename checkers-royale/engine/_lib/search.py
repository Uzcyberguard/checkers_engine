"""
Alpha-beta search with iterative deepening, a transposition table, move
ordering and a hard time budget.

Improvements over the original `minimax_funktion` / `engine`:

  * the root shares one alpha window across sibling moves, so root pruning
    actually happens (the original passed a fresh -inf/+inf per root move and
    therefore threw away nearly all of its cutoffs)
  * iterative deepening, so the engine can be given a time budget instead of a
    fixed depth - essential when running as a serverless function
  * a transposition table, which matters a lot in draughts where move orders
    transpose constantly
  * move ordering: transposition-table move first, then captures by size, then
    killer moves and a history heuristic
  * capture extensions, so the search is never cut off in the middle of a
    forced exchange
  * randomised tie-breaking, so the engine does not replay an identical game
    every time (the original always kept the first of several equal moves)
"""

import random
import time
from typing import Dict, List, Optional, Sequence, Tuple

from .evaluate import evaluate, piece_count
from .rules import Move, board_key, legal_moves

MATE = 1_000_000
MAX_PLY = 64

EXACT, LOWER, UPPER = 0, 1, 2


class SearchTimeout(Exception):
    pass


class SearchStats:
    __slots__ = ("nodes", "depth", "elapsed", "score", "tt_hits", "pv")

    def __init__(self) -> None:
        self.nodes = 0
        self.depth = 0
        self.elapsed = 0.0
        self.score = 0
        self.tt_hits = 0
        self.pv: List[str] = []


class Engine:
    """A stateless-per-call search. Build one, call `best_move`, throw it away."""

    def __init__(self, time_budget: float = 1.5, max_depth: int = 24,
                 randomness: int = 0, seed: Optional[int] = None) -> None:
        self.time_budget = time_budget
        self.max_depth = max_depth
        # Root moves within `randomness` centipawns of the best are considered
        # equally good and one is picked at random.
        self.randomness = randomness
        self.rng = random.Random(seed)
        self.tt: Dict[Tuple, Tuple[int, int, int, Optional[str]]] = {}
        self.killers: List[List[Optional[str]]] = [[None, None] for _ in range(MAX_PLY)]
        self.history: Dict[str, int] = {}
        self.stats = SearchStats()
        self._deadline = 0.0

    # -- helpers ---------------------------------------------------------

    def _check_time(self) -> None:
        if time.monotonic() > self._deadline:
            raise SearchTimeout()

    def _order(self, moves: List[Move], ply: int, tt_move) -> List[Move]:
        if len(moves) < 2:
            return moves

        killers = self.killers[ply] if ply < MAX_PLY else (None, None)
        killer_a, killer_b = killers[0], killers[1]
        history = self.history

        def score(move: Move) -> int:
            uid = move.uid
            if uid == tt_move:
                return 1_000_000
            if move.captured:
                # Bigger captures first; a capture that crowns is better still.
                return 500_000 + 1000 * len(move.captured) + (200 if move.promoted else 0)
            if uid == killer_a:
                return 400_000
            if uid == killer_b:
                return 390_000
            if move.promoted:
                return 300_000
            return history.get(uid, 0)

        return sorted(moves, key=score, reverse=True)

    def _store_killer(self, move: Move, ply: int) -> None:
        if move.captured or ply >= MAX_PLY:
            return
        slot = self.killers[ply]
        if slot[0] != move.uid:
            slot[1] = slot[0]
            slot[0] = move.uid

    # -- search ----------------------------------------------------------

    def _negamax(
        self,
        board: Sequence[Sequence[int]],
        player: int,
        depth: int,
        alpha: int,
        beta: int,
        ply: int,
        extensions: int,
    ) -> int:
        self.stats.nodes += 1
        if (self.stats.nodes & 1023) == 0:
            self._check_time()

        alpha_origin = alpha
        key = board_key(board, player)
        entry = self.tt.get(key)
        tt_move: Optional[str] = None
        if entry is not None:
            stored_depth, stored_score, flag, stored_move = entry
            tt_move = stored_move
            if stored_depth >= depth:
                self.stats.tt_hits += 1
                if flag == EXACT:
                    return stored_score
                if flag == LOWER and stored_score > alpha:
                    alpha = stored_score
                elif flag == UPPER and stored_score < beta:
                    beta = stored_score
                if alpha >= beta:
                    return stored_score

        moves = legal_moves(board, player)
        if not moves:
            # No legal move: the side to move has lost. Prefer quicker mates.
            return -MATE + ply

        # Stand on a forced capture rather than evaluating mid-exchange.
        if depth <= 0:
            if moves[0].captured and extensions > 0:
                depth = 1
                extensions -= 1
            else:
                return player * evaluate(board)

        best_score = -MATE * 2
        best_move = None

        for move in self._order(moves, ply, tt_move):
            score = -self._negamax(
                move.board, -player, depth - 1, -beta, -alpha, ply + 1, extensions
            )
            if score > best_score:
                best_score = score
                best_move = move.uid
            if score > alpha:
                alpha = score
            if alpha >= beta:
                self._store_killer(move, ply)
                uid = move.uid
                self.history[uid] = self.history.get(uid, 0) + depth * depth
                break

        if best_score <= alpha_origin:
            flag = UPPER
        elif best_score >= beta:
            flag = LOWER
        else:
            flag = EXACT
        self.tt[key] = (depth, best_score, flag, best_move)
        return best_score

    def _search_root(
        self, board: Sequence[Sequence[int]], player: int, moves: List[Move], depth: int
    ) -> List[Tuple[int, Move]]:
        alpha = -MATE * 2
        beta = MATE * 2
        scored: List[Tuple[int, Move]] = []

        entry = self.tt.get(board_key(board, player))
        tt_move = entry[3] if entry else None

        for move in self._order(moves, 0, tt_move):
            score = -self._negamax(
                move.board, -player, depth - 1, -beta, -alpha, 1, 6
            )
            scored.append((score, move))
            if score > alpha:
                alpha = score

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return scored

    def best_move(
        self, board: Sequence[Sequence[int]], player: int
    ) -> Tuple[Optional[Move], SearchStats]:
        started = time.monotonic()
        self._deadline = started + self.time_budget
        self.stats = SearchStats()

        moves = legal_moves(board, player)
        if not moves:
            self.stats.elapsed = time.monotonic() - started
            return None, self.stats

        if len(moves) == 1:
            self.stats.elapsed = time.monotonic() - started
            self.stats.depth = 1
            self.stats.score = 0
            return moves[0], self.stats

        # Endgames are cheap, so let the engine push deeper there.
        remaining = piece_count(board)
        depth_cap = self.max_depth if remaining > 8 else min(self.max_depth, 30)

        best_ordering: List[Tuple[int, Move]] = [(0, move) for move in moves]
        completed_depth = 0
        best_score = 0

        for depth in range(1, depth_cap + 1):
            try:
                ordered = self._search_root(
                    board, player, [pair[1] for pair in best_ordering], depth
                )
            except SearchTimeout:
                break

            best_ordering = ordered
            completed_depth = depth
            best_score = ordered[0][0]

            # A forced win or loss is found; no point searching deeper.
            if abs(best_score) > MATE - MAX_PLY:
                break
            if time.monotonic() > self._deadline:
                break

        top = best_ordering[0][0]
        pool = [
            move
            for score, move in best_ordering
            if score >= top - self.randomness
        ] or [best_ordering[0][1]]
        chosen = self.rng.choice(pool)

        self.stats.elapsed = time.monotonic() - started
        self.stats.depth = completed_depth
        self.stats.score = best_score
        self.stats.pv = [move.notation for _, move in best_ordering[:5]]
        return chosen, self.stats


DIFFICULTY = {
    "beginner": {"time": 0.05, "depth": 2, "randomness": 140, "blunder": 0.30},
    "easy": {"time": 0.15, "depth": 4, "randomness": 70, "blunder": 0.12},
    "normal": {"time": 0.60, "depth": 8, "randomness": 25, "blunder": 0.0},
    "hard": {"time": 1.80, "depth": 14, "randomness": 0, "blunder": 0.0},
    "master": {"time": 4.00, "depth": 24, "randomness": 0, "blunder": 0.0},
}


def choose_move(
    board: Sequence[Sequence[int]],
    player: int,
    difficulty: str = "normal",
    seed: Optional[int] = None,
    time_budget: Optional[float] = None,
) -> Tuple[Optional[Move], SearchStats, str]:
    """Pick a move at the requested strength.

    Weak levels deliberately mix in a sub-optimal choice sometimes, which makes
    them feel human rather than merely shallow.
    """
    level = DIFFICULTY.get(difficulty, DIFFICULTY["normal"])
    engine = Engine(
        time_budget=time_budget if time_budget is not None else level["time"],
        max_depth=level["depth"],
        randomness=level["randomness"],
        seed=seed,
    )
    move, stats = engine.best_move(board, player)

    if move is not None and level["blunder"] > 0:
        rng = random.Random(seed)
        if rng.random() < level["blunder"]:
            options = legal_moves(board, player)
            if len(options) > 1:
                move = rng.choice(options)

    return move, stats, difficulty
