import abc


class IPlayer(object, metaclass=abc.ABCMeta):

    def __init__(self, name, board, side, is_player):
        self.is_player = is_player
        self._pressed_position = None
        self._name = name
        self._board = board
        self._side = side

    @property
    def side(self):
        return self._side

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    def set_pressed_position(self, position):
        self._pressed_position = position

    @abc.abstractmethod
    def make_disidion(self) -> (int, int):
        """ Should return position chosen by this AI  
        """
        raise NotImplementedError
