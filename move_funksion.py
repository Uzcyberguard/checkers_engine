class Move:


    def create_form(self,board, path):
        return [board,path]


    def is_there_captures(self,position):

        board = position[0]
        r = position[1][-1][0]
        c = position[1][-1][1]
        a = board[r][c]

        v1 = True
        v2 = True
        v3 = True
        v4 = True

        for q in [1, 2, 3, 4, 5, 6, 7]:

            # ===========================================================================================================

            if r - q >= 0 and c - q >= 0 and v1:
                if board[r - q][c - q] == -a or board[r - q][c - q] == int(-a / 3):

                    k = q + 1

                    while True:
                        if r - k < 0 or c - k < 0:
                            break
                        elif board[r - k][c - k] == 0:

                            return True
                        else:
                            v1 = False
                            break

                        k = k + 1
                elif board[r - q][c - q] == a or board[r - q][c - q] == int(a / 3):
                    v1 = False
            # ============================================================ ========================================
            if r + q <= 7 and c + q <= 7 and v2:
                if board[r + q][c + q] == -a or board[r + q][c + q] == int(-a / 3):
                    k = q + 1
                    while True:
                        if r + k > 7 or c + k > 7:
                            break
                        elif board[r + k][c + k] == 0:
                            return True
                        else:
                            v2 = False
                            break

                        k = k + 1
                elif board[r + q][c + q] == a or board[r + q][c + q] == int(a / 3):
                    v2 = False
                    # ============================================================================================
            if r - q >= 0 and c + q < 7 and v3:
                if board[r - q][c + q] == -a or board[r - q][c + q] == int(-a / 3):

                    k = q + 1

                    while True:
                        if 0 > r - k or c + k > 7:
                            break
                        if board[r - k][c + k] == 0:

                            return True
                        else:
                            v3 = False
                            break
                        k += 1
                elif board[r - q][c + q] == a or board[r - q][c + q] == int(a / 3):
                    v3 = False
                    # ============================================================================================
            if r + q < 7 and c - q >= 0 and v4:
                if board[r + q][c - q] == -a or board[r + q][c - q] == int(-a / 3):

                    k = q + 1

                    while True:
                        if r + k > 7 or c - k < 0:
                            break
                        if board[r + k][c - k] == 0:

                            return True
                        else:
                            v4 = False
                            break
                        k += 1
                elif board[r + q][c - q] == a or board[r + q][c - q] == int(a / 3):
                    v4 = False
        return False


    def find_captures(self,p_capture):
        captures = [p_capture.copy()]

        trash_list = []

        i = 0

        while i < len(captures):
            king_caps = []
            have_capture = False
            board = captures[i][0]
            r = captures[i][1][-1][0]
            c = captures[i][1][-1][1]
            a = board[r][c]
            # =================================================================================================
            if a == 1 or a == -1:

                for q in [-1, 1]:

                    if (r - 2 * q >= 0 and c - 2 * q >= 0) and (r - 2 * q <= 7 and c - 2 * q <= 7):
                        if board[r - q][c - q] == -a and board[r - 2 * q][c - 2 * q] == 0:
                            new_board = [row[:] for row in board]
                            new_board[r][c] = 0
                            new_board[r - q][c - q] = 0
                            new_board[r - 2 * q][c - 2 * q] = a
                            path = (captures[i][1]).copy()
                            path.append((r - 2 * q, c - 2 * q))
                            if r - 2 * q == 0 and a == 1:
                                new_board[r - 2 * q][c - 2 * q] = 3
                            elif r - 2 * q == 7 and a == -1:
                                new_board[r - 2 * q][c - 2 * q] = -3

                            captures.append(self.create_form(new_board, path))
                            have_capture = True

                for p in [-1, 1]:

                    if (r - 2 * p >= 0 and c + 2 * p >= 0) and (r - 2 * p <= 7 and c + 2 * p <= 7):
                        if board[r - p][c + p] == -a and board[r - 2 * p][c + 2 * p] == 0:
                            new_board = [row[:] for row in board]
                            new_board[r][c] = 0
                            new_board[r - p][c + p] = 0
                            new_board[r - 2 * p][c + 2 * p] = a
                            path = (captures[i][1]).copy()
                            path.append((r - 2 * p, c + 2 * p))
                            if r - 2 * p == 0 and a == 1:
                                new_board[r - 2 * p][c + 2 * p] = 3
                            elif r - 2 * p == 7 and a == -1:
                                new_board[r - 2 * p][c + 2 * p] = -3
                            captures.append(self.create_form(new_board, path))
                            have_capture = True
            # ====================================================================================================================
            # ====================================================================================================================


            if a == 3 or a == -3:
                v1 = True
                v2 = True
                v3 = True
                v4 = True

                for q in [1, 2, 3, 4, 5, 6, 7]:

                    # ===========================================================================================================

                    if r - q >= 0 and c - q >= 0 and v1:
                        if board[r - q][c - q] == -a or board[r - q][c - q] == int(-a / 3):

                            k = q + 1

                            while True:
                                if r - k < 0 or c - k < 0:
                                    break
                                elif board[r - k][c - k] == 0:
                                    new_board = [row[:] for row in board]
                                    new_board[r][c] = 0
                                    new_board[r - q][c - q] = 0
                                    new_board[r - k][c - k] = a
                                    path = (captures[i][1]).copy()
                                    path.append((r - k, c - k))
                                    king_caps.append(self.create_form(new_board, path))
                                    have_capture = True
                                else:
                                    v1 = False
                                    break

                                k = k + 1
                        elif board[r - q][c - q] == a or board[r - q][c - q] == int(a / 3):
                            v1 = False
                    # ============================================================ ========================================
                    if r + q <= 7 and c + q <= 7 and v2:
                        if board[r + q][c + q] == -a or board[r + q][c + q] == int(-a / 3):
                            k = q + 1
                            while True:
                                if r + k > 7 or c + k > 7:
                                    break
                                elif board[r + k][c + k] == 0:
                                    new_board = [row[:] for row in board]
                                    new_board[r][c] = 0
                                    new_board[r + q][c + q] = 0
                                    new_board[r + k][c + k] = a
                                    path = (captures[i][1]).copy()
                                    path.append((r + k, c + k))
                                    king_caps.append(self.create_form(new_board, path))
                                    have_capture = True
                                else:
                                    v2 = False
                                    break

                                k = k + 1
                        elif board[r + q][c + q] == a or board[r + q][c + q] == int(a / 3):
                            v2 = False
                            # ============================================================================================
                    if r - q >= 0 and c + q < 7 and v3:
                        if board[r - q][c + q] == -a or board[r - q][c + q] == int(-a / 3):

                            k = q + 1

                            while True:
                                if 0 > r - k or c + k > 7:
                                    break
                                if board[r - k][c + k] == 0:
                                    new_board = [row[:] for row in board]
                                    new_board[r][c] = 0
                                    new_board[r - q][c + q] = 0
                                    new_board[r - k][c + k] = a
                                    path = (captures[i][1]).copy()
                                    path.append((r - k, c + k))
                                    king_caps.append(self.create_form(new_board, path))
                                    have_capture = True
                                else:
                                    v3 = False
                                    break
                                k += 1
                        elif board[r - q][c + q] == a or board[r - q][c + q] == int(a / 3):
                            v3 = False
                            # ============================================================================================
                    if r + q < 7 and c - q >= 0 and v4:
                        if board[r + q][c - q] == -a or board[r + q][c - q] == int(-a / 3):

                            k = q + 1

                            while True:
                                if r + k > 7 or c - k < 0:
                                    break
                                if board[r + k][c - k] == 0:
                                    new_board = [row[:] for row in board]
                                    new_board[r][c] = 0
                                    new_board[r + q][c - q] = 0
                                    new_board[r + k][c - k] = a
                                    path = (captures[i][1]).copy()
                                    path.append((r + k, c - k))
                                    king_caps.append(self.create_form(new_board, path))
                                    have_capture = True
                                else:
                                    v4 = False
                                    break
                                k += 1
                        elif board[r + q][c - q] == a or board[r + q][c - q] == int(a / 3):
                            v4 = False
            b = 0
            for pos in king_caps:
                if self.is_there_captures(pos):
                    captures.append(pos)
                    b += 1

            if b == 0:
                captures.extend(king_caps)

            # ===========================================================================================================================
            if have_capture:
                trash_list.append(captures[i])
            i += 1

        return [x for x in captures if x not in trash_list]

    def find_moves(self,start_poss):
        board = start_poss[0]
        r = start_poss[1][-1][0]
        c = start_poss[1][-1][1]
        path = start_poss[1]
        possible_moves = []
        f = board[r][c]
        # =======================================================================
        if f == 1:
            if r - 1 >= 0 and c - 1 >= 0:
                if board[r - 1][c - 1] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = 0
                    new_board[r - 1][c - 1] = 1
                    path1 = path.copy()
                    path1.append((r - 1, c - 1))
                    if r - 1 == 0:
                        new_board[r - 1][c - 1] = 3
                    possible_moves.append(self.create_form(new_board, path1))

            if r - 1 >= 0 and c + 1 <= 7:
                if board[r - 1][c + 1] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = 0
                    new_board[r - 1][c + 1] = 1
                    path1 = path.copy()
                    path1.append((r - 1, c + 1))
                    if r - 1 == 0:
                        new_board[r - 1][c + 1] = 3
                    possible_moves.append(self.create_form(new_board, path1))
        elif f == -1:
            if r + 1 <= 7 and c - 1 >= 0:
                if board[r + 1][c - 1] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = 0
                    new_board[r + 1][c - 1] = -1
                    path1 = path.copy()
                    path1.append((r + 1, c - 1))
                    if r + 1 == 7:
                        new_board[r + 1][c - 1] = -3

                    possible_moves.append(self.create_form(new_board, path1))

            if r + 1 <= 7 and c + 1 <= 7:
                if board[r + 1][c + 1] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = 0
                    new_board[r + 1][c + 1] = -1
                    path1 = path.copy()
                    path1.append((r + 1, c + 1))
                    if r + 1 == 7:
                        new_board[r + 1][c + 1] = -3
                    possible_moves.append(self.create_form(new_board, path1))

        elif f == 3 or f == -3:
            d1 = True
            d2 = True
            d3 = True
            d4 = True
            for h in [1, 2, 3, 4, 5, 6, 7]:
                if r + h <= 7 and c + h <= 7 and d1:
                    if board[r + h][c + h] == 0:
                        new_board = [row[:] for row in board]
                        new_board[r][c] = 0
                        new_board[r + h][c + h] = f
                        path1 = path.copy()
                        path1.append((r + h, c + h))
                        possible_moves.append(self.create_form(new_board, path1))
                    else:
                        d1 = False

                if r + h <= 7 and c - h >= 0 and d2:
                    if board[r + h][c - h] == 0:
                        new_board = [row[:] for row in board]
                        new_board[r][c] = 0
                        new_board[r + h][c - h] = f
                        path1 = path.copy()
                        path1.append((r + h, c - h))
                        possible_moves.append(self.create_form(new_board, path1))
                    else:
                        d2 = False
                if r - h >= 0 and c - h >= 0 and d3:
                    if board[r - h][c - h] == 0:
                        new_board = [row[:] for row in board]
                        new_board[r][c] = 0
                        new_board[r - h][c - h] = f
                        path1 = path.copy()
                        path1.append((r - h, c - h))
                        possible_moves.append(self.create_form(new_board, path1))
                    else:
                        d3 = False
                if r - h >= 0 and c + h <= 7 and d4:
                    if board[r - h][c + h] == 0:
                        new_board = [row[:] for row in board]
                        new_board[r][c] = 0
                        new_board[r - h][c + h] = f
                        path1 = path.copy()
                        path1.append((r - h, c + h))
                        possible_moves.append(self.create_form(new_board, path1))
                    else:
                        d4 = False

        return possible_moves

    def legal_moves(self,piece, board):
        caps = []
        moves = []

        for i in range(8):
            for j in range(8):
                if piece == 1 and (board[i][j] == 1 or board[i][j] == 3):

                    cap = self.find_captures(self.create_form(board, [(i,j)]))
                    if len(cap) > 1 or len(cap[0][1]) > 1:
                        caps.extend(cap)
                    else:
                        moves.extend(self.find_moves(self.create_form(board,[(i,j)])))


                if piece == -1 and (board[i][j] == -1 or board[i][j] == -3):

                    cap = self.find_captures(self.create_form(board, [(i,j)]))
                    if len(cap) > 1 or len(cap[0][1]) > 1:
                        caps.extend(cap)
                    else:
                        moves.extend(self.find_moves(self.create_form(board, [(i,j)])))
        if caps:
            return caps
        else:
            return moves