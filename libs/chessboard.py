from libs.exceptions import InvalidMoveException
from libs.figures import (
	Figure, Pawn, Knight, Bishop, Rook, Queen, King
)


class ChessBoard:
	
	def __init__(self):
		self.__setup_initial_board()

		# current turn
		self.turn = Figure.Color.WHITE
	
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
	
	def get_piece_coordinates(piece):
		"""
		Get the coordinates of the current piece
		"""
		for i in range(8):
			for k in range(8):
				if self.board[i][k] == piece:
					return (i, k)
		return None
	
	def get_piece_at_coordinates(self, coordinates):
		"""
		Get piece on given coordinates. If the coordinates is empty
		return None
		"""
		x, y = coordinates
		return self.board[x][y]
	
	def draw_board(self):
		board = []
		for row in self.board[::-1]:

			row_content = []
			for square in row:
				if square is None:
					row_content.append('  ')
				else:
					name = str(square)
					initials = ''.join([w[0] for w in name.split()])
					row_content.append(initials)
			board.append(' '.join(row_content))
		return '\n'.join(board) + '\n'
	
	def move(self, _from, to):
		"""
		Move piece from "_from" coordinates to "to"
		"""

		# check coordinate sanity
		for coordinate in _from + to:
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
		# else: continue traditional process

		# handle the path
		for square in figure.path(_from, to):

			# if something stands in the path raise Exception
			if self.get_piece_at_coordinates(square) is not None:
				raise InvalidMoveException()

		# handle destination
		dest = self.get_piece_at_coordinates(to)
		if dest is not None:
			if dest.color == figure.color:
				raise InvalidMoveException()
			else:
				#TODO - kill
				return
		else:
			self.__apply_move(figure, _from, to)

		self.turn = Figure.Color.WHITE if self.turn == Figure.Color.BLACK else Figure.Color.BLACK
			
			
	def __apply_move(self, figure, _from, to):

		from_x, from_y = _from
		to_x, to_y = to
		self.board[from_x][from_y] = None
		self.board[to_x][to_y] = figure

			
	
	def move_pawn(self, color, _from, to):

		from_x, from_y = _from
		to_x, to_y = to

		if color == Color.WHITE:
			diff = (to_x - from_x, to_y - from_y)
		else:
			diff = (from_x - to_x, from_y - to_y)

		if diff == (1, 0):
			if self.get_piece_at_coordinates(to) is None:
				self.board[from_x][from_y] = None
				self.board[to_x][to_y] = (Figure.PAWN, color)
			else:
				raise InvalidMoveException()

		elif diff == (2, 0):
			# if pawn are not on the initial position raise InvalidMove
			if (color == Color.BLACK and from_y != 6) or (color == Color.WHITE and from_y != 1):
				raise InvalidMoveException()

			if self.get_piece_at_coordinates(to) is None:
				self.board[from_x][from_y] = None
				self.board[to_x][to_y] = (Figure.PAWN, color)
			else:
				raise InvalidMoveException()

		elif diff == (1, -1) or diff == (1, 1):
			pass
		else:
			raise InvalidMoveException()

