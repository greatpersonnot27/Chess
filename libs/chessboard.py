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
        self.number_possible_moves = 0
        self.number_prunned_moves = [0, 0, 0, 0]
        self.info_count = 0

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
        utility, move = self.maximize(float("-inf"), float("inf"), self, 4, self)
        fro, to = move
        # print(self.draw_board())
        return chr(ord('a') + fro[1]) + str(int(fro[0]) + 1) + chr(ord('a') + to[1]) + str(int(to[0]) + 1)

    def __get_all_legal_moves(self):
        moves = []
        for x, row in enumerate(self.board):
            for y, figure in enumerate(row):
                if figure is not None and figure.color == self.turn:
                    moves += self.__get_figure_legal_moves(figure, (x, y))
        moves += self.__get_all_special_moves()
        return moves

    def get_all_legal_moves(self):
        moves = self.__get_all_legal_moves()
        valid_moves = []
        for move in moves:
            _from = self.board[move[0][0]][move[0][1]]
            to = self.board[move[1][0]][move[1][1]]
            board_copy = ChessBoard(self)
            board_copy.move(move[0], move[1])
            if not board_copy.is_opponent_in_check():
                valid_moves.append(move)
        # if len(valid_moves) == 0:
        #     raise Exception("Checkmate!")
        return valid_moves

    def __get_figure_legal_moves(self, figure, pos):
        moves = []

        for move_list in figure.get_all_moves(pos):
            for x, y in move_list:
                if self.board[x][y] is None:
                    if not (str(figure).endswith("Pawn") and pos[1] != y):
                        # if square is empty add to possible moves
                        moves.append((pos, (x, y)))
                    if str(figure).endswith("Pawn") and (pos[0] - x) % 2 == 0:
                        for square in figure.path(Vector2(pos), Vector2((x, y))):
                            if square is not None:
                                moves.pop()
                elif self.board[x][y].color != figure.color:
                    if not (str(figure).endswith("Pawn") and pos[1] == y):
                        # make kill
                        moves.append((pos, (x, y)))
                        break
                else:
                    break
        return moves

    def __get_all_special_moves(self):
        moves = []
        # castling
        moves += self.__check_castling()
        # impassant
        return moves

    def __check_castling(self):
        # check special moves
        moves = []
        if self.turn == Figure.Color.WHITE:
            if str(self.board[0][4]) == "White King" and not self.board[0][4].been_moved:
                if str(self.board[0][0]) == "White Rook" and not self.board[0][0].been_moved:
                    if not any(self.board[0][1:4]):
                        moves.append(((0, 4), (0, 2)))
                if str(self.board[0][7]) == "White Rook" and not self.board[0][7].been_moved:
                    if not any(self.board[0][5:7]):
                        moves.append(((0, 4), (0, 6)))
        else:
            if str(self.board[7][4]) == "Black King" and not self.board[7][4].been_moved:
                if str(self.board[7][0]) == "Black Rook" and not self.board[7][0].been_moved:
                    if not any(self.board[7][1:4]):
                        moves.append(((7, 4), (7, 2)))
                if str(self.board[7][7]) == "Black Rook" and not self.board[7][7].been_moved:
                    if not any(self.board[7][5:7]):
                        moves.append(((7, 4), (7, 6)))
        return moves

    def move(self, _from, to):
        """
        Move piece from "_from" coordinates to "to"
        """
        # print("moving")
        # check coordinate sanity
        for coordinate in list(_from) + list(to):
            if 0 > coordinate > 7:
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
        if str(figure) == "White King" and _from == (0, 4):
            if to == (0, 2):
                self.__apply_castling(figure, _from, to, "long")
                return
            if to == (0, 6):
                self.__apply_castling(figure, _from, to, "short")
                return
        if str(figure) == "Black King" and _from == (7, 4):
            if to == (7, 2):
                self.__apply_castling(figure, _from, to, "long")
                return
            if to == (7, 6):
                self.__apply_castling(figure, _from, to, "short")
                return

        # check for pawn promotion

        if isinstance(figure, Pawn) and to[0] in (0, 7):
            self.__apply_pawn_promotion(figure, _from, to, self.history[-1][-1].lower())
            return

        # Change coordinates to vector
        _from = Vector2(_from)
        to = Vector2(to)
        diff = to - _from

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
        elif str(figure).endswith("Pawn") and (abs(diff.x) == abs(diff.y) == 1):
            raise InvalidMoveException()
        else:
            self.__apply_move(figure, _from, to)

        # change turn
        self.change_turn()
        # print(self.draw_board())

    def is_opponent_in_check(self):
        return self.__is_check(opponent=True)

    def is_player_in_check(self):
        return self.__is_check()

    def __is_check(self, opponent=False):
        # change the turn
        if not opponent:
            self.change_turn()

        check = False

        moves = self.__get_all_legal_moves()
        for move in moves:
            fro, to = move
            dest_figure = self.board[to[0]][to[1]]
            if isinstance(dest_figure, King):
                check = True

        if not opponent:
            self.change_turn()

        return check

    def __apply_move(self, figure, _from, to):

        figure.been_moved = True
        _from = Vector2(_from)
        to = Vector2(to)

        self.board[_from.x][_from.y] = None
        self.board[to.x][to.y] = figure

    def __apply_castling(self, figure, _from, to, type):
        figure.been_moved = True
        _from = Vector2(_from)
        to = Vector2(to)

        self.board[_from.x][_from.y] = None
        self.board[to.x][to.y] = figure

        if type == "long":
            self.board[_from.x][3] = self.get_piece_at_coordinates((_from.x, 0))
            self.board[_from.x][0] = None
        if type == "short":
            self.board[_from.x][5] = self.get_piece_at_coordinates((_from.x, 7))
            self.board[_from.x][7] = None
        self.change_turn()

    def __apply_pawn_promotion(self, pawn, _from, to, figure):
        _from = Vector2(_from)
        to = Vector2(to)

        if figure == "q":
            self.board[_from.x][_from.y] = None
            self.board[to.x][to.y] = Queen(pawn.color)
        if figure == "b":
            self.board[_from.x][_from.y] = None
            self.board[to.x][to.y] = Bishop(pawn.color)
        if figure == "r":
            self.board[_from.x][_from.y] = None
            self.board[to.x][to.y] = Rook(pawn.color)
        if figure == "n":
            self.board[_from.x][_from.y] = None
            self.board[to.x][to.y] = Knight(pawn.color)
        self.change_turn()

    def __kill(self, fro, to):

        killer = self.board[fro[0]][fro[1]]
        killee = self.board[to[0]][to[1]]

        if killer is None or killee is None or killer.color == killee.color:
            raise RuntimeError()

        self.board[fro[0]][fro[1]] = None
        self.board[to[0]][to[1]] = killer

        self.dead_figures.append(killee)

    def maximize(self, alpha, beta, board, depth, original_board):
        original_board.number_possible_moves += 1
        if depth == 0:
            return board.evaluate_board(), None
        maximum_utility = float('-inf')
        move_with_max_utility = None

        for move in board.get_all_legal_moves():
            cb = ChessBoard(board)
            cb.move(move[0], move[1])
            utility, mv = self.minimize(alpha, beta, cb, depth - 1, original_board)
            if utility is not None:
                if utility > maximum_utility:
                    maximum_utility = utility
                    move_with_max_utility = move
                alpha = max(alpha, utility)
                if alpha >= beta:
                    original_board.number_prunned_moves[depth - 1] += 1
                    return None, None
        if depth >= 2:
            print("info: depth: " + str(depth) + " possible_moves: " + str(
                original_board.number_possible_moves) + " prunned_moves: depth 1: " + str(
                original_board.number_prunned_moves[0]) + " depth 2: " + str(
                original_board.number_prunned_moves[1]) + " depth 3: " + str(
                original_board.number_prunned_moves[2]))
        return maximum_utility, move_with_max_utility

    def minimize(self, alpha, beta, board, depth, original_board):
        original_board.number_possible_moves += 1
        if depth == 0:
            return board.evaluate_board(), None
        minimum_utility = float('inf')
        move_with_min_utility = None

        for move in board.get_all_legal_moves():
            cb = ChessBoard(board)
            cb.move(move[0], move[1])
            utility, mv = self.maximize(alpha, beta, cb, depth - 1, original_board)
            if utility is not None:
                if utility < minimum_utility:
                    minimum_utility = utility
                    move_with_min_utility = move
                beta = min(beta, utility)
                if alpha >= beta:
                    original_board.number_prunned_moves[depth - 1] += 1
                    return None, None
        if depth >= 2:
            print("info: depth: " + str(depth) + " possible_moves: " + str(
                original_board.number_possible_moves) + " prunned_moves: depth 1: " + str(
                original_board.number_prunned_moves[0]) + " depth 2: " + str(
                original_board.number_prunned_moves[1]) + " depth 3: " + str(
                original_board.number_prunned_moves[2]))
        return minimum_utility, move_with_min_utility

    def evaluate_board(self):
        """
        using simple shannon function to evaluate relative value of the board
        only the material part. Need to add double pawn and other type of metrics
        """
        figure_count = self.get_figure_count()
        position_value = 20000 * (figure_count.get("White King", 0) - figure_count.get("Black King", 0)) + 900 * (
                figure_count.get("White Queen", 0) - figure_count.get("Black Queen", 0)) + 500 * (
                                 figure_count.get("White Rook", 0) - figure_count.get("Black Rook", 0)) + 330 * (
                                 figure_count.get("White Knight", 0) - figure_count.get("Black Knight", 0) +
                                 figure_count.get("White Bishop", 0) - figure_count.get("Black Bishop", 0)) + 100 * (
                                 figure_count.get("White Pawn", 0) - figure_count.get("Black Pawn", 0))
        white_st_sum = 0
        black_st_sum = 0
        for x, row in enumerate(self.board):
            for y, figure in enumerate(row):
                if figure is not None:
                    if figure.color:
                        black_st_sum += figure.get_square_table()[x][y]
                    else:
                        white_st_sum += figure.get_square_table()[x][y]
        return (position_value + black_st_sum - white_st_sum) * -1

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

    def change_turn(self):
        self.turn = Figure.Color.WHITE if self.turn == Figure.Color.BLACK else Figure.Color.BLACK
