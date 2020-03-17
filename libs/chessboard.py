import random
import copy
from libs.exceptions import InvalidMoveException
from libs.utils import Vector2
from libs.figures import (
    Figure, Pawn, Knight, Bishop, Rook, Queen, King
)


class ChessBoard:

    def __init__(self, chessboard=None):

        # current turn
        self.turn = Figure.Color.WHITE

        # Game history
        self.history = []
        self.dead_figures = []

        if chessboard is not None:
            self.board = copy.deepcopy(chessboard.board)
            self.turn = chessboard.turn
        else:
            self.__setup_initial_board()

    def __setup_first_row(self, color):
        row = [None] * 8
        row[0] = Rook(color)
        row[1] = Knight(color)
        row[2] = Bishop(color)
        row[3] = Queen(color)
        row[4] = King(color)
        row[5] = Bishop(color)
        row[6] = Knight(color)
        row[7] = Rook(color)
        return row

    def __setup_initial_board(self):
        self.board = [[None] * 8 for i in range(8)]

        # setup pawns
        self.board[1] = [Pawn(Figure.Color.WHITE) for i in range(8)]
        self.board[6] = [Pawn(Figure.Color.BLACK) for i in range(8)]

        # setup rest of the figures
        self.board[0] = self.__setup_first_row(Figure.Color.WHITE)
        self.board[7] = self.__setup_first_row(Figure.Color.BLACK)

    def get_piece_at_coordinates(self, coordinates):
        """
        Get piece on given coordinates. If the coordinates is empty
        return None
        """
        x, y = coordinates
        return self.board[x][y]

    def draw_board(self):
        board = ['   ' + ('   ').join('ABCDEFGH')]

        for i, row in enumerate(self.board[::-1]):
            row_content = [str(8 - i)]
            for square in row:
                if square is None:
                    row_content.append('  ')
                else:
                    name = str(square)
                    initials = ''.join([w[0] for w in name.split()])
                    row_content.append(initials)
            board.append('  '.join(row_content))
        return '\n'.join(board) + '\n'

    def get_random_move(self):
        move = random.choice(self.get_all_legal_moves())
        fro, to = move
        return chr(ord('a') + fro[1]) + str(int(fro[0]) + 1) + chr(ord('a') + to[1]) + str(int(to[0]) + 1)

    def get_minmax_move(self):
        utility, move = self.maximize(self, 3)
        fro, to = move
        return chr(ord('a') + fro[1]) + str(int(fro[0]) + 1) + chr(ord('a') + to[1]) + str(int(to[0]) + 1)

    def get_all_legal_moves(self):
        moves = []
        for x, row in enumerate(self.board):
            for y, figure in enumerate(row):
                if figure is not None and figure.color == self.turn:
                    moves += self.__get_figure_legal_moves(figure, (x, y))
        moves += self.__get_all_special_moves()
        return moves

    def __get_figure_legal_moves(self, figure, pos):
        moves = []

        for move_list in figure.get_all_moves(pos):
            for x, y in move_list:
                if self.board[x][y] is None:
                    # if square is empty add to possible moves
                    moves.append((pos, (x, y)))
                elif not isinstance(figure, Pawn) and self.board[x][y].color != figure.color:
                    # make kill
                    moves.append((pos, (x, y)))
                    break
                else:
                    break
        return moves

    def __get_all_special_moves(self):
        # get pawn kills
        # check special moves
        return []

    def move(self, _from, to):
        """
        Move piece from "_from" coordinates to "to"
        """
        # print("moving")
        # check coordinate sanity
        for coordinate in list(_from) + list(to):
            if 0 > coordinate > 8:
                raise InvalidMoveException()

        figure = self.get_piece_at_coordinates(_from)

        # figure is on right position
        if figure is None:
            raise InvalidMoveException()

        # not the turn of the current player
        if figure.color != self.turn:
            raise InvalidMoveException("Not your turn")

        # TODO -
        # check special moves like pawn promotion, castling, etc..
        # else: continue usual process

        # Change coordinates to vector
        _from = Vector2(_from)
        to = Vector2(to)

        # handle the path
        for square in figure.path(_from, to):

            # if something stands in the path raise Exception
            if self.get_piece_at_coordinates(square) is not None:
                raise InvalidMoveException()

        # handle destination square
        dest = self.get_piece_at_coordinates(to)
        if dest is not None:
            if dest.color == figure.color:
                raise InvalidMoveException()
            else:
                self.__kill(_from, to)
        else:
            self.__apply_move(figure, _from, to)

        # change turn
        self.turn = Figure.Color.WHITE if self.turn == Figure.Color.BLACK else Figure.Color.BLACK

    def __apply_move(self, figure, _from, to):

        _from = Vector2(_from)
        to = Vector2(to)

        self.board[_from.x][_from.y] = None
        self.board[to.x][to.y] = figure

    def __kill(self, fro, to):

        killer = self.board[fro[0]][fro[1]]
        killee = self.board[to[0]][to[1]]

        if killer is None or killee is None or killer.color == killee.color:
            raise RuntimeError()

        self.board[fro[0]][fro[1]] = None
        self.board[to[0]][to[1]] = killer

        self.dead_figures.append(killee)

    def maximize(self, board, depth):
        if depth == 0:
            return board.evaluate_board(), None
        maximum_utility = float('-inf')
        move_with_max_utility = None

        for move in board.get_all_legal_moves():
            cb = ChessBoard(board)
            cb.move(move[0], move[1])
            utility, mv = self.minimize(cb, depth - 1)
            if utility > maximum_utility:
                maximum_utility = utility
                move_with_max_utility = move
        return maximum_utility, move_with_max_utility

    def minimize(self, board, depth):
        if depth == 0:
            return board.evaluate_board(), None
        minimum_utility = float('inf')
        move_with_min_utility = None

        for move in board.get_all_legal_moves():
            cb = ChessBoard(board)
            cb.move(move[0], move[1])
            utility, mv = self.maximize(cb, depth - 1)
            if utility < minimum_utility:
                minimum_utility = utility
                move_with_min_utility = move
        return minimum_utility, move_with_min_utility

    def evaluate_board(self):
        """
        using simple shannon function to evaluate relative value of the board
        only the material part. Need to add double pawn and other type of metrics
        """
        figure_count = self.get_figure_count()
        position_value = 200 * (figure_count.get("White King", 0) - figure_count.get("Black King", 0)) + 9 * (
                figure_count.get("White Queen", 0) - figure_count.get("Black Queen", 0)) + 5 * (
                                 figure_count.get("White Rook", 0) - figure_count.get("Black Rook", 0)) + 3 * (
                                 figure_count.get("White Knight", 0) - figure_count.get("Black Knight", 0) +
                                 figure_count.get("White Bishop", 0) - figure_count.get("Black Bishop", 0)) + 1 * (
                                 figure_count.get("White Pawn", 0) - figure_count.get("Black Pawn", 0))

        return position_value * -1

    def get_figure_count(self):
        figure_count = dict()
        for row in self.board:
            for figure in row:
                if figure is not None:
                    if str(figure) in figure_count.keys():
                        figure_count[str(figure)] += 1
                    else:
                        figure_count[str(figure)] = 1
        return figure_count
