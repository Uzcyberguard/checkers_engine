"""
Engine tests. Run from the project root:

    python -m pytest tests/test_engine.py -q      # if pytest is installed
    python tests/test_engine.py                   # or standalone

The perft numbers are the published move-tree counts for Russian draughts from
the initial position. They are the single most valuable check here: they catch
rules bugs that reading the code will not.
"""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))

from _lib import rules  # noqa: E402
from _lib.evaluate import evaluate  # noqa: E402
from _lib.search import Engine, choose_move  # noqa: E402

PERFT = [7, 49, 302, 1469, 7482, 37986]


def perft(board, player, depth):
    moves = rules.legal_moves(board, player)
    if depth == 1:
        return len(moves)
    return sum(perft(m.board, -player, depth - 1) for m in moves)


def test_perft_matches_published_counts():
    start = rules.starting_board()
    for depth, expected in enumerate(PERFT, start=1):
        assert perft(start, 1, depth) == expected, f"perft({depth}) mismatch"


def test_evaluation_is_antisymmetric():
    """Mirroring the board and swapping colours must negate the score."""
    rng = random.Random(11)
    for _ in range(2000):
        board = [[0] * 8 for _ in range(8)]
        for _ in range(rng.randint(2, 14)):
            row, col = rng.randrange(8), rng.randrange(8)
            if (row + col) % 2 == 0:
                continue
            value = rng.choice([1, -1, 3, -3])
            if (value == 1 and row == 0) or (value == -1 and row == 7):
                continue
            board[row][col] = value
        mirrored = [[-board[7 - r][c] for c in range(8)] for r in range(8)]
        assert evaluate(board) == -evaluate(mirrored)


def test_start_position_is_balanced():
    assert evaluate(rules.starting_board()) == 0


def test_captures_are_compulsory():
    board = [[0] * 8 for _ in range(8)]
    board[5][2] = 1
    board[4][3] = -1
    board[7][0] = 1  # a quiet move exists, but must not be offered
    moves = rules.legal_moves(board, 1)
    assert all(m.captured for m in moves), "a quiet move was offered alongside a capture"


def test_man_promotes_mid_capture_and_continues_as_king():
    board = [[0] * 8 for _ in range(8)]
    board[2][1] = 1   # white man, one jump from the crowning row
    board[1][2] = -1
    board[1][4] = -1
    moves = rules.legal_moves(board, 1)
    assert moves, "expected a capture"
    for move in moves:
        end_row, end_col = move.path[-1]
        assert move.board[end_row][end_col] == 3, "should have crowned"
        assert move.promoted
        assert len(move.captured) == 2, "must keep capturing as a king"


def test_flying_king_captures_at_range():
    board = [[0] * 8 for _ in range(8)]
    board[7][0] = 3   # white king on a1
    board[5][2] = -1  # black man on c3
    moves = rules.legal_moves(board, 1)
    assert moves
    landings = {tuple(m.path[-1]) for m in moves}
    assert len(landings) >= 3, "a king may stop on any empty square beyond its victim"
    assert all(len(m.captured) == 1 for m in moves)


def test_turkish_strike_piece_is_not_jumped_twice():
    """A captured piece stays on the board as a blocker until the move ends."""
    board = [[0] * 8 for _ in range(8)]
    board[7][0] = 3
    board[5][2] = -1
    for move in rules.legal_moves(board, 1):
        squares = [tuple(sq) for sq in move.captured]
        assert len(squares) == len(set(squares)), "a piece was captured twice"


def test_no_legal_moves_is_a_loss_for_the_side_to_move():
    board = [[0] * 8 for _ in range(8)]
    board[0][1] = -1  # black man on b8
    board[1][0] = 1   # a7 blocks one step; jumping it would land off the board
    board[1][2] = 1   # c7 blocks the other step...
    board[2][3] = 1   # ...and d6 denies the jump over it
    assert rules.legal_moves(board, -1) == []


def test_search_finds_the_only_move_instantly():
    board = [[0] * 8 for _ in range(8)]
    board[5][2] = 1
    board[4][3] = -1
    board[2][3] = -1
    move, stats = Engine(time_budget=1.0).best_move(board, 1)
    assert move is not None
    assert len(move.captured) == 2
    assert move.notation == "c3:e5:c7"


def test_deeper_budget_reaches_deeper():
    start = rules.starting_board()
    _, shallow = Engine(time_budget=0.05, max_depth=24).best_move(start, 1)
    _, deep = Engine(time_budget=1.2, max_depth=24).best_move(start, 1)
    assert deep.depth > shallow.depth


def test_difficulty_levels_all_return_a_legal_move():
    start = rules.starting_board()
    legal = {m.notation for m in rules.legal_moves(start, 1)}
    for level in ("beginner", "easy", "normal", "hard", "master"):
        move, _, _ = choose_move(start, 1, level, seed=5)
        assert move is not None and move.notation in legal, level


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {test.__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
