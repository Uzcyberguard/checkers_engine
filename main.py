""" Created on Mon Jun  8 15:54:51 2026 Hasan Normamatov """
from move_funksion import Move
from evaluate_funksion import Evaluate
from minimax_funktion import Minimax


import time
t = time.time()
DEPTH = 12
PLAYER = 1
BOARD = [
    [ 0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [ 0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [ 0,-1, 0, 0, 0, 0, 0, 0],  # 2
    [ 0, 0, 0, 0, 0, 0,-1, 0],  # 3
    [ 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [ 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [ 0, 3, 0, 0, 0, 0, 0, 0],  # 6
    [ 0, 0, 0, 0, 0, 0, 0, 0]   # 7
  #   0  1  2  3  4  5  6  7
]


move = Move()
evaluate = Evaluate()
minimax = Minimax()





def best_move(board, player, depth):

    moves = move.legal_moves(player, board)

    if player == 1:
        best_score = -float("inf")
    else:
        best_score = float("inf")

    best_path = None

    for new_board, path in moves:

        score = minimax.minimax(
            new_board,
            depth-1,
            -float("inf"),
            float("inf"),
            -player,
            1
        )
        if abs(score) > 950:
            mate_ply = 1000-abs(score)
            mate_moves = (mate_ply+1)//2
            if score>0:
                print(path,f"+M{mate_moves}")
            else:
                print(path,f"-M{mate_moves}")
        else:
            print(path,score)
        if player == 1:
            if score > best_score:
                best_score = score
                best_path = path
        else:
            if score < best_score:
                best_score = score
                best_path = path

    return best_path





print(best_move(BOARD,PLAYER,DEPTH))
print(time.time()-t)


