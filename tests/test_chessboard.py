import unittest

from libs.chessboard import ChessBoard

class test_chessboard(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def test_evaluation_start_position(self):
        board = ChessBoard()

        self.assertEqual(board.evaluate_board(), 0)

    def test_evaluation_queen_killed_start_pos(self):

        board = ChessBoard()
        board.set_piece_at((0,3), None)

        self.assertEqual(board.evaluate_board(), 895)

    def test_minmax_move(self):
        position = "position startpos moves e2e4"
        board = ChessBoard()
        board.evaluate_board()
        moves = position.split()[3:]
        for move in moves:
            fro = (int(move[:2][1]) - 1, ord(move[:2][0].lower()) - ord('a'))
            to = (int(move[2:4][1]) - 1, ord(move[2:4][0].lower()) - ord('a'))
            board.move(fro, to)

        self.assertEqual("b8c6", board.get_minmax_move())

    def test_get_all_figures_basic(self):
        figures = [(0, 0, 'White Rook'), (0, 1, 'White Knight'), (0, 2, 'White Bishop'), (0, 3, 'White Queen'),
                   (0, 4, 'White King'), (0, 5, 'White Bishop'), (0, 6, 'White Knight'), (0, 7, 'White Rook'),
                   (1, 0, 'White Pawn'), (1, 1, 'White Pawn'), (1, 2, 'White Pawn'), (1, 3, 'White Pawn'),
                   (1, 4, 'White Pawn'), (1, 5, 'White Pawn'), (1, 6, 'White Pawn'), (1, 7, 'White Pawn'),
                   (2, 0, 'None'), (2, 1, 'None'), (2, 2, 'None'), (2, 3, 'None'), (2, 4, 'None'), (2, 5, 'None'),
                   (2, 6, 'None'), (2, 7, 'None'), (3, 0, 'None'), (3, 1, 'None'), (3, 2, 'None'), (3, 3, 'None'),
                   (3, 4, 'None'), (3, 5, 'None'), (3, 6, 'None'), (3, 7, 'None'), (4, 0, 'None'), (4, 1, 'None'),
                   (4, 2, 'None'), (4, 3, 'None'), (4, 4, 'None'), (4, 5, 'None'), (4, 6, 'None'), (4, 7, 'None'),
                   (5, 0, 'None'), (5, 1, 'None'), (5, 2, 'None'), (5, 3, 'None'), (5, 4, 'None'), (5, 5, 'None'),
                   (5, 6, 'None'), (5, 7, 'None'), (6, 0, 'Black Pawn'), (6, 1, 'Black Pawn'), (6, 2, 'Black Pawn'),
                   (6, 3, 'Black Pawn'), (6, 4, 'Black Pawn'), (6, 5, 'Black Pawn'), (6, 6, 'Black Pawn'),
                   (6, 7, 'Black Pawn'), (7, 0, 'Black Rook'), (7, 1, 'Black Knight'), (7, 2, 'Black Bishop'),
                   (7, 3, 'Black Queen'), (7, 4, 'Black King'), (7, 5, 'Black Bishop'), (7, 6, 'Black Knight'),
                   (7, 7, 'Black Rook')]
        board = ChessBoard()
        self.assertEqual(figures, [ (i[0], i[1], str(i[2])) for i in board.get_all_figures()])

if __name__ == '__main__':
    unittest.main()