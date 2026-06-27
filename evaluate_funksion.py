from move_funksion import Move
m = Move()

class Evaluate:




    def centralization_weight(self, board):

        point = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                      point+=(100+7-i)
                      if i<=5 and 1 <= j <= 6:
                          point += 15

                elif board[i][j] == -1:
                      point-=(100+i)
                      if i>=2 and 1 <= j <= 6:
                          point-= 15

                elif board[i][j] == 3 or board[i][j] ==-3 :
                    mobility = 0
                    r = i ; c = j
                    a = board[i][j]
                    point+=a*300
                    d1 = True
                    d2 = True
                    d3 = True
                    d4 = True
                    for h in [1, 2, 3, 4, 5, 6, 7]:
                        if r + h <= 7 and c + h <= 7 and d1:
                            if board[r + h][c + h] == 0:
                                point += a
                                mobility+=1
                            else:
                                d1 = False

                        if r + h <= 7 and c - h >= 0 and d2:
                            if board[r + h][c - h] == 0:
                                point += a
                                mobility+=1
                            else:
                                d2 = False
                        if r - h >= 0 and c - h >= 0 and d3:
                            if board[r - h][c - h] == 0:
                                point += a
                                mobility+=1
                            else:
                                d3 = False
                        if r - h >= 0 and c + h <= 7 and d4:
                            if board[r - h][c + h] == 0:
                                point += a
                                mobility+=1
                            else:
                                d4 = False
                    if mobility == 0 and not m.is_there_captures([board,[(i,j)]]):
                        point -= 20*a
                    elif mobility == 1 and not m.is_there_captures([board,[(i,j)]]) :
                        point -= 10*a
        return point/100



    def evaluate(self, board):
        score = 0


        score+=self.centralization_weight(board)
        return score


























