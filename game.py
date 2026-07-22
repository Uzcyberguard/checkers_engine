import pygame
from sys import exit
from pieces import Piece
from generate_move import Move
class Game:
     def __init__(self,name,board_surface,black_piece,white_piece,black_king,white_king):
        self.pygame = pygame
        self.pygame.init()
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



        self.pieces = [
            # Black pieces
            Piece(0, 1, "black"),
            Piece(0, 3, "black"),
            Piece(0, 5, "black"),
            Piece(0, 7, "black"),

            Piece(1, 0, "black"),
            Piece(1, 2, "black"),
            Piece(1, 4, "black"),
            Piece(1, 6, "black"),

            Piece(2, 1, "black"),
            Piece(2, 3, "black"),
            Piece(2, 5, "black"),
            Piece(2, 7, "black"),

            # White pieces
            Piece(5, 0, "white"),
            Piece(5, 2, "white"),
            Piece(5, 4, "white"),
            Piece(5, 6, "white"),

            Piece(6, 1, "white"),
            Piece(6, 3, "white"),
            Piece(6, 5, "white"),
            Piece(6, 7, "white"),

            Piece(7, 0, "white"),
            Piece(7, 2, "white"),
            Piece(7, 4, "white"),
            Piece(7, 6, "white"),
        ]
        self.selected_piece = None
        self.mouse_pos = (-10,-10)

     def draw(self):
         self.screen.blit(self.board_surface, (25, 25))

         for p in self.pieces:
             x, y = self.board_cor[p.row][p.col]

             if p.color == "white":
                 img = self.white_king if p.king else self.white_piece
             else:
                 img = self.black_king if p.king else self.black_piece
             p.rect = img.get_rect(topleft=(x, y))
             self.screen.blit(img, p.rect)
             if p.rect.collidepoint(self.mouse_pos):
                 self.selected_piece = p
             if p == self.selected_piece:
                 pygame.draw.rect(
                     self.screen,
                     (255,255, 0),
                     p.rect.inflate(6, 6),
                     width=3
                 )


     def event_handler(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.mouse_pos = pygame.mouse.get_pos()
                 self.selected_piece = None
                 for p in self.pieces:
                     if p.rect.collidepoint(self.mouse_pos):
                         self.selected_piece = p
                         break
     def run(self):
        while True:

           self.event_handler()
           self.draw()

           pygame.display.update()
           self.clock.tick(60)