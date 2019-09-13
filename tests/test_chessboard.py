import unittest

import libs.chessboard
import libs.figures

class test_chessboard(unittest.TestCase):
    @classmethod
    def create_chessboard():
        return libs.chessboard.ChessBoard()

    

if __name__ == '__main__':
    unittest.main()