import queue
import sys
from libs.chessboard import ChessBoard
from libs.exceptions import InvalidMoveException


class GameEngine:
    def __init__(self):
        self.board = None
        self.options = {}

    def engine_loop(self):
        self.initialize()

        while True:
            # Check input from GUI
            _input = input()
            if _input == "isready":
                print("readyok")

            elif _input.startswith("position"):
                self.handle_position(_input)

            elif _input.startswith("go"):
                self.handle_go(_input)
            
            elif _input == "stop":
                self.handle_stop()

            elif _input == "quit":
                exit()

    def handle_position(self, position):
        self.board = ChessBoard()
        moves = position.split()[3:]
        for move in moves:
            self.board.move_algebra(move[:2], move[2:4])
        print(self.board.draw_board())

    def handle_go(self, go):
        if self.board is not None:
            self.board.next_move_ai()

    def handle_stop(self):
        raise NotImplementedError

    def initialize(self):
        if input() == 'uci':
            print("id name AIengine")
            print("id author ika&shota")
            print("uciok")
            sys.stdout.flush()
        else:
            exit(1)


if __name__ == '__main__':
    engine = GameEngine()
    engine.engine_loop()
