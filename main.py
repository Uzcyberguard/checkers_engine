import pygame
from game import Game
from engine import Engine
pygame.init()

board = [
    [ 0,-1, 0,-1, 0,-1, 0,-1],  # 0
    [-1, 0, 0, 0,-1, 0,-1, 0],  # 1
    [ 0,-1, 0, 0, 0,-1, 0,-1],  # 2
    [ 0, 0, 0, 0, 0, 0, 0, 0],  # 3
    [ 0, 0, 0, 0, 0,-1, 0, 0],  # 4
    [ 1, 0, 1, 0, 1, 0, 3, 0],  # 5
    [ 0, 1, 0, 1, 0, 1, 0, 1],  # 6
    [ 1, 0, 1, 0, 1, 0, 1, 0]   # 7
    # 0  1  2  3  4  5  6  7
]

name = "KingKong"
board_surface = "checkers_boards/board_emerald_ivory.png"
black_piece = "checkers_boards/piece_red.png"
white_piece ="checkers_boards/piece_white.png"
black_king = "checkers_boards/king_red.png"
white_king = "checkers_boards/king_white.png"

game = Game(name,board_surface,black_piece,white_piece,black_king,white_king,board)
eng = Engine(8,1,board)
# print(eng.best_move())

game.run()