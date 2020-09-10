from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.scenes.node_scene import NodeScene
from ui.views.node_graphics_view import QDMGraphicsView
from ui.widgets.edges import Edge, EDGE_TYPE_BEZIER
from ui.widgets.node import Node

DEBUG = False


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.style_sheet_filename = 'ui/qss/nodestyle.qss'
        self.loadStyleSheet(self.style_sheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1000, 1000)
        self.setWindowTitle('Node Editor')

        # LAYOUT
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        # SCENE
        self.scene = NodeScene()
        # self.grScene = self.scene.grScene
        self.addNodes()

        # GRAPHICS
        self.view = QDMGraphicsView(self.scene.grScene, self)
        # RENDER AND SHOW
        self.layout.addWidget(self.view)
        self.show()

        # self.addDebugContent()

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(4)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText('Hello World', QFont('Ubuntu'))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget_1 = QPushButton('Hello World')
        proxy_1 = self.grScene.addWidget(widget_1)
        proxy_1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy_1.setPos(0, 30)

        widget_2 = QTextEdit()
        proxy_2 = self.grScene.addWidget(widget_2)
        proxy_2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy_2.setPos(0, 60)

        line = self.grScene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStyleSheet(self, file_name):
        if DEBUG:
            print('Style loading: {}'.format(str(file_name)))
        file = QFile(file_name)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def addNodes(self):
        # Node instances
        node1 = Node(self.scene, 'My Awesome Node 1', inputs=[0, 2, 3], outputs=[1])
        node2 = Node(self.scene, 'My Awesome Node 2', inputs=[0, 4, 3], outputs=[1])
        node3 = Node(self.scene, 'My Awesome Node 3', inputs=[0, 0, 2], outputs=[1])
        # Node positions
        node1.setPos(-350, -200)
        node2.setPos(0, 0)
        node3.setPos(250, 100)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[1], edge_type=EDGE_TYPE_BEZIER)
