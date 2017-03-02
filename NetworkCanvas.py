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

        self.fig.frameon=False
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98)
        #self.axes.get_xaxis().set_visible(False)
        #self.axes.get_yaxis().set_visible(False)
        #self.fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

        # We want theaxes cleared every time plot() is called
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        #self.fig.tight_layout()
        #self.fig.tight_layout(pad=0.5)
        #self.fig.figsize=(6,6)
        plt.margins(0.01, 0.005,tight=True)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.axis('off')
        self.network = Network(modApp,vwApp,self.axes,self.fig)


    #def updateView(self):
        #self.axes.set_xlim([0, 1.07])
        #self.axes.set_ylim([0, 1.07])
        #self.network.updateView()
        #self.fig.canvas.draw()

