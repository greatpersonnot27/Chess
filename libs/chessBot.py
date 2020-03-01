class ChessBot:
    def __init__(self):
        self.count = 0
        self.moves = ["g8f6"]

    def make_move(self, board):
        print("bestmove " + self.moves[self.count])