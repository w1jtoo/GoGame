from client.API.StoneSide import StoneSide


class StoneGroup(object):
    def __init__(self, side: StoneSide, free_stones, *args):
        self._free_stones = free_stones
        self._positions = set(args)
        self.__liberty = 0
        self.__side = side
        self._count = 0

    def __len__(self):
        return len(self._positions)

    def _add(self, stone: (int, int), free_stones):
        # adding one stone
        self._free_stones = self._free_stones.union(
            free_stones)
        self._positions.add(stone)

    def update(self, other):
        self._positions = self._positions.union(
            other._positions)
        # if self.liberty < other.liberty:
        self._free_stones = self._free_stones.union(
            other._free_stones)

    @property
    def side(self):
        return self.__side

    @property
    def liberty(self):
        return len(self._free_stones)

    def __iter__(self):
        yield from self._positions

    def __next__(self):
        if not self._positions:
            raise StopIteration
        return self._positions.pop()

    def __str__(self):
        result = ''.join(str(self._positions))
        return result

    def is_neighbour(self, position: (int, int)) -> bool:
        if position in self._positions:
            raise Exception('This stone is a part of its group')
        for stone in self:
            if (stone[0] + 1, stone[1]) == position\
                    or (stone[0] - 1, stone[1]) == position\
                    or (stone[0], stone[1] + 1) == position\
                    or (stone[0], stone[1] - 1) == position:
                return True
        return False

    def __eq__(self, other):
        return self._positions == other._positions
