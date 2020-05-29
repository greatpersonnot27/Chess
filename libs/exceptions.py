class AIChess(Exception):
    pass

class InvalidMoveException(AIChess):
    pass


class CheckMateException(AIChess):
    pass

class StalemateException(AIChess):
    pass