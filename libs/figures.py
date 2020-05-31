from libs.exceptions import InvalidMoveException


class Figure:
    """
        This is a class for figures on the board. It stores the color of the figure
        and returns its possible moves and paths it needs to take.

        Attributes:

            color (Color): if white it is 0, else it is 1.

            been_moved (bool): True if figure has been moved before, else False

            square_table_reversed (list): list of integer lists (reversed)

        """
    class Color:
        WHITE = 0
        BLACK = 1

    def __init__(self, color):
        """
        Constructs a figure with give color

        Parameters
        ----------

            color (Color):

                color of the figure
        """
        self.color = color
        self.been_moved = False
        self.square_table_reversed = self.square_table[::-1]

    def __str__(self):
        """
        Returns White if figure is white else Black

            Returns:

                str: White or Black

        """
        color = "White" if self.color == Figure.Color.WHITE else "Black"
        return color + ' ' + self.__class__.__name__

    def get_square_table(self):
        """
        Returns the Square table of the figure

            Returns:

                (list): list of integer lists

        """
        if self.color == Figure.Color.WHITE:
            return self.square_table_reversed
        return self.square_table

    def _return_path(self, fro, to):
        """
        Returns a list of squares on the board that a figure needs to pass
        to get to its destination

            Returns:

                path (list): list of tuples of two integers

        """
        diff = to - fro

        # abs to make sure we don't change the sign
        normal_vector = diff // max(abs(diff.x), abs(diff.y))

        path = []
        fro += normal_vector

        while fro != to:
            path.append(fro)
            fro += normal_vector

        return path

    def path(self, fro, to):
        raise NotImplementedError()

    def get_all_moves(self, position):
        raise NotImplementedError

    def _get_all_moves_jumpers(self, pos, vectors):
        """
        This method is used to get all the moves of Knight and King.
        Knight and King are called jumpers, because they can only jump one vector.

            Returns:

                moves (list): list of tuples of tuples containing two integers describing the move
        """
        moves = []

        for x, y in vectors:
            move = (pos[0] + x, pos[1] + y)
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                moves.append([move])

        return moves

    def _get_all_moves_sliders(self, pos, vectors):
        """
        This method is used to get all the moves of Queen, Bishop and Rook.
        Queen, Bishop and Rook are sliders, because they slide towards the vector direction.

            Returns:

                moves (list): list of tuples of tuples containing two integers describing the move
        """
        moves = []

        for x, y in vectors:
            move_list = []
            move = (pos[0] + x, pos[1] + y)
            while 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                move_list.append(move)
                move = (move[0] + x, move[1] + y)
            if move_list:
                moves.append(move_list)

        return moves


