import random
import sys
import traceback
from enum import Enum

import time
import math
from PyQt5.QtCore import (QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QImage, QPainter)
from PyQt5.QtCore import (QTimer, Qt)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem,  QGraphicsScene,
                             QLabel, QGridLayout, QGraphicsDropShadowEffect,
                             QGraphicsView, QMainWindow, QPushButton)

# Generated gui module
from gui import Ui_Field as Ui_MainWindow


class StoneSide(Enum):
    BLACK = 'B'
    WHITE = 'W'
    EMPTY = 'E'


class StoneGroup(object):
    def __init__(self, side: StoneSide, *args):
        self._positions = set(args)
        self.__liberty = 0
        self.__side = side
        self._count = 0

    def __len__(self):
        return len(self._positions)

    def _add(self, stone: (int, int)):
        self._positions.add(stone)

    def __add__(self, other):
        self._positions.union(
            other._positions.copy())
        if self.liberty < other.liberty:
            self.liberty = other.liberty

    def __iadd__(self, other):
        self = self + other

    def update(self, other):
        self._positions = self._positions.union(
            other._positions)
        if self.liberty < other.liberty:
            self.liberty = other.liberty

    @property
    def side(self):
        return self.__side

    @property
    def liberty(self):
        return self.__liberty

    @liberty.setter
    def liberty(self, update: int):
        self.__liberty = update

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


class Board(object):
    EMPTY_GROUP = StoneGroup(StoneSide.EMPTY, (-1, -1))

    # TODO create iter

    def __init__(self, dimensionality):
        self._dimensionality = dimensionality
        self.groups = []
        self._score = 0
        self._turn = StoneSide.BLACK
        self._last_position = None

    def is_possible(self, position: (int, int)):
        if self.get_liberty(position) == 0:
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

    def _change_turn(self):
        if self._turn == StoneSide.BLACK:
            self._turn = StoneSide.WHITE
        elif self._turn == StoneSide.WHITE:
            self._turn = StoneSide.BLACK
        else:
            raise Exception('Wrong turn')

    def add(self, position: (int, int)):
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
                        group._add(position)
                    added_group = group
                    # self.update()
        if added_group == self.EMPTY_GROUP:
            self.groups.append(StoneGroup(self.turn, position))
        for group in remove_list:
            self.groups.remove(group)
        self._last_position = position
        self.update()
        self._change_turn()
        # print(len(self.groups))

    def get_liberty(self, position):
        # return liberty of single stone
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

    def update(self):
        remove_list = []
        for group in self.groups:
            group.liberty = 0
            for position in group:
                liberty = self.get_liberty(position)
                if group.liberty < liberty:
                    group.liberty = liberty
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
        # TODO ok string format
        result = ''
        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += self[(dy, dx)].side.value
                else:
                    result += 'E'
            result += '\n'
        return result

    def str_with_liberty(self):
        result = 'Board with {} groups.\n'.format(len(self.groups)) +\
            'Score: {}\n'.format(self._score)
        # for group in self:
        #    result += str(group) + '\n'

        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += str(self[(dy, dx)].liberty)
                else:
                    result += '-'
            result += '\n'
        return result

    def game_format(self):
        result = 'Board with {} groups.\n'.format(len(self.groups)) +\
            'Score: {}\n'.format(self._score)
        # for group in self:
        #    result += str(group) + '\n'

        for dx in range(self.dimensionality):
            for dy in range(self.dimensionality):
                if self[(dy, dx)]:
                    result += str(self[(dy, dx)].liberty)
                else:
                    result += ' '
            result += '\n'
        return result

    def get_neighbours(self, position):
        result = []
        if type(self[(position[0] + 1, position[1])]) == StoneGroup:
            result.append((position[0] + 1, position[1]))
        if type(self[(position[0] - 1, position[1])]) == StoneGroup:
            result.append((position[0] - 1, position[1]))
        if type(self[(position[0], position[1] + 1)]) == StoneGroup:
            result.append((position[0], position[1] + 1))
        if type(self[(position[0], position[1] - 1)]) == StoneGroup:
            result.append((position[0], position[1] - 1))
        return result


