from libs.exceptions import InvalidMoveException
from libs.utils import Vector2, args_to_vector


class Figure:
	class Color:
		WHITE = 0
		BLACK = 1

	def __init__(self, color):
		self.color = color
	
	def __str__(self):
		color = "White" if self.color == Figure.Color.WHITE else "Black"
		return color + ' ' + self.__class__.__name__
	
	@args_to_vector
	def _return_path(self, fro, to):

		diff = to - fro

		# abs to make sure we don't change the sign
		diff_vector = diff // abs(max(diff))

		
		path = []
		fro += diff_vector

		while fro != to:
			path.append(tmp)
			fro += diff_vector

		return path
	
	def path(self, fro, to):
		raise NotImplementedError()
		
	
class Pawn(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
		
	def path(self, fro, to):

		diff = (to[0] - fro[0], to[1] - fro[1])

		if self.color == Figure.Color.WHITE:
			valid_moves = ((1, 0), (2, 0), (1, -1), (-1, -1))

		else:
			valid_moves = ((-1, 0), (-2, 0), (-1, -1), (-1, 1))

		if diff not in valid_moves:
			raise InvalidMoveException()

		if diff == (2, 0) or diff == (-2, 0):
			# check the inital positions if pawn moves over two squares
			if (self.color == Figure.Color.WHITE and fro[0] != 1):
				raise InvalidMoveException()

			elif (self.color == Figure.Color.BLACK and fro[0] != 6):
				raise InvalidMoveException()
			
			return [(fro[0] + (diff[0] // 2), fro[1])]
		# else there is no square in the path
		return []

class Knight(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
	@args_to_vector
	def path(self, fro, to):

		abs_diff = abs(fro - to)

		if abs_diff != (2, 1) and abs_diff != (1, 2):
			raise InvalidMoveException()

		return []

class Bishop(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
	def __norm(self, num):
		return 1 if num > 0 else -1
	
	@args_to_vector
	def path(self, fro, to):
		
		diff = to - fro

		# if absolute values of diff equal each other
		# it's a valid move for bishop
		if abs(diff.x) != abs(diff.y):
			raise InvalidMoveException()
		
		return self._return_path(fro, to)



class Rook(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	@args_to_vector
	def path(self, fro, to):
		
		diff = to - fro

		# if absolute values of diff equal each other
		# it's a valid move for bishop
		if 0 not in diff:
			raise InvalidMoveException()
		
		return self._return_path(fro, to)

class Queen(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	@args_to_vector
	def path(self, fro, to):
		
		diff = to - fro

		# check for diagonal and (horizontal,vertical)
		if abs(diff.x) != abs(diff.y) and 0 not in diff:
			raise InvalidMoveException()
		
		return self._return_path(fro, to)

class King(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	@args_to_vector
	def path(self, fro, to):
		
		abs_diff = abs(to - fro)

		if abs_diff != (1, 1) and abs_diff != (1, 0) and abs_diff != (0, 1):
			raise InvalidMoveException()
		
		return []
