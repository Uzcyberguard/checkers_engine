"""
Russian draughts (shashki) rules engine.

Board encoding (unchanged from the original engine by Hasan Normamatov):
     0 = empty
     1 = white man      3 = white king
    -1 = black man     -3 = black king

Player is 1 (white, moves toward row 0) or -1 (black, moves toward row 7).

Rules implemented:
  * men step one square diagonally forward
  * men capture in all four diagonal directions (forward and backward)
  * kings fly: they slide any distance along a clear diagonal
  * kings capture at range and may land on any empty square beyond the victim
  * captures are mandatory; if any capture exists, only captures are legal
  * a capture sequence must be continued while further captures are available
  * a man that reaches the far rank mid-capture promotes and continues as a king
  * "Turkish strike": captured pieces stay on the board as blockers until the
    whole sequence completes, and may never be jumped twice
"""

from typing import Iterator, List, Optional, Sequence, Tuple

SIZE = 8
DIRECTIONS: Tuple[Tuple[int, int], ...] = ((-1, -1), (-1, 1), (1, -1), (1, 1))

Board = List[List[int]]
Square = Tuple[int, int]

MAN = 1
KING = 3


class Move:
    """One complete legal move, including a full multi-capture sequence."""

    __slots__ = ("path", "board", "captured", "promoted", "was_man", "uid")

    def __init__(
        self,
        path: List[Square],
        board: Board,
        captured: List[Square],
        promoted: bool,
        was_man: bool,
    ) -> None:
        self.path = path
        self.board = board
        self.captured = captured
        self.promoted = promoted
        self.was_man = was_man
        # Cheap exact identity, used for move ordering, killers and history.
        # Building this once beats re-deriving algebraic notation in the
        # sort key of every node in the tree.
        self.uid = tuple(path)

    @property
    def origin(self) -> Square:
        return self.path[0]

    @property
    def destination(self) -> Square:
        return self.path[-1]

    def to_dict(self) -> dict:
        return {
            "path": [list(sq) for sq in self.path],
            "board": self.board,
            "captured": [list(sq) for sq in self.captured],
            "promoted": self.promoted,
            "wasMan": self.was_man,
            "notation": self.notation,
        }

    @property
    def notation(self) -> str:
        """Algebraic notation: c3-d4 for a step, c3:e5:c7 for a capture."""
        sep = ":" if self.captured else "-"
        return sep.join(square_name(sq) for sq in self.path)


def square_name(square: Square) -> str:
    row, col = square
    return "{}{}".format("abcdefgh"[col], SIZE - row)


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < SIZE and 0 <= col < SIZE


def copy_board(board: Sequence[Sequence[int]]) -> Board:
    return [list(row) for row in board]


def is_king(piece: int) -> bool:
    return piece == KING or piece == -KING


def owner(piece: int) -> int:
    """+1 for a white piece, -1 for a black piece, 0 for an empty square."""
    if piece > 0:
        return 1
    if piece < 0:
        return -1
    return 0


def promotion_row(player: int) -> int:
    return 0 if player == 1 else SIZE - 1


# ---------------------------------------------------------------------------
# capture generation
# ---------------------------------------------------------------------------


def _man_capture_targets(
    board: Board, row: int, col: int, player: int, captured: List[Square]
) -> Iterator[Tuple[Square, Square]]:
    """Yield (victim, landing) pairs for a man standing on (row, col)."""
    for d_row, d_col in DIRECTIONS:
        victim_row, victim_col = row + d_row, col + d_col
        land_row, land_col = row + 2 * d_row, col + 2 * d_col
        if not in_bounds(land_row, land_col):
            continue
        victim = board[victim_row][victim_col]
        if owner(victim) != -player:
            continue
        if (victim_row, victim_col) in captured:
            continue
        if board[land_row][land_col] != 0:
            continue
        yield (victim_row, victim_col), (land_row, land_col)


def _king_capture_targets(
    board: Board, row: int, col: int, player: int, captured: List[Square]
) -> Iterator[Tuple[Square, Square]]:
    """Yield (victim, landing) pairs for a flying king on (row, col)."""
    for d_row, d_col in DIRECTIONS:
        step = 1
        while True:
            scan_row, scan_col = row + step * d_row, col + step * d_col
            if not in_bounds(scan_row, scan_col) or board[scan_row][scan_col] != 0:
                break
            step += 1

        scan_row, scan_col = row + step * d_row, col + step * d_col
        if not in_bounds(scan_row, scan_col):
            continue
        victim = board[scan_row][scan_col]
        # A friendly piece, or one already captured in this sequence, blocks.
        if owner(victim) != -player or (scan_row, scan_col) in captured:
            continue

        landing = step + 1
        while True:
            land_row, land_col = row + landing * d_row, col + landing * d_col
            if not in_bounds(land_row, land_col) or board[land_row][land_col] != 0:
                break
            yield (scan_row, scan_col), (land_row, land_col)
            landing += 1


def _capture_targets(
    board: Board, row: int, col: int, player: int, captured: List[Square]
) -> Iterator[Tuple[Square, Square]]:
    if is_king(board[row][col]):
        return _king_capture_targets(board, row, col, player, captured)
    return _man_capture_targets(board, row, col, player, captured)