class Pawn(Figure):
    """
       A class for the Pawn inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [50, 50, 50, 50, 50, 50, 50, 50],
                             [10, 10, 20, 30, 30, 20, 10, 10],
                             [5, 5, 10, 25, 25, 10, 5, 5],
                             [0, 0, 0, 20, 20, 0, 0, 0],
                             [5, -5, -10, 0, 0, -10, -5, 5],
                             [5, 10, 10, -20, -20, 10, 10, 5],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the pawn for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        if pos[0] in (0, 7):
            return []
        if self.color == Figure.Color.WHITE:
            moves = [(pos[0] + 1, pos[1]), (pos[0] + 2, pos[1])]
            kill_move1 = (pos[0] + 1, pos[1] + 1)
            kill_move2 = (pos[0] + 1, pos[1] - 1)
            valid_kill_moves = list()
            if pos[1] == 0:
                valid_kill_moves.append(kill_move1)
            elif pos[1] == 7:
                valid_kill_moves.append(kill_move2)
            else:
                valid_kill_moves.append(kill_move1)
                valid_kill_moves.append(kill_move2)
            if pos[0] != 1:
                moves.pop()
            return [moves] + [valid_kill_moves]
        elif self.color == Figure.Color.BLACK:
            moves = [(pos[0] - 1, pos[1]), (pos[0] - 2, pos[1])]
            kill_move1 = (pos[0] - 1, pos[1] + 1)
            kill_move2 = (pos[0] - 1, pos[1] - 1)
            valid_kill_moves = list()
            if pos[1] == 0:
                valid_kill_moves.append(kill_move1)
            elif pos[1] == 7:
                valid_kill_moves.append(kill_move2)
            else:
                valid_kill_moves.append(kill_move1)
                valid_kill_moves.append(kill_move2)
            if pos[0] != 6:
                moves.pop()
            return [moves] + [valid_kill_moves]

    def path(self, fro, to):
        """
        Returns list of squares on the table Pawn needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        diff = to - fro

        if self.color == Figure.Color.WHITE:
            valid_moves = ((1, 0), (2, 0), (1, 1), (1, -1))

        else:
            valid_moves = ((-1, 0), (-2, 0), (-1, 1), (-1, -1))

        if tuple(diff) not in valid_moves:
            raise InvalidMoveException()

        if diff == (2, 0) or diff == (-2, 0):
            # check the inital positions if pawn moves over two squares
            if self.color == Figure.Color.WHITE and fro.x != 1:
                raise InvalidMoveException()

            elif self.color == Figure.Color.BLACK and fro.x != 6:
                raise InvalidMoveException()

            return [fro + (diff // 2)]
        # else there is no square in the path
        return []


class Knight(Figure):
    """
       A class for the Knight inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[-50, -40, -30, -30, -30, -30, -40, -50],
                             [-40, -20, 0, 0, 0, 0, -20, -40],
                             [-30, 0, 10, 15, 15, 10, 0, -30],
                             [-30, 5, 15, 20, 20, 15, 5, -30],
                             [-30, 0, 15, 20, 20, 15, 0, -30],
                             [-30, 5, 10, 15, 15, 10, 5, -30],
                             [-40, -20, 0, 5, 5, 0, -20, -40],
                             [-50, -40, -30, -30, -30, -30, -40, -50]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the Knight for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        vectors = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                   (2, 1), (-2, 1), (2, -1), (-2, -1)]
        return self._get_all_moves_jumpers(pos, vectors)

    def path(self, fro, to):
        """
        Returns list of squares on the table Knight needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        abs_diff = abs(fro - to)

        if abs_diff != (2, 1) and abs_diff != (1, 2):
            raise InvalidMoveException()

        return []


class Bishop(Figure):
    """
       A class for the Bishop inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[-20, -10, -10, -10, -10, -10, -10, -20],
                             [-10, 0, 0, 0, 0, 0, 0, -10],
                             [-10, 0, 5, 10, 10, 5, 0, -10],
                             [-10, 5, 5, 10, 10, 5, 5, -10],
                             [-10, 0, 10, 10, 10, 10, 0, -10],
                             [-10, 10, 10, 10, 10, 10, 10, -10],
                             [-10, 5, 0, 0, 0, 0, 5, -10],
                             [-20, -10, -10, -10, -10, -10, -10, -20]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the Bishop for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        vectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        return self._get_all_moves_sliders(pos, vectors)

    def path(self, fro, to):
        """
        Returns list of squares on the table Bishop needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        diff = to - fro

        # if absolute values of diff don't equal  each other
        # it's not a valid bishop move.
        if abs(diff.x) != abs(diff.y):
            raise InvalidMoveException()

        return self._return_path(fro, to)


class Rook(Figure):
    """
       A class for the Rook inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [5, 10, 10, 10, 10, 10, 10, 5],
                             [-5, 0, 0, 0, 0, 0, 0, -5],
                             [-5, 0, 0, 0, 0, 0, 0, -5],
                             [-5, 0, 0, 0, 0, 0, 0, -5],
                             [-5, 0, 0, 0, 0, 0, 0, -5],
                             [-5, 0, 0, 0, 0, 0, 0, -5],
                             [0, 0, 0, 5, 5, 0, 0, 0]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the Rook for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._get_all_moves_sliders(pos, vectors)

    def path(self, fro, to):
        """
        Returns list of squares on the table Rook needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        diff = to - fro

        # if absolute values of diff equal each other
        # it's a valid move for bishop
        if 0 not in diff:
            raise InvalidMoveException()

        return self._return_path(fro, to)


class Queen(Figure):
    """
       A class for the Queen inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[-20, -10, -10, -5, -5, -10, -10, -20],
                             [-10, 0, 0, 0, 0, 0, 0, -10],
                             [-10, 0, 5, 5, 5, 5, 0, -10],
                             [-5, 0, 5, 5, 5, 5, 0, -5],
                             [0, 0, 5, 5, 5, 5, 0, -5],
                             [-10, 5, 5, 5, 5, 5, 0, -10],
                             [-10, 0, 5, 0, 0, 0, 0, -10],
                             [-20, -10, -10, -5, -5, -10, -10, -20]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the Queen for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        return self._get_all_moves_sliders(pos, vectors)

    def path(self, fro, to):
        """
        Returns list of squares on the table Queen needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        diff = to - fro

        # check for diagonal and (horizontal,vertical)
        if abs(diff.x) != abs(diff.y) and 0 not in diff:
            raise InvalidMoveException()

        return self._return_path(fro, to)


class King(Figure):
    """
       A class for the King inherits from the Figure

       Attributes:

           color (Color): if white it is 0, else it is 1.

           square_table (list): list of positional values for every square

           of the board for the evaluation algorithm
    """
    def __init__(self, color):
        self.square_table = [[-30, -40, -40, -50, -50, -40, -40, -30],
                             [-30, -40, -40, -50, -50, -40, -40, -30],
                             [-30, -40, -40, -50, -50, -40, -40, -30],
                             [-30, -40, -40, -50, -50, -40, -40, -30],
                             [-20, -30, -30, -40, -40, -30, -30, -20],
                             [-10, -20, -20, -20, -20, -20, -20, -10],
                             [20, 20, 0, 0, 0, 0, 20, 20],
                             [20, 30, 10, 0, 0, 10, 30, 20]]
        super().__init__(color)

    def get_all_moves(self, pos):
        """
        Returns all possible moves for the King for the given position

            Returns:

                (list): list of tuples of tuples containing two integers describing the move
        """
        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        return self._get_all_moves_jumpers(pos, vectors)

    def path(self, fro, to):
        """
        Returns list of squares on the table King needs to pass to execute the move

            Returns:

                (list): list of tuples containing two integers describing the path
        """
        abs_diff = abs(to - fro)

        if abs_diff != (1, 1) and abs_diff != (1, 0) and abs_diff != (0, 1):
            raise InvalidMoveException()

        return []
