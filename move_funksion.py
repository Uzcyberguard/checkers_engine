class Move():
    def __init__(self):
        pass

    def is_there_capture(self,position):
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
            if a == 1 or a == -1:  # oddiy donalar uchun

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

                            captures.append([new_board, path])
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
                            captures.append([new_board, path])
                            have_capture = True
            # ====================================================================================================================
            # ====================================================================================================================
            #  DAMKAAAAAAAAAAAAAAAAAA

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
                                    king_caps.append([new_board, path])
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
                                    king_caps.append([new_board, path])
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
                                    king_caps.append([new_board, path])
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
                                    king_caps.append([new_board, path])
                                    have_capture = True
                                else:
                                    v4 = False
                                    break
                                k += 1
                        elif board[r + q][c - q] == a or board[r + q][c - q] == int(a / 3):
                            v4 = False
            b = 0
            for pos in king_caps:
                if self.is_there_capture(pos):
                    captures.append(pos)
                    b += 1

            if b == 0:
                captures.extend(king_caps)

            # ===========================================================================================================================
            if have_capture:
                trash_list.append(captures[i])
            i += 1

        return [x for x in captures if x not in trash_list]
