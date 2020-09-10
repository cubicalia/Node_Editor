from ui.widgets.socket_graphics import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
DEBUG = False


class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.grSocket = QDMGraphicsSocket(self, self.socket_type)
        # print('Creating socket at node: ', self.node.title, 'with param: ', self.index, self.position)

        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    def __str__(self):
        return "<Socket: > {}".format(hex(id(self)))

    def getSocketPositions(self):
        result = self.node.getSocketPosition(self.index, self.position)
        if DEBUG:
            print('SocketPosition: ', result, self.index, self.position, 'Node: ', self.node.title)
        return result

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
