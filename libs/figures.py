from libs.exceptions import InvalidMoveException


class Figure:
	class Color:
		WHITE = 0
		BLACK = 1

	def __init__(self, color):
		self.color = color
	
	def __str__(self):
		color = "White" if self.color == Figure.Color.WHITE else "Black"
		return color + ' ' + self.__class__.__name__
	
	def __return_path(self, _from, to):

		diff = (to[0] - _from[0], to[1] - _from[1])

		# abs to make sure we don't change the sign
		divisor = abs(max(diff))
		diff_vector = (diff[0] // divisor, diff[1] // divisor)
		
		path = []
		_from = (_from[0] + diff_vector[0], _from[1] + diff_vector[1])

		while _from != to:
			path.append(tmp)
			_from = (_from[0] + diff_vector[0], _from[1] + diff_vector[1])

		return path
	
	def path(self, _from, to):
		raise NotImplementedError()
		
	
class Pawn(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
		
	def path(self, _from, to):

		diff = (to[0] - _from[0], to[1] - _from[1])

		if self.color == Figure.Color.WHITE:
			valid_moves = ((1, 0), (2, 0), (1, -1), (-1, -1))

		else:
			valid_moves = ((-1, 0), (-2, 0), (-1, -1), (-1, 1))

		if diff not in valid_moves:
			raise InvalidMoveException()

		if diff == (2, 0) or diff == (-2, 0):
			# check the inital positions if pawn moves over two squares
			if (self.color == Figure.Color.WHITE and _from[0] != 1):
				raise InvalidMoveException()

			elif (self.color == Figure.Color.BLACK and _from[0] != 6):
				raise InvalidMoveException()
			
			return [(_from[0] + (diff[0] // 2), _from[1])]
		# else there is no square in the path
		return []

class Knight(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
	def path(self, _from, to):

		abs_diff = (abs(to[0] - _from[0]), abs(to[1] - _from[1]))

		print(abs_diff)
		if abs_diff != (2, 1) and abs_diff != (1, 2):
			raise InvalidMoveException()

		return []

class Bishop(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
	
	def __norm(self, num):
		return 1 if num > 0 else -1
	
	def path(self, _from, to):
		
		diff = (to[0] - _from[0], to[1] - _from[1])

		# if absolute values of diff equal each other
		# it's a valid move for bishop
		if abs(diff[0]) != abs(diff[1]):
			raise InvalidMoveException()
		
		return super().__return_path(_From, to)



class Rook(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	def path(self, _from, to):
		
		diff = (to[0] - _from[0], to[1] - _from[1])

		# if absolute values of diff equal each other
		# it's a valid move for bishop
		if 0 not in diff:
			raise InvalidMoveException()
		
		return super().__return_path(_From, to)

class Queen(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	def path(self, _from, to):
		
		diff = (to[0] - _from[0], to[1] - _from[1])

		# check for diagonal and (horizontal,vertical)
		if abs(diff[0]) != abs(diff[1]) and 0 not in diff:
			raise InvalidMoveException()
		
		return super().__return_path(_From, to)

class King(Figure):

	def __init__(self, *arg, **kwarg):
		super().__init__(*arg, **kwarg)

	def path(self, _from, to):
		
		abs_diff = (abs(to[0] - _from[0]), abs(to[1] - _from[1]))

		if abs_diff != (1, 1) and abs_diff != (1, 0) and abs_diff != (0, 1):
			raise InvalidMoveException()
		
		return []
