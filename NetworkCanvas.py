#-*- coding: utf-8
from sys import path
path.append("fitness/")
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtGui

from Network import Network


class NetworkCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, modApp):

        self.modApp=modApp

        self.fig, self.axes =  plt.subplots()
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.fig.tight_layout()
        self.axes.axis('off')

        self.G=nx.DiGraph()
        self.network = Network(self.modApp, self.G, self.axes, self.fig)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        # TODO : Delete following line ?
        # self.setParent(parent)  def ...(..., parent=None)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        plt.axis('off')
        self.network.update(0.5,0.5)
        self.axes.set_xlim([0, 1.07])
        self.axes.set_ylim([0, 1.07])

    def updateGraph(self,ts,ds):
        self.network.update(ts,ds)

