#-*- coding: utf-8
import matplotlib
matplotlib.use("qt4agg")
#matplotlib.rcParams['backend'] = 'Q'
import matplotlib.pyplot as plt
#plt.switch_backend("qt4agg")
import networkx as nx

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4 import QtGui
from Network import Network

class NetworkGenes(FigureCanvas, QtGui.QWidget):
    def __init__(self, modGene, vwGene):
        self.modGene=modGene
        self.vwGene=vwGene
        self.fig, self.axes = plt.subplots()

        self.fig.frameon = False
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.5, bottom=0.05, right=0.98, top=0.98)
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        plt.margins(0.01, 0.005, tight=True)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.axis('off')
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

    def drawNetwork(self):
        nx.draw(self.modGene.G, self.modGene.pos, with_labels=False)
        nx.draw_networkx_labels(self.modGene.G,self.modGene.lpos,self.modGene.labels)

    def updateView(self, hover=None):
        self.axes.clear()
        self.axes.hold(True)
        self.drawNetwork()
        self.vwGene.networkGUI.fig.canvas.draw()
        self.axes.hold(True)
        self.fig.subplots_adjust(left=0.00001, bottom=0.00001, right=0.99999, top=0.99999)
