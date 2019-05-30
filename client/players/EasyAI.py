import time
import random as rand
from client.players.IPlayer import IPlayer

class EasyAI (IPlayer):
    def __init__(self, name, board, side):
        super(EasyAI, self).__init__()
        self._name = name
        self._board = board
        self._side = side
        self.is_player = False

    def make_disidion(self):
        weight = rand.randint(0, 20)

        time.sleep(rand.random())
        if weight < 15:
            if self._board._last_position:
                last_stones = self._board.get_free_stones(self._board._last_position)
                for stone in last_stones:
                    if self._board.is_cantainable(stone):
                        return stone
                    else:
                        return None
            else:
                return self._get_random_free_position()
        elif(14 < weight < 20):
            return self._get_random_free_position()
        else:
            return # like a change turn
            
        return # like a change turn  


    def _get_random_free_position(self):
        ticks_out = 0
        dx = rand.randint(0, self._board._dimensionality)
        dy = rand.randint(0, self._board._dimensionality)
        while(not self._board.is_cantainable((dx, dy))):
            dx = rand.randint(0, self._board._dimensionality)
            dy = rand.randint(0, self._board._dimensionality)
            if ticks_out >= self._board.dimensionality * 10:
                return # passed
            ticks_out += 1
        return (dx, dy)

    @property
    def name(self):
        return "Easy Bot"
        #return self._name
