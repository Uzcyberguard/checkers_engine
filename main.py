import pygame
from sys import exit
from pieces import Piece
pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("deok")
clock = pygame.time.Clock()

# test_surface = pygame.Surface((100,200))
# test_surface.fill("green")
X = 75 # x coordinate of first piece
Y = 78 # y coordinate of first piece
D = 83 # distance between two neighbour squares



board_cor = [
    [ (round(X + j * D),round(Y + i * D))  for j in range(8) ]
    for i in range(8)
]

board_surface = pygame.image.load("checkers_boards/board4.png").convert_alpha()
board_surface = pygame.transform.scale(board_surface, (750, 750))



black_piece = pygame.image.load("checkers_boards/piece_red.png").convert_alpha()
black_piece = pygame.transform.scale(black_piece,(70,70))
white_piece = pygame.image.load("checkers_boards/piece_white.png").convert_alpha()
white_piece = pygame.transform.scale(white_piece, (70, 70))
black_king = pygame.image.load("checkers_boards/piece_red.png").convert_alpha()
black_king = pygame.transform.scale(black_king,(70,70))
white_king = pygame.image.load("checkers_boards/piece_white.png").convert_alpha()
white_king= pygame.transform.scale(white_king, (70, 70))



pieces = [
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


while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()
   screen.blit(board_surface,(25,25))
   for piece in pieces:
       x, y = board_cor[piece.row][piece.col]
       if piece.color == "white":
           img = white_king if piece.king else white_piece
       else:
           img = black_king if piece.king else black_piece
       screen.blit(img,(x,y))

   pygame.display.update()
   clock.tick(60)