#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QCoreApplication
from classes.CanvGraph import CanvGraph
from classes.FramAction import FramAction
from classes.ClassGraph import ClassGraph
from classes.MenuBar import MenuBar

import matplotlib.pyplot as plt
import copy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as QCanvas


class Window(QtGui.QMainWindow):

    def __init__(self, graph: ClassGraph):
        QtGui.QMainWindow.__init__(self)
        mainWid = QtGui.QWidget(self)
        self.setWindowTitle("Class management")
        self.gridLayout = QtGui.QGridLayout(mainWid)
        mainWid.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setCentralWidget(mainWid)

        self.graph = graph

        self.canv = CanvGraph(graph)
        self.canv.addObserver(self)
        self.frame = FramAction(graph.unboundNode)

        self.frame.button1.addObserver(self)
        self.frame.button2.addObserver(self)

        self.gridLayout.setSpacing(5)
        self.canv.setMinimumSize(200, 200)

        self.gridLayout.addWidget(self.canv, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 1)
        self.selectedNode = None
        MenuBar(self)



        QtGui.QMainWindow.show(self)

    def notify(self, selectedNode=None, keepSelected = False):
        if keepSelected:
            selectedNode = self.selectedNode
        else:
            self.selectedNode = selectedNode
        self.canv.paint(selectedNode)
        self.frame.setListsValues(self.graph.unboundNode, selectedNode)
        QCoreApplication.processEvents()

