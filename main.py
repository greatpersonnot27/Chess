from libs.chessboard import ChessBoard
from libs.exceptions import InvalidMoveException


def main():
	board = ChessBoard()
	print(board.draw_board())

	while True:
		# coordinate parsing
		_input = input("move: ")
		if _input == "":
			print(board.draw_board())
			continue
		c = _input.split()

		# moving
		try:
			board.move_algebr(c[0], c[1])
			print(board.draw_board())
				
		except InvalidMoveException as e:
			print(e)
			continue


if __name__ == '__main__':
	main()
