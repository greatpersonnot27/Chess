import unittest

from libs.utils import Vector2
from libs.figures import Figure, Queen, Knight, Bishop, Rook, Pawn, King

"""
   a   b   c   d   e   f   g   h
8  BR  BK  BB  BQ  BK  BB  BK  BR
7  BP  BP  BP  BP  BP  BP  BP  BP
6
5
4
3
2  WP  WP  WP  WP  WP  WP  WP  WP
1  WR  WK  WB  WQ  WK  WB  WK  WR

"""


class test_figures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def test_pawn_get_all_moves_startpos_white(self):
        pawn = Pawn(Figure.Color.WHITE)
        possible_positions = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 2, pos[1]), (pos[0] + 1, pos[1] + 1),
                                     (pos[0] + 1, pos[1] - 1)])

    def test_pawn_get_all_moves_startpos_edges_white(self):
        pawn = Pawn(Figure.Color.WHITE)
        possible_positions = [[1, 0], [1, 7]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            if pos[1] == 0:
                self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 2, pos[1]), (pos[0] + 1, pos[1] + 1)])
            elif pos[1] == 7:
                self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 2, pos[1]), (pos[0] + 1, pos[1] - 1)])

    def test_pawn_get_all_moves_advancedpos_white(self):
        pawn = Pawn(Figure.Color.WHITE)
        possible_positions = [[row, col] for col in range(1, 7) for row in range(2, 7)]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1),
                                     (pos[0] + 1, pos[1] - 1)])

    def test_pawn_get_all_moves_advancedpos_edges_white(self):
        pawn = Pawn(Figure.Color.WHITE)
        possible_positions = [[row, col] for row in range(2, 7) for col in [0, 7]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            if pos[1] == 0:
                self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1)])
            elif pos[1] == 7:
                self.assertEqual(moves, [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] - 1)])

    def test_pawn_get_all_moves_endpos_white(self):
        pawn = Pawn(Figure.Color.WHITE)
        possible_positions = [[7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [])

    def test_pawn_get_all_moves_startpos_black(self):
        pawn = Pawn(Figure.Color.BLACK)
        possible_positions = [[6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 2, pos[1]), (pos[0] - 1, pos[1] + 1),
                                     (pos[0] - 1, pos[1] - 1)])

    def test_pawn_get_all_moves_startpos_edges_black(self):
        pawn = Pawn(Figure.Color.BLACK)
        possible_positions = [[6, 0], [6, 7]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            if pos[1] == 0:
                self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 2, pos[1]), (pos[0] - 1, pos[1] + 1)])
            elif pos[1] == 7:
                self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 2, pos[1]), (pos[0] - 1, pos[1] - 1)])

    def test_pawn_get_all_moves_advancedpos_black(self):
        pawn = Pawn(Figure.Color.BLACK)
        possible_positions = [[row, col] for col in range(1, 7) for row in range(5, 0)]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] + 1),
                                     (pos[0] - 1, pos[1] - 1)])

    def test_pawn_get_all_moves_advancedpos_edges_black(self):
        pawn = Pawn(Figure.Color.BLACK)
        possible_positions = [[row, col] for row in range(5, 0) for col in [0, 7]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            if pos[1] == 0:
                self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] + 1)])
            elif pos[1] == 7:
                self.assertEqual(moves, [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] - 1)])


    def test_pawn_get_all_moves_endpos_black(self):
        pawn = Pawn(Figure.Color.BLACK)
        possible_positions = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6]]
        for pos in possible_positions:
            moves = pawn.get_all_moves(pos)
            self.assertEqual(moves, [])

if __name__ == '__main__':
    unittest.main()
