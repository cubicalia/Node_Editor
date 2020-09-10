from ui.widgets.node_graphics import QDMGraphicsNode
from ui.widgets.content_widgets import QDMNodeContentWidget
from ui.widgets.sockets import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM


class Node():
    def __init__(self, scene, title='Undefined Node', inputs=None, outputs=None):

        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self, self.content)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22

        # inputs
        self.inputs = []
        in_counter = 0
        for item in inputs:
            socket = Socket(node=self, index=in_counter, position=LEFT_BOTTOM, socket_type=item)
            in_counter += 1
            self.inputs.append(socket)
        # Outputs
        self.outputs = []
        out_counter = 0
        for item in outputs:
            socket = Socket(node=self, index=out_counter, position=RIGHT_TOP, socket_type=item)
            out_counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node: > {}".format(hex(id(self)))

    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - index * self.socket_spacing - self.grNode.edge_size - self.grNode.padding
        else:
            y = self.grNode.title_height + self.grNode.padding + self.grNode.edge_size + index * 20
        return [x, y]

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

