""" Created on Mon Jun  8 15:54:51 2026 Hasan Normamatov """
from move_funksion import Move
from evaluate_funksion import Evaluate
from minimax_funktion import Minimax


import time
t = time.time()
PIECE = 1
BOARD = [
    [ 0,-1, 0, 0, 0, 0, 0, 0], # 0
    [-1, 0,-1, 0, 0, 0, 0, 1], # 1
    [ 0, 0, 0, 0, 0,-1, 0, 0], # 2
    [ 0, 0, 1, 0, 0, 0, 0, 0], # 3
    [ 0, 0, 0, 0, 0, 0, 0, 0], # 4
    [ 0, 0, 0, 0, 0, 0,-1, 0], # 5
    [ 0, 0, 0, 0, 0, 0, 0,-1], # 6
    [ 0, 0, 0, 0, 1, 0, 1, 0]  # 7
  #   0  1  2  3  4  5  6  7
]


move = Move()
evaluate = Evaluate()
minimax = Minimax()





def best_move(board, player, depth):

    moves = move.legal_moves(player, board)

    best_score = -float("inf")
    best_path = None

    for new_board, path in moves:

        score = minimax.minimax(
            new_board,
            depth-1,
            -float("inf"),
            float("inf"),
            -player
        )
        print(path,score)
        if score > best_score:
            best_score = score
            best_path = path

    return best_path


print(best_move(BOARD,1,1))
print(t - time.time())