class MyApp(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.timer = QTimer(self)
        self.timer_interval = 30
        self.setWindowTitle('Go game')
        self.mouse_position = None
        x = 0
        y = 0
        self.text = "x: {0},  y: {1}".format(x, y)
        self.board = Board(13)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Variables
        self.end = False
        self.key = Qt.Key_Up
        grid = QGridLayout()
        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)


        self.setMouseTracking(1)
        # self.scene.setGeometry(0, 0, 500, 600)
        self.setGeometry(0, 0, 500, 500)
        self.show()
        # self.setMouseTracking(True)
        # self.QGraph_field.setGeometry(0, 0, 500, 500)

    def mousePressEvent(self, e):
        if 75 < e.x() < 75 + (self.board.dimensionality - 1) * 30\
                and 75 < e.y() < 75 + (self.board.dimensionality - 1) * 30:
            dx = (e.x() - 60) // 30
            dy = (e.y() - 60) // 30
            self.board.add((dx, dy))

        print(self.board.str_with_liberty())
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)
        self.update()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        if 75 < e.x() < 75 + (self.board.dimensionality - 1) * 30\
                and 75 < e.y() < 75 + (self.board.dimensionality - 1) * 30:
            dx = (e.x() - 60) // 30
            dy = (e.y() - 60) // 30
            if self.board.is_possible((dx, dy)):
                self.mouse_position = (dx, dy)
        else:
            self.mouse_position = None

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)
        self.update()

    def start(self):
        self.timer.start(self.timer_interval)


    def paintEvent(self, e):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(50,200,200))
        shadow.setBlurRadius(30)
        shadow.setOffset(4,-3)

        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QColor(155, 88, 19, 200))
        painter.setBackground(Qt.blue)
        self.draw_board(painter)
        painter.drawText(75,38, 'Счет:' + str(self.board.score))

    def draw_board(self, painter):
        BoardQGrapics(dimensionality=self.board.dimensionality).paint(painter)
        if self.mouse_position:
            dx = self.mouse_position[0] - 0.5
            dy = self.mouse_position[1] - 0.5
            StoneQGrapics((dx, dy), QColor(155, 88, 19, 30)).paint(painter)

        for x in range(self.board.dimensionality + 1):
            for y in range(self.board.dimensionality + 1):
                if self.board[(x, y)] is None:
                    continue
                elif self.board[(x, y)].side is StoneSide.BLACK:
                    StoneQGrapics((x - 0.5, y - 0.5), 'black').paint(painter)
                elif self.board[(x, y)].side is StoneSide.WHITE:
                    StoneQGrapics((x - 0.5, y - 0.5), 'white').paint(painter)

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()


class BoardQGrapics(QGraphicsItem):
    def __init__(self, xy=(75, 75), dimensionality=9, radius=30):
        self.dimensionality = dimensionality
        QGraphicsItem.__init__(self)
        self.colour = QColor(155, 88, 19)
        self.dx = xy[0]
        self.dy = xy[1]
        self._radius = radius

    def boundingRect(self):
        x, y = self.xy
        return QRectF(x*30, y*30, 30, 30)

    def paint(self, painter):
        distance = (self.dimensionality - 1) / 2
        distances = [distance,
                     distance * 5 / 3,
                     distance / 3]
        for x in range(self.dimensionality - 1):
            for y in range(self.dimensionality - 1):
                # draw field
                painter.setBrush(self.colour)
                painter.drawRect(self.dx + x * 30, self.dx +
                                 y * 30, 30, 30)
                # draw some circles
                if x in distances and y in distances:
                    StoneQGrapics((x - 0.15, y - 0.15),
                                  radius=10).paint(painter)

                # x, y = self.xy
        # colour = QBrush(QColor(self.colour))
        # painter.setBrush(colour)


class StoneQGrapics(QGraphicsItem):
    def __init__(self, xy=(75, 75), colour='black', radius=28):
        QGraphicsItem.__init__(self)
        self.colour = colour
        self.xy = xy
        self.dx = xy[0]
        self.dy = xy[1]
        self._radius = radius

    def boundingRect(self):
        x, y = self.xy
        return QRectF(x*30, y*30, self._radius, self._radius)

    def paint(self, painter):
        x, y = self.xy
        colour = QBrush(QColor(self.colour))
        painter.setBrush(colour)
        painter.drawEllipse(x*30 + 75, y*30 + 75, self._radius, self._radius)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    window.start()
    sys.exit(app.exec_())

if __name__ == "__main__1":
    b = Board(9)
    count = 0
    while 1:
        pos = input().split()
        if count % 2 == 0:
            print('Black Turn')
            count += 1
            side = StoneSide.BLACK
        else:
            print('White Turn')
            side = StoneSide.WHITE
        print(b.str_with_liberty())
        print(str(b))
