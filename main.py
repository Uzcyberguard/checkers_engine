""" Created on Mon Jun  8 15:54:51 2026 Hasan Normamatov """
from move_funksion import Move
from evaluate_funksion import Evaluate
import time
t = time.time()
PIECE = 1
BOARD = [
    [ 0,-1, 0,-1, 0,-1, 0,-1], # 0
    [-1, 0,-1, 0,-1, 0,-1, 0], # 1
    [ 0, 0, 0,-1, 0,-1, 0,-1], # 2
    [-1, 0, 0, 0, 0, 0, 0, 0], # 3
    [ 0, 0, 0, 0, 0, 0, 0, 0], # 4
    [ 1, 0, 1, 0, 1, 0, 1, 0], # 5
    [ 0, 1, 0, 1, 0, 1, 0, 1], # 6
    [ 1, 0, 1, 0, 1, 0, 1, 0]  # 7
  #   0  1  2  3  4  5  6  7
]
FIRST_MOVES = []
SECOND_MOVES = []
THIRD_MOVES = []
FOURTH_MOVES = []
FIFTH_MOVES = []

move = Move()
evaluate = Evaluate()



def evaluate(board):
    FIRST_MOVES = []
    SECOND_MOVES = []
    THIRD_MOVES = []
    # FOURTH_MOVES=[]
    # FIFTH_MOVES=[]

    starting = move.legal_moves(1, board, [])

    for depth in starting:
        FIRST_MOVES.extend(move.legal_moves(-1, depth[0], depth[1]))

    for depth2 in FIRST_MOVES:
        for depth3 in move.legal_moves(1, depth2[0], depth2[1]):
            SECOND_MOVES.extend(move.legal_moves(-1, depth3[0], depth3[1]))

    for depth4 in SECOND_MOVES:
        for depth5 in move.legal_moves(1, depth4[0], depth4[1]):
            THIRD_MOVES.extend(move.legal_moves(-1, depth5[0], depth5[1]))
    for depth6 in THIRD_MOVES:
        for depth7 in move.legal_moves(1, depth6[0], depth6[1]):
            FOURTH_MOVES.extend(move.legal_moves(-1, depth7[0], depth7[1]))
    # for depth8 in FOURTH_MOVES:
    #     for depth8 in legal_moves(1, depth8[0]):
    #         FIFTH_MOVES.extend(legal_moves(-1, depth8[0]))
    print(len(FOURTH_MOVES))
    path_to_best_move = []
    best_advantage = 0
    for x in FOURTH_MOVES[0][0]:
        best_advantage += sum(x)

    for poss in FOURTH_MOVES:
        eval_bar = 0
        for row in poss[0]:
            eval_bar += sum(row)
        if eval_bar >= best_advantage:
            best_advantage = eval_bar
            path_to_best_move = poss[1]

    return path_to_best_move


def best_move(piece, board):
    pass


print((evaluate(BOARD)))
print(t - time.time())


