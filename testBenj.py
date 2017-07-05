from PyQt4 import QtGui, QtCore
#from classes.CanvGraph import CanvGraph
import networkx as nx
import matplotlib.pyplot as plt
import copy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as QCanvas


class Window(QtGui.QMainWindow):

   def __init__(self, modApp):
       QtGui.QMainWindow.__init__(self)
       mainWid = QtGui.QWidget(self)
       self.gridLayout = QtGui.QGridLayout(mainWid)
       mainWid.setFocus()
       self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
       self.setWindowState(QtCore.Qt.WindowMaximized)

       fig = plt.figure("Classes")
       fig.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98)

       plt.margins(0.01, 0.005,tight=True)

       label = {}
       for i in range(5):
           label[i] = i

       nx.draw(modApp.G, style="dashed", node_color="blue", labels=label, font_color='r')

       self.modApp = modApp
       canv = QCanvas(fig)
       QCanvas.setSizePolicy(canv, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
       #canv.setMinimumSize(200, 200)
       cb = QtGui.QComboBox()
       cb.addItem("1")
       cb.addItem("2")
       cb.addItem("3")
       cb.addItem("4")

       #self.gridLayout.addWidget(CanvGraph(), 0, 0, 1, 1)
       #self.gridLayout.addWidget(CanvGraph
       self.gridLayout.setSpacing(5)
       self.gridLayout.addWidget(canv, 0, 0, 1, 1)
       self.gridLayout.addWidget(cb, 1, 0)
       self.gridLayout.addWidget(canv, 2, 2)
       #self.gridLayout.addWidget(canv, 2, 2, -1, -1)


       self.setCentralWidget(mainWid)
       QtGui.QMainWindow.show(self)
       #plt.show()
       print("end")

import networkx as nx
import numpy as np

class ClassesModel:
   def __init__(self):
       self.G = None
       self.initGraph()

   def initGraph(self):
       self.G = nx.DiGraph()

       self.G.add_nodes_from(range(5))
       self.G.add_edge(1, 2)
       self.G.add_edge(2, 3)
       self.G.add_edge(1, 3)
       self.G.add_edge(3, 4)
       self.G.add_edge(3, 0)
#-*- coding: utf-8


#from ClassesView import ClassesView

from RFGraph_Controller import RFGraph_Controller
from QtConnector import QtConnector
import sys
from PyQt4 import QtGui


modApp=ClassesModel()
qApp = QtGui.QApplication(sys.argv)
vwApp = Window(modApp)
#cntrApp=RFGraph_Controller(modApp,vwApp)
#vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#QtConnector(vwApp, cntrApp)
sys.exit(qApp.exec_())