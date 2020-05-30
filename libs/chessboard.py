import random
import copy
from libs.exceptions import InvalidMoveException, CheckMateException, StalemateException
from libs.utils import Vector2
from libs.figures import (
    Figure, Pawn, Knight, Bishop, Rook, Queen, King
)


class ChessBoard:
    """
    This is a class containing the chessboard state,
    with methods for validating and generating possible moves

    Attributes
    ----------
    turn : Figure.Color

        the color of the player whose turn it is to make a move

    history: list

        list of made moves (two tuples of two integers each)

    dead_figures: list

        list of figures that were killed

    number_possible_moves: int

        total possible moves for the given depth

    number_prunned_moves: int

        number of moves prunned as a result of alpha-beta prunning
    """
    def __init__(self, chessboard=None):
        """
        Constructs a new chessboard of chessboard parameter is none
        , else creates an new chessboard from it

        Parameters
        ----------
            chessboard: ChessBoard

                instance of Chessboard object with possibly some
                registered activity
        """
        # current turn
        self.turn = Figure.Color.WHITE

        self.white_king_pos = Vector2((0, 4))
        self.black_king_pos = Vector2((7, 4))

        self.white_in_check = False
        self.black_in_check = False

        self.depth = 4
        # Game history
        self.history = []
        self.dead_figures = []
        self.number_possible_moves = 0
        self.number_prunned_moves = [0, 0, 0, 0, 0, 0]
        self.info_count = 0

        if chessboard is not None:
            self.board = copy.copy(chessboard.board)
            self.turn = chessboard.turn
            self.white_king_pos = chessboard.white_king_pos
            self.black_king_pos = chessboard.black_king_pos
        else:
            self.__setup_initial_board()

    def __setup_first_row(self, color):
        """Receives the color attribute and Sets up a list of Figures on the first row, returns the list"""
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
        """Populates the chessboard (list of lists) with figures"""
        self.board = self.__setup_first_row(Figure.Color.WHITE)
        self.board += [Pawn(Figure.Color.WHITE) for i in range(8)]
        self.board += [None] * 32
        self.board += [Pawn(Figure.Color.BLACK) for i in range(8)]
        self.board += self.__setup_first_row(Figure.Color.BLACK)

    def get_piece_at(self, coordinates):
        """
        Get piece on given coordinates. If the coordinates is empty

            Parameters:

                coordinates (tuple): tuple of integers

            Returns:

                (Figure) : Figure contained at the given coordinates
        """
        x, y = coordinates
        if isinstance(y, slice):
            return self.board[x * 8 + y.start : x * 8 + y.stop]
        return self.board[x * 8 + y]

    def set_piece_at(self, coordinates, value):
        x, y = coordinates
        self.board[x * 8 + y] = value

    def get_minmax_move(self):
        """
        Returns next move calculated with minmax algorithm

            Returns:

                str: move in long algebraic notation. Example: C7C2
        """
        utility, move = self.maximize(float("-inf"), float("inf"), self, self.depth, self)
        fro, to = move
        # print(self.draw_board())
        print(chr(ord('a') + fro[1]) + str(int(fro[0]) + 1) + chr(ord('a') + to[1]) + str(int(to[0]) + 1))
        return chr(ord('a') + fro[1]) + str(int(fro[0]) + 1) + chr(ord('a') + to[1]) + str(int(to[0]) + 1)

    def __get_all_legal_moves(self):
        """
        Returns all legal moves as a list of tuples for the current
        position

            Returns:

                moves (list): list of tuples containing 2 integers
                each. Example: [((0, 1),(0, 2)),((0, 4),(0, 6))]
        """
        moves = []
        for x, y, figure in self.get_all_figures():
            if figure is not None and figure.color == self.turn:
                moves += self.__get_figure_legal_moves(figure, (x, y))
        moves += self.__get_all_special_moves()
        return moves

    def get_all_figures(self):
        for k, figure in enumerate(self.board):
            x = k//8
            y = k%8
            yield x, y, figure

    def get_all_legal_moves(self):

        moves = self.__get_all_legal_moves()
        valid_moves = []
        for move in moves:

            board_copy = ChessBoard(self)
            board_copy.move(move[0], move[1])

            move_v2 = Vector2(move[0])
            king_pos = self.white_king_pos if self.turn == Figure.Color.WHITE else self.black_king_pos
            direction_vector = abs(move_v2 - king_pos)
            normal_vector = Vector2((1, 1)) if direction_vector.x == 0 and direction_vector.y == 0 else direction_vector / max(abs(direction_vector.x), abs(direction_vector.y))
            if (normal_vector.x, normal_vector.y) in [(1, 1), (0, 1), (1, 0)]:
                if not board_copy.is_opponent_in_check():
                    valid_moves.append(move)
            else:
                valid_moves.append(move)
        if len(valid_moves) == 0:
            if self.__is_check():
                raise CheckMateException("Checkmate!")
            raise StalemateException("Stalemate!")
        return valid_moves

    def __get_figure_legal_moves(self, figure, pos):
        """
        Returns all legal moves for a given figure in a given
        position

            Parameters:

                figure (Figure): object of type Figure

                pos (tuple): tuple of two integers

            Returns:

                moves (list): list of two tuples each with two
                integers
        """
        moves = []

        for move_list in figure.get_all_moves(pos):
            for x, y in move_list:
                if self.get_piece_at((x, y)) is None:
                    if not (str(figure).endswith("Pawn") and pos[1] != y):
                        # if square is empty add to possible moves
                        moves.append((pos, (x, y)))
                    if str(figure).endswith("Pawn") and (pos[0] - x) % 2 == 0:
                        for square in figure.path(Vector2(pos), Vector2((x, y))):
                            if self.get_piece_at((square[0], square[1])) is not None:
                                moves.pop()
                elif self.get_piece_at((x, y)).color != figure.color:
                    if not (str(figure).endswith("Pawn") and pos[1] == y):
                        # make kill
                        moves.append((pos, (x, y)))
                        break
                else:
                    break
        return moves

    def __get_all_special_moves(self):
        """
        Returns special type of moves like castling or impassant

            Returns:

                moves (list): list of two tuples each with two integers
        """
        moves = []
        # castling
        moves += self.__check_castling()
        # impassant
        return moves

    def __check_castling(self):
        """
        Returns available castling moves

            Returns:

                moves (list): list of two tuples each with two integers
        """
        # check special moves
        moves = []
        if self.turn == Figure.Color.WHITE:
            if str(self.get_piece_at((0, 4))) == "White King" and not self.get_piece_at((0, 4)).been_moved:
                if str(self.get_piece_at((0, 0))) == "White Rook" and not self.get_piece_at((0, 0)).been_moved:
                    if not any(self.get_piece_at((0, slice(1,4)))):
                        moves.append(((0, 4), (0, 2)))
                if str(self.get_piece_at((0, 7))) == "White Rook" and not self.get_piece_at((0, 7)).been_moved:
                    if not any(self.get_piece_at((0, slice(5,7)))):
                        moves.append(((0, 4), (0, 6)))
        else:
            if str(self.get_piece_at((7, 4))) == "Black King" and not self.get_piece_at((7, 4)).been_moved:
                if str(self.get_piece_at((7, 0))) == "Black Rook" and not self.get_piece_at((7, 0)).been_moved:
                    if not any(self.get_piece_at((7, slice(1, 4)))):
                        moves.append(((7, 4), (7, 2)))
                if str(self.get_piece_at((7, 7))) == "Black Rook" and not self.get_piece_at((7, 7)).been_moved:
                    if not any(self.get_piece_at((7, slice(5, 7)))):
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

        figure = self.get_piece_at(_from)

        # figure is on right position
        if figure is None:
            raise InvalidMoveException()

        # not the turn of the current player
        if figure.color != self.turn:
            raise InvalidMoveException("Not your turn")

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
            self.__apply_pawn_promotion(figure, _from, to, "q")
            return

        # Change coordinates to vector
        _from = Vector2(_from)
        to = Vector2(to)
        diff = to - _from

        # handle the path
        for square in figure.path(_from, to):

            # if something stands in the path raise Exception
            if self.get_piece_at(square) is not None:
                raise InvalidMoveException()

        # handle destination square
        dest = self.get_piece_at(to)
        if dest is not None:
            if dest.color == figure.color:
                raise InvalidMoveException()
            else:
                self.__kill(_from, to)
        elif str(figure).endswith("Pawn") and (abs(diff.x) == abs(diff.y) == 1):
            raise InvalidMoveException()
        else:
            self.__apply_move(figure, _from, to)

        if isinstance(figure, King):
            if figure.color == Figure.Color.WHITE:
                self.white_king_pos = to
            else:
                self.black_king_pos = to

        # change turn
        self.change_turn()
        # print(self.draw_board())

    def is_opponent_in_check(self):
        """
        Returns true if opponent is in check else returns false

            Returns:

                check (bool)
        """
        return self.__is_check(opponent=True)

    def is_player_in_check(self):
        """
        Returns true if player is in check else returns false

            Returns:

                check (bool)
        """
        return self.__is_check()

    def __is_check(self, opponent=False):
        """
        Checks if player or opponent is in check

            Parameters:

                opponent (bool): true if the function should check
                for the opponent else false

            Returns:

                check (bool)
        """
        # change the turn
        if not opponent:
            self.change_turn()

        check = False

        moves = self.__get_all_legal_moves()
        for move in moves:
            fro, to = move
            dest_figure = self.get_piece_at((to[0], to[1]))
            if isinstance(dest_figure, King):
                check = True

        if not opponent:
            self.change_turn()

        return check

    def __apply_move(self, figure, _from, to):
        """
        Makes the move on the board object and sets the been_moved
        flag to true for a figure being moved

            Parameters:

                figure (Figure): figure that needs to be moved

                _from (tuple): tuple of two integers describing
                from which place the piece is being moved

                _to (tuple): tuple of two integers describing to
                which place the piece is being moved
        """

        figure.been_moved = True
        _from = Vector2(_from)
        to = Vector2(to)

        self.set_piece_at((_from.x, _from.y), None)
        self.set_piece_at((to.x, to.y), figure)

    def __apply_castling(self, figure, _from, to, type):
        """
        Makes the castling move on the board object and sets the
        been_moved flag to true for a figure being moved

            Parameters:

                figure (Figure): figure that needs to be moved

                _from (tuple): tuple of two integers describing
                from which place the piece is being moved

                _to (tuple): tuple of two integers describing to
                which place the piece is being moved

                type (str): "long" or "short" depending which type
                of castling is being applied
        """
        figure.been_moved = True
        _from = Vector2(_from)
        to = Vector2(to)

        if figure.color == Figure.Color.WHITE:
            self.white_king_pos = to
        else:
            self.black_king_pos = to

        self.set_piece_at((_from.x, _from.y), None)
        self.set_piece_at((to.x, to.y), figure)

        if type == "long":
            self.set_piece_at((_from.x, 3), self.get_piece_at((_from.x, 0)))
            self.set_piece_at((_from.x, 0), None)
        if type == "short":
            self.set_piece_at((_from.x, 5), self.get_piece_at((_from.x, 7)))
            self.set_piece_at((_from.x, 7), None)
        self.change_turn()

    def __apply_pawn_promotion(self, pawn, _from, to, figure):
        """
        Applies the promotion rule to the given pawn with
        the chosen figure

            Parameters:

                pawn (Figure): pawn that needs to be moved

                _from (tuple): tuple of two integers describing
                from which place the piece is being moved

                _to (tuple): tuple of two integers describing to
                which place the piece is being moved

                figure (figure): "long" or "short" depending which
                type of castling is being applied
        """
        _from = Vector2(_from)
        to = Vector2(to)

        if figure == "q":
            self.set_piece_at((_from.x, _from.y), None)
            self.set_piece_at((to.x, to.y), Queen(pawn.color))
        if figure == "b":
            self.set_piece_at((_from.x, _from.y), None)
            self.set_piece_at((to.x, to.y), Bishop(pawn.color))
        if figure == "r":
            self.set_piece_at((_from.x, _from.y), None)
            self.set_piece_at((to.x, to.y), Rook(pawn.color))
        if figure == "n":
            self.set_piece_at((_from.x, _from.y), None)
            self.set_piece_at((to.x, to.y), Knight(pawn.color))
        self.change_turn()

    def __kill(self, fro, to):
        """
        Removes the killed figure from the board object and
        replaces it with the killer figure

            Parameters:

                fro (tuple): tuple of two integers -
                coordinates of the killer

                to (tuple): tuple of two integers -
                coordinates of the killee
        """
        killer = self.get_piece_at((fro[0], fro[1]))
        killee = self.get_piece_at((to[0], to[1]))

        if killer is None or killee is None or killer.color == killee.color:
            raise RuntimeError()

        self.set_piece_at((fro[0], fro[1]), None)
        self.set_piece_at((to[0], to[1]), killer)

        self.dead_figures.append(killee)

    def maximize(self, alpha, beta, board, depth, original_board):
        """
        Returns the value of the maximum utility and
        the corresponding move

            Parameters:

                alpha (float): maximizing functions best
                utility value for the current depth or above

                beta (float): minimizing functions best
                utility value for the current depth or above

                board (ChessBoard): board to be copied

                depth (str): the depth limit for the
                recursive call of the function

                original_board (ChessBoard): the original Chessboard object

            Returns:

                maximum_utility (float): value of the
                maximum utility generated

                move_with_max_utility (tuple): tuple of
                two tuples each with two integers describing the move
        """
        original_board.number_possible_moves += 1
        if depth == 0:
            return board.evaluate_board(), None
        maximum_utility = float('-inf')
        move_with_max_utility = None
        try:
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
        except (CheckMateException, StalemateException) as e:
            if depth != self.depth:
                return -50000, None
            else:
                if isinstance(e, CheckMateException):
                    print("info: Game Lost")
                else:
                    print("info: Stalemate!")
                exit()
        # if depth >= 5:
        #     print("info: depth: " + str(depth) + " possible_moves: " + str(
        #         original_board.number_possible_moves) + " prunned_moves: depth 1: " + str(
        #         original_board.number_prunned_moves[0]) + " depth 2: " + str(
        #         original_board.number_prunned_moves[1]) + " depth 3: " + str(
        #         original_board.number_prunned_moves[2]))
        return maximum_utility, move_with_max_utility

    def minimize(self, alpha, beta, board, depth, original_board):
        """
        Returns the value of the minimum utility and
        the corresponding move

            Parameters:

                alpha (float): maximizing functions best
                utility value for the current depth or above

                beta (float): minimizing functions best
                utility value for the current depth or above

                board (ChessBoard): board to be copied

                depth (str): the depth limit for the
                recursive call of the function

                original_board (ChessBoard): the
                original Chessboard object

            Returns:

                minimum_utility (float): value of the minimum utility
                generated

                move_with_min_utility (tuple): tuple of two
                tuples each with two integers describing the move
        """
        original_board.number_possible_moves += 1
        if depth == 0:
            return board.evaluate_board(), None
        minimum_utility = float('inf')
        move_with_min_utility = None
        try:
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
        except CheckMateException as e:
            return 50000, None
        except StalemateException as e:
            return 39000, None
        # if depth >= 2:
        #     print("info: depth: " + str(depth) + " possible_moves: " + str(
        #         original_board.number_possible_moves) + " prunned_moves: depth 1: " + str(
        #         original_board.number_prunned_moves[0]) + " depth 2: " + str(
        #         original_board.number_prunned_moves[1]) + " depth 3: " + str(
        #         original_board.number_prunned_moves[2]))
        return minimum_utility, move_with_min_utility

    def evaluate_board(self):
        """
        Returns the value evaluating the advantageous position
        using simple shannon function

        to evaluate relative value of the board - the material
        part plus the positional values

            Returns:

                (int): value of the evaluated board
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
        for x, y, figure in self.get_all_figures():
            if figure is not None:
                if figure.color:
                    black_st_sum += figure.get_square_table()[x][y]
                else:
                    white_st_sum += figure.get_square_table()[x][y]
        return (position_value + black_st_sum - white_st_sum) * -1

    def get_figure_count(self):
        """
        Returns the dictionary with Figures as keys and
        number of the contained in the ChessBoard object as values

            Returns:

                figure_count (dictionary): key - Figure,
                value - # of that figure on the Board
        """
        figure_count = dict()

        for x,y,figure in self.get_all_figures():
            if figure is not None:
                if str(figure) in figure_count.keys():
                    figure_count[str(figure)] += 1
                else:
                    figure_count[str(figure)] = 1
        return figure_count

    def change_turn(self):
        """Flips the turn attribute (when the current player makes the move)"""
        self.turn = Figure.Color.WHITE if self.turn == Figure.Color.BLACK else Figure.Color.BLACK
