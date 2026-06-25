from move_funksion import Move
m = Move()

class Evaluate:




    def centralization(self, board):
        point = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                      if i<=5 and 1 <= j <= 6:
                          point += 15+(7-i)

                elif board[i][j] == -1:
                      if i>=3 and 1 <= j <= 6:
                          point-=(15+i)
                elif board[i][j] == 3 or board[i][j] ==-3 :
                    r = i ; c = j
                    a = board[i][j]
                    d1 = True
                    d2 = True
                    d3 = True
                    d4 = True
                    for h in [1, 2, 3, 4, 5, 6, 7]:
                        if r + h <= 7 and c + h <= 7 and d1:
                            if board[r + h][c + h] == 0:
                                point += a
                            else:
                                d1 = False

                        if r + h <= 7 and c - h >= 0 and d2:
                            if board[r + h][c - h] == 0:
                                point += a
                            else:
                                d2 = False
                        if r - h >= 0 and c - h >= 0 and d3:
                            if board[r - h][c - h] == 0:
                                point += a
                            else:
                                d3 = False
                        if r - h >= 0 and c + h <= 7 and d4:
                            if board[r - h][c + h] == 0:
                                point += a
                            else:
                                d4 = False
        return point/100



    def evaluate(self, board):
        score = 0
        for row in board:
            score+=sum(row)
        score+=self.centralization(board)
        return score


























