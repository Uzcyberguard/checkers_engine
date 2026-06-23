class Evaluate():
    def __init__(self,board):
        self.board = board
        self.score = 0



    def evaluate(self, board):
        for row in board:
            self.score+=sum(row)

