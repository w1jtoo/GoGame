import abc

class IPlayer(object,metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        self._pressed_position = None

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError


    def set_pressed_position(self, position):
        self._pressed_position = position

    @abc.abstractmethod
    def make_disidion(self):
        raise NotImplementedError
    