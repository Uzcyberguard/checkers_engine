import pygame
from game import Game
pygame.init()

name = "KingKong"
board_surface = "checkers_boards/board4.png"
black_piece = "checkers_boards/piece_red.png"
white_piece ="checkers_boards/piece_white.png"
black_king = "checkers_boards/piece_red.png"
white_king = "checkers_boards/piece_white.png"

game = Game(name,board_surface,black_piece,white_piece,black_king,white_king)

game.run()