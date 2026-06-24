from move_funksion import Move
m = Move()

class Evaluate():




    def centralization(self, board):
        for i in board:
            for j in i:
                if board[i][j] != 0:
                    pass


    def evaluate(self, board):
        score = 0
        for row in board:
            score+=sum(row)*10

        score+=len(m.legal_moves(1,board))
        score-=len(m.legal_moves(-1,board))
        return score

    def game_over(self,board,player):
        if m.legal_moves(player,board) == 0:
            return False

























