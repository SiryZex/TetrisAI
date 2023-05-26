# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from random import randrange

from threading import Lock
from settings import *
from text import Text
import sys

def new_board():
	board = [[0 for x in range(COLS)] for y in range(ROWS)]
	board += [[1 for x in range(COLS)]]
	return board

class Tetris(object):
	def __init__(self, runner=None):
		self.DROPEVENT = pg.USEREVENT + 1

		pg.init()
		pg.display.set_caption("Tetris AI (GENETIC ALGORITHM)")
		pg.key.set_repeat(250,25)
		self.text = Text(self)
		self.sprite_group = pg.sprite.Group()
		self.width = TILE_SIZE * (COLS+10)
		self.height = TILE_SIZE * ROWS
		self.default_font = pg.font.Font(pg.font.get_default_font(), 11)
		self.screen = pg.display.set_mode(WIN_RES)
		self.next_tetromino = TETROMINOES[randrange(len(TETROMINOES))]
		self.gameover = False
		self.runner = runner
		self.ai = None
		self.lock = Lock()
		self.init_game()
	
	def new_tetromino(self):
		self.tetromino = self.next_tetromino
		self.next_tetromino = TETROMINOES[randrange(len(TETROMINOES))]
		self.tetromino_x = COLS//2 - len(self.tetromino[0])//2
		self.tetromino_y = 0
		self.score += 1
		
		if check_collision(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y)):
			self.gameover = True
			if self.runner:
				self.runner.on_game_over(self.score)

	def init_game(self):
		self.board = new_board()
		self.score = 0
		self.new_tetromino()
		pg.time.set_timer(self.DROPEVENT, DROP_TIME)
	
	def draw_grid(self):
		for x in range(COLS):
			for y in range(ROWS):
				pg.draw.rect(self.screen, 'black',
								(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				if val:
					try:
						pg.draw.rect(self.screen, COLORS[val], 
							pg.Rect((off_x+x)*TILE_SIZE, (off_y+y)*TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
					except IndexError:
						print("Corrupted board")
						print(self.board)
	
	def add_cl_lines(self, n):
		linescores = [0, 40, 100, 300, 1200]
		self.score += linescores[n]
	
	def move_to(self, x):
		self.move(x - self.tetromino_x)

	def move(self, delta_x):
		if not self.gameover:
			new_x = self.tetromino_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > COLS - len(self.tetromino[0]):
				new_x = COLS - len(self.tetromino[0])
			if not check_collision(self.board, self.tetromino, (new_x, self.tetromino_y)):
				self.tetromino_x = new_x
	
	def drop(self):
		self.lock.acquire()
		if not self.gameover:
			self.tetromino_y += 1
			if check_collision(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y)):
				self.board = join_matrices(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y))
				self.new_tetromino()
				cleared_rows = 0
				for i, row in enumerate(self.board[:-1]):
					if 0 not in row:
						self.board = remove_row(self.board, i)
						cleared_rows += 1
				self.add_cl_lines(cleared_rows)

				self.lock.release()				
				if self.ai:
					self.ai.make_move()

				return True
		self.lock.release()
		return False

	def start_game(self):
		if self.gameover:
			self.init_game()
			self.gameover = False
   
	def center_msg(self, score):
		self.screen.fill(BG_COLOR)
		self.text.font.render_to(self.screen, (WIN_W * 0.38, WIN_H * 0.38),
            text='Game Over!', fgcolor='red', size=TILE_SIZE, bgcolor=(45, 45, 45))
		self.text.font.render_to(self.screen, (WIN_W * 0.33, WIN_H * 0.48),
            text='Your score: %d' % score, fgcolor='red', size=TILE_SIZE, bgcolor=(45, 45, 45))
		self.text.font.render_to(self.screen, (WIN_W * 0.26, WIN_H * 0.58),
            text='Press space to continue', fgcolor='red', size=TILE_SIZE, bgcolor=(45, 45, 45))

	def run(self):
		key_actions = {
			'ESCAPE':	sys.exit,
			'SPACE': self.start_game,
		}
		
		clock = pg.time.Clock()
		while True:
			if DRAW:
				self.screen.fill(BG_COLOR)
				self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
				if self.gameover:
					self.center_msg(self.score)
				else:
					self.text.draw()
					self.draw_grid()
					self.draw_matrix(self.board, (0,0))
					self.draw_matrix(self.tetromino, (self.tetromino_x, self.tetromino_y))
					self.draw_matrix(self.next_tetromino, NEXT_POS_OFFSET)
				pg.display.update()
			
			for event in pg.event.get():
				if event.type == self.DROPEVENT:
					self.drop()
				elif event.type == pg.QUIT:
					sys.exit()
				elif event.type == pg.KEYDOWN:
					for key in key_actions:
						if event.key == eval("pg.K_" + key):
							key_actions[key]()
					
			clock.tick(MAX_FPS)

if __name__ == "__main__":
	from ai import AI
	app = Tetris()
	app.ai = AI(app)
	app.ai.instant_play = False
	app.run()