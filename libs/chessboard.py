from libs.exceptions import InvalidMoveException
from libs.utils import Vector2
from libs.figures import (
	Figure, Pawn, Knight, Bishop, Rook, Queen, King
)


class ChessBoard:
	
	def __init__(self):
		self.__setup_initial_board()

		# current turn
		self.turn = Figure.Color.WHITE

		# Game history
		self.history = []
		self.dead_figures = []
	
	def __setup_first_row(self, color):
		row = [None] * 8
		row[0] = Rook(color)
		row[1] = Knight(color)
		row[2] = Bishop(color)
		row[3] = Queen(color)
		row[4] = King(color)
		row[5] = Bishop(color)
		row[6] = Knight(color)
		row[7] = Rook(color)
		return row

	def __setup_initial_board(self):
		self.board = [[None] * 8 for i in range(8)]

		# setup pawns
		self.board[1] = [Pawn(Figure.Color.WHITE) for i in range(8)]
		self.board[6] = [Pawn(Figure.Color.BLACK) for i in range(8)]

		# setup rest of the figures
		self.board[0] = self.__setup_first_row(Figure.Color.WHITE)
		self.board[7] = self.__setup_first_row(Figure.Color.BLACK)
	
	def get_piece_at_coordinates(self, coordinates):
		"""
		Get piece on given coordinates. If the coordinates is empty
		return None
		"""
		x, y = coordinates
		return self.board[x][y]
	
	def draw_board(self):

		board = ['   ' + ('   ').join('abcdefgh')]
		for i, row in enumerate(self.board[::-1]):

			row_content = [str(8 - i)]
			for square in row:
				if square is None:
					row_content.append('  ')
				else:
					name = str(square)
					initials = ''.join([w[0] for w in name.split()])
					row_content.append(initials)
			board.append('  '.join(row_content))
		return '\n'.join(board) + '\n'
	
	def move_algebra(self, fro, to):
		new_from = (int(fro[1]) - 1, ord(fro[0].lower()) - ord('a'))
		new_to = (int(to[1]) - 1, ord(to[0].lower()) - ord('a'))
		self.move(new_from, new_to)
		
	def move(self, _from, to):
		"""
		Move piece from "_from" coordinates to "to"
		"""
		#print("moving")
		# check coordinate sanity
		for coordinate in list(_from) + list(to):
			if 0 > coordinate > 8:
				raise InvalidMoveException()

		figure = self.get_piece_at_coordinates(_from)

		# figure is on right position
		if figure is None:
			raise InvalidMoveException()

		# not the turn of the current player
		if figure.color != self.turn:
			raise InvalidMoveException("Not your turn")

		#TODO -
		# check special moves like pawn promotion, castling, etc..
		# else: continue usual process

		# Change coordinates to vector
		_from = Vector2(_from)
		to = Vector2(to)

		# handle the path
		for square in figure.path(_from, to):

			# if something stands in the path raise Exception
			if self.get_piece_at_coordinates(square) is not None:
				raise InvalidMoveException()

		# handle destination square
		dest = self.get_piece_at_coordinates(to)
		if dest is not None:
			if dest.color == figure.color:
				raise InvalidMoveException()
			else:
				self.__kill(_from, to)
		else:
			self.__apply_move(figure, _from, to)

		# change turn
		self.turn = Figure.Color.WHITE if self.turn == Figure.Color.BLACK else Figure.Color.BLACK
			
			
	def __apply_move(self, figure, _from, to):

		_from = Vector2(_from)
		to = Vector2(to)

		self.board[_from.x][_from.y] = None
		self.board[to.x][to.y] = figure
	
	
	def __kill(self, fro, to):

		killer = self.board[fro[0]][fro[1]]
		killee = self.board[to[0]][to[1]]
	
		if killer is None or killee is None or killer.color == killee.color:
			raise RuntimeError()

		self.board[fro[0]][fro[1]] = None
		self.board[to[0]][to[1]] = killer

		self.dead_figures.append(killee)