
# import stone objects
from client.API.StoneGroup import StoneGroup
from client.API.StoneSide import StoneSide

from functools import lru_cache
from client.utils.Common import once
import threading


class Board(object):
    EMPTY_GROUP = StoneGroup(StoneSide.EMPTY, (-1, -1))

    # TODO create iter
    def __init__(self, dimensionality):
        # TODO think ...
        self._dimensionality = dimensionality
        self.groups = []
        self._score = 0
        self.is_started = True
        self._turn = StoneSide.BLACK
        self._last_position = None
        self._last_stones = []
        self._is_passed = False
        self._players = {}
        self.paused = False

    # @lru_cache()
    def is_possible(self, position: (int, int)) -> bool:
        """ Shows if *position* on the board is possible to
        be setted by stone.  
        """

        if self.get_liberty(position) == 0:
            # the KO rule
            if len(self._last_stones)-2 > 0 and \
                    self._last_stones[len(self._last_stones)-2] == position:
                return False
            if self._last_position == position:
                return False

            for neighbour in self.get_neighbours(position):
                if self[neighbour].liberty == 1\
                        and self[neighbour].side != self.turn:
                    return True

            bad_liberty = True
            for neighbour in self.get_neighbours(position):
                if self[neighbour].side == self.turn\
                        and self[neighbour].liberty != 1:
                    bad_liberty = False
            if bad_liberty:
                return False

        return True

    @property
    def turn(self):
        return self._turn

    @property
    def dimensionality(self):
        return self._dimensionality

    @property
    def score(self):
        return self._score

    @property
    def is_ready(self):
        return len(self._players.keys()) >= 2

    def restart(self, dim: int):
        """ Prepare game to new game, don't stop game loop
        """

        players = self._players
        self.paused = True
        self.__init__(dim)
        self._is_passed = False
        self._players = players
        for player in self._players:
            player.__init__()
        self.paused = False

    def is_cantainable(self, position: (int, int)) -> bool:
        if 0 <= position[0] < self.dimensionality\
                and 0 <= position[1] < self.dimensionality:
            for group in self.groups:
                if position in group:
                    return False
            return True
        return False

    def __getitem__(self, position: (int, int)):
        for group in self.groups:
            if position in group:
                return group
        return None

    def pass_move(self):
        """ Skip move and change turn. """

        if self._is_passed:
            self.paused = True
            self.update_score()
        self._is_passed = True
        self._change_turn()

    def update_score(self):
        """ Update score and culc score using liberty 
        and sone location
        """

        # TODO
        pass

    def _change_turn(self):
        # clear of cache
        # self.is_possible.cache_clear()
        self.get_neighbours.cache_clear()
        self.get_liberty.cache_clear()

        # TODO here is danger part of code: idea of 2 StoneSides is broken
        if self._turn == StoneSide.BLACK:
            self._turn = StoneSide.WHITE
        elif self._turn == StoneSide.WHITE:
            self._turn = StoneSide.BLACK
        else:
            raise Exception('Wrong turn')

    def add(self, position: (int, int)):
        """ Add stone  with *position* to board.

            All main game logic is here. """

        if position is None:
            # self.update()
            return
        if not 0 <= position[0] < self.dimensionality\
                or not 0 <= position[1] < self.dimensionality:
            raise Exception('Out of dimensionality')
        for group in self.groups:
            if position in group:
                return
        if not self.is_possible(position):
            return
        added_group = self.EMPTY_GROUP
        remove_list = []
        for group in self.groups:
            if self.turn == group.side:
                if group.is_neighbour(position):
                    if not added_group == self.EMPTY_GROUP:
                        group.update(added_group)
                        remove_list.append(added_group)
                    else:
                        group._add(position,
                                   self.get_free_stones(position))
                    added_group = group

        if added_group == self.EMPTY_GROUP:
            self.groups.append(StoneGroup(self.turn,
                                          self.get_free_stones(position),
                                          position))
        for group in remove_list:
            self.groups.remove(group)

        self._last_position = position
        self._last_stones.append(position)
        self._update()
        self._change_turn()
        self._is_passed = False
        # print(len(self.groups))

    def get_free_stones(self, position):
        # TODO remove

        result = set()
        if self.is_cantainable((position[0] + 1, position[1])):
            result.add((position[0] + 1, position[1]))
        if self.is_cantainable((position[0] - 1, position[1])):
            result.add((position[0] - 1, position[1]))
        if self.is_cantainable((position[0], position[1] + 1)):
            result.add((position[0], position[1] + 1))
        if self.is_cantainable((position[0], position[1] - 1)):
            result.add((position[0], position[1] - 1))
        return result

    @lru_cache()
    def get_liberty(self, position):
        """ Return liberty of single stone.
        """

        liberty = 0
        if self.is_cantainable((position[0] + 1, position[1])):
            liberty += 1
        if self.is_cantainable((position[0] - 1, position[1])):
            liberty += 1
        if self.is_cantainable((position[0], position[1] + 1)):
            liberty += 1
        if self.is_cantainable((position[0], position[1] - 1)):
            liberty += 1
        return liberty

    def _update(self):
        """ Update and remove odd created groups. 
        """
        remove_list = []
        for group in self.groups:
            group._free_stones = set()
            for position in group:
                group._free_stones.update(
                    self.get_free_stones(position))

        for group in self.groups:
            if group.liberty == 0 and not self._last_position in group:
                remove_list.append(group)

        for group in remove_list:
            if group.side == StoneSide.WHITE:
                self._score += len(group)
            else:
                self._score -= len(group)
            self.groups.remove(group)

    def __str__(self):
        # TODO string fit to serialization

        result = ''
        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += self[(dy, dx)].side.value
                else:
                    result += 'E'
            result += '\n'
        return result

    def str_with_liberty(self) -> str:
        """ Return game field with number of group liberty in stone
        location.
        """

        result = 'Board with {} groups.\n'.format(len(self.groups)) +\
            'Score: {}\n'.format(self._score)

        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += str(self[(dy, dx)].liberty)
                else:
                    result += '-'
            result += '\n'

        return result

    def game_format(self) -> str:
        """ Return game field with 'B' - black and 'W' - white in cell. 
        """

        result = 'Board with {} groups.\n'.format(len(self.groups)) +\
            'Score: {}\n'.format(self._score)

        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += str(self[(dy, dx)].liberty)
                else:
                    result += ' '
            result += '\n'

        return result

    @lru_cache()
    def get_neighbours(self, position) -> list:
        """ Return neighbours of *position* on the board
        """
        result = []
        # here were "=="'s
        if type(self[(position[0] + 1, position[1])]) is StoneGroup:
            result.append((position[0] + 1, position[1]))
        if type(self[(position[0] - 1, position[1])]) is StoneGroup:
            result.append((position[0] - 1, position[1]))
        if type(self[(position[0], position[1] + 1)]) is StoneGroup:
            result.append((position[0], position[1] + 1))
        if type(self[(position[0], position[1] - 1)]) is StoneGroup:
            result.append((position[0], position[1] - 1))
        return result

    # @once
    def set_players(self, *args):
        # TODO add sides to StoneSide
        """ Set players in game, clear old players list"""
        self._players.clear()

        for player in args:
            self._players[player.side] = player

    def get_current_player(self):
        """ Return current IPlayer object """
        return self._players[self.turn]

    def game_update(self):
        """ Method to game update loop """

        while self.is_started:
            if self.is_ready and \
                    not self.paused and\
                    self._players[self.turn]:
                self.add(self._players[self.turn].make_disidion())
            self._update()
