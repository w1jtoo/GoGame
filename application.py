import _thread

# import QT
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import (QLabel, QGridLayout, QPushButton,
                             QGraphicsDropShadowEffect, QMainWindow)

# import game play things
from client.API.Board import Board
from client.API.StoneSide import StoneSide
from client.players.Player import Player
from client.players.GoAI import GoAI


# import GUI
from client.gui.BoardQGraphics import BoardQGraphics
from client.gui.StoneQGraphics import StoneQGraphics

import time
import threading

WINDOW_HIGHT = 700
WINDOW_WIDTH = 900


class MyApp(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.timer = QTimer(self)
        self.timer_interval = 1
        self.setWindowTitle('Go game')
        self.mouse_position = None
        x = 0
        y = 0
        self.text = "x: {0},  y: {1}".format(x, y)
        self._dimensionality = 19
        self.board = Board(self._dimensionality)
        self.score_label = QLabel('Счет: 0', self)
        self.game_position = QLabel('Ход игорка с ником:', self)
        self.initUI()
        self._players = {}
        # now bots train own skill
        self.change_game_with_no_player()

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setMaximumHeight(WINDOW_HIGHT)
        self.setMaximumWidth(WINDOW_WIDTH)
        self.setMinimumHeight(WINDOW_HIGHT)
        self.setMinimumWidth(WINDOW_WIDTH)

        # Variables
        grid = QGridLayout()
        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        self.setMouseTracking(1)
        self.font = QFont('Comic Sans MS')
        self.score_label.setGeometry(660, 105, 200, 40)
        self.score_label.setFont(QFont('Comic Sans MS', 25))
        self.game_position.setGeometry(660, 135, 200, 80)
        self.game_position.setFont(QFont('Comic Sans MS', 20))

        # button reset
        self.QBut_reset = QPushButton('Начать заново', self)
        self.QBut_reset.setGeometry(650, 340, 200, 40)
        self.font.setPointSize(14)
        self.QBut_reset.setFont(self.font)
        self.QBut_reset.clicked.connect(self.reset)
        self.QBut_reset.setStyleSheet("background-color:rgb(240, 180, 30)")

        # button pass
        self.QBut_pass = QPushButton('Пропустить ход', self)
        self.QBut_pass.setGeometry(650, 280, 200, 40)
        self.font.setPointSize(14)
        self.QBut_pass.setFont(self.font)
        self.QBut_pass.clicked.connect(self.pass_move)
        self.QBut_pass.setStyleSheet("background-color:rgb(240, 180, 30)")

        # game stop button
        self.QBut_stop = QPushButton('Закончить игру', self)
        self.QBut_stop.setGeometry(650, 380, 200, 40)
        self.font.setPointSize(14)
        self.QBut_stop.setFont(self.font)
        self.QBut_stop.clicked.connect(self.stop)
        self.QBut_stop.setStyleSheet("background-color:rgb(240, 180, 30)")

        # game with bot
        self.QBut_robot = QPushButton('Играть с ботом', self)
        self.QBut_robot.setGeometry(650, 420, 200, 40)
        self.font.setPointSize(14)
        self.QBut_robot.setFont(self.font)
        self.QBut_robot.clicked.connect(self.change_game_with_player)
        self.QBut_robot.setStyleSheet("background-color:rgb(240, 180, 30)")

        # game with two players
        self.QBut_player = QPushButton('Играть вдвоем', self)
        self.QBut_player.setGeometry(650, 460, 200, 40)
        self.font.setPointSize(14)
        self.QBut_player.setFont(self.font)
        self.QBut_player.clicked.connect(self.change_game_with_two_players)
        self.QBut_player.setStyleSheet("background-color:rgb(240, 180, 30)")

        self.timer.timeout.connect(self.update)
        self.timer.setSingleShot(False)
        self.show()

    def GPU_update(self):
        self.update()
        self.show()

    def mousePressEvent(self, e):
        if 75 < e.x() < 75 + (self.board.dimensionality - 1) * 30\
                and 75 < e.y() < 75 + (self.board.dimensionality - 1) * 30:
            dx = (e.x() - 60) // 30
            dy = (e.y() - 60) // 30
            self._players[self.board.turn].turn_position = (dx, dy)

    def turn_loop(self):
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

    def start(self):
        self.timer.start(self.timer_interval)

    def spawn_players(self):
        for player in self._players.values():
            player.spawn()

    # region buttons

    def stop(self):
        self.board.is_started = False

    def reset(self):
        self.board.restart()

    def pass_move(self):
        self.board.pass_move()

    def change_game_with_two_players(self):
        self.board.is_started = False
        time.sleep(1)
        self.board.restart()
        self._players = {StoneSide.BLACK: Player('Игорк 1', self.board,
                                                 StoneSide.BLACK),
                         StoneSide.WHITE: Player('Игрок 2', self.board,
                                                 StoneSide.WHITE)}
        self.spawn_players()

    def change_game_with_player(self):
        self.board.is_started = False
        time.sleep(1)
        self.board.restart()
        self._players = {StoneSide.BLACK: GoAI('Робот', self.board,
                                               StoneSide.BLACK),
                         StoneSide.WHITE: Player('Игрок', self.board,
                                                 StoneSide.WHITE)}
        self.spawn_players()

    def change_game_with_no_player(self):
        self.board.is_started = False
        time.sleep(1)
        self.board.restart()
        self._players = {StoneSide.BLACK: GoAI('Робот 1', self.board,
                                               StoneSide.BLACK),
                         StoneSide.WHITE: GoAI('Робот 2', self.board,
                                               StoneSide.WHITE)}
        self.spawn_players()
    # endregion

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QColor(155, 88, 19, 200))
        painter.setBackground(Qt.blue)
        if self._players[self.board.turn].is_player:
            self.QBut_pass.setEnabled(True)
        else:
            self.QBut_pass.setEnabled(False)

        if self.board.is_started:
            self.QBut_reset.setEnabled(True)
        else:
            self.QBut_reset.setEnabled(False)
        self.draw_game_place(painter)
        self.draw_board(painter)

    def draw_game_place(self, painter):
        painter.setBrush(QColor(255, 157, 0))
        painter.drawRect(-1, -1, WINDOW_WIDTH + 1, WINDOW_HIGHT + 1)
        painter.setFont = QFont("Times", 50, QFont.Bold)
        text = 'Ход:' + str(self._players[self.board.turn].name)
        self.game_position.setText(text)
        text = 'Счет:' + str(self.board.score)
        self.score_label.setText(text)

    def draw_board(self, painter):
        BoardQGraphics(dimensionality=self.board.dimensionality).paint(painter)
        # stone mouse
        if self.mouse_position and self.board.is_started:
            dx = self.mouse_position[0] - 0.5
            dy = self.mouse_position[1] - 0.5
            if self.board.turn == StoneSide.BLACK:
                StoneQGraphics((dx, dy), QColor(0, 0, 0, 200)).paint(painter)
            if self.board.turn == StoneSide.WHITE:
                StoneQGraphics((dx, dy), QColor(
                    255, 255, 255, 150)).paint(painter)
        # stone groups
        for x in range(self.board.dimensionality + 1):
            for y in range(self.board.dimensionality + 1):
                if self.board[(x, y)] is None:
                    continue
                elif self.board[(x, y)].side is StoneSide.BLACK:
                    StoneQGraphics((x - 0.5, y - 0.5), 'black').paint(painter)
                elif self.board[(x, y)].side is StoneSide.WHITE:
                    StoneQGraphics((x - 0.5, y - 0.5), 'white').paint(painter)
        # last stone that was chosen
        last_stone = self.board._last_position
        if type(last_stone) is tuple:
            last_stone = (last_stone[0] - 0.5, last_stone[1] - 0.5)
            StoneQGraphics((last_stone), QColor(
                72, 177, 203, 75)).paint(painter)

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
