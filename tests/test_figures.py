import unittest

from libs.utils import Vector2
from libs.figures import Figure
from libs.chessboard import ChessBoard

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

    def test_return_path(self):
        figure = Figure(Figure.Color.WHITE)
        # members of the path - 1. from 2. to 3. correct path
        paths = [
            (Vector2([0,0]), Vector2([0,1]), []), 
            (Vector2([0,0]), Vector2([7,0]), [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]),
            (Vector2([0,0]), Vector2([5,5]), [(1,1),(2,2),(3,3),(4,4)]),
            (Vector2([5,5]), Vector2([0,0]), [(4,4), (3,3), (2,2), (1,1)])
            ]
        [self.assertEqual(figure._return_path(path[0],path[1]), path[2]) for path in paths]

    def test_pawn(self):
        pass

    def test_knight(self):
        pass

    def test_bishop(self):
        pass

    def test_rook(self):
        pass

    def test_queen(self):
        pass

    def test_king(self):
        pass

if __name__ == '__main__':
    unittest.main()