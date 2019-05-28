
from client.gui.StoneQGraphics import StoneQGraphics

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem


class BoardQGraphics(QGraphicsItem):
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
                    StoneQGraphics((x - 0.15, y - 0.15),
                                   radius=10).paint(painter)

                # x, y = self.xy
        # colour = QBrush(QColor(self.colour))
        # painter.setBrush(colour)
