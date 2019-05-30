import time
import random as rand
from client.players.IPlayer import IPlayer


class EasyAI (IPlayer):
    def __init__(self, name, board, side):
        super(EasyAI, self).__init__(name, board, side, False)

    def make_disidion(self):
        weight = rand.randint(0, 20)
        result = None

        time.sleep(rand.random())
        if weight < 15:
            if self._board._last_position:
                last_stones = self._board.get_free_stones(
                    self._board._last_position)
                for stone in last_stones:
                    if self._board.is_cantainable(stone) and\
                            self._board.is_possible(stone):
                        result = stone
                    else:
                        result = None
            else:
                result = self._get_random_free_position()
        elif(14 < weight < 20):
            result = self._get_random_free_position()
        else:
            result = None # like a change turn
            
        if result is None:
            return 
        return result if self._board.is_possible(result) else None

    def _get_random_free_position(self):
        ticks_out = 0
        dx = rand.randint(0, self._board._dimensionality)
        dy = rand.randint(0, self._board._dimensionality)
        while(not self._board.is_cantainable((dx, dy)) or
              not self._board.is_possible((dx, dy))):
            dx = rand.randint(0, self._board._dimensionality)
            dy = rand.randint(0, self._board._dimensionality)
            if ticks_out >= self._board.dimensionality * 10:
                return  # passed
            ticks_out += 1
        return (dx, dy)

    @property
    def name(self):
        return "Easy Bot"
        # return self._name
