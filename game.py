import pygame
from sys import exit
from pieces import Piece
from generate_move import Move
class Game:
     def __init__(self,name,board_surface,black_piece,white_piece,black_king,white_king,board):
        self.pygame = pygame
        self.pygame.init()
        self.board = board
        self.screen = pygame.display.set_mode((1200,800))
        self.pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.X = 70 # x coordinate of first piece
        self.Y = 72 # y coordinate of first piece
        self.D = 84 # distance between two neighbour squares
        self.board_cor = [[ (round(self.X + j * self.D),round(self.Y + i * self.D))  for j in range(8) ]   for i in range(8) ]
        self.board_surface = pygame.image.load(board_surface).convert_alpha()
        self.board_surface = pygame.transform.scale(self.board_surface, (750, 750))


        self.black_piece = pygame.image.load(black_piece).convert_alpha()
        self.black_piece = pygame.transform.scale(self.black_piece,(70,70))
        self.white_piece = pygame.image.load(white_piece).convert_alpha()
        self.white_piece = pygame.transform.scale(self.white_piece, (70, 70))
        self.black_king = pygame.image.load(black_king).convert_alpha()
        self.black_king = pygame.transform.scale(self.black_king,(70,70))
        self.white_king = pygame.image.load(white_king).convert_alpha()
        self.white_king= pygame.transform.scale(self.white_king, (70, 70))



        self.pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j]==1:
                    self.pieces.append(Piece(i,j,1,False))
                elif self.board[i][j]==-1:
                    self.pieces.append(Piece(i, j, -1,False))
                elif self.board[i][j] == 3:
                    self.pieces.append(Piece(i,j,1,True))
                elif self.board[i][j] == -3 :
                    self.pieces.append(Piece(i,j,-1,True))
        self.selected_piece = None
        self.move_to = None
        self.mouse_pos = (-10,-10)


     def highlight_moves(self):
         row = self.selected_piece.row
         col = self.selected_piece.col
         for legal in Move().legal_moves(self.selected_piece.color,self.board):

             if (row,col) == legal[1][0]:

                 caps = []
                 moves = []
                 if self.selected_piece.color == 1 and (self.board[row][col] == 1 or self.board[row][col] == 3):

                     cap = Move().find_captures(Move().create_form(self.board, [(row, col)]))
                     if len(cap) > 1 or len(cap[0][1]) > 1:
                         caps.extend(cap)
                     else:
                         moves.extend(Move().find_moves(Move().create_form(self.board, [(row, col)])))


                 # elif self.selected_piece.color == -1 and (self.board[row][col] == -1 or self.board[row][col] == -3):
                 #
                 #     cap = Move().find_captures(Move().create_form(self.board, [(row, col)]))
                 #     if len(cap) > 1 or len(cap[0][1]) > 1:
                 #         caps.extend(cap)
                 #     else:
                 #         moves.extend(Move().find_moves(Move().create_form(self.board, [(row, col)])))

                 if caps:
                     for i in caps:
                            for j in range(1,len(i[1])):

                                 x, y = self.board_cor[ i[1][j][0] ][ i[1][j][1] ]

                                 pygame.draw.circle(self.screen, (255, 255, 0), (x + self.D // 2 - 5, y + self.D // 2 - 5), 10)


                 else:
                     for i in moves:
                         for j in range(1, len(i[1])):
                             x, y = self.board_cor[i[1][j][0]][i[1][j][1]]
                             pygame.draw.circle(self.screen, (255, 255, 0), (x + self.D // 2 - 5, y + self.D // 2 - 5), 10)

     def draw(self):
         self.screen.blit(self.board_surface, (25, 25))

         for p in self.pieces:
             x, y = self.board_cor[p.row][p.col]

             if p.color == 1:
                 img = self.white_king if p.king else self.white_piece
             else:
                 img = self.black_king if p.king else self.black_piece
             p.rect = img.get_rect(topleft=(x, y))
             self.screen.blit(img, p.rect)

             if p == self.selected_piece:
                 pygame.draw.rect(
                     self.screen,
                     (255,255, 0),
                     p.rect.inflate(7, 7),
                     width=3
                 )
                 self.highlight_moves()
             if self.move_to is not None:
                 p.row = self.move_to[0]
                 p.col = self.move_to[1]
                 self.move_to = None

     def event_handler(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.mouse_pos = pygame.mouse.get_pos()
                 self.move_to = None
                 for i in range(8):
                     for j in range(8):
                         if (5< self.board_cor[i][j][0]-self.mouse_pos[0]<70) and (5< self.board_cor[i][j][1]-self.mouse_pos[1]<70):
                             self.move_to = (i,j)
                 self.selected_piece = None
                 for p in self.pieces:
                     if p.rect.collidepoint(self.mouse_pos) and p.color == 1:
                         self.selected_piece = p
                         print(self.selected_piece.color)
                         break
     def run(self):
        while True:

           self.event_handler()
           self.draw()

           pygame.display.update()
           self.clock.tick(60)