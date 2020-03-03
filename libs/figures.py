from libs.exceptions import InvalidMoveException
from libs.utils import Vector2


class Figure:
	class Color:
		WHITE = 0
		BLACK = 1

	def __init__(self, color):
		self.color = color
	
	def __str__(self):
		color = "White" if self.color == Figure.Color.WHITE else "Black"
		return color + ' ' + self.__class__.__name__
	
	def _return_path(self, fro, to):
		diff = to - fro

		# abs to make sure we don't change the sign
		normal_vector = diff // abs(max(diff))

		path = []
		fro += normal_vector

		while fro != to:
			path.append(fro)
			fro += normal_vector

		return path
	
	def path(self, fro, to):
		raise NotImplementedError()

	def get_all_moves(self, position):
		raise NotImplementedError

	def _get_all_moves_jumpers(self, pos, vectors):
		"""
        This method is used to get all the moves of Knight and King.
        Knight and King are called jumpers, because they can only jump one vector.
		"""
		moves = []

		for x, y in vectors:
			move = (pos[0] + x, pos[1] + y)
			if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
				moves.append([move])

		return moves

	def _get_all_moves_sliders(self, pos, vectors):
		"""
        This method is used to get all the moves of Queen, Bishop and Rook.
        Queen, Bishop and Rook are sliders, because they slide towards the vector direction.
		"""
		moves = []

		for x, y in vectors:
			move_list = []
			move = (pos[0] + x, pos[1] + y)
			while 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
				move_list.append(move)
				move = (move[0] + x, move[1] + y)
			if move_list != []:
				moves.append(move_list)

		return moves
		
	
class Pawn(Figure):
	def get_all_moves(self, pos):
		if self.color == Figure.Color.WHITE:

			move1 = (pos[0] + 1, pos[1])
			move2 = (pos[0] + 2, pos[1])

			if pos[0] == 1:
				return [[move1, move2]]
			return [[move1]]

		elif self.color == Figure.Color.BLACK:
			move1 = (pos[0] - 1, pos[1])
			move2 = (pos[0] - 2, pos[1])

			if pos[0] == 6:
				return [[move1, move2]]
			return [[move1]]

	def path(self, fro, to):

		diff = to - fro

		if self.color == Figure.Color.WHITE:
			valid_moves = ((1, 0), (2, 0), (1, -1), (-1, -1))

		else:
			valid_moves = ((-1, 0), (-2, 0), (-1, -1), (-1, 1))

		if tuple(diff) not in valid_moves:
			raise InvalidMoveException()

		if diff == (2, 0) or diff == (-2, 0):
			# check the inital positions if pawn moves over two squares
			if (self.color == Figure.Color.WHITE and fro.x != 1):
				raise InvalidMoveException()

			elif (self.color == Figure.Color.BLACK and fro.x != 6):
				raise InvalidMoveException()
			
			return [fro + (diff // 2)]
		# else there is no square in the path
		return []

class Knight(Figure):
	def get_all_moves(self, pos):
		vectors = [(1, 2), (-1, 2), (1, -2), (-1, -2),
				 (2, 1), (-2, 1), (2, -1), (-2, -1)]
		return self._get_all_moves_jumpers(pos, vectors)


	def path(self, fro, to):
		abs_diff = abs(fro - to)

		if abs_diff != (2, 1) and abs_diff != (1, 2):
			raise InvalidMoveException()

		return []

class Bishop(Figure):
	def get_all_moves(self, pos):
		vectors = [(1, 1), (-1, 1), (-1, 1), (-1, -1)]
		return self._get_all_moves_sliders(pos, vectors)

	def path(self, fro, to):
		diff = to - fro

		# if absolute values of diff don't equal  each other
		# it's not a valid bishop move.
		if abs(diff.x) != abs(diff.y):
			raise InvalidMoveException()
		
		return self._return_path(fro, to)


class Rook(Figure):
	def get_all_moves(self, pos):
		vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		return self._get_all_moves_sliders(pos, vectors)

	def path(self, fro, to):
		diff = to - fro

		# if absolute values of diff equal each other
		# it's a valid move for bishop
		if 0 not in diff:
			raise InvalidMoveException()
		
		return self._return_path(fro, to)

class Queen(Figure):
	def get_all_moves(self, pos):
		vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, 1), (-1, -1)]
		return self._get_all_moves_sliders(pos, vectors)

	def path(self, fro, to):
		diff = to - fro

		# check for diagonal and (horizontal,vertical)
		if abs(diff.x) != abs(diff.y) and 0 not in diff:
			raise InvalidMoveException()
		
		return self._return_path(fro, to)

class King(Figure):
	def get_all_moves(self, pos):
		vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, 1), (-1, -1)]
		return self._get_all_moves_jumpers(pos, vectors)


	def path(self, fro, to):
		abs_diff = abs(to - fro)

		if abs_diff != (1, 1) and abs_diff != (1, 0) and abs_diff != (0, 1):
			raise InvalidMoveException()
		
		return []
