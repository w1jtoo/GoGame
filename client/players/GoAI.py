import time
import random as rand
from client.players.IPlayer import IPlayer

class GoAI(IPlayer):
    def __init__(self, name, board, side):
        super(GoAI, self).__init__()
        self._name = name
        self._board = board
        self._side = side
        self.is_player = False

    def make_disidion(self):
        time.sleep(rand.random() / 2 + 0.3)
        return self._get_free_position()


    def _get_free_position(self):
        dx = rand.randint(0, self._board._dimensionality)
        dy = rand.randint(0, self._board._dimensionality)
        while(not self._board.is_cantainable((dx, dy))):
            dx = rand.randint(0, self._board._dimensionality)
            dy = rand.randint(0, self._board._dimensionality)
        return (dx, dy)

    @property
    def name(self):
        return "Random Bot"
        # return self._name
