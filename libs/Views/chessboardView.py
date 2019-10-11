import sys
import os
import pygame

from libs.chessboard import ChessBoard
from libs.figures import *


def draw_board(board_array, image_dict, screen):
    for row_index, row in enumerate(board_array):
        for col_index, piece in enumerate(row):
            if isinstance(piece, Pawn):
                screen.blit(image_dict['white_pawn'], (col_index * 67, row_index * 67))

def load_images(path_to_directory):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png') and 'board' not in filename:
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pygame.image.load(path)
    return image_dict

path_to_directory = r'libs\Views\sprites'
pygame.init()
HEIGHT = 550
WIDTH = 550
SIZE = (WIDTH, HEIGHT)

SCREEN = pygame.display.set_mode(SIZE)
BG = pygame.image.load(r'libs\Views\sprites\chessboard.png')
BG = pygame.transform.scale(BG, SIZE)

pieces_image_dict = load_images(path_to_directory)
cb = ChessBoard()
print(cb.board)

RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    SCREEN.blit(BG, (0, 0))
    draw_board(cb.board, pieces_image_dict, SCREEN)
    pygame.display.update()