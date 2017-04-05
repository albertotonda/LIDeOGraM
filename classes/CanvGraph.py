#-*- coding: utf-8
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as QCanvas
from PyQt4 import QtGui
import networkx as nx
import nx_pylab_angle as nxa
from PyQt4.QtCore import QCoreApplication
import threading
import classes.ClassNode as ClassNode
import classes.ClassMode as ClassMode


class CanvGraph(QCanvas):

    def clicked(self, event):
        (x, y) = (event.xdata, event.ydata)
        if x is None or y is None:
            return

        dst = [(pow(x - pos[0], 2) + pow(y - pos[1], 2), node) for node, pos in
               # compute the distance to each node
               self.nodesPos.items()]
        if self.nodeSelected is not None:
            self.nodeSelected.lineWidth = 1

        if len(list(filter(lambda x: x[0] < 0.002, dst))) == 0 and event.button == 1:
            self.notifyAll()
        elif event.button != 3:
            nodeClicked = min(dst, key=(lambda x: x[0]))[1]
            if self.mode != ClassMode.ClassMode.moveMode:
                self.constructionNode = ClassNode.ClassNode("", [], pos=(x, y), color=(1, 1, 1), size=0)
                self.graph.add_node(self.constructionNode)
                self.graph.add_edge(nodeClicked, self.constructionNode)
                self.nodeSelected = self.constructionNode
            else:
                self.nodeSelected = nodeClicked
            self.notifyAll(self.nodeSelected)#Send to observers the node clicked

    def prepareDrag(self, event):
        self.lastEvent = event
        if not self.onMoveMutex.acquire(False):
            return
        #self.drag(event)
        self.drag(event)

        while self.lastEvent != event:
            event = self.lastEvent
            # print('computing last : ' + str(self.lastEvent))
            #self.drag(event)
            self.drag(event)

        self.onMoveMutex.release()

    def drag(self, event):
        #print(vars(event))
        (x, y) = (event.xdata, event.ydata)
        if not x or not y:
            return
        if (event.inaxes == None):
            return
        #x = (0 if x < 0 else 1 if x > 1 else x)
        #y = (0 if y < 0 else 1 if y > 1 else y)

        if (event.button == 1 and self.nodeSelected is not None):

            self.nodeSelected.pos = (x, y)
            self.paint(self.nodeSelected)
            QCoreApplication.processEvents()

    def release(self, event):
        if self.constructionNode is not None:
            (x, y) = (event.xdata, event.ydata)
            if x is not None and y is not None:
                self.nodesPos.pop(self.constructionNode)
                dst = [(pow(x - pos[0], 2) + pow(y - pos[1], 2), node) for node, pos in self.nodesPos.items()]
                if len(list(filter(lambda x: x[0] < 0.002, dst))) > 0:
                    nIn = self.graph.in_edges(self.constructionNode)[0][0]
                    nOut = min(dst, key=(lambda x: x[0]))[1]
                    if nIn == nOut:
                        self.nodeSelected = nIn
                    elif self.mode == ClassMode.ClassMode.addEdgeMode:
                        self.createEdge(nIn, nOut)
                    elif self.mode == ClassMode.ClassMode.delEdgeMode:
                        self.delEdge(nIn, nOut)
                    self.nodeSelected = nOut
                else:
                    self.nodeSelected = None
            else :
                self.nodeSelected = None
            self.graph.remove_node(self.constructionNode)
            self.constructionNode = None
            self.notifyAll(self.nodeSelected)

    def createEdge(self, nodeIn: ClassNode.ClassNode, nodeOut: ClassNode.ClassNode):
        if self.graph.has_edge(nodeIn, nodeOut):
            msg = QtGui.QMessageBox()
            s = "Invalid action : Edge already exist"
            msg.setText(s)
            msg.setWindowTitle("Edge error")
            msg.exec()
        else:
            self.graph.add_edge(nodeIn, nodeOut)
            if len(list(nx.simple_cycles(self.graph))) > 0:
                self.graph.remove_edge(nodeIn, nodeOut)
                msg = QtGui.QMessageBox()
                s = "Invalid action : The graph become cyclic"
                msg.setText(s)
                msg.setWindowTitle("Edge error")
                msg.exec()

    def delEdge(self, nodeIn: ClassNode.ClassNode, nodeOut: ClassNode.ClassNode):
        if self.graph.has_edge(nodeIn, nodeOut):
            self.graph.remove_edge(nodeIn, nodeOut)
        elif self.graph.has_edge(nodeOut, nodeIn):
            self.graph.remove_edge(nodeOut, nodeIn)
        else:
            msg = QtGui.QMessageBox()
            s = "Invalid action : No edge to remove"
            msg.setText(s)
            msg.setWindowTitle("Edge error")
            msg.exec()

    def __init__(self, graph: nx.DiGraph):
        self.constructionNode = None
        self.onMoveMutex = threading.Lock()
        self.observers = []
        fig, axes = plt.subplots()
        self.fig=fig
        self.mode = ""
        self.nodeSelected = None
        fig.frameon=False
        fig.tight_layout()
        fig.subplots_adjust(left=0.00001, bottom=0.00001, right=0.99999, top=0.99999)

        axes.hold(False)
        fig.patch.set_visible(False)

        QCanvas.__init__(self, fig)

        QCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        QCanvas.updateGeometry(self)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)

        self.graph = graph
        self.axes = axes
        axes.autoscale(False)
        for node in graph.nodes():
            node.pos = (random.random(), random.random())

        self.mpl_connect('button_press_event', self.clicked)
        self.mpl_connect('motion_notify_event', self.prepareDrag)
        self.mpl_connect('button_release_event', self.release)

        self.paint()

    def paint(self, nodeSelected: ClassNode.ClassNode = None):
        self.nodeSelected = nodeSelected
        if nodeSelected:
            nodeSelected.lineWidth = 5
        graph = self.graph
        axes = self.axes
        axes.set_xlim(-0.2, 1.2)
        axes.set_ylim(-0.2, 1.2)

        eBold = []
        eColor = []
        labels = {}
        lineWidths = []
        nodesPos = dict()
        nodesColor = []
        nodesSize = []
        self.nodesPos = nodesPos
        for edge in graph.edges():
            eBold.append(False)
            if edge[1] == self.constructionNode:
                if self.mode == ClassMode.ClassMode.addEdgeMode:
                    eColor.append((0, 0.8, 0))
                elif self.mode == ClassMode.ClassMode.delEdgeMode:
                    eColor.append((0.8, 0, 0))
            else:
                eColor.append((0, 0, 0))
        for node in self.graph.nodes():
            labels[node] = "  " + str(node);
            lineWidths.append(node.lineWidth)
            nodesPos[node] = node.pos
            nodesColor.append(node.color)
            nodesSize.append(node.size)


        nxa.draw_networkx_nodes(graph, nodesPos,
                                node_color=nodesColor,
                                linewidths=lineWidths,
                                linewidthsColors=(0, 0, 0),
                                ax=axes,
                                node_size=nodesSize
                                )

        axes.set_xlim(-0.2, 1.2)
        axes.set_ylim(-0.2, 1.2)

        nxa.draw_networkx_edges(graph,
                                nodesPos,
                                edgelist=graph.edges(),
                                edge_color=eColor,
                                edge_bold=eBold,
                                ax=axes
                                )
        nxa.draw_networkx_labels_angle(graph,
                                       nodesPos,
                                       labels,
                                       ax=axes,
                                       rotate=45
                                       )
        if (random.random() < 0.02):
            a = 5
        self.draw()


    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyAll(self, nodeSelected=None):
        for obs in self.observers:
            obs.notify(nodeSelected)

