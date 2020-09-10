from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsItem


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6.0
        self.outline_width = 1.0
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52E220"),
            QColor("#FF0056A6"),
            QColor("#FFA86DB1"),
            QColor("#FFDBE220"),
            QColor("#FFDBE220"),
            QColor('#FFB54747')
        ]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # Painting the socket circle

        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def boundingRect(self):
        return QRectF(
            -self.radius - self.outline_width,
            -self.radius - self.outline_width,
            2*self.radius + 2*self.outline_width,
            2*self.radius + 2 * self.outline_width,
        )

