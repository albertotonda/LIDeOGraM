#-*- coding: utf-8
from sys import path
path.append("fitness/")
import fitness
import networkx as nx
from RFGraph_Model import RFGraph_Model
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtGui

import network

curr_tabl=[]


class RFGraphCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, modApp, parent=None, width=5, height=4, dpi=100):
        self.modApp=modApp
        self.fig, self.axes =  plt.subplots()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.fig.patch.set_visible(False)
        self.fig.tight_layout()
        self.axes.axis('off')
        self.axes.set_xlim([0,0.1])
        self.axes.set_ylim([0, 0.6])
        self.G=nx.DiGraph()
        self.pos=self.modApp.pos_graph()

        self.network = network.network(self.modApp,self.G, self.axes, self.fig, self.pos)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        plt.axis('off')
        self.network.update(0.5,0.5)
        self.axes.set_xlim([0, 1.07])
        self.axes.set_ylim([0, 1.07])

    def updateGraph(self,ts,ds):
        self.network.update(ts,ds)

