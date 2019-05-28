import pytest
from main import (
    Board,
    Point,
    StoneSide,
    Stone
)


WHITE_STONE = Stone(StoneSide.WHITE)
BLACK_STONE = Stone(StoneSide.BLACK)

@pytest.fixture
# region some board tests
# TODO tests by name
def creating_board_tests():
    board = Board(5)
    board.add(WHITE_STONE, 1, 0)
    print(board.is_empty(1, 0))
    print(board.is_empty(0, 0))

# endregion


# region some stone tests
# TODO tests by name


def creating_stone_tests():
    assert True

# endregion


# region some point tests
# TODO tests by name
def point_init_test():
    assert True

# endregion
