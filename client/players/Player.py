import threading


class Player(object):
    def __init__(self, name, board, side):
        self._name = name
        self._board = board
        self._side = side
        self._waiting = False
        self.turn_position = ()
        self.is_player = True

    def spawn(self):
        self.t = threading.Thread(target=self.think)
        self.t.start()

    def mouse_event_processing(self, dx, dy):
        if self._waiting:
            self._board.add((dx, dy))
        self._waiting = False

    def think(self):
        while self._board.is_started:
            if self._side == self._board.turn:
                if self.turn_position:
                    self._board.add(self.turn_position)
                    self.turn_position = ()

    @property
    def name(self):
        return self._name
