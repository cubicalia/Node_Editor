from PyQt5.QtGui import QFont, QPainterPath, QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.QtCore import *


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, content, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        # Settings
        self._title_color = Qt.white
        self._title_font = QFont('Ubuntu', 10)
        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 5.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.initTitle()
        self.title = self.node.title

        # initiate the sockets
        self.initSockets()
        # Initiate the content
        self.initContent()
        self.initUI()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.node.updateConnectedEdges()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width - 2*self._padding)

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2*self.edge_size, self.height - 2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)

    def initSockets(self):
        pass

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # Title enclosure
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # Content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # Outline of the node
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    @property
    def padding(self):
        return self._padding
