import pygame as pg

vec = pg.math.Vector2
BG_COLOR = (45, 45, 45)
FIELD_COLOR = (211, 211, 211)

SPRITE_DIR_PATH = 'assets/sprites'
FONT_PATH = 'assets/font/ALUMNISANS.ttf'

ANIM_TIME_INTERVAL = 150  # milliseconds
FAST_ANIM_TIME_INTERVAL = 15

TILE_SIZE = 35

FIELD_SIZE = COLS, ROWS = 10, 22
FIELD_RES = COLS * TILE_SIZE, ROWS * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vec(COLS // 2 - 1, 0)
NEXT_POS_OFFSET = vec(COLS * 1.2, ROWS * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

MAX_FPS = 60
DROP_TIME = 20
DRAW = True

COLORS = [
	(45, 45, 45),
	(255, 85,  85),
	(100, 200, 115),
	(120, 108, 245),
	(255, 140, 50),
	(50,  120, 52),
	(146, 202, 73),
	(150, 161, 218),
	(35,  35,  35) 
]

TETROMINOS = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]