def _extend_captures(
    board: Board,
    row: int,
    col: int,
    player: int,
    captured: List[Square],
    path: List[Square],
    out: List[Move],
    was_man: bool,
) -> None:
    """Depth-first walk of every maximal capture sequence from (row, col)."""
    piece = board[row][col]
    found_continuation = False

    for victim, landing in list(
        _capture_targets(board, row, col, player, captured)
    ):
        found_continuation = True
        land_row, land_col = landing

        moved = piece
        if not is_king(piece) and land_row == promotion_row(player):
            moved = KING * player

        board[row][col] = 0
        board[land_row][land_col] = moved
        captured.append(victim)
        path.append(landing)

        _extend_captures(
            board, land_row, land_col, player, captured, path, out, was_man
        )

        path.pop()
        captured.pop()
        board[land_row][land_col] = 0
        board[row][col] = piece

    if not found_continuation and captured:
        final = copy_board(board)
        for victim_row, victim_col in captured:
            final[victim_row][victim_col] = 0
        final[path[0][0]][path[0][1]] = 0
        final[row][col] = piece
        promoted = was_man and is_king(piece)
        out.append(Move(list(path), final, list(captured), promoted, was_man))


def captures_for_piece(board: Board, row: int, col: int, player: int) -> List[Move]:
    piece = board[row][col]
    if owner(piece) != player:
        return []
    out: List[Move] = []
    working = copy_board(board)
    _extend_captures(
        working, row, col, player, [], [(row, col)], out, not is_king(piece)
    )
    return out


def has_capture(board: Board, row: int, col: int, player: int) -> bool:
    for _ in _capture_targets(board, row, col, player, []):
        return True
    return False


# ---------------------------------------------------------------------------
# quiet move generation
# ---------------------------------------------------------------------------


def quiet_moves_for_piece(board: Board, row: int, col: int, player: int) -> List[Move]:
    piece = board[row][col]
    if owner(piece) != player:
        return []

    out: List[Move] = []
    if is_king(piece):
        for d_row, d_col in DIRECTIONS:
            step = 1
            while True:
                land_row, land_col = row + step * d_row, col + step * d_col
                if not in_bounds(land_row, land_col) or board[land_row][land_col] != 0:
                    break
                new_board = copy_board(board)
                new_board[row][col] = 0
                new_board[land_row][land_col] = piece
                out.append(
                    Move(
                        [(row, col), (land_row, land_col)], new_board, [], False, False
                    )
                )
                step += 1
        return out

    forward = -1 if player == 1 else 1
    for d_col in (-1, 1):
        land_row, land_col = row + forward, col + d_col
        if not in_bounds(land_row, land_col) or board[land_row][land_col] != 0:
            continue
        new_board = copy_board(board)
        new_board[row][col] = 0
        promoted = land_row == promotion_row(player)
        new_board[land_row][land_col] = KING * player if promoted else piece
        out.append(
            Move([(row, col), (land_row, land_col)], new_board, [], promoted, True)
        )
    return out


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------


def legal_moves(board: Board, player: int) -> List[Move]:
    """All legal moves for `player`. Captures are mandatory when available.

    Two passes on purpose: find which pieces can capture at all before running
    the (allocating) capture search, so a quiet position never pays for a
    single board copy.
    """
    origins: List[Square] = []
    capturing: List[Square] = []

    for row in range(SIZE):
        row_values = board[row]
        for col in range(SIZE):
            if owner(row_values[col]) != player:
                continue
            origins.append((row, col))
            if has_capture(board, row, col, player):
                capturing.append((row, col))

    if capturing:
        captures: List[Move] = []
        for row, col in capturing:
            captures.extend(captures_for_piece(board, row, col, player))
        return captures

    quiet: List[Move] = []
    for row, col in origins:
        quiet.extend(quiet_moves_for_piece(board, row, col, player))
    return quiet


def board_key(board: Sequence[Sequence[int]], player: int) -> Tuple:
    return (tuple(map(tuple, board)), player)


def count_material(board: Sequence[Sequence[int]]) -> dict:
    counts = {"whiteMen": 0, "whiteKings": 0, "blackMen": 0, "blackKings": 0}
    for row in board:
        for value in row:
            if value == 1:
                counts["whiteMen"] += 1
            elif value == 3:
                counts["whiteKings"] += 1
            elif value == -1:
                counts["blackMen"] += 1
            elif value == -3:
                counts["blackKings"] += 1
    return counts


def starting_board() -> Board:
    board = [[0] * SIZE for _ in range(SIZE)]
    for row in range(3):
        for col in range(SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = -1
    for row in range(5, SIZE):
        for col in range(SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = 1
    return board


def validate_board(raw) -> Optional[str]:
    if not isinstance(raw, list) or len(raw) != SIZE:
        return "board must be an 8x8 array"
    for row in raw:
        if not isinstance(row, list) or len(row) != SIZE:
            return "board must be an 8x8 array"
        for value in row:
            if value not in (0, 1, -1, 3, -3):
                return "board contains an invalid piece value: {!r}".format(value)
    return None
