#-*- coding: utf-8
from sys import path
import matplotlib
matplotlib.use('qt4agg')

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtGui

from Network import Network


class NetworkCanvas(FigureCanvas):
    def __init__(self, modApp):
        self.modApp=modApp
        self.fig, self.axes =  plt.subplots()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.fig.tight_layout()
        self.axes.axis('off')
        self.network = Network(self.modApp, self.axes)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateView(self):
        self.network.updateView()
        self.axes.set_xlim([0, 1.07])
        self.axes.set_ylim([0, 1.07])
        self.fig.canvas.draw()

