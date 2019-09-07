from libs.chessboard import ChessBoard


def main():
	board = ChessBoard()
	print(board.draw_board())
	board.move((1,1), (3,1))
	print(board.draw_board())
	board.move((0,1), (2,0))
	print(board.draw_board())


if __name__ == '__main__':
	main()
