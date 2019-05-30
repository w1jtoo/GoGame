from client.players.IPlayer import IPlayer


class Player(IPlayer):
    def __init__(self, name, board, side):
        super(Player, self).__init__(name, board, side, True)
        self.turn_position = ()

    def make_disidion(self):
        while self._board.paused and not self._pressed_position:
            pass
        pressed = self._pressed_position
        self._pressed_position = None
        return pressed

    @property
    def name(self):
        return self._name
