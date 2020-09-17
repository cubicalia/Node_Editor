from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.widgets.edge_graphics import QDMGraphicsEdge, QDMAbstractGraphicsEdge
from ui.widgets.edges import Edge, EDGE_TYPE_BEZIER
from ui.widgets.socket_graphics import QDMGraphicsSocket
from ui.widgets.edge_graphics import QDMGraphicsEdge

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_THRESHOLD = 10

DEBUG = True


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QDMGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # Calculate the zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate the zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoom_step
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoom_step

        # Clamping
        clamped = False
        if self.zoom < self.zoom_range[0]:
            self.zoom, clamped = self.zoom_range[0], True

        if self.zoom > self.zoom_range[1]:
            self.zoom, clamped = self.zoom_range[1], True

        # Set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def middleMouseButtonRelease(self, event):
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        # print(item)         # This is amazing at debugging!! returns the item you are clicking on
        self.init_click_pos = self.mapToScene(event.pos())
        if type(item) is QDMGraphicsSocket:
            # print('Socket was clicked', item)
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return

        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item, QDMAbstractGraphicsEdge): print('DEBUG Edge; ', item.edge, 'connecting: ',
                                                                item.edge.start_socket, '-->',
                                                                item.edge.end_socket)
            if type(item) is QDMGraphicsSocket: print('DEBUG Socket: ', item.socket, 'has edge: ', item.socket.edge)

            if item is None:
                print('DEBUGGER SCENE:')
                print('----Nodes: ')
                for node in self.grScene.scene.nodes: print('         ', node)
                print('----Edges: ')
                for edge in self.grScene.scene.edges: print('         ', edge)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)
        if self.mode == MODE_EDGE_DRAG:
            if self.distance_is_negligeable(event):
                pass
            else:
                res = self.edgeDragEnd(item)
                if res:
                    return

        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()
        super().mouseMoveEvent(event)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG: print('Edge being created')
        if DEBUG: print('----Assigning socket to: ', item.socket)
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, edge_type=EDGE_TYPE_BEZIER)
        if DEBUG: print('Edge Drag started at ', item.socket)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if DEBUG:
                print('-- Socket end assigned', item.socket)
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            if DEBUG:
                print('View::edgeDragEnd ~ Assigned start and end sockets to dragEdge')
            self.dragEdge.updatePositions()
            return True

        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG:
            print('View::edgeDragEnd ~ Done')



        return False

    def distance_is_negligeable(self, event):
        last_click_pos = self.mapToScene(event.pos())
        dist_btw_clicks = last_click_pos - self.init_click_pos
        euclid_dist = dist_btw_clicks.x() ** 2 + dist_btw_clicks.y() ** 2 < EDGE_THRESHOLD ** 2
        return euclid_dist
