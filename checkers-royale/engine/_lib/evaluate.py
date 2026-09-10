"""
Positional evaluation, in centipawns, always from White's point of view.

Positive means White stands better; the search negates it per side. The
function is exactly antisymmetric: mirroring the board vertically and swapping
colours negates the score (there is a test for this).

Design notes
------------
The original engine's `centralization_weight` was material plus a very flat
advancement term plus king mobility, which is a sound if blunt shape. The terms
here keep that shape and add the two things a search cannot see for itself:

  * back-rank integrity, which is what stops a side from cheerfully shoving
    every man up the board and handing the opponent a promotion lane, and
  * support structure, because a man backed up on its diagonal is far harder
    to win material against.

Deliberately absent: any penalty for a man blocked by its *own* pieces. That
reads as "trapped" but is really just a normal, healthy phalanx, and paying to
dissolve it is how an engine talks itself into a losing advance.
"""

from typing import Sequence

from .rules import DIRECTIONS, SIZE, in_bounds

MAN_VALUE = 100
KING_VALUE = 300

# Value a man gains as it nears promotion, indexed by rows still to travel.
ADVANCEMENT = (0, 14, 8, 5, 3, 2, 1, 0)

# Mild preference for the middle files; the rim is safe but passive, so it is
# scored as neutral rather than punished.
FILE_BONUS = (0, 2, 4, 5, 5, 4, 2, 0)

BACK_RANK_BONUS = 11
SUPPORT_BONUS = 5
KING_MOBILITY = 2
KING_MOBILITY_CAP = 10
KING_TRAPPED = 30
ENDGAME_TRADE_BONUS = 14
ENDGAME_PIECES = 8

Board = Sequence[Sequence[int]]


def _king_mobility(board: Board, row: int, col: int) -> int:
    squares = 0
    for d_row, d_col in DIRECTIONS:
        step = 1
        while True:
            scan_row, scan_col = row + step * d_row, col + step * d_col
            if not in_bounds(scan_row, scan_col) or board[scan_row][scan_col] != 0:
                break
            squares += 1
            step += 1
    return squares


def _support(board: Board, row: int, col: int, player: int) -> int:
    """Friendly pieces diagonally behind a man, which make it hard to attack."""
    behind = 1 if player == 1 else -1
    found = 0
    for d_col in (-1, 1):
        scan_row, scan_col = row + behind, col + d_col
        if not in_bounds(scan_row, scan_col):
            # The rim counts as support: nothing can come from off the board.
            found += 1
        elif board[scan_row][scan_col] * player > 0:
            found += 1
    return found


def evaluate(board: Board) -> int:
    score = 0
    white_pieces = black_pieces = 0

    for row in range(SIZE):
        for col in range(SIZE):
            piece = board[row][col]
            if piece == 0:
                continue

            if piece == 1:
                white_pieces += 1
                score += MAN_VALUE + ADVANCEMENT[row] + FILE_BONUS[col]
                if row == SIZE - 1:
                    score += BACK_RANK_BONUS
                score += SUPPORT_BONUS * _support(board, row, col, 1)

            elif piece == -1:
                black_pieces += 1
                score -= MAN_VALUE + ADVANCEMENT[SIZE - 1 - row] + FILE_BONUS[col]
                if row == 0:
                    score -= BACK_RANK_BONUS
                score -= SUPPORT_BONUS * _support(board, row, col, -1)

            elif piece == 3:
                white_pieces += 1
                mobility = _king_mobility(board, row, col)
                score += KING_VALUE + KING_MOBILITY * min(mobility, KING_MOBILITY_CAP)
                if mobility == 0:
                    score -= KING_TRAPPED

            elif piece == -3:
                black_pieces += 1
                mobility = _king_mobility(board, row, col)
                score -= KING_VALUE + KING_MOBILITY * min(mobility, KING_MOBILITY_CAP)
                if mobility == 0:
                    score += KING_TRAPPED

    # With few pieces left, the side that is ahead wants to keep trading down.
    if white_pieces + black_pieces <= ENDGAME_PIECES and white_pieces != black_pieces:
        lead = white_pieces - black_pieces
        score += ENDGAME_TRADE_BONUS * lead

    return score


def material_balance(board: Board) -> int:
    total = 0
    for row in board:
        for piece in row:
            if piece == 1:
                total += MAN_VALUE
            elif piece == -1:
                total -= MAN_VALUE
            elif piece == 3:
                total += KING_VALUE
            elif piece == -3:
                total -= KING_VALUE
    return total


def piece_count(board: Board) -> int:
    return sum(1 for row in board for piece in row if piece != 0)
