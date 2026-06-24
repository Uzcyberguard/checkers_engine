from move_funksion import Move
m = Move()

class Evaluate():




    def centralization(self, board):
        point = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                      if i<=5 and 1 <= j <= 6:
                          point += 15+i

                if board[i][j] == -1:
                      if i>=3 and 1 <= j <= 6:
                          point-=(22+i)

        return point
    def king_dominance(self,board):
        pass



    def evaluate(self, board):
        score = 0
        for row in board:
            score+=sum(row)*100

        score+=len(m.legal_moves(1,board))*5
        score-=len(m.legal_moves(-1,board))*5
        score+=self.centralization(board)
        return score


























