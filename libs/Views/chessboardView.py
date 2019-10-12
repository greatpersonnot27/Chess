import sys
import os
import pygame

from libs.chessboard import ChessBoard
from libs.figures import *

path_to_directory = r'libs\Views\sprites'
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 480
FIGURE_SIZE = 60
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

def draw_board(board_array, image_dict, screen):
    for row_index, row in enumerate(board_array):
        for col_index, piece in enumerate(row):
            if piece:
                screen.blit(image_dict[str(piece)], (col_index * FIGURE_SIZE, row_index * FIGURE_SIZE))

def load_images(path_to_directory):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png') and 'board' not in filename:
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pygame.image.load(path)
    return image_dict

def mouse_handler(positions):
    mouse_position = pygame.mouse.get_pos()
    row = int(mouse_position[1]/60)
    column = int(mouse_position[0]/60)
    if positions[0]:
        positions[1] = (row, column)
        cb.move(positions[0], positions[1])
        positions[0] = None
    else:
        positions[0] = (row,column)


pygame.init()

SCREEN = pygame.display.set_mode(SIZE)
BG = pygame.image.load(r'libs\Views\sprites\chessboard.png')
BG = pygame.transform.scale(BG, SIZE)

pieces_image_dict = load_images(path_to_directory)
cb = ChessBoard()

RUN = True
mouse_start_pos = None
mouse_end_pos = None
positions = [mouse_start_pos, mouse_end_pos]
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_handler(positions)

    SCREEN.blit(BG, (0, 0))
    draw_board(cb.board, pieces_image_dict, SCREEN)
    pygame.display.update()