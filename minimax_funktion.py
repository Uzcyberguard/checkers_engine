from evaluate_funksion import Evaluate
from move_funksion import Move
e = Evaluate()
m = Move()
class Minimax:



        def minimax(self,board, depth, alpha, beta, player, ply):

            if depth == 0 :
                return e.evaluate(board)

            moves = m.legal_moves(player,board)
            if len(moves)==0 :
                if player ==1:
                   return -1000+ply
                else:
                   return 1000-ply
            if player == 1:  # MAX

                value = -float("inf")

                for move in moves:

                    new_board = move[0]

                    value = max(
                        value,
                        self.minimax(
                            new_board,
                            depth-1,
                            alpha,
                            beta,
                            -player,
                            ply+1
                        )
                    )
                    alpha = max(alpha, value)

                    if alpha >= beta:
                        break

                return value

            else:  # MIN

                value = float("inf")

                for move in moves:

                    new_board = move[0]

                    value = min(
                        value,
                        self.minimax(
                            new_board,
                            depth-1,
                            alpha,
                            beta,
                            -player,
                            ply+1
                        )
                    )

                    beta = min(beta, value)

                    if alpha >= beta:
                        break

                return value