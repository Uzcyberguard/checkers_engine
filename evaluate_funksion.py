from move_funksion import Move
m = Move()

class Evaluate():
    def __init__(self):

        self.score = 0

    def centralization(self, board):
        for i in board:
            for j in i:
                if board[i][j] != 0:


    def evaluate(self, board):
        for row in board:
            self.score+=sum(row)*10

        self.score+=len(m.legal_moves(1,board,[]))*3
        self.score+=len(m.legal_moves(-1,board,[]))*(-3)





        return self.score
    def minimax(self,board,is_max):
        pass