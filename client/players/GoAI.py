import time
import random as rand
import threading


class GoAI(object):
    def __init__(self, name, board, side):
        self._name = name
        self._board = board
        self._side = side
        self._waiting = False
        self.turn_position = ()
        self.is_player = False

    def spawn(self):
        self.t = threading.Thread(target=self.think)
        self.t.start()


    def get_free_position(self):
        dx = rand.randint(0, self._board._dimensionality)
        dy = rand.randint(0, self._board._dimensionality)
        while(not self._board.is_cantainable((dx, dy))):
            dx = rand.randint(0, self._board._dimensionality)
            dy = rand.randint(0, self._board._dimensionality)
        return (dx, dy)

    def think(self):
        # time.sleep(1)
        while self._board.is_started:
            if self._side == self._board.turn:
                time.sleep(rand.random() / 2 + 0.3)
                self._board.add(self.get_free_position())

    @property
    def name(self):
        return self._name
