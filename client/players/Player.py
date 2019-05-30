from client.players.IPlayer import IPlayer

class Player(IPlayer):
    def __init__(self, name, board, side):
        super(Player, self).__init__()
        self._name = name
        self._board = board
        self._side = side

        self.turn_position = ()
        self.is_player = True



    def make_disidion(self):
        while self._board.paused and not self._pressed_position:
            pass
        pressed = self._pressed_position
        self._pressed_position = None
        return pressed



    @property
    def name(self):
        return self._name
