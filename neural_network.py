from tetris import check_collision, COLS, join_matrices, rotate_clockwise
import heuristic
from collections import namedtuple

Move = namedtuple('Move', ['x_pos', 'rotation', 'result'])

class NeuralNetwork(object):
	def __init__(self, tetris):
		self.tetris = tetris
		self.heuristics = {
			heuristic.num_holes: -364,
			heuristic.num_tetrominoes: 123,
			heuristic.max_height: -865,
			heuristic.avg_height: -533,
			heuristic.num_tetrominoes_above_holes: 475,
			heuristic.num_gaps: -23,			
		}
		self.instant_play = True

	def board_with_tetromino(self, x, y, tetromino):
		return join_matrices(self.tetris.board, tetromino, (x, y))

	def intersection_point(self, x, tetromino):
		y = 0
		while not check_collision(self.tetris.board, tetromino, (x, y)):
			y += 1
		return y - 1

	@staticmethod
	def max_x_pos_for_tetromino(tetromino):
		return COLS - len(tetromino[0])

	@staticmethod
	def num_rotations(tetromino):
		tetrominos = [tetromino]
		while True:
			tetromino = rotate_clockwise(tetromino)
			if tetromino in tetrominos:
				return len(tetrominos)
			tetrominos.append(tetromino)

	def utility(self, board):
		return sum([fun(board)*weight for (fun, weight) in self.heuristics.items()])

	def all_possible_moves(self):
		moves = []
		tetromino = self.tetris.tetromino
		for r in range(NeuralNetwork.num_rotations(tetromino)):
			for x in range(self.max_x_pos_for_tetromino(tetromino)+1):
				y = self.intersection_point(x, tetromino)
				board = self.board_with_tetromino(x, y, tetromino)
				moves.append(Move(x, r, board))
			tetromino = rotate_clockwise(tetromino)
		return moves		

	def best_move(self):
		return max(self.all_possible_moves(), key=lambda m: self.utility(m.result))		

	def make_move(self):
		tetris = self.tetris

		move = self.best_move()

		tetris.lock.acquire()
		for _ in range(move.rotation):
			tetris.tetromino = rotate_clockwise(tetris.tetromino)
		tetris.move_to(move.x_pos)		
		if self.instant_play:
			tetris.tetromino_y = self.intersection_point(move.x_pos, tetris.tetromino)
		tetris.lock.release()
