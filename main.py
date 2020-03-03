from libs.chessBot import ChessBot
from libs.chessboard import ChessBoard
from libs.exceptions import InvalidMoveException


def main():
	board = ChessBoard()
	bot = ChessBot()
	board_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

	while True:
		# coordinate parsing
		_input = input()
		if _input == "":
			continue
		if _input == "uci":
			print("id name AIengine")
			print("id author ika&shota")
			print("uciok")
		if _input =="isready":
			print("readyok")
		if _input == "ucinewgame":
			board = ChessBoard()
		if _input.startswith("position"):
			c = _input.split()
			c = c[-1]
			try:
				board.move_algebra(c[:2], c[2:4])
				bot.make_move(board)

			except InvalidMoveException as e:
				print(e)
				continue
		if _input == "quit":
			exit()


if __name__ == '__main__':
	main()
