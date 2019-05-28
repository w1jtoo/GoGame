import sys

from client.API.application import MyApp
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    window.start()
    sys.exit(app.exec_())




""" 
TODO созать таймер игровой логики
создать класс игры и запускать его лупу (вместе с ботами)
удалить треды для ИИ
"""

