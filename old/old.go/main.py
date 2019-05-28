from enum import Enum
import copy


class Point(object):
    def __init__(self, dx: int, dy: int):
        self._x = dx
        self._y = dy

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self) -> str:
        return 'Point ({}, {})'.format(self.x, self.y)

    def __hash__(self):
        # TODO use const instead of 50
        return self._x * 50 + self._y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def _get_neighbours(self):
        return [Point(self.x + 1, self.y), Point(self.x - 1, self.y),
                Point(self.x, self.y + 1), Point(self.x, self.y - 1)]


class StoneSide(Enum):
    BLACK = 'B'
    WHITE = 'W'


class Stone(object):
    def __init__(self, side):
        self._liberty = 0
        self._side = side

    @property
    def liberty(self):
        return self._liberty

    @liberty.setter
    def liberty(self, update: int):
        self._liberty = update

    @property
    def side(self):
        return self._side

    def str_side(self) -> str:
        return str(self._side.value)

    def __eq__(self, other):
        return self._side == other._side

    def __str__(self):
        # TODO ok string format
        return str(self._side.value)

#


class Board(object):
    def __init__(self, dimensionality: int):
        self._dimensionality = dimensionality
        self._grids = {}

    @property
    def dimensionality(self):
        return self._dimensionality

    def __setitem__(self, point: Point, stone: Stone):
        self._grids[point] = stone

    def __getitem__(self, point: Point):
        return self._grids[point]

    def in_bound(self, point: Point) -> bool:
        return 0 <= point.x < self.dimensionality\
            and 0 <= point.y < self.dimensionality

    def add(self, stone: Stone, dx: int, dy: int):
        if Point(dx, dy) in self._grids.keys():
            raise Exception('Already added.')
        if self.dimensionality < dx - 1 \
                or self.dimensionality < dy - 1:
            raise Exception('Out of board range.')

        self._grids[Point(dx, dy)] = copy.deepcopy(stone)
        self.update_stone_liberty(Point(dx, dy))

    def _remove(self, dx: int, dy: int):
        if not Point(dx, dy) in self._grids.keys():
            raise Exception('Already empty.')
        if self.dimensionality < dx - 1 \
                or self.dimensionality < dy - 1:
            raise Exception('Out of board range.')
        self._grids.pop(Point(dx, dy))
        self.update_stone_liberty(Point(dx, dy))

    def is_empty(self, dx: int, dy: int) -> bool:
        return not Point(dx, dy) in self._grids.keys()

    def update_stone_liberty(self, position: Point, last_points=set()):
        max_liberty = 0
        free_neighbours = 0
        neighbours = position._get_neighbours()
        for current_point in neighbours:
            if current_point in last_points:
                continue
            if current_point in self._grids.keys():
                if self[position].side == self[current_point].side:
                    self[current_point] = self[position]
                last_points.add(position)
                self.update_stone_liberty(current_point, last_points)
            elif self.in_bound(current_point):
                free_neighbours += 1

        self[position].liberty = free_neighbours

    def count(self) -> int:
        return len(self._grids.keys())

    def __str__(self):
        return 'Board. Stone count: {}. Dimensionality: {}'\
            .format(self.count(), self._dimensionality)

    def to_string_format(self):
        """ return current look of board  """
        result = ''
        for y in range(self.dimensionality):
            for x in range(self.dimensionality):
                if Point(x, y) in self._grids.keys():
                    result += self[Point(x, y)].str_side()
                else:
                    result += "E"
            result += '\n'
        return result

    def to_string_format_with_liberty(self):
        """ return current look of board  """
        result = ''
        for y in range(self.dimensionality):
            for x in range(self.dimensionality):
                if Point(x, y) in self._grids.keys():
                    result += str(self[Point(x, y)].liberty)
                else:
                    result += '-'
            result += '\n'
        return result


WHITE_STONE = Stone(StoneSide.WHITE)
BLACK_STONE = Stone(StoneSide.BLACK)


def main():
    board = Board(5)
    board.add(WHITE_STONE, 1, 0)
    board.add(BLACK_STONE, 0, 0)
    board.add(BLACK_STONE, 0, 1)
    board.add(WHITE_STONE, 2, 0)
    board.add(WHITE_STONE, 2, 1)
    board.add(WHITE_STONE, 1, 1)
    board.add(BLACK_STONE, 3, 0)
    #board.add(BLACK_STONE, 3, 1)
    board.add(BLACK_STONE, 2, 2)
    board.add(BLACK_STONE, 1, 2)

    print(board.to_string_format_with_liberty())
    print(Board.to_string_format(board))


if __name__ == "__main__":
    main()
