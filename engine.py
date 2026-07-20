""" Created on Mon Jun  8 15:54:51 2026 Hasan Normamatov """
from generate_move import Move
from evaluate_funksion import Evaluate
from minimax_funktion import Minimax
import time
t = time.time()




class Engine:
    def __init__(self, depth, player, board):
        self.move = Move()
        self.evaluate = Evaluate()
        self.minimax = Minimax()
        self.depth = depth
        self.player = player
        self.board = [
            [ 0,-1, 0,-1, 0,-1, 0,-1],  # 0
            [ 0, 0,-1, 0, 0, 0, 0, 0],  # 1
            [ 0, 0, 0, 0, 0, 0, 0, 0],  # 2
            [-3, 0, 0, 0, 0, 0, 0, 0],  # 3
            [ 0, 0, 0, 1, 0, 1, 0, 0],  # 4
            [ 3, 0, 0, 0, 0, 0, 1, 0],  # 5
            [ 0, 1, 0, 0, 0, 0, 0, 1],  # 6
            [ 0, 0, 1, 0, 1, 0, 1, 0]   # 7
            # 0  1  2  3  4  5  6  7
        ]








    def best_move(self):

        moves = self.move.legal_moves(self.player, self.board)
        if not moves:
            print("this team has already checkmated")
            return ""
        if self.player == 1:
            best_score = -float("inf")
        else:
            best_score = float("inf")

        best_path = None

        for new_board, path in moves:

            score = self.minimax.minimax(
                new_board,
                self.depth-1,
                -float("inf"),
                float("inf"),
                -self.player,
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
            if self.player == 1:
                if score > best_score:
                    best_score = score
                    best_path = path
            else:
                if score < best_score:
                    best_score = score
                    best_path = path

        return best_path









