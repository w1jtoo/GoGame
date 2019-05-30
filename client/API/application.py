import _thread

# import QT
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton,\
    QGraphicsDropShadowEffect, QMainWindow, QMessageBox

# import game play things
from client.API.Board import Board
from client.API.StoneSide import StoneSide
from client.players.Player import Player
from client.players.GoAI import GoAI
from client.players.EasyAI import EasyAI


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
        self.last_pressed_but = None
        self.timer = QTimer(self)
        self.timer_interval = 1
        self.setWindowTitle('Go game')
        self.mouse_position = None
        x = 0
        y = 0
        self.text = "x: {0},  y: {1}".format(x, y)
        self._dimensionality = 19
        self.board = Board(self._dimensionality)
        self._ai = GoAI
        self.score_label = QLabel('Счет: 0', self)
        self.game_position = QLabel('Ход игорка с ником:', self)
        self.initUI()
        self.timer.timeout.connect(self.update)
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
        # self.QBut_stop = QPushButton('Закончить игру', self)
        # self.QBut_stop.setGeometry(650, 380, 200, 40)
        # self.font.setPointSize(14)
        # self.QBut_stop.setFont(self.font)
        # self.QBut_stop.clicked.connect(self.stop)
        # self.QBut_stop.setStyleSheet("background-color:rgb(240, 180, 30)")

        # game with bot
        self.QBut_robot = QPushButton('Играть с ботом', self)
        self.QBut_robot.setGeometry(650, 420, 200, 40)
        self.font.setPointSize(14)
        self.QBut_robot.setFont(self.font)
        self.QBut_robot.clicked.connect(self.change_game_with_player)
        self.QBut_robot.setStyleSheet("background-color:rgb(240, 180, 30)")

        self.game_hard_buttons()

        # game with two players
        self.QBut_player = QPushButton('Играть вдвоем', self)
        self.QBut_player.setGeometry(650, 500, 200, 40)
        self.font.setPointSize(14)
        self.QBut_player.setFont(self.font)
        self.QBut_player.clicked.connect(self.change_game_with_two_players)
        self.QBut_player.setStyleSheet("background-color:rgb(240, 180, 30)")

        self.game_dimensionality_buttons()

        self.show()

    def mousePressEvent(self, e):
        if type(self.board._players[self.board.turn]) is Player:
            if 75 < e.x() < 75 + (self.board.dimensionality - 1) * 30\
                    and 75 < e.y() < 75 + (self.board.dimensionality - 1) * 30:
                dx = (e.x() - 60) // 30
                dy = (e.y() - 60) // 30
                self.board._players[self.board.turn].set_pressed_position(
                    (dx, dy))

    def game_dimensionality_buttons(self):
        # to change dimentionality to 
        indent = 50
        counter = 0
        for dim in [9, 13, 17, 19]:
            self.dim_settins = QPushButton(str(dim), self)
            self.dim_settins.setGeometry(660 + counter * indent, 385, 30, 30)
            self.font.setPointSize(14)
            self.dim_settins.setFont(self.font)
            self.dim_settins.clicked.connect(
                self.set_dimensionality_method(dim, self.dim_settins))
            self.dim_settins.setStyleSheet(
                "background-color:rgb(176, 176, 63)")
            counter += 1


    def game_hard_buttons(self):
        # to change dimentionality to 
        indent = 50
        counter = 0
        for hard in ['50k', '40k', '20k', '10k']:
            self.hard_settins = QPushButton(str(hard), self)
            self.hard_settins.setGeometry(660 + counter * indent, 465, 30, 30)
            self.font.setPointSize(14)
            self.hard_settins.setFont(self.font)
            self.hard_settins.clicked.connect(
                self._set_hard_method(hard, self.hard_settins))
            self.hard_settins.setStyleSheet(
                "background-color:rgb(176, 176, 63)")
            if counter > 1:
                self.hard_settins.setEnabled(False)
            counter += 1

    def _set_hard_method(self, hard, but):
        def _set():
            if self.last_pressed_but:
                self.last_pressed_but.setEnabled(True)
            but.setEnabled(False)
            self.last_pressed_but = but
            self._ai = GoAI if hard == '50k' else EasyAI
        return _set


    def set_dimensionality_method(self, dim: int, but):
        def _set():
            if self.last_pressed_but:
                self.last_pressed_but.setEnabled(True)
            but.setEnabled(False)
            self.last_pressed_but = but
            self._dimensionality = dim
        return _set

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
        self.board.is_started = True
        threading.Thread(target=self.board.game_update).start()
        self.timer.start(self.timer_interval)

    # region buttons

    def stop(self):
        self.board.is_started = False

    def reset(self):
        self.board.restart(self._dimensionality)

    def pass_move(self):
        self.board.pass_move()

    def change_game_with_two_players(self):
        self.board.restart(self._dimensionality)
        self.board.set_players(Player('Игрок 1', self.board,
                                      StoneSide.BLACK),
                               Player('Игрок 2', self.board,
                                      StoneSide.WHITE))

    def change_game_with_player(self):
        self.board.restart(self._dimensionality)
        self.board.set_players(self._ai('Робот', self.board,
                                    StoneSide.BLACK),
                               Player('Игрок', self.board,
                                      StoneSide.WHITE))

    def change_game_with_no_player(self):
        self.board.restart(self._dimensionality)
        self.board.set_players(self._ai('Виталя', self.board,
                                    StoneSide.BLACK),
                               self._ai('W1354', self.board,
                                    StoneSide.WHITE))

    # endregion

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QColor(155, 88, 19, 200))
        painter.setBackground(Qt.blue)
        # off buttons

        if self.board.get_current_player().is_player:
            self.QBut_pass.setEnabled(True)
        else:
            self.QBut_pass.setEnabled(False)

        if self.board.is_started:
            self.QBut_reset.setEnabled(True)
        else:
            self.QBut_reset.setEnabled(False)
        self.draw_game_place(painter)
        self.draw_board(painter)

    def closeEvent(self, event):
        quit_msg = "Вы точно хотите выйти из игры?"
        reply = QMessageBox.question(self, 'Выход.',
                                           quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.board.is_started = False
            event.accept()
        else:
            event.ignore()

    def draw_game_place(self, painter):
        painter.setBrush(QColor(255, 157, 0))
        painter.drawRect(-1, -1, WINDOW_WIDTH + 1, WINDOW_HIGHT + 1)
        painter.setFont = QFont("Times", 50, QFont.Bold)
        text = 'Ход:' + str(self.board.get_current_player().name)
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
                elif self.board[(x, y)].side == StoneSide.BLACK:
                    StoneQGraphics((x - 0.5, y - 0.5), 'black').paint(painter)
                elif self.board[(x, y)].side == StoneSide.WHITE:
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
