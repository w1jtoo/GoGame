from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem


class StoneQGraphics(QGraphicsItem):
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
