import pygame as pg
from copy import deepcopy
from enum import Enum

vec = pg.math.Vector2
BG_COLOR = (45, 45, 45)
FIELD_COLOR = (211, 211, 211)

FONT_PATH = 'assets/font/ALUMNISANS.ttf'

TILE_SIZE = 35
COLS, ROWS = 10, 22
FIELD_RES = COLS * TILE_SIZE, ROWS * TILE_SIZE
FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H
NEXT_POS_OFFSET = vec(COLS * 1.2, ROWS * 0.45)

MAX_FPS = 30
DROP_TIME = 50
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

TETROMINOES = [
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

def rotate_clockwise(shape):
	return [ [ shape[y][x]
		for y in range(len(shape)) ]
		for x in range(len(shape[0])-1, -1, -1) ]

def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[cy + off_y][cx + off_x]:
					return True
			except IndexError:
				return True
	return False

def remove_full_line(board, row):
	del board[row]
	return [[0 for i in range(COLS)]] + board
	
def join_matrices(matrix1, matrix2, matrix2_off):
	matrix3 = deepcopy(matrix1)
	off_x, off_y = matrix2_off
	for cy, row in enumerate(matrix2):
		for cx, val in enumerate(row):
			matrix3[cy+off_y-1][cx+off_x] += val
	return matrix3

class SelectionMethod(Enum):
	roulette = 1
 
class CrossoverMethod(Enum):
	random_attributes = 1
	average_attributes = 2

POPULATION_SIZE = 20
GAMES_TO_AVG = 2
SURVIVORS_PER_GENERATION = 6 # crossover probability = NEWBORNS / POPULATION_SIZE
NEWBORNS_PER_GENERATION = POPULATION_SIZE - SURVIVORS_PER_GENERATION
SELECTION_METHOD = SelectionMethod.roulette
CROSSOVER_METHOD = CrossoverMethod.random_attributes
MUTATION_PASSES = 3
MUTATION_RATE = 20 # mutation probability for a given chromosome is MUTATION_PASSES / MUTATION_RATE
CONVERGED_THRESHOLD = 15