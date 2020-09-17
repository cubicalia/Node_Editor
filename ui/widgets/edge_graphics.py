from PyQt5.QtGui import QPen, QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem
from PyQt5.QtCore import Qt, QPointF


class QDMAbstractGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self._color = QColor('#001000')
        self._color_selected = QColor('#00FF00')
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidth(3)
        self._pen_selected.setWidth(3)
        self._pen_dragging.setWidth(3)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.edge = edge

    def __str__(self):
        return "<Edge: > {}".format(hex(id(self)))

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        raise NotImplemented('This method has to be overridden in a child class')


class QDMGraphicsEdge(QDMAbstractGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMAbstractGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = abs((d[0] - s[0]) / 2)

        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(s[0] + dist,
                     s[1],
                     d[0] - dist,
                     d[1],
                     d[0],
                     d[1])
        self.setPath(path)