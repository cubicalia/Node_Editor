from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QPen
import math


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        # Settings
        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor("#292929")

        self.gridSize = 20
        self.gridSquares = 5

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # Brackground
        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rectangle):
        super().drawBackground(painter, rectangle)
        # Creating the grid
        left = int(math.floor(rectangle.left()))
        right = int(math.ceil(rectangle.right()))
        top = int(math.floor(rectangle.top()))
        bottom = int(math.ceil(rectangle.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # Computing the lines to be drawn
        lines_light = []
        lines_dark = []
        for x_line in range(first_left, right, self.gridSize):
            if x_line % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x_line, top, x_line, bottom))
            else:
                lines_dark.append(QLine(x_line, top, x_line, bottom))
        for v_line in range(first_top, bottom, self.gridSize):
            if v_line % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, v_line, right, v_line))
            else:
                lines_dark.append(QLine(left, v_line, right, v_line))

        # Draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)
