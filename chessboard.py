from exceptions import InvalidMoveException


# figures enum
class Figure:
	PAWN = 0
	KNIGHT = 1
	BISHOP = 2
	ROOK = 3
	QUEEN = 4
	KING = 5

# Colors enum
class Color:
	WHITE = 0
	BLACK = 1

class ChessBoard:
	
	def __init__(self):
		self.__setup_initial_board()
	
	def __setup_first_row(self, color):
		row = [None] * 8
		row[0] = (Figure.ROOK, color)
		row[1] = (Figure.KNIGHT, color)
		row[2] = (Figure.BISHOP, color)
		row[3] = (Figure.QUEEN, color)
		row[4] = (Figure.KING, color)
		row[5] = (Figure.BISHOP, color)
		row[6] = (Figure.KNIGHT, color)
		row[7] = (Figure.ROOK, color)
		return row

	def __setup_initial_board(self):
		self.board = [[None] * 8 for i in range(8)]

		# setup pawns
		self.board[1] = [(Figure.PAWN, Color.WHITE)] * 8
		self.board[6] = [(Figure.PAWN, Color.BLACK)] * 8

		# setup rest of the figures
		self.board[0] = self.__setup_first_row(Color.WHITE)
		self.board[7] = self.__setup_first_row(Color.BLACK)
	
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
		for row in self.board[::-1]:
			print(' ' .join(['x' if i is not None else ' ' for i in row]))
	
	def move(self, piece, _from, to):
		"""
		Move piece from "_from" coordinates to "to"
		"""
		figure, color = piece
		for c in to:
			if c not in range(8):
				raise InvalidMoveException()
		
		if figure == Figure.PAWN:
			self.move_pawn(color, _from, to)

		elif figure == Figure.ROOK:
			self.move_rook(color, _from, to)

		elif figure == Figure.KNIGHT:
			self.move_knight(color, _from, to)
		
		elif figure == Figure.BISHOP:
			self.move_bishop(color, _from, to)

		elif figure == Figure.QUEEN:
			self.move_queen(color, _from, to)

		elif figure == Figure.KING:
			self.move_king(color, _from, to)
	
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
			if (color == Color.BLACK and from_x != 6) or (color == Color.WHITE and from_x != 1):
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

	def move_rook(self, color, _from, to):

			from_x, from_y = _from
			to_x, to_y = to
			diff = (to_x - from_x, to_y - from_y)

			if 0 not in diff:
				raise InvalidMoveException()

			diff_unit_vector = (diff[0]//max(diff),diff[1]//max(diff))
			temp_from = _from

			while temp_from != to:
				temp_from = (temp_from[0]+diff_unit_vector[0], temp_from[1]+diff_unit_vector[1])
				piece = self.get_piece_at_coordinates(temp_from)
				if piece:
					if piece[1] == color:
						raise InvalidMoveException()
					else:
						#TODO
						return
			
			self.__apply_move((Figure.ROOK, color), _from, to)
			
	def __apply_move(self, piece, _from, to):
		from_x, from_y = _from
		to_x, to_y = to

		self.board[from_x][from_y] = None
		self.board[to_x][to_y] = piece


				
			

def test():
	board = ChessBoard()
	board.draw_board()
	board.move((Figure.PAWN, Color.WHITE), (1,1), (3,1))
	board.draw_board()

	board.move((Figure.PAWN, Color.WHITE), (1,0), (3,0))
	board.draw_board()

	board.move((Figure.ROOK, Color.WHITE), (0,0), (2,0))
	board.draw_board()


	
	board.move((Figure.ROOK, Color.WHITE), (2,0), (2,4))
	board.draw_board()
	

if __name__ == '__main__':
	test()
		
