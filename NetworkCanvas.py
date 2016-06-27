#-*- coding: utf-8
from sys import path
path.append("fitness/")
import matplotlib
matplotlib.use("qt4agg")
#matplotlib.rcParams['backend'] = 'Q'
import matplotlib.pyplot as plt
#plt.switch_backend("qt4agg")

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4 import QtGui
from Network import Network

# TODO Change la couleur des "edges" lorsque l'on déplace le slider
class NetworkCanvas(FigureCanvas):
    def __init__(self, modApp, vwApp):
        self.modApp=modApp
        self.vwApp=vwApp
        self.fig, self.axes =  plt.subplots()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.fig.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.axis('off')
        self.network = Network(modApp,vwApp,self.axes)


    def updateView(self):
        self.axes.set_xlim([0, 1.07])
        self.axes.set_ylim([0, 1.07])
        self.network.updateView()
        self.fig.canvas.draw()

