import queue
import sys
from libs.chessboard import ChessBoard
from libs.exceptions import InvalidMoveException
from libs.engineOptions import EngineOptions


class GameEngine:
    def __init__(self):
        self.board = None
        self.options = EngineOptions()

    def engine_loop(self):

        while True:
            # Check input from GUI
            _input = input()
            if _input == "uci":
                self.initialize()

            elif _input == "isready":
                print("readyok")

            elif _input.startswith("setoption"):
                self.options.set_option(_input)

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
        self.board.evaluate_board()
        moves = position.split()[3:]
        for move in moves:
            fro = (int(move[:2][1]) - 1, ord(move[:2][0].lower()) - ord('a'))
            to = (int(move[2:4][1]) - 1, ord(move[2:4][0].lower()) - ord('a'))
            self.board.move(fro, to)

        # all_moves = self.board.get_all_possible_moves()
        # for _from, to in all_moves:
        #    print(str(self.board.board[_from[0]][_from[1]]), to)

    def handle_go(self, go):
        if self.board is not None:
            print('bestmove ' + self.board.get_minmax_move())

    def handle_stop(self):
        raise NotImplementedError

    def initialize(self):
        print("id name AIengine")
        print("id author ika&shota")
        self.options.send_available_options()
        print("uciok")
        sys.stdout.flush()


if __name__ == '__main__':
    engine = GameEngine()
    engine.engine_loop()